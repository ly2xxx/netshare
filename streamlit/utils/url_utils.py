"""
URL utility functions for background handling and link processing
Handles YouTube, Google Drive, and general web URL conversions
"""

import re
from typing import Optional


def is_web_url(background_str: str) -> bool:
    """
    Check if a background string is a web URL.

    Args:
        background_str: Background identifier (filename or URL)

    Returns:
        True if the string is a web URL, False otherwise
    """
    if not background_str:
        return False
    background_lower = background_str.lower()
    return background_lower.startswith(('http://', 'https://')) or \
           'youtu.be' in background_lower or \
           'youtube.com' in background_lower


def classify_background(background_str: str) -> str:
    """
    Classify background type based on URL pattern.

    Args:
        background_str: Background identifier (filename or URL)

    Returns:
        One of: 'local_file', 'youtube', 'google_drive', 'direct_video', 'other_url', or 'invalid'
    """
    if not background_str:
        return 'invalid'

    if not is_web_url(background_str):
        return 'local_file'

    background_lower = background_str.lower()

    # Check for Google Drive URLs
    if 'drive.google.com' in background_lower and '/file/d/' in background_lower:
        return 'google_drive'

    # Check for YouTube URLs
    if 'youtube.com' in background_lower or 'youtu.be' in background_lower:
        return 'youtube'

    # Check for direct video URLs (by extension)
    if any(background_lower.endswith(ext) for ext in ['.mp4', '.webm', '.mov', '.avi', '.m3u8']):
        return 'direct_video'

    # Check if it's a generic URL
    if background_lower.startswith(('http://', 'https://')):
        return 'other_url'

    return 'invalid'


def convert_youtube_to_embed_url(youtube_url: str) -> Optional[str]:
    """
    Convert various YouTube URL formats to embeddable iframe URL.

    Handles:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - youtu.be/VIDEO_ID (without protocol)

    Args:
        youtube_url: YouTube URL in any supported format

    Returns:
        Embed URL in format https://www.youtube.com/embed/VIDEO_ID, or None if invalid
    """
    if not youtube_url:
        return None

    # YouTube video ID pattern: 11 characters (alphanumeric, hyphens, underscores)
    video_id_pattern = r'[a-zA-Z0-9_-]{11}'

    # Try different URL patterns
    patterns = [
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',  # youtube.com/watch?v=ID
        r'youtu\.be/([a-zA-Z0-9_-]{11})',              # youtu.be/ID
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',     # youtube.com/embed/ID
    ]

    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"

    return None


def convert_google_drive_to_embed_url(drive_url: str) -> Optional[str]:
    """
    Convert Google Drive share URL to embeddable preview URL.

    Input format: https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing
    Output format: https://drive.google.com/file/d/{FILE_ID}/preview

    Args:
        drive_url: Google Drive share URL

    Returns:
        Embed URL or None if FILE_ID cannot be extracted
    """
    # Pattern to extract FILE_ID from Google Drive URL
    # Matches: /file/d/{FILE_ID}/ where FILE_ID is alphanumeric with hyphens/underscores
    match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', drive_url)

    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/file/d/{file_id}/preview"

    return None


def linkify_urls(text: str) -> str:
    """
    Convert URLs in text to clickable HTML links.

    Args:
        text: Plain text that may contain URLs

    Returns:
        Text with URLs wrapped in <a> tags
    """
    # Regex pattern for http/https URLs
    # Matches: http:// or https:// followed by valid URL characters
    # Captures full URL including domain extensions (.com, .org, etc.)
    # Trailing punctuation is removed by cleanup code below
    url_pattern = r'(https?://[^\s<>\'"\)]+)'

    def replace_url(match):
        url = match.group(1)
        # Remove trailing punctuation that might have been captured
        while url and url[-1] in '.,;:!?)':
            url = url[:-1]
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: #667eea; text-decoration: underline;">{url}</a>'

    return re.sub(url_pattern, replace_url, text)
