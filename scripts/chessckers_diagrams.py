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
ARROW_COLOR = "#2e7d32"
CROWN_FILL = "#e53935"
CROWN_STROKE = "#7f1d1d"

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
    # Each arrow is (start, end, curve_offset_px). 0 = straight.
    arrows: list[tuple[tuple[int, int], tuple[int, int], float]] = field(default_factory=list)


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
    parts = [
        '<defs>',
        f'<marker id="arrowhead" viewBox="0 0 10 10" refX="7" refY="5" '
        f'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{ARROW_COLOR}"/></marker>',
    ]
    for letter, inner in WHITE_PIECES.items():
        parts.append(
            f'<symbol id="piece-w{letter}" viewBox="0 0 {PIECE_VIEWBOX} {PIECE_VIEWBOX}">{inner}</symbol>'
        )
    parts.append('</defs>')
    return "\n".join(parts)


def draw_arrow(start: tuple[int, int], end: tuple[int, int], curve: float = 0, label: str = "") -> str:
    x1, y1 = square_center(*start)
    x2, y2 = square_center(*end)
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / length, dy / length
    # Start just outside the source piece's circle; stop short of the target center.
    head_offset = SQ // 2 - 10
    tail_offset = 10
    sx, sy = x1 + ux * head_offset, y1 + uy * head_offset
    ex, ey = x2 - ux * tail_offset, y2 - uy * tail_offset
    stroke = (
        f'stroke="{ARROW_COLOR}" stroke-width="5" stroke-linecap="round" '
        f'marker-end="url(#arrowhead)" opacity="0.9"'
    )
    if curve == 0:
        line = f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" {stroke}/>'
        mx, my = (sx + ex) / 2, (sy + ey) / 2
    else:
        # Quadratic Bezier control point perpendicular to the direction.
        px, py = -uy, ux
        mx0, my0 = (sx + ex) / 2, (sy + ey) / 2
        cx, cy = mx0 + px * curve, my0 + py * curve
        line = (
            f'<path d="M {sx:.1f} {sy:.1f} Q {cx:.1f} {cy:.1f} {ex:.1f} {ey:.1f}" '
            f'fill="none" {stroke}/>'
        )
        # Bezier midpoint (t=0.5) sits halfway between line midpoint and control.
        mx, my = (mx0 + cx) / 2, (my0 + cy) / 2
    if not label:
        return line
    label_svg = (
        f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" dy="0.35em" '
        f'font-size="15" font-weight="bold" fill="{ARROW_COLOR}" '
        f'stroke="white" stroke-width="3" paint-order="stroke">{label}</text>'
    )
    return line + label_svg


def draw_tower(file: int, rank: int, tower: Tower) -> str:
    cx, cy = square_center(file, rank)
    radius = SQ // 2 - 5
    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" '
        f'fill="{BLACK_FILL}" stroke="{BLACK_STROKE}" stroke-width="1.5"/>'
    ]
    if tower.top == "K":
        ny = cy - radius + 3
        for dx_off in (-10, 0, 10):
            parts.append(
                f'<polygon points="{cx + dx_off - 4},{ny} {cx + dx_off + 4},{ny} '
                f'{cx + dx_off},{ny - 6}" fill="{CROWN_FILL}" stroke="{CROWN_STROKE}" stroke-width="1.2"/>'
            )
    # Render the stack as a horizontal list of piece letters,
    # bottom of stack on the left, top of stack on the right.
    n = tower.height
    available_w = 2 * radius - 8
    char_w_ratio = 0.6  # monospace char width / font size
    font_size = min(22, max(8, int(available_w / (n * char_w_ratio))))
    letter_w = font_size * char_w_ratio
    total_w = letter_w * n
    start_x = cx - total_w / 2 + letter_w / 2
    baseline_y = cy + font_size * 0.35
    for i, piece in enumerate(tower.pieces):
        x = start_x + i * letter_w
        parts.append(
            f'<text x="{x:.1f}" y="{baseline_y:.1f}" text-anchor="middle" '
            f'font-size="{font_size}" font-weight="bold" fill="{BLACK_GLYPH}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">'
            f'{piece.lower()}</text>'
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
    for arrow in pos.arrows:
        parts.append(draw_arrow(*arrow))
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


def stone_e6() -> Position:
    pos = Position()
    pos.black[(5, 6)] = Tower(["S"])
    # e6 → d5, e6 → f5
    pos.arrows.append(((5, 6), (4, 5), 0))
    pos.arrows.append(((5, 6), (6, 5), 0))
    return pos


def king_e6() -> Position:
    pos = Position()
    pos.black[(5, 6)] = Tower(["K"])
    # e6 → d5, f5, d7, f7
    for target in ((4, 5), (6, 5), (4, 7), (6, 7)):
        pos.arrows.append(((5, 6), target, 0))
    return pos


def deploy_e5_c3() -> Position:
    """[s, s, s, K] on e5; deploy top 2 pieces to c3 along the SW diagonal."""
    pos = Position()
    pos.black[(5, 5)] = Tower(["S", "S", "S", "K"])
    pos.arrows.append(((5, 5), (3, 3), 0, "[2]"))
    return pos


def deploy_e5_c3_after() -> Position:
    """Resulting state of e5c3[2]: [s, s] on e5, deployed [s, k] on c3."""
    pos = Position()
    pos.black[(5, 5)] = Tower(["S", "S"])
    pos.black[(3, 3)] = Tower(["S", "K"])
    return pos


def stone_stone_e6() -> Position:
    pos = Position()
    pos.black[(5, 6)] = Tower(["S", "S"])
    # Stone-top: forward diagonals only (toward rank 1), up to n=2 squares.
    pos.arrows.append(((5, 6), (4, 5), 0))   # d5 (near SW)
    pos.arrows.append(((5, 6), (6, 5), 0))   # f5 (near SE)
    pos.arrows.append(((5, 6), (3, 4), 22))  # c4 (far SW, curved)
    pos.arrows.append(((5, 6), (7, 4), 22))  # g4 (far SE, curved)
    return pos


def stone_king_e6() -> Position:
    pos = Position()
    pos.black[(5, 6)] = Tower(["S", "K"])
    near = [(4, 5), (6, 5), (4, 7), (6, 7)]      # d5, f5, d7, f7
    far  = [(3, 4), (7, 4), (3, 8), (7, 8)]      # c4, g4, c8, g8
    for target in near:
        pos.arrows.append(((5, 6), target, 0))
    for target in far:
        pos.arrows.append(((5, 6), target, 22))
    return pos


OUT_DIR = Path(__file__).resolve().parent.parent / "static" / "images" / "chessckers"


def write(name: str, svg: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.svg"
    path.write_text(svg)
    print(f"wrote {path}")


def main() -> None:
    write("initial-position", render(initial_position()))
    write("stone-e6", render(stone_e6()))
    write("king-e6", render(king_e6()))
    write("stone-king-e6", render(stone_king_e6()))
    write("stone-stone-e6", render(stone_stone_e6()))
    write("deploy-e5-c3", render(deploy_e5_c3()))
    write("deploy-e5-c3-after", render(deploy_e5_c3_after()))


if __name__ == "__main__":
    main()
