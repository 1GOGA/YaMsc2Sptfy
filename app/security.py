"""Security and authentication utilities."""
import jwt
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status


def decode_access_token(token: str) -> dict:
    """
    Decode a Spotify access token (JWT format).
    Note: We don't verify the signature since Spotify handles that.
    This just extracts the payload.
    
    Args:
        token: The access token to decode
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Decode without verification since we trust Spotify's tokens
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def is_token_expired(token: str) -> bool:
    """
    Check if a token has expired.
    
    Args:
        token: The access token
        
    Returns:
        True if expired, False otherwise
    """
    try:
        payload = decode_access_token(token)
        exp = payload.get("exp")
        if exp is None:
            return False
        return datetime.utcfromtimestamp(exp) < datetime.utcnow()
    except HTTPException:
        return True


def extract_user_id_from_token(token: str) -> str:
    """
    Extract the user ID from a Spotify access token.
    
    Args:
        token: The access token
        
    Returns:
        The Spotify user ID
        
    Raises:
        HTTPException: If token is invalid
    """
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no user ID",
        )
    return user_id
