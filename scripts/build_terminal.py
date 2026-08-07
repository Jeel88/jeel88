from pathlib import Path
import re


# -----------------------------------------
# Project paths
# -----------------------------------------

ROOT = Path(__file__).resolve().parent.parent

TERMINAL_FILE = ROOT / "assets" / "svg" / "terminal.svg"
ASCII_FILE = ROOT / "assets" / "svg" / "ascii.svg"

OUTPUT_FILE = ROOT / "assets" / "svg" / "profile-terminal.svg"


# -----------------------------------------
# Portrait box
# -----------------------------------------

BOX_X = 45
BOX_Y = 200

BOX_WIDTH = 500
BOX_HEIGHT = 350

PADDING = 15


# -----------------------------------------
# Read files
# -----------------------------------------

terminal = TERMINAL_FILE.read_text(
    encoding="utf-8"
)

ascii_svg = ASCII_FILE.read_text(
    encoding="utf-8"
)


# -----------------------------------------
# Get ASCII dimensions
# -----------------------------------------

width_match = re.search(
    r'width="([0-9.]+)"',
    ascii_svg
)

height_match = re.search(
    r'height="([0-9.]+)"',
    ascii_svg
)

if not width_match or not height_match:
    raise ValueError(
        "Could not determine ASCII SVG dimensions."
    )


ascii_width = float(width_match.group(1))
ascii_height = float(height_match.group(1))


# -----------------------------------------
# Extract ASCII content
# -----------------------------------------

match = re.search(
    r"<g>(.*?)</g>",
    ascii_svg,
    re.DOTALL
)

if not match:
    raise ValueError(
        "Could not find ASCII <g> element."
    )


ascii_content = match.group(1)


# -----------------------------------------
# Calculate automatic scale
# -----------------------------------------

available_width = BOX_WIDTH - (PADDING * 2)
available_height = BOX_HEIGHT - (PADDING * 2)

scale_x = available_width / ascii_width
scale_y = available_height / ascii_height

scale = min(scale_x, scale_y)


# -----------------------------------------
# Center the portrait
# -----------------------------------------

scaled_width = ascii_width * scale
scaled_height = ascii_height * scale

offset_x = (
    BOX_X
    + (BOX_WIDTH - scaled_width) / 2
)

offset_y = (
    BOX_Y
    + (BOX_HEIGHT - scaled_height) / 2
)


# -----------------------------------------
# Portrait SVG group
# -----------------------------------------

portrait = f"""
<g
    transform="translate({offset_x:.2f} {offset_y:.2f}) scale({scale:.4f})">

    {ascii_content}

</g>
"""


# -----------------------------------------
# Replace placeholder
# -----------------------------------------

marker = "<!-- PORTRAIT_PLACEHOLDER -->"

if marker not in terminal:
    raise ValueError(
        "PORTRAIT_PLACEHOLDER not found in terminal.svg"
    )


final_svg = terminal.replace(
    marker,
    portrait
)


# -----------------------------------------
# Save
# -----------------------------------------

OUTPUT_FILE.write_text(
    final_svg,
    encoding="utf-8"
)


print("======================================")
print(" TERMINAL SVG BUILT SUCCESSFULLY")
print("======================================")
print()
print(f"ASCII size : {ascii_width:.0f} x {ascii_height:.0f}")
print(f"Scale      : {scale:.4f}")
print(f"Final size : {scaled_width:.0f} x {scaled_height:.0f}")
print()
print(f"Output: {OUTPUT_FILE}")