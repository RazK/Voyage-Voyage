"""API routers for Voyage Voyage."""

from fastapi import APIRouter

from .routes import health


api_router = APIRouter()
api_router.include_router(health.router, prefix="/api")

__all__ = ["api_router"]
