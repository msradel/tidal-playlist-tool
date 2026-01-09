"""
Randomize Routes
Playlist shuffling functionality
"""

from fastapi import APIRouter, HTTPException
from ...core.models import RandomizeRequest, Playlist

router = APIRouter()

@router.post("/")
async def randomize_playlist(request: RandomizeRequest) -> Playlist:
    """
    Randomize a playlist
    
    Creates a new playlist with tracks in random order.
    Original playlist remains unchanged.
    """
    # TODO: Implement randomization
    # 1. Fetch tracks from source playlist
    # 2. Shuffle using selected algorithm
    # 3. Create new playlist
    # 4. Add shuffled tracks
    # 5. Return new playlist info
    
    raise HTTPException(
        status_code=501,
        detail="Randomization coming soon! Check back Monday."
    )

@router.get("/algorithms")
async def list_algorithms():
    """List available shuffle algorithms"""
    return {
        "algorithms": [
            {
                "id": "smart",
                "name": "Smart Shuffle",
                "description": "Spreads out artists to avoid repetition",
                "recommended": True
            },
            {
                "id": "pure",
                "name": "Pure Random",
                "description": "Completely random order (Fisher-Yates algorithm)",
                "recommended": False
            }
        ]
    }
