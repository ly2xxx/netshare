"""
View Page (Mobile Greeting View)
Displays greeting in a clean, mobile-friendly format when scanned from QR code
"""

import streamlit as st
from greeting_formats import decode_greeting_from_url
from config import THEME_ICONS
from i18n import get_text as _


def render() -> None:
    """
    Display a greeting message in a clean, mobile-friendly format.
    This is shown when users scan the QR code with their phone camera.
    """
    # Get query parameters
    query_params = dict(st.query_params)
    
    # Check if this is a funnel-type greeting
    greeting_type = query_params.get("t", "")
    
    if greeting_type == "funnel":
        render_funnel_view(query_params)
        return

    # Decode greeting from URL parameters
    greeting = decode_greeting_from_url(query_params)

    if not greeting:
        st.error(_("view_page.invalid_data"))
        st.write(_("view_page.scan_prompt"))
        if st.button(_("common.buttons.go_home")):
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
        st.markdown(f'<div class="greeting-from">{_("view_page.from", name=from_name)}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Subtle link to create your own (not prominent)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption(_("view_page.create_prompt"))
        if st.button(_("common.buttons.create_greeting"), type="secondary", width='stretch'):
            st.query_params.clear()
            st.rerun()


def render_funnel_view(params: dict) -> None:
    """
    Render marketing funnel experience when QR is scanned.
    """
    # Import here to avoid circular imports
    from utils.video_utils import convert_to_embed_url
    import streamlit.components.v1 as components
    
    # Extract funnel parameters (using compact names)
    headline = params.get("fh", "Special Offer")
    offer_text = params.get("m", "")
    cta_text = params.get("fc", "Learn More")
    cta_url = params.get("fu", "#")
    promo_code = params.get("fp", "")
    urgency = params.get("fg", "")
    video_url = params.get("bg", "")
    brand_name = params.get("f", "")
    theme = params.get("th", "fireworks")
    
    embed_url = convert_to_embed_url(video_url) if video_url else None
    
    # CSS for funnel experience
    st.markdown("""
    <style>
        .funnel-container {
            max-width: 100%;
            min-height: 100vh;
            background: #1a1a2e;
        }
        .funnel-video {
            width: 100%;
            height: 40vh;
        }
        .funnel-video iframe, .funnel-video video {
            width: 100%;
            height: 100%;
            border: none;
            object-fit: cover;
        }
        .funnel-overlay {
            background: white;
            margin: -30px 15px 15px 15px;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 -10px 40px rgba(0,0,0,0.3);
            position: relative;
            z-index: 10;
        }
        .funnel-headline {
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
            text-align: center;
            margin-bottom: 15px;
        }
        .funnel-offer {
            font-size: 1.1em;
            color: #555;
            text-align: center;
            line-height: 1.6;
            margin-bottom: 20px;
            white-space: pre-wrap;
        }
        .funnel-promo {
            background: linear-gradient(135deg, #ffd700 0%, #ffb347 100%);
            color: #333;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1.2em;
            text-align: center;
            margin-bottom: 15px;
        }
        .funnel-urgency {
            color: #e74c3c;
            text-align: center;
            font-size: 0.95em;
            margin-bottom: 15px;
        }
        .funnel-cta {
            display: block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 30px;
            font-weight: bold;
            font-size: 1.2em;
            text-align: center;
            margin: 20px auto;
            max-width: 300px;
        }
        .funnel-brand {
            text-align: center;
            color: #888;
            font-size: 0.85em;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Build video HTML
    video_html = ""
    if embed_url:
        if 'youtube.com' in embed_url:
            video_id = embed_url.split('/')[-1]
            video_html = f'''
            <div class="funnel-video">
                <iframe src="{embed_url}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0"
                        allow="autoplay; encrypted-media" allowfullscreen></iframe>
            </div>
            '''
        elif 'vimeo.com' in embed_url:
            video_html = f'''
            <div class="funnel-video">
                <iframe src="{embed_url}?autoplay=1&muted=1&loop=1&background=1"
                        allow="autoplay" allowfullscreen></iframe>
            </div>
            '''
        else:
            video_html = f'''
            <div class="funnel-video">
                <video autoplay muted loop playsinline>
                    <source src="{embed_url}" type="video/mp4">
                </video>
            </div>
            '''
    
    promo_html = f'<div class="funnel-promo">🏷️ {promo_code}</div>' if promo_code else ""
    urgency_html = f'<div class="funnel-urgency">⏰ {urgency}</div>' if urgency else ""
    brand_html = f'<div class="funnel-brand">from {brand_name}</div>' if brand_name else ""
    
    funnel_html = f'''
    <div class="funnel-container">
        {video_html}
        <div class="funnel-overlay">
            <div class="funnel-headline">{headline}</div>
            <div class="funnel-offer">{offer_text}</div>
            {promo_html}
            {urgency_html}
            <a href="{cta_url}" target="_blank" rel="noopener" class="funnel-cta">
                {cta_text}
            </a>
            {brand_html}
        </div>
    </div>
    '''
    
    components.html(funnel_html, height=700, scrolling=True)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("Powered by QR-Greeting")
        if st.button("Create Your Own Marketing Funnel", type="secondary", use_container_width=True):
            st.query_params.clear()
            st.query_params["tab"] = "funnel"
            st.rerun()
