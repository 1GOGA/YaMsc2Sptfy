"""Dependency injection functions for FastAPI routes."""
from typing import Optional
from fastapi import Cookie, HTTPException, status
from app.security import is_token_expired, extract_user_id_from_token


async def get_current_user(spotify_token: Optional[str] = Cookie(None)) -> dict:
    """
    Get the current authenticated user from the Spotify token.
    
    Args:
        spotify_token: The Spotify access token from cookies
        
    Returns:
        Dictionary containing user_id and token
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    if not spotify_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please login to Spotify first.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if is_token_expired(spotify_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired. Please login again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = extract_user_id_from_token(spotify_token)
    
    return {
        "user_id": user_id,
        "access_token": spotify_token,
    }
