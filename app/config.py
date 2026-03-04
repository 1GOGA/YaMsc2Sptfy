"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings, loaded from .env file."""
    
    # Spotify API Credentials
    spotify_client_id: str
    spotify_client_secret: str
    redirect_uri: str
    
    # Application Settings
    debug: bool = False
    app_name: str = "YaMsc2Sptfy"
    app_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
