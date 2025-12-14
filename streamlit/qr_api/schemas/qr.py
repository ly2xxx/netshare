#!/usr/bin/env python3
"""
Pydantic schemas for QR code operations
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal

class QRGenerateRequest(BaseModel):
    """Request to generate a QR code"""
    data: str = Field(..., description="Data to encode in QR code")
    theme: str = Field(default="general", description="Theme icon to embed")
    error_correction: Literal["L", "M", "Q", "H"] = Field(
        default="H",
        description="Error correction level"
    )

class QRGenerateResponse(BaseModel):
    """Response containing generated QR code"""
    image_base64: str = Field(..., description="Base64-encoded PNG image")
    stats: dict = Field(..., description="QR code statistics")

class ThemeListResponse(BaseModel):
    """List of available themes"""
    themes: list[dict] = Field(..., description="List of theme metadata")

class QRDecodeRequest(BaseModel):
    """Request to decode a QR code from image"""
    image_base64: str = Field(..., description="Base64-encoded image")

class QRDecodeResponse(BaseModel):
    """Response containing decoded QR data"""
    data: Optional[str] = Field(None, description="Decoded data")
    success: bool = Field(..., description="Whether decoding succeeded")
