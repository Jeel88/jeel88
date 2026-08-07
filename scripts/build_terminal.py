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
# Check files
# -----------------------------------------

if not TERMINAL_FILE.exists():
    raise FileNotFoundError(
        f"Terminal SVG not found:\n{TERMINAL_FILE}"
    )

if not ASCII_FILE.exists():
    raise FileNotFoundError(
        f"ASCII SVG not found:\n{ASCII_FILE}"
    )


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
# Extract the ASCII SVG content
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
# Create portrait container
# -----------------------------------------

portrait = f"""
<g transform="translate(55 220) scale(0.82)">

    {ascii_content}

</g>
"""


# -----------------------------------------
# Add portrait to terminal
# -----------------------------------------

marker = """
<!-- PORTRAIT_PLACEHOLDER -->
"""


if marker not in terminal:
    raise ValueError(
        "PORTRAIT_PLACEHOLDER not found "
        "inside terminal.svg"
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
print(f"Terminal : {TERMINAL_FILE}")
print(f"ASCII    : {ASCII_FILE}")
print(f"Output   : {OUTPUT_FILE}")