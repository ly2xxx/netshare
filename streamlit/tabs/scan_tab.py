"""
Scan Greeting Tab
UI for scanning/decoding greeting QR codes
"""

import streamlit as st
from PIL import Image
import numpy as np

# Import cv2 lazily to avoid startup crashes if system libs missing
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError as e:
    CV2_AVAILABLE = False
    CV2_IMPORT_ERROR = str(e)

from greeting_formats import (
    parse_greeting,
    format_greeting_display,
    decode_greeting_from_url
)
from qr.display import display_greeting_letter


def render() -> None:
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
