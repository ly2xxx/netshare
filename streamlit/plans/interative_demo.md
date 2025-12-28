# Interactive Demo Feature - Detailed Implementation Plan

**Project**: Holiday Greeting QR Code Generator  
**Feature**: Interactive Demo Tab  
**Purpose**: Low-friction entry point for new users to experience the product in <60 seconds  
**Target Conversion**: Convert 15-20% of demo users to full greeting creation  
**Created**: December 27, 2025

---

## Table of Contents
1. [Feature Overview](#feature-overview)
2. [User Experience Design](#user-experience-design)
3. [Technical Architecture](#technical-architecture)
4. [Implementation Guide](#implementation-guide)
5. [Code Specifications](#code-specifications)
6. [Integration Points](#integration-points)
7. [Success Metrics](#success-metrics)
8. [Future Enhancements](#future-enhancements)

---

## Feature Overview

### What is the Interactive Demo?

The Interactive Demo is a lightweight, low-friction feature that allows first-time users to create a sample QR code greeting in under 60 seconds without any form friction or required fields. It serves as:

- **Product Discovery**: Show what's possible in the app
- **Conversion Funnel**: Gateway to full greeting creation
- **Social Proof Generator**: Create shareable examples
- **User Onboarding**: Guide new users through the workflow

### Key Principles

1. **Speed**: Generate a greeting in <10 clicks
2. **Simplicity**: Minimal cognitive load (no confusing options)
3. **Beauty**: Impressive visual output to motivate deeper exploration
4. **Engagement**: Interactive elements that feel fun, not robotic
5. **Frictionless**: No signup, login, or complex decisions required
6. **Guided**: Natural progression toward full app features

### Success Definition

- Demo tab receives >30% of new user traffic
- >15% of demo users click "Create My Own Greeting"
- Average session time: 2-3 minutes
- Mobile conversion rate: >20%
- Desktop conversion rate: >25%

---

## User Experience Design

### User Flow Diagram
```
Landing (First-time User)
    ↓
See "Try Interactive Demo" CTA in header/sidebar
    ↓
Click → Enters Demo Tab
    ↓
Sees Pre-filled Sample Greeting:
  From: Sarah
  To: Mike
  Occasion: Christmas 2025
  Message: "Wishing you a magical holiday season..."
  Theme: Snowflake (shown visually)
    ↓
Three Paths Available:
    ├─→ Path A: "Generate Demo QR" (Instant generation)
    │      ↓
    │   Sees animated QR code generation
    │      ↓
    │   QR code displays beautifully
    │      ↓
    │   Shows scan result preview on mobile frame
    │      ↓
    │   [Next Steps Button: "Create My Own Greeting"]
    │
    ├─→ Path B: "Customize Demo" (Quick tweaks)
    │      ↓
    │   Edit: From Name (text field)
    │   Edit: Occasion (dropdown quick select)
    │   Edit: Theme (visual theme selector)
    │   Edit: Message (textarea)
    │      ↓
    │   Live preview updates in real-time
    │      ↓
    │   "Generate Custom Demo QR"
    │      ↓
    │   [Share or Create My Own]
    │
    └─→ Path C: "Start From Scratch" (Full creation)
         ↓
      Takes user to full "Create Greeting" tab
```

### Screen Layout (Desktop)
```
┌─────────────────────────────────────────────────────────────┐
│  Header: "✨ Try the Interactive Demo ✨"                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Left Panel (50%)          │  Right Panel (50%)              │
│  ────────────────────────  │  ────────────────────────      │
│                            │                                 │
│  Sample Greeting Preview:  │  Interactive QR Output:        │
│  ┌──────────────────────┐  │  ┌──────────────────────────┐  │
│  │ From: Sarah          │  │  │                          │  │
│  │ To: Mike             │  │  │      [QR CODE]          │  │
│  │ Occasion: Christmas  │  │  │      (animated)         │  │
│  │ Theme: ❄️ Snowflake │  │  │                          │  │
│  │                      │  │  │  Scans reveal:          │  │
│  │ Message:             │  │  │  ┌────────────────────┐ │  │
│  │ "Wishing you a       │  │  │  │ Christmas Greeting │ │  │
│  │  magical holiday..." │  │  │  │ From: Sarah To: Mike│ │  │
│  └──────────────────────┘  │  │  │ Message appears...  │ │  │
│                            │  │  └────────────────────┘ │  │
│  [Customize Demo]          │  │                          │  │
│  [Generate Demo QR] (CTA)  │  │  [Download QR]          │  │
│                            │  │  [Share to Social]      │  │
│                            │  │  [Try Full Creator]     │  │
│                            │  │                          │  │
│  Theme Quick Selector:     │  └──────────────────────────┘  │
│  ❄️ ☃️ 🎆 ✨ 🎉 🥂 ❤️ 👋  │                                 │
│                            │                                 │
└─────────────────────────────────────────────────────────────┘
```

### Screen Layout (Mobile)
```
┌──────────────────────────┐
│ Try the Demo             │
├──────────────────────────┤
│                          │
│ Sample Greeting:         │
│ ┌────────────────────┐   │
│ │ From: Sarah        │   │
│ │ To: Mike           │   │
│ │ Occasion: Xmas     │   │
│ │ Theme: ❄️ Snowflake│   │
│ │                    │   │
│ │ "Wishing you a     │   │
│ │  magical holiday..."│  │
│ └────────────────────┘   │
│                          │
│ [Customize ↓]            │
│ [Generate QR →]          │
│                          │
├──────────────────────────┤
│                          │
│  QR Code (Full Width):   │
│  ┌────────────────────┐  │
│  │                    │  │
│  │    [QR CODE]       │  │
│  │    (Animated)      │  │
│  │                    │  │
│  └────────────────────┘  │
│                          │
│ When Scanned:            │
│ ┌────────────────────┐   │
│ │ Christmas Greeting │   │
│ │ From: Sarah        │   │
│ │ To: Mike           │   │
│ │                    │   │
│ │ Message appears    │   │
│ │ with snowflake     │   │
│ │ animation...       │   │
│ └────────────────────┘   │
│                          │
│ [Download] [Share]       │
│ [Create My Own] (CTA)    │
│                          │
└──────────────────────────┘
```

### Key UI Elements

#### 1. Welcome Section
- Prominent headline: "✨ Try the Interactive Demo ✨"
- Subheading: "Create a sample greeting in under 60 seconds"
- No login/signup required badge

#### 2. Pre-filled Sample Data
```python
DEFAULT_DEMO_GREETING = {
    "from": "Sarah",
    "to": "Mike",
    "occasion": "Christmas 2025",
    "message": "Wishing you a magical holiday season filled with joy, laughter, and special moments with loved ones!",
    "theme": "snowflake",
    "animation": "FadeInCenterOut"
}
```

#### 3. Three Call-to-Action Buttons

**Button 1: "Generate Demo QR"** (Primary CTA)
- Style: Bold, prominent button
- Color: Theme-matched (e.g., snowflake blue)
- Icon: ✨ or 🎁
- Action: Generate QR immediately with default data
- Feedback: Animated confetti or smooth transition

**Button 2: "Customize Demo"** (Secondary CTA)
- Style: Secondary button style
- Opens: Expandable customization panel
- Allows: Quick edits to demo data
- Real-time preview: Updates as user types

**Button 3: "Create My Own Greeting"** (Conversion CTA)
- Style: Tertiary or text link
- Appears: After QR generation
- Action: Navigate to full "Create Greeting" tab
- Tracking: Log conversion event

#### 4. Theme Selector (Visual Carousel)
```
Theme Selection Carousel:
← [❄️ Snowflake] [☃️ Winter] [🎆 Fireworks] [✨ Lights] 
   [⭐ Stars] [🎉 Confetti] [🥂 Champagne] [❤️ Hearts] →
```

Features:
- Click to preview theme instantly
- Shows theme name on hover
- Animated appearance
- Mobile: Horizontal scroll

#### 5. QR Code Display with Mobile Frame

**Desktop View:**
- Large QR code (400x400px minimum)
- Shows surrounding smartphone frame mockup
- Displays what greeting looks like when scanned
- Animated reveal of decoded message

**Mobile View:**
- Full-width QR code
- Shows stacked mockup (what user sees on their phone)
- Tap to expand/fullscreen

### Customization Panel (Collapsed by Default)

When user clicks "Customize Demo":
```
┌─ Customize Your Demo ─────────────────────────┐
│                                                │
│ From: [Sarah                        ]           │
│ (Your name)                                     │
│                                                │
│ To: [Mike                           ]           │
│ (Recipient's name)                            │
│                                                │
│ Occasion:                                       │
│ ○ Birthday      ○ Christmas  ○ Wedding       │
│ ○ Anniversary   ○ New Year   ○ Other         │
│ Custom: [Enter occasion              ]        │
│                                                │
│ Theme:                                         │
│ [❄️] [☃️] [🎆] [✨] [🎉] [🥂] [❤️] [👋]      │
│                                                │
│ Message Preview:                               │
│ [Wishing you a magical holiday season...    ] │
│ (char count: 87/500)                          │
│                                                │
│ [Update Preview] [Reset to Default]           │
│                                                │
└────────────────────────────────────────────────┘
```

### Interaction Patterns

#### Real-Time Updates
- As user edits "From" name: Preview updates
- Theme selection: QR code color changes live
- Message edit: Character count updates
- Occasion change: Suggested themes highlight

#### Micro-interactions
- Input fields: Soft focus effect on click
- Theme buttons: Smooth scale-up on hover
- Message count: Color changes when approaching limit
- Success state: Checkmark animation when customization complete

#### Progressive Disclosure
1. User sees default greeting
2. Clicks "Customize" to reveal more options
3. Edits are hidden until explicitly requested
4. Creates feeling of simplicity with depth

---

## Technical Architecture

### Module Structure
```
streamlit/
├── app.py (main app)
├── tabs/
│   ├── __init__.py
│   ├── create_tab.py (existing)
│   ├── scan_tab.py (existing)
│   ├── examples_tab.py (existing)
│   ├── batch_tab.py (existing)
│   ├── about_tab.py (existing)
│   ├── view_page.py (existing)
│   └── demo_tab.py (NEW)
├── utils/
│   ├── __init__.py
│   ├── qr_generator.py (new utility functions)
│   └── demo_data.py (NEW)
├── config.py (existing)
└── greeting_formats.py (existing)
```

### Data Structures

#### Demo Data Module (demo_data.py)
```python
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DemoGreeting:
    """Represents a demo greeting configuration"""
    from_name: str
    to_name: str
    occasion: str
    message: str
    theme: str
    animation: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat() + "Z"
    
    def to_dict(self) -> Dict:
        return {
            "v": "1.0",
            "type": "greeting",
            "from": self.from_name,
            "to": self.to_name,
            "occasion": self.occasion,
            "message": self.message,
            "theme": self.theme,
            "animation": self.animation,
            "created": self.created_at
        }

# Default demo greeting configurations
DEFAULT_DEMO = DemoGreeting(
    from_name="Sarah",
    to_name="Mike",
    occasion="Christmas 2025",
    message="Wishing you a magical holiday season filled with joy, laughter, and special moments with loved ones!",
    theme="snowflake",
    animation="FadeInCenterOut"
)

# Alternative demo greetings (rotate based on season/date)
SEASONAL_DEMOS: Dict[str, DemoGreeting] = {
    "christmas": DemoGreeting(
        from_name="Sarah",
        to_name="Mike",
        occasion="Christmas 2025",
        message="Wishing you a magical holiday season filled with joy and laughter!",
        theme="snowflake",
        animation="FadeInCenterOut"
    ),
    "newyear": DemoGreeting(
        from_name="Alex",
        to_name="Jordan",
        occasion="New Year 2026",
        message="Here's to new beginnings, fresh starts, and amazing adventures in 2026!",
        theme="fireworks",
        animation="RadialRipple"
    ),
    "valentine": DemoGreeting(
        from_name="Emma",
        to_name="James",
        occasion="Valentine's Day",
        message="To the person who makes every day feel like a celebration. Happy Valentine's Day!",
        theme="hearts",
        animation="FadeInCenterOut"
    ),
    "wedding": DemoGreeting(
        from_name="Friends",
        to_name="The Happy Couple",
        occasion="Wedding Day",
        message="Congratulations on your special day! Wishing you a lifetime of love and happiness together.",
        theme="champagne",
        animation="RadialRipple"
    ),
    "general": DemoGreeting(
        from_name="You",
        to_name="Someone Special",
        occasion="Any Occasion",
        message="Life is what you make it. Make every moment special and share it with those you love.",
        theme="lights",
        animation="FadeInTopDown"
    )
}

def get_seasonal_demo() -> DemoGreeting:
    """
    Returns appropriate demo based on current date/season
    Falls back to general if not in special season
    """
    from datetime import datetime
    
    month = datetime.now().month
    
    if month == 12:
        return SEASONAL_DEMOS["christmas"]
    elif month == 1:
        return SEASONAL_DEMOS["newyear"]
    elif month == 2:
        return SEASONAL_DEMOS["valentine"]
    else:
        return SEASONAL_DEMOS["general"]

# Occasion presets for quick selection
OCCASION_PRESETS: List[str] = [
    "Birthday",
    "Anniversary",
    "Christmas",
    "New Year",
    "Wedding",
    "Graduation",
    "Congratulations",
    "Thank You",
    "Get Well",
    "Just Because"
]

# Animation presets
ANIMATION_PRESETS: Dict[str, List[str]] = {
    "snowflake": ["FadeInCenterOut", "FadeInTopDown"],
    "fireworks": ["RadialRipple", "MaterializeIn"],
    "lights": ["FadeInTopDown", "FadeInCenterOut"],
    "stars": ["RadialRippleIn", "MaterializeIn"],
    "confetti": ["MaterializeIn", "RadialRipple"],
    "champagne": ["RadialRipple", "FadeInCenterOut"],
    "hearts": ["FadeInCenterOut", "FadeInTopDown"],
    "farewell": ["FadeInTopDown", "FadeInCenterOut"],
}
```

#### State Management
```python
# Session state keys for demo tab
DEMO_STATE_KEYS = {
    "demo_greeting": "current_demo_greeting",
    "demo_qr_generated": "demo_qr_has_been_generated",
    "demo_customize_expanded": "demo_customize_panel_expanded",
    "demo_qr_image": "demo_qr_code_image",
    "demo_conversion_tracked": "demo_conversion_event_tracked"
}

# Initialize in demo_tab.py:
def init_demo_state():
    if DEMO_STATE_KEYS["demo_greeting"] not in st.session_state:
        st.session_state[DEMO_STATE_KEYS["demo_greeting"]] = get_seasonal_demo()
    if DEMO_STATE_KEYS["demo_qr_generated"] not in st.session_state:
        st.session_state[DEMO_STATE_KEYS["demo_qr_generated"]] = False
    if DEMO_STATE_KEYS["demo_customize_expanded"] not in st.session_state:
        st.session_state[DEMO_STATE_KEYS["demo_customize_expanded"]] = False
```

### QR Generation Integration

The demo will use existing QR generation code but with cached/optimized rendering:
```python
# In demo_tab.py - using existing greeting_formats and config

from greeting_formats import encode_greeting
from config import THEME_COLORS, THEME_ANIMATIONS
import qrcode
from PIL import Image
import streamlit as st

def generate_demo_qr(demo_greeting: DemoGreeting) -> Image.Image:
    """
    Generate QR code for demo greeting
    Uses existing greeting format encoding
    """
    # Convert to greeting JSON format
    greeting_json = encode_greeting({
        "v": "1.0",
        "type": "greeting",
        "from": demo_greeting.from_name,
        "to": demo_greeting.to_name,
        "occasion": demo_greeting.occasion,
        "message": demo_greeting.message,
        "theme": demo_greeting.theme,
        "created": demo_greeting.created_at
    })
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=None,  # Auto version
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(greeting_json)
    qr.make(fit=True)
    
    # Apply theme colors
    theme_color = THEME_COLORS.get(demo_greeting.theme, THEME_COLORS["general"])
    img = qr.make_image(
        fill_color=theme_color["module"],
        back_color="#ffffff"
    )
    
    return img

@st.cache_data(ttl=3600)
def get_cached_demo_qr(greeting_dict_str: str) -> Image.Image:
    """
    Cached QR generation for demo greetings
    Key: stringified greeting dict for cache key
    TTL: 1 hour
    """
    # Reconstruct greeting from string
    import json
    greeting_dict = json.loads(greeting_dict_str)
    demo_greeting = DemoGreeting(**greeting_dict)
    return generate_demo_qr(demo_greeting)
```

---

## Implementation Guide

### Step 1: Create demo_data.py

**File**: `streamlit/utils/demo_data.py`
```python
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DemoGreeting:
    """Represents a demo greeting configuration"""
    from_name: str
    to_name: str
    occasion: str
    message: str
    theme: str
    animation: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat() + "Z"
    
    def to_dict(self) -> Dict:
        return {
            "from": self.from_name,
            "to": self.to_name,
            "occasion": self.occasion,
            "message": self.message,
            "theme": self.theme,
            "animation": self.animation,
            "created": self.created_at
        }

# [Copy all SEASONAL_DEMOS, OCCASION_PRESETS, etc. from Code Specifications section above]
```

**Status**: Ready to implement

### Step 2: Create demo_tab.py

**File**: `streamlit/tabs/demo_tab.py`

See full implementation code in Code Specifications section below.

**Status**: See full code below

### Step 3: Update app.py

Modify `streamlit/app.py` to include demo tab:

**Location**: Import section (line ~12)
```python
from tabs import create_tab, scan_tab, examples_tab, batch_tab, about_tab, view_page, demo_tab
```

**Location**: Main tabs section (around line ~90)
```python
# Update tab creation:
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎁 Try Demo",  # NEW - First position for visibility
    "Create Greeting", 
    "Scan QR Code", 
    "Examples", 
    "About"
])

# Note: Reorder so demo is prominent - catches attention first!
with tab1:
    demo_tab.render()

with tab2:
    create_tab.render()
    
# ... etc
```

**Alternative (if not reordering)**: Add as optional tab
```python
if show_demo:  # Add checkbox in sidebar
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Create Greeting", 
        "Try Demo",  # NEW
        "Scan QR Code", 
        "Examples", 
        "Batch",
        "About"
    ])
    # ... render each
else:
    # Original tabs
```

### Step 4: Testing Checklist

- [ ] Demo loads without errors
- [ ] Default greeting displays correctly
- [ ] QR code generates on button click
- [ ] Customization panel opens/closes smoothly
- [ ] Real-time preview updates as user edits
- [ ] Theme selector changes QR colors
- [ ] Mobile layout is responsive
- [ ] Conversion button navigates to Create tab
- [ ] Download QR works correctly
- [ ] Social share buttons function
- [ ] Loading states are smooth
- [ ] Session state persists across refreshes
- [ ] Analytics events fire correctly

### Step 5: Deployment

1. Test locally: `streamlit run app.py`
2. Push to GitHub
3. Streamlit Cloud auto-deploys
4. Monitor analytics for demo usage

---

## Code Specifications

### demo_tab.py - Complete Implementation
```python
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
from greeting_formats import encode_greeting
from config import THEME_COLORS, THEME_ICONS, THEME_ANIMATIONS

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
    
    return img

@st.cache_data(ttl=3600)
def cached_qr_generation(greeting_json_str: str) -> bytes:
    """Cache QR code generation"""
    greeting_dict = json.loads(greeting_json_str)
    greeting = DemoGreeting(**greeting_dict)
    img = generate_demo_qr_code(greeting)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

# ============================================================================
# UI Components
# ============================================================================

def display_greeting_preview(greeting: DemoGreeting):
    """Display sample greeting in a nice card"""
    
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Theme emoji
            theme_emoji = THEME_ICONS.get(greeting.theme, "🎁")
            st.markdown(f"### {theme_emoji} {greeting.theme.title()}")
        
        with col2:
            # Occasion badge
            st.markdown(f"**Occasion**: {greeting.occasion}")
        
        # Greeting card preview
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 10px 0;
        ">
            <p><strong>From:</strong> {greeting.from_name}</p>
            <p><strong>To:</strong> {greeting.to_name}</p>
            <p style="font-style: italic; margin-top: 15px;">"{greeting.message}"</p>
        </div>
        """, unsafe_allow_html=True)

def display_theme_selector(current_theme: str) -> str:
    """Display theme selector with visual icons"""
    
    st.markdown("**Choose a Theme:**")
    
    themes = list(THEME_ICONS.keys())
    cols = st.columns(min(8, len(themes)))
    
    selected_theme = current_theme
    for idx, theme in enumerate(themes):
        with cols[idx % len(cols)]:
            emoji = THEME_ICONS.get(theme, "🎁")
            if st.button(f"{emoji}\\n{theme.title()}", key=f"theme_{theme}"):
                selected_theme = theme
                # Provide haptic feedback (visual)
                st.session_state.demo_greeting.theme = theme
    
    return selected_theme

def display_customization_panel() -> Dict:
    """Display expandable customization panel"""
    
    with st.expander("✏️ Customize Demo", expanded=st.session_state.demo_customize_expanded):
        
        greeting = st.session_state.demo_greeting
        
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
            occasion = st.selectbox(
                "Occasion",
                options=OCCASION_PRESETS,
                index=0 if greeting.occasion in OCCASION_PRESETS else 0,
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
        st.markdown("**Message (max 500 characters)**")
        message = st.text_area(
            "Your greeting message",
            value=greeting.message,
            height=100,
            max_chars=500,
            key="demo_message",
            label_visibility="collapsed"
        )
        
        char_count = len(message)
        col1, col2 = st.columns([3, 1])
        with col2:
            st.caption(f"{char_count}/500")
            if char_count > 400:
                st.warning("Getting close to limit!")
        
        # Theme selection in customization
        st.markdown("**Select Theme**")
        theme = display_theme_selector(greeting.theme)
        
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
        st.markdown("### 📱 Generated QR Code")
        st.image(qr_image, use_column_width=True, caption="Scan to see the greeting")
        
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
                file_name=f"{greeting.from_name}_{greeting.to_name}_greeting.png",
                mime="image/png",
                key="demo_download_qr"
            )
        
        with button_col2:
            if st.button("📤 Share", key="demo_share"):
                st.info("Share functionality coming soon!")
        
        with button_col3:
            if st.button("🔄 New", key="demo_new"):
                st.session_state.demo_greeting = get_seasonal_demo()
                st.session_state.demo_qr_generated = False
                st.rerun()
    
    with col2:
        st.markdown("### 📲 When Scanned")
        
        # Mobile frame mockup
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 20px;
            text-align: center;
            color: white;
        ">
            <div style="
                background: white;
                color: #333;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 10px;
            ">
                <h3 style="margin: 0;">✨ Greeting ✨</h3>
            </div>
            
            <div style="
                background: white;
                color: #333;
                padding: 20px;
                border-radius: 10px;
                text-align: left;
            ">
                <p><strong>From:</strong> {greeting.from_name}</p>
                <p><strong>To:</strong> {greeting.to_name}</p>
                <p style="margin-top: 15px;"><em>"{greeting.message}"</em></p>
                <p style="margin-top: 15px; font-size: 0.9em; color: #888;">
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
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>✨ Try the Interactive Demo ✨</h1>
        <p style="font-size: 1.1em; color: #666;">
            Create a sample greeting in under 60 seconds
        </p>
        <p style="color: #999; font-size: 0.9em;">
            ✅ No signup required • ✅ No login needed • ✅ Fully interactive
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== LAYOUT ==========
    demo_col1, demo_col2 = st.columns([1, 1])
    
    with demo_col1:
        st.markdown("### 📝 Sample Greeting")
        display_greeting_preview(st.session_state.demo_greeting)
        
        # Customization button
        if st.button("✏️ Customize Demo", key="customize_btn", width='stretch'):
            st.session_state.demo_customize_expanded = not st.session_state.demo_customize_expanded
            st.rerun()
        
        # Generate button (primary CTA)
        if st.button(
            "✨ Generate QR Code",
            key="generate_btn",
            width='stretch',
            type="primary"
        ):
            st.session_state.demo_qr_generated = True
            st.rerun()
    
    # Handle customization if expanded
    if st.session_state.demo_customize_expanded:
        st.divider()
        custom_data = display_customization_panel()
        
        # Update greeting with customizations
        st.session_state.demo_greeting = DemoGreeting(
            from_name=custom_data["from_name"],
            to_name=custom_data["to_name"],
            occasion=custom_data["occasion"],
            message=custom_data["message"],
            theme=custom_data["theme"],
            animation=custom_data["animation"]
        )
        
        if st.button(
            "Update QR Preview",
            key="update_preview_btn",
            width='stretch',
            type="secondary"
        ):
            st.session_state.demo_qr_generated = True
            st.rerun()
    
    # ========== QR CODE GENERATION & DISPLAY ==========
    if st.session_state.demo_qr_generated:
        st.divider()
        
        # Generate QR code
        qr_image = generate_demo_qr_code(st.session_state.demo_greeting)
        
        # Display QR with mockup
        display_qr_with_mobile_mockup(qr_image, st.session_state.demo_greeting)
        
        # ========== NEXT STEPS ==========
        st.divider()
        
        st.markdown("""
        <div style="background: #f0f8ff; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>👉 Next Step</h3>
            <p>Liked what you created? Now it's time to make your own!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🎁 Create My Own Greeting",
                key="convert_btn",
                width='stretch',
                type="primary"
            ):
                # Log conversion event (placeholder for analytics)
                st.session_state["demo_converted"] = True
                # Navigate to create tab
                st.switch_page("pages/create.py")  # Adjust based on your routing
    
    # ========== FOOTER ==========
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.9em; margin-top: 30px;">
        <p>
            💡 <strong>Pro Tip:</strong> Messages work best under 300 characters for optimal QR code size
        </p>
        <p>
            Questions? Check out the <strong>About</strong> tab for more info
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# If running as main module (for testing)
# ============================================================================

if __name__ == "__main__":
    render()
```

---

## Integration Points

### 1. Navigation Integration

**In app.py sidebar:**
```python
st.markdown("---")
st.markdown("### 🚀 Quick Start")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Try Demo",