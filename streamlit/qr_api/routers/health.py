"""
Health Check Router

Provides health check endpoints for monitoring and load balancers.
"""

from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

from .. import __version__


router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str
    timestamp: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API service is running and healthy."
)
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
    - **status**: Current service status
    - **version**: API version
    - **timestamp**: Current server time
    """
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@router.get(
    "/",
    summary="API Root",
    description="API root endpoint with basic information."
)
async def root():
    """API root with welcome message and links."""
    return {
        "message": "QR Code Generation API",
        "version": __version__,
        "docs": "/docs",
        "health": "/api/v1/health"
    }
