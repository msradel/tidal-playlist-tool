"""
Platform Routes
List available platforms and their capabilities
"""

from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

@router.get("/")
async def list_platforms() -> List[Dict]:
    """List all supported music platforms"""
    return [
        {
            "id": "tidal",
            "name": "TIDAL",
            "status": "available",
            "features": {
                "playlists": True,
                "randomize": True,
                "transfer": True,
                "sync": False,
                "playback": False
            }
        },
        {
            "id": "spotify",
            "name": "Spotify",
            "status": "coming_soon",
            "features": {
                "playlists": False,
                "randomize": False,
                "transfer": False,
                "sync": False,
                "playback": False
            }
        }
    ]

@router.get("/{platform_id}")
async def get_platform(platform_id: str) -> Dict:
    """Get details about a specific platform"""
    platforms = {
        "tidal": {
            "id": "tidal",
            "name": "TIDAL",
            "description": "High-fidelity music streaming",
            "website": "https://tidal.com",
            "api_docs": "https://developer.tidal.com"
        },
        "spotify": {
            "id": "spotify",
            "name": "Spotify",
            "description": "Music for everyone",
            "website": "https://spotify.com",
            "api_docs": "https://developer.spotify.com"
        }
    }
    
    if platform_id not in platforms:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    return platforms[platform_id]
