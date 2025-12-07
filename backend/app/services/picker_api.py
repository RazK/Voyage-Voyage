"""Google Photos Picker API service."""
from typing import Optional
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from app.core.config import settings
from app.core.encryption import decrypt_token
from app.core.oauth import refresh_access_token, OAuthError
from app.models import User, OAuthCredential
from sqlalchemy.orm import Session

PICKER_API_BASE = "https://photospicker.googleapis.com/v1"


class PickerAPIError(Exception):
    """Raised when Picker API operations fail."""

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
        PickerAPIError: If credentials are missing or refresh fails.
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
        raise PickerAPIError("User has no OAuth credentials")

    # Decrypt refresh token
    try:
        refresh_token = decrypt_token(oauth_cred.refresh_token)
    except Exception as e:
        raise PickerAPIError(f"Failed to decrypt refresh token: {e}") from e

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
        raise PickerAPIError(f"Failed to refresh credentials: {e}") from e


def create_picker_session(user: User, db: Session) -> dict:
    """
    Create a new Picker API session.

    Args:
        user: User model instance.
        db: Database session.

    Returns:
        Dict with session_id and pickerUri.

    Raises:
        PickerAPIError: If session creation fails.
    """
    credentials = get_user_credentials(user, db)

    # Get access token
    if not credentials.valid:
        request = Request()
        credentials.refresh(request)

    url = f"{PICKER_API_BASE}/sessions"
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
    }

    try:
        # Picker API CreateSession doesn't require a request body
        response = requests.post(url, headers=headers, json={}, timeout=30)
        response.raise_for_status()

        data = response.json()

        return {
            "sessionId": data.get("id"),  # API returns "id", not "sessionId"
            "pickerUri": data.get("pickerUri"),
        }
    except requests.exceptions.RequestException as e:
        raise PickerAPIError(f"Picker API error: {e}") from e
    except Exception as e:
        raise PickerAPIError(f"Failed to create picker session: {e}") from e


def get_picker_session_status(user: User, db: Session, session_id: str) -> dict:
    """
    Get the status of a Picker API session.

    Args:
        user: User model instance.
        db: Database session.
        session_id: Picker session ID.

    Returns:
        Dict with session status information.

    Raises:
        PickerAPIError: If status check fails.
    """
    credentials = get_user_credentials(user, db)

    # Get access token
    if not credentials.valid:
        request = Request()
        credentials.refresh(request)

    url = f"{PICKER_API_BASE}/sessions/{session_id}"
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        return {
            "sessionId": data.get("id"),  # API returns "id", not "sessionId"
            "mediaItemsSet": data.get("mediaItemsSet", False),
            "state": data.get("state"),  # PENDING, ACTIVE, COMPLETED, EXPIRED
        }
    except requests.exceptions.RequestException as e:
        raise PickerAPIError(f"Picker API error: {e}") from e
    except Exception as e:
        raise PickerAPIError(f"Failed to get session status: {e}") from e


def get_picker_session_items(
    user: User, db: Session, session_id: str, page_token: Optional[str] = None
) -> dict:
    """
    Get media items selected in a Picker API session.

    Args:
        user: User model instance.
        db: Database session.
        session_id: Picker session ID.
        page_token: Optional page token for pagination.

    Returns:
        Dict with mediaItems list and optional nextPageToken.

    Raises:
        PickerAPIError: If fetching items fails.
    """
    credentials = get_user_credentials(user, db)

    # Get access token
    if not credentials.valid:
        request = Request()
        credentials.refresh(request)

    # Picker API: GET /v1/mediaItems?sessionId={sessionId}
    # sessionId must be a query parameter, not in the path
    url = f"{PICKER_API_BASE}/mediaItems"
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
    }
    params = {
        "sessionId": session_id,  # Required: sessionId as query param
        "pageSize": 50,
    }
    if page_token:
        params["pageToken"] = page_token

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        response.raise_for_status()

        data = response.json()

        # Transform to our API format
        # Picker API structure: item.mediaFile.baseUrl, item.mediaFile.mimeType, etc.
        # Note: baseUrl needs =d parameter appended for full resolution download
        media_items = []
        for item in data.get("mediaItems", []):
            media_file = item.get("mediaFile", {})
            base_url = media_file.get("baseUrl", "")
            # Append =d for full resolution download (or =wXXX-hYYY for specific dimensions)
            # If already has parameters, don't add =d
            if base_url and "=" not in base_url:
                base_url = base_url + "=d"
            
            media_items.append(
                {
                    "id": item.get("id"),
                    "filename": media_file.get("filename", ""),
                    "mimeType": media_file.get("mimeType", ""),
                    "mediaMetadata": media_file.get("mediaFileMetadata", {}),
                    "baseUrl": base_url,  # Now includes =d for full resolution
                    "type": item.get("type", ""),  # PHOTO or VIDEO
                    "createTime": item.get("createTime", ""),
                }
            )

        return {
            "mediaItems": media_items,
            "nextPageToken": data.get("nextPageToken"),
        }
    except requests.exceptions.RequestException as e:
        raise PickerAPIError(f"Picker API error: {e}") from e
    except Exception as e:
        raise PickerAPIError(f"Failed to get session items: {e}") from e

