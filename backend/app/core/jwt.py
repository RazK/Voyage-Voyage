"""JWT token utilities."""
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from jose import JWTError as JoseJWTError, jwt

from app.core.config import settings

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24 * 7  # 7 days


class JWTError(Exception):
    """Raised when JWT operations fail."""

    pass


def create_access_token(user_id: UUID, email: str) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User UUID.
        email: User email.

    Returns:
        Encoded JWT token string.

    Raises:
        JWTError: If JWT_SECRET is not configured.
    """
    if not settings.jwt_secret:
        raise JWTError("JWT_SECRET must be set in environment variables")

    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    to_encode = {
        "sub": str(user_id),  # Subject (user ID)
        "email": email,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string.

    Returns:
        Decoded token payload (dict with sub, email, exp, iat).

    Raises:
        JWTError: If token is invalid or expired.
    """
    if not settings.jwt_secret:
        raise JWTError("JWT_SECRET must be set in environment variables")

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except JoseJWTError as e:
        raise JWTError(f"Invalid token: {e}") from e


def get_user_id_from_token(token: str) -> UUID:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string.

    Returns:
        User UUID.

    Raises:
        JWTError: If token is invalid or user_id is missing.
    """
    payload = decode_access_token(token)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise JWTError("Token missing user ID (sub)")

    try:
        return UUID(user_id_str)
    except ValueError as e:
        raise JWTError(f"Invalid user ID format in token: {e}") from e

