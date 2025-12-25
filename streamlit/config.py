"""
Configuration and constants for QR Greeting Card Generator
Contains theme definitions, CSS styles, and application settings
"""

# Theme to emoji mapping
THEME_ICONS = {
    "snowflake": "❄️",
    "fireworks": "🎆",
    "lights": "✨",
    "stars": "⭐",
    "confetti": "🎉",
    "champagne": "🥂",
    "hearts": "❤️",
    "farewell": "👋",
    "general": None  # No icon for general theme
}

# Page configuration settings
PAGE_CONFIG = {
    "page_title": "Holiday Greeting QR",
    "page_icon": "🎄",
    "layout": "wide"
}

# Custom CSS styles
CSS_STYLES = """
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .greeting-box {
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stats-box {
        padding: 1rem;
        background: #e8eaf6;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .letter-container {
        background-color: #fdfbf7;
        padding: 40px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        min-height: 400px;
        position: relative;
        font-family: 'Georgia', serif;
        color: #333;
        margin-top: 20px;
    }
    .letter-header {
        margin-bottom: 30px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    .letter-from, .letter-to {
        font-size: 1.1em;
        margin: 5px 0;
    }
    .letter-body {
        font-size: 1.25em;
        line-height: 1.6;
        white-space: pre-wrap;
        margin-bottom: 60px;
    }
    .letter-watermark {
        position: absolute;
        bottom: 20px;
        right: 20px;
        opacity: 0.8;
        width: 100px;
        height: 100px;
    }
    .letter-footer {
        position: absolute;
        bottom: 20px;
        left: 20px;
        font-size: 0.8em;
        color: #888;
    }
    /* QR Code Protection - Global fallback */
    .qr-code-protected {
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        user-select: none;
        -webkit-user-drag: none;
    }
</style>
"""
