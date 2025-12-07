"""Health check endpoint."""

from datetime import datetime, timezone

from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/health")
async def get_health() -> dict[str, str]:
    """Return service health metadata."""
    return {"status": "ok", "time": datetime.now(tz=timezone.utc).isoformat()}
