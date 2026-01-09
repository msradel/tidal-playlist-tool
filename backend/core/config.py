"""
AudioArchitect Configuration
Centralized settings management
"""

from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    APP_NAME: str = "AudioArchitect"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    
    # API Settings
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    EXPORT_DIR: Path = BASE_DIR / "exports"
    CACHE_DIR: Path = BASE_DIR / ".cache"
    
    # Session Storage
    TIDAL_SESSION_FILE: Path = Path.home() / ".audioarchitect_tidal.txt"
    SPOTIFY_SESSION_FILE: Path = Path.home() / ".audioarchitect_spotify.txt"
    
    # Cache Settings
    CACHE_TTL_SECONDS: int = 300  # 5 minutes
    
    # TIDAL Settings
    TIDAL_BATCH_SIZE: int = 100
    
    # Spotify Settings
    SPOTIFY_CLIENT_ID: Optional[str] = None
    SPOTIFY_CLIENT_SECRET: Optional[str] = None
    SPOTIFY_REDIRECT_URI: str = "http://localhost:8888/callback"
    
    # Feature Flags
    ENABLE_RANDOMIZER: bool = True
    ENABLE_TRANSFER: bool = True
    ENABLE_SYNC: bool = False  # Coming soon
    ENABLE_PLAYBACK: bool = False  # Phase 2
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()

# Create directories if they don't exist
settings.EXPORT_DIR.mkdir(exist_ok=True)
settings.CACHE_DIR.mkdir(exist_ok=True)
