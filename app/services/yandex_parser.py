"""Yandex Music playlist parser."""
import logging
import re
import time
from typing import List, Optional
from app.models import TrackInfo

logger = logging.getLogger(__name__)


class YandexParser:
    """
    Parser for public Yandex Music playlists using yandex-music library.
    """
    
    def __init__(self):
        """Initialize the Yandex parser."""
        self.logger = logger
        # Lazy import to avoid issues if library isn't installed
        try:
            from yandex_music import Client
            self.Client = Client
        except ImportError:
            self.logger.error("yandex-music library not installed")
            raise
    
    @staticmethod
    def extract_playlist_id(url_or_id: str) -> str:
        """
        Extract playlist ID from a Yandex Music URL or return ID as-is.
        
        Handles formats like:
        - https://music.yandex.ru/users/yamusicbot/playlists/1015
        - yamusicbot/1015
        - 1015 (assumes 'yamusicbot' as default user)
        
        Args:
            url_or_id: URL or playlist ID
            
        Returns:
            Playlist ID string
        """
        # Handle full URL
        match = re.search(r'users/([^/]+)/playlists/(\d+)', url_or_id)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        
        # Handle user/id format
        if '/' in url_or_id and url_or_id.count('/') == 1:
            return url_or_id
        
        # Assume it's just an ID, use default user
        return f"yamusicbot/{url_or_id}"
    
    def parse_playlist(self, playlist_url_or_id: str) -> List[TrackInfo]:
        """
        Parse a public Yandex Music playlist and extract track information.
        
        Args:
            playlist_url_or_id: URL or ID of the playlist
            
        Returns:
            List of TrackInfo objects
            
        Raises:
            ValueError: If playlist is invalid or inaccessible
        """
        try:
            # Extract playlist ID
            playlist_id = self.extract_playlist_id(playlist_url_or_id)
            self.logger.info(f"Parsing Yandex playlist: {playlist_id}")
            
            # Initialize client (public access doesn't require authentication)
            client = self.Client()
            
            # Fetch playlist
            playlist = client.playlist(playlist_id)
            
            if not playlist:
                raise ValueError(f"Playlist not found or is private: {playlist_id}")
            
            # Extract tracks
            tracks_info = []
            playlist_items = playlist.tracks or []
            
            self.logger.info(f"Found {len(playlist_items)} tracks in playlist")
            
            for item in playlist_items:
                try:
                    track = item.track if hasattr(item, 'track') else item
                    if not track:
                        continue
                    
                    # Extract artist and title
                    artist = "Unknown"
                    if hasattr(track, 'artists') and track.artists:
                        # Join multiple artists if present
                        artist = ", ".join([a.name for a in track.artists if hasattr(a, 'name')])
                    
                    title = track.title if hasattr(track, 'title') else "Unknown"
                    
                    if artist and title:
                        tracks_info.append(TrackInfo(artist=artist, title=title))
                        self.logger.debug(f"Extracted: {artist} - {title}")
                    
                    # Rate limiting: add small delay between requests
                    time.sleep(0.05)
                    
                except Exception as e:
                    self.logger.warning(f"Error extracting track info: {e}")
                    continue
            
            if not tracks_info:
                raise ValueError("No tracks found in playlist or all tracks failed to parse")
            
            self.logger.info(f"Successfully parsed {len(tracks_info)} tracks from Yandex")
            return tracks_info
            
        except ValueError as e:
            self.logger.error(f"Yandex parser error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error parsing Yandex playlist: {e}")
            raise ValueError(f"Failed to parse Yandex playlist: {str(e)}")
