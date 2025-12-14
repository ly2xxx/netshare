"""
API Routers package
"""

from .qr import router as qr_router
from .greeting import router as greeting_router
from .health import router as health_router

__all__ = ["qr_router", "greeting_router", "health_router"]
