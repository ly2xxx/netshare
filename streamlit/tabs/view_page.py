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
    Updated with warm, pottery-focused design for creators like Mia Mueller.
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
    
    # CSS will be embedded in the HTML for the iframe
    funnel_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Source+Sans+Pro:wght@400;600&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            background: #FAF7F2;
        }
        .funnel-container {
            max-width: 100%;
            min-height: 100vh;
            background: #FAF7F2;
            font-family: 'Source Sans Pro', sans-serif;
        }
        .funnel-video {
            width: 100%;
            height: 50vh;
            position: relative;
        }
        .funnel-video iframe, .funnel-video video {
            width: 100%;
            height: 100%;
            border: none;
            object-fit: cover;
        }
        .funnel-content {
            background: #FAF7F2;
            padding: 40px 20px;
            max-width: 600px;
            margin: 0 auto;
        }
        .funnel-headline {
            font-family: 'Poppins', sans-serif;
            font-size: 2em;
            font-weight: 600;
            color: #3E3830;
            text-align: center;
            margin-bottom: 15px;
            line-height: 1.2;
        }
        .funnel-offer {
            font-size: 1.1em;
            color: #3E3830;
            text-align: center;
            line-height: 1.7;
            margin-bottom: 25px;
            white-space: pre-wrap;
        }
        .funnel-benefits {
            margin: 25px 0;
            padding: 0;
        }
        .funnel-benefit {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
            font-size: 1.05em;
            color: #3E3830;
        }
        .funnel-benefit::before {
            content: '✓';
            color: #B8956A;
            font-weight: bold;
            margin-right: 10px;
            font-size: 1.3em;
        }
        .funnel-promo {
            background: #B8956A;
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.25em;
            text-align: center;
            margin: 25px auto;
            max-width: 300px;
            box-shadow: 0 3px 10px rgba(184, 149, 106, 0.3);
        }
        .funnel-urgency {
            color: #E74C3C;
            text-align: center;
            font-size: 1em;
            margin-bottom: 20px;
            font-weight: 500;
        }
        .funnel-urgency::before {
            content: '⏱ ';
        }
        .funnel-cta {
            display: block;
            background: linear-gradient(135deg, #B8956A 0%, #A67C52 100%);
            color: white !important;
            text-decoration: none;
            padding: 18px 40px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.25em;
            text-align: center;
            margin: 25px auto;
            max-width: 320px;
            box-shadow: 0 4px 12px rgba(184, 149, 106, 0.4);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .funnel-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(184, 149, 106, 0.5);
        }
        .funnel-separator {
            border: 0;
            height: 1px;
            background: #E8DCC8;
            margin: 30px 20px;
        }
        .funnel-trust {
            text-align: center;
            color: #666;
            font-size: 0.95em;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #E8DCC8;
        }
        .funnel-brand {
            text-align: center;
            color: #888;
            font-size: 0.9em;
            margin-top: 15px;
            font-style: italic;
        }
        .youtube-icon {
            width: 20px;
            height: 20px;
            vertical-align: middle;
            margin-right: 8px;
        }
    </style>
    """
    
    # Build video HTML
    video_html = ""
    if embed_url:
        if 'youtube.com' in embed_url:
            video_id = embed_url.split('/')[-1]
            video_html = f'''
            <div class="funnel-video">
                <iframe src="{embed_url}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=1"
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
    
    # Parse offer text for bullet points (if they exist)
    offer_lines = offer_text.split('\n')
    benefits_html = ""
    main_offer = []
    
    for line in offer_lines:
        line = line.strip()
        if line.startswith('✓') or line.startswith('•') or line.startswith('-'):
            # It's a benefit bullet
            benefit_text = line.lstrip('✓•- ').strip()
            benefits_html += f'<div class="funnel-benefit">{benefit_text}</div>'
        elif line:
            # Regular offer text
            main_offer.append(line)
    
    main_offer_text = '<br>'.join(main_offer)
    
    if benefits_html:
        benefits_section = f'<div class="funnel-benefits">{benefits_html}</div>'
    else:
        benefits_section = ""
    
    promo_html = f'<div class="funnel-promo">Use Code: {promo_code}</div>' if promo_code else ""
    urgency_html = f'<div class="funnel-urgency">{urgency}</div>' if urgency else ""
    
    # Trust section for pottery creators
    trust_html = ""
    if brand_name:
        trust_html = f'''
        <div class="funnel-trust">
            <img src="https://upload.wikimedia.org/wikipedia/commons/e/e5/Google_YouTube_icon_(2015-2022).svg" 
                 alt="YouTube" class="youtube-icon">
            As seen on {brand_name}
        </div>
        '''
    
    funnel_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {funnel_css}
    </head>
    <body>
        <div class="funnel-container">
            {video_html}
            <div class="funnel-content">
                <div class="funnel-headline">{headline}</div>
                <div class="funnel-offer">{main_offer_text}</div>
                {benefits_section}
                {promo_html}
                {urgency_html}
                <a href="{cta_url}" target="_blank" rel="noopener" class="funnel-cta">
                    {cta_text}
                </a>
                {trust_html}
            </div>
        </div>
    </body>
    </html>
    '''
    
    components.html(funnel_html, height=800, scrolling=True)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("Powered by QR-Greeting · Marketing Funnel")
        if st.button("Create Your Own Marketing Funnel", type="secondary", use_container_width=True):
            st.query_params.clear()
            st.query_params["tab"] = "funnel"
            st.rerun()
