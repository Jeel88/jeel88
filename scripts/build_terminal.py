from pathlib import Path
import re


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parent.parent

TERMINAL_FILE = (
    ROOT
    / "assets"
    / "svg"
    / "terminal.svg"
)

ASCII_FILE = (
    ROOT
    / "assets"
    / "svg"
    / "ascii.svg"
)

OUTPUT_FILE = (
    ROOT
    / "assets"
    / "svg"
    / "profile-terminal.svg"
)


# =========================================================
# PORTRAIT BOX
# =========================================================

PORTRAIT_X = 45
PORTRAIT_Y = 205

PORTRAIT_WIDTH = 500
PORTRAIT_HEIGHT = 335


# =========================================================
# READ TERMINAL
# =========================================================

if not TERMINAL_FILE.exists():

    raise FileNotFoundError(
        f"Terminal SVG not found:\n{TERMINAL_FILE}"
    )


if not ASCII_FILE.exists():

    raise FileNotFoundError(
        f"ASCII SVG not found:\n{ASCII_FILE}"
    )


terminal = TERMINAL_FILE.read_text(
    encoding="utf-8"
)

ascii_svg = ASCII_FILE.read_text(
    encoding="utf-8"
)


# =========================================================
# GET ASCII DIMENSIONS
# =========================================================

width_match = re.search(
    r'width="([0-9.]+)"',
    ascii_svg
)

height_match = re.search(
    r'height="([0-9.]+)"',
    ascii_svg
)

viewbox_match = re.search(
    r'viewBox="([^"]+)"',
    ascii_svg
)


if not width_match or not height_match:

    raise ValueError(
        "Could not read ASCII SVG dimensions."
    )


ascii_width = float(
    width_match.group(1)
)

ascii_height = float(
    height_match.group(1)
)


# =========================================================
# VIEWBOX
# =========================================================

if viewbox_match:

    viewbox = viewbox_match.group(1)

else:

    viewbox = (
        f"0 0 "
        f"{ascii_width} "
        f"{ascii_height}"
    )


# =========================================================
# EXTRACT ASCII TEXT
# =========================================================

# Get everything between <svg> and </svg>
# without the outer SVG itself.

content_match = re.search(
    r"<svg[^>]*>(.*?)</svg>",
    ascii_svg,
    re.DOTALL
)


if not content_match:

    raise ValueError(
        "Could not extract ASCII SVG content."
    )


ascii_content = content_match.group(1)


# =========================================================
# REMOVE XML HEADER IF PRESENT
# =========================================================

ascii_content = re.sub(
    r"<\?xml.*?\?>",
    "",
    ascii_content,
    flags=re.DOTALL
)


# =========================================================
# BUILD NESTED SVG
# =========================================================

portrait_svg = f'''
    <!-- ================================= -->
    <!-- AUTO GENERATED ASCII PORTRAIT -->
    <!-- ================================= -->

    <svg
        x="{PORTRAIT_X}"
        y="{PORTRAIT_Y}"
        width="{PORTRAIT_WIDTH}"
        height="{PORTRAIT_HEIGHT}"
        viewBox="{viewbox}"
        preserveAspectRatio="xMidYMid meet"
        overflow="hidden">

        {ascii_content}

    </svg>
'''


# =========================================================
# FIND PLACEHOLDER
# =========================================================

placeholder = (
    "<!-- PORTRAIT_PLACEHOLDER -->"
)


if placeholder not in terminal:

    raise ValueError(
        """
PORTRAIT_PLACEHOLDER is missing
from terminal.svg.

Add:

<!-- PORTRAIT_PLACEHOLDER -->

where the portrait should appear.
"""
    )


# =========================================================
# INSERT PORTRAIT
# =========================================================

final_svg = terminal.replace(
    placeholder,
    portrait_svg
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
    f"Portrait   : "
    f"{PORTRAIT_WIDTH} × "
    f"{PORTRAIT_HEIGHT}px"
)

print(
    f"Viewport   : "
    f"{viewbox}"
)

print()

print(
    f"Output     : "
    f"{OUTPUT_FILE}"
)

print()
print("PORTRAIT CLIPPED + SCALED SUCCESSFULLY")
print()