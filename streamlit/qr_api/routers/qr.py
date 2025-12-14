"""
QR Code Generation Router

Endpoints for QR code generation and theme management.
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
import io

from ..schemas.qr import (
    QRGenerateRequest,
    QRGenerateResponse,
    QRDimensions,
    ThemeInfo,
    ThemeListResponse
)
from ..services.qr_generator import get_qr_service
from ..services.theme_manager import get_theme_manager


router = APIRouter(prefix="/qr", tags=["QR Code"])


@router.post(
    "/generate",
    response_model=QRGenerateResponse,
    summary="Generate QR Code",
    description="Generate a QR code image with optional theme icon embedding."
)
async def generate_qr_code(request: QRGenerateRequest):
    """
    Generate a QR code from the provided data.
    
    - **data**: The string data to encode (URL, text, etc.)
    - **theme**: Theme for icon embedding (snowflake, hearts, etc.)
    - **error_correction**: Error correction level (L, M, Q, H)
    - **output_format**: Response format (base64 JSON or binary PNG)
    - **size**: Optional target image size in pixels
    """
    qr_service = get_qr_service()
    
    try:
        if request.output_format == "binary":
            # Return raw PNG bytes
            img_bytes, metadata = qr_service.generate_bytes(
                data=request.data,
                theme=request.theme,
                error_correction=request.error_correction.value,
                size=request.size
            )
            return Response(
                content=img_bytes,
                media_type="image/png",
                headers={
                    "X-QR-Version": str(metadata["qr_version"]),
                    "X-Theme-Applied": metadata["theme_applied"]
                }
            )
        else:
            # Return base64 encoded in JSON
            img_base64, metadata = qr_service.generate_base64(
                data=request.data,
                theme=request.theme,
                error_correction=request.error_correction.value,
                size=request.size
            )
            
            return QRGenerateResponse(
                success=True,
                image_base64=img_base64,
                mime_type="image/png",
                dimensions=QRDimensions(**metadata["dimensions"]),
                qr_version=metadata["qr_version"],
                data_size_bytes=metadata["data_size_bytes"],
                theme_applied=metadata["theme_applied"]
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR generation failed: {str(e)}")


@router.get(
    "/themes",
    response_model=ThemeListResponse,
    summary="List Available Themes",
    description="Get a list of all available themes for QR code icon embedding."
)
async def list_themes():
    """
    Get all available themes with their metadata.
    
    Each theme includes:
    - **key**: Theme identifier for API calls
    - **emoji**: Emoji representation
    - **label**: Human-readable name
    - **has_icon**: Whether an embeddable icon is available
    """
    theme_manager = get_theme_manager()
    themes_data = theme_manager.get_all_themes()
    
    themes = [ThemeInfo(**t) for t in themes_data]
    
    return ThemeListResponse(themes=themes, total=len(themes))


@router.get(
    "/themes/{theme_key}",
    response_model=ThemeInfo,
    summary="Get Theme Info",
    description="Get information about a specific theme."
)
async def get_theme(theme_key: str):
    """
    Get detailed information about a specific theme.
    
    - **theme_key**: Theme identifier (e.g., "snowflake", "hearts")
    """
    theme_manager = get_theme_manager()
    theme_info = theme_manager.get_theme_info(theme_key)
    
    if theme_info is None:
        raise HTTPException(status_code=404, detail=f"Theme '{theme_key}' not found")
    
    return ThemeInfo(**theme_info)


@router.get(
    "/themes/{theme_key}/icon",
    summary="Get Theme Icon",
    description="Get the PNG icon image for a theme.",
    responses={
        200: {"content": {"image/png": {}}},
        404: {"description": "Theme or icon not found"}
    }
)
async def get_theme_icon(theme_key: str, size: int = 60):
    """
    Get the theme icon as a PNG image.
    
    - **theme_key**: Theme identifier
    - **size**: Icon size in pixels (default: 60)
    """
    if size < 16 or size > 500:
        raise HTTPException(status_code=400, detail="Size must be between 16 and 500 pixels")
    
    theme_manager = get_theme_manager()
    
    # Check theme exists
    if theme_key not in theme_manager.THEME_ICONS:
        raise HTTPException(status_code=404, detail=f"Theme '{theme_key}' not found")
    
    if theme_key == "general":
        raise HTTPException(status_code=404, detail="General theme has no icon")
    
    # Get icon bytes
    icon_bytes = theme_manager.get_icon_as_bytes(theme_key, size)
    
    if icon_bytes is None:
        raise HTTPException(status_code=404, detail=f"Icon not found for theme '{theme_key}'")
    
    return Response(content=icon_bytes, media_type="image/png")
