"""
Shared UI components for tabs
Contains reusable UI elements and workflows
"""

import streamlit as st
import io
from datetime import datetime
from typing import Optional

# Import internationalization
from i18n import get_text as _

from greeting_formats import (
    create_holiday_greeting,
    get_greeting_stats,
    encode_greeting_to_url
)
from utils.url_utils import (
    is_web_url,
    classify_background,
    convert_youtube_to_embed_url,
    convert_google_drive_to_embed_url,
    convert_facebook_to_embed_url,
    convert_instagram_to_embed_url
)
from utils.image_utils import get_theme_display_icon
from utils.download_tracker import log_download
from qr.generator import generate_qr_code
from qr.display import display_qr_with_protection, display_animated_qr
from config import THEME_ANIMATIONS, THEME_COLORS


def render_theme_selector() -> str:
    """
    Render theme selector as a dropdown with icon preview (mobile-friendly)

    Returns:
        Selected theme name
    """
    # Theme options with emoji indicators for the dropdown
    themes = [
        ("snowflake", _("components.themes.snowflake")),
        ("fireworks", _("components.themes.fireworks")),
        ("lights", _("components.themes.lights")),
        ("stars", _("components.themes.stars")),
        ("confetti", _("components.themes.confetti")),
        ("champagne", _("components.themes.champagne")),
        ("hearts", _("components.themes.hearts")),
        ("farewell", _("components.themes.farewell")),
        ("burn_after_read", _("components.themes.burn")),
        ("general", _("components.themes.general"))
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
        _("components.theme.label"),
        options=theme_labels,
        index=current_index,
        help=_("components.theme.help"),
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
                st.image(icon_preview, caption=_("components.theme_preview"), width='content')
    else:
        st.caption(_("components.theme_general_info"))

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
        st.session_state.custom_url_validation_message = _("components.video_validation.invalid_format")
        return

    bg_type = classify_background(url)

    if bg_type == 'youtube':
        embed_url = convert_youtube_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = _("components.video_validation.youtube_valid")
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = _("components.video_validation.youtube_invalid")

    elif bg_type == 'google_drive':
        embed_url = convert_google_drive_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = _("components.video_validation.gdrive_valid")
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = _("components.video_validation.gdrive_invalid")

    elif bg_type == 'facebook':
        embed_url = convert_facebook_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = _("components.video_validation.facebook_valid")
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = _("components.video_validation.facebook_invalid")

    elif bg_type == 'instagram':
        embed_url = convert_instagram_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = _("components.video_validation.instagram_warning")
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = _("components.video_validation.instagram_invalid")

    elif bg_type == 'direct_video':
        st.session_state.custom_url_validation_status = 'valid'
        file_ext = url.split('.')[-1].upper()
        st.session_state.custom_url_validation_message = _("components.video_validation.direct_valid", format=file_ext)

    elif bg_type == 'other_url':
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = _("components.video_validation.unsupported")

    else:
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = _("components.video_validation.error")


def render_qr_generation_flow(
    from_name: str,
    to_name: str,
    message: str,
    theme: str,
    background: str = "",
    visible_message: str = "",
    all_sides: bool = False,
    warning_text: Optional[str] = None,
    use_animation: bool = False,
    animation_type: Optional[str] = None,
    qr_module_color: Optional[str] = None,
    qr_ring_color: Optional[str] = None
) -> None:
    """
    Unified QR generation and display flow

    This function eliminates code duplication by providing a single workflow for:
    1. Creating greeting data
    2. Encoding to URL
    3. Generating QR code
    4. Displaying QR with protection (animated or static)
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
        use_animation: Whether to use animated QR (default: True)
        animation_type: Animation type override (None = use theme default)
        qr_module_color: QR module color override (None = use theme default)
        qr_ring_color: QR position ring color override (None = use theme default)

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

    # 4. Determine animation and colors
    final_animation = animation_type if animation_type is not None else THEME_ANIMATIONS.get(theme, "MaterializeIn")
    theme_colors = THEME_COLORS.get(theme, {"module": "#1f77b4", "ring": "#ff7f0e"})
    final_module_color = qr_module_color if qr_module_color else theme_colors["module"]
    final_ring_color = qr_ring_color if qr_ring_color else theme_colors["ring"]

    # 5. Display QR code (animated or static)
    if use_animation:
        # Use new animated QR display
        display_animated_qr(
            data=greeting_url,
            theme=theme,
            animation=final_animation,
            module_color=final_module_color,
            position_ring_color=final_ring_color,
            visible_message=visible_message if not all_sides else None,  # Web component doesn't support all_sides
            width=300,
            caption=f"Greeting QR Code for {to_name}"
        )
    else:
        # Use traditional static QR display (backward compatibility)
        # Generate QR code image with theme icon and colors
        qr_img = generate_qr_code(
            greeting_url,
            theme=theme,
            visible_message=visible_message,
            all_sides=all_sides,
            module_color=final_module_color,
            position_ring_color=final_ring_color
        )

        display_qr_with_protection(
            qr_img,
            caption=f"Greeting QR Code for {to_name}",
            width=None
        )

    # 6. Show statistics
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.write(_("components.qr_stats.title"))
    st.write(_("components.qr_stats.data_size", bytes=stats['byte_size']))
    st.write(_("components.qr_stats.qr_version", version=stats['recommended_qr_version']))
    st.write(_("components.qr_stats.scannable_yes") if stats['fits_in_qr'] else _("components.qr_stats.scannable_no"))
    st.caption(_("components.qr_tip"))
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. Provide download button with tracking
    # Generate static QR image for download (even if animated version was displayed)
    if use_animation:
        download_qr_img = generate_qr_code(
            greeting_url,
            theme=theme,
            visible_message=visible_message,
            all_sides=all_sides,
            module_color=final_module_color,
            position_ring_color=final_ring_color
        )
    else:
        download_qr_img = qr_img  # Already generated above

    buf = io.BytesIO()
    download_qr_img.save(buf, format='PNG')
    byte_im = buf.getvalue()

    # Generate filename first for consistency
    filename = f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    # Download button with tracking callback
    st.download_button(
        label=_("common.buttons.download"),
        data=byte_im,
        file_name=filename,
        mime="image/png",
        width='stretch',
        on_click=log_download,
        args=(filename,)
    )

    # 8. Add Goodwill Payment Button
    st.markdown("---")
    st.link_button(_("common.buttons.buy_coffee"), "https://www.paypal.com/ncp/payment/NUQG396UTFRMG", help="Support the project with a small donation")
