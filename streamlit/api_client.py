#!/usr/bin/env python3
"""
HTTP client wrapper for QR API
Handles retries, timeouts, and error handling
"""
import httpx
import base64
from typing import Optional, Dict, Any
from PIL import Image
import io


class QRApiClient:
    """Client for QR code generation API"""

    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: float = 5.0):
        """
        Initialize API client

        Args:
            base_url: Base URL for API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.api_prefix = f"{base_url}/api/v1"
        self.timeout = timeout
        self._client = None

    def _get_client(self) -> httpx.Client:
        """Get or create HTTP client"""
        if self._client is None:
            self._client = httpx.Client(timeout=self.timeout)
        return self._client

    def close(self):
        """Close HTTP client"""
        if self._client is not None:
            self._client.close()
            self._client = None

    def health_check(self) -> bool:
        """
        Check if API is healthy

        Returns:
            True if API is responsive
        """
        try:
            response = self._get_client().get(f"{self.api_prefix}/health")
            return response.status_code == 200
        except Exception:
            return False

    def generate_qr(
        self,
        data: str,
        theme: str = "general",
        error_correction: str = "H",
        retries: int = 2
    ) -> Optional[Image.Image]:
        """
        Generate QR code via API

        Args:
            data: Data to encode
            theme: Theme name
            error_correction: Error correction level
            retries: Number of retry attempts

        Returns:
            PIL Image or None if failed
        """
        payload = {
            "data": data,
            "theme": theme,
            "error_correction": error_correction
        }

        for attempt in range(retries + 1):
            try:
                response = self._get_client().post(
                    f"{self.api_prefix}/qr/generate",
                    json=payload
                )

                if response.status_code == 200:
                    result = response.json()
                    img_base64 = result["image_base64"]

                    # Decode base64 to PIL Image
                    img_bytes = base64.b64decode(img_base64)
                    return Image.open(io.BytesIO(img_bytes))

            except Exception as e:
                if attempt == retries:
                    print(f"[API Client] QR generation failed after {retries + 1} attempts: {e}")
                    return None
                # Wait before retry (exponential backoff)
                import time
                time.sleep(0.1 * (2 ** attempt))

        return None

    def get_themes(self, retries: int = 2) -> Optional[list]:
        """
        Get list of available themes

        Args:
            retries: Number of retry attempts

        Returns:
            List of theme dicts or None
        """
        for attempt in range(retries + 1):
            try:
                response = self._get_client().get(f"{self.api_prefix}/qr/themes")

                if response.status_code == 200:
                    result = response.json()
                    return result["themes"]

            except Exception as e:
                if attempt == retries:
                    print(f"[API Client] Get themes failed: {e}")
                    return None

        return None

    def encode_greeting(
        self,
        from_name: str,
        to_name: str,
        message: str,
        theme: str = "general",
        base_url: Optional[str] = None,
        retries: int = 2
    ) -> Optional[Dict[str, Any]]:
        """
        Encode greeting to URL

        Args:
            from_name: Sender name
            to_name: Recipient name
            message: Message content
            theme: Theme name
            base_url: Base URL for greeting app
            retries: Number of retry attempts

        Returns:
            Dict with 'url' and 'stats' or None
        """
        payload = {
            "from_name": from_name,
            "to_name": to_name,
            "message": message,
            "theme": theme
        }

        if base_url:
            payload["base_url"] = base_url

        for attempt in range(retries + 1):
            try:
                response = self._get_client().post(
                    f"{self.api_prefix}/greeting/encode",
                    json=payload
                )

                if response.status_code == 200:
                    return response.json()

            except Exception as e:
                if attempt == retries:
                    print(f"[API Client] Encode greeting failed: {e}")
                    return None

        return None

    def decode_greeting(
        self,
        query_params: Dict,
        retries: int = 2
    ) -> Optional[Dict]:
        """
        Decode greeting from query parameters

        Args:
            query_params: Query parameter dict
            retries: Number of retry attempts

        Returns:
            Greeting dict or None
        """
        payload = {"query_params": query_params}

        for attempt in range(retries + 1):
            try:
                response = self._get_client().post(
                    f"{self.api_prefix}/greeting/decode",
                    json=payload
                )

                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        return result["greeting"]

            except Exception as e:
                if attempt == retries:
                    print(f"[API Client] Decode greeting failed: {e}")
                    return None

        return None

    def validate_greeting(
        self,
        message: str,
        from_name: str = "",
        to_name: str = "",
        theme: str = "general",
        retries: int = 2
    ) -> Optional[Dict]:
        """
        Validate if greeting fits in QR code

        Args:
            message: Message content
            from_name: Sender name
            to_name: Recipient name
            theme: Theme name
            retries: Number of retry attempts

        Returns:
            Dict with 'valid' and 'stats' or None
        """
        payload = {
            "message": message,
            "from_name": from_name,
            "to_name": to_name,
            "theme": theme
        }

        for attempt in range(retries + 1):
            try:
                response = self._get_client().post(
                    f"{self.api_prefix}/greeting/validate",
                    json=payload
                )

                if response.status_code == 200:
                    return response.json()

            except Exception as e:
                if attempt == retries:
                    print(f"[API Client] Validate greeting failed: {e}")
                    return None

        return None

    def decode_qr(self, image_base64: str, retries: int = 2) -> Optional[str]:
        """
        Decode QR code from image

        Args:
            image_base64: Base64-encoded image
            retries: Number of retry attempts

        Returns:
            Decoded data or None
        """
        payload = {"image_base64": image_base64}

        for attempt in range(retries + 1):
            try:
                response = self._get_client().post(
                    f"{self.api_prefix}/qr/decode",
                    json=payload
                )

                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        return result["data"]

            except Exception as e:
                if attempt == retries:
                    print(f"[API Client] Decode QR failed: {e}")
                    return None

        return None
