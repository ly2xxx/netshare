"""
Image utility functions for icon loading and base64 conversion
Handles theme icon loading and image encoding
"""

import base64
import os
from PIL import Image
from typing import Optional


def get_img_as_base64(file_path: str) -> str:
    """
    Read image file and return base64 string

    Args:
        file_path: Path to image file

    Returns:
        Base64 encoded string of the image
    """
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def load_theme_icon(theme: str, size: int = 100) -> Optional[Image.Image]:
    """
    Load and resize theme icon from file

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Desired icon size in pixels

    Returns:
        PIL Image with transparent background, or None if not found
    """
    # Path to icon file
    icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", f"{theme}.png")

    try:
        # Load icon
        icon = Image.open(icon_path)

        # Resize to desired size with high-quality resampling
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)

        # Ensure RGBA mode for transparency
        if icon.mode != 'RGBA':
            icon = icon.convert('RGBA')

        return icon
    except FileNotFoundError:
        # Icon file doesn't exist - return None to skip icon
        return None
    except Exception as e:
        print(f"Error loading icon for theme '{theme}': {e}")
        return None


def get_theme_display_icon(theme: str, size: int = 60) -> Optional[Image.Image]:
    """
    Load theme icon for display in UI preview

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Preview size in pixels (default 60px for grid display)

    Returns:
        PIL Image or None if theme is "general" or icon not found
    """
    if theme == "general":
        return None

    icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", f"{theme}.png")

    if not os.path.exists(icon_path):
        return None

    try:
        icon = Image.open(icon_path)
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        return icon
    except Exception:
        return None
