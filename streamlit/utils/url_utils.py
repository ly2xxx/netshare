"""
URL utility functions for background handling and link processing
Handles YouTube, Google Drive, Facebook, Instagram, and general web URL conversions
"""

import re
import urllib.parse
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
           any(domain in background_lower for domain in [
               'youtu.be', 'youtube.com', 'facebook.com', 'fb.watch', 'instagram.com'
           ])


def classify_background(background_str: str) -> str:
    """
    Classify background type based on URL pattern.

    Args:
        background_str: Background identifier (filename or URL)

    Returns:
        One of: 'local_file', 'youtube', 'google_drive', 'facebook', 'instagram',
                'direct_video', 'other_url', or 'invalid'
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

    # Check for Facebook URLs
    if 'facebook.com' in background_lower or 'fb.watch' in background_lower:
        # Verify it's a video/reel URL
        if any(pattern in background_lower for pattern in ['/reel/', '/videos/', '/watch', 'fb.watch']):
            return 'facebook'

    # Check for Instagram URLs
    if 'instagram.com' in background_lower:
        # Verify it's a reel/post/tv URL
        if any(pattern in background_lower for pattern in ['/reel/', '/p/', '/tv/']):
            return 'instagram'

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


def convert_facebook_to_embed_url(facebook_url: str) -> Optional[str]:
    """
    Convert Facebook video/reel URL to embeddable iframe URL.

    Supports:
    - https://www.facebook.com/reel/{ID}
    - https://www.facebook.com/{user}/videos/{ID}
    - https://www.facebook.com/watch?v={ID}
    - https://fb.watch/{SHORT_ID}

    Args:
        facebook_url: Facebook video/reel URL

    Returns:
        Embed URL using Facebook's video plugin, or None if invalid

    Notes:
        - Uses Facebook's plugin: https://www.facebook.com/plugins/video.php
        - Requires URL encoding of original Facebook URL
        - May not work for all Reels (Facebook limitation as of 2025)
    """
    if not facebook_url:
        return None

    # Normalize URL
    url_lower = facebook_url.lower()

    # Pattern 1: facebook.com/reel/{ID}
    reel_match = re.search(r'facebook\.com/reel/(\d+)', facebook_url)
    if reel_match:
        reel_id = reel_match.group(1)
        # Reconstruct canonical URL
        canonical_url = f"https://www.facebook.com/reel/{reel_id}"
        encoded_url = urllib.parse.quote(canonical_url, safe='')
        return f"https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=false&width=560"

    # Pattern 2: facebook.com/*/videos/{ID} or facebook.com/watch?v={ID}
    video_match = re.search(r'facebook\.com/(?:[\w.]+/videos/|watch\?v=)(\d+)', facebook_url)
    if video_match:
        # Use original URL for embedding (preserve full path)
        encoded_url = urllib.parse.quote(facebook_url, safe='')
        return f"https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=false&width=560"

    # Pattern 3: fb.watch/{SHORT_ID}
    fbwatch_match = re.search(r'fb\.watch/([a-zA-Z0-9_-]+)', facebook_url)
    if fbwatch_match:
        # fb.watch redirects to full URL, but plugin should handle it
        encoded_url = urllib.parse.quote(facebook_url, safe='')
        return f"https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=false&width=560"

    return None


def convert_instagram_to_embed_url(instagram_url: str) -> Optional[str]:
    """
    Convert Instagram reel/post URL to embeddable format.

    Supports:
    - https://www.instagram.com/reel/{ID}/
    - https://www.instagram.com/p/{ID}/
    - https://www.instagram.com/tv/{ID}/

    Args:
        instagram_url: Instagram reel/post URL

    Returns:
        Embed URL using Instagram's embed format, or None if invalid

    Notes:
        - Instagram embed requires /embed/ path suffix
        - May not work reliably without Meta oEmbed API (2025 limitation)
        - Fallback: Display message to user about opening in Instagram app
    """
    if not instagram_url:
        return None

    # Pattern: instagram.com/{type}/{ID}
    # Where type is: reel, p (post), tv (IGTV)
    # ID is alphanumeric (usually 11 chars but can vary)
    match = re.search(r'instagram\.com/(reel|p|tv)/([a-zA-Z0-9_-]+)', instagram_url)

    if match:
        content_type = match.group(1)
        content_id = match.group(2)

        # Instagram embed URL pattern
        # Note: This may not work without Meta API access in 2025
        return f"https://www.instagram.com/{content_type}/{content_id}/embed/"

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
