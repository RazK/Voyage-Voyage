"""Photos Picker API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.models import User
from app.services.picker_api import PickerAPIError, create_picker_session, get_picker_session_status, get_picker_session_items

router = APIRouter()


@router.post("/session")
async def create_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new Google Photos Picker session.

    Returns:
        Dict with sessionId and pickerUri.
        The user should visit pickerUri to select photos.
    """
    try:
        result = create_picker_session(current_user, db)
        return result
    except PickerAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create picker session: {str(e)}",
        ) from e


@router.get("/session/{session_id}")
async def get_session_status(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get the status of a Picker API session.

    Returns:
        Dict with sessionId, mediaItemsSet (bool), and state.
    """
    try:
        result = get_picker_session_status(current_user, db, session_id)
        return result
    except PickerAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session status: {str(e)}",
        ) from e


@router.get("/session/{session_id}/items")
async def get_session_items(
    session_id: str,
    page_token: str | None = Query(None, description="Page token for pagination"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get media items selected in a Picker API session.

    Returns:
        Dict with mediaItems list and optional nextPageToken.
    """
    try:
        result = get_picker_session_items(current_user, db, session_id, page_token=page_token)
        return result
    except PickerAPIError as e:
        # 404 if items not available yet (user hasn't selected)
        status_code = status.HTTP_404_NOT_FOUND if "Media items not available yet" in str(e) else status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=f"Failed to get session items: {str(e)}",
        ) from e

