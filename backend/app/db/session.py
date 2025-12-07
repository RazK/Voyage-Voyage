"""Database session management."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def _build_engine():
    settings = get_settings()
    return create_engine(settings.database_url, pool_pre_ping=True)


engine = _build_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)

SessionDependency = Generator[Session, None, None]


def get_session() -> SessionDependency:
    """Provide a SQLAlchemy session dependency."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
