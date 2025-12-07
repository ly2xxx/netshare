#!/usr/bin/env python3
"""
Greeting JSON Schema Module
Handles creation and parsing of holiday greeting data in compact JSON format
"""

import json
from datetime import datetime
from typing import Dict, Optional


def create_holiday_greeting(
    from_name: str,
    to_name: str,
    message: str,
    theme: str = "general"
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
    return {
        "message": message,
        "from": from_name,
        "to": to_name,
        "theme": theme,
        "created": datetime.utcnow().isoformat()
    }


def compact_greeting(payload: Dict) -> str:
    """
    Minimize JSON payload by removing whitespace

    Args:
        payload: Greeting dictionary

    Returns:
        Compact JSON string
    """
    return json.dumps(payload, separators=(',', ':'))


def parse_greeting(qr_data: str) -> Optional[Dict]:
    """
    Parse raw text QR code into a greeting structure
    """
    if not qr_data:
        return None
        
    # Return structure compliant with expected app format, but with defaults
    return {
        "v": "1.0",
        "type": "greeting",
        "from": "", # Not stored in QR
        "to": "",   # Not stored in QR
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
