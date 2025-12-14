#!/usr/bin/env python3
"""
Greeting encoding/decoding service
Extracted from greeting_formats.py
"""
import json
import base64
import zlib
from datetime import datetime
from typing import Dict, Optional
from urllib.parse import urlencode, parse_qs, quote, unquote
from ..config import GREETING_APP_URL


def encode_greeting_to_url(greeting: Dict, base_url: str = GREETING_APP_URL) -> str:
    """
    Encode greeting data into a URL with compressed query parameters

    Args:
        greeting: Greeting dictionary with from, to, message, theme
        base_url: Base URL for the greeting app

    Returns:
        Full URL with encoded greeting data
    """
    message = greeting.get("message", "")
    from_name = greeting.get("from", "")
    to_name = greeting.get("to", "")
    theme = greeting.get("theme", "general")

    # Use base64 + zlib compression for long messages
    if len(message) > 50:
        compressed = zlib.compress(message.encode('utf-8'), level=9)
        encoded_msg = base64.urlsafe_b64encode(compressed).decode('ascii')
        msg_param = f"mc={encoded_msg}"
    else:
        msg_param = f"m={quote(message, safe='')}"

    params = {
        "tab": "scan",
        "f": from_name,
        "t": to_name,
        "th": theme
    }

    query = urlencode(params, safe='')
    full_url = f"{base_url}?{query}&{msg_param}"

    return full_url


def decode_greeting_from_url(query_params: Dict) -> Optional[Dict]:
    """
    Decode greeting data from URL query parameters

    Args:
        query_params: Dictionary of query parameters

    Returns:
        Greeting dictionary or None if invalid
    """
    try:
        def get_param(key, default=""):
            val = query_params.get(key, default)
            if isinstance(val, list):
                return val[0] if val else default
            return val or default

        from_name = get_param("f")
        to_name = get_param("t")
        theme = get_param("th", "general")

        compressed_msg = get_param("mc")
        plain_msg = get_param("m")

        if compressed_msg:
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

        return {
            "v": "1.0",
            "type": "greeting",
            "from": from_name,
            "to": to_name,
            "message": message,
            "theme": theme,
            "created": datetime.utcnow().isoformat()
        }
    except Exception:
        return None


def create_holiday_greeting(
    from_name: str,
    to_name: str,
    message: str,
    theme: str = "general"
) -> Dict:
    """Create a structured holiday greeting payload"""
    return {
        "message": message,
        "from": from_name,
        "to": to_name,
        "theme": theme,
        "created": datetime.utcnow().isoformat()
    }


def compact_greeting(payload: Dict) -> str:
    """Minimize JSON payload by removing whitespace"""
    return json.dumps(payload, separators=(',', ':'), ensure_ascii=False)


def parse_greeting(qr_data: str) -> Optional[Dict]:
    """
    Parse raw QR code text into greeting structure
    Supports URL and JSON formats
    """
    if not qr_data:
        return None

    # Check if it's a URL
    if qr_data.startswith("http://") or qr_data.startswith("https://"):
        try:
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(qr_data)
            query_params = parse_qs(parsed_url.query)

            greeting = decode_greeting_from_url(query_params)
            if greeting:
                return greeting
        except Exception:
            pass

    # Try JSON format
    try:
        data = json.loads(qr_data)
        if isinstance(data, dict):
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
        "from": "",
        "to": "",
        "message": qr_data,
        "theme": "general",
        "created": datetime.utcnow().isoformat()
    }


def format_greeting_display(greeting: Dict) -> str:
    """Format greeting data for display"""
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
    """Get statistics about greeting size"""
    byte_size = len(greeting_json.encode('utf-8'))

    qr_versions = [
        (10, 224),
        (15, 432),
        (20, 666),
        (25, 952),
        (30, 1276),
        (40, 1852),
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
        "fits_in_qr": byte_size <= 1852
    }
