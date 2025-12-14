#!/usr/bin/env python3
"""
Configuration for QR API Service
"""
from pathlib import Path

# API Configuration
API_HOST = "127.0.0.1"
API_PORT = 8000
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# File Paths (absolute paths to ensure compatibility in both app.py and API contexts)
STREAMLIT_DIR = Path(__file__).parent.parent
ICONS_DIR = STREAMLIT_DIR / "icons"

# QR Code Settings
DEFAULT_ERROR_CORRECTION = "H"  # High error correction
DEFAULT_BOX_SIZE = 10
DEFAULT_BORDER = 4
ICON_SIZE_RATIO = 0.22  # Icon is 22% of QR code size

# Theme Configuration
THEME_ICONS = {
    "snowflake": "❄️",
    "fireworks": "🎆",
    "lights": "✨",
    "stars": "⭐",
    "confetti": "🎉",
    "champagne": "🥂",
    "hearts": "❤️",
    "general": None  # No icon for general theme
}

# Greeting App URL (for encoding)
GREETING_APP_URL = "https://qr-greeting.streamlit.app/"
