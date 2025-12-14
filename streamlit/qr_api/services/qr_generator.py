#!/usr/bin/env python3
"""
QR code generation service
Extracted from app.py
"""
import qrcode
from PIL import Image, ImageDraw
import base64
import io
from typing import Optional
from ..config import (
    DEFAULT_ERROR_CORRECTION,
    DEFAULT_BOX_SIZE,
    DEFAULT_BORDER,
    ICON_SIZE_RATIO,
    THEME_ICONS
)
from .theme_manager import load_theme_icon

# Error correction mapping
ERROR_CORRECTION_MAP = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}


def generate_qr_code(
    data: str,
    theme: str = "general",
    error_correction: str = DEFAULT_ERROR_CORRECTION
) -> Image.Image:
    """
    Generate QR code from data string

    Args:
        data: String data to encode
        theme: Theme name for icon embedding
        error_correction: Error correction level ("L", "M", "Q", "H")

    Returns:
        PIL Image of QR code
    """
    ec_level = ERROR_CORRECTION_MAP.get(error_correction, qrcode.constants.ERROR_CORRECT_H)

    qr = qrcode.QRCode(
        version=None,
        error_correction=ec_level,
        box_size=DEFAULT_BOX_SIZE,
        border=DEFAULT_BORDER,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    pil_img = img.convert('RGB')

    # Add theme icon if applicable
    if theme in THEME_ICONS and THEME_ICONS[theme]:
        qr_width, qr_height = pil_img.size
        icon_size = int(min(qr_width, qr_height) * ICON_SIZE_RATIO)

        try:
            icon = load_theme_icon(theme, icon_size)

            if icon is None:
                return pil_img

            # Calculate center position
            icon_pos = (
                (qr_width - icon_size) // 2,
                (qr_height - icon_size) // 2
            )

            # Create white background circle
            background = Image.new('RGBA', (icon_size, icon_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(background)
            draw.ellipse([0, 0, icon_size, icon_size], fill=(255, 255, 255, 255))

            # Convert to RGBA for pasting
            pil_img = pil_img.convert('RGBA')

            # Paste white circle, then icon
            pil_img.paste(background, icon_pos, background)
            pil_img.paste(icon, icon_pos, icon)

            # Convert back to RGB
            pil_img = pil_img.convert('RGB')
        except Exception as e:
            print(f"Warning: Could not embed icon for theme '{theme}': {e}")

    return pil_img


def qr_image_to_base64(img: Image.Image) -> str:
    """
    Convert PIL Image to base64 string

    Args:
        img: PIL Image object

    Returns:
        Base64-encoded PNG string
    """
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def decode_qr_from_base64(image_base64: str) -> Optional[str]:
    """
    Decode QR code from base64-encoded image

    Args:
        image_base64: Base64-encoded image string

    Returns:
        Decoded data or None if failed
    """
    try:
        import cv2
        import numpy as np

        # Decode base64 to image
        img_bytes = base64.b64decode(image_base64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Detect and decode QR
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        return data if data else None
    except Exception as e:
        print(f"Error decoding QR: {e}")
        return None
