from pathlib import Path
import re


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parent.parent

TERMINAL_FILE = ROOT / "assets" / "svg" / "terminal.svg"
ASCII_FILE = ROOT / "assets" / "svg" / "ascii.svg"

OUTPUT_FILE = ROOT / "assets" / "svg" / "profile-terminal.svg"


# =========================================================
# PORTRAIT WINDOW
# =========================================================

BOX_X = 45
BOX_Y = 205

BOX_WIDTH = 500
BOX_HEIGHT = 335

PADDING = 12


# =========================================================
# READ SVG FILES
# =========================================================

terminal = TERMINAL_FILE.read_text(
    encoding="utf-8"
)

ascii_svg = ASCII_FILE.read_text(
    encoding="utf-8"
)


# =========================================================
# GET ASCII SVG DIMENSIONS
# =========================================================

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


ascii_width = float(
    width_match.group(1)
)

ascii_height = float(
    height_match.group(1)
)


# =========================================================
# EXTRACT ASCII CONTENT
# =========================================================

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


# =========================================================
# AVAILABLE PORTRAIT SPACE
# =========================================================

available_width = (
    BOX_WIDTH - PADDING * 2
)

available_height = (
    BOX_HEIGHT - PADDING * 2
)


# =========================================================
# CALCULATE PROPORTIONAL SCALE
# =========================================================

scale_x = (
    available_width / ascii_width
)

scale_y = (
    available_height / ascii_height
)

scale = min(
    scale_x,
    scale_y
)


# =========================================================
# FINAL SIZE AFTER SCALE
# =========================================================

final_width = (
    ascii_width * scale
)

final_height = (
    ascii_height * scale
)


# =========================================================
# CENTER ASCII
# =========================================================

offset_x = (
    BOX_X
    + (BOX_WIDTH - final_width) / 2
)

offset_y = (
    BOX_Y
    + (BOX_HEIGHT - final_height) / 2
)


# =========================================================
# INSERT ASCII
# =========================================================

portrait = f"""
<g clip-path="url(#portraitClip)">

    <g
        transform="
        translate({offset_x:.2f} {offset_y:.2f})
        scale({scale:.4f})">

        {ascii_content}

    </g>

</g>
"""


# =========================================================
# PLACEHOLDER
# =========================================================

placeholder = (
    "<!-- PORTRAIT_PLACEHOLDER -->"
)


if placeholder not in terminal:

    raise ValueError(
        "PORTRAIT_PLACEHOLDER is missing "
        "from terminal.svg"
    )


# =========================================================
# BUILD FINAL SVG
# =========================================================

final_svg = terminal.replace(
    placeholder,
    portrait
)


# =========================================================
# SAVE
# =========================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE.write_text(
    final_svg,
    encoding="utf-8"
)


# =========================================================
# RESULT
# =========================================================

print()
print("======================================")
print(" GLASS TERMINAL GENERATED")
print("======================================")
print()

print(
    f"ASCII size : "
    f"{ascii_width:.0f} × "
    f"{ascii_height:.0f}px"
)

print(
    f"Scale      : "
    f"{scale:.4f}"
)

print(
    f"Final size : "
    f"{final_width:.0f} × "
    f"{final_height:.0f}px"
)

print()

print(
    f"Output     : "
    f"{OUTPUT_FILE}"
)

print()