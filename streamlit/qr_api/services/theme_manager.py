"""
Theme Manager Service

Handles theme icons and metadata for QR code generation.
Extracted from app.py for separation of concerns.
"""

import os
from typing import Optional, Dict, List
from PIL import Image

from ..config import ICONS_DIR


class ThemeManager:
    """
    Manages theme icons and metadata for QR code generation.
    
    Themes include visual icons that can be embedded in QR code centers.
    """
    
    # Theme to emoji mapping
    THEME_ICONS: Dict[str, Optional[str]] = {
        "snowflake": "❄️",
        "fireworks": "🎆",
        "lights": "✨",
        "stars": "⭐",
        "confetti": "🎉",
        "champagne": "🥂",
        "hearts": "❤️",
        "general": None  # No icon for general theme
    }
    
    # Human-readable labels for themes
    THEME_LABELS: Dict[str, str] = {
        "snowflake": "Snowflake",
        "fireworks": "Fireworks",
        "lights": "Lights",
        "stars": "Stars",
        "confetti": "Confetti",
        "champagne": "Champagne",
        "hearts": "Hearts",
        "general": "General (No Icon)"
    }
    
    def __init__(self, icons_dir: str = ICONS_DIR):
        """
        Initialize ThemeManager with icons directory.
        
        Args:
            icons_dir: Path to directory containing theme icon PNG files
        """
        self.icons_dir = icons_dir
    
    def get_all_themes(self) -> List[Dict]:
        """
        Get list of all available themes with metadata.
        
        Returns:
            List of theme dictionaries with key, emoji, label, has_icon
        """
        themes = []
        for key, emoji in self.THEME_ICONS.items():
            has_icon = self._icon_exists(key)
            themes.append({
                "key": key,
                "emoji": emoji,
                "label": self.THEME_LABELS.get(key, key.title()),
                "has_icon": has_icon
            })
        return themes
    
    def get_theme_info(self, theme_key: str) -> Optional[Dict]:
        """
        Get information about a specific theme.
        
        Args:
            theme_key: Theme identifier
            
        Returns:
            Theme dictionary or None if not found
        """
        if theme_key not in self.THEME_ICONS:
            return None
        
        return {
            "key": theme_key,
            "emoji": self.THEME_ICONS[theme_key],
            "label": self.THEME_LABELS.get(theme_key, theme_key.title()),
            "has_icon": self._icon_exists(theme_key)
        }
    
    def load_theme_icon(self, theme: str, size: int = 100) -> Optional[Image.Image]:
        """
        Load and resize theme icon from file.
        
        Args:
            theme: Theme name (e.g., "snowflake", "hearts")
            size: Desired icon size in pixels
            
        Returns:
            PIL Image with transparent background, or None if not found
        """
        if theme == "general" or theme not in self.THEME_ICONS:
            return None
        
        icon_path = os.path.join(self.icons_dir, f"{theme}.png")
        
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
            return None
        except Exception as e:
            print(f"Error loading icon for theme '{theme}': {e}")
            return None
    
    def get_theme_display_icon(self, theme: str, size: int = 60) -> Optional[Image.Image]:
        """
        Load theme icon for display in UI preview.
        
        Args:
            theme: Theme name (e.g., "snowflake", "hearts")
            size: Preview size in pixels (default 60px for grid display)
            
        Returns:
            PIL Image or None if theme is "general" or icon not found
        """
        if theme == "general":
            return None
        
        return self.load_theme_icon(theme, size)
    
    def theme_has_icon(self, theme: str) -> bool:
        """
        Check if a theme has an embeddable icon.
        
        Args:
            theme: Theme identifier
            
        Returns:
            True if theme has an icon file, False otherwise
        """
        if theme == "general" or theme not in self.THEME_ICONS:
            return False
        return self._icon_exists(theme)
    
    def _icon_exists(self, theme: str) -> bool:
        """Check if icon file exists for theme."""
        if theme == "general":
            return False
        icon_path = os.path.join(self.icons_dir, f"{theme}.png")
        return os.path.exists(icon_path)
    
    def get_icon_as_bytes(self, theme: str, size: int = 60) -> Optional[bytes]:
        """
        Get theme icon as PNG bytes for HTTP response.
        
        Args:
            theme: Theme identifier
            size: Icon size in pixels
            
        Returns:
            PNG bytes or None if icon not found
        """
        icon = self.load_theme_icon(theme, size)
        if icon is None:
            return None
        
        import io
        buf = io.BytesIO()
        icon.save(buf, format='PNG')
        return buf.getvalue()


# Singleton instance for convenience
_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """Get or create singleton ThemeManager instance."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
