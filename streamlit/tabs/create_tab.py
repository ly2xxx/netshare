"""
Create Greeting Tab
UI for creating new greeting QR codes
"""

import streamlit as st
import os
from tabs.components import (
    render_theme_selector,
    validate_custom_url_callback,
    render_qr_generation_flow
)
from utils.file_utils import get_available_gifs
from utils.url_utils import is_web_url
from config import THEME_ICONS
from qr.display import display_greeting_letter
from datetime import datetime
from i18n import get_text as _


def load_params_from_url():
    """Load greeting parameters from URL query params if present"""
    try:
        query_params = st.query_params
        
        # Check if we have plaintext API parameters
        if 'from' in query_params or 'message' in query_params:
            # Mark that we've loaded from URL (only do this once)
            if 'params_loaded_from_url' not in st.session_state:
                st.session_state.params_loaded_from_url = True
                
                # Load from parameter
                if 'from' in query_params:
                    st.session_state.create_from_name = query_params['from']
                
                # Load to parameter
                if 'to' in query_params:
                    st.session_state.create_to_name = query_params['to']
                
                # Load message parameter
                if 'message' in query_params:
                    message_text = query_params['message']
                    # Append URL to message if URL parameter exists
                    if 'url' in query_params:
                        message_text = f"{message_text}\n{query_params['url']}"
                    st.session_state.create_message = message_text
                
                # Load theme parameter
                if 'theme' in query_params:
                    st.session_state.selected_theme = query_params['theme']
                
                # Load URL parameter (store for later use or display)
                if 'url' in query_params:
                    st.session_state.source_url = query_params['url']
                    # Show info banner that this was shared from another app
                    st.session_state.show_source_banner = True

                # Load background parameter
                if 'background' in query_params:
                    background_param = query_params['background']

                    # Web URL: Set custom option and validate
                    if is_web_url(background_param):
                        st.session_state.selected_gif_option = _("create_tab.background.custom")
                        st.session_state.custom_video_url = background_param

                        # Trigger validation manually
                        st.session_state.custom_video_url_input = background_param
                        validate_custom_url_callback()

                        # Store validation errors for banner display
                        if st.session_state.custom_url_validation_status != 'valid':
                            st.session_state.background_validation_warning = (
                                f"⚠️ Background URL validation issue: "
                                f"{st.session_state.custom_url_validation_message}"
                            )

                    # Local file: Verify existence
                    else:
                        available_gifs = get_available_gifs()
                        if background_param in available_gifs:
                            st.session_state.selected_gif_option = background_param
                        else:
                            st.session_state.background_validation_warning = (
                                f"⚠️ Background file '{background_param}' not found. Using no background."
                            )
                            st.session_state.selected_gif_option = _("create_tab.background.none")
    except Exception as e:
        # Silently handle any query param errors
        pass


def render() -> None:
    """Tab for creating new greeting QR codes"""
    
    # Load URL parameters if present (only runs once)
    load_params_from_url()
    
    # Show banner if this greeting was shared from another app
    if st.session_state.get('show_source_banner', False):
        source_url = st.session_state.get('source_url', '')
        st.info(f"✨ Pre-filled from: {source_url}")
        st.session_state.show_source_banner = False  # Only show once

    # Show background validation warning if present
    if st.session_state.get('background_validation_warning', ''):
        st.warning(st.session_state.background_validation_warning)
        st.session_state.background_validation_warning = ''  # Only show once

    # Display the banner image as the header (left-aligned, smaller for clarity)
    banner_path = os.path.join(os.path.dirname(__file__), "..", "banner", "qr-greeting-banner-4x.png")
    if os.path.exists(banner_path):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.image(banner_path, width='stretch')
    else:
        # Fallback to text header if banner not found
        st.markdown(f'<div class="main-header"><h1>{_("create_tab.header")}</h1></div>',
                    unsafe_allow_html=True)
        st.markdown(f"### {_('create_tab.subtitle')}")

    st.write(_("create_tab.intro"))

    # =========================================================================
    # Step 1: Choose Theme & Background
    # =========================================================================
    st.markdown(_("create_tab.step1.title"))
    st.info(_("create_tab.step1.tip"))

    # Theme selector outside form to allow interactive button clicks
    theme = render_theme_selector()

    st.markdown("---")

    # GIF background dropdown - OUTSIDE form to allow immediate preview
    available_gifs = get_available_gifs()
    gif_options = [_("create_tab.background.none"), _("create_tab.background.custom")] + available_gifs

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
        _("create_tab.background.label"),
        options=gif_options,
        index=gif_options.index(st.session_state.selected_gif_option) if st.session_state.selected_gif_option in gif_options else 0,
        help=_("create_tab.background.help"),
        key="greeting_gif_background_interactive"
    )

    # Update session state
    st.session_state.selected_gif_option = selected_gif_option

    # Show custom URL input when "(Enter custom URL...)" is selected
    if selected_gif_option == _("create_tab.background.custom"):
        custom_url = st.text_input(
            _("create_tab.video_url.label"),
            value=st.session_state.custom_video_url,
            placeholder=_("create_tab.video_url.placeholder"),
            help=_("create_tab.video_url.help"),
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
            st.info(_("create_tab.video_url.validating"))
        else:
            st.info(_("create_tab.video_url.enter_prompt"))

    # Convert selection to background parameter
    if selected_gif_option == _("create_tab.background.none"):
        selected_gif = ""
    elif selected_gif_option == _("create_tab.background.custom"):
        # Use custom URL if validated, otherwise empty
        if st.session_state.custom_url_validation_status == 'valid':
            selected_gif = st.session_state.custom_video_url
        else:
            selected_gif = ""
    else:
        # Local file selected
        selected_gif = selected_gif_option

    # Immediate preview below the dropdown (only for local files)
    if selected_gif and selected_gif_option != _("create_tab.background.custom"):
        gif_path = os.path.join(os.path.dirname(__file__), "..", "gif", selected_gif)
        if os.path.exists(gif_path):
            st.image(gif_path, caption=_("create_tab.gif_preview", gif_name=selected_gif), width='stretch')
        else:
            st.warning(_("create_tab.gif_not_found", file=selected_gif))

    st.divider()

    # =========================================================================
    # Step 2: Preview & Personalize (matching demo_tab layout)
    # =========================================================================
    st.markdown(_("create_tab.step2.title"))
    st.info(_("create_tab.step2.tip"))

    # Initialize session state for greeting fields with sample data
    if 'create_from_name' not in st.session_state:
        st.session_state.create_from_name = _("common.placeholders.your_name")
    if 'create_to_name' not in st.session_state:
        st.session_state.create_to_name = _("common.placeholders.friend_name")
    if 'create_message' not in st.session_state:
        st.session_state.create_message = _("create_tab.default_message")
    if 'create_visible_message' not in st.session_state:
        st.session_state.create_visible_message = ""
    if 'create_all_sides' not in st.session_state:
        st.session_state.create_all_sides = False

    # Get theme emoji for preview
    theme_emoji = THEME_ICONS.get(theme, "🎁")

    # Live Greeting Card Preview (matching demo_tab style)
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; color: white; box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4); max-width: 600px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 3em; margin-bottom: 10px;">{theme_emoji}</div>
    </div>
    <div style="background: rgba(255,255,255,0.95); color: #333; padding: 25px; border-radius: 15px; position: relative;">
        <p style="margin: 5px 0 0 0; font-weight: 600; font-size: 1.1em;">{_("create_tab.preview.from", name=st.session_state.create_from_name)}</p>
        <p style="margin: 5px 0 20px 0; font-weight: 600; font-size: 1.1em;">{_("create_tab.preview.to", name=st.session_state.create_to_name)}</p>
        <p style="font-family: Georgia, serif; font-size: 1.15em; line-height: 1.6; color: #444; font-style: italic; margin: 0;">"{st.session_state.create_message}"</p>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Expandable edit section (matching demo_tab style)
    with st.expander(_("create_tab.edit.title"), expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_from = st.text_input(
                _("common.labels.from"),
                value=st.session_state.create_from_name,
                key="edit_from_name",
                placeholder=_("common.placeholders.your_name")
            )
            # Auto-update session state
            if new_from != st.session_state.create_from_name:
                st.session_state.create_from_name = new_from
                st.rerun()
        with col2:
            new_to = st.text_input(
                _("common.labels.to"),
                value=st.session_state.create_to_name,
                key="edit_to_name",
                placeholder=_("common.placeholders.friend_name")
            )
            # Auto-update session state
            if new_to != st.session_state.create_to_name:
                st.session_state.create_to_name = new_to
                st.rerun()

        new_message = st.text_area(
            _("common.labels.message"),
            value=st.session_state.create_message,
            height=100,
            key="edit_message",
            placeholder=_("common.placeholders.message")
        )
        # Auto-update session state
        if new_message != st.session_state.create_message:
            st.session_state.create_message = new_message
            st.rerun()

        # Character counter
        if new_message:
            st.caption(_("create_tab.message_length", count=len(new_message)))

    # QR Code options section (keeping existing features)
    with st.expander(_("create_tab.qr_options.title"), expanded=False):
        visible_message = st.text_input(
            _("create_tab.visible_message.label"),
            value=st.session_state.create_visible_message,
            placeholder=_("create_tab.visible_message.placeholder"),
            help=_("create_tab.visible_message.help"),
            key="edit_visible_message"
        )

        all_sides = st.checkbox(
            _("create_tab.add_all_sides"),
            value=st.session_state.create_all_sides,
            help=_("create_tab.add_all_sides_help"),
            key="edit_all_sides"
        )

        # Update session state when changed
        if visible_message != st.session_state.create_visible_message:
            st.session_state.create_visible_message = visible_message
        if all_sides != st.session_state.create_all_sides:
            st.session_state.create_all_sides = all_sides

    st.divider()

    # =========================================================================
    # Step 3: Generate & Preview
    # =========================================================================
    st.markdown(_("create_tab.step3.title"))
    st.info(_("create_tab.step3.tip"))

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            _("common.buttons.generate"),
            type="primary",
            key="create_tab_generate_btn",
            icon=":material/qr_code_2:"
        )

    if generate_btn:
        # Get values from session state
        from_name = st.session_state.create_from_name
        to_name = st.session_state.create_to_name
        message = st.session_state.create_message
        visible_message = st.session_state.create_visible_message
        all_sides = st.session_state.create_all_sides

        # Validate inputs
        if not from_name or not to_name or not message:
            st.error(_("create_tab.error.required_fields"))
        # elif from_name == "Your Name" or to_name == "Friend's Name":
        #     st.warning("⚠️ Please personalize the From and To names before generating!")
        else:
            # Determine background and warning text
            warning_text = None
            background = selected_gif

            if selected_gif_option == _("create_tab.background.custom"):
                if not st.session_state.custom_video_url:
                    warning_text = _("create_tab.warning.no_video")
                    background = ""
                elif st.session_state.custom_url_validation_status != 'valid':
                    st.error(_("create_tab.error.invalid_video", message=st.session_state.custom_url_validation_message))
                    st.info(_("create_tab.error.video_suggestion"))
                    st.stop()

            # Show success message
            st.success(_("create_tab.success"))

            # Show warning if applicable
            if warning_text:
                st.warning(warning_text)

            # Two-column layout matching demo_tab
            qr_col, preview_col = st.columns([1, 1])

            with qr_col:
                st.markdown(f"#### {_('create_tab.qr_section')}")
                # Generate and display QR code
                render_qr_generation_flow(
                    from_name=from_name,
                    to_name=to_name,
                    message=message,
                    theme=theme,
                    background=background,
                    visible_message=visible_message,
                    all_sides=all_sides
                )

            with preview_col:
                st.markdown(f"#### {_('create_tab.preview_section')}")
                st.caption(_("create_tab.preview_caption"))
                # Create greeting dict matching what display_greeting_letter expects
                preview_greeting = {
                    'to': to_name,
                    'from': from_name,
                    'message': message,
                    'theme': theme,
                    'background': background,
                    'created': datetime.now().strftime('%Y-%m-%d')
                }
                # Use the same display function as scan_tab
                display_greeting_letter(preview_greeting)

            st.markdown("---")

            # Start Over button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(_("common.buttons.create_another"), type="secondary", key="create_tab_start_over"):
                    # Reset session state
                    st.session_state.create_from_name = _("common.placeholders.your_name")
                    st.session_state.create_to_name = _("common.placeholders.friend_name")
                    st.session_state.create_message = _("create_tab.default_message")
                    st.session_state.create_visible_message = ""
                    st.session_state.create_all_sides = False
                    # Clear URL param flag
                    if 'params_loaded_from_url' in st.session_state:
                        del st.session_state.params_loaded_from_url
                    # Clear background validation warning
                    if 'background_validation_warning' in st.session_state:
                        del st.session_state.background_validation_warning
                    st.rerun()
