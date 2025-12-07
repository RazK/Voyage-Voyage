"""FastAPI entrypoint for Voyage Voyage."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api import api_router
from app.core.config import get_settings, settings_summary


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Run startup/shutdown hooks."""
    settings = get_settings()
    # Log a minimal startup summary for observability without leaking secrets.
    print(f"[startup] environment={settings.environment}")  # noqa: T201
    yield
    print("[shutdown] application stopped")  # noqa: T201


app = FastAPI(title="Voyage Voyage API", lifespan=lifespan)


@app.get("/api/config", tags=["health"])
async def get_config_summary() -> dict[str, str]:
    """Expose a sanitized configuration summary for troubleshooting."""
    return settings_summary()


app.include_router(api_router)
