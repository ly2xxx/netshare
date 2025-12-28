"""
QR code display module
Handles QR code display with protection and greeting letter rendering
"""

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64
import io
import os
from typing import Dict

from config import THEME_ICONS
from utils.url_utils import (
    is_web_url,
    classify_background,
    convert_youtube_to_embed_url,
    convert_google_drive_to_embed_url,
    convert_facebook_to_embed_url,
    convert_instagram_to_embed_url,
    linkify_urls
)
from utils.image_utils import get_img_as_base64


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


def display_animated_qr(
    data: str,
    theme: str = "general",
    animation: str = "MaterializeIn",
    module_color: str = "#1f77b4",
    position_ring_color: str = "#ff7f0e",
    visible_message: str = None,
    width: int = 300,
    caption: str = ""
) -> None:
    """
    Display QR code with animation using @bitjson/qr-code web component.

    Args:
        data: URL or text to encode in QR code
        theme: Theme name from config.THEME_ICONS
        animation: Animation type (FadeInTopDown|FadeInCenterOut|MaterializeIn|RadialRipple|RadialRippleIn|None)
        module_color: Hex color for QR modules/dots
        position_ring_color: Hex color for position detection markers
        visible_message: Optional text overlay below QR code
        width: Display width in pixels
        caption: Caption text to display below QR code

    Returns:
        None (renders HTML component directly)
    """
    # Get theme emoji for icon slot
    icon_emoji = THEME_ICONS.get(theme, "🎨") if theme != "general" else ""

    # Generate unique ID for this QR code instance
    unique_id = f"qr-{abs(hash(data)) % 10000000}"

    # Prepare icon HTML if theme has an emoji
    icon_html = ""
    if icon_emoji:
        icon_html = f'<div slot="icon" style="font-size: 48px; line-height: 1;">{icon_emoji}</div>'

    # Prepare visible message HTML if provided
    message_html = ""
    if visible_message:
        message_html = f'''
        <div style="text-align: center; margin-top: 15px; font-size: 1.1em; color: #333; font-weight: 500;">
            {visible_message}
        </div>
        '''

    # Prepare caption HTML if provided
    caption_html = ""
    if caption:
        caption_html = f'<p style="text-align: center; color: #666; font-size: 0.9em; margin-top: 10px;">{caption}</p>'

    # Run animation when component is ready
    animation_script = f"""
    // Helper to start animation safely
    const animate = () => {{
        try {{
            qr.animateQRCode('{animation}');
        }} catch (e) {{
            // Ignore errors if animation is already running or component not ready
            console.warn('Animation attempt failed:', e);
        }}
    }};

    // Wait for custom element to be upgraded
    customElements.whenDefined('qr-code').then(() => {{
        const qr = document.getElementById('{unique_id}');
        if (!qr) return;

        // 1. Listen for render events (normal flow)
        qr.addEventListener('codeRendered', () => {{
            setTimeout(animate, 100);
        }});

        // 2. Fallback: Try to animate after a delay in case we missed the event
        // (common race condition if component renders fast)
        setTimeout(animate, 500);
    }});
    """

    if animation == "None" or not animation:
        animation_script = ""

    # Calculate iframe height (QR + message + caption + padding)
    iframe_height = width + (80 if visible_message else 0) + (40 if caption else 0) + 100

    # Build complete HTML with web component
    # Added onerror handler to script to show user feedback if CDN fails
    html_code = f"""
    <script type="module" src="https://unpkg.com/@bitjson/qr-code@1.0.2/dist/qr-code.js" 
            onerror="document.getElementById('{unique_id}-error').style.display='block';"></script>
    
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px;">
        <div id="{unique_id}-error" style="display:none; color: #d32f2f; background: #ffebee; padding: 10px; border-radius: 4px; margin-bottom: 10px; text-align: center;">
             ⚠️ Unable to load QR animation library. <br>Please check your internet connection.
        </div>
        
        <qr-code id="{unique_id}"
          contents="{data}"
          module-color="{module_color}"
          position-ring-color="{position_ring_color}"
          position-center-color="{position_ring_color}"
          style="width: {width}px; height: {width}px; background-color: white;">
          {icon_html}
        </qr-code>
        {message_html}
        {caption_html}
    </div>
    <script>
    (function() {{
        const qr = document.getElementById('{unique_id}');
        if (!qr) {{
            return;
        }}

        {animation_script}

        // Add right-click protection
        qr.addEventListener('contextmenu', e => {{ e.preventDefault(); return false; }});
        qr.addEventListener('dragstart', e => {{ e.preventDefault(); return false; }});
        qr.addEventListener('copy', e => {{ e.preventDefault(); return false; }});
    }})();
    </script>
    """

    components.html(html_code, height=iframe_height, scrolling=False)


def display_greeting_letter(greeting: Dict) -> None:
    """
    Display greeting in a letter format with optional background

    Args:
        greeting: Dictionary containing greeting data (to, from, message, theme, background, created)

    Returns:
        None (renders greeting directly)
    """
    # Prepare icon for HTML
    theme_name = greeting.get('theme', 'general')
    icon_html = ""
    if theme_name in THEME_ICONS and theme_name != 'general':
        icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", f"{theme_name}.png")
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
            elif bg_type == 'facebook':
                # Facebook embed iframe
                embed_url = convert_facebook_to_embed_url(background_name)
                if embed_url:
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}"
                        allow="autoplay; encrypted-media; picture-in-picture"
                        allowfullscreen
                    ></iframe>'''
            elif bg_type == 'instagram':
                # Instagram embed iframe with fallback button
                embed_url = convert_instagram_to_embed_url(background_name)
                if embed_url:
                    # Attempt embed but also provide fallback button
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}"
                        allowfullscreen
                    ></iframe>
                    <div style="position: absolute; top: 10px; right: 10px; z-index: 5;">
                        <a href="{background_name}" target="_blank" rel="noopener noreferrer"
                           style="display: inline-block; padding: 10px 20px; background: #e4405f; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">
                            📱 Open in Instagram
                        </a>
                    </div>'''
            elif bg_type == 'direct_video':
                # Direct HTML5 video from URL
                background_html = f'''<video autoplay loop muted playsinline
                    style="position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translate(-50%, -50%); object-fit: cover; z-index: -1; opacity: 0.7;">
                    <source src="{background_name}" type="video/mp4">
                </video>'''
        else:
            # Local file - Check keep/ folder first, then gif/ folder
            keep_path = os.path.join(os.path.dirname(__file__), "..", "keep", background_name)
            gif_path = os.path.join(os.path.dirname(__file__), "..", "gif", background_name)

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
