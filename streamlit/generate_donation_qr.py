# Script to generate a specific PayPal Donation QR code
# Run this from the codebase\streamlit directory:
# python generate_donation_qr.py

import os
import sys

# Ensure we can import from local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qr.generator import generate_qr_code
from config import THEME_COLORS

def create_donation_qr():
    # PayPal URL
    paypal_url = "https://www.paypal.com/ncp/payment/NUQG396UTFRMG"
    
    # Text Options
    # You can change this to: "Scan to Support ☕", "Feed the Developer", etc.
    visible_message = "Scan to Donate £1"
    
    # Theme configuration (Snowflake/Blue)
    theme = "snowflake"
    colors = THEME_COLORS.get(theme, {"module": "black", "ring": "black"})
    
    print(f"Generating Donation QR Code for: {paypal_url}")
    print(f"Message: {visible_message}")
    
    img = generate_qr_code(
        data=paypal_url,
        theme=theme,
        visible_message=visible_message,
        all_sides=False, # Set to True for text on all sides
        module_color=colors["module"],
        position_ring_color=colors["ring"]
    )
    
    filename = "donation_qr_snowflake.png"
    img.save(filename)
    print(f"Success! Saved to {filename}")

if __name__ == "__main__":
    create_donation_qr()
