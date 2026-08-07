from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import html


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parent.parent

PHOTO = ROOT / "photo" / "profile.jpg"
OUTPUT = ROOT / "assets" / "svg" / "ascii.svg"


# =========================================================
# ASCII SETTINGS
# =========================================================

COLUMNS = 110

ASCII_CHARS = "-:.=+*#%@"

TEXT_COLOR = "#FFFFFF"

FONT_SIZE = 5
LINE_HEIGHT = 6

PADDING = 10

BRIGHTNESS = 1.35
CONTRAST = 1.6
SHARPNESS = 1.2


# =========================================================
# IMAGE ADJUSTMENT
# =========================================================

# Brightness
BRIGHTNESS = 1.65

# Contrast
CONTRAST = 1.45

# Sharpness
SHARPNESS = 1.35


# =========================================================
# CHECK PHOTO
# =========================================================

if not PHOTO.exists():
    raise FileNotFoundError(
        f"Photo not found:\n{PHOTO}"
    )


# =========================================================
# LOAD IMAGE
# =========================================================

image = Image.open(PHOTO)

# Convert to grayscale
image = ImageOps.grayscale(image)


# =========================================================
# BRIGHTEN DARK PHOTO
# =========================================================

image = ImageEnhance.Brightness(
    image
).enhance(BRIGHTNESS)


# =========================================================
# INCREASE CONTRAST
# =========================================================

image = ImageEnhance.Contrast(
    image
).enhance(CONTRAST)


# =========================================================
# SHARPEN
# =========================================================

image = ImageEnhance.Sharpness(
    image
).enhance(SHARPNESS)


# =========================================================
# AUTO-CONTRAST
# =========================================================

image = ImageOps.autocontrast(
    image,
    cutoff=2
)


# =========================================================
# RESIZE
# =========================================================

original_width, original_height = image.size

aspect_ratio = (
    original_height / original_width
)

CHARACTER_RATIO = 0.5

rows = max(
    1,
    int(
        COLUMNS
        * aspect_ratio
        * CHARACTER_RATIO
    )
)

image = image.resize(
    (COLUMNS, rows),
    Image.Resampling.LANCZOS
)


# =========================================================
# ASCII CONVERSION
# =========================================================

pixels = list(image.getdata())

ascii_lines = []


for row in range(rows):

    line = ""

    for column in range(COLUMNS):

        pixel = pixels[
            row * COLUMNS + column
        ]

        # Brightness → ASCII character
        index = int(
            pixel
            / 255
            * (len(ASCII_CHARS) - 1)
        )

        line += ASCII_CHARS[index]

    ascii_lines.append(line)


# =========================================================
# SVG DIMENSIONS
# =========================================================

svg_width = (
    COLUMNS
    * FONT_SIZE
    * 0.62
    + PADDING * 2
)

svg_height = (
    rows
    * LINE_HEIGHT
    + PADDING * 2
)


# =========================================================
# CREATE SVG
# =========================================================

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{svg_width:.0f}"
height="{svg_height:.0f}"
viewBox="0 0 {svg_width:.0f} {svg_height:.0f}"
xml:space="preserve">

<style>

.ascii {{
    font-family:
        "SFMono-Regular",
        "Cascadia Mono",
        "JetBrains Mono",
        Consolas,
        monospace;

    font-size: {FONT_SIZE}px;

    font-weight: 700;

    fill: {TEXT_COLOR};

    letter-spacing: 0px;
}}

</style>

<g>
'''


# =========================================================
# ADD ASCII
# =========================================================

for index, line in enumerate(ascii_lines):

    safe_line = html.escape(line)

    y = (
        PADDING
        + FONT_SIZE
        + index * LINE_HEIGHT
    )

    svg += f'''
<text
    class="ascii"
    x="{PADDING}"
    y="{y}">
    {safe_line}
</text>
'''


# =========================================================
# CLOSE SVG
# =========================================================

svg += """
</g>
</svg>
"""


# =========================================================
# SAVE
# =========================================================

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)


# =========================================================
# OUTPUT
# =========================================================

print()
print("======================================")
print(" BRIGHT ASCII PORTRAIT GENERATED")
print("======================================")
print()
print(f"Columns   : {COLUMNS}")
print(f"Rows      : {rows}")
print(f"Brightness: {BRIGHTNESS}")
print(f"Contrast  : {CONTRAST}")
print(f"Sharpness : {SHARPNESS}")
print(f"Color     : {TEXT_COLOR}")
print()
print(f"Output: {OUTPUT}")
print()