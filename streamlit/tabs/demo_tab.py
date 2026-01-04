"""
Interactive Demo Tab
Allows users to create a sample greeting in <60 seconds without friction
"""

import streamlit as st
from datetime import datetime
import json
from typing import Dict
import qrcode
from PIL import Image
import io

# Import utilities
from utils.demo_data import (
    DemoGreeting,
    get_seasonal_demo,
    ANIMATION_PRESETS
)
from config import THEME_COLORS, THEME_ICONS
from i18n import get_text as _

# ============================================================================
# State Management
# ============================================================================

def init_demo_state():
    """Initialize session state for demo tab"""
    if "demo_greeting" not in st.session_state:
        st.session_state.demo_greeting = get_seasonal_demo()
    else:
        # Validate and fix corrupted message field (should be plain text, not HTML)
        greeting = st.session_state.demo_greeting
        if "<" in greeting.message and ">" in greeting.message:
            # Message contains HTML tags - reset to default
            st.session_state.demo_greeting = get_seasonal_demo()

    if "demo_qr_generated" not in st.session_state:
        st.session_state.demo_qr_generated = False
    if "demo_customize_expanded" not in st.session_state:
        st.session_state.demo_customize_expanded = False
    if "demo_qr_image" not in st.session_state:
        st.session_state.demo_qr_image = None

# ============================================================================
# QR Code Generation
# ============================================================================

def generate_demo_qr_code(greeting: DemoGreeting) -> Image.Image:
    """Generate QR code image for demo greeting"""
    
    # Encode greeting data
    greeting_json = json.dumps(greeting.to_dict())
    
    # Create QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(greeting_json)
    qr.make(fit=True)
    
    # Get theme colors
    theme_colors = THEME_COLORS.get(greeting.theme, THEME_COLORS["general"])
    
    # Generate image
    img = qr.make_image(
        fill_color=theme_colors["module"],
        back_color="white"
    )
    
    return img.convert('RGB')

# ============================================================================
# UI Components
# ============================================================================

def get_step_container_style(step_num: int, is_active: bool) -> str:
    """Get CSS style for step containers"""
    
    border_color = "#667eea" if is_active else "#e0e0e0"
    bg_color = "#ffffff" if is_active else "#f9f9f9"
    opacity = "1.0" if is_active else "0.7"
    
    return f"""
    <div style="
        border: 2px solid {border_color};
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: {bg_color};
        opacity: {opacity};
        transition: all 0.3s ease;
    ">
        <div style="
            display: inline-block;
            background: {border_color};
            color: white;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            margin-right: 10px;
        ">{step_num}</div>
        <span style="font-size: 1.2em; font-weight: bold; color: #333;">
    """

def display_greeting_card_preview(greeting: DemoGreeting):
    """Display the greeting card preview"""
    
    theme_emoji = THEME_ICONS.get(greeting.theme, "🎁")
    
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; color: white; box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4); max-width: 600px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 3em; margin-bottom: 10px;">{theme_emoji}</div>
    </div>
    <div style="background: rgba(255,255,255,0.95); color: #333; padding: 25px; border-radius: 15px; position: relative;">
        <p style="margin: 5px 0 0 0; font-weight: 600; font-size: 1.1em;">{_('common.labels.from')}: {greeting.from_name}</p>
        <p style="margin: 5px 0 20px 0; font-weight: 600; font-size: 1.1em;">{_('common.labels.to')}: {greeting.to_name}</p>
        <p style="font-family: Georgia, serif; font-size: 1.15em; line-height: 1.6; color: #444; font-style: italic; margin: 0;">"{greeting.message}"</p>
    </div>
</div>
""", unsafe_allow_html=True)

def display_theme_buttons(current_theme: str):
    """Display theme selection buttons"""
    
    themes = list(THEME_ICONS.keys())
    themes = [t for t in themes if t != "general" and THEME_ICONS.get(t)]
    
    cols = st.columns(8)
    
    for idx, theme in enumerate(themes):
        with cols[idx % 8]:
            emoji = THEME_ICONS.get(theme, "🎁")
            is_selected = theme == current_theme
            
            # Use columns to center buttons if needed
            if st.button(
                f"{emoji}",
                key=f"step1_theme_{theme}",
                help=_("demo_tab.theme_selection_help", theme=theme.title()),
                width='stretch',
                type="primary" if is_selected else "secondary"
            ):
                return theme
                
    return current_theme

def render_step_1_theme():
    """Render Step 1: Choose Theme"""
    
    greeting = st.session_state.demo_greeting
    
    st.markdown(_("demo_tab.step1.title"))
    st.info(_("demo_tab.step1.tip"))
    
    new_theme = display_theme_buttons(greeting.theme)
    if new_theme != greeting.theme:
        st.session_state.demo_greeting.theme = new_theme
        st.session_state.demo_greeting.animation = ANIMATION_PRESETS.get(new_theme, ["MaterializeIn"])[0]
        st.rerun()

def render_step_2_preview():
    """Render Step 2: Preview & Personalize"""
    
    greeting = st.session_state.demo_greeting
    
    st.markdown(_("demo_tab.step2.title"))
    st.info(_("demo_tab.step2.tip"))
    
    # Preview
    display_greeting_card_preview(greeting)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Inline customization using expander
    with st.expander(_("demo_tab.edit.title"), expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_from = st.text_input(_("common.labels.from"), value=greeting.from_name, key="step2_from")
        with col2:
            new_to = st.text_input(_("common.labels.to"), value=greeting.to_name, key="step2_to")

        new_message = st.text_area(_("common.labels.message"), value=greeting.message, height=100, key="step2_msg")

        # Apply changes button
        if st.button(_("common.buttons.update_preview"), type="secondary", width='stretch'):
            # Validate message doesn't contain HTML (strip tags if found)
            if "<" in new_message and ">" in new_message:
                import re
                cleaned_message = re.sub(r'<[^>]+>', '', new_message)
                st.warning(_("demo_tab.warning.html_removed"))
                new_message = cleaned_message

            st.session_state.demo_greeting.from_name = new_from
            st.session_state.demo_greeting.to_name = new_to
            st.session_state.demo_greeting.message = new_message
            st.rerun()

def render_step_3_generate():
    """Render Step 3: Generate Action"""
    
    st.markdown(_("demo_tab.step3.title"))
    st.info(_("demo_tab.step3.tip"))
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            _("demo_tab.generate_button"),
            type="primary",
            width='stretch',
            key="step3_generate_btn"
        ):
            st.session_state.demo_qr_generated = True
            st.rerun()

def render_step_4_result():
    """Render Step 4: The Result"""

    greeting = st.session_state.demo_greeting

    st.success(_("demo_tab.success"))
    st.info(_("demo_tab.demo_mode_info"), icon="ℹ️")

    # Privacy benefits highlight
    st.info(_("demo_tab.privacy_info"), icon="🔒")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(_("demo_tab.qr_section"))
        # Generate QR
        qr_img = generate_demo_qr_code(greeting)
        st.image(qr_img, width='stretch', caption=_("demo_tab.scan_me"))
        
        # Download (disabled for demo)
        img_byte_arr = io.BytesIO()
        qr_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        st.download_button(
            _("demo_tab.download_button"),
            data=img_byte_arr.getvalue(),
            file_name="my_greeting_qr.png",
            mime="image/png",
            width='stretch',
            disabled=True,
            help=_("demo_tab.download_disabled")
        )

        st.caption(_("demo_tab.preview_only"))

    with col2:
        st.markdown(_("demo_tab.preview_section"))
        # Mobile frame mockup simplified
        theme_emoji = THEME_ICONS.get(greeting.theme, "🎁")
        st.markdown(f"""
<div style="border: 8px solid #333; border-radius: 30px; padding: 15px; background: white; max-width: 300px; margin: 0 auto; position: relative;">
    <div style="background: #f0f0f0; border-radius: 20px; padding: 15px; text-align: center; min-height: 350px;">
        <div style="font-size: 2.5em; margin-top: 20px;">{theme_emoji}</div>
        <h4 style="margin: 10px 0; color: #667eea;">{_('demo_tab.preview_title')}</h4>
        <p style="font-size: 0.9em; color: #555;">"{greeting.message[:80]}..."</p>
        <div style="margin-top: 20px; font-size: 0.8em; color: #888;">{_('demo_tab.preview_hint')}</div>
    </div>
</div>
""", unsafe_allow_html=True)
        
    st.markdown("---")

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3>{_('demo_tab.ready_prompt')}</h3>
        <p>{_('demo_tab.ready_description')}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Use markdown styled as button to navigate like the hyperlinks do
        st.markdown(f"""
        <a href="?tab=create" style="
            display: inline-block;
            width: 100%;
            padding: 0.5rem 1rem;
            background-color: #ff4b4b;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 1rem;
            border: 1px solid transparent;
            transition: all 0.2s;
        " onmouseover="this.style.backgroundColor='#ff2b2b'" onmouseout="this.style.backgroundColor='#ff4b4b'">
            {_('demo_tab.create_my_own')}
        </a>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(_("demo_tab.start_over"), type="secondary", width='stretch'):
            st.session_state.demo_qr_generated = False
            st.session_state.demo_greeting = get_seasonal_demo()
            st.rerun()

# ============================================================================
# Main Render Function
# ============================================================================

def render():
    """Main demo tab render function"""
    
    # Initialize state
    init_demo_state()
    
    # Header with demo notice
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>{_('demo_tab.header')}</h1>
        <p style="color: #666;">{_('demo_tab.subtitle')}</p>
        <div style="background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%); color: white; padding: 12px 20px; border-radius: 10px; margin: 15px auto; max-width: 600px; font-weight: 500;">
            {_('demo_tab.info').replace('[**', '<strong><a href="?tab=create" style="color: white; text-decoration: underline;">').replace('**](?tab=create)', '</a></strong>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render steps
    if not st.session_state.demo_qr_generated:
        # Step 1
        with st.container():
            render_step_1_theme()
            st.divider()
            
        # Step 2
        with st.container():
            render_step_2_preview()
            st.divider()
            
        # Step 3
        with st.container():
            render_step_3_generate()
            
    else:
        # Result View
        render_step_4_result()


# ============================================================================
# If running as main module (for testing)
# ============================================================================

if __name__ == "__main__":
    render()
