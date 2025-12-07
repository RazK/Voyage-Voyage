"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.core.encryption import encrypt_token
from app.core.jwt import create_access_token
from app.core.oauth import (
    OAuthError,
    exchange_code_for_tokens,
    get_authorization_url,
    generate_state_token,
)
from app.models import User, OAuthCredential

router = APIRouter()


@router.get("/google/start")
async def google_oauth_start():
    """
    Start Google OAuth flow.

    Returns:
        JSON with authorization URL and state token.
    """
    try:
        state = generate_state_token()
        auth_url = get_authorization_url(state)

        return {"auth_url": auth_url, "state": state}
    except OAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth configuration error: {str(e)}",
        ) from e


@router.get("/google/callback")
async def google_oauth_callback(
    code: str = Query(..., description="Authorization code from Google"),
    state: str = Query(None, description="State token for CSRF protection"),
    db: Session = Depends(get_db),
):
    """
    Handle Google OAuth callback.

    Exchanges authorization code for tokens, creates/updates user,
    and returns JWT token.
    """
    try:
        # Exchange code for tokens
        credentials, user_info = exchange_code_for_tokens(code)

        if not user_info.get("email") or not user_info.get("google_user_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing email or user ID in OAuth response",
            )

        email = user_info["email"]
        google_user_id = user_info["google_user_id"]

        # Find or create user
        user = db.query(User).filter(User.google_user_id == google_user_id).first()

        if not user:
            user = User(
                google_user_id=google_user_id,
                email=email,
            )
            db.add(user)
            db.flush()  # Get user.id
        else:
            # Update email if changed
            if user.email != email:
                user.email = email

        # Store or update OAuth credentials
        refresh_token_encrypted = encrypt_token(credentials.refresh_token)

        oauth_cred = (
            db.query(OAuthCredential)
            .filter(
                OAuthCredential.user_id == user.id,
                OAuthCredential.provider == "google",
            )
            .first()
        )

        if oauth_cred:
            # Update existing credentials
            oauth_cred.refresh_token = refresh_token_encrypted
            oauth_cred.scopes = credentials.scopes or []
            oauth_cred.expires_at = credentials.expiry
        else:
            # Create new credentials
            oauth_cred = OAuthCredential(
                user_id=user.id,
                provider="google",
                refresh_token=refresh_token_encrypted,
                scopes=credentials.scopes or [],
                expires_at=credentials.expiry,
            )
            db.add(oauth_cred)

        db.commit()

        # Generate JWT token
        jwt_token = create_access_token(user.id, user.email)

        return {
            "user": {
                "id": str(user.id),
                "email": user.email,
            },
            "token": jwt_token,
        }

    except OAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth error: {str(e)}",
        ) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}",
        ) from e


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.

    Returns:
        User information.
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
    }

