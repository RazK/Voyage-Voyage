"""Google OAuth utilities."""
import secrets
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

from app.core.config import settings


# Google Photos API scopes
# Picker API requires photospicker.mediaitems.readonly scope
# Library API appendonly + readonly.appcreateddata for creating/managing curated albums (output)
GOOGLE_PHOTOS_SCOPES = [
    "https://www.googleapis.com/auth/photospicker.mediaitems.readonly",  # Required for Picker API
    "https://www.googleapis.com/auth/photoslibrary.appendonly",  # Create albums and upload photos
    "https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata",  # Read app-created albums
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


class OAuthError(Exception):
    """Raised when OAuth operations fail."""

    pass


def create_oauth_flow() -> Flow:
    """
    Create Google OAuth flow.

    Returns:
        Configured OAuth flow instance.

    Raises:
        OAuthError: If OAuth configuration is invalid.
    """
    if not settings.google_client_id or not settings.google_client_secret:
        raise OAuthError("Google OAuth credentials not configured")

    client_config = {
        "web": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.google_redirect_uri],
        }
    }

    return Flow.from_client_config(
        client_config,
        scopes=GOOGLE_PHOTOS_SCOPES,
        redirect_uri=settings.google_redirect_uri,
    )


def generate_state_token() -> str:
    """Generate a secure random state token for OAuth."""
    return secrets.token_urlsafe(32)


def get_authorization_url(state: Optional[str] = None) -> str:
    """
    Get Google OAuth authorization URL.

    Args:
        state: Optional state token for CSRF protection. If None, generates one.

    Returns:
        Authorization URL.
    """
    flow = create_oauth_flow()
    if state is None:
        state = generate_state_token()

    authorization_url, _ = flow.authorization_url(
        access_type="offline",  # Request refresh token
        include_granted_scopes="true",
        state=state,
        prompt="consent",  # Force consent screen to ensure refresh token
    )

    return authorization_url


def exchange_code_for_tokens(code: str) -> tuple[Credentials, dict]:
    """
    Exchange authorization code for OAuth tokens.

    Args:
        code: Authorization code from Google.

    Returns:
        Tuple of (Credentials object, user info dict with email and sub).

    Raises:
        OAuthError: If token exchange fails.
    """
    try:
        # Manually exchange code to avoid scope validation issues
        # Google may return additional scopes (e.g., readonly/appendonly when requesting photoslibrary)
        import requests
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        if not token_response.ok:
            try:
                error_detail = token_response.json()
            except:
                error_detail = token_response.text
            raise OAuthError(f"Token exchange failed ({token_response.status_code}): {error_detail}")
        
        token_data = token_response.json()
        
        from google.oauth2.credentials import Credentials
        granted_scopes = token_data.get("scope", "").split() if token_data.get("scope") else None
        credentials = Credentials(
            token=token_data.get("access_token"),
            refresh_token=token_data.get("refresh_token"),
            id_token=token_data.get("id_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            scopes=granted_scopes,
        )

        # Get user info
        from google.oauth2 import id_token

        request = Request()
        # Use id_token from credentials (either from flow or manual exchange)
        id_token_str = credentials.id_token if hasattr(credentials, 'id_token') and credentials.id_token else None
        if not id_token_str:
            # Fallback: get user info from userinfo endpoint if no ID token
            import requests
            userinfo_response = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {credentials.token}"}
            )
            userinfo_response.raise_for_status()
            userinfo = userinfo_response.json()
            id_info = {
                "email": userinfo.get("email"),
                "sub": userinfo.get("id"),
                "name": userinfo.get("name"),
            }
        else:
            id_info = id_token.verify_oauth2_token(
                id_token_str, request, settings.google_client_id
            )

        user_info = {
            "email": id_info.get("email"),
            "google_user_id": id_info.get("sub"),
            "name": id_info.get("name"),
        }

        return credentials, user_info
    except Exception as e:
        raise OAuthError(f"Failed to exchange code for tokens: {e}") from e


def refresh_access_token(refresh_token: str) -> Credentials:
    """
    Refresh an access token using a refresh token.

    Args:
        refresh_token: The refresh token (encrypted in storage, should be decrypted).

    Returns:
        New Credentials object with refreshed access token.

    Raises:
        OAuthError: If token refresh fails.
    """
    try:
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
        )

        request = Request()
        credentials.refresh(request)

        return credentials
    except Exception as e:
        raise OAuthError(f"Failed to refresh access token: {e}") from e

