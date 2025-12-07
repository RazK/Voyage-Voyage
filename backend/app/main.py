"""Main FastAPI application entry point."""
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.routing import APIRouter

from app.api import auth, picker

app = FastAPI(
    title="Voyage Voyage",
    description="Transform messy Google Photos trip albums into clean, cinematic, curated experiences",
    version="0.1.0",
)

# API router with /api prefix
api_router = APIRouter(prefix="/api")


@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "time": datetime.now(timezone.utc).isoformat(),
    }


# Include auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include picker routes
api_router.include_router(picker.router, prefix="/photos/picker", tags=["picker"])

app.include_router(api_router)

