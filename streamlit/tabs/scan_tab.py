"""
Scan Greeting Tab
UI for scanning/decoding greeting QR codes
"""

import streamlit as st
from PIL import Image
import numpy as np
from i18n import get_text as _

# Import cv2 lazily to avoid startup crashes if system libs missing
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError as e:
    CV2_AVAILABLE = False
    CV2_IMPORT_ERROR = str(e)

except ImportError as e:
    CV2_AVAILABLE = False
    CV2_IMPORT_ERROR = str(e)

try:
    import zxingcpp
    ZXING_AVAILABLE = True
except ImportError:
    ZXING_AVAILABLE = False

from greeting_formats import (
    parse_greeting,
    format_greeting_display,
    decode_greeting_from_url
)
from qr.display import display_greeting_letter


def render() -> None:
    """Tab for scanning/decoding greeting QR codes"""
    st.markdown(f'<div class="main-header"><h1>{_("scan_tab.header")}</h1></div>',
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
            st.success(_("scan_tab.success"))

            # Display the full letter format
            display_greeting_letter(greeting)

            st.markdown("---")
            st.link_button(_("common.buttons.buy_coffee"), "https://www.paypal.com/ncp/payment/NUQG396UTFRMG", help="Support the project with a small donation")

            # Option to create their own or scan another
            col1, col2 = st.columns(2)
            with col1:
                if st.button(_("scan_tab.create_own"), width='stretch'):
                    st.query_params.clear()
                    st.query_params["tab"] = "create"
                    st.rerun()
            with col2:
                if st.button(_("common.buttons.scan_another"), width='stretch'):
                    # Clear only the greeting params, keep tab=scan
                    st.query_params.clear()
                    st.query_params["tab"] = "scan"
                    st.rerun()

            return  # Don't show the upload interface
        else:
            st.warning(_("scan_tab.url_decode_error"))

    # Normal upload interface
    st.write(_("scan_tab.intro"))

    uploaded_file = st.file_uploader(
        _("scan_tab.upload.label"),
        type=['png', 'jpg', 'jpeg'],
        help=_("scan_tab.upload.help")
    )

    if uploaded_file is not None:
        try:
            # Display uploaded image
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader(_("scan_tab.uploaded_qr"))
                image = Image.open(uploaded_file)
                st.image(image, caption=_("scan_tab.uploaded_image"), width='stretch')

            # Decode QR code
            try:
                decoded_data = None
                
                # Check for zxing-cpp first (better detection rate and no system deps)
                if ZXING_AVAILABLE:
                    try:
                        # zxing-cpp works best with grayscale
                        img_gray = image.convert('L')
                        results = zxingcpp.read_barcodes(img_gray)
                        if results:
                            decoded_data = results[0].text
                    except Exception as e:
                        print(f"ZXing-cpp scan error: {e}")
                
                # Fallback to OpenCV if zxing-cpp failed or not available
                if not decoded_data and CV2_AVAILABLE:
                    # Use OpenCV for decoding
                    # Convert PIL Image to BGR numpy array
                    image_array = np.array(image.convert('RGB'))
                    image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

                    detector = cv2.QRCodeDetector()
                    data, bbox, _points = detector.detectAndDecode(image_array)
                    
                    if data:
                        decoded_data = data

                if decoded_data:
                    qr_data = decoded_data

                    # Parse greeting (handles both URL and JSON formats)
                    greeting = parse_greeting(qr_data)

                    with col2:
                        st.subheader(_("scan_tab.greeting_message"))

                        if greeting:
                            # Display formatted greeting
                            display_greeting_letter(greeting)

                            st.markdown("---")
                            st.link_button(_("common.buttons.buy_coffee"), "https://www.paypal.com/ncp/payment/NUQG396UTFRMG", help="Support the project with a small donation")
                        else:
                            st.warning(_("scan_tab.invalid_format"))
                            st.write(_("scan_tab.decoded_data"))
                            st.code(qr_data)
                else:
                    msg = _("scan_tab.no_qr_found")
                    if not ZXING_AVAILABLE and not CV2_AVAILABLE:
                        msg += " " + _("scan_tab.no_libs")
                    elif not ZXING_AVAILABLE:
                        msg += " " + _("scan_tab.zxing_suggestion")

                    st.error(msg)

            except ImportError as e:
                st.error(_("scan_tab.opencv_required"))
                st.info(_("scan_tab.manual_entry"))

                manual_data = st.text_area(_("scan_tab.paste_label"))
                if manual_data:
                    greeting = parse_greeting(manual_data)
                    if greeting:
                        st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                        st.write(format_greeting_display(greeting))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(_("scan_tab.invalid_data"))

            except Exception as e:
                st.error(_("scan_tab.error", error=str(e)))
                st.info(_("scan_tab.alternative"))

                manual_data = st.text_area(_("scan_tab.paste_label"), key="manual_data_exception")
                if manual_data:
                    greeting = parse_greeting(manual_data)
                    if greeting:
                        st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                        st.write(format_greeting_display(greeting))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(_("scan_tab.invalid_data"))

        except Exception as e:
            st.error(_("scan_tab.error", error=str(e)))
