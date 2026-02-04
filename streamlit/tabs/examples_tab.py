"""
Examples Tab
Displays example greeting configurations and their QR codes
"""

import streamlit as st
from greeting_formats import create_holiday_greeting, encode_greeting_to_url
from qr.generator import generate_qr_code
from qr.display import display_qr_with_protection
from config import THEME_COLORS
from i18n import get_text as _


def render() -> None:
    """Tab showing example greetings"""
    st.markdown(f'<div class="main-header"><h1>{_("examples_tab.header")}</h1></div>',
                unsafe_allow_html=True)

    st.write(_("examples_tab.intro"))

    examples = [
        {
            "title": _("examples_tab.christmas.title"),
            "from": _("examples_tab.christmas.from"),
            "to": _("examples_tab.christmas.to"),
            "theme": "snowflake",
            "message": _("examples_tab.christmas.message")
        },
        {
            "title": _("examples_tab.newyear.title"),
            "from": _("examples_tab.newyear.from"),
            "to": _("examples_tab.newyear.to"),
            "theme": "fireworks",
            "message": _("examples_tab.newyear.message")
        },
        {
            "title": _("examples_tab.wedding.title"),
            "from": _("examples_tab.wedding.from"),
            "to": _("examples_tab.wedding.to"),
            "theme": "champagne",
            "message": _("examples_tab.wedding.message")
        },
        {
            "title": _("examples_tab.farewell.title"),
            "from": _("examples_tab.farewell.from"),
            "to": _("examples_tab.farewell.to"),
            "theme": "farewell",
            "message": _("examples_tab.farewell.message"),
            "visible_message": _("examples_tab.farewell.visible_message")
        },
        {
            "title": _("examples_tab.valentine.title"),
            "from": _("examples_tab.valentine.from"),
            "to": _("examples_tab.valentine.to"),
            "theme": "valentine",
            "message": _("examples_tab.valentine.message"),
            "visible_message": _("examples_tab.valentine.visible_message")
        },
        {
            "title": _("examples_tab.marketing.title"),
            "from": _("examples_tab.marketing.from"),
            "to": _("examples_tab.marketing.to"),
            "theme": "lights",
            "message": _("examples_tab.marketing.message"),
            "visible_message": _("examples_tab.marketing.visible_message"),
            "background": "https://youtu.be/dQw4w9WgXcQ"
        },
        {
            "title": _("examples_tab.mission.title"),
            "from": _("examples_tab.mission.from"),
            "to": _("examples_tab.mission.to"),
            "theme": "burn_after_read",
            "message": _("examples_tab.mission.message"),
            "visible_message": _("examples_tab.mission.visible_message"),
            "all_sides": True
        }
    ]

    for example in examples:
        with st.expander(example["title"]):
            col1, col2 = st.columns([1, 1])

            with col1:
                st.write(f"**{_('common.labels.from')}:** {example['from']}")
                st.write(f"**{_('common.labels.to')}:** {example['to']}")
                st.write(f"**{_('create_tab.step1.title').replace('### ', '').replace('Step 1: Choose Your ', '').replace('步骤 1：选择您的', '')}:** {example['theme']}")
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
                display_qr_with_protection(qr_img, caption=_("display.qr_preview"), width=None)
