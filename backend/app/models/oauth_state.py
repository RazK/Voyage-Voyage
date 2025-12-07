"""OAuth state token model for CSRF protection."""
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, DateTime, Index, String, Text

from app.core.database import Base

# State tokens expire after 10 minutes
STATE_TOKEN_EXPIRY_MINUTES = 10


class OAuthState(Base):
    """OAuth state token model for CSRF protection."""

    __tablename__ = "oauth_states"

    state_token = Column(Text, primary_key=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        Index("ix_oauth_states_created_at", "created_at"),
    )

    def is_expired(self) -> bool:
        """
        Check if the state token has expired.

        Returns:
            True if expired, False otherwise.
        """
        expiry_time = self.created_at + timedelta(minutes=STATE_TOKEN_EXPIRY_MINUTES)
        return datetime.now(timezone.utc) > expiry_time

    def __repr__(self) -> str:
        return f"<OAuthState(state_token={self.state_token[:16]}..., created_at={self.created_at})>"
