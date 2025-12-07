"""Google Photos API service."""
from typing import Optional
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from app.core.config import settings
from app.core.encryption import decrypt_token
from app.core.oauth import refresh_access_token, OAuthError
from app.models import User, OAuthCredential
from sqlalchemy.orm import Session

GOOGLE_PHOTOS_API_BASE = "https://photoslibrary.googleapis.com/v1"


class GooglePhotosError(Exception):
    """Raised when Google Photos API operations fail."""

    pass


def get_user_credentials(user: User, db: Session) -> Credentials:
    """
    Get valid OAuth credentials for a user, refreshing if necessary.

    Args:
        user: User model instance.
        db: Database session.

    Returns:
        Valid Credentials object.

    Raises:
        GooglePhotosError: If credentials are missing or refresh fails.
    """
    oauth_cred = (
        db.query(OAuthCredential)
        .filter(
            OAuthCredential.user_id == user.id,
            OAuthCredential.provider == "google",
        )
        .first()
    )

    if not oauth_cred:
        raise GooglePhotosError("User has no OAuth credentials")

    # Decrypt refresh token
    try:
        refresh_token = decrypt_token(oauth_cred.refresh_token)
    except Exception as e:
        raise GooglePhotosError(f"Failed to decrypt refresh token: {e}") from e

    # Refresh credentials
    try:
        credentials = refresh_access_token(refresh_token)

        # Update stored credentials if token changed
        if credentials.refresh_token and credentials.refresh_token != refresh_token:
            from app.core.encryption import encrypt_token

            oauth_cred.refresh_token = encrypt_token(credentials.refresh_token)
            oauth_cred.expires_at = credentials.expiry
            db.commit()

        return credentials
    except OAuthError as e:
        raise GooglePhotosError(f"Failed to refresh credentials: {e}") from e


def list_albums(user: User, db: Session, page_token: Optional[str] = None) -> dict:
    """
    List user's Google Photos albums.

    Args:
        user: User model instance.
        db: Database session.
        page_token: Optional page token for pagination.

    Returns:
        Dict with 'albums' list and optional 'nextPageToken'.

    Raises:
        GooglePhotosError: If API call fails.
    """
    credentials = get_user_credentials(user, db)

    # Get access token
    if not credentials.valid:
        request = Request()
        credentials.refresh(request)

    url = f"{GOOGLE_PHOTOS_API_BASE}/albums"
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
    }
    params = {
        "pageSize": 50,
    }
    if page_token:
        params["pageToken"] = page_token

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Transform to our API format
        albums = []
        for album in data.get("albums", []):
            albums.append(
                {
                    "id": album.get("id"),
                    "title": album.get("title", ""),
                    "mediaItemCount": int(album.get("mediaItemsCount", 0)),
                    "productUrl": album.get("productUrl", ""),
                }
            )

        return {
            "albums": albums,
            "nextPageToken": data.get("nextPageToken"),
        }
    except requests.exceptions.RequestException as e:
        raise GooglePhotosError(f"Google Photos API error: {e}") from e
    except Exception as e:
        raise GooglePhotosError(f"Failed to list albums: {e}") from e

