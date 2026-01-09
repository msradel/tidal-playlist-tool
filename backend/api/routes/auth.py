"""
Authentication Routes
Handle TIDAL and Spotify OAuth
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class AuthStatus(BaseModel):
    platform: str
    authenticated: bool
    user_id: Optional[str] = None
    expires_at: Optional[str] = None

@router.get("/status")
async def auth_status() -> Dict[str, AuthStatus]:
    """Get authentication status for all platforms"""
    # TODO: Implement actual session checking
    return {
        "tidal": AuthStatus(platform="tidal", authenticated=False),
        "spotify": AuthStatus(platform="spotify", authenticated=False)
    }

@router.post("/tidal/login")
async def tidal_login():
    """Start TIDAL OAuth flow"""
    # TODO: Implement TIDAL OAuth
    return {"status": "not_implemented"}

@router.post("/spotify/login")
async def spotify_login():
    """Start Spotify OAuth flow"""
    # TODO: Implement Spotify OAuth
    return {"status": "not_implemented"}

@router.post("/logout")
async def logout(platform: str):
    """Logout from a platform"""
    # TODO: Clear session
    return {"status": "logged_out", "platform": platform}
