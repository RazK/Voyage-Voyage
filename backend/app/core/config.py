"""Application configuration settings."""

from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Base application settings loaded from environment."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Voyage Voyage"
    environment: str = "local"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/voyage"
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/auth/google/callback"
    jwt_secret: str = ""
    token_encryption_key: str = ""
    enhancement_api_key: str = ""
    restyle_api_key: str = ""
    temp_bucket_name: str = "voyage-temp-dev"
    gcp_project_id: str = ""


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()


def settings_summary() -> dict[str, Any]:
    """Expose a non-sensitive subset of settings for diagnostics."""
    settings = get_settings()
    return {
        "environment": settings.environment,
        "temp_bucket_name": settings.temp_bucket_name,
        "gcp_project_id": settings.gcp_project_id,
    }
