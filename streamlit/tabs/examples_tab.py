"""
Examples Tab
Displays example greeting configurations and their QR codes
"""

import streamlit as st
from greeting_formats import create_holiday_greeting, encode_greeting_to_url
from qr.generator import generate_qr_code
from qr.display import display_qr_with_protection
from config import THEME_COLORS


def render() -> None:
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
        },
        {
            "title": "👋 Farewell to Colleagues",
            "from": "Alex",
            "to": "The Team",
            "theme": "farewell",
            "message": "It's been an amazing journey working with you all! Thank you for the memories, the laughs, and the lessons. Let's stay in touch!",
            "visible_message": "Scan to read my farewell note"
        },
        {
            "title": "🔥 Mission Impossible - Self-Destructing Message",
            "from": "IMF Agent",
            "to": "Field Operative",
            "theme": "burn_after_read",
            "message": "Your mission: Rendezvous at Café Milano, 1800 hours. Bring the package. Delete this message after reading. No digital trail - no email interception, no AI monitoring, no server logs. For your eyes only. 🕵️",
            "visible_message": "DELETE ME",
            "all_sides": True
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
                visible_msg = example.get('visible_message', None)

                # Get all_sides parameter from example (defaults to False)
                all_sides = example.get('all_sides', False)

                # Get theme colors for colorized QR code
                theme_colors = THEME_COLORS.get(example['theme'], THEME_COLORS['general'])

                qr_img = generate_qr_code(
                    greeting_url,
                    theme=example['theme'],
                    visible_message=visible_msg,
                    all_sides=all_sides,
                    module_color=theme_colors['module'],
                    position_ring_color=theme_colors['ring']
                )
                display_qr_with_protection(qr_img, caption="QR Code", width=None)
