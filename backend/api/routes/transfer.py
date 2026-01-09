"""
Transfer Routes
Cross-platform playlist transfer
"""

from fastapi import APIRouter, HTTPException
from ...core.models import TransferRequest, Playlist

router = APIRouter()

@router.post("/")
async def transfer_playlist(request: TransferRequest) -> Playlist:
    """
    Transfer playlist between platforms
    
    Matches tracks using ISRC and metadata fuzzy matching.
    """
    # TODO: Implement transfer
    raise HTTPException(
        status_code=501,
        detail="Transfer coming soon! After TIDAL + Spotify adapters ready."
    )

@router.get("/preview")
async def preview_transfer(
    source_platform: str,
    source_playlist_id: str,
    destination_platform: str
):
    """Preview what a transfer would look like"""
    # TODO: Show match confidence, unmatchable tracks, etc.
    return {
        "status": "not_implemented",
        "message": "Preview feature coming in Phase 2"
    }
