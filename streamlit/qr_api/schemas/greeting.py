"""
Pydantic schemas for greeting encoding/decoding endpoints
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class GreetingStats(BaseModel):
    """Statistics about the encoded greeting"""
    byte_size: int = Field(description="Size of encoded URL in bytes")
    char_count: int = Field(description="Character count of encoded URL")
    recommended_qr_version: int = Field(
        description="Recommended QR version for this data size"
    )
    fits_in_qr: bool = Field(
        description="Whether data fits in maximum QR capacity"
    )


class GreetingEncodeRequest(BaseModel):
    """Request model for encoding a greeting to URL"""
    from_name: str = Field(
        ...,
        description="Sender's name",
        min_length=1,
        max_length=100,
        examples=["Alice"]
    )
    to_name: str = Field(
        ...,
        description="Recipient's name",
        min_length=1,
        max_length=100,
        examples=["Bob"]
    )
    message: str = Field(
        ...,
        description="Greeting message",
        min_length=1,
        max_length=1000,
        examples=["Merry Christmas! Wishing you joy and happiness!"]
    )
    theme: str = Field(
        default="general",
        description="Theme identifier",
        examples=["snowflake", "hearts", "general"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "from_name": "Alice",
                    "to_name": "Bob",
                    "message": "Merry Christmas! Wishing you joy and happiness!",
                    "theme": "snowflake"
                }
            ]
        }
    }


class GreetingEncodeResponse(BaseModel):
    """Response model for greeting encoding"""
    success: bool = Field(default=True)
    url: str = Field(description="Encoded URL for QR code")
    stats: GreetingStats


class GreetingDecodeRequest(BaseModel):
    """Request model for decoding a greeting from URL"""
    url: str = Field(
        ...,
        description="Full URL or query string containing encoded greeting",
        examples=["https://qr-greeting.streamlit.app/?tab=scan&f=Alice&t=Bob&th=snowflake&m=Hello"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://qr-greeting.streamlit.app/?tab=scan&f=Alice&t=Bob&th=snowflake&m=Hello"
                }
            ]
        }
    }


class GreetingData(BaseModel):
    """Full greeting data structure"""
    v: str = Field(default="1.0", description="Schema version")
    type: str = Field(default="greeting", description="Data type identifier")
    from_name: str = Field(alias="from", description="Sender's name")
    to_name: str = Field(alias="to", description="Recipient's name")
    message: str = Field(description="Greeting message")
    theme: str = Field(description="Theme identifier")
    created: str = Field(description="ISO timestamp of creation")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "v": "1.0",
                    "type": "greeting",
                    "from": "Alice",
                    "to": "Bob",
                    "message": "Merry Christmas!",
                    "theme": "snowflake",
                    "created": "2024-12-14T15:00:00Z"
                }
            ]
        }
    }


class GreetingDecodeResponse(BaseModel):
    """Response model for greeting decoding"""
    success: bool
    greeting: Optional[GreetingData] = Field(
        default=None,
        description="Decoded greeting data (None if decoding failed)"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if decoding failed"
    )
