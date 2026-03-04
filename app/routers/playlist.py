"""Playlist migration routes."""
import logging
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from datetime import datetime, timedelta

from app.models import (
    MigrationRequest,
    MigrationStatus,
    LogEvent,
)
from app.dependencies import get_current_user
from app.services.playlist_converter import PlaylistConverter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/migrate", tags=["migration"])

# Store active migrations (in production, use database or Redis)
# Format: {job_id: {"status": MigrationStatus, "logs": [LogEvent], "created_at": datetime}}
_active_migrations = {}


def _cleanup_old_migrations():
    """Remove migrations older than 1 hour."""
    now = datetime.utcnow()
    expired_jobs = [
        job_id for job_id, data in _active_migrations.items()
        if now - data.get("created_at", now) > timedelta(hours=1)
    ]
    for job_id in expired_jobs:
        del _active_migrations[job_id]


@router.post("/")
async def start_migration(
    request: MigrationRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Start a new playlist migration job.
    
    Args:
        request: Migration request with Yandex playlist URL
        current_user: Authenticated user from Spotify token
        
    Returns:
        Job ID for tracking the migration
    """
    # Clean up old migrations
    _cleanup_old_migrations()
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Initialize migration state
    _active_migrations[job_id] = {
        "status": MigrationStatus(
            status="pending",
            progress=0,
            total=0,
            message="Initializing migration...",
        ),
        "logs": [],
        "created_at": datetime.utcnow(),
    }
    
    logger.info(f"Started migration job {job_id} for user {current_user['user_id']}")
    
    # Start background migration (async generator)
    # In production, use a task queue like Celery
    async def _run_migration():
        try:
            converter = PlaylistConverter(current_user["access_token"])
            
            async for event_type, event_data in converter.convert_playlist(request.yandex_playlist_url):
                if event_type == "log":
                    log_event = LogEvent(
                        level=event_data["level"],
                        message=event_data["message"],
                    )
                    _active_migrations[job_id]["logs"].append(log_event)
                    logger.log(
                        level=logging.getLevelName(event_data["level"].upper()),
                        msg=event_data["message"],
                    )
                
                elif event_type == "progress":
                    _active_migrations[job_id]["status"].progress = event_data["found"]
                    _active_migrations[job_id]["status"].total = event_data["total"]
                
                elif event_type == "complete":
                    _active_migrations[job_id]["status"].status = "complete"
                    _active_migrations[job_id]["status"].playlist_id = event_data["playlist_id"]
                    _active_migrations[job_id]["status"].playlist_url = event_data["playlist_url"]
                    _active_migrations[job_id]["status"].message = (
                        f"Successfully created playlist '{event_data['playlist_name']}' "
                        f"with {event_data['total_added']} tracks"
                    )
                
                elif event_type == "error":
                    _active_migrations[job_id]["status"].status = "error"
                    _active_migrations[job_id]["status"].message = event_data["message"]
        
        except Exception as e:
            logger.error(f"Migration job {job_id} failed with error: {e}", exc_info=True)
            _active_migrations[job_id]["status"].status = "error"
            _active_migrations[job_id]["status"].message = f"Unexpected error: {str(e)}"
    
    # Start the migration as a background task
    # Note: In production, use BackgroundTasks or a task queue
    import asyncio
    asyncio.create_task(_run_migration())
    
    return {"job_id": job_id, "message": "Migration started"}


@router.get("/{job_id}/status")
async def get_migration_status(
    job_id: str,
    current_user: dict = Depends(get_current_user),
):
    """
    Get the current status of a migration job.
    
    Args:
        job_id: Migration job ID
        current_user: Authenticated user
        
    Returns:
        Current MigrationStatus
    """
    if job_id not in _active_migrations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration job not found",
        )
    
    return _active_migrations[job_id]["status"].model_dump()


@router.get("/{job_id}/logs")
async def get_migration_logs(
    job_id: str,
    since: Optional[datetime] = None,
    current_user: dict = Depends(get_current_user),
):
    """
    Get logs for a migration job (for polling-based updates).
    
    Args:
        job_id: Migration job ID
        since: Only return logs after this timestamp (optional)
        current_user: Authenticated user
        
    Returns:
        List of LogEvent objects
    """
    if job_id not in _active_migrations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration job not found",
        )
    
    logs = _active_migrations[job_id]["logs"]
    
    # Filter by timestamp if provided
    if since:
        logs = [log for log in logs if log.timestamp > since]
    
    return [log.model_dump() for log in logs]
