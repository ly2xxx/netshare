"""
Video utility functions for Marketing Funnel feature
Handles video URL validation and metadata extraction
"""

import re
from typing import Tuple, Optional
from utils.url_utils import (
    convert_youtube_to_embed_url,
    convert_google_drive_to_embed_url
)


def validate_video_url(url: str) -> Tuple[bool, str, str]:
    """
    Validate if a URL is a supported video source.
    
    Args:
        url: Video URL to validate
        
    Returns:
        Tuple of (is_valid, video_type, error_message)
        video_type is one of: 'YouTube', 'Vimeo', 'Direct Video', 'Google Drive'
    """
    if not url:
        return False, "", "No URL provided"
    
    url_lower = url.lower()
    
    # YouTube
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        embed_url = convert_youtube_to_embed_url(url)
        if embed_url:
            return True, "YouTube", ""
        else:
            return False, "", "Invalid YouTube URL format"
    
    # Vimeo
    if 'vimeo.com' in url_lower:
        vimeo_match = re.search(r'vimeo\.com/(\d+)', url)
        if vimeo_match:
            return True, "Vimeo", ""
        else:
            return False, "", "Invalid Vimeo URL format"
    
    # Google Drive
    if 'drive.google.com' in url_lower:
        embed_url = convert_google_drive_to_embed_url(url)
        if embed_url:
            return True, "Google Drive", ""
        else:
            return False, "", "Invalid Google Drive URL format"
    
    # Direct video files
    video_extensions = ['.mp4', '.webm', '.mov', '.m4v', '.avi']
    if any(url_lower.endswith(ext) for ext in video_extensions):
        return True, "Direct Video", ""
    
    # Check for video in URL path (some CDNs)
    if any(ext in url_lower for ext in video_extensions):
        return True, "Direct Video", ""
    
    return False, "", "Unsupported video URL. Use YouTube, Vimeo, Google Drive, or direct video links (.mp4, .webm)"


def get_youtube_thumbnail(video_id: str, quality: str = "hq") -> str:
    """Get YouTube video thumbnail URL."""
    quality_map = {
        "maxres": "maxresdefault",
        "hq": "hqdefault",
        "mq": "mqdefault",
        "sd": "sddefault",
        "default": "default"
    }
    quality_slug = quality_map.get(quality, "hqdefault")
    return f"https://img.youtube.com/vi/{video_id}/{quality_slug}.jpg"


def convert_to_embed_url(url: str) -> Optional[str]:
    """Convert any supported video URL to embeddable format."""
    if not url:
        return None
        
    is_valid, video_type, _ = validate_video_url(url)
    
    if not is_valid:
        return None
    
    if video_type == "YouTube":
        return convert_youtube_to_embed_url(url)
    
    if video_type == "Vimeo":
        vimeo_match = re.search(r'vimeo\.com/(\d+)', url)
        if vimeo_match:
            return f"https://player.vimeo.com/video/{vimeo_match.group(1)}"
    
    if video_type == "Google Drive":
        return convert_google_drive_to_embed_url(url)
    
    if video_type == "Direct Video":
        return url
    
    return None
