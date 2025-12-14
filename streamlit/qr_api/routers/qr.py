#!/usr/bin/env python3
"""
QR code generation and decoding endpoints
"""
from fastapi import APIRouter, HTTPException
from ..schemas.qr import (
    QRGenerateRequest,
    QRGenerateResponse,
    QRDecodeRequest,
    QRDecodeResponse,
    ThemeListResponse
)
from ..services.qr_generator import (
    generate_qr_code,
    qr_image_to_base64,
    decode_qr_from_base64
)
from ..services.theme_manager import (
    get_available_themes,
    get_theme_icon_base64
)
from ..services.greeting_service import get_greeting_stats

router = APIRouter(prefix="/qr", tags=["qr"])


@router.post("/generate", response_model=QRGenerateResponse)
async def generate_qr(request: QRGenerateRequest):
    """
    Generate a QR code with optional theme icon

    Args:
        request: QR generation parameters

    Returns:
        Base64-encoded PNG image with stats
    """
    try:
        # Generate QR code
        qr_img = generate_qr_code(
            data=request.data,
            theme=request.theme,
            error_correction=request.error_correction
        )

        # Convert to base64
        img_base64 = qr_image_to_base64(qr_img)

        # Get stats
        stats = get_greeting_stats(request.data)
        stats["theme"] = request.theme
        stats["error_correction"] = request.error_correction

        return QRGenerateResponse(
            image_base64=img_base64,
            stats=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR generation failed: {str(e)}")


@router.get("/themes", response_model=ThemeListResponse)
async def list_themes():
    """
    Get list of available themes

    Returns:
        List of theme metadata
    """
    themes = get_available_themes()
    return ThemeListResponse(themes=themes)


@router.get("/themes/{theme}/icon")
async def get_theme_icon(theme: str, size: int = 60):
    """
    Get theme icon preview as base64

    Args:
        theme: Theme name
        size: Icon size in pixels

    Returns:
        JSON with base64-encoded icon
    """
    icon_base64 = get_theme_icon_base64(theme, size)

    if icon_base64 is None:
        raise HTTPException(status_code=404, detail=f"Icon not found for theme '{theme}'")

    return {
        "theme": theme,
        "size": size,
        "icon_base64": icon_base64
    }


@router.post("/decode", response_model=QRDecodeResponse)
async def decode_qr(request: QRDecodeRequest):
    """
    Decode QR code from uploaded image

    Args:
        request: Base64-encoded image

    Returns:
        Decoded data or error
    """
    try:
        data = decode_qr_from_base64(request.image_base64)

        if data is None:
            return QRDecodeResponse(success=False, data=None)

        return QRDecodeResponse(success=True, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR decoding failed: {str(e)}")
