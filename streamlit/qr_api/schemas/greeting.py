#!/usr/bin/env python3
"""
Pydantic schemas for greeting operations
"""
from pydantic import BaseModel, Field
from typing import Optional

class GreetingEncodeRequest(BaseModel):
    """Request to encode a greeting to URL"""
    from_name: str = Field(..., description="Sender's name")
    to_name: str = Field(..., description="Recipient's name")
    message: str = Field(..., description="Greeting message")
    theme: str = Field(default="general", description="Theme identifier")
    base_url: Optional[str] = Field(None, description="Base URL for greeting app")

class GreetingEncodeResponse(BaseModel):
    """Response containing encoded greeting URL"""
    url: str = Field(..., description="Full URL with encoded greeting")
    stats: dict = Field(..., description="Greeting statistics")

class GreetingDecodeRequest(BaseModel):
    """Request to decode a greeting from query params"""
    query_params: dict = Field(..., description="URL query parameters")

class GreetingDecodeResponse(BaseModel):
    """Response containing decoded greeting"""
    greeting: Optional[dict] = Field(None, description="Decoded greeting data")
    success: bool = Field(..., description="Whether decoding succeeded")

class GreetingValidateRequest(BaseModel):
    """Request to validate greeting size"""
    message: str = Field(..., description="Message to validate")
    from_name: str = Field(default="", description="Sender's name")
    to_name: str = Field(default="", description="Recipient's name")
    theme: str = Field(default="general", description="Theme identifier")

class GreetingValidateResponse(BaseModel):
    """Response containing validation results"""
    valid: bool = Field(..., description="Whether greeting fits in QR code")
    stats: dict = Field(..., description="Size statistics")
