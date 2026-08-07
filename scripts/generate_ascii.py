from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parent.parent

PHOTO = ROOT / "photo" / "profile.jpg"

OUTPUT = ROOT / "assets" / "svg" / "ascii.svg"


# =========================================================
# ASCII SETTINGS
# =========================================================

# High-density photographic ASCII
COLUMNS = 110

# Dark -> bright
ASCII_CHARS = " .:-=+*#%@"

# White ASCII
TEXT_COLOR = "#FFFFFF"

# Character appearance
FONT_SIZE = 5
LINE_HEIGHT = 6

# SVG padding
PADDING = 10


# =========================================================
# PHOTO ADJUSTMENT
# =========================================================

# Good starting values for a dark photograph
BRIGHTNESS = 1.35
CONTRAST = 1.60
SHARPNESS = 1.20


# =========================================================
# CHECK PHOTO
# =========================================================

if not PHOTO.exists():

    raise FileNotFoundError(
        f"""
Photo not found:

{PHOTO}

Put your photo here:

photo/profile.jpg
"""
    )


# =========================================================
# LOAD PHOTO
# =========================================================

image = Image.open(PHOTO)

print()
print("======================================")
print(" GENERATING ASCII PORTRAIT")
print("======================================")
print()

print(f"Input : {PHOTO}")


# =========================================================
# GRAYSCALE
# =========================================================

image = ImageOps.grayscale(image)


# =========================================================
# BRIGHTNESS
# =========================================================

image = ImageEnhance.Brightness(
    image
).enhance(BRIGHTNESS)


# =========================================================
# CONTRAST
# =========================================================

image = ImageEnhance.Contrast(
    image
).enhance(CONTRAST)


# =========================================================
# SHARPNESS
# =========================================================

image = ImageEnhance.Sharpness(
    image
).enhance(SHARPNESS)


# =========================================================
# AUTO CONTRAST
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

# ASCII characters are taller than they are wide.
# This compensates for that difference.
CHARACTER_ASPECT = 0.50

rows = max(
    1,
    int(
        COLUMNS
        * aspect_ratio
        * CHARACTER_ASPECT
    )
)


image = image.resize(
    (
        COLUMNS,
        rows
    ),
    Image.Resampling.LANCZOS
)


# =========================================================
# CONVERT TO ASCII
# =========================================================

pixels = list(
    image.getdata()
)

ascii_lines = []


for y in range(rows):

    line = ""

    for x in range(COLUMNS):

        brightness = pixels[
            y * COLUMNS + x
        ]

        # Map 0-255 to ASCII characters
        index = int(
            brightness
            / 255
            * (
                len(ASCII_CHARS) - 1
            )
        )

        line += ASCII_CHARS[index]

    ascii_lines.append(line)


# =========================================================
# SVG DIMENSIONS
# =========================================================

CHAR_WIDTH = FONT_SIZE * 0.62

SVG_WIDTH = (
    COLUMNS
    * CHAR_WIDTH
    + PADDING * 2
)

SVG_HEIGHT = (
    rows
    * LINE_HEIGHT
    + PADDING * 2
)


# =========================================================
# BUILD SVG
# =========================================================

svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{SVG_WIDTH:.2f}"
    height="{SVG_HEIGHT:.2f}"
    viewBox="0 0 {SVG_WIDTH:.2f} {SVG_HEIGHT:.2f}"
    xml:space="preserve">

'''


# =========================================================
# ASCII TEXT
# =========================================================

for row, line in enumerate(ascii_lines):

    # Escape XML-sensitive characters
    line = (
        line
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    y = (
        PADDING
        + FONT_SIZE
        + row * LINE_HEIGHT
    )

    svg += f'''
    <text
        x="{PADDING}"
        y="{y:.2f}"
        fill="{TEXT_COLOR}"
        font-family="monospace"
        font-size="{FONT_SIZE}px"
        font-weight="700"
        letter-spacing="0"
        xml:space="preserve">{line}</text>
'''


# =========================================================
# CLOSE SVG
# =========================================================

svg += """
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
# RESULT
# =========================================================

print()
print("--------------------------------------")
print(f"Columns   : {COLUMNS}")
print(f"Rows      : {rows}")
print(f"Brightness: {BRIGHTNESS}")
print(f"Contrast  : {CONTRAST}")
print(f"Sharpness : {SHARPNESS}")
print(f"Color     : {TEXT_COLOR}")
print("--------------------------------------")
print()
print(f"Output: {OUTPUT}")
print()
print("ASCII PORTRAIT GENERATED SUCCESSFULLY")
print()