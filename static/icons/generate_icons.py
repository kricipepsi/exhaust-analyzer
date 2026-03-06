#!/usr/bin/env python3
"""
Generate PWA icon set for Exhaust Analyzer
Requires Pillow: pip install pillow
"""

from PIL import Image, ImageDraw

def create_icon(size, filename, bg_color=(255, 255, 255), accent_color=(0, 102, 204)):
    """Create a simple icon with a blue circle and '5G' text."""
    img = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw circle (slightly inset)
    margin = size // 8
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=accent_color
    )

    # Add text "5G" (simplified - no font)
    # Since we may not have fonts, we'll draw a simple text representation
    # In production, use a proper .ttf font file
    try:
        # Try to use a built-in font; may fail on some systems
        from PIL import ImageFont
        font_size = size // 3
        # Use default font
        font = ImageFont.load_default()
        text = "5G"
        # Calculate text position (approximate)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        position = ((size - text_w) // 2, (size - text_h) // 2)
        draw.text(position, text, fill='white', font=font)
    except Exception as e:
        # Fallback: draw a simple "5" shape
        draw.rectangle([size//3, size//3, size//2, size//2], fill='white')

    img.save(filename)
    print(f"Created {filename}")

def main():
    import os
    icons_dir = os.path.dirname(__file__) or '.'
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]

    for size in sizes:
        filename = os.path.join(icons_dir, f"icon-{size}x{size}.png")
        create_icon(size, filename)

    print("✅ All icons generated!")

if __name__ == '__main__':
    main()