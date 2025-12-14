#!/usr/bin/env python3
"""
Greeting encoding and decoding endpoints
"""
from fastapi import APIRouter, HTTPException
from ..schemas.greeting import (
    GreetingEncodeRequest,
    GreetingEncodeResponse,
    GreetingDecodeRequest,
    GreetingDecodeResponse,
    GreetingValidateRequest,
    GreetingValidateResponse
)
from ..services.greeting_service import (
    create_holiday_greeting,
    encode_greeting_to_url,
    decode_greeting_from_url,
    get_greeting_stats
)
from ..config import GREETING_APP_URL

router = APIRouter(prefix="/greeting", tags=["greeting"])


@router.post("/encode", response_model=GreetingEncodeResponse)
async def encode_greeting(request: GreetingEncodeRequest):
    """
    Encode greeting to URL format

    Args:
        request: Greeting data

    Returns:
        URL with encoded greeting
    """
    try:
        greeting = create_holiday_greeting(
            from_name=request.from_name,
            to_name=request.to_name,
            message=request.message,
            theme=request.theme
        )

        base_url = request.base_url or GREETING_APP_URL
        url = encode_greeting_to_url(greeting, base_url)

        stats = get_greeting_stats(url)

        return GreetingEncodeResponse(url=url, stats=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encoding failed: {str(e)}")


@router.post("/decode", response_model=GreetingDecodeResponse)
async def decode_greeting(request: GreetingDecodeRequest):
    """
    Decode greeting from query parameters

    Args:
        request: Query parameters dictionary

    Returns:
        Decoded greeting data
    """
    try:
        greeting = decode_greeting_from_url(request.query_params)

        if greeting is None:
            return GreetingDecodeResponse(success=False, greeting=None)

        return GreetingDecodeResponse(success=True, greeting=greeting)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decoding failed: {str(e)}")


@router.post("/validate", response_model=GreetingValidateResponse)
async def validate_greeting(request: GreetingValidateRequest):
    """
    Validate if greeting will fit in QR code

    Args:
        request: Greeting data to validate

    Returns:
        Validation result with stats
    """
    try:
        greeting = create_holiday_greeting(
            from_name=request.from_name,
            to_name=request.to_name,
            message=request.message,
            theme=request.theme
        )

        url = encode_greeting_to_url(greeting)
        stats = get_greeting_stats(url)

        return GreetingValidateResponse(
            valid=stats["fits_in_qr"],
            stats=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
