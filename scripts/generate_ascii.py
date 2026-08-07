from pathlib import Path
import html


# -----------------------------------------
# Paths
# -----------------------------------------

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "assets" / "ascii" / "portrait.txt"
OUTPUT_FILE = ROOT / "assets" / "svg" / "ascii.svg"


# -----------------------------------------
# Configuration
# -----------------------------------------

FONT_SIZE = 10
LINE_HEIGHT = 12

TEXT_COLOR = "#E5E7EB"
BACKGROUND = "transparent"

PADDING = 20


# -----------------------------------------
# Read ASCII
# -----------------------------------------

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Could not find ASCII file: {INPUT_FILE}"
    )


ascii_art = INPUT_FILE.read_text(
    encoding="utf-8"
).replace("\r\n", "\n").rstrip("\n")


lines = ascii_art.split("\n")


# -----------------------------------------
# Calculate dimensions
# -----------------------------------------

max_width = max(
    (len(line) for line in lines),
    default=1
)

height = (
    len(lines) * LINE_HEIGHT
    + PADDING * 2
)

width = (
    max_width * (FONT_SIZE * 0.62)
    + PADDING * 2
)


# -----------------------------------------
# Generate SVG
# -----------------------------------------

svg = []

svg.append(
    f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{width:.0f}"
height="{height}"
viewBox="0 0 {width:.0f} {height}">

<style>

.ascii {{
    font-family:
        "SFMono-Regular",
        "Cascadia Code",
        "JetBrains Mono",
        Consolas,
        monospace;

    font-size: {FONT_SIZE}px;
    fill: {TEXT_COLOR};

    white-space: pre;
}}

</style>
'''
)


# -----------------------------------------
# Add ASCII lines
# -----------------------------------------

for index, line in enumerate(lines):

    safe_line = html.escape(line)

    y = (
        PADDING
        + FONT_SIZE
        + index * LINE_HEIGHT
    )

    delay = index * 0.035

    svg.append(
        f'''
<text
class="ascii"
x="{PADDING}"
y="{y}"
style="animation-delay:{delay:.3f}s">

{safe_line}

</text>
'''
    )


# -----------------------------------------
# Animation
# -----------------------------------------

svg.append(
    '''
<style>

.ascii {
    opacity: 0;
    animation:
        reveal
        0.4s
        ease-out
        forwards;
}

@keyframes reveal {

    from {
        opacity: 0;
        transform: translateX(-8px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }

}

</style>
'''
)


svg.append("</svg>")


# -----------------------------------------
# Write SVG
# -----------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE.write_text(
    "".join(svg),
    encoding="utf-8"
)


print("ASCII SVG generated successfully.")
print(f"Input : {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")