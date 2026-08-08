from pathlib import Path
import re


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_FILE = (
    BASE_DIR
    / "assets"
    / "svg"
    / "terminal.svg"
)

ASCII_FILE = (
    BASE_DIR
    / "assets"
    / "svg"
    / "ascii.svg"
)

NAME_FILE = (
    BASE_DIR
    / "assets"
    / "svg"
    / "name.svg"
)

OUTPUT_FILE = (
    BASE_DIR
    / "assets"
    / "svg"
    / "profile-terminal.svg"
)


# ============================================================
# PORTRAIT SETTINGS
# ============================================================

PORTRAIT_X = 45
PORTRAIT_Y = 205

PORTRAIT_WIDTH = 280
PORTRAIT_HEIGHT = 300


# ============================================================
# NAME SETTINGS
# ============================================================

NAME_X = 520
NAME_Y = 200


# ============================================================
# CHECK FILES
# ============================================================

for file in [
    TEMPLATE_FILE,
    ASCII_FILE,
    NAME_FILE
]:

    if not file.exists():

        raise FileNotFoundError(
            f"\nRequired file not found:\n{file}"
        )


# ============================================================
# READ FILES
# ============================================================

template = TEMPLATE_FILE.read_text(
    encoding="utf-8"
)

ascii_svg = ASCII_FILE.read_text(
    encoding="utf-8"
)

name_svg = NAME_FILE.read_text(
    encoding="utf-8"
)


# ============================================================
# GET ASCII VIEWBOX
# ============================================================

viewbox_match = re.search(
    r'viewBox\s*=\s*["\']([^"\']+)["\']',
    ascii_svg,
    re.IGNORECASE
)


if viewbox_match:

    ascii_viewbox = viewbox_match.group(1)

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
            "Could not determine ASCII SVG size."
        )

    ascii_width = width_match.group(1)
    ascii_height = height_match.group(1)

    ascii_viewbox = (
        f"0 0 {ascii_width} {ascii_height}"
    )


# ============================================================
# EXTRACT SVG CONTENT
# ============================================================

def extract_svg_content(svg):

    match = re.search(
        r'<svg\b[^>]*>(.*)</svg>',
        svg,
        re.IGNORECASE | re.DOTALL
    )

    if not match:

        raise ValueError(
            "Invalid SVG file."
        )

    return match.group(1)


ascii_content = extract_svg_content(
    ascii_svg
)

name_content = extract_svg_content(
    name_svg
)


# ============================================================
# REMOVE ORIGINAL SVG DEFS
# ============================================================

ascii_content = re.sub(
    r'<defs\b[^>]*>.*?</defs>',
    '',
    ascii_content,
    flags=re.IGNORECASE | re.DOTALL
)


# ============================================================
# REMOVE ASCII OUTER BACKGROUND
# ============================================================

ascii_content = re.sub(
    r'<rect\b[^>]*/>',
    '',
    ascii_content,
    flags=re.IGNORECASE
)


# ============================================================
# EMBED PORTRAIT
# ============================================================

embedded_portrait = f'''
<svg
    x="{PORTRAIT_X}"
    y="{PORTRAIT_Y}"
    width="{PORTRAIT_WIDTH}"
    height="{PORTRAIT_HEIGHT}"
    viewBox="{ascii_viewbox}"
    preserveAspectRatio="xMidYMid meet"
    overflow="hidden"
    xmlns="http://www.w3.org/2000/svg">

    {ascii_content}

</svg>
'''


# ============================================================
# EMBED JEEL NAME
# ============================================================

embedded_name = f'''
<svg
    x="{NAME_X}"
    y="{NAME_Y}"
    width="410"
    height="100"
    viewBox="0 0 410 100"
    overflow="hidden"
    xmlns="http://www.w3.org/2000/svg">

    {name_content}

</svg>
'''


# ============================================================
# INSERT PORTRAIT
# ============================================================

portrait_placeholder = (
    "<!-- PORTRAIT_PLACEHOLDER -->"
)

if portrait_placeholder not in template:

    raise ValueError(
        "PORTRAIT_PLACEHOLDER "
        "not found in terminal.svg"
    )


template = template.replace(
    portrait_placeholder,
    embedded_portrait
)


# ============================================================
# INSERT NAME
# ============================================================

name_placeholder = (
    "<!-- NAME_PLACEHOLDER -->"
)

if name_placeholder not in template:

    raise ValueError(
        "NAME_PLACEHOLDER "
        "not found in terminal.svg"
    )


template = template.replace(
    name_placeholder,
    embedded_name
)


# ============================================================
# WRITE FINAL SVG
# ============================================================

OUTPUT_FILE.write_text(
    template,
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

print(f"Portrait : {ASCII_FILE}")
print(f"Name     : {NAME_FILE}")
print(f"Template : {TEMPLATE_FILE}")
print(f"Output   : {OUTPUT_FILE}")

print()

print("Portrait:")
print(
    f"  {PORTRAIT_WIDTH}px × "
    f"{PORTRAIT_HEIGHT}px"
)

print()

print("JEEL:")
print("  410px × 100px")
print("  Left → right typing animation")

print()

print("✓ Portrait fitted")
print("✓ Portrait overflow prevented")
print("✓ Extra portrait background removed")
print("✓ JEEL ASCII inserted")
print("✓ JEEL animation enabled")

print()
print("=" * 60)