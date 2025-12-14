"""
Pydantic schemas for QR code generation endpoints
"""

from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel, Field


class ErrorCorrectionLevel(str, Enum):
    """QR code error correction levels"""
    L = "L"  # ~7% recovery
    M = "M"  # ~15% recovery
    Q = "Q"  # ~25% recovery
    H = "H"  # ~30% recovery (default, best for icons)


class QRGenerateRequest(BaseModel):
    """Request model for QR code generation"""
    data: str = Field(
        ...,
        description="Data string to encode in QR code",
        min_length=1,
        max_length=2000,
        examples=["https://example.com"]
    )
    theme: str = Field(
        default="general",
        description="Theme for icon embedding (snowflake, fireworks, hearts, etc.)",
        examples=["snowflake", "general"]
    )
    error_correction: ErrorCorrectionLevel = Field(
        default=ErrorCorrectionLevel.H,
        description="Error correction level (H recommended for icon embedding)"
    )
    output_format: str = Field(
        default="base64",
        description="Output format: 'base64' (JSON response) or 'binary' (raw PNG)",
        pattern="^(base64|binary)$"
    )
    size: Optional[int] = Field(
        default=None,
        description="Target size in pixels (None for auto-size based on data)",
        ge=100,
        le=2000
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": "https://qr-greeting.streamlit.app/?f=Alice&t=Bob&m=Hello",
                    "theme": "snowflake",
                    "error_correction": "H",
                    "output_format": "base64"
                }
            ]
        }
    }


class QRDimensions(BaseModel):
    """QR code image dimensions"""
    width: int
    height: int


class QRGenerateResponse(BaseModel):
    """Response model for QR code generation"""
    success: bool = Field(default=True)
    image_base64: Optional[str] = Field(
        default=None,
        description="Base64 encoded PNG image (when output_format=base64)"
    )
    mime_type: str = Field(default="image/png")
    dimensions: QRDimensions
    qr_version: int = Field(
        description="QR code version (1-40, higher = more data capacity)"
    )
    data_size_bytes: int = Field(
        description="Size of encoded data in bytes"
    )
    theme_applied: str = Field(
        description="Theme that was applied (or 'general' if none)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
                    "mime_type": "image/png",
                    "dimensions": {"width": 500, "height": 500},
                    "qr_version": 15,
                    "data_size_bytes": 245,
                    "theme_applied": "snowflake"
                }
            ]
        }
    }


class ThemeInfo(BaseModel):
    """Information about a single theme"""
    key: str = Field(description="Theme identifier")
    emoji: Optional[str] = Field(description="Emoji representation")
    label: str = Field(description="Human-readable label")
    has_icon: bool = Field(description="Whether theme has an embeddable icon")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "key": "snowflake",
                    "emoji": "❄️",
                    "label": "Snowflake",
                    "has_icon": True
                }
            ]
        }
    }


class ThemeListResponse(BaseModel):
    """Response containing list of available themes"""
    themes: list[ThemeInfo]
    total: int = Field(description="Total number of themes")
