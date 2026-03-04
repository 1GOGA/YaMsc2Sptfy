"""Playlist conversion orchestration."""
import logging
from datetime import datetime
from typing import List, AsyncGenerator, Dict, Tuple
import asyncio
from app.services.spotify_client import SpotifyClient
from app.services.yandex_parser import YandexParser
from app.models import LogEvent, TrackMatch

logger = logging.getLogger(__name__)


class PlaylistConverter:
    """
    Orchestrates the conversion of a Yandex Music playlist to Spotify.
    Coordinates Yandex parsing, track matching, and Spotify playlist creation.
    """
    
    def __init__(self, access_token: str):
        """
        Initialize the converter with user's Spotify access token.
        
        Args:
            access_token: User's Spotify OAuth access token
        """
        self.spotify = SpotifyClient(access_token)
        self.yandex = YandexParser()
        self.logger = logger
    
    async def convert_playlist(self, yandex_url: str) -> AsyncGenerator[Tuple[str, Dict], None]:
        """
        Convert a Yandex Music playlist to Spotify.
        Yields progress updates (status, data) as an async generator.
        
        Args:
            yandex_url: URL or ID of the Yandex playlist
            
        Yields:
            Tuples of (event_type, data_dict) where event_type is one of:
            - "log": data contains {"level": str, "message": str}
            - "progress": data contains {"found": int, "total": int}
            - "complete": data contains {"playlist_id": str, "playlist_url": str, "total_added": int}
            - "error": data contains {"message": str}
        """
        try:
            # Step 1: Parse Yandex playlist
            yield "log", {"level": "info", "message": "Starting to parse Yandex Music playlist..."}
            
            try:
                yandex_tracks = self.yandex.parse_playlist(yandex_url)
                total_tracks = len(yandex_tracks)
                yield "log", {"level": "info", "message": f"Found {total_tracks} tracks in Yandex playlist"}
                yield "progress", {"found": 0, "total": total_tracks}
            except ValueError as e:
                error_msg = f"Failed to parse Yandex playlist: {str(e)}"
                self.logger.error(error_msg)
                yield "log", {"level": "error", "message": error_msg}
                yield "error", {"message": error_msg}
                return
            
            # Step 2: Search for tracks in Spotify
            yield "log", {"level": "info", "message": "Searching for tracks in Spotify..."}
            
            matched_tracks = []
            found_count = 0
            not_found_list = []
            
            for idx, track in enumerate(yandex_tracks, 1):
                try:
                    # Search track in Spotify
                    spotify_uri = self.spotify.search_track(track.artist, track.title)
                    
                    if spotify_uri:
                        matched_tracks.append(spotify_uri)
                        found_count += 1
                    else:
                        not_found_list.append(f"{track.artist} - {track.title}")
                    
                    # Yield progress every 5 tracks or at the end
                    if idx % 5 == 0 or idx == total_tracks:
                        yield "progress", {"found": found_count, "total": total_tracks}
                        yield "log", {"level": "info", "message": f"Progress: {idx}/{total_tracks} tracks"}
                    
                    # Rate limiting
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    self.logger.warning(f"Error searching for track {track.artist} - {track.title}: {e}")
                    not_found_list.append(f"{track.artist} - {track.title}")
            
            # Report search results
            yield "log", {"level": "info", "message": f"Found {found_count}/{total_tracks} tracks on Spotify"}
            
            if not_found_list:
                not_found_msg = f"Could not find {len(not_found_list)} tracks on Spotify"
                yield "log", {"level": "warning", "message": not_found_msg}
                if len(not_found_list) <= 5:
                    for track in not_found_list:
                        yield "log", {"level": "warning", "message": f"  - {track}"}
            
            if not matched_tracks:
                error_msg = "No tracks found on Spotify. Cannot create playlist."
                self.logger.error(error_msg)
                yield "log", {"level": "error", "message": error_msg}
                yield "error", {"message": error_msg}
                return
            
            # Step 3: Create Spotify playlist
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            playlist_name = f"Migrated from Yandex ({timestamp})"
            playlist_description = f"Playlist migrated from Yandex Music. Found {found_count}/{total_tracks} tracks."
            
            yield "log", {"level": "info", "message": f"Creating Spotify playlist: '{playlist_name}'"}
            
            try:
                playlist_id = self.spotify.create_playlist(playlist_name, playlist_description)
            except Exception as e:
                error_msg = f"Failed to create Spotify playlist: {str(e)}"
                self.logger.error(error_msg)
                yield "log", {"level": "error", "message": error_msg}
                yield "error", {"message": error_msg}
                return
            
            # Step 4: Add tracks to playlist
            yield "log", {"level": "info", "message": f"Adding {len(matched_tracks)} tracks to Spotify playlist..."}
            
            try:
                self.spotify.batch_add_tracks(playlist_id, matched_tracks)
            except Exception as e:
                error_msg = f"Failed to add tracks to playlist: {str(e)}"
                self.logger.error(error_msg)
                yield "log", {"level": "error", "message": error_msg}
                yield "error", {"message": error_msg}
                return
            
            # Step 5: Complete
            playlist_url = self.spotify.get_playlist_url(playlist_id)
            
            success_msg = f"Successfully created playlist with {len(matched_tracks)} tracks!"
            yield "log", {"level": "info", "message": success_msg}
            
            yield "complete", {
                "playlist_id": playlist_id,
                "playlist_url": playlist_url,
                "total_added": len(matched_tracks),
                "playlist_name": playlist_name,
            }
            
        except Exception as e:
            error_msg = f"Unexpected error during conversion: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            yield "log", {"level": "error", "message": error_msg}
            yield "error", {"message": error_msg}
