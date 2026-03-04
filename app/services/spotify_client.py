"""Wrapper around Spotipy for Spotify API interactions."""
import logging
from typing import Optional, List
import spotipy
from spotipy.exceptions import SpotifyException

logger = logging.getLogger(__name__)


class SpotifyClient:
    """
    Wrapper around spotipy.Spotify for API calls.
    Handles error handling, rate limiting, and batch operations.
    """
    
    def __init__(self, access_token: str):
        """
        Initialize the Spotify client with an access token.
        
        Args:
            access_token: Valid Spotify OAuth access token
        """
        self.client = spotipy.Spotify(auth=access_token)
        self.logger = logger
    
    def search_track(self, artist: str, title: str) -> Optional[str]:
        """
        Search for a track in Spotify and return its URI.
        
        Args:
            artist: Artist name
            title: Track title
            
        Returns:
            Spotify track URI if found, None otherwise
        """
        try:
            # Build search query: "artist:name track:title"
            query = f'artist:"{artist}" track:"{title}"'
            results = self.client.search(q=query, type='track', limit=1)
            
            tracks = results.get('tracks', {}).get('items', [])
            if tracks:
                track_uri = tracks[0]['uri']
                self.logger.info(f"Found track: {artist} - {title} (URI: {track_uri})")
                return track_uri
            
            self.logger.debug(f"Track not found: {artist} - {title}")
            return None
            
        except SpotifyException as e:
            self.logger.error(f"Spotify error searching for {artist} - {title}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error searching for track: {e}")
            raise
    
    def create_playlist(self, name: str, description: str = "") -> str:
        """
        Create a new playlist in the current user's account.
        
        Args:
            name: Playlist name
            description: Playlist description
            
        Returns:
            Spotify playlist ID
            
        Raises:
            SpotifyException: If playlist creation fails
        """
        try:
            playlist = self.client.current_user_playlist_create(
                name=name,
                public=True,
                description=description
            )
            playlist_id = playlist['id']
            self.logger.info(f"Created playlist: {name} (ID: {playlist_id})")
            return playlist_id
            
        except SpotifyException as e:
            self.logger.error(f"Spotify error creating playlist: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error creating playlist: {e}")
            raise
    
    def batch_add_tracks(self, playlist_id: str, track_uris: List[str]) -> bool:
        """
        Add tracks to a playlist in batches (max 100 per request).
        
        Args:
            playlist_id: Spotify playlist ID
            track_uris: List of Spotify track URIs
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            SpotifyException: If adding tracks fails
        """
        if not track_uris:
            self.logger.info("No tracks to add")
            return True
        
        try:
            # Batch into chunks of 100 (Spotify API limit)
            batch_size = 100
            total = len(track_uris)
            
            for i in range(0, total, batch_size):
                batch = track_uris[i:i + batch_size]
                self.client.playlist_add_items(playlist_id, batch)
                self.logger.info(f"Added {len(batch)} tracks to playlist (batch {i // batch_size + 1})")
            
            self.logger.info(f"Successfully added {total} tracks to playlist {playlist_id}")
            return True
            
        except SpotifyException as e:
            self.logger.error(f"Spotify error adding tracks: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error adding tracks: {e}")
            raise
    
    def get_playlist_url(self, playlist_id: str) -> str:
        """
        Get the URL for a playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            
        Returns:
            Spotify playlist URL
        """
        try:
            playlist = self.client.playlist(playlist_id)
            external_urls = playlist.get('external_urls', {})
            return external_urls.get('spotify', f'https://open.spotify.com/playlist/{playlist_id}')
        except Exception as e:
            self.logger.error(f"Error getting playlist URL: {e}")
            return f'https://open.spotify.com/playlist/{playlist_id}'
