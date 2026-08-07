from pathlib import Path
import html


# -----------------------------------------
# Project paths
# -----------------------------------------

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "assets" / "ascii" / "portrait.txt"
OUTPUT_FILE = ROOT / "assets" / "svg" / "ascii.svg"


# -----------------------------------------
# Configuration
# -----------------------------------------

FONT_SIZE = 8
LINE_HEIGHT = 9

TEXT_COLOR = "#E5E7EB"

PADDING = 20


# -----------------------------------------
# Check input
# -----------------------------------------

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"ASCII file not found:\n{INPUT_FILE}"
    )


# -----------------------------------------
# Read ASCII
# -----------------------------------------

ascii_art = INPUT_FILE.read_text(
    encoding="utf-8"
)

ascii_art = ascii_art.replace("\r\n", "\n")

# Remove accidental escaped asterisks.
ascii_art = ascii_art.replace(r"\*", "*")

# Remove accidental escaped backslashes.
ascii_art = ascii_art.replace(r"\\", "\\")

# Remove empty lines at the beginning/end.
ascii_art = ascii_art.strip("\n")

lines = ascii_art.split("\n")


# -----------------------------------------
# Calculate dimensions
# -----------------------------------------

max_width = max(
    len(line)
    for line in lines
)

width = (
    max_width * FONT_SIZE * 0.60
    + PADDING * 2
)

height = (
    len(lines) * LINE_HEIGHT
    + PADDING * 2
)


# -----------------------------------------
# Start SVG
# -----------------------------------------

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{width:.0f}"
height="{height:.0f}"
viewBox="0 0 {width:.0f} {height:.0f}"
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
    fill: {TEXT_COLOR};

    opacity: 0;

    animation:
        reveal
        0.5s
        ease-out
        forwards;
}}

@keyframes reveal {{

    from {{
        opacity: 0;
        transform: translateX(-6px);
    }}

    to {{
        opacity: 1;
        transform: translateX(0);
    }}

}}

</style>

<g>
'''


# -----------------------------------------
# Generate each ASCII line
# -----------------------------------------

for index, line in enumerate(lines):

    safe_line = html.escape(line)

    y = (
        PADDING
        + FONT_SIZE
        + index * LINE_HEIGHT
    )

    delay = index * 0.025

    svg += f'''
<text
    class="ascii"
    x="{PADDING}"
    y="{y:.0f}"
    style="animation-delay:{delay:.3f}s"
>{safe_line}</text>
'''


# -----------------------------------------
# Close SVG
# -----------------------------------------

svg += """
</g>
</svg>
"""


# -----------------------------------------
# Save
# -----------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE.write_text(
    svg,
    encoding="utf-8"
)


print("======================================")
print(" ASCII SVG GENERATED SUCCESSFULLY")
print("======================================")
print(f"Lines : {len(lines)}")
print(f"Width : {width:.0f}px")
print(f"Height: {height:.0f}px")
print()
print(f"Input : {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")