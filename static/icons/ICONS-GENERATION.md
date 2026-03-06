# Icon Assets for Android PWA

## Required Sizes
- 72x72
- 96x96
- 128x128
- 144x144
- 152x152
- 192x192 (adaptive/legacy)
- 384x384
- 512x512 (adaptive/legacy)

## Design Guidelines
- Simple: Exhaust pipe or gauge icon
- Colors: Blue theme (#0066cc) matching web app
- Background: White or transparent
- Icons should be clear at small sizes

## Generation Options

### Option 1: Use ImageMagick (if installed)
Create a base 512x512 SVG or PNG, then resize:

```bash
# From a source 512x512 icon.png
convert icon.png -resize 192x192 icon-192x192.png
# Repeat for each size
```

### Option 2: Online tools
- https://www.canva.com/ (create 512x512, export multiples)
- https://favicon.io/ (generate from text/emoji)

### Option 3: Placeholder (temporary)
Use a simple colored square with text "5G" or "EA"

## Placeholder Icon Generation (Python)

```python
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    # Draw a blue circle
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill='#0066cc')
    # Add text (approximate)
    try:
        font_size = size // 3
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = None
    text = "5G"
    bbox = draw.textbbox((0,0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    position = ((size - text_w) // 2, (size - text_h) // 2)
    draw.text(position, text, fill='white', font=font)
    img.save(filename)

for size in [72, 96, 128, 144, 152, 192, 384, 512]:
    create_icon(size, f"icon-{size}x{size}.png")
```

## Directory Structure
Place icons in `deployments/exhaust-analyzer/static/icons/`:
```
static/
  icons/
    icon-72x72.png
    icon-96x96.png
    ... etc
```

After adding icons, commit and push to your deployed web app. Bubblewrap will pick them up automatically.
