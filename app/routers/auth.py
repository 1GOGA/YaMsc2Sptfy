"""Authentication routes for Spotify OAuth2."""
import logging
import secrets
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import RedirectResponse
import requests

from app.config import settings
from app.models import TokenResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Store state tokens for CSRF protection (in production, use Redis or database)
_oauth_states = {}


@router.get("/login")
async def login():
    """
    Initiate Spotify OAuth2 authorization flow.
    Redirects user to Spotify authorization page.
    """
    # Generate state token for CSRF protection
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = True
    
    # Build authorization URL
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": settings.spotify_client_id,
        "response_type": "code",
        "redirect_uri": settings.redirect_uri,
        "scope": "playlist-modify-public playlist-modify-private",
        "state": state,
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    auth_endpoint = f"{auth_url}?{query_string}"
    
    logger.info("User initiating Spotify login")
    return RedirectResponse(url=auth_endpoint)


@router.get("/callback")
async def callback(code: Optional[str] = None, state: Optional[str] = None, response: Response = None):
    """
    Handle Spotify OAuth2 callback.
    Exchanges authorization code for access token.
    """
    # Validate state token
    if not state or state not in _oauth_states:
        logger.warning("Invalid or missing state token in callback")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state token. Possible CSRF attack.",
        )
    
    del _oauth_states[state]
    
    # Check for authorization errors
    if not code:
        error = "Unknown authorization error"
        logger.error(f"OAuth callback error: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authorization failed: {error}",
        )
    
    # Exchange code for access token
    try:
        token_url = "https://accounts.spotify.com/api/token"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.redirect_uri,
            "client_id": settings.spotify_client_id,
            "client_secret": settings.spotify_client_secret,
        }
        
        response_data = requests.post(token_url, data=payload)
        response_data.raise_for_status()
        
        token_info = response_data.json()
        access_token = token_info.get("access_token")
        expires_in = token_info.get("expires_in", 3600)
        
        if not access_token:
            logger.error("No access token in Spotify response")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to obtain access token from Spotify",
            )
        
        logger.info("Successfully obtained Spotify access token")
        
        # Set token as httponly cookie (secure for production)
        response_obj = RedirectResponse(url="/")
        response_obj.set_cookie(
            key="spotify_token",
            value=access_token,
            max_age=expires_in,
            httponly=True,
            samesite="lax",
            secure=not settings.debug,  # HTTPS in production
        )
        
        return response_obj
        
    except requests.RequestException as e:
        logger.error(f"Error exchanging Spotify code: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to exchange authorization code",
        )
    except Exception as e:
        logger.error(f"Unexpected error in OAuth callback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during authentication",
        )


@router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing the token cookie.
    """
    response = RedirectResponse(url="/")
    response.delete_cookie(key="spotify_token")
    logger.info("User logged out")
    return response


@router.get("/status")
async def auth_status(spotify_token: Optional[str] = None):
    """
    Check if user is authenticated.
    Returns user authentication status.
    """
    is_authenticated = bool(spotify_token)
    return {
        "is_authenticated": is_authenticated,
    }
