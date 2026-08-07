from pathlib import Path
import re


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_FILE = BASE_DIR / "assets" / "svg" / "terminal.svg"
ASCII_FILE = BASE_DIR / "assets" / "svg" / "ascii.svg"
OUTPUT_FILE = BASE_DIR / "assets" / "svg" / "profile-terminal.svg"


# ============================================================
# PORTRAIT POSITION / SIZE
# ============================================================

PORTRAIT_X = 45
PORTRAIT_Y = 205

PORTRAIT_WIDTH = 300
PORTRAIT_HEIGHT = 330


# ============================================================
# CHECK FILES
# ============================================================

if not TEMPLATE_FILE.exists():
    raise FileNotFoundError(
        f"Terminal template not found:\n{TEMPLATE_FILE}"
    )

if not ASCII_FILE.exists():
    raise FileNotFoundError(
        f"ASCII SVG not found:\n{ASCII_FILE}\n\n"
        "Run generate_ascii.py first."
    )


# ============================================================
# READ FILES
# ============================================================

template = TEMPLATE_FILE.read_text(encoding="utf-8")
ascii_svg = ASCII_FILE.read_text(encoding="utf-8")


# ============================================================
# GET VIEWBOX
# ============================================================

viewbox_match = re.search(
    r'viewBox\s*=\s*["\']([^"\']+)["\']',
    ascii_svg,
    re.IGNORECASE
)

if viewbox_match:
    viewbox = viewbox_match.group(1)

else:

    width_match = re.search(
        r'<svg[^>]*width\s*=\s*["\']([\d.]+)',
        ascii_svg,
        re.IGNORECASE
    )

    height_match = re.search(
        r'<svg[^>]*height\s*=\s*["\']([\d.]+)',
        ascii_svg,
        re.IGNORECASE
    )

    if not width_match or not height_match:
        raise ValueError(
            "Could not determine ASCII SVG dimensions."
        )

    width = width_match.group(1)
    height = height_match.group(1)

    viewbox = f"0 0 {width} {height}"


# ============================================================
# GET CONTENT INSIDE ASCII SVG
# ============================================================

svg_match = re.search(
    r'<svg\b[^>]*>(.*)</svg>',
    ascii_svg,
    re.IGNORECASE | re.DOTALL
)

if not svg_match:
    raise ValueError(
        "Could not read ascii.svg"
    )

ascii_content = svg_match.group(1)


# ============================================================
# REMOVE ASCII SVG BACKGROUND RECTANGLES
# ============================================================

# Remove common full-size background rectangles.
ascii_content = re.sub(
    r'<rect\b[^>]*'
    r'(?:width\s*=\s*["\'][^"\']+["\'][^>]*'
    r'height\s*=\s*["\'][^"\']+["\'][^>]*)'
    r'[^>]*/>',
    '',
    ascii_content,
    flags=re.IGNORECASE
)


# ============================================================
# REMOVE EXTRA CLIP / FILTER DEFINITIONS
# ============================================================

# We don't need the ASCII SVG's own outer effects.
# The main terminal handles the visual design.

ascii_content = re.sub(
    r'<defs\b[^>]*>.*?</defs>',
    '',
    ascii_content,
    flags=re.IGNORECASE | re.DOTALL
)


# ============================================================
# EMBED ASCII
# ============================================================

embedded_ascii = f"""
<svg
    x="{PORTRAIT_X}"
    y="{PORTRAIT_Y}"
    width="{PORTRAIT_WIDTH}"
    height="{PORTRAIT_HEIGHT}"
    viewBox="{viewbox}"
    preserveAspectRatio="xMidYMid meet"
    overflow="hidden"
    xmlns="http://www.w3.org/2000/svg">

    {ascii_content}

</svg>
"""


# ============================================================
# FIND PLACEHOLDER
# ============================================================

placeholder = "<!-- PORTRAIT_PLACEHOLDER -->"

if placeholder not in template:

    raise ValueError(
        "PORTRAIT_PLACEHOLDER not found in terminal.svg"
    )


# ============================================================
# INSERT ASCII
# ============================================================

result = template.replace(
    placeholder,
    embedded_ascii
)


# ============================================================
# WRITE FINAL SVG
# ============================================================

OUTPUT_FILE.write_text(
    result,
    encoding="utf-8"
)


# ============================================================
# SUCCESS
# ============================================================

print()
print("=" * 60)
print("       PROFILE TERMINAL GENERATED SUCCESSFULLY")
print("=" * 60)

print()

print(f"Input ASCII : {ASCII_FILE}")
print(f"Template    : {TEMPLATE_FILE}")
print(f"Output      : {OUTPUT_FILE}")

print()

print("Portrait:")
print(f"  X      = {PORTRAIT_X}px")
print(f"  Y      = {PORTRAIT_Y}px")
print(f"  Width  = {PORTRAIT_WIDTH}px")
print(f"  Height = {PORTRAIT_HEIGHT}px")

print()

print(f"ASCII viewBox = {viewbox}")

print()

print("✓ ASCII scaled")
print("✓ ASCII centered")
print("✓ ASCII overflow prevented")
print("✓ Extra ASCII background removed")
print("✓ Extra ASCII border removed")

print()
print("=" * 60)