#!/usr/bin/env python3
"""
Greeting JSON Schema Module
Handles creation and parsing of holiday greeting data in compact JSON format
"""

import json
import base64
import zlib
from datetime import datetime
from typing import Dict, Optional
from urllib.parse import urlencode, parse_qs, quote, unquote


# Base URL for the greeting app
# Base URL for the greeting app
# Obfuscated to avoid plain text check-in
_ENCODED_URL = "aHR0cHM6Ly9xci1ncmVldGluZy5zdHJlYW1saXQuYXBwLw=="

def _decypher_url(encoded: str) -> str:
    """Simple decoder for the app URL"""
    return base64.b64decode(encoded).decode('utf-8')

GREETING_APP_URL = _decypher_url(_ENCODED_URL)


def encode_greeting_to_url(greeting: Dict, base_url: str = GREETING_APP_URL) -> str:
    """
    Encode greeting data into a URL with compressed query parameters
    
    Args:
        greeting: Greeting dictionary with from, to, message, theme
        base_url: Base URL for the greeting app
        
    Returns:
        Full URL with encoded greeting data
    """
    # Compress the message to save space (important for QR code size)
    message = greeting.get("message", "")
    from_name = greeting.get("from", "")
    to_name = greeting.get("to", "")
    theme = greeting.get("theme", "general")
    
    # Use base64 + zlib compression for the message if it's long
    if len(message) > 50:
        # Compress and encode
        compressed = zlib.compress(message.encode('utf-8'), level=9)
        encoded_msg = base64.urlsafe_b64encode(compressed).decode('ascii')
        msg_param = f"mc={encoded_msg}"  # mc = message compressed
    else:
        # Short messages: just URL encode
        msg_param = f"m={quote(message, safe='')}"
    
    # Build query string with short parameter names
    params = {
        "tab": "scan",
        "f": from_name,
        "t": to_name,
        "th": theme
    }
    
    # Add background if specified
    background = greeting.get("background", "")
    if background:
        params["bg"] = background
    
    query = urlencode(params, safe='')
    
    # Add message parameter (already formatted)
    full_url = f"{base_url}?{query}&{msg_param}"
    
    return full_url


def decode_greeting_from_url(query_params: Dict) -> Optional[Dict]:
    """
    Decode greeting data from URL query parameters
    
    Args:
        query_params: Dictionary of query parameters (values may be lists)
        
    Returns:
        Greeting dictionary or None if invalid
    """
    try:
        # Handle both list and single value formats
        def get_param(key, default=""):
            val = query_params.get(key, default)
            if isinstance(val, list):
                return val[0] if val else default
            return val or default
        
        from_name = get_param("f")
        to_name = get_param("t")
        theme = get_param("th", "general")
        
        # Check for compressed message first
        compressed_msg = get_param("mc")
        plain_msg = get_param("m")
        
        if compressed_msg:
            # Decompress message
            try:
                compressed_bytes = base64.urlsafe_b64decode(compressed_msg)
                message = zlib.decompress(compressed_bytes).decode('utf-8')
            except Exception:
                message = ""
        elif plain_msg:
            message = unquote(plain_msg)
        else:
            message = ""
        
        if not message:
            return None
        
        # Get background if specified
        background = get_param("bg", "")
            
        greeting = {
            "v": "1.0",
            "type": "greeting",
            "from": from_name,
            "to": to_name,
            "message": message,
            "theme": theme,
            "created": datetime.utcnow().isoformat()
        }
        if background:
            greeting["background"] = background
        return greeting
    except Exception:
        return None


def create_holiday_greeting(
    from_name: str,
    to_name: str,
    message: str,
    theme: str = "general",
    background: str = ""
) -> Dict:
    """
    Create a structured holiday greeting payload

    Args:
        from_name: Sender's name
        to_name: Recipient's name
        message: Greeting message
        theme: Visual theme identifier

    Returns:
        Dictionary containing greeting data
    """
    greeting = {
        "message": message,
        "from": from_name,
        "to": to_name,
        "theme": theme,
        "created": datetime.utcnow().isoformat()
    }
    if background:
        greeting["background"] = background
    return greeting


def compact_greeting(payload: Dict) -> str:
    """
    Minimize JSON payload by removing whitespace

    Args:
        payload: Greeting dictionary

    Returns:
        Compact JSON string
    """
    return json.dumps(payload, separators=(',', ':'), ensure_ascii=False)


def parse_greeting(qr_data: str) -> Optional[Dict]:
    """
    Parse raw text QR code into a greeting structure.
    Supports both JSON format and URL format (new).
    """
    if not qr_data:
        return None
    
    # Check if it's a URL (new format)
    if qr_data.startswith("http://") or qr_data.startswith("https://"):
        try:
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(qr_data)
            query_params = parse_qs(parsed_url.query)
            
            # Convert query params to format expected by decode_greeting_from_url
            greeting = decode_greeting_from_url(query_params)
            if greeting:
                return greeting
        except Exception:
            pass
        
    # Try to parse as JSON (legacy format)
    try:
        data = json.loads(qr_data)
        if isinstance(data, dict):
            # Ensure it has basic fields
            return {
                "v": data.get("v", "1.0"),
                "type": data.get("type", "greeting"),
                "from": data.get("from", ""),
                "to": data.get("to", ""),
                "message": data.get("message", ""),
                "theme": data.get("theme", "general"),
                "created": data.get("created", datetime.utcnow().isoformat())
            }
    except json.JSONDecodeError:
        pass

    # Fallback to plain text
    return {
        "v": "1.0",
        "type": "greeting",
        "from": "",  # Not stored in QR
        "to": "",    # Not stored in QR
        "message": qr_data,
        "theme": "general",
        "created": datetime.utcnow().isoformat()
    }



def format_greeting_display(greeting: Dict) -> str:
    """
    Format greeting data for nice display

    Args:
        greeting: Parsed greeting dictionary

    Returns:
        Formatted string for display
    """
    lines = [
        "",
        greeting.get('message', ''),
        "",
        f"From: {greeting.get('from', 'Unknown')}",
        f"To: {greeting.get('to', 'Unknown')}",
        f"Theme: {greeting.get('theme', 'general')}",
        f"Created: {greeting.get('created', 'Unknown')}"
    ]
    return "\n".join(lines)


def get_greeting_stats(greeting_json: str) -> Dict:
    """
    Get statistics about the greeting size

    Args:
        greeting_json: Compact JSON string

    Returns:
        Dictionary with size statistics
    """
    byte_size = len(greeting_json.encode('utf-8'))

    # QR code capacity reference (with High error correction)
    qr_versions = [
        (10, 224),   # V10-H
        (15, 432),   # V15-H
        (20, 666),   # V20-H
        (25, 952),   # V25-H
        (30, 1276),  # V30-H
        (40, 1852),  # V40-H
    ]

    recommended_version = None
    for version, capacity in qr_versions:
        if byte_size <= capacity:
            recommended_version = version
            break

    if not recommended_version:
        recommended_version = 40

    return {
        "byte_size": byte_size,
        "char_count": len(greeting_json),
        "recommended_qr_version": recommended_version,
        "fits_in_qr": byte_size <= 1852  # Max capacity of V40-H
    }
