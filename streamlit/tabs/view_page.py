"""
View Page (Mobile Greeting View)
Displays greeting in a clean, mobile-friendly format when scanned from QR code
"""

import streamlit as st
from greeting_formats import decode_greeting_from_url
from config import THEME_ICONS


def render() -> None:
    """
    Display a greeting message in a clean, mobile-friendly format.
    This is shown when users scan the QR code with their phone camera.
    """
    # Get query parameters
    query_params = dict(st.query_params)

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
        if st.button("Create Greeting", type="secondary", use_container_width=True):
            st.query_params.clear()
            st.rerun()
