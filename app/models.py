"""Pydantic models for request/response validation and data structures."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TrackInfo(BaseModel):
    """Information about a track from Yandex Music."""
    artist: str = Field(..., description="Track artist name")
    title: str = Field(..., description="Track title")


class TrackMatch(BaseModel):
    """Result of matching a Yandex track with Spotify."""
    artist: str = Field(..., description="Track artist name")
    title: str = Field(..., description="Track title")
    spotify_id: Optional[str] = Field(None, description="Spotify track URI or None if not found")


class MigrationRequest(BaseModel):
    """Request to migrate a Yandex Music playlist to Spotify."""
    yandex_playlist_url: str = Field(..., description="URL or ID of the Yandex Music playlist")


class MigrationStatus(BaseModel):
    """Current status of a playlist migration."""
    status: str = Field(..., description="Current status: pending, searching, creating, complete, error")
    progress: int = Field(0, description="Number of tracks found so far")
    total: int = Field(0, description="Total tracks in the Yandex playlist")
    message: str = Field("", description="Current status message")
    playlist_id: Optional[str] = Field(None, description="Spotify playlist ID if created")
    playlist_url: Optional[str] = Field(None, description="Spotify playlist URL if created")


class LogEvent(BaseModel):
    """A single event in the migration log."""
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When this event occurred")
    level: str = Field(..., description="Log level: info, warning, error")
    message: str = Field(..., description="Event message")


class TokenResponse(BaseModel):
    """Response containing OAuth token information."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int


class UserData(BaseModel):
    """Current user data."""
    user_id: str
    display_name: Optional[str] = None
    is_authenticated: bool = False
