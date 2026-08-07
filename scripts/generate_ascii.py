from pathlib import Path
from PIL import Image, ImageOps
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

# Number of characters across.
# 55 works nicely inside our terminal.
COLUMNS = 55

# Characters go from dark -> bright.
ASCII_CHARS = "@%#*+=-:. "

# White ASCII for the glass terminal.
TEXT_COLOR = "#FFFFFF"

# Font size inside SVG.
FONT_SIZE = 7

# Character height.
LINE_HEIGHT = 7

# SVG padding.
PADDING = 10


# =========================================================
# CHECK PHOTO
# =========================================================

if not PHOTO.exists():
    raise FileNotFoundError(
        f"\nPhoto not found:\n{PHOTO}\n\n"
        "Put your photo at:\n"
        "photo/profile.jpg"
    )


# =========================================================
# LOAD IMAGE
# =========================================================

image = Image.open(PHOTO)

# Convert to grayscale.
image = ImageOps.grayscale(image)


# =========================================================
# RESIZE
# =========================================================

original_width, original_height = image.size

aspect_ratio = original_height / original_width

# Characters are taller than they are wide,
# so compensate for terminal character proportions.
CHARACTER_RATIO = 0.5

rows = max(
    1,
    int(COLUMNS * aspect_ratio * CHARACTER_RATIO)
)

image = image.resize(
    (COLUMNS, rows)
)


# =========================================================
# CONVERT IMAGE → ASCII
# =========================================================

pixels = list(image.getdata())

ascii_lines = []

for row in range(rows):

    line = ""

    for column in range(COLUMNS):

        pixel = pixels[
            row * COLUMNS + column
        ]

        # Convert brightness to ASCII character.
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
    COLUMNS * FONT_SIZE * 0.62
    + PADDING * 2
)

svg_height = (
    rows * LINE_HEIGHT
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
    font-weight: 600;
    fill: {TEXT_COLOR};
}}

</style>

<g>
'''


# =========================================================
# ADD ASCII LINES
# =========================================================

for index, line in enumerate(ascii_lines):

    # Escape XML characters.
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
# WRITE FILE
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
print("======================================")
print(" ASCII PORTRAIT GENERATED")
print("======================================")
print()
print(f"Photo      : {PHOTO}")
print(f"Characters : {COLUMNS} columns")
print(f"Rows       : {rows}")
print(f"SVG size   : {svg_width:.0f} x {svg_height:.0f}px")
print(f"Color      : {TEXT_COLOR}")
print(f"Output     : {OUTPUT}")
print()