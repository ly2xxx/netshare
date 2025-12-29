#!/usr/bin/env python3
"""
Generate burn_after_read.png icon
Envelope on fire with Mission Impossible aesthetic
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_burn_after_read_icon(size=512):
    """Create envelope-on-fire icon with Mission Impossible styling"""

    # Create transparent canvas
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Mission Impossible colors
    flame_orange = (255, 69, 0, 255)  # #FF4500
    dark_red = (139, 0, 0, 255)       # #8B0000
    near_black = (26, 26, 26, 255)    # #1A1A1A
    envelope_white = (240, 240, 240, 255)

    center_x = size // 2
    center_y = size // 2

    # 1. Draw flames in background (behind envelope)
    # Multiple flame shapes with gradient effect
    flame_positions = [
        # Bottom flames
        (center_x - 120, center_y + 100, 80, 150),
        (center_x - 40, center_y + 120, 70, 140),
        (center_x + 40, center_y + 110, 75, 145),
        (center_x + 120, center_y + 90, 65, 135),
        # Side flames
        (center_x - 160, center_y + 40, 60, 120),
        (center_x + 160, center_y + 50, 55, 115),
    ]

    for fx, fy, fw, fh in flame_positions:
        # Draw flame shape (teardrop/flame)
        flame_points = []
        # Create flame outline
        for i in range(20):
            angle = (i / 20) * math.pi
            x = fx + math.cos(angle) * fw
            y = fy + math.sin(angle) * (fh * 0.6)
            flame_points.append((x, y))
        # Flame tip
        flame_points.append((fx, fy - fh))

        # Draw with gradient effect (outer darker, inner brighter)
        draw.polygon(flame_points, fill=dark_red, outline=None)

        # Inner brighter flame
        inner_points = []
        for i in range(20):
            angle = (i / 20) * math.pi
            x = fx + math.cos(angle) * (fw * 0.6)
            y = fy + math.sin(angle) * (fh * 0.4)
            inner_points.append((x, y))
        inner_points.append((fx, fy - fh * 0.7))
        draw.polygon(inner_points, fill=flame_orange, outline=None)

    # 2. Draw envelope
    envelope_top = center_y - 60
    envelope_bottom = center_y + 80
    envelope_left = center_x - 140
    envelope_right = center_x + 140

    # Envelope body (rectangle)
    draw.rectangle(
        [envelope_left, envelope_top + 50, envelope_right, envelope_bottom],
        fill=envelope_white,
        outline=near_black,
        width=3
    )

    # Envelope flap (triangle)
    flap_points = [
        (envelope_left, envelope_top + 50),
        (center_x, envelope_top),
        (envelope_right, envelope_top + 50)
    ]
    draw.polygon(flap_points, fill=(220, 220, 220, 255), outline=near_black, width=3)

    # Envelope flap lines (to show it's closed)
    draw.line([envelope_left, envelope_top + 50, center_x, envelope_top], fill=near_black, width=2)
    draw.line([center_x, envelope_top, envelope_right, envelope_top + 50], fill=near_black, width=2)

    # 3. Add "TOP SECRET" stamp
    stamp_x = center_x
    stamp_y = center_y + 20

    # Red stamp background
    stamp_bg = (200, 0, 0, 180)  # Semi-transparent red
    draw.ellipse(
        [stamp_x - 60, stamp_y - 30, stamp_x + 60, stamp_y + 30],
        fill=stamp_bg,
        outline=(150, 0, 0, 255),
        width=2
    )

    # Try to add text (will use default font if custom not available)
    try:
        # Try to load a font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Draw "TOP SECRET" text
    text = "TOP SECRET"
    # Get text bbox for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = stamp_x - text_width // 2
    text_y = stamp_y - text_height // 2

    draw.text((text_x, text_y), text, fill=near_black, font=font)

    # 4. Add more flames on top of envelope edges (burning effect)
    top_flames = [
        (envelope_left + 30, envelope_top + 30, 40, 80),
        (envelope_right - 30, envelope_top + 40, 35, 75),
        (center_x - 60, envelope_bottom - 20, 45, 70),
        (center_x + 60, envelope_bottom - 15, 40, 65),
    ]

    for fx, fy, fw, fh in top_flames:
        # Draw flame shape
        flame_points = []
        for i in range(15):
            angle = (i / 15) * math.pi
            x = fx + math.cos(angle) * fw
            y = fy + math.sin(angle) * (fh * 0.5)
            flame_points.append((x, y))
        flame_points.append((fx, fy - fh))

        draw.polygon(flame_points, fill=flame_orange, outline=dark_red, width=2)

    # 5. Add glow effect around flames (optional, for dramatic effect)
    # This is simulated by adding semi-transparent orange circles
    for fx, fy, _, fh in flame_positions + top_flames:
        glow_radius = fh * 0.4
        draw.ellipse(
            [fx - glow_radius, fy - glow_radius, fx + glow_radius, fy + glow_radius],
            fill=(255, 140, 0, 40)  # Semi-transparent orange glow
        )

    return img

if __name__ == "__main__":
    print("Generating burn_after_read.png icon...")
    icon = create_burn_after_read_icon(512)

    # Save to icons directory
    output_path = "/mnt/e/code2/netshare/streamlit/icons/burn_after_read.png"
    icon.save(output_path, "PNG")
    print(f"✓ Icon saved to {output_path}")
    print(f"  Size: {icon.size}")
    print("  Design: Envelope on fire with Mission Impossible aesthetic")
    print("  Colors: Flame orange (#FF4500) + Near-black (#1A1A1A)")
