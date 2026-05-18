"""
Generate SVG diagrams for the Chessckers article series.

Usage:
    python scripts/chessckers_diagrams.py

Writes SVG files to static/images/chessckers/.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# Geometry
SQ = 56
BOARD = 8
TOTAL = BOARD + 2  # 10 (board + rim on each side)
MARGIN = 32
W = H_BOARD = TOTAL * SQ + 2 * MARGIN

# Palette
LIGHT = "#f0d9b5"
DARK = "#b58863"
RIM = "#eeeeee"
RIM_STROKE = "#cccccc"
LABEL = "#666666"
BLACK_FILL = "#2a2a2a"
BLACK_STROKE = "#000000"
BLACK_GLYPH = "#ffffff"

CBURNETT_DIR = Path(__file__).resolve().parent / "assets" / "cburnett"
PIECE_VIEWBOX = 45  # cburnett pieces are designed on a 45x45 grid


def _load_cburnett() -> dict[str, str]:
    """Load cburnett white pieces; return {piece_letter: inner SVG markup}."""
    pieces: dict[str, str] = {}
    for letter in "KQRBNP":
        raw = (CBURNETT_DIR / f"w{letter}.svg").read_text()
        # Strip the outer <svg ...>...</svg> wrapper; keep only inner markup.
        inner = re.sub(r"^.*?<svg[^>]*>", "", raw, count=1, flags=re.DOTALL)
        inner = re.sub(r"</svg>\s*$", "", inner)
        pieces[letter] = inner.strip()
    return pieces


WHITE_PIECES = _load_cburnett()


@dataclass
class Tower:
    """Bottom-to-top stack of Black pieces. Each entry is 'S' or 'K'."""
    pieces: list[str]

    @property
    def height(self) -> int:
        return len(self.pieces)

    @property
    def top(self) -> str:
        return self.pieces[-1]


@dataclass
class Position:
    white: dict[tuple[int, int], str] = field(default_factory=dict)
    black: dict[tuple[int, int], Tower] = field(default_factory=dict)


# Coordinate system: files 1..8 = a..h, ranks 1..8. Rim is file/rank in {0, 9}.
# SVG: top-left origin, rank 8 drawn at top.

def square_xy(file: int, rank: int) -> tuple[int, int]:
    x = MARGIN + file * SQ
    y = MARGIN + (9 - rank) * SQ
    return x, y


def square_center(file: int, rank: int) -> tuple[int, int]:
    x, y = square_xy(file, rank)
    return x + SQ // 2, y + SQ // 2


def is_rim(file: int, rank: int) -> bool:
    return file in (0, 9) or rank in (0, 9)


def is_light_square(file: int, rank: int) -> bool:
    return (file + rank) % 2 == 1


def draw_squares() -> str:
    parts = []
    for f in range(10):
        for r in range(10):
            x, y = square_xy(f, r)
            if is_rim(f, r):
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" '
                    f'fill="{RIM}" stroke="{RIM_STROKE}" stroke-dasharray="3,3"/>'
                )
            else:
                color = LIGHT if is_light_square(f, r) else DARK
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" fill="{color}"/>'
                )
    return "\n".join(parts)


def draw_axis_labels() -> str:
    parts = []
    for i, letter in enumerate("abcdefgh", start=1):
        x = MARGIN + i * SQ + SQ // 2
        y = MARGIN + 10 * SQ + 16
        parts.append(
            f'<text x="{x}" y="{y}" text-anchor="middle" '
            f'font-size="13" fill="{LABEL}">{letter}</text>'
        )
    for r in range(1, 9):
        x = MARGIN - 8
        y = MARGIN + (9 - r) * SQ + SQ // 2 + 5
        parts.append(
            f'<text x="{x}" y="{y}" text-anchor="end" '
            f'font-size="13" fill="{LABEL}">{r}</text>'
        )
    return "\n".join(parts)


def draw_white(file: int, rank: int, piece: str) -> str:
    size = SQ - 6  # slight padding inside the square
    x, y = square_xy(file, rank)
    return f'<use href="#piece-w{piece}" x="{x + 3}" y="{y + 3}" width="{size}" height="{size}"/>'


def piece_defs() -> str:
    parts = ['<defs>']
    for letter, inner in WHITE_PIECES.items():
        parts.append(
            f'<symbol id="piece-w{letter}" viewBox="0 0 {PIECE_VIEWBOX} {PIECE_VIEWBOX}">{inner}</symbol>'
        )
    parts.append('</defs>')
    return "\n".join(parts)


def draw_tower(file: int, rank: int, tower: Tower) -> str:
    cx, cy = square_center(file, rank)
    radius = SQ // 2 - 5
    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" '
        f'fill="{BLACK_FILL}" stroke="{BLACK_STROKE}" stroke-width="1.5"/>'
    ]
    if tower.top == "K":
        # three crown notches on top
        ny = cy - radius + 3
        for dx in (-10, 0, 10):
            parts.append(
                f'<polygon points="{cx + dx - 4},{ny} {cx + dx + 4},{ny} '
                f'{cx + dx},{ny - 6}" fill="{BLACK_FILL}" stroke="{BLACK_STROKE}"/>'
            )
    parts.append(
        f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" '
        f'font-size="22" font-weight="bold" fill="{BLACK_GLYPH}">{tower.top}</text>'
    )
    if tower.height > 1:
        bx, by = cx + radius - 8, cy + radius - 4
        parts.append(
            f'<circle cx="{bx}" cy="{by}" r="9" fill="#ffffff" stroke="#000000"/>'
            f'<text x="{bx}" y="{by + 4}" text-anchor="middle" '
            f'font-size="11" font-weight="bold" fill="#000000">{tower.height}</text>'
        )
    return "\n".join(parts)


def render(pos: Position) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H_BOARD}" '
        f'width="{W}" height="{H_BOARD}" '
        f'font-family="system-ui, -apple-system, Segoe UI, sans-serif">',
        piece_defs(),
        draw_squares(),
        draw_axis_labels(),
    ]
    for (f, r), piece in pos.white.items():
        parts.append(draw_white(f, r, piece))
    for (f, r), tower in pos.black.items():
        parts.append(draw_tower(f, r, tower))
    parts.append("</svg>")
    return "\n".join(parts)


def initial_position() -> Position:
    pos = Position()
    for f, p in enumerate("RNBQKBNR", start=1):
        pos.white[(f, 1)] = p
        pos.white[(f, 2)] = "P"
    for f in range(1, 9):
        pos.black[(f, 6)] = Tower(["S"])
        pos.black[(f, 7)] = Tower(["K"])
        pos.black[(f, 8)] = Tower(["S"])
    return pos


OUT_DIR = Path(__file__).resolve().parent.parent / "static" / "images" / "chessckers"


def write(name: str, svg: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.svg"
    path.write_text(svg)
    print(f"wrote {path}")


def main() -> None:
    write("initial-position", render(initial_position()))


if __name__ == "__main__":
    main()
