from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = (
    BASE_DIR
    / "assets"
    / "svg"
    / "name.svg"
)


# ============================================================
# ASCII JEEL
# ============================================================

JEEL = [
    "     ██╗███████╗███████╗██╗     ",
    "     ██║██╔════╝██╔════╝██║     ",
    "     ██║█████╗  █████╗  ██║     ",
    "██   ██║██╔══╝  ██╔══╝  ██║     ",
    "╚█████╔╝███████╗███████╗███████╗",
    " ╚════╝ ╚══════╝╚══════╝╚══════╝",
]


# ============================================================
# SETTINGS
# ============================================================

WIDTH = 410
HEIGHT = 100

FONT_SIZE = 10
LINE_HEIGHT = 13

TEXT_X = 0
TEXT_Y = 12


# ============================================================
# BUILD ASCII TEXT
# ============================================================

text_elements = []

for index, line in enumerate(JEEL):

    y = TEXT_Y + (index * LINE_HEIGHT)

    text_elements.append(
        f'''
        <text
            x="{TEXT_X}"
            y="{y}"
            fill="#38bdf8"
            font-size="{FONT_SIZE}px"
            font-family="monospace"
            xml:space="preserve">{line}</text>
        '''
    )


ascii_text = "\n".join(text_elements)


# ============================================================
# SVG
# ============================================================

svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">

    <!-- ================================= -->
    <!-- JEEL CLIP -->
    <!-- ================================= -->

    <clipPath id="typingClip">

        <rect
            x="0"
            y="0"
            width="0"
            height="{HEIGHT}">

            <animate
                attributeName="width"
                from="0"
                to="{WIDTH}"
                dur="1.8s"
                begin="0s"
                fill="freeze"/>

        </rect>

    </clipPath>


    <!-- ================================= -->
    <!-- ASCII NAME -->
    <!-- ================================= -->

    <g clip-path="url(#typingClip)">

        {ascii_text}

    </g>


    <!-- ================================= -->
    <!-- CURSOR -->
    <!-- ================================= -->

    <rect
        x="0"
        y="4"
        width="3"
        height="72"
        fill="#38bdf8">

        <animate
            attributeName="x"
            from="0"
            to="{WIDTH}"
            dur="1.8s"
            begin="0s"
            fill="freeze"/>

        <animate
            attributeName="opacity"
            values="1;1;0;1"
            dur="0.8s"
            begin="0s"
            repeatCount="indefinite"/>

    </rect>

</svg>
'''


# ============================================================
# WRITE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE.write_text(
    svg,
    encoding="utf-8"
)


# ============================================================
# SUCCESS
# ============================================================

print()
print("=" * 55)
print("          JEEL ASCII NAME GENERATED")
print("=" * 55)

print()
print(f"Output : {OUTPUT_FILE}")
print(f"Size   : {WIDTH}px × {HEIGHT}px")
print("Effect : Left → right terminal typing animation")

print()
print("=" * 55)