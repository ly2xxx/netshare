"""
QR Code Generation API - Main Application

FastAPI application entry point with all routes configured.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .config import API_TITLE, API_DESCRIPTION, CORS_ORIGINS
from .routers import qr_router, greeting_router, health_router


# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(health_router)  # Root level for / and /health
app.include_router(qr_router, prefix="/api/v1")
app.include_router(greeting_router, prefix="/api/v1")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print(f"🚀 {API_TITLE} v{__version__} starting...")
    print(f"📚 Swagger docs available at: http://localhost:8000/docs")
    print(f"📖 ReDoc available at: http://localhost:8000/redoc")


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    from .config import API_HOST, API_PORT
    
    uvicorn.run(
        "qr_api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )
