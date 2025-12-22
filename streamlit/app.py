#!/usr/bin/env python3
"""
Holiday Greeting QR Code Generator
A Streamlit app for creating and reading holiday greeting QR codes
"""

import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import json
from datetime import datetime
import numpy as np
import csv
import csv
from pathlib import Path
import base64
import os
import streamlit.components.v1 as components
from typing import Optional

# Import cv2 lazily to avoid startup crashes if system libs missing
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError as e:
    CV2_AVAILABLE = False
    CV2_IMPORT_ERROR = str(e)

from greeting_formats import (
    create_holiday_greeting,
    compact_greeting,
    parse_greeting,
    format_greeting_display,
    get_greeting_stats,
    encode_greeting_to_url,
    decode_greeting_from_url
)


# ============================================================================
# Download Tracking Functions
# ============================================================================

def log_download(filename: str) -> None:
    """
    Log a QR code download event to track.csv

    Args:
        filename: Name of the downloaded file

    Thread-safe implementation using file locking
    """
    # CSV file path (same directory as app.py)
    csv_path = Path(__file__).parent / "track.csv"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Create file with headers if it doesn't exist
        if not csv_path.exists():
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['filename', 'timestamp'])

        # Append with exclusive lock (prevents concurrent write corruption)
        with open(csv_path, 'a', newline='') as f:
            # Acquire exclusive lock (blocks other processes)
            try:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            except (ImportError, AttributeError):
                # fcntl not available on Windows, skip locking
                pass

            try:
                writer = csv.writer(f)
                writer.writerow([filename, timestamp])
            finally:
                # Release lock if fcntl is available
                try:
                    import fcntl
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (ImportError, AttributeError):
                    pass
    except Exception as e:
        # Silent failure - don't interrupt user experience
        import sys
        print(f"Warning: Failed to log download: {e}", file=sys.stderr)


def get_download_count() -> int:
    """
    Read and count total downloads from track.csv

    Returns:
        Number of downloads, or 0 if file doesn't exist or error occurs
    """
    csv_path = Path(__file__).parent / "track.csv"

    try:
        if not csv_path.exists():
            return 0

        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader, None)
            # Count remaining rows
            count = sum(1 for _ in reader)
            return count
    except Exception as e:
        # Return 0 on error (graceful degradation)
        import sys
        print(f"Warning: Failed to read download count: {e}", file=sys.stderr)
        return 0

# Theme to emoji mapping
THEME_ICONS = {
    "snowflake": "❄️",
    "fireworks": "🎆",
    "lights": "✨",
    "stars": "⭐",
    "confetti": "🎉",
    "champagne": "🥂",
    "hearts": "❤️",
    "farewell": "👋",
    "general": None  # No icon for general theme
}

# Page config
st.set_page_config(
    page_title="Holiday Greeting QR",
    page_icon="🎄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .greeting-box {
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stats-box {
        padding: 1rem;
        background: #e8eaf6;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .letter-container {
        background-color: #fdfbf7;
        padding: 40px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        min-height: 400px;
        position: relative;
        font-family: 'Georgia', serif;
        color: #333;
        margin-top: 20px;
    }
    .letter-header {
        margin-bottom: 30px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    .letter-from, .letter-to {
        font-size: 1.1em;
        margin: 5px 0;
    }
    .letter-body {
        font-size: 1.25em;
        line-height: 1.6;
        white-space: pre-wrap;
        margin-bottom: 60px;
    }
    .letter-watermark {
        position: absolute;
        bottom: 20px;
        right: 20px;
        opacity: 0.8;
        width: 100px;
        height: 100px;
    }
    .letter-footer {
        position: absolute;
        bottom: 20px;
        left: 20px;
        font-size: 0.8em;
        color: #888;
    }
    /* QR Code Protection - Global fallback */
    .qr-code-protected {
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        user-select: none;
        -webkit-user-drag: none;
    }
</style>
""", unsafe_allow_html=True)



def get_img_as_base64(file_path):
    """Read image file and return base64 string"""
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


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
        One of: 'local_file', 'youtube', 'direct_video', 'other_url', or 'invalid'
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
    import re

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
    import re

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
    import re
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


def display_qr_with_protection(qr_img: Image.Image, caption: str = "", width: int = None) -> None:
    """
    Display QR code image with right-click protection

    Args:
        qr_img: PIL Image object of QR code
        caption: Caption text to display below image
        width: Width in pixels (None for auto-width, matching Streamlit's 'stretch')

    Returns:
        None (renders HTML component directly)
    """
    # Convert PIL Image to base64 data URI
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()
    img_data_uri = f"data:image/png;base64,{img_base64}"

    # Get actual QR image dimensions
    img_width, img_height = qr_img.size

    # Use constrained width for consistent display
    # Max 500px width works well across devices (desktop and mobile)
    max_display_width = 500
    actual_display_width = min(img_width, max_display_width)

    # QR codes are square usually, but visible message increases height
    # Calculate height based on aspect ratio
    scaled_height = actual_display_width * (img_height / img_width) if img_width > 0 else actual_display_width

    # Add extra space for caption and margins
    caption_space = 80 if caption else 40
    iframe_height = scaled_height + caption_space

    # Build protected HTML with inline styles and JavaScript
    width_style = f"max-width: {max_display_width}px; width: 100%;"

    # Use id(qr_img) for unique element ID
    unique_id = f"qr-preview-{id(qr_img)}"

    html_code = f"""
    <div style="text-align: center; margin: 1rem 0;">
        <img
            id="{unique_id}"
            src="{img_data_uri}"
            alt="QR Code Preview"
            style="{width_style} height: auto; display: block; margin: 0 auto;
                   -webkit-touch-callout: none; -webkit-user-select: none;
                   -moz-user-select: none; -ms-user-select: none; user-select: none;
                   -webkit-user-drag: none; user-drag: none;"
            oncontextmenu="return false;"
            ondragstart="return false;"
        >
        {f'<p style="text-align: center; color: #666; font-size: 0.9em; margin-top: 0.5rem;">{caption}</p>' if caption else ''}
    </div>
    <script>
    (function() {{
        const img = document.getElementById('{unique_id}');
        if (img) {{
            img.addEventListener('contextmenu', e => {{ e.preventDefault(); return false; }});
            img.addEventListener('dragstart', e => {{ e.preventDefault(); return false; }});
            img.addEventListener('copy', e => {{ e.preventDefault(); return false; }});
        }}
    }})();
    </script>
    """

    components.html(html_code, height=iframe_height, scrolling=False)


def display_greeting_letter(greeting):
    """Display greeting in a letter format"""
    # Prepare icon for HTML
    theme_name = greeting.get('theme', 'general')
    icon_html = ""
    if theme_name in THEME_ICONS and theme_name != 'general':
        icon_path = os.path.join(os.path.dirname(__file__), "icons", f"{theme_name}.png")
        if os.path.exists(icon_path):
            b64_icon = get_img_as_base64(icon_path)
            icon_html = f'<img src="data:image/png;base64,{b64_icon}" class="letter-watermark">'

    # Handle background if specified
    background_html = ""
    background_style = ""
    background_name = greeting.get('background', '')

    if background_name:
        # Check if background is a web URL
        if is_web_url(background_name):
            bg_type = classify_background(background_name)

            if bg_type == 'youtube':
                # YouTube embed iframe
                embed_url = convert_youtube_to_embed_url(background_name)
                if embed_url:
                    # Extract video ID for playlist parameter (required for loop)
                    video_id = embed_url.split('/')[-1]
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}?autoplay=1&mute=1&loop=1&playlist={video_id}"
                        allow="autoplay; encrypted-media"
                        allowfullscreen
                    ></iframe>'''
            elif bg_type == 'google_drive':
                # Google Drive embed iframe
                embed_url = convert_google_drive_to_embed_url(background_name)
                if embed_url:
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}"
                        allowfullscreen
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    ></iframe>'''
            elif bg_type == 'direct_video':
                # Direct HTML5 video from URL
                background_html = f'''<video autoplay loop muted playsinline
                    style="position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translate(-50%, -50%); object-fit: cover; z-index: -1; opacity: 0.7;">
                    <source src="{background_name}" type="video/mp4">
                </video>'''
        else:
            # Local file - Check keep/ folder first, then gif/ folder
            keep_path = os.path.join(os.path.dirname(__file__), "keep", background_name)
            gif_path = os.path.join(os.path.dirname(__file__), "gif", background_name)

            if os.path.exists(keep_path):
                background_path = keep_path
            elif os.path.exists(gif_path):
                background_path = gif_path
            else:
                background_path = None

            if background_path and os.path.exists(background_path):
                ext = os.path.splitext(background_name)[1].lower()

                if ext in ['.mp4', '.webm']:
                    # Video background - embed as base64
                    b64_video = get_img_as_base64(background_path)
                    mime = "video/mp4" if ext == ".mp4" else "video/webm"
                    background_html = f'<video autoplay loop muted playsinline style="position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translate(-50%, -50%); object-fit: cover; z-index: -1; opacity: 0.7;"><source src="data:{mime};base64,{b64_video}" type="{mime}"></video>'
                elif ext in ['.mp3', '.wav', '.ogg']:
                    # Audio background - embed as base64
                    b64_audio = get_img_as_base64(background_path)
                    mime = {".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg"}.get(ext, "audio/mpeg")
                    background_html = f'<audio autoplay loop style="position: absolute; bottom: 10px; left: 10px; z-index: 10; opacity: 0.7; width: 200px;"><source src="data:{mime};base64,{b64_audio}" type="{mime}"></audio>'
                elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
                    # Image background
                    b64_img = get_img_as_base64(background_path)
                    background_style = f"background-image: url(data:image/{ext[1:]};base64,{b64_img}); background-size: cover; background-position: center;"

    # Only add positioning styles if we have a background
    additional_style = ""
    if background_name and (background_html or background_style):
        additional_style = "position: relative; overflow: hidden;"

    # Combine styles
    final_style = f"{background_style} {additional_style}".strip() if (background_style or additional_style) else ""

    # Construct opening div tag with or without style
    if final_style:
        container_opening = f'<div class="letter-container" style="{final_style}">'
    else:
        container_opening = '<div class="letter-container">'

    # Render HTML Letter
    # Use components.html() for greetings with backgrounds (handles large base64 data)
    # Use st.markdown() for greetings without backgrounds (faster, cleaner)
    if background_html or background_style:
        # Add 'with-background' class for enhanced text contrast
        container_opening_with_bg = container_opening.replace(
            'class="letter-container"',
            'class="letter-container with-background"'
        )

        # Include inline CSS styles when using components.html() (doesn't inherit Streamlit CSS)
        html_content = f"""
        <style>
        .letter-container {{
            background-color: #fdfbf7;
            padding: 40px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
            min-height: 400px;
            max-width: 100%;
            width: 100%;
            height: auto;
            position: relative;
            z-index: 0;  /* Establish stacking context so video (z-index: -1) stays visible */
            isolation: isolate;
            font-family: 'Georgia', serif;
            color: #333;
            margin-top: 20px;
            overflow: hidden;
        }}

        /* Dark overlay for better text readability on backgrounds */
        .letter-container.with-background::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.25);
            z-index: 0;
            pointer-events: none;
        }}

        /* White text with shadows for backgrounds */
        .letter-container.with-background {{
            color: white;
        }}

        .letter-container.with-background .letter-header,
        .letter-container.with-background .letter-to,
        .letter-container.with-background .letter-from,
        .letter-container.with-background .letter-body,
        .letter-container.with-background .letter-footer {{
            position: relative;
            z-index: 1;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9),
                         1px 1px 2px rgba(0, 0, 0, 0.8),
                         -1px -1px 1px rgba(0, 0, 0, 0.7);
        }}

        # /* Semi-transparent background for message body */
        # .letter-container.with-background .letter-body {{
        #     background: rgba(0, 0, 0, 0.35);
        #     padding: 20px;
        #     border-radius: 8px;
        #     backdrop-filter: blur(3px);
        # }}

        .letter-header {{
            margin-bottom: 30px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.5);
            padding-bottom: 10px;
        }}
        .letter-from, .letter-to {{
            font-size: 1.1em;
            margin: 5px 0;
        }}
        .letter-body {{
            font-size: 1.25em;
            line-height: 1.6;
            white-space: pre-wrap;
            margin-bottom: 60px;
        }}
        .letter-watermark {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            opacity: 0.8;
            width: 100px;
            height: 100px;
            z-index: 1;
        }}
        .letter-footer {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            font-size: 0.8em;
            z-index: 1;
        }}
        </style>
        {container_opening_with_bg}
            {background_html}
            <div class="letter-header">
                <div class="letter-to"><strong>To:</strong> {greeting.get('to', 'Friend')}</div>
                <div class="letter-from"><strong>From:</strong> {greeting.get('from', 'Me')}</div>
            </div>
            <div class="letter-body">
{linkify_urls(greeting.get('message', ''))}
            </div>
            {icon_html}
            <div class="letter-footer">
                Created: {greeting.get('created', '').split('T')[0]}
            </div>
        </div>
        """
        # Use components.html() to handle large base64 data without size limits
        components.html(html_content, height=600, scrolling=True)
    else:
        # No background: use st.markdown() (inherits Streamlit CSS)
        html_content = f"""
        {container_opening}
            <div class="letter-header">
                <div class="letter-to"><strong>To:</strong> {greeting.get('to', 'Friend')}</div>
                <div class="letter-from"><strong>From:</strong> {greeting.get('from', 'Me')}</div>
            </div>
            <div class="letter-body">
{linkify_urls(greeting.get('message', ''))}
            </div>
            {icon_html}
            <div class="letter-footer">
                Created: {greeting.get('created', '').split('T')[0]}
            </div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)


def load_theme_icon(theme: str, size: int = 100) -> Image.Image:
    """
    Load and resize theme icon from file

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Desired icon size in pixels

    Returns:
        PIL Image with transparent background, or None if not found
    """
    import os

    # Path to icon file
    icon_path = os.path.join(os.path.dirname(__file__), "icons", f"{theme}.png")

    try:
        # Load icon
        icon = Image.open(icon_path)

        # Resize to desired size with high-quality resampling
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)

        # Ensure RGBA mode for transparency
        if icon.mode != 'RGBA':
            icon = icon.convert('RGBA')

        return icon
    except FileNotFoundError:
        # Icon file doesn't exist - return None to skip icon
        return None
    except Exception as e:
        print(f"Error loading icon for theme '{theme}': {e}")
        return None


def get_theme_display_icon(theme: str, size: int = 60) -> Image.Image:
    """
    Load theme icon for display in UI preview

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Preview size in pixels (default 60px for grid display)

    Returns:
        PIL Image or None if theme is "general" or icon not found
    """
    if theme == "general":
        return None

    icon_path = os.path.join(os.path.dirname(__file__), "icons", f"{theme}.png")

    if not os.path.exists(icon_path):
        return None

    try:
        icon = Image.open(icon_path)
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        return icon
    except Exception:
        return None


def render_theme_selector() -> str:
    """
    Render theme selector as a dropdown with icon preview (mobile-friendly)

    Returns:
        Selected theme name
    """
    # Theme options with emoji indicators for the dropdown
    themes = [
        ("snowflake", "❄️ Snowflake"),
        ("fireworks", "🎆 Fireworks"),
        ("lights", "✨ Lights"),
        ("stars", "⭐ Stars"),
        ("confetti", "🎉 Confetti"),
        ("champagne", "🥂 Champagne"),
        ("hearts", "❤️ Hearts"),
        ("farewell", "👋 Farewell"),
        ("general", "⊞ General (No Icon)")
    ]

    # Create lookup dictionaries
    theme_keys = [t[0] for t in themes]
    theme_labels = [t[1] for t in themes]
    key_to_label = {t[0]: t[1] for t in themes}
    label_to_key = {t[1]: t[0] for t in themes}

    # Initialize session state for theme selection
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = "snowflake"

    # Get current selection's label for the selectbox default
    current_label = key_to_label.get(st.session_state.selected_theme, theme_labels[0])
    current_index = theme_labels.index(current_label) if current_label in theme_labels else 0

    # Dropdown selector
    selected_label = st.selectbox(
        "Theme",
        options=theme_labels,
        index=current_index,
        help="Choose a theme icon to embed in your QR code",
        key="theme_dropdown"
    )

    # Update session state based on selection
    selected_theme = label_to_key.get(selected_label, "snowflake")
    st.session_state.selected_theme = selected_theme

    # Show preview of selected icon
    if selected_theme != "general":
        icon_preview = get_theme_display_icon(selected_theme, size=80)
        if icon_preview:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(icon_preview, caption="Selected Icon Preview", width='content')
    else:
        st.caption("ℹ️ General theme: QR code will have no embedded icon")

    return selected_theme


def generate_qr_code(data: str, theme: str = "general", visible_message: str = None, all_sides: bool = False, error_correction=qrcode.constants.ERROR_CORRECT_H) -> Image.Image:
    """
    Generate QR code from data string

    Args:
        data: String data to encode
        visible_message: Optional text to display around the QR code
        all_sides: If True, display visible_message on all 4 sides (top, bottom, left, right)
        error_correction: QR error correction level

    Returns:
        PIL Image of QR code
    """
    qr = qrcode.QRCode(
        version=None,  # Auto-detect version
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    # Convert qrcode.image.pil.PilImage to standard PIL.Image.Image
    pil_img = img.convert('RGB')

    # Add theme icon if applicable
    if theme in THEME_ICONS and THEME_ICONS[theme]:
        qr_width, qr_height = pil_img.size

        # Icon should be ~15% of QR code size for reliable scanning (safe margin under 20%)
        icon_size = int(min(qr_width, qr_height) * 0.15)

        try:
            # Load icon from file
            icon = load_theme_icon(theme, icon_size)

            # If icon not found, skip embedding
            if icon is None:
                return pil_img

            # Calculate center position
            icon_pos = (
                (qr_width - icon_size) // 2,
                (qr_height - icon_size) // 2
            )

            # Create white background circle for better contrast
            background = Image.new('RGBA', (icon_size, icon_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(background)
            draw.ellipse([0, 0, icon_size, icon_size], fill=(255, 255, 255, 255))

            # Convert pil_img to RGBA for pasting
            pil_img = pil_img.convert('RGBA')

            # Paste white circle, then icon
            pil_img.paste(background, icon_pos, background)
            pil_img.paste(icon, icon_pos, icon)

            # Convert back to RGB
            pil_img = pil_img.convert('RGB')
        except Exception as e:
            # If icon embedding fails, just return plain QR code
            print(f"Warning: Could not embed icon for theme '{theme}': {e}")


    # Add visible message if provided
    if visible_message:
        try:
            # Prepare for font loading
            font_path = None
            font_size = 20 # Start with a baseline
            
            # Common fonts to try (including CJK support)
            # msyh.ttf = Microsoft YaHei (Windows Chinese)
            # simhei.ttf = SimHei (Windows Chinese)
            # NotoSansCJK... = Linux CJK
            font_names = ["msyh.ttf", "simhei.ttf", "arial.ttf", "calibri.ttf", "seguiemj.ttf", 
                          "segoeui.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf",
                          "WenQuanYiMicroHei.ttf", "NotoSansCJK-Regular.ttc"]
            
            for name in font_names:
                try:
                    # check if we can load it
                    ImageFont.truetype(name, font_size)
                    font_path = name
                    break
                except OSError:
                    continue
            
            # Helper to get text size
            def get_text_size(text, font):
                draw_dummy = ImageDraw.Draw(pil_img)
                if hasattr(draw_dummy, 'textbbox'):
                    bbox = draw_dummy.textbbox((0, 0), text, font=font)
                    return bbox[2] - bbox[0], bbox[3] - bbox[1]
                else:
                    return draw_dummy.textsize(text, font=font)

            qr_width, qr_height = pil_img.size
            target_width = qr_width * 0.9  # Use 90% of width for safe margins (5% each side)
            
            # Formatting
            padding = int(qr_height * 0.05) # 5% of QR height as vertical padding
            if padding < 20: padding = 20

            # Add spacing between QR code and text to prevent overlap
            text_padding = int(qr_height * 0.08)  # 8% of QR height for clear separation
            if text_padding < 15: text_padding = 15  # Minimum 15px spacing

            font = None
            if font_path:
                # Iterative sizing or calculation
                # Heuristic: Width is roughly proportional to font size
                # 1. Measure at base size
                test_font = ImageFont.truetype(font_path, font_size)
                w, h = get_text_size(visible_message, test_font)
                
                if w > 0:
                    # Calculate desired size
                    # scale = target / current
                    scale_factor = target_width / w
                    new_font_size = int(font_size * scale_factor)
                    
                    # Clamp limits
                    min_size = 12
                    max_size = int(qr_height * 0.2) # Max text height 20% of QR? Or just cap size. 
                                                  # Let's cap max size to avoid absurdity on short words like "Hi"
                    
                    if new_font_size < min_size: new_font_size = min_size
                    if new_font_size > max_size: new_font_size = max_size
                    
                    font_size = new_font_size
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = test_font
            else:
                # Fallback to default (cannot resize)
                font = ImageFont.load_default()

            # Final measurement
            text_width, text_height = get_text_size(visible_message, font)
            
            if all_sides:
                # All 4 sides mode: add text on top, bottom, left, and right
                # Calculate final image size (QR + text on all sides)
                # Use larger margin for left/right sides to prevent text from touching QR code
                side_padding = text_height + (text_padding * 3)  # Horizontal space for rotated text

                # For vertical space, we need to fit BOTH the QR code AND the rotated text
                # Rotated text height = original text_width
                # Ensure we have enough vertical space for whichever is taller
                vertical_content_height = max(qr_height, text_width)  # QR or rotated text, whichever is taller

                final_width = qr_width + 2 * side_padding  # Left and right sides
                final_height = vertical_content_height + 2 * (text_height + text_padding)  # Top and bottom text

                new_img = Image.new('RGB', (final_width, final_height), 'white')

                # Center QR code vertically within the available content area
                qr_x = side_padding
                qr_y = text_height + text_padding + (vertical_content_height - qr_height) // 2
                new_img.paste(pil_img, (qr_x, qr_y))
                
                draw_new = ImageDraw.Draw(new_img)
                
                # Draw top text (centered horizontally)
                top_text_x = (final_width - text_width) // 2
                top_text_y = (text_height + text_padding - text_height) // 2
                draw_new.text((top_text_x, top_text_y), visible_message, fill="black", font=font)
                
                # Draw bottom text (centered horizontally)
                bottom_text_x = (final_width - text_width) // 2
                bottom_text_y = text_height + text_padding + vertical_content_height + text_padding // 2
                draw_new.text((bottom_text_x, bottom_text_y), visible_message, fill="black", font=font)
                
                # Create rotated text image for left side (rotated 90 degrees counter-clockwise)
                # Add extra padding to canvas to prevent text clipping from font metrics
                canvas_padding = text_height  # Extra space for descenders/ascenders
                left_canvas_w = text_width + 2 * canvas_padding
                left_canvas_h = text_height + 2 * canvas_padding
                left_text_img = Image.new('RGBA', (left_canvas_w, left_canvas_h), (255, 255, 255, 0))
                left_draw = ImageDraw.Draw(left_text_img)
                left_draw.text((canvas_padding, canvas_padding), visible_message, fill="black", font=font)
                left_text_rotated = left_text_img.rotate(90, expand=True)

                # Paste left text (centered both horizontally in side margin and vertically in content area)
                left_x = (side_padding - left_text_rotated.width) // 2
                left_y = text_height + text_padding + (vertical_content_height - left_text_rotated.height) // 2
                new_img.paste(left_text_rotated, (left_x, left_y), left_text_rotated)
                
                # Create rotated text image for right side (rotated 90 degrees clockwise)
                right_canvas_w = text_width + 2 * canvas_padding
                right_canvas_h = text_height + 2 * canvas_padding
                right_text_img = Image.new('RGBA', (right_canvas_w, right_canvas_h), (255, 255, 255, 0))
                right_draw = ImageDraw.Draw(right_text_img)
                right_draw.text((canvas_padding, canvas_padding), visible_message, fill="black", font=font)
                right_text_rotated = right_text_img.rotate(-90, expand=True)

                # Paste right text (centered both horizontally in side margin and vertically in content area)
                right_x = qr_x + qr_width + (side_padding - right_text_rotated.width) // 2
                right_y = text_height + text_padding + (vertical_content_height - right_text_rotated.height) // 2
                new_img.paste(right_text_rotated, (right_x, right_y), right_text_rotated)
                
                return new_img
            else:
                # Bottom only mode (original behavior)
                # Create new image
                # Width: at least QR width. If text is somehow wider (min size limit), expand.
                final_width = max(qr_width, text_width + int(qr_width * 0.1)) # Ensure margins if text is wider
                final_height = qr_height + text_height + 2 * padding + text_padding  # Include text spacing
                
                new_img = Image.new('RGB', (final_width, final_height), 'white')
                
                # Paste QR code (centered horizontally)
                qr_x = (final_width - qr_width) // 2
                qr_y = padding // 2
                new_img.paste(pil_img, (qr_x, qr_y))
                
                # Draw text (centered horizontally, below QR)
                draw_new = ImageDraw.Draw(new_img)
                text_x = (final_width - text_width) // 2
                text_y = qr_y + qr_height + text_padding
                
                draw_new.text((text_x, text_y), visible_message, fill="black", font=font)
                
                return new_img
            
        except Exception as e:
            print(f"Warning: Failed to add visible message: {e}")
            return pil_img

    return pil_img


def create_greeting_tab():
    """Tab for creating new greeting QR codes"""
    # Display the banner image as the header (left-aligned, smaller for clarity)
    banner_path = os.path.join(os.path.dirname(__file__), "banner", "qr-greeting-banner-4x.png")
    if os.path.exists(banner_path):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.image(banner_path, use_container_width=True)
    else:
        # Fallback to text header if banner not found
        st.markdown('<div class="main-header"><h1>🎄 Create Holiday Greeting QR Code</h1></div>',
                    unsafe_allow_html=True)
        st.markdown("### *A greener, smarter way to say happy holidays.*")
    
    st.write("Create a personalized holiday greeting that can be shared via QR code!")

    # Two column layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Greeting Details")

        # Theme selector outside form to allow interactive button clicks
        theme = render_theme_selector()

        st.markdown("---")

        # GIF background dropdown - OUTSIDE form to allow immediate preview
        available_gifs = get_available_gifs()
        gif_options = ["(No background animation)", "(Enter custom URL...)"] + available_gifs
        
        # Initialize session state for GIF selection if needed
        if 'selected_gif_option' not in st.session_state:
             st.session_state.selected_gif_option = gif_options[0]

        if 'custom_video_url' not in st.session_state:
            st.session_state.custom_video_url = ""

        if 'custom_url_validation_status' not in st.session_state:
            st.session_state.custom_url_validation_status = None  # None, 'valid', 'invalid'

        if 'custom_url_validation_message' not in st.session_state:
            st.session_state.custom_url_validation_message = ""

        selected_gif_option = st.selectbox(
            "Background Animation (Optional)",
            options=gif_options,
            index=gif_options.index(st.session_state.selected_gif_option) if st.session_state.selected_gif_option in gif_options else 0,
            help="Choose a GIF animation to display behind your greeting",
            key="greeting_gif_background_interactive"
        )
        
        # Update session state
        st.session_state.selected_gif_option = selected_gif_option

        # Show custom URL input when "(Enter custom URL...)" is selected
        if selected_gif_option == "(Enter custom URL...)":
            custom_url = st.text_input(
                "Video URL",
                value=st.session_state.custom_video_url,
                placeholder="https://youtu.be/..., https://drive.google.com/file/d/.../view or https://example.com/video.mp4",
                help="Paste a YouTube URL, Google Drive shared video, or direct video link (.mp4, .webm, .mov, .avi, .m3u8)",
                key="custom_video_url_input",
                on_change=validate_custom_url_callback
            )
            st.session_state.custom_video_url = custom_url

            # Display validation status
            if st.session_state.custom_url_validation_status == 'valid':
                st.success(st.session_state.custom_url_validation_message)
            elif st.session_state.custom_url_validation_status == 'invalid':
                st.warning(st.session_state.custom_url_validation_message)
            elif st.session_state.custom_video_url:
                st.info("ℹ️ Validating URL...")
            else:
                st.info("ℹ️ Enter a video URL above to enable background animation")

        # Convert selection to background parameter
        if selected_gif_option == "(No background animation)":
            selected_gif = ""
        elif selected_gif_option == "(Enter custom URL...)":
            # Use custom URL if validated, otherwise empty
            if st.session_state.custom_url_validation_status == 'valid':
                selected_gif = st.session_state.custom_video_url
            else:
                selected_gif = ""
        else:
            # Local file selected
            selected_gif = selected_gif_option

        # Immediate preview below the dropdown (only for local files)
        if selected_gif and selected_gif_option != "(Enter custom URL...)":
            gif_path = os.path.join(os.path.dirname(__file__), "gif", selected_gif)
            if os.path.exists(gif_path):
                st.image(gif_path, caption=f"Preview: {selected_gif}", use_container_width=True)
            else:
                st.warning(f"GIF file not found: {selected_gif}")
        
        st.markdown("---")

        with st.form("greeting_form"):
            from_name = st.text_input(
                "From (Your Name)",
                placeholder="Alice",
                help="Who is sending this greeting?",
                key="greeting_from_name"
            )

            to_name = st.text_input(
                "To (Recipient Name)",
                placeholder="Bob",
                help="Who will receive this greeting?",
                key="greeting_to_name"
            )

            message = st.text_area(
                "Your Message",
                placeholder="Merry Christmas! Wishing you joy and happiness this season...",
                height=150,
                help="Your personalized greeting message",
                key="greeting_message"
            )
            
            visible_message = st.text_input(
                "Visible Message (Optional)",
                placeholder="Scan me!",
                help="Short text to display below the QR code image",
                key="greeting_visible_message"
            )
            
            all_sides = st.checkbox(
                "Add message to all 4 sides",
                value=False,
                help="Display the visible message on top, bottom, left, and right of the QR code",
                key="greeting_all_sides"
            )



            # Character counter
            if message:
                st.caption(f"Message length: {len(message)} characters")

            generate_btn = st.form_submit_button("Generate QR Code", icon=":material/qr_code_2:", type="primary", width='stretch')

    with col2:
        st.subheader("QR Code Preview")

        # Show GIF preview immediately when selected


        if generate_btn:
            # Debug: Check what values we received
            # st.write(f"Debug - from_name: '{from_name}', to_name: '{to_name}', message: '{message}'")

            if not from_name or not to_name or not message:
                st.error("Please fill in all required fields (From, To, and Message)")
            elif selected_gif_option == "(Enter custom URL...)":
                # Validate custom URL before generation
                if not st.session_state.custom_video_url:
                    st.warning("⚠️ No video URL entered. Generating QR code without background animation.")
                    # Continue with selected_gif = "" (already set)
                    greeting = create_holiday_greeting(
                        from_name=from_name,
                        to_name=to_name,
                        message=message,
                        theme=theme,
                        background=selected_gif
                    )

                    # Encode greeting as URL (for mobile scanning)
                    greeting_url = encode_greeting_to_url(greeting)

                    # Get statistics based on URL length
                    stats = get_greeting_stats(greeting_url)

                    # Generate QR code with URL data and theme icon
                    qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_message, all_sides=all_sides)

                    # Display QR code
                    display_qr_with_protection(qr_img, caption=f"Greeting QR Code for {to_name}", width=None)

                    # Statistics
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.write("**QR Code Statistics:**")
                    st.write(f"- Data size: {stats['byte_size']} bytes")
                    st.write(f"- QR Version: ~{stats['recommended_qr_version']}")
                    st.write(f"- Scannable: {'✅ Yes' if stats['fits_in_qr'] else '❌ Too large'}")
                    st.caption("📱 Scan with phone camera to open greeting directly!")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download button
                    buf = io.BytesIO()
                    qr_img.save(buf, format='PNG')
                    byte_im = buf.getvalue()

                    # Generate filename first for consistency
                    filename = f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

                    # Download button with tracking callback
                    st.download_button(
                        label="📥 Download QR Code",
                        data=byte_im,
                        file_name=filename,
                        mime="image/png",
                        width='stretch',
                        on_click=log_download,
                        args=(filename,)
                    )
                elif st.session_state.custom_url_validation_status != 'valid':
                    st.error(f"❌ Invalid video URL: {st.session_state.custom_url_validation_message}")
                    st.info("💡 Please enter a valid YouTube or video URL, or select a different background option.")
                else:
                    # Valid URL - proceed
                    greeting = create_holiday_greeting(
                        from_name=from_name,
                        to_name=to_name,
                        message=message,
                        theme=theme,
                        background=selected_gif
                    )

                    # Encode greeting as URL (for mobile scanning)
                    greeting_url = encode_greeting_to_url(greeting)

                    # Get statistics based on URL length
                    stats = get_greeting_stats(greeting_url)

                    # Generate QR code with URL data and theme icon
                    qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_message, all_sides=all_sides)

                    # Display QR code
                    display_qr_with_protection(qr_img, caption=f"Greeting QR Code for {to_name}", width=None)

                    # Statistics
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.write("**QR Code Statistics:**")
                    st.write(f"- Data size: {stats['byte_size']} bytes")
                    st.write(f"- QR Version: ~{stats['recommended_qr_version']}")
                    st.write(f"- Scannable: {'✅ Yes' if stats['fits_in_qr'] else '❌ Too large'}")
                    st.caption("📱 Scan with phone camera to open greeting directly!")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download button
                    buf = io.BytesIO()
                    qr_img.save(buf, format='PNG')
                    byte_im = buf.getvalue()

                    # Generate filename first for consistency
                    filename = f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

                    # Download button with tracking callback
                    st.download_button(
                        label="📥 Download QR Code",
                        data=byte_im,
                        file_name=filename,
                        mime="image/png",
                        width='stretch',
                        on_click=log_download,
                        args=(filename,)
                    )
            else:
                # Normal flow (local file or no background)
                greeting = create_holiday_greeting(
                    from_name=from_name,
                    to_name=to_name,
                    message=message,
                    theme=theme,
                    background=selected_gif
                )

                # Encode greeting as URL (for mobile scanning)
                greeting_url = encode_greeting_to_url(greeting)

                # Get statistics based on URL length
                stats = get_greeting_stats(greeting_url)

                # Generate QR code with URL data and theme icon
                qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_message, all_sides=all_sides)

                # Display QR code
                display_qr_with_protection(qr_img, caption=f"Greeting QR Code for {to_name}", width=None)

                # Statistics
                st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                st.write("**QR Code Statistics:**")
                st.write(f"- Data size: {stats['byte_size']} bytes")
                st.write(f"- QR Version: ~{stats['recommended_qr_version']}")
                st.write(f"- Scannable: {'✅ Yes' if stats['fits_in_qr'] else '❌ Too large'}")
                st.caption("📱 Scan with phone camera to open greeting directly!")
                st.markdown('</div>', unsafe_allow_html=True)

                # Download button
                buf = io.BytesIO()
                qr_img.save(buf, format='PNG')
                byte_im = buf.getvalue()

                # Generate filename first for consistency
                filename = f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

                # Download button with tracking callback
                st.download_button(
                    label="📥 Download QR Code",
                    data=byte_im,
                    file_name=filename,
                    mime="image/png",
                    width='stretch',
                    on_click=log_download,
                    args=(filename,)
                )

                # Show JSON data
                # Show raw data (Removed as it's now just the message)
                # with st.expander("View Greeting Data"):
                #     st.text(greeting_json)





def scan_greeting_tab():
    """Tab for scanning/decoding greeting QR codes"""
    st.markdown('<div class="main-header"><h1>📱 Scan Greeting QR Code</h1></div>',
                unsafe_allow_html=True)

    # Check if greeting data is passed via URL parameters (from QR code scan)
    try:
        query_params = st.query_params
    except:
        query_params = st.experimental_get_query_params()
    
    # Check if we have greeting data in URL (m or mc parameter indicates a message)
    has_url_greeting = query_params.get('m') or query_params.get('mc')
    
    if has_url_greeting:
        # Decode greeting from URL parameters and display it
        greeting = decode_greeting_from_url(dict(query_params))
        
        if greeting:
            st.success("🎉 Greeting received!")
            
            # Display the full letter format
            display_greeting_letter(greeting)
            
            st.markdown("---")
            
            # Option to create their own or scan another
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝 Create Your Own Greeting", width='stretch'):
                    st.query_params.clear()
                    st.rerun()
            with col2:
                if st.button("📤 Scan Another QR Code", width='stretch'):
                    # Clear only the greeting params, keep tab=scan
                    st.query_params.clear()
                    st.query_params["tab"] = "scan"
                    st.rerun()
            
            return  # Don't show the upload interface
        else:
            st.warning("Could not decode greeting from URL. Try uploading the QR code image instead.")

    # Normal upload interface
    st.write("Upload a greeting QR code image to view the message!")

    uploaded_file = st.file_uploader(
        "Choose a QR code image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image containing a greeting QR code"
    )

    if uploaded_file is not None:
        try:
            # Display uploaded image
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("Uploaded QR Code")
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", width='stretch')

            # Decode QR code
            try:
                if not CV2_AVAILABLE:
                    raise ImportError(f"OpenCV not available: {CV2_IMPORT_ERROR}")

                # Use OpenCV for decoding (No pyzbar dependency)
                # Convert PIL Image to BGR numpy array
                image_array = np.array(image.convert('RGB'))
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

                detector = cv2.QRCodeDetector()
                data, bbox, _ = detector.detectAndDecode(image_array)

                if data:
                    qr_data = data

                    # Parse greeting (handles both URL and JSON formats)
                    greeting = parse_greeting(qr_data)

                    with col2:
                        st.subheader("Greeting Message")

                        if greeting:
                            # Display formatted greeting
                            display_greeting_letter(greeting)
                        else:
                            st.warning("This QR code doesn't contain a valid greeting format.")
                            st.write("**Decoded data:**")
                            st.code(qr_data)
                else:
                    st.error("No QR code found in the image. Please upload a valid QR code image.")

            except ImportError as e:
                st.error(f"QR code scanning requires OpenCV system libraries.")
                st.info("Please use manual JSON entry below:")

                manual_data = st.text_area("Paste QR Code Data (JSON)")
                if manual_data:
                    greeting = parse_greeting(manual_data)
                    if greeting:
                        st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                        st.write(format_greeting_display(greeting))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Invalid greeting data format")

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Alternatively, you can manually paste the QR code data below:")

                manual_data = st.text_area("Paste QR Code Data (JSON)", key="manual_data_exception")
                if manual_data:
                    greeting = parse_greeting(manual_data)
                    if greeting:
                        st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                        st.write(format_greeting_display(greeting))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Invalid greeting data format")

        except Exception as e:
            st.error(f"Error processing image: {str(e)}")


def examples_tab():
    """Tab showing example greetings"""
    st.markdown('<div class="main-header"><h1>📖 Examples</h1></div>',
                unsafe_allow_html=True)

    st.write("Here are some example holiday greetings you can create:")

    examples = [
        {
            "title": "🎄 Christmas Greeting",
            "from": "Alice",
            "to": "Bob",
            "theme": "snowflake",
            "message": "Merry Christmas! Wishing you joy and happiness this season. Thank you for being a wonderful friend!"
        },
        {
            "title": "🎆 New Year Message",
            "from": "Bob",
            "to": "Future Me",
            "theme": "fireworks",
            "message": "2025 was incredible! Here's to growth and new adventures in 2026!"
        },
        {
            "title": "💍 Wedding Save the Date",
            "from": "Emma & James",
            "to": "Friends and Family",
            "theme": "champagne",
            "message": "We're getting married! Save the date: June 15, 2026. More details to follow!"
        },
        {
            "title": "👋 Farewell to Colleagues",
            "from": "Alex",
            "to": "The Team",
            "theme": "farewell",
            "message": "It's been an amazing journey working with you all! Thank you for the memories, the laughs, and the lessons. Let's stay in touch!",
            "visible_message": "Scan to read my farewell note"
        }
    ]

    for example in examples:
        with st.expander(example["title"]):
            col1, col2 = st.columns([1, 1])

            with col1:
                st.write(f"**From:** {example['from']}")
                st.write(f"**To:** {example['to']}")
                st.write(f"**Theme:** {example['theme']}")
                st.markdown("---")
                st.write(example['message'])

            with col2:
                # Generate QR for example
                greeting = create_holiday_greeting(
                    from_name=example['from'],
                    to_name=example['to'],
                    message=example['message'],
                    theme=example['theme']
                )
                # Use URL encoding for QR code
                greeting_url = encode_greeting_to_url(greeting)
                visible_msg = example.get('visible_message', None)
                qr_img = generate_qr_code(greeting_url, theme=example['theme'], visible_message=visible_msg)
                display_qr_with_protection(qr_img, caption="QR Code", width=None)


def get_available_backgrounds():
    """Get list of available background files from keep/ folder"""
    keep_path = Path(__file__).parent / "keep"
    if not keep_path.exists():
        return []

    # Support images and videos
    extensions = {'.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'}
    backgrounds = []
    for f in keep_path.iterdir():
        if f.suffix.lower() in extensions:
            backgrounds.append(f.name)
    return sorted(backgrounds)


def validate_custom_url_callback():
    """Validate custom video URL when user types"""
    url = st.session_state.get('custom_video_url_input', '').strip()

    if not url:
        st.session_state.custom_url_validation_status = None
        st.session_state.custom_url_validation_message = ""
        return

    if not is_web_url(url):
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = "⚠️ Invalid URL format. Must start with http:// or https://"
        return

    bg_type = classify_background(url)

    if bg_type == 'youtube':
        embed_url = convert_youtube_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = "✅ Valid YouTube URL"
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = "⚠️ Invalid YouTube URL. Could not extract video ID."

    elif bg_type == 'google_drive':
        embed_url = convert_google_drive_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = "✅ Valid Google Drive URL"
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = "⚠️ Invalid Google Drive URL. Could not extract file ID."

    elif bg_type == 'direct_video':
        st.session_state.custom_url_validation_status = 'valid'
        file_ext = url.split('.')[-1].upper()
        st.session_state.custom_url_validation_message = f"✅ Valid video URL ({file_ext})"

    elif bg_type == 'other_url':
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = "⚠️ Unsupported URL type. Use YouTube or direct video links (.mp4, .webm, .mov, .avi, .m3u8)"

    else:
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = "⚠️ Could not validate URL format"


def get_available_gifs():
    """Get list of available background files (GIF, JPG) from gif/ folder"""
    gif_path = Path(__file__).parent / "gif"
    if not gif_path.exists():
        return []

    gifs = []
    for f in gif_path.iterdir():
        if f.suffix.lower() in ['.gif', '.jpg', '.jpeg']:
            gifs.append(f.name)
    return sorted(gifs)


def batch_greeting_tab():
    """Tab for batch QR code generation from Excel"""
    st.markdown('<div class="main-header"><h1>📦 Batch QR Code Generation</h1></div>',
                unsafe_allow_html=True)

    st.write("Generate multiple QR codes at once by uploading an Excel spreadsheet.")
    st.info("💡 **New Feature**: You can now use YouTube URLs or direct video URLs as backgrounds! Just paste the URL in the Background column.")
    
    # Available themes and backgrounds for reference
    available_themes = list(THEME_ICONS.keys())
    available_backgrounds = get_available_backgrounds()
    
    st.markdown("---")
    
    # Template download section
    st.subheader("1. Download Template")
    st.write("Download the Excel template, fill in your greetings, then upload it below.")
    
    # Create template Excel file in memory
    try:
        import pandas as pd
        from io import BytesIO
        
        # Create sample data with 4 test cases
        sample_data = {
            "From": ["Alice", "Bob", "Charlie", "David"],
            "To": ["Bob", "Alice", "Dana", "Eve"],
            "Message": ["Merry Christmas!", "Happy New Year!", "Season's Greetings!\nhttps://qr-greeting.co.uk", "Enjoy the holidays!"],
            "Theme": ["snowflake", "fireworks", "hearts", "lights"],
            "Background": ["letter-background-design-01.jpg", "letter-background-design-02.jpg", "https://youtu.be/6SuLXoRmykE", "christmas-lights.gif"],
            "VisibleMessage": ["Scan me!", "BOB", "Happy Holidays!", "Ho Ho Ho!"]
        }
        df_template = pd.DataFrame(sample_data)
        
        # Save to BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_template.to_excel(writer, index=False, sheet_name='Greetings')
            
            # Add a reference sheet with valid options
            # Include local backgrounds and web URL examples
            background_examples = available_backgrounds + [
                "",
                "# Web URLs are also supported:",
                "youtu.be/6SuLXoRmykE",
                "https://www.youtube.com/watch?v=VIDEO_ID",
                "https://example.com/video.mp4"
            ]

            ref_data = {
                "Valid Themes": available_themes + [""] * (max(0, len(background_examples) - len(available_themes))),
                "Valid Backgrounds": background_examples + [""] * (max(0, len(available_themes) - len(background_examples)))
            }
            # Pad to same length
            max_len = max(len(available_themes), len(background_examples))
            ref_data["Valid Themes"] = (available_themes + [""] * max_len)[:max_len]
            ref_data["Valid Backgrounds"] = (background_examples + [""] * max_len)[:max_len]

            df_ref = pd.DataFrame(ref_data)
            df_ref.to_excel(writer, index=False, sheet_name='Valid Options')
        
        excel_bytes = output.getvalue()
        
        st.download_button(
            label="📥 Download Template (.xlsx)",
            data=excel_bytes,
            file_name="qr_greeting_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Show valid options for reference
        with st.expander("View Valid Options"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Valid Themes:**")
                for theme in available_themes:
                    emoji = THEME_ICONS.get(theme, "")
                    st.write(f"- `{theme}` {emoji if emoji else ''}")
            with col2:
                st.write("**Valid Backgrounds:**")
                st.write("*Local files from `keep/` folder:*")
                if available_backgrounds:
                    for bg in available_backgrounds:
                        st.write(f"- `{bg}`")
                else:
                    st.write("No backgrounds available in `keep/` folder")
                st.write("")
                st.write("*Or use web video URLs:*")
                st.write("- YouTube: `youtu.be/VIDEO_ID`")
                st.write("- YouTube: `https://www.youtube.com/watch?v=VIDEO_ID`")
                st.write("- Direct video: `https://example.com/video.mp4`")
        
    except ImportError:
        st.error("pandas and openpyxl are required for batch processing. Please install them: `pip install pandas openpyxl`")
        return
    
    st.markdown("---")
    
    # Upload section
    st.subheader("2. Upload Filled Template")
    
    uploaded_file = st.file_uploader(
        "Choose your filled Excel file",
        type=['xlsx', 'xls'],
        help="Upload the template with your greeting data"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Greetings')
            
            st.success(f"Loaded {len(df)} greetings from Excel!")
            
            # Preview data
            with st.expander("Preview Data"):
                st.dataframe(df)
            
            # Validate data
            required_cols = ["From", "To", "Message"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                return
            
            # Validate themes
            if "Theme" in df.columns:
                invalid_themes = df[~df["Theme"].isna() & ~df["Theme"].isin(available_themes)]["Theme"].unique()
                if len(invalid_themes) > 0:
                    st.warning(f"Some rows have invalid themes: {list(invalid_themes)}. They will use 'general'.")
            
            # Generate button
            if st.button("🚀 Generate All QR Codes", type="primary"):
                import zipfile
                
                zip_buffer = BytesIO()
                
                progress = st.progress(0)
                status = st.empty()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for idx, row in df.iterrows():
                        from_name = str(row.get("From", ""))
                        to_name = str(row.get("To", ""))
                        message = str(row.get("Message", ""))
                        theme = str(row.get("Theme", "general")) if pd.notna(row.get("Theme")) else "general"
                        background = str(row.get("Background", "")) if pd.notna(row.get("Background")) else ""
                        visible_msg = str(row.get("VisibleMessage", "")) if pd.notna(row.get("VisibleMessage")) else ""
                        
                        # Validate theme
                        if theme not in available_themes:
                            theme = "general"

                        # Validate background (local file or web URL)
                        if background:
                            if is_web_url(background):
                                # Validate web URL format
                                bg_type = classify_background(background)
                                if bg_type == 'youtube':
                                    # Validate YouTube URL can be converted to embed format
                                    if convert_youtube_to_embed_url(background) is None:
                                        st.warning(f"Row {idx + 1}: Invalid YouTube URL '{background}' - skipping background")
                                        background = ""
                                elif bg_type == 'google_drive':
                                    # Validate Google Drive URL can be converted to embed format
                                    if convert_google_drive_to_embed_url(background) is None:
                                        st.warning(f"Row {idx + 1}: Invalid Google Drive URL '{background}' - skipping background")
                                        background = ""
                                elif bg_type == 'direct_video':
                                    # Direct video URLs are accepted as-is
                                    # Note: CORS and accessibility depend on the video host
                                    pass
                                else:
                                    # Other URL types not supported
                                    st.warning(f"Row {idx + 1}: Unsupported URL type '{background}' - skipping background")
                                    background = ""
                            elif background not in available_backgrounds:
                                # Local file not found
                                background = ""
                        
                        status.text(f"Generating QR {idx + 1}/{len(df)}: {to_name}...")
                        
                        # Create greeting
                        greeting = create_holiday_greeting(
                            from_name=from_name,
                            to_name=to_name,
                            message=message,
                            theme=theme,
                            background=background
                        )
                        
                        # Encode to URL
                        greeting_url = encode_greeting_to_url(greeting)
                        
                        # Generate QR code
                        qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_msg)
                        
                        # Save to zip
                        img_buffer = BytesIO()
                        qr_img.save(img_buffer, format='PNG')
                        img_buffer.seek(0)
                        
                        # Filename: to_name_index.png
                        safe_name = "".join(c for c in to_name if c.isalnum() or c in (' ', '-', '_')).strip()
                        filename = f"{safe_name}_{idx + 1}.png"
                        
                        zf.writestr(filename, img_buffer.read())
                        
                        progress.progress((idx + 1) / len(df))
                
                status.text("✅ All QR codes generated!")
                
                zip_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download All QR Codes (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"qr_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip"
                )
                
        except Exception as e:
            st.error(f"Error processing Excel file: {str(e)}")


def about_tab():
    """About the application"""
    st.markdown('<div class="main-header"><h1>ℹ️ About</h1></div>',
                unsafe_allow_html=True)

    st.write("""
    ## Holiday Greeting QR Code Generator

    This application allows you to create personalized holiday greetings encoded in QR codes.
    Share your messages in a unique and modern way!
    """)

    st.markdown("---")
    # Video player in centered column
    col1, col2, col3 = st.columns([0.5, 2, 0.5], gap="medium")
    with col2:
        st.video("https://www.youtube.com/watch?v=6SuLXoRmykE")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Video section with styled heading
    st.markdown("""
<div style="text-align: center; margin: 2rem 0 1rem 0;">
    <h3 style="color: #333; margin-bottom: 0.5rem;">See It In Action</h3>
    <p style="color: #666; margin-bottom: 1.5rem; font-size: 1rem;">
        Watch a quick demo of how easy it is to create and share personalized greeting QR codes.
    </p>
</div>
""", unsafe_allow_html=True)

    # Video player in centered column
    col1, col2, col3 = st.columns([0.5, 2, 0.5], gap="medium")
    with col2:
        st.video("https://www.youtube.com/watch?v=hJdGamlet5A")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Core positioning messages
    st.markdown("---")
    st.subheader("Why Choose QR Greetings?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🌱 Environment Friendly

        **Zero paper. Zero postage. Instant delivery.**

        Traditional paper cards consume materials, printing resources, and shipping energy.
        QR greetings are 100% digital — no trees harmed, no carbon footprint from delivery trucks.

        Send your love without leaving a trace on the planet.
        """)

    with col2:
        st.markdown("""
        ### 🔐 Secret in Transit

        **Your message stays private until revealed.**

        Unlike public social media posts, your greeting is encoded within the QR pattern itself.
        Only the recipient who scans it can see your heartfelt message.

        It's like a digital sealed envelope — personal, intimate, and special.
        """)

    with col3:
        st.markdown("""
        ### 📱 Device Friendly

        **Works on any phone. No app required.**

        Recipients simply point their camera at the QR code — that's it!
        Works seamlessly on both iOS and Android, opening directly in the browser.

        No downloads, no sign-ups, no friction. Just scan and smile.
        """)

    st.markdown("---")

    st.write("""
    ### Features
    - ✨ Create custom greeting QR codes
    - 📱 Scan and read greeting QR codes
    - 🎨 Multiple theme options with embedded icons
    - 📥 Download QR codes as images
    - 💾 Compact JSON format for efficient encoding

    ### How It Works
    1. Enter your greeting details (from, to, message)
    2. Choose a theme
    3. Generate the QR code
    4. Download and share!

    Recipients can scan the QR code with their phone camera or upload it to this app to view your message.

    ### Technical Details
    - Uses high error correction (Level H) for reliable scanning
    - Compact JSON format minimizes QR code size
    - Supports messages up to ~500 characters comfortably
    - Built with Streamlit and netshare

    ### Powered By
    - **netshare** - Network sharing and QR code utilities
    - **Streamlit** - Interactive web interface
    - **qrcode** - QR code generation
    - **Pillow** - Image processing
    """)

    # Display download count (just the number)
    count = get_download_count()
    st.write(count)


def view_greeting_page(query_params: dict):
    """
    Display a greeting message in a clean, mobile-friendly format.
    This is shown when users scan the QR code with their phone camera.
    
    Args:
        query_params: URL query parameters containing greeting data
    """
    # Decode greeting from URL parameters
    greeting = decode_greeting_from_url(query_params)
    
    if not greeting:
        st.error("Invalid or missing greeting data.")
        st.write("Please scan a valid greeting QR code or go to the main page to create one.")
        if st.button("Go to Home Page"):
            st.query_params.clear()
            st.rerun()
        return
    
    # Get theme for styling
    theme = greeting.get("theme", "general")
    theme_emoji = THEME_ICONS.get(theme, "🎄")
    
    # Mobile-optimized greeting display (message only)
    st.markdown("""
    <style>
        .mobile-greeting-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 2rem 1rem;
            text-align: center;
        }
        .greeting-emoji {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        .greeting-message {
            font-family: 'Georgia', serif;
            font-size: 1.5rem;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #fdfbf7 0%, #f5f0e8 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 1rem 0;
            white-space: pre-wrap;
        }
        .greeting-from {
            font-size: 1.1rem;
            color: #666;
            margin-top: 1.5rem;
            font-style: italic;
        }
        .view-full-link {
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #888;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the greeting
    st.markdown('<div class="mobile-greeting-container">', unsafe_allow_html=True)
    
    # Theme emoji
    if theme_emoji:
        st.markdown(f'<div class="greeting-emoji">{theme_emoji}</div>', unsafe_allow_html=True)
    
    # The message (main content)
    message = greeting.get("message", "")
    st.markdown(f'<div class="greeting-message">{message}</div>', unsafe_allow_html=True)
    
    # From attribution (subtle)
    from_name = greeting.get("from", "")
    if from_name:
        st.markdown(f'<div class="greeting-from">— From {from_name}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Subtle link to create your own (not prominent)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("Create your own greeting QR code!")
        if st.button("Create Greeting", type="secondary", width='stretch'):
            st.query_params.clear()
            st.rerun()


def main():
    """Main application"""

    # Sidebar
    with st.sidebar:
        # st.image("https://raw.githubusercontent.com/anthropics/anthropic-quickstarts/main/computer-use-demo/image.png",
        #          width=100)
        st.title("Holiday Greeting QR")
        st.write("Create and share personalized holiday greetings via QR codes!")
        st.markdown("*A greener, smarter way to say happy holidays.*")

        st.markdown("---")

        st.write("### Quick Tips")
        st.info("""
        💡 Keep messages under 300 characters for best QR code size

        📱 Test QR codes with your phone camera app

        🎨 Choose themes that match your occasion
        """)
        
        st.markdown("---")
        
        # Batch tab toggle
        show_batch = st.checkbox("Show Batch Tab", value=False, help="Enable batch QR code generation from Excel")

    # Read query param for tab selection
    try:
        query_params = st.query_params
        tab_param = query_params.get('tab', 'create')
    except:
        # Fallback for older Streamlit versions
        query_params = st.experimental_get_query_params()
        tab_param = query_params.get('tab', ['create'])[0]

    # Check if this is a "view" request (from QR code scan)
    if tab_param == "view":
        # Show mobile-friendly greeting view (message only)
        view_greeting_page(dict(query_params))
        return  # Don't show the normal app interface

    # Map tab names to indices (depends on whether batch tab is shown)
    if show_batch:
        tab_map = {"create": 0, "scan": 1, "examples": 2, "batch": 3, "about": 4}
    else:
        tab_map = {"create": 0, "scan": 1, "examples": 2, "about": 3}
    tab_index = tab_map.get(tab_param, 0)

    # Inject JavaScript to click the correct tab (only if not the first tab)
    if tab_index > 0:
        st.components.v1.html(f"""
            <script>
            (function() {{
                let attempts = 0;
                const maxAttempts = 10;

                function clickTab() {{
                    const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');

                    if (tabs && tabs.length > {tab_index}) {{
                        tabs[{tab_index}].click();
                        return true;
                    }} else if (attempts < maxAttempts) {{
                        attempts++;
                        setTimeout(clickTab, 100);
                    }}
                }}

                clickTab();
            }})();
            </script>
        """, height=0)

    # Main tabs (conditionally include batch tab)
    if show_batch:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Create Greeting", "Scan QR Code", "Examples", "Batch", "About"])
        
        with tab1:
            create_greeting_tab()

        with tab2:
            scan_greeting_tab()

        with tab3:
            examples_tab()

        with tab4:
            batch_greeting_tab()

        with tab5:
            about_tab()
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["Create Greeting", "Scan QR Code", "Examples", "About"])

        with tab1:
            create_greeting_tab()

        with tab2:
            scan_greeting_tab()

        with tab3:
            examples_tab()

        with tab4:
            about_tab()


if __name__ == "__main__":
    main()
