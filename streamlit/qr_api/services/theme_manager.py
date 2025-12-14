#!/usr/bin/env python3
"""
Theme icon management service
Extracted from app.py
"""
from PIL import Image
from pathlib import Path
import base64
from typing import Optional
import io
from ..config import ICONS_DIR, THEME_ICONS


def load_theme_icon(theme: str, size: int = 100) -> Optional[Image.Image]:
    """
    Load and resize theme icon from file

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Desired icon size in pixels

    Returns:
        PIL Image with transparent background, or None if not found
    """
    icon_path = ICONS_DIR / f"{theme}.png"

    try:
        icon = Image.open(icon_path)
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)

        if icon.mode != 'RGBA':
            icon = icon.convert('RGBA')

        return icon
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error loading icon for theme '{theme}': {e}")
        return None


def get_theme_display_icon(theme: str, size: int = 60) -> Optional[Image.Image]:
    """
    Load theme icon for display in UI preview

    Args:
        theme: Theme name
        size: Preview size in pixels

    Returns:
        PIL Image or None
    """
    if theme == "general":
        return None

    icon_path = ICONS_DIR / f"{theme}.png"

    if not icon_path.exists():
        return None

    try:
        icon = Image.open(icon_path)
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        return icon
    except Exception:
        return None


def get_img_as_base64(file_path: Path) -> str:
    """Read image file and return base64 string"""
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def get_available_themes() -> list[dict]:
    """
    Get list of available themes with metadata

    Returns:
        List of theme dictionaries
    """
    themes = []
    for theme_name, emoji in THEME_ICONS.items():
        icon_path = ICONS_DIR / f"{theme_name}.png"
        themes.append({
            "name": theme_name,
            "emoji": emoji,
            "has_icon": icon_path.exists() if theme_name != "general" else False
        })
    return themes


def get_theme_icon_base64(theme: str, size: int = 60) -> Optional[str]:
    """
    Get theme icon as base64 string for API responses

    Args:
        theme: Theme name
        size: Icon size in pixels

    Returns:
        Base64-encoded PNG or None
    """
    icon = get_theme_display_icon(theme, size)
    if icon is None:
        return None

    buf = io.BytesIO()
    icon.save(buf, format='PNG')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()
