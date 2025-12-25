"""
About Tab
Information about the application and its features
"""

import streamlit as st
from utils.download_tracker import get_download_count


def render() -> None:
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
