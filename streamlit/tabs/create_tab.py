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


def render() -> None:
    """Tab for creating new greeting QR codes"""
    # Display the banner image as the header (left-aligned, smaller for clarity)
    banner_path = os.path.join(os.path.dirname(__file__), "..", "banner", "qr-greeting-banner-4x.png")
    if os.path.exists(banner_path):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.image(banner_path, width='stretch')
    else:
        # Fallback to text header if banner not found
        st.markdown('<div class="main-header"><h1>🎄 Create Holiday Greeting QR Code</h1></div>',
                    unsafe_allow_html=True)
        st.markdown("### *A greener, smarter way to say happy holidays.*")

    st.write("Create a personalized holiday greeting that can be shared via QR code!")

    # =========================================================================
    # Step 1: Choose Theme & Background
    # =========================================================================
    st.markdown("### Step 1: Choose Your Theme & Background")
    st.info("💡 **Tip:** Pick a theme that matches your occasion. The colors will adapt automatically!")

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
            placeholder="https://youtu.be/..., https://facebook.com/reel/..., or https://example.com/video.mp4",
            help="Paste a YouTube URL, Google Drive shared video, Facebook video/reel, Instagram reel, or direct video link (.mp4, .webm, .mov, .avi, .m3u8)",
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
        gif_path = os.path.join(os.path.dirname(__file__), "..", "gif", selected_gif)
        if os.path.exists(gif_path):
            st.image(gif_path, caption=f"Preview: {selected_gif}", width='stretch')
        else:
            st.warning(f"GIF file not found: {selected_gif}")

    st.divider()

    # =========================================================================
    # Step 2: Greeting Details
    # =========================================================================
    st.markdown("### Step 2: Enter Your Greeting Details")
    st.info("💡 **Tip:** Fill in who the greeting is from, who it's for, and your personalized message!")

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

    st.divider()

    # =========================================================================
    # Step 3: Generate & Preview
    # =========================================================================
    st.markdown("### Step 3: QR Code Preview")

    if generate_btn:
        # Validate inputs
        if not from_name or not to_name or not message:
            st.error("Please fill in all required fields (From, To, and Message)")
        elif selected_gif_option == "(Enter custom URL...)":
            # Handle custom URL cases
            if not st.session_state.custom_video_url:
                # No URL entered - generate without background
                render_qr_generation_flow(
                    from_name=from_name,
                    to_name=to_name,
                    message=message,
                    theme=theme,
                    background=selected_gif,
                    visible_message=visible_message,
                    all_sides=all_sides,
                    warning_text="⚠️ No video URL entered. Generating QR code without background animation."
                )
            elif st.session_state.custom_url_validation_status != 'valid':
                # Invalid URL
                st.error(f"❌ Invalid video URL: {st.session_state.custom_url_validation_message}")
                st.info("💡 Please enter a valid YouTube or video URL, or select a different background option.")
            else:
                # Valid URL - proceed normally
                render_qr_generation_flow(
                    from_name=from_name,
                    to_name=to_name,
                    message=message,
                    theme=theme,
                    background=selected_gif,
                    visible_message=visible_message,
                    all_sides=all_sides
                )
        else:
            # Normal flow (local file or no background)
            render_qr_generation_flow(
                from_name=from_name,
                to_name=to_name,
                message=message,
                theme=theme,
                background=selected_gif,
                visible_message=visible_message,
                all_sides=all_sides
            )
    else:
        st.info("💡 **Tip:** Click 'Generate QR Code' above to create your personalized QR code!")
