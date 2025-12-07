#!/usr/bin/env python3
"""
Holiday Greeting QR Code Generator
A Streamlit app for creating and reading holiday greeting QR codes
"""

import streamlit as st
import qrcode
from PIL import Image
import io
import json
from datetime import datetime
import cv2
import numpy as np
from greeting_formats import (
    create_holiday_greeting,
    compact_greeting,
    parse_greeting,
    format_greeting_display,
    get_greeting_stats
)

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
</style>
""", unsafe_allow_html=True)


def generate_qr_code(data: str, error_correction=qrcode.constants.ERROR_CORRECT_H) -> Image.Image:
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
    return pil_img


def create_greeting_tab():
    """Tab for creating new greeting QR codes"""
    st.markdown('<div class="main-header"><h1>🎄 Create Holiday Greeting QR Code</h1></div>',
                unsafe_allow_html=True)

    st.write("Create a personalized holiday greeting that can be shared via QR code!")

    # Two column layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Greeting Details")

        from_name = st.text_input(
            "From (Your Name)",
            placeholder="Alice",
            help="Who is sending this greeting?"
        )

        to_name = st.text_input(
            "To (Recipient Name)",
            placeholder="Bob",
            help="Who will receive this greeting?"
        )

        occasion = st.selectbox(
            "Occasion",
            [
                "Christmas 2025",
                "New Year 2026",
                "Holiday Season 2025",
                "Birthday",
                "Wedding",
                "Anniversary",
                "Thank You",
                "Custom"
            ]
        )

        if occasion == "Custom":
            occasion = st.text_input("Custom Occasion", placeholder="Enter custom occasion")

        theme = st.selectbox(
            "Theme",
            [
                "snowflake",
                "fireworks",
                "lights",
                "stars",
                "confetti",
                "champagne",
                "hearts",
                "general"
            ],
            help="Visual theme for the greeting"
        )

        message = st.text_area(
            "Your Message",
            placeholder="Merry Christmas! Wishing you joy and happiness this season...",
            height=150,
            help="Your personalized greeting message"
        )

        # Character counter
        if message:
            st.caption(f"Message length: {len(message)} characters")

        generate_btn = st.button("🎁 Generate QR Code", type="primary", use_container_width=True)

    with col2:
        st.subheader("QR Code Preview")

        if generate_btn:
            if not from_name or not to_name or not message:
                st.error("Please fill in all required fields (From, To, and Message)")
            else:
                # Create greeting payload
                greeting = create_holiday_greeting(
                    from_name=from_name,
                    to_name=to_name,
                    message=message,
                    occasion=occasion,
                    theme=theme
                )

                # Compact to JSON
                greeting_json = compact_greeting(greeting)

                # Get statistics
                stats = get_greeting_stats(greeting_json)

                # Generate QR code
                qr_img = generate_qr_code(greeting_json)

                # Display QR code
                st.image(qr_img, caption=f"Greeting QR Code for {to_name}", width='stretch')

                # Statistics
                st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                st.write("**QR Code Statistics:**")
                st.write(f"- Data size: {stats['byte_size']} bytes")
                st.write(f"- QR Version: ~{stats['recommended_qr_version']}")
                st.write(f"- Scannable: {'✅ Yes' if stats['fits_in_qr'] else '❌ Too large'}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Download button
                buf = io.BytesIO()
                qr_img.save(buf, format='PNG')
                byte_im = buf.getvalue()

                st.download_button(
                    label="📥 Download QR Code",
                    data=byte_im,
                    file_name=f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True
                )

                # Show JSON data
                with st.expander("View JSON Data"):
                    st.code(json.dumps(greeting, indent=2), language='json')





def scan_greeting_tab():
    """Tab for scanning/decoding greeting QR codes"""
    st.markdown('<div class="main-header"><h1>📱 Scan Greeting QR Code</h1></div>',
                unsafe_allow_html=True)

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
            # Decode QR code
            try:
                # Use OpenCV for decoding (No pyzbar dependency)
                # Convert PIL Image to BGR numpy array
                image_array = np.array(image.convert('RGB'))
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

                detector = cv2.QRCodeDetector()
                data, bbox, _ = detector.detectAndDecode(image_array)

                if data:
                    qr_data = data

                    # Parse greeting
                    greeting = parse_greeting(qr_data)

                    with col2:
                        st.subheader("Greeting Message")

                        if greeting:
                            # Display formatted greeting
                            st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                            st.write(f"**From:** {greeting['from']}")
                            st.write(f"**To:** {greeting['to']}")
                            st.write(f"**Occasion:** {greeting['occasion']}")
                            st.markdown("---")
                            st.write(greeting['message'])
                            st.markdown("---")
                            st.caption(f"Theme: {greeting.get('theme', 'general')}")
                            st.caption(f"Created: {greeting.get('created', 'Unknown')}")
                            st.markdown('</div>', unsafe_allow_html=True)

                            # Show raw data
                            with st.expander("View Raw Data"):
                                st.code(json.dumps(greeting, indent=2), language='json')
                        else:
                            st.warning("This QR code doesn't contain a valid greeting format.")
                            st.write("**Decoded data:**")
                            st.code(qr_data)
                else:
                    st.error("No QR code found in the image. Please upload a valid QR code image.")

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Alternatively, you can manually paste the QR code data below:")
                
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
            "occasion": "Christmas 2025",
            "theme": "snowflake",
            "message": "Merry Christmas! Wishing you joy and happiness this season. Thank you for being a wonderful friend!"
        },
        {
            "title": "🎆 New Year Message",
            "from": "Bob",
            "to": "Future Me",
            "occasion": "New Year 2026",
            "theme": "fireworks",
            "message": "2025 was incredible! Here's to growth and new adventures in 2026!"
        },
        {
            "title": "💍 Wedding Save the Date",
            "from": "Emma & James",
            "to": "Friends and Family",
            "occasion": "Wedding Announcement",
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
                st.write(f"**Occasion:** {example['occasion']}")
                st.write(f"**Theme:** {example['theme']}")
                st.markdown("---")
                st.write(example['message'])

            with col2:
                # Generate QR for example
                greeting = create_holiday_greeting(
                    from_name=example['from'],
                    to_name=example['to'],
                    message=example['message'],
                    occasion=example['occasion'],
                    theme=example['theme']
                )
                greeting_json = compact_greeting(greeting)
                qr_img = generate_qr_code(greeting_json)
                st.image(qr_img, caption="QR Code", width='stretch')


def about_tab():
    """About the application"""
    st.markdown('<div class="main-header"><h1>ℹ️ About</h1></div>',
                unsafe_allow_html=True)

    st.write("""
    ## Holiday Greeting QR Code Generator

    This application allows you to create personalized holiday greetings encoded in QR codes.
    Share your messages in a unique and modern way!

    ### Features
    - 🎁 Create custom greeting QR codes
    - 📱 Scan and read greeting QR codes
    - 🎨 Multiple theme options
    - 📥 Download QR codes as images
    - 💾 Compact JSON format for efficient encoding

    ### How It Works
    1. Enter your greeting details (from, to, message, occasion)
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


def main():
    """Main application"""

    # Sidebar
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/anthropics/anthropic-quickstarts/main/computer-use-demo/image.png",
                 width=100)
        st.title("Holiday Greeting QR")
        st.write("Create and share personalized holiday greetings via QR codes!")

        st.markdown("---")

        st.write("### Quick Tips")
        st.info("""
        💡 Keep messages under 300 characters for best QR code size

        📱 Test QR codes with your phone camera app

        🎨 Choose themes that match your occasion
        """)

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
