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

    # Check if we have greeting data in URL (m or mc parameter indicates a message, or t=funnel for funnel)
    has_url_greeting = query_params.get('m') or query_params.get('mc') or query_params.get('t') == 'funnel'

    if has_url_greeting:
        # Check if this is a funnel-type QR code
        if query_params.get('t') == 'funnel':
            # Display funnel preview
            st.success(_("scan_tab.success") + " (Marketing Funnel)")
            
            # Extract funnel parameters
            headline = query_params.get("fh", "Special Offer")
            offer_text = query_params.get("m", "")
            cta_text = query_params.get("fc", "Learn More")
            cta_url = query_params.get("fu", "#")
            promo_code = query_params.get("fp", "")
            urgency = query_params.get("fg", "")
            video_url = query_params.get("bg", "")
            brand_name = query_params.get("f", "")
            theme = query_params.get("th", "fireworks")
            
            # Display funnel preview (similar to view_page but for scan tab)
            st.markdown("### 📈 Marketing Funnel QR Code Preview")
            
            col_a, col_b = st.columns([1, 1])
            
            with col_a:
                st.markdown("**📋 Funnel Details:**")
                st.write(f"**Headline:** {headline}")
                st.write(f"**Offer:** {offer_text[:100]}{'...' if len(offer_text) > 100 else ''}")
                st.write(f"**CTA Button:** {cta_text}")
                st.write(f"**Landing URL:** {cta_url}")
                if promo_code:
                    st.write(f"**Promo Code:** 🏷️ {promo_code}")
                if urgency:
                    st.write(f"**Urgency:** ⏰ {urgency}")
                if video_url:
                    st.write(f"**Video:** 🎬 {video_url[:50]}...")
                if brand_name:
                    st.write(f"**Brand:** {brand_name}")
                st.write(f"**Theme:** {theme}")
            
            with col_b:
                st.markdown("**👀 Mobile Preview:**")
                # Show a mockup of what the funnel looks like when scanned
                promo_html = f'<div style="background: #ffd700; color: #333; padding: 5px 15px; border-radius: 5px; font-weight: bold; margin: 10px 0; display: inline-block;">🏷️ {promo_code}</div>' if promo_code else ""
                urgency_html = f'<div style="color: #e74c3c; font-size: 0.9em; margin: 10px 0;">⏰ {urgency}</div>' if urgency else ""
                video_badge = "🎬 Video" if video_url else "No video"
                
                st.markdown(f"""
                <div style="border: 2px solid #333; border-radius: 15px; padding: 15px; 
                            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
                            color: white; max-width: 300px;">
                    <div style="background: #000; border-radius: 8px; height: 100px; 
                                display: flex; align-items: center; justify-content: center;
                                margin-bottom: 10px; position: relative;">
                        <span style="font-size: 2em;">🎬</span>
                        <div style="position: absolute; bottom: 5px; right: 5px; 
                                    background: rgba(255,255,255,0.2); padding: 2px 8px; 
                                    border-radius: 3px; font-size: 0.7em;">
                            {video_badge}
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.95); color: #333; 
                                padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 1.1em; font-weight: bold; margin-bottom: 8px;">
                            {headline}
                        </div>
                        <div style="font-size: 0.85em; margin-bottom: 10px; line-height: 1.4;">
                            {offer_text[:80]}{'...' if len(offer_text) > 80 else ''}
                        </div>
                        {promo_html}
                        {urgency_html}
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    color: white; padding: 10px 20px; border-radius: 20px; 
                                    font-weight: bold; cursor: pointer; display: inline-block; margin-top: 5px;">
                            {cta_text}
                        </div>
                    </div>
                    <div style="text-align: center; margin-top: 8px; font-size: 0.75em; opacity: 0.7;">
                        {f"from {brand_name}" if brand_name else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Option to create their own funnel or scan another
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📈 Create Your Own Funnel", width='stretch'):
                    st.query_params.clear()
                    st.query_params["tab"] = "funnel"
                    st.rerun()
            with col2:
                if st.button(_("common.buttons.scan_another"), width='stretch'):
                    st.query_params.clear()
                    st.query_params["tab"] = "scan"
                    st.rerun()
            
            return  # Don't show the upload interface
        else:
            # Regular greeting
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
                        # Update session state to ensure tab switches correctly
                        st.session_state.current_tab_index = 1  # create tab index
                        st.rerun()
                with col2:
                    if st.button(_("common.buttons.scan_another"), width='stretch'):
                        # Clear only the greeting params, keep tab=scan
                        st.query_params.clear()
                        st.query_params["tab"] = "scan"
                        # Update session state to ensure tab stays on scan
                        st.session_state.current_tab_index = 2  # scan tab index
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

                    # Check if this is a funnel QR code (contains t=funnel in URL)
                    is_funnel = 't=funnel' in qr_data or '&t=funnel' in qr_data
                    
                    with col2:
                        st.subheader(_("scan_tab.greeting_message"))

                        if is_funnel:
                            # Parse URL parameters from funnel QR
                            import urllib.parse
                            try:
                                # Extract query parameters
                                if '?' in qr_data:
                                    query_string = qr_data.split('?', 1)[1]
                                    params = dict(urllib.parse.parse_qsl(query_string))
                                    
                                    # Display funnel preview
                                    st.success("Marketing Funnel QR Decoded!")
                                    
                                    headline = params.get("fh", "Special Offer")
                                    offer_text = params.get("m", "")
                                    cta_text = params.get("fc", "Learn More")
                                    cta_url = params.get("fu", "#")
                                    promo_code = params.get("fp", "")
                                    urgency = params.get("fg", "")
                                    video_url = params.get("bg", "")
                                    brand_name = params.get("f", "")
                                    
                                    st.markdown("**📋 Funnel Details:**")
                                    st.write(f"**Headline:** {headline}")
                                    st.write(f"**Offer:** {offer_text}")
                                    st.write(f"**CTA Button:** {cta_text}")
                                    st.write(f"**Landing URL:** {cta_url}")
                                    if promo_code:
                                        st.write(f"**Promo Code:** 🏷️ {promo_code}")
                                    if urgency:
                                        st.write(f"**Urgency:** ⏰ {urgency}")
                                    if video_url:
                                        st.write(f"**Video:** 🎬 Yes")
                                    if brand_name:
                                        st.write(f"**Brand:** {brand_name}")
                                    
                                    st.markdown("---")
                                    st.info("💡 This is a Marketing Funnel QR. When scanned with a phone, it will play a video and show this offer.")
                                    
                            except Exception as e:
                                st.error(f"Error parsing funnel QR: {e}")
                                st.code(qr_data)
                        else:
                            # Parse as regular greeting (handles both URL and JSON formats)
                            greeting = parse_greeting(qr_data)

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
