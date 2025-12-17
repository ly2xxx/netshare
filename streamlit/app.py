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

    # QR codes are square, so height = width
    # Add extra space for caption and margins
    caption_space = 80 if caption else 40
    iframe_height = actual_display_width + caption_space

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

    # Render HTML Letter
    st.markdown(f"""
    <div class="letter-container">
        <div class="letter-header">
            <div class="letter-to"><strong>To:</strong> {greeting.get('to', 'Friend')}</div>
            <div class="letter-from"><strong>From:</strong> {greeting.get('from', 'Me')}</div>
        </div>
        <div class="letter-body">
{greeting.get('message', '')}
        </div>
        {icon_html}
        <div class="letter-footer">
            Created: {greeting.get('created', '').split('T')[0]}
        </div>
    </div>
    """, unsafe_allow_html=True)


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


def generate_qr_code(data: str, theme: str = "general", visible_message: str = None, error_correction=qrcode.constants.ERROR_CORRECT_H) -> Image.Image:
    """
    Generate QR code from data string

    Args:
        data: String data to encode
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

        # Icon should be ~20-25% of QR code size (safe margin under 30%)
        icon_size = int(min(qr_width, qr_height) * 0.22)

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
            
            # Common fonts to try
            font_names = ["arial.ttf", "calibri.ttf", "seguiemj.ttf", "segoeui.ttf", 
                          "LiberationSans-Regular.ttf", "DejaVuSans.ttf"]
            
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
            
            text_padding = int(padding / 2)

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
            
            # Create new image
            # Width: at least QR width. If text is somehow wider (min size limit), expand.
            final_width = max(qr_width, text_width + int(qr_width * 0.1)) # Ensure margins if text is wider
            final_height = qr_height + text_height + 2 * padding
            
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

            # Character counter
            if message:
                st.caption(f"Message length: {len(message)} characters")

            generate_btn = st.form_submit_button("Generate QR Code", icon=":material/qr_code_2:", type="primary", width='stretch')

    with col2:
        st.subheader("QR Code Preview")

        if generate_btn:
            # Debug: Check what values we received
            # st.write(f"Debug - from_name: '{from_name}', to_name: '{to_name}', message: '{message}'")

            if not from_name or not to_name or not message:
                st.error("Please fill in all required fields (From, To, and Message)")
            else:
                # Create greeting payload
                greeting = create_holiday_greeting(
                    from_name=from_name,
                    to_name=to_name,
                    message=message,
                    theme=theme
                )

                # Encode greeting as URL (for mobile scanning)
                greeting_url = encode_greeting_to_url(greeting)

                # Get statistics based on URL length
                stats = get_greeting_stats(greeting_url)

                # Generate QR code with URL data and theme icon
                qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_message)

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
                qr_img = generate_qr_code(greeting_url, theme=example['theme'])
                display_qr_with_protection(qr_img, caption="QR Code", width=None)


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

    # Map tab names to indices
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

    # Main tabs
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
