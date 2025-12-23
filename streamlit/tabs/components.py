"""
Shared UI components for tabs
Contains reusable UI elements and workflows
"""

import streamlit as st
import io
from datetime import datetime
from typing import Optional

from greeting_formats import (
    create_holiday_greeting,
    get_greeting_stats,
    encode_greeting_to_url
)
from utils.url_utils import (
    is_web_url,
    classify_background,
    convert_youtube_to_embed_url,
    convert_google_drive_to_embed_url
)
from utils.image_utils import get_theme_display_icon
from utils.download_tracker import log_download
from qr.generator import generate_qr_code
from qr.display import display_qr_with_protection


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


def validate_custom_url_callback() -> None:
    """
    Validate custom video URL when user types
    Updates session state with validation status and message
    """
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


def render_qr_generation_flow(
    from_name: str,
    to_name: str,
    message: str,
    theme: str,
    background: str = "",
    visible_message: str = "",
    all_sides: bool = False,
    warning_text: Optional[str] = None
) -> None:
    """
    Unified QR generation and display flow

    This function eliminates code duplication by providing a single workflow for:
    1. Creating greeting data
    2. Encoding to URL
    3. Generating QR code
    4. Displaying QR with protection
    5. Showing statistics
    6. Providing download button

    Args:
        from_name: Sender name
        to_name: Recipient name
        message: Greeting message
        theme: Visual theme
        background: Background file/URL
        visible_message: Text overlay on QR
        all_sides: Display message on all 4 sides
        warning_text: Optional warning to display above QR (e.g., "No video URL entered")

    Returns:
        None (displays QR in Streamlit UI)
    """
    # Show warning if provided
    if warning_text:
        st.warning(warning_text)

    # 1. Create greeting data
    greeting = create_holiday_greeting(
        from_name=from_name,
        to_name=to_name,
        message=message,
        theme=theme,
        background=background
    )

    # 2. Encode greeting as URL (for mobile scanning)
    greeting_url = encode_greeting_to_url(greeting)

    # 3. Get statistics based on URL length
    stats = get_greeting_stats(greeting_url)

    # 4. Generate QR code with URL data and theme icon
    qr_img = generate_qr_code(
        greeting_url,
        theme=theme,
        visible_message=visible_message,
        all_sides=all_sides
    )

    # 5. Display QR code with right-click protection
    display_qr_with_protection(
        qr_img,
        caption=f"Greeting QR Code for {to_name}",
        width=None
    )

    # 6. Show statistics
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.write("**QR Code Statistics:**")
    st.write(f"- Data size: {stats['byte_size']} bytes")
    st.write(f"- QR Version: ~{stats['recommended_qr_version']}")
    st.write(f"- Scannable: {'✅ Yes' if stats['fits_in_qr'] else '❌ Too large'}")
    st.caption("📱 Scan with phone camera to open greeting directly!")
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. Provide download button with tracking
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
