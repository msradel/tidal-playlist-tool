"""
AudioArchitect Data Models
Platform-agnostic representations
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class Platform(str, Enum):
    """Supported music platforms"""
    TIDAL = "tidal"
    SPOTIFY = "spotify"
    APPLE_MUSIC = "apple_music"
    YOUTUBE_MUSIC = "youtube_music"

class Track(BaseModel):
    """Universal track representation"""
    
    # Universal identifiers
    isrc: Optional[str] = None
    title: str
    artist: str
    album: Optional[str] = None
    duration_ms: Optional[int] = None
    
    # Platform-specific IDs
    platform_ids: Dict[str, Optional[str]] = Field(default_factory=dict)
    
    # Metadata
    year: Optional[int] = None
    genre: Optional[str] = None
    explicit: bool = False
    
    # Matching metadata
    match_confidence: float = 1.0
    match_method: Optional[str] = None  # "isrc", "metadata", "fuzzy"
    
    class Config:
        json_schema_extra = {
            "example": {
                "isrc": "USRC17607839",
                "title": "Blinding Lights",
                "artist": "The Weeknd",
                "album": "After Hours",
                "duration_ms": 200040,
                "platform_ids": {
                    "tidal": "123456789",
                    "spotify": "0VjIjW4GlUZAMYd2vXMi3b"
                },
                "year": 2019,
                "explicit": False,
                "match_confidence": 1.0
            }
        }

class Playlist(BaseModel):
    """Universal playlist representation"""
    
    id: str
    name: str
    platform: Platform
    
    # Metadata
    description: Optional[str] = None
    owner: Optional[str] = None
    public: bool = True
    collaborative: bool = False
    
    # Stats
    track_count: int = 0
    duration_ms: int = 0
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Image
    image_url: Optional[str] = None
    
    # Tracks (loaded on demand)
    tracks: Optional[List[Track]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "abc123",
                "name": "My Awesome Playlist",
                "platform": "tidal",
                "description": "The best tracks ever",
                "owner": "msradel",
                "track_count": 2033,
                "duration_ms": 7200000
            }
        }

class RandomizeRequest(BaseModel):
    """Request to randomize a playlist"""
    
    platform: Platform
    playlist_id: str
    algorithm: str = "smart"  # "smart" or "pure"
    new_playlist_name: Optional[str] = None
    
class TransferRequest(BaseModel):
    """Request to transfer playlist between platforms"""
    
    source_platform: Platform
    source_playlist_id: str
    destination_platform: Platform
    new_playlist_name: Optional[str] = None
    match_strategy: str = "best"  # "isrc_only", "metadata_only", "best"
