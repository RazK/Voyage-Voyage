"""OAuth credentials model."""
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class OAuthCredential(Base):
    """OAuth credentials model for storing encrypted refresh tokens."""

    __tablename__ = "oauth_credentials"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    provider = Column(String(50), primary_key=True, default="google")
    refresh_token = Column(Text, nullable=False)  # Encrypted
    expires_at = Column(DateTime(timezone=True), nullable=True)
    scopes = Column(ARRAY(Text), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationship
    user = relationship("User", backref="oauth_credentials")

    def __repr__(self) -> str:
        return f"<OAuthCredential(user_id={self.user_id}, provider={self.provider})>"


