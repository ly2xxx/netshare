"""
Marketing Funnel Tab
Create QR codes that convert video viewers to customers

This tab can be used:
1. Standalone - user enters all data manually
2. Pre-filled - data comes from NetPull via URL parameters
"""

import streamlit as st
import urllib.parse
from datetime import datetime
from typing import Optional, Dict
import io

from i18n import get_text as _
from config import THEME_COLORS, THEME_ICONS
from qr.generator import generate_qr_code
from qr.display import display_qr_with_protection
from utils.video_utils import validate_video_url, convert_to_embed_url
from utils.download_tracker import log_download


def load_funnel_params_from_url():
    """
    Load pre-filled data from URL parameters (from NetPull redirect).
    
    Expected parameters:
    - landing_url: CTA destination
    - video_url: Video to play
    - headline: Suggested headline
    - offer_text: Suggested offer description
    - og_image: Preview image
    - source: Where the data came from (e.g., 'netpull')
    """
    try:
        params = st.query_params
        
        # Check if we have NetPull data
        if 'landing_url' in params and 'source' not in st.session_state.get('funnel_loaded', {}):
            st.session_state.funnel_loaded = {'source': params.get('source', 'direct')}
            
            # Load all available params
            if 'landing_url' in params:
                st.session_state.funnel_landing_url = params['landing_url']
            if 'video_url' in params:
                st.session_state.funnel_video_url = params['video_url']
            if 'headline' in params:
                st.session_state.funnel_headline = params['headline']
            if 'offer_text' in params:
                st.session_state.funnel_offer_text = params['offer_text']
            if 'og_image' in params:
                st.session_state.funnel_og_image = params['og_image']
            
            # Show success banner
            st.session_state.funnel_show_prefill_banner = True
            
    except Exception as e:
        pass  # Silently handle param errors


def encode_funnel_to_url(funnel_data: Dict) -> str:
    """
    Encode funnel data to URL parameters for QR code.
    
    Uses compact parameter names to minimize QR code complexity.
    """
    base_url = "https://qr-greeting.streamlit.app/"
    
    params = {
        "tab": "view",
        "t": "funnel",  # type
        "f": funnel_data.get("brand", ""),  # from/brand
        "th": funnel_data.get("theme", "fireworks"),  # theme
        "bg": funnel_data.get("video_url", ""),  # background video
        "m": funnel_data.get("offer_text", ""),  # message/offer
        "fh": funnel_data.get("headline", ""),  # funnel headline
        "fc": funnel_data.get("cta_text", ""),  # funnel CTA text
        "fu": funnel_data.get("landing_url", ""),  # funnel CTA URL
        "fp": funnel_data.get("promo_code", ""),  # funnel promo
        "fg": funnel_data.get("urgency", ""),  # funnel urgency
    }
    
    # Remove empty params to save space
    params = {k: v for k, v in params.items() if v}
    
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def render() -> None:
    """Marketing Funnel tab main render function"""
    
    # Load URL parameters if present (from NetPull)
    load_funnel_params_from_url()
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 20px; color: white; 
                text-align: center; margin-bottom: 30px;">
        <h1>📈 Marketing Funnel QR</h1>
        <p style="font-size: 1.2em; opacity: 0.9;">
            Transform video content into high-converting QR experiences
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show pre-fill banner if data came from NetPull
    if st.session_state.get('funnel_show_prefill_banner', False):
        st.success("✅ **Data loaded from NetPull!** Review and customize below.")
        st.session_state.funnel_show_prefill_banner = False
    
    # Value proposition
    st.info("""
    **💡 The Attention Economy Problem:**  
    People watch your videos but never visit your website.
    
    **✨ The Solution:**  
    Create QR codes that play your video AND show your offer.
    
    **💪 Pro Tip:** Use [NetPull](https://net-test.streamlit.app) to auto-extract page data first!
    """)
    
    st.markdown("---")
    
    # ==========================================================================
    # Step 1: Video & Landing Page
    # ==========================================================================
    st.markdown("### 📹 Step 1: Your Content")
    
    col1, col2 = st.columns(2)
    
    with col1:
        video_url = st.text_input(
            "🎬 Video URL",
            value=st.session_state.get('funnel_video_url', ''),
            placeholder="https://youtube.com/watch?v=... or https://youtu.be/...",
            help="YouTube, Vimeo, or direct video URL (.mp4)",
            key="funnel_video_input"
        )
        
        # Validate and show preview
        if video_url:
            is_valid, video_type, error_msg = validate_video_url(video_url)
            if is_valid:
                st.success(f"✅ Valid {video_type} video")
            else:
                st.error(f"❌ {error_msg}")
    
    with col2:
        landing_url = st.text_input(
            "🔗 Landing Page URL",
            value=st.session_state.get('funnel_landing_url', ''),
            placeholder="https://yoursite.com/offer",
            help="Where users go after seeing your video + offer",
            key="funnel_landing_input"
        )
        
        if landing_url:
            if landing_url.startswith(("http://", "https://")):
                st.success("✅ Valid URL")
            else:
                st.warning("⚠️ URL should start with https://")
    
    st.markdown("---")
    
    # ==========================================================================
    # Step 2: Your Offer
    # ==========================================================================
    st.markdown("### 🎁 Step 2: Your Offer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        headline = st.text_input(
            "📢 Headline",
            value=st.session_state.get('funnel_headline', '🎁 EXCLUSIVE OFFER'),
            placeholder="e.g., 🎁 EXCLUSIVE OFFER, 🔥 LIMITED TIME",
            help="Attention-grabbing headline (use emojis!)",
            key="funnel_headline_input"
        )
        
        offer_text = st.text_area(
            "💬 Offer Description",
            value=st.session_state.get('funnel_offer_text', 
                "Get 20% OFF your first order!\n\nWatch the video to see why customers love us."),
            height=100,
            placeholder="Describe your value proposition...",
            help="What's in it for them? Keep it concise.",
            key="funnel_offer_input"
        )
    
    with col2:
        cta_text = st.text_input(
            "🖱️ Call-to-Action Button",
            value="Shop Now →",
            placeholder="e.g., Shop Now, Learn More, Get Started",
            help="Action text for the button",
            key="funnel_cta_input"
        )
        
        promo_code = st.text_input(
            "🏷️ Promo Code (optional)",
            placeholder="e.g., SAVE20, WELCOME10",
            help="Discount code to display",
            key="funnel_promo_input"
        )
        
        urgency_text = st.text_input(
            "⏰ Urgency Text (optional)",
            placeholder="e.g., Offer expires in 48 hours",
            help="Create FOMO - scarcity drives action",
            key="funnel_urgency_input"
        )
    
    st.markdown("---")
    
    # ==========================================================================
    # Step 3: Branding & Theme
    # ==========================================================================
    st.markdown("### 🎨 Step 3: Branding")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        brand_name = st.text_input(
            "🏢 Brand Name",
            placeholder="Your Company Name",
            help="Shown as 'from' attribution",
            key="funnel_brand_input"
        )
    
    with col2:
        theme_options = {
            "fireworks": "🎆 Fireworks (Excitement)",
            "lights": "✨ Lights (Premium)",
            "confetti": "🎉 Confetti (Celebration)",
            "stars": "⭐ Stars (Aspirational)",
            "champagne": "🥂 Champagne (Luxury)",
        }
        
        selected_theme_label = st.selectbox(
            "🎨 Visual Theme",
            options=list(theme_options.values()),
            index=0,
            help="Sets the mood for your funnel",
            key="funnel_theme_select"
        )
        
        selected_theme = [k for k, v in theme_options.items() 
                         if v == selected_theme_label][0]
    
    with col3:
        visible_message = st.text_input(
            "📝 QR Label (optional)",
            placeholder="e.g., SCAN FOR 20% OFF",
            help="Text printed around the QR code",
            key="funnel_visible_msg_input"
        )
    
    st.markdown("---")
    
    # ==========================================================================
    # Step 4: Generate
    # ==========================================================================
    st.markdown("### 🚀 Step 4: Generate Your Funnel QR")
    
    # Validation
    can_generate = all([landing_url, headline, offer_text, cta_text])
    
    if not can_generate:
        missing = []
        if not landing_url: missing.append("Landing Page URL")
        if not headline: missing.append("Headline")
        if not offer_text: missing.append("Offer Description")
        if not cta_text: missing.append("CTA Button Text")
        st.warning(f"⚠️ Please fill in: {', '.join(missing)}")
    
    if not video_url:
        st.info("💡 **Tip:** Adding a video increases engagement significantly!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            "🚀 Generate Marketing Funnel QR",
            type="primary",
            disabled=not can_generate,
            use_container_width=True,
            key="funnel_generate_btn"
        )
    
    if generate_btn and can_generate:
        # Create funnel data
        funnel_data = {
            "video_url": video_url,
            "landing_url": landing_url,
            "headline": headline,
            "offer_text": offer_text,
            "cta_text": cta_text,
            "promo_code": promo_code,
            "urgency": urgency_text,
            "brand": brand_name,
            "theme": selected_theme
        }
        
        # Encode to URL
        funnel_url = encode_funnel_to_url(funnel_data)
        
        st.success("✅ Marketing Funnel QR Generated!")
        
        # Display results
        result_col1, result_col2 = st.columns([1, 1])
        
        with result_col1:
            st.markdown("#### 📱 Your Funnel QR Code")
            
            # Get theme colors
            theme_colors = THEME_COLORS.get(selected_theme, THEME_COLORS["fireworks"])
            
            # Generate QR
            qr_img = generate_qr_code(
                funnel_url,
                theme=selected_theme,
                visible_message=visible_message if visible_message else None,
                module_color=theme_colors["module"],
                position_ring_color=theme_colors["ring"]
            )
            
            display_qr_with_protection(qr_img, caption="Scan to preview your funnel")
            
            # Download button
            buf = io.BytesIO()
            qr_img.save(buf, format='PNG')
            filename = f"funnel_qr_{brand_name or 'marketing'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            st.download_button(
                label="⬇️ Download QR Code",
                data=buf.getvalue(),
                file_name=filename,
                mime="image/png",
                use_container_width=True,
                on_click=log_download,
                args=(filename,)
            )
        
        with result_col2:
            st.markdown("#### 👀 Preview: What Users See")
            
            # Mockup of the funnel experience
            st.markdown(f"""
            <div style="border: 3px solid #333; border-radius: 20px; padding: 15px; 
                        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
                        color: white; max-width: 350px; margin: 0 auto;">
                <div style="background: #000; border-radius: 10px; height: 150px; 
                            display: flex; align-items: center; justify-content: center;
                            margin-bottom: 15px; position: relative;">
                    <span style="font-size: 3em;">🎬</span>
                    <div style="position: absolute; bottom: 5px; right: 10px; 
                                background: rgba(255,255,255,0.2); padding: 2px 8px; 
                                border-radius: 3px; font-size: 0.8em;">
                        {"Video Playing..." if video_url else "No video"}
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.95); color: #333; 
                            padding: 20px; border-radius: 15px; text-align: center;">
                    <div style="font-size: 1.3em; font-weight: bold; margin-bottom: 10px;">
                        {headline}
                    </div>
                    <div style="font-size: 0.95em; margin-bottom: 15px; line-height: 1.4;">
                        {offer_text[:100]}{'...' if len(offer_text) > 100 else ''}
                    </div>
                    {"<div style='background: #ffd700; color: #333; padding: 5px 15px; border-radius: 5px; font-weight: bold; margin-bottom: 10px; display: inline-block;'>🏷️ " + promo_code + "</div>" if promo_code else ""}
                    {"<div style='color: #e74c3c; font-size: 0.85em; margin-bottom: 10px;'>⏰ " + urgency_text + "</div>" if urgency_text else ""}
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                color: white; padding: 12px 25px; border-radius: 25px; 
                                font-weight: bold; cursor: pointer; display: inline-block;">
                        {cta_text}
                    </div>
                </div>
                <div style="text-align: center; margin-top: 10px; font-size: 0.8em; opacity: 0.7;">
                    {f"from {brand_name}" if brand_name else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Usage tips
        with st.expander("📋 How to Use Your Funnel QR", expanded=True):
            st.markdown(f"""
            **Print it on:**
            - 📦 Product packaging
            - 📄 Flyers and brochures  
            - 🪧 Posters and banners
            - 💳 Business cards
            - 🧾 Receipts and invoices
            - 📱 Social media posts
            
            **Pro Tips:**
            1. **Test it first** - Scan with your phone to verify the experience
            2. **Track conversions** - Use UTM parameters in your landing URL
            3. **A/B test** - Try different headlines and CTAs
            4. **Update regularly** - Change offers to keep it fresh
            
            **Your Funnel URL:**
            ```
            {funnel_url}
            ```
            """)
