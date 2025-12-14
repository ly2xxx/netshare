"""
QR Code Generator Service

Core QR code generation logic extracted from app.py for separation of concerns.
"""

import io
import base64
from typing import Optional, Tuple, Dict, Any

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image, ImageDraw

from .theme_manager import ThemeManager, get_theme_manager
from ..config import ICON_SIZE_RATIO


class QRGeneratorService:
    """
    Service for generating QR codes with optional theme icon embedding.
    """
    
    # Map string error correction levels to qrcode constants
    ERROR_CORRECTION_MAP = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H
    }
    
    def __init__(self, theme_manager: Optional[ThemeManager] = None):
        """
        Initialize QR Generator service.
        
        Args:
            theme_manager: ThemeManager instance for icon loading
        """
        self.theme_manager = theme_manager or get_theme_manager()
    
    def generate(
        self,
        data: str,
        theme: str = "general",
        error_correction: str = "H",
        size: Optional[int] = None
    ) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Generate QR code from data string with optional theme icon.
        
        Args:
            data: String data to encode
            theme: Theme for icon embedding (e.g., "snowflake", "general")
            error_correction: Error correction level (L, M, Q, H)
            size: Optional target size in pixels
            
        Returns:
            Tuple of (PIL Image, metadata dict with version, dimensions, etc.)
        """
        # Get error correction constant
        ec_level = self.ERROR_CORRECTION_MAP.get(
            error_correction.upper(), 
            ERROR_CORRECT_H
        )
        
        # Create QR code
        qr = qrcode.QRCode(
            version=None,  # Auto-detect version
            error_correction=ec_level,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        pil_img = img.convert('RGB')
        
        # Get QR version for metadata
        qr_version = qr.version
        
        # Embed theme icon if applicable
        theme_applied = "general"
        if theme != "general" and self.theme_manager.theme_has_icon(theme):
            pil_img = self._embed_icon(pil_img, theme)
            theme_applied = theme
        
        # Resize if specific size requested
        if size is not None:
            pil_img = pil_img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Build metadata
        width, height = pil_img.size
        metadata = {
            "qr_version": qr_version,
            "dimensions": {"width": width, "height": height},
            "data_size_bytes": len(data.encode('utf-8')),
            "theme_applied": theme_applied,
            "error_correction": error_correction.upper()
        }
        
        return pil_img, metadata
    
    def _embed_icon(self, qr_img: Image.Image, theme: str) -> Image.Image:
        """
        Embed theme icon in center of QR code.
        
        Args:
            qr_img: QR code PIL Image
            theme: Theme name for icon
            
        Returns:
            QR code with embedded icon
        """
        qr_width, qr_height = qr_img.size
        
        # Icon should be ~20-25% of QR code size (safe margin under 30%)
        icon_size = int(min(qr_width, qr_height) * ICON_SIZE_RATIO)
        
        try:
            # Load icon from theme manager
            icon = self.theme_manager.load_theme_icon(theme, icon_size)
            
            if icon is None:
                return qr_img
            
            # Calculate center position
            icon_pos = (
                (qr_width - icon_size) // 2,
                (qr_height - icon_size) // 2
            )
            
            # Create white background circle for better contrast
            background = Image.new('RGBA', (icon_size, icon_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(background)
            draw.ellipse([0, 0, icon_size, icon_size], fill=(255, 255, 255, 255))
            
            # Convert QR to RGBA for pasting
            qr_img = qr_img.convert('RGBA')
            
            # Paste white circle, then icon
            qr_img.paste(background, icon_pos, background)
            qr_img.paste(icon, icon_pos, icon)
            
            # Convert back to RGB
            qr_img = qr_img.convert('RGB')
            
        except Exception as e:
            print(f"Warning: Could not embed icon for theme '{theme}': {e}")
        
        return qr_img
    
    def generate_base64(
        self,
        data: str,
        theme: str = "general",
        error_correction: str = "H",
        size: Optional[int] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate QR code and return as base64 encoded PNG.
        
        Args:
            data: String data to encode
            theme: Theme for icon embedding
            error_correction: Error correction level
            size: Optional target size in pixels
            
        Returns:
            Tuple of (base64 string, metadata dict)
        """
        img, metadata = self.generate(data, theme, error_correction, size)
        
        # Convert to base64
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_base64, metadata
    
    def generate_bytes(
        self,
        data: str,
        theme: str = "general",
        error_correction: str = "H",
        size: Optional[int] = None
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Generate QR code and return as PNG bytes.
        
        Args:
            data: String data to encode
            theme: Theme for icon embedding
            error_correction: Error correction level
            size: Optional target size in pixels
            
        Returns:
            Tuple of (PNG bytes, metadata dict)
        """
        img, metadata = self.generate(data, theme, error_correction, size)
        
        # Convert to bytes
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        
        return buf.getvalue(), metadata


# Singleton instance for convenience
_qr_service: Optional[QRGeneratorService] = None


def get_qr_service() -> QRGeneratorService:
    """Get or create singleton QRGeneratorService instance."""
    global _qr_service
    if _qr_service is None:
        _qr_service = QRGeneratorService()
    return _qr_service
