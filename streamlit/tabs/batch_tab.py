"""
Batch Tab
Batch QR code generation from CSV upload
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
from datetime import datetime
import zipfile

from greeting_formats import create_holiday_greeting, encode_greeting_to_url
from qr.generator import generate_qr_code
from utils.file_utils import get_all_available_backgrounds, get_available_backgrounds, get_available_gifs
from utils.url_utils import is_web_url, classify_background, convert_youtube_to_embed_url, convert_google_drive_to_embed_url
from config import THEME_ICONS


def render() -> None:
    """Tab for batch QR code generation from Excel"""

    # Initialize session state for batch DataFrame
    if 'batch_df' not in st.session_state:
        st.session_state.batch_df = None

    st.markdown('<div class="main-header"><h1>📦 Batch QR Code Generation</h1></div>',
                unsafe_allow_html=True)

    st.write("Generate multiple QR codes at once by uploading an Excel spreadsheet.")
    st.info("💡 **New Feature**: You can now use YouTube URLs or direct video URLs as backgrounds! Just paste the URL in the Background column.")

    # Available themes and backgrounds for reference
    available_themes = list(THEME_ICONS.keys())
    all_backgrounds, background_folder_map = get_all_available_backgrounds()
    available_backgrounds_keep = get_available_backgrounds()
    available_backgrounds_gif = get_available_gifs()

    st.markdown("---")

    # Template download section
    st.subheader("1. Download Template")
    st.write("Download the Excel template, fill in your greetings, then upload it below.")

    # Create template Excel file in memory
    try:
        # Create sample data with 4 test cases
        sample_data = {
            "From": ["Alice", "Bob", "Charlie", "David"],
            "To": ["Bob", "Alice", "Dana", "Eve"],
            "Message": ["Merry Christmas!", "Happy New Year!", "Season's Greetings!\nhttps://qr-greeting.co.uk", "Enjoy the holidays!"],
            "Theme": ["snowflake", "fireworks", "hearts", "lights"],
            "Background": ["letter-background-design-01.jpg", "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4", "https://youtu.be/6SuLXoRmykE", "christmas-lights.gif"],
            "VisibleMessage": ["Scan me!", "BOB", "Happy Holidays!", "Ho Ho Ho!"]
        }
        df_template = pd.DataFrame(sample_data)

        # Save to CSV
        csv_data = df_template.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download Template (.csv)",
            data=csv_data,
            file_name="qr_greeting_template.csv",
            mime="text/csv"
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
                if available_backgrounds_keep:
                    for bg in available_backgrounds_keep:
                        st.write(f"- `{bg}`")
                else:
                    st.write("No backgrounds available in `keep/` folder")
                st.write("")
                st.write("*Local files from `gif/` folder:*")
                if available_backgrounds_gif:
                    for bg in available_backgrounds_gif:
                        st.write(f"- `{bg}`")
                else:
                    st.write("No backgrounds available in `gif/` folder")
                st.write("")
                st.write("*Or use web video URLs:*")
                st.write("- YouTube: `youtu.be/VIDEO_ID`")
                st.write("- YouTube: `https://www.youtube.com/watch?v=VIDEO_ID`")
                st.write("- Direct video: `https://example.com/video.mp4`")

    except ImportError:
        st.error("pandas is required for batch processing. Please install it: `pip install pandas`")
        return

    st.markdown("---")

    # Upload section
    st.subheader("2. Upload Filled Template")

    uploaded_file = st.file_uploader(
        "Choose your filled CSV file",
        type=['csv'],
        help="Upload the template with your greeting data"
    )

    if uploaded_file is not None:
        try:
            # Load CSV into session state (only when new file is uploaded)
            df = pd.read_csv(uploaded_file)
            # Check if this is a new upload by comparing with existing data
            if st.session_state.batch_df is None or len(df) != len(st.session_state.batch_df):
                st.session_state.batch_df = df

            st.success(f"Loaded {len(st.session_state.batch_df)} greetings from CSV!")

            # Preview data with editable interface
            with st.expander("Preview Data"):
                st.session_state.batch_df = st.data_editor(
                    st.session_state.batch_df,
                    key="batch_data_editor",
                    num_rows="dynamic"
                )

            # Validate data
            required_cols = ["From", "To", "Message"]
            missing_cols = [col for col in required_cols if col not in st.session_state.batch_df.columns]

            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                return

            # Validate themes
            if "Theme" in st.session_state.batch_df.columns:
                invalid_themes = st.session_state.batch_df[~st.session_state.batch_df["Theme"].isna() & ~st.session_state.batch_df["Theme"].isin(available_themes)]["Theme"].unique()
                if len(invalid_themes) > 0:
                    st.warning(f"Some rows have invalid themes: {list(invalid_themes)}. They will use 'general'.")

            # Generate button
            if st.button("🚀 Generate All QR Codes", type="primary"):
                zip_buffer = BytesIO()

                progress = st.progress(0)
                status = st.empty()

                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for idx, row in st.session_state.batch_df.iterrows():
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
                            else:
                                # Check if background exists in either folder
                                background_found = False

                                # Check keep/ folder first
                                keep_path = Path(__file__).parent.parent / "keep" / background
                                if keep_path.exists():
                                    background_found = True
                                else:
                                    # Check gif/ folder
                                    gif_path = Path(__file__).parent.parent / "gif" / background
                                    if gif_path.exists():
                                        background_found = True

                                if not background_found:
                                    st.warning(f"Row {idx + 1}: Background file '{background}' not found in keep/ or gif/ folders - skipping background")
                                    background = ""

                        status.text(f"Generating QR {idx + 1}/{len(st.session_state.batch_df)}: {to_name}...")

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

                        progress.progress((idx + 1) / len(st.session_state.batch_df))

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
