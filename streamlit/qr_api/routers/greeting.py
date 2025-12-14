"""
Greeting Encoding/Decoding Router

Endpoints for encoding greetings to URLs and decoding from URLs.
"""

from fastapi import APIRouter, HTTPException

from ..schemas.greeting import (
    GreetingEncodeRequest,
    GreetingEncodeResponse,
    GreetingDecodeRequest,
    GreetingDecodeResponse,
    GreetingData,
    GreetingStats
)
from ..services.greeting_service import get_greeting_service


router = APIRouter(prefix="/greeting", tags=["Greeting"])


@router.post(
    "/encode",
    response_model=GreetingEncodeResponse,
    summary="Encode Greeting to URL",
    description="Encode greeting data into a URL suitable for QR code generation."
)
async def encode_greeting(request: GreetingEncodeRequest):
    """
    Encode a greeting message into a compressed URL.
    
    The URL can be used directly as QR code data. Long messages are
    automatically compressed using zlib + base64 to minimize QR code size.
    
    - **from_name**: Sender's name
    - **to_name**: Recipient's name  
    - **message**: Greeting message text
    - **theme**: Visual theme identifier
    """
    greeting_service = get_greeting_service()
    
    try:
        # Create greeting payload
        greeting = greeting_service.create_greeting(
            from_name=request.from_name,
            to_name=request.to_name,
            message=request.message,
            theme=request.theme
        )
        
        # Encode to URL
        url = greeting_service.encode_to_url(greeting)
        
        # Get statistics
        stats_data = greeting_service.get_stats(url)
        stats = GreetingStats(**stats_data)
        
        return GreetingEncodeResponse(
            success=True,
            url=url,
            stats=stats
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encoding failed: {str(e)}")


@router.post(
    "/decode",
    response_model=GreetingDecodeResponse,
    summary="Decode Greeting from URL",
    description="Decode greeting data from a URL or query parameters."
)
async def decode_greeting(request: GreetingDecodeRequest):
    """
    Decode a greeting from an encoded URL.
    
    Supports both compressed (mc parameter) and plain (m parameter) messages.
    
    - **url**: Full URL or query string containing encoded greeting
    """
    greeting_service = get_greeting_service()
    
    try:
        # Decode from URL
        greeting_data = greeting_service.decode_from_url(request.url)
        
        if greeting_data is None:
            return GreetingDecodeResponse(
                success=False,
                greeting=None,
                error="Could not decode greeting from URL. Invalid or missing parameters."
            )
        
        # Convert to response model
        greeting = GreetingData(
            v=greeting_data.get("v", "1.0"),
            type=greeting_data.get("type", "greeting"),
            **{"from": greeting_data.get("from", "")},
            **{"to": greeting_data.get("to", "")},
            message=greeting_data.get("message", ""),
            theme=greeting_data.get("theme", "general"),
            created=greeting_data.get("created", "")
        )
        
        return GreetingDecodeResponse(
            success=True,
            greeting=greeting
        )
    
    except Exception as e:
        return GreetingDecodeResponse(
            success=False,
            greeting=None,
            error=f"Decoding failed: {str(e)}"
        )
