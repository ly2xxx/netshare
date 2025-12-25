"""
QR code generation module
Handles QR code creation with theme icons and visible messages
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
from config import THEME_ICONS
from utils.image_utils import load_theme_icon


def generate_qr_code(data: str, theme: str = "general", visible_message: str = None, all_sides: bool = False, error_correction=qrcode.constants.ERROR_CORRECT_H) -> Image.Image:
    """
    Generate QR code from data string

    Args:
        data: String data to encode
        theme: Theme name for icon overlay
        visible_message: Optional text to display around the QR code
        all_sides: If True, display visible_message on all 4 sides (top, bottom, left, right)
        error_correction: QR error correction level

    Returns:
        PIL Image of QR code
    """
    qr = qrcode.QRCode(
        version=None,  # Auto-detect version
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    # Convert qrcode.image.pil.PilImage to standard PIL.Image.Image
    pil_img = img.convert('RGB')

    # Add theme icon if applicable
    if theme in THEME_ICONS and THEME_ICONS[theme]:
        qr_width, qr_height = pil_img.size

        # Icon should be ~15% of QR code size for reliable scanning (safe margin under 20%)
        icon_size = int(min(qr_width, qr_height) * 0.15)

        try:
            # Load icon from file
            icon = load_theme_icon(theme, icon_size)

            # If icon not found, skip embedding
            if icon is None:
                return pil_img

            # Calculate center position
            icon_pos = (
                (qr_width - icon_size) // 2,
                (qr_height - icon_size) // 2
            )

            # Create white background circle for better contrast
            background = Image.new('RGBA', (icon_size, icon_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(background)
            draw.ellipse([0, 0, icon_size, icon_size], fill=(255, 255, 255, 255))

            # Convert pil_img to RGBA for pasting
            pil_img = pil_img.convert('RGBA')

            # Paste white circle, then icon
            pil_img.paste(background, icon_pos, background)
            pil_img.paste(icon, icon_pos, icon)

            # Convert back to RGB
            pil_img = pil_img.convert('RGB')
        except Exception as e:
            # If icon embedding fails, just return plain QR code
            print(f"Warning: Could not embed icon for theme '{theme}': {e}")


    # Add visible message if provided
    if visible_message:
        try:
            # Prepare for font loading
            font_path = None
            font_size = 20 # Start with a baseline

            # Common fonts to try (including CJK support)
            # msyh.ttf = Microsoft YaHei (Windows Chinese)
            # simhei.ttf = SimHei (Windows Chinese)
            # NotoSansCJK... = Linux CJK
            font_names = ["msyh.ttf", "simhei.ttf", "arial.ttf", "calibri.ttf", "seguiemj.ttf",
                          "segoeui.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf",
                          "WenQuanYiMicroHei.ttf", "NotoSansCJK-Regular.ttc"]

            for name in font_names:
                try:
                    # check if we can load it
                    ImageFont.truetype(name, font_size)
                    font_path = name
                    break
                except OSError:
                    continue

            # Helper to get text size
            def get_text_size(text, font):
                draw_dummy = ImageDraw.Draw(pil_img)
                if hasattr(draw_dummy, 'textbbox'):
                    bbox = draw_dummy.textbbox((0, 0), text, font=font)
                    return bbox[2] - bbox[0], bbox[3] - bbox[1]
                else:
                    return draw_dummy.textsize(text, font=font)

            qr_width, qr_height = pil_img.size
            target_width = qr_width * 0.9  # Use 90% of width for safe margins (5% each side)

            # Formatting
            padding = int(qr_height * 0.05) # 5% of QR height as vertical padding
            if padding < 20: padding = 20

            # Add spacing between QR code and text to prevent overlap
            text_padding = int(qr_height * 0.08)  # 8% of QR height for clear separation
            if text_padding < 15: text_padding = 15  # Minimum 15px spacing

            font = None
            if font_path:
                # Iterative sizing or calculation
                # Heuristic: Width is roughly proportional to font size
                # 1. Measure at base size
                test_font = ImageFont.truetype(font_path, font_size)
                w, h = get_text_size(visible_message, test_font)

                if w > 0:
                    # Calculate desired size
                    # scale = target / current
                    scale_factor = target_width / w
                    new_font_size = int(font_size * scale_factor)

                    # Clamp limits
                    min_size = 12
                    max_size = int(qr_height * 0.2) # Max text height 20% of QR? Or just cap size.
                                                  # Let's cap max size to avoid absurdity on short words like "Hi"

                    if new_font_size < min_size: new_font_size = min_size
                    if new_font_size > max_size: new_font_size = max_size

                    font_size = new_font_size
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = test_font
            else:
                # Fallback to default (cannot resize)
                font = ImageFont.load_default()

            # Final measurement
            text_width, text_height = get_text_size(visible_message, font)

            if all_sides:
                # All 4 sides mode: add text on top, bottom, left, and right
                # Calculate final image size (QR + text on all sides)
                # Use larger margin for left/right sides to prevent text from touching QR code
                side_padding = text_height + (text_padding * 3)  # Horizontal space for rotated text

                # For vertical space, we need to fit BOTH the QR code AND the rotated text
                # Rotated text height = original text_width
                # Ensure we have enough vertical space for whichever is taller
                vertical_content_height = max(qr_height, text_width)  # QR or rotated text, whichever is taller

                final_width = qr_width + 2 * side_padding  # Left and right sides
                final_height = vertical_content_height + 2 * (text_height + text_padding)  # Top and bottom text

                new_img = Image.new('RGB', (final_width, final_height), 'white')

                # Center QR code vertically within the available content area
                qr_x = side_padding
                qr_y = text_height + text_padding + (vertical_content_height - qr_height) // 2
                new_img.paste(pil_img, (qr_x, qr_y))

                draw_new = ImageDraw.Draw(new_img)

                # Draw top text (centered horizontally)
                top_text_x = (final_width - text_width) // 2
                top_text_y = (text_height + text_padding - text_height) // 2
                draw_new.text((top_text_x, top_text_y), visible_message, fill="black", font=font)

                # Draw bottom text (centered horizontally)
                bottom_text_x = (final_width - text_width) // 2
                bottom_text_y = text_height + text_padding + vertical_content_height + text_padding // 2
                draw_new.text((bottom_text_x, bottom_text_y), visible_message, fill="black", font=font)

                # Create rotated text image for left side (rotated 90 degrees counter-clockwise)
                # Add extra padding to canvas to prevent text clipping from font metrics
                canvas_padding = text_height  # Extra space for descenders/ascenders
                left_canvas_w = text_width + 2 * canvas_padding
                left_canvas_h = text_height + 2 * canvas_padding
                left_text_img = Image.new('RGBA', (left_canvas_w, left_canvas_h), (255, 255, 255, 0))
                left_draw = ImageDraw.Draw(left_text_img)
                left_draw.text((canvas_padding, canvas_padding), visible_message, fill="black", font=font)
                left_text_rotated = left_text_img.rotate(90, expand=True)

                # Paste left text (centered both horizontally in side margin and vertically in content area)
                left_x = (side_padding - left_text_rotated.width) // 2
                left_y = text_height + text_padding + (vertical_content_height - left_text_rotated.height) // 2
                new_img.paste(left_text_rotated, (left_x, left_y), left_text_rotated)

                # Create rotated text image for right side (rotated 90 degrees clockwise)
                right_canvas_w = text_width + 2 * canvas_padding
                right_canvas_h = text_height + 2 * canvas_padding
                right_text_img = Image.new('RGBA', (right_canvas_w, right_canvas_h), (255, 255, 255, 0))
                right_draw = ImageDraw.Draw(right_text_img)
                right_draw.text((canvas_padding, canvas_padding), visible_message, fill="black", font=font)
                right_text_rotated = right_text_img.rotate(-90, expand=True)

                # Paste right text (centered both horizontally in side margin and vertically in content area)
                right_x = qr_x + qr_width + (side_padding - right_text_rotated.width) // 2
                right_y = text_height + text_padding + (vertical_content_height - right_text_rotated.height) // 2
                new_img.paste(right_text_rotated, (right_x, right_y), right_text_rotated)

                return new_img
            else:
                # Bottom only mode (original behavior)
                # Create new image
                # Width: at least QR width. If text is somehow wider (min size limit), expand.
                final_width = max(qr_width, text_width + int(qr_width * 0.1)) # Ensure margins if text is wider
                final_height = qr_height + text_height + 2 * padding + text_padding  # Include text spacing

                new_img = Image.new('RGB', (final_width, final_height), 'white')

                # Paste QR code (centered horizontally)
                qr_x = (final_width - qr_width) // 2
                qr_y = padding // 2
                new_img.paste(pil_img, (qr_x, qr_y))

                # Draw text (centered horizontally, below QR)
                draw_new = ImageDraw.Draw(new_img)
                text_x = (final_width - text_width) // 2
                text_y = qr_y + qr_height + text_padding

                draw_new.text((text_x, text_y), visible_message, fill="black", font=font)

                return new_img

        except Exception as e:
            print(f"Warning: Failed to add visible message: {e}")
            return pil_img

    return pil_img
