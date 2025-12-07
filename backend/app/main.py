"""Main FastAPI application entry point."""
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.routing import APIRouter

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


app.include_router(api_router)

