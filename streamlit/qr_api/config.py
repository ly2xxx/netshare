"""
Configuration settings for QR API service
"""

import os
from typing import List

# Server settings
API_HOST: str = os.getenv("QR_API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("QR_API_PORT", "8000"))

# CORS settings
CORS_ORIGINS: List[str] = [
    "http://localhost:8501",  # Local Streamlit
    "http://127.0.0.1:8501",
    "https://qr-greeting.streamlit.app",  # Production Streamlit
    "*"  # Allow all for development (restrict in production)
]

# API settings
API_VERSION: str = "1.0.0"
API_TITLE: str = "QR Code Generation API"
API_DESCRIPTION: str = """
## QR Code Generation API

A RESTful API for generating QR codes with optional theme icons.

### Features
- Generate QR codes from any data string
- Embed theme icons in QR code center
- URL encoding/decoding for greeting messages
- Multiple output formats (PNG, base64)

### Authentication
Currently no authentication required (development mode).
"""

# QR Code settings
DEFAULT_QR_SIZE: int = 500
DEFAULT_ERROR_CORRECTION: str = "H"
MAX_DATA_SIZE: int = 2000  # Maximum bytes for QR data

# Icon settings
ICONS_DIR: str = os.path.join(os.path.dirname(__file__), "icons")
DEFAULT_ICON_SIZE: int = 100
ICON_SIZE_RATIO: float = 0.22  # Icon should be ~22% of QR code size

# Base URL for greeting app (used in URL encoding)
GREETING_APP_URL: str = os.getenv(
    "GREETING_APP_URL", 
    "https://qr-greeting.streamlit.app/"
)
