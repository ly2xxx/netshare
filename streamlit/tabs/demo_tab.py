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
    OCCASION_PRESETS,
    ANIMATION_PRESETS
)
from config import THEME_COLORS, THEME_ICONS

# ============================================================================
# State Management
# ============================================================================

def init_demo_state():
    """Initialize session state for demo tab"""
    if "demo_greeting" not in st.session_state:
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

def display_greeting_preview(greeting: DemoGreeting):
    """Display sample greeting in a nice card"""
    
    # Theme emoji
    theme_emoji = THEME_ICONS.get(greeting.theme, "🎁")
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="font-size: 2em;">{theme_emoji}</span>
            <span style="
                background: rgba(255,255,255,0.2);
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
            ">{greeting.occasion}</span>
        </div>
        <div style="
            background: rgba(255,255,255,0.95);
            color: #333;
            padding: 20px;
            border-radius: 10px;
        ">
            <p style="margin: 5px 0; font-size: 1.1em;"><strong>From:</strong> {greeting.from_name}</p>
            <p style="margin: 5px 0 15px 0; font-size: 1.1em;"><strong>To:</strong> {greeting.to_name}</p>
            <p style="
                font-style: italic;
                color: #555;
                border-left: 3px solid #667eea;
                padding-left: 15px;
                margin: 15px 0 0 0;
            ">"{greeting.message}"</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_theme_selector(current_theme: str, key_prefix: str = "main") -> str:
    """Display theme selector with visual icons
    
    Args:
        current_theme: Currently selected theme
        key_prefix: Unique prefix for button keys to avoid duplicates
    """
    
    themes = list(THEME_ICONS.keys())
    # Filter out None/general for cleaner display
    themes = [t for t in themes if t != "general" and THEME_ICONS.get(t)]
    
    cols = st.columns(min(8, len(themes)))
    
    selected_theme = current_theme
    for idx, theme in enumerate(themes):
        with cols[idx % len(cols)]:
            emoji = THEME_ICONS.get(theme, "🎁")
            is_selected = theme == current_theme
            btn_type = "primary" if is_selected else "secondary"
            if st.button(
                f"{emoji}",
                key=f"{key_prefix}_theme_{theme}",
                help=theme.title(),
                use_container_width=True
            ):
                selected_theme = theme
    
    return selected_theme


def display_customization_panel(greeting: DemoGreeting) -> Dict:
    """Display expandable customization panel"""
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        from_name = st.text_input(
            "From (Your Name)",
            value=greeting.from_name,
            key="demo_from_name"
        )
        
        to_name = st.text_input(
            "To (Recipient Name)",
            value=greeting.to_name,
            key="demo_to_name"
        )
    
    with col2:
        # Find current occasion index
        occasion_index = 0
        if greeting.occasion in OCCASION_PRESETS:
            occasion_index = OCCASION_PRESETS.index(greeting.occasion)
        
        occasion = st.selectbox(
            "Occasion",
            options=OCCASION_PRESETS,
            index=occasion_index,
            key="demo_occasion"
        )
        
        custom_occasion = st.text_input(
            "Or enter custom occasion",
            value="",
            key="demo_custom_occasion"
        )
        
        # Use custom if provided, otherwise use selected
        final_occasion = custom_occasion if custom_occasion else occasion
    
    # Message customization
    st.markdown("**Message** *(max 500 characters)*")
    message = st.text_area(
        "Your greeting message",
        value=greeting.message,
        height=100,
        max_chars=500,
        key="demo_message",
        label_visibility="collapsed"
    )
    
    char_count = len(message)
    char_color = "#28a745" if char_count < 300 else ("#ffc107" if char_count < 400 else "#dc3545")
    st.markdown(f"<p style='text-align:right; color:{char_color}; margin-top:-10px;'>{char_count}/500</p>", unsafe_allow_html=True)
    
    # Theme selection
    st.markdown("**Select Theme**")
    theme = display_theme_selector(greeting.theme, key_prefix="custom")
    
    # Update theme in session state if changed
    if theme != greeting.theme:
        st.session_state.demo_greeting.theme = theme
    
    # Return customized data
    return {
        "from_name": from_name,
        "to_name": to_name,
        "occasion": final_occasion,
        "message": message,
        "theme": theme,
        "animation": ANIMATION_PRESETS.get(theme, ["MaterializeIn"])[0]
    }


def display_qr_with_mobile_mockup(qr_image: Image.Image, greeting: DemoGreeting):
    """Display QR code with mobile frame mockup showing scan result"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📱 Your QR Code")
        st.image(qr_image, use_container_width=True, caption="Scan to see the greeting")
        
        # Action buttons
        button_col1, button_col2, button_col3 = st.columns(3)
        
        with button_col1:
            # Download button
            img_byte_arr = io.BytesIO()
            qr_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            st.download_button(
                label="⬇️ Download",
                data=img_byte_arr.getvalue(),
                file_name=f"demo_{greeting.from_name}_{greeting.to_name}_greeting.png",
                mime="image/png",
                key="demo_download_qr"
            )
        
        with button_col2:
            if st.button("📤 Share", key="demo_share"):
                st.info("Share functionality coming soon!")
        
        with button_col3:
            if st.button("🔄 Reset", key="demo_new"):
                st.session_state.demo_greeting = get_seasonal_demo()
                st.session_state.demo_qr_generated = False
                st.session_state.demo_customize_expanded = False
                st.rerun()
    
    with col2:
        st.markdown("### 👀 Preview When Scanned")
        
        # Mobile frame mockup with gradient
        theme_emoji = THEME_ICONS.get(greeting.theme, "🎁")
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 25px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        ">
            <div style="
                background: white;
                color: #333;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 15px;
            ">
                <span style="font-size: 2.5em;">{theme_emoji}</span>
                <h3 style="margin: 10px 0 0 0; color: #667eea;">Special Greeting</h3>
            </div>
            
            <div style="
                background: white;
                color: #333;
                padding: 20px;
                border-radius: 12px;
                text-align: left;
            ">
                <p style="margin: 5px 0;"><strong>From:</strong> {greeting.from_name}</p>
                <p style="margin: 5px 0;"><strong>To:</strong> {greeting.to_name}</p>
                <p style="margin: 15px 0 5px 0; font-style: italic; color: #555;">
                    "{greeting.message}"
                </p>
                <hr style="margin: 15px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 0.85em; color: #888; margin: 0;">
                    {greeting.theme.title()} Theme • {datetime.now().strftime('%b %d, %Y')}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Main Render Function
# ============================================================================

def render():
    """Main demo tab render function"""
    
    # Initialize state
    init_demo_state()
    
    # ========== HEADER ==========
    st.markdown("""
    <div style="
        text-align: center;
        margin-bottom: 30px;
        padding: 30px 20px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    ">
        <h1 style="margin: 0; font-size: 2.5em;">✨ Try the Interactive Demo ✨</h1>
        <p style="font-size: 1.2em; margin: 15px 0 0 0; opacity: 0.95;">
            Create a sample greeting in under 60 seconds
        </p>
        <div style="margin-top: 20px;">
            <span style="
                background: rgba(255,255,255,0.2);
                padding: 8px 15px;
                border-radius: 20px;
                margin: 0 5px;
                font-size: 0.9em;
            ">✅ No signup required</span>
            <span style="
                background: rgba(255,255,255,0.2);
                padding: 8px 15px;
                border-radius: 20px;
                margin: 0 5px;
                font-size: 0.9em;
            ">✅ Fully interactive</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== MAIN CONTENT ==========
    if not st.session_state.demo_qr_generated:
        # Show greeting preview and options
        demo_col1, demo_col2 = st.columns([1, 1])
        
        with demo_col1:
            st.markdown("### 📝 Sample Greeting")
            display_greeting_preview(st.session_state.demo_greeting)
            
            # Quick theme selector
            st.markdown("##### Quick Theme Change")
            new_theme = display_theme_selector(st.session_state.demo_greeting.theme, key_prefix="quick")
            if new_theme != st.session_state.demo_greeting.theme:
                st.session_state.demo_greeting = DemoGreeting(
                    from_name=st.session_state.demo_greeting.from_name,
                    to_name=st.session_state.demo_greeting.to_name,
                    occasion=st.session_state.demo_greeting.occasion,
                    message=st.session_state.demo_greeting.message,
                    theme=new_theme,
                    animation=ANIMATION_PRESETS.get(new_theme, ["MaterializeIn"])[0]
                )
                st.rerun()
        
        with demo_col2:
            st.markdown("### 🎯 Actions")
            
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 20px;
            ">
                <h4 style="margin: 0 0 10px 0; color: #00838f;">🚀 Quick Start</h4>
                <p style="color: #006064; margin: 0;">
                    Click "Generate QR Code" to see your greeting come to life!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate button (primary CTA)
            if st.button(
                "✨ Generate QR Code",
                key="generate_btn",
                use_container_width=True,
                type="primary"
            ):
                st.session_state.demo_qr_generated = True
                st.rerun()
            
            st.markdown("")
            
            # Customization toggle
            with st.expander("✏️ Customize This Demo", expanded=st.session_state.demo_customize_expanded):
                custom_data = display_customization_panel(st.session_state.demo_greeting)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Apply Changes", use_container_width=True, type="primary"):
                        st.session_state.demo_greeting = DemoGreeting(
                            from_name=custom_data["from_name"],
                            to_name=custom_data["to_name"],
                            occasion=custom_data["occasion"],
                            message=custom_data["message"],
                            theme=custom_data["theme"],
                            animation=custom_data["animation"]
                        )
                        st.rerun()
                with col2:
                    if st.button("🔄 Reset Default", use_container_width=True):
                        st.session_state.demo_greeting = get_seasonal_demo()
                        st.rerun()
    
    else:
        # ========== QR CODE GENERATED VIEW ==========
        # Generate QR code
        qr_image = generate_demo_qr_code(st.session_state.demo_greeting)
        
        # Display QR with mockup
        display_qr_with_mobile_mockup(qr_image, st.session_state.demo_greeting)
        
        # ========== CONVERSION CTA ==========
        st.markdown("---")
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            color: white;
            margin: 20px 0;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        ">
            <h2 style="margin: 0 0 15px 0;">🎉 Love what you created?</h2>
            <p style="font-size: 1.1em; opacity: 0.9; margin-bottom: 20px;">
                Now make your own personalized greeting with all the features!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🎁 Create My Own Greeting",
                key="convert_btn",
                use_container_width=True,
                type="primary"
            ):
                # Reset demo state and signal to go to create tab
                st.session_state["from_demo"] = True
                st.info("👆 Click the **Create Greeting** tab above to start creating your own personalized greeting!")
        
        # Back to edit option
        st.markdown("")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("← Edit This Demo", key="back_to_edit", use_container_width=True):
                st.session_state.demo_qr_generated = False
                st.rerun()
    
    # ========== FOOTER ==========
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9em; padding: 20px 0;">
        <p style="margin: 5px 0;">
            💡 <strong>Pro Tip:</strong> Messages work best under 300 characters for optimal QR code size
        </p>
        <p style="margin: 5px 0;">
            Questions? Check out the <strong>About</strong> tab for more info
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# If running as main module (for testing)
# ============================================================================

if __name__ == "__main__":
    render()
