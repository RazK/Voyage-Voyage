"""OAuth state token utilities."""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models.oauth_state import OAuthState, STATE_TOKEN_EXPIRY_MINUTES


def cleanup_expired_state_tokens(db: Session) -> int:
    """
    Clean up expired OAuth state tokens from the database.

    Args:
        db: Database session.

    Returns:
        Number of tokens deleted.
    """
    expiry_threshold = datetime.now(timezone.utc) - timedelta(minutes=STATE_TOKEN_EXPIRY_MINUTES)
    
    expired_tokens = db.query(OAuthState).filter(
        OAuthState.created_at < expiry_threshold
    ).all()
    
    count = len(expired_tokens)
    for token in expired_tokens:
        db.delete(token)
    
    if count > 0:
        db.commit()
    
    return count
