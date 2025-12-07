"""Application configuration."""
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Google OAuth
    google_client_id: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = os.getenv(
        "GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback"
    )

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql://voyage:voyage@localhost:5433/voyage"
    )

    # JWT and Encryption
    jwt_secret: Optional[str] = os.getenv("JWT_SECRET")
    token_encryption_key: Optional[str] = os.getenv("TOKEN_ENCRYPTION_KEY")

    # Enhancement APIs
    enhancement_api_key: Optional[str] = os.getenv("ENHANCEMENT_API_KEY")
    restyle_api_key: Optional[str] = os.getenv("RESTYLE_API_KEY")

    # GCP
    temp_bucket_name: str = os.getenv("TEMP_BUCKET_NAME", "voyage-temp-dev")
    gcp_project_id: Optional[str] = os.getenv("GCP_PROJECT_ID")


settings = Settings()

