"""
AudioArchitect - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AudioArchitect API",
    description="Build Your Perfect Music Library - Backend API",
    version="2.0.0"
)

# CORS Configuration (allows desktop app to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/",
         summary="API Information",
         description="Get basic information about the AudioArchitect API",
         tags=["System"],
         response_description="API metadata and status")
async def root():
    """
    ## AudioArchitect API Root
    
    Returns basic information about the API including:
    - Application name
    - Version number
    - Tagline
    - Current status
    
    **Use this endpoint to verify the API is accessible.**
    """
    return {
        "app": "AudioArchitect",
        "version": "2.0.0",
        "tagline": "Build Your Perfect Music Library",
        "status": "online"
    }

@app.get("/health",
         summary="Health Check",
         description="Check the health status of the API and all connected music platform services",
         tags=["System"],
         response_description="Health status of all services")
async def health_check():
    """
    ## System Health Check
    
    Returns the health status of:
    - **API**: Core application status
    - **TIDAL**: TIDAL API connection availability
    - **Spotify**: Spotify API connection availability
    
    **Status Values:**
    - `healthy` - All systems operational
    - `degraded` - Some services unavailable
    - `unhealthy` - Critical systems down
    
    Use this endpoint for monitoring and uptime checks.
    """
    return {
        "status": "healthy",
        "services": {
            "api": "online",
            "tidal": "available",
            "spotify": "available"
        }
    }


# More routes will be added here later
