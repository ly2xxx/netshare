"""
Greeting encoding/decoding service

Handles URL encoding and decoding for greeting messages.
Adapted from greeting_formats.py for API use.
"""

import json
import base64
import zlib
from datetime import datetime
from typing import Dict, Optional
from urllib.parse import urlencode, parse_qs, quote, unquote, urlparse

from ..config import GREETING_APP_URL


class GreetingService:
    """
    Service for encoding and decoding greeting messages.
    
    Provides URL encoding with compression for efficient QR code data.
    """
    
    def __init__(self, base_url: str = GREETING_APP_URL):
        """
        Initialize greeting service.
        
        Args:
            base_url: Base URL for the greeting app
        """
        self.base_url = base_url
    
    def create_greeting(
        self,
        from_name: str,
        to_name: str,
        message: str,
        theme: str = "general"
    ) -> Dict:
        """
        Create a structured greeting payload.
        
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
    
    def encode_to_url(self, greeting: Dict) -> str:
        """
        Encode greeting data into a URL with compressed query parameters.
        
        Args:
            greeting: Greeting dictionary with from, to, message, theme
            
        Returns:
            Full URL with encoded greeting data
        """
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
        
        query = urlencode(params, safe='')
        
        # Add message parameter (already formatted)
        full_url = f"{self.base_url}?{query}&{msg_param}"
        
        return full_url
    
    def decode_from_url(self, url_or_params: str | Dict) -> Optional[Dict]:
        """
        Decode greeting data from URL or query parameters.
        
        Args:
            url_or_params: Full URL string or dictionary of query parameters
            
        Returns:
            Greeting dictionary or None if invalid
        """
        try:
            # Handle full URL string
            if isinstance(url_or_params, str):
                parsed = urlparse(url_or_params)
                query_params = parse_qs(parsed.query)
            else:
                query_params = url_or_params
            
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
    
    def get_stats(self, url: str) -> Dict:
        """
        Get statistics about the greeting URL size.
        
        Args:
            url: Encoded greeting URL
            
        Returns:
            Dictionary with size statistics
        """
        byte_size = len(url.encode('utf-8'))
        
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
            "char_count": len(url),
            "recommended_qr_version": recommended_version,
            "fits_in_qr": byte_size <= 1852  # Max capacity of V40-H
        }


# Singleton instance for convenience
_greeting_service: Optional[GreetingService] = None


def get_greeting_service() -> GreetingService:
    """Get or create singleton GreetingService instance."""
    global _greeting_service
    if _greeting_service is None:
        _greeting_service = GreetingService()
    return _greeting_service
