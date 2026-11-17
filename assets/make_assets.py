#!/usr/bin/env python3
"""Generate the kawaii pixel-art SVGs for the GitHub profile README.

Run:  python3 assets/make_assets.py      (writes the .svg files next to this script)

Everything is drawn from code — no external images or fonts — so GitHub renders it as-is.
The mascots (three kawaii cats) are original characters.
Pixel font and drawing helpers are shared with the Discovery Piscine README generator.
"""
import math
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)


def n(v):
    if isinstance(v, float):
        if v.is_integer():
            return str(int(v))
        return f"{v:.2f}".rstrip("0").rstrip(".")
    return str(v)


# ------------------------------------------------------------------ pixel font
_U = {
    'A': ".###. #...# #...# ##### #...# #...# #...#",
    'B': "####. #...# #...# ####. #...# #...# ####.",
    'C': ".###. #...# #.... #.... #.... #...# .###.",
    'D': "####. #...# #...# #...# #...# #...# ####.",
    'E': "##### #.... #.... ####. #.... #.... #####",
    'F': "##### #.... #.... ####. #.... #.... #....",
    'G': ".###. #...# #.... #.### #...# #...# .####",
    'H': "#...# #...# #...# ##### #...# #...# #...#",
    'I': ".###. ..#.. ..#.. ..#.. ..#.. ..#.. .###.",
    'J': "..### ...#. ...#. ...#. #..#. #..#. .##..",
    'K': "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    'L': "#.... #.... #.... #.... #.... #.... #####",
    'M': "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    'N': "#...# #...# ##..# #.#.# #..## #...# #...#",
    'O': ".###. #...# #...# #...# #...# #...# .###.",
    'P': "####. #...# #...# ####. #.... #.... #....",
    'Q': ".###. #...# #...# #...# #.#.# #..#. .##.#",
    'R': "####. #...# #...# ####. #.#.. #..#. #...#",
    'S': ".#### #.... #.... .###. ....# ....# ####.",
    'T': "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    'U': "#...# #...# #...# #...# #...# #...# .###.",
    'V': "#...# #...# #...# #...# #...# .#.#. ..#..",
    'W': "#...# #...# #...# #.#.# #.#.# #.#.# .#.#.",
    'X': "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    'Y': "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    'Z': "##### ....# ...#. ..#.. .#... #.... #####",
    '0': ".###. #...# #..## #.#.# ##..# #...# .###.",
    '1': "..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.",
    '2': ".###. #...# ....# ...#. ..#.. .#... #####",
    '3': "##### ...#. ..#.. ...#. ....# #...# .###.",
    '4': "...#. ..##. .#.#. #..#. ##### ...#. ...#.",
    '5': "##### #.... ####. ....# ....# #...# .###.",
    '6': "..##. .#... #.... ####. #...# #...# .###.",
    '7': "##### ....# ...#. ..#.. .#... .#... .#...",
    '8': ".###. #...# #...# .###. #...# #...# .###.",
    '9': ".###. #...# #...# .#### ....# ...#. .##..",
    ' ': "..... ..... ..... ..... ..... ..... .....",
    '.': "..... ..... ..... ..... ..... .##.. .##..",
    ',': "..... ..... ..... ..... .##.. .##.. .#...",
    '!': "..#.. ..#.. ..#.. ..#.. ..#.. ..... ..#..",
    '?': ".###. #...# ....# ...#. ..#.. ..... ..#..",
    '-': "..... ..... ..... .###. ..... ..... .....",
    '+': "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
    '=': "..... ..... ##### ..... ##### ..... .....",
    ':': "..... .##.. .##.. ..... .##.. .##.. .....",
    '/': "....# ....# ...#. ..#.. .#... #.... #....",
    '_': "..... ..... ..... ..... ..... ..... #####",
    '$': "..#.. .#### #.#.. .###. ..#.# ####. ..#..",
    '>': ".#... ..#.. ...#. ....# ...#. ..#.. .#...",
    '<': "...#. ..#.. .#... #.... .#... ..#.. ...#.",
    '(': "...#. ..#.. .#... .#... .#... ..#.. ...#.",
    ')': ".#... ..#.. ...#. ...#. ...#. ..#.. .#...",
    '~': "..... ..... .#... #.#.# ...#. ..... .....",
    '*': "..... #.#.# .###. ##### .###. #.#.# .....",
    '#': ".#.#. .#.#. ##### .#.#. ##### .#.#. .#.#.",
    "'": "..#.. ..#.. .#... ..... ..... ..... .....",
    '"': ".#.#. .#.#. ..... ..... ..... ..... .....",
    '·': "..... ..... ..#.. .###. ..#.. ..... .....",
    '♥': "..... .#.#. ##### ##### .###. ..#.. .....",
    '▶': "#.... ##... ###.. ####. ###.. ##... #....",
    '▼': "..... ..... ##### .###. ..#.. ..... .....",
    '[': ".###. .#... .#... .#... .#... .#... .###.",
    ']': ".###. ...#. ...#. ...#. ...#. ...#. .###.",
    '|': "..#.. ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
}
_L = {
    'a': "..... ..... .###. ....# .#### #...# .#### .....",
    'b': "#.... #.... ####. #...# #...# #...# ####. .....",
    'c': "..... ..... .###. #.... #.... #.... .###. .....",
    'd': "....# ....# .#### #...# #...# #...# .#### .....",
    'e': "..... ..... .###. #...# ##### #.... .###. .....",
    'f': "..##. .#... ####. .#... .#... .#... .#... .....",
    'g': "..... ..... .#### #...# #...# .#### ....# .###.",
    'h': "#.... #.... ####. #...# #...# #...# #...# .....",
    'i': "..#.. ..... .##.. ..#.. ..#.. ..#.. .###. .....",
    'j': "...#. ..... ..##. ...#. ...#. ...#. #..#. .##..",
    'k': "#.... #.... #..#. #.#.. ##... #.#.. #..#. .....",
    'l': ".##.. ..#.. ..#.. ..#.. ..#.. ..#.. .###. .....",
    'm': "..... ..... ##.#. #.#.# #.#.# #.#.# #...# .....",
    'n': "..... ..... ####. #...# #...# #...# #...# .....",
    'o': "..... ..... .###. #...# #...# #...# .###. .....",
    'p': "..... ..... ####. #...# #...# ####. #.... #....",
    'q': "..... ..... .#### #...# #...# .#### ....# ....#",
    'r': "..... ..... #.##. ##..# #.... #.... #.... .....",
    's': "..... ..... .#### #.... .###. ....# ####. .....",
    't': ".#... .#... ####. .#... .#... .#..# ..##. .....",
    'u': "..... ..... #...# #...# #...# #..## .##.# .....",
    'v': "..... ..... #...# #...# #...# .#.#. ..#.. .....",
    'w': "..... ..... #...# #...# #.#.# #.#.# .#.#. .....",
    'x': "..... ..... #...# .#.#. ..#.. .#.#. #...# .....",
    'y': "..... ..... #...# #...# #...# .#### ....# .###.",
    'z': "..... ..... ##### ...#. ..#.. .#... ##### .....",
}
FONT = {k: v.split() for k, v in {**_U, **_L}.items()}
ADV = 6


def _runs(rows, x0, y0, sc, on="#"):
    d = []
    for gy, row in enumerate(rows):
        gx = 0
        while gx < len(row):
            if row[gx] == on:
                s = gx
                while gx < len(row) and row[gx] == on:
                    gx += 1
                w = (gx - s) * sc
                d.append(f"M{n(x0 + s * sc)} {n(y0 + gy * sc)}h{n(w)}v{n(sc)}h{n(-w)}z")
            else:
                gx += 1
    return "".join(d)


def text_d(s, x, y, sc):
    return "".join(_runs(FONT.get(ch, FONT["?"]), x + i * ADV * sc, y, sc) for i, ch in enumerate(s))


def tw(s, sc):
    return (len(s) * ADV - 1) * sc


def _a(attrs):
    return " " + attrs if attrs else ""


def text(s, x, y, sc, fill, attrs=""):
    return f'<path d="{text_d(s, x, y, sc)}" fill="{fill}"{_a(attrs)}/>'


def ctext(s, cx, y, sc, fill, attrs=""):
    return text(s, round(cx - tw(s, sc) / 2), y, sc, fill, attrs)


def stext(s, x, y, sc, fill, shadow, off=None, attrs=""):
    off = sc if off is None else off
    return f'<g{_a(attrs)}>{text(s, x + off, y + off, sc, shadow)}{text(s, x, y, sc, fill)}</g>'


def cstext(s, cx, y, sc, fill, shadow, off=None, attrs=""):
    return stext(s, round(cx - tw(s, sc) / 2), y, sc, fill, shadow, off, attrs)


# ------------------------------------------------------------------ primitives
def rect(x, y, w, h, fill, attrs=""):
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" fill="{fill}"{_a(attrs)}/>'


def sprite(rows, pal, x0, y0, sc):
    layers = {}
    for gy, row in enumerate(rows):
        gx = 0
        while gx < len(row):
            c = row[gx]
            if c in pal:
                s = gx
                while gx < len(row) and row[gx] == c:
                    gx += 1
                w = (gx - s) * sc
                layers.setdefault(pal[c], []).append(
                    f"M{n(x0 + s * sc)} {n(y0 + gy * sc)}h{n(w)}v{n(sc)}h{n(-w)}z")
            else:
                gx += 1
    return "".join(f'<path d="{"".join(v)}" fill="{k}"/>' for k, v in layers.items())


def ppath(x, y, w, h, s=4, offs=(3, 1, 1)):
    """Rectangle with stair-stepped (pixel-rounded) corners."""
    o = list(offs) + [0]
    m = len(offs)
    pts = [(x + o[0] * s, y), (x + w - o[0] * s, y)]
    for k in range(m):
        pts += [(x + w - o[k] * s, y + (k + 1) * s), (x + w - o[k + 1] * s, y + (k + 1) * s)]
    pts.append((x + w, y + h - m * s))
    for k in reversed(range(m)):
        pts += [(x + w - o[k] * s, y + h - (k + 1) * s), (x + w - o[k] * s, y + h - k * s)]
    pts.append((x + o[0] * s, y + h))
    for k in range(m):
        pts += [(x + o[k] * s, y + h - (k + 1) * s), (x + o[k + 1] * s, y + h - (k + 1) * s)]
    pts.append((x, y + m * s))
    for k in reversed(range(m)):
        pts += [(x + o[k] * s, y + (k + 1) * s), (x + o[k] * s, y + k * s)]
    return "M" + "L".join(f"{n(a)} {n(b)}" for a, b in pts) + "Z"


def cells_d(cells, s, ox=0, oy=0):
    rows = {}
    for i, j in cells:
        rows.setdefault(j, set()).add(i)
    d = []
    for j in sorted(rows):
        xs = sorted(rows[j])
        k = 0
        while k < len(xs):
            a = xs[k]
            while k + 1 < len(xs) and xs[k + 1] == xs[k] + 1:
                k += 1
            w = (xs[k] - a + 1) * s
            d.append(f"M{n(ox + a * s)} {n(oy + j * s)}h{n(w)}v{n(s)}h{n(-w)}z")
            k += 1
    return "".join(d)


def disc_cells(r, s, inner=0.0, pred=None):
    R = int(math.ceil(r / s)) + 1
    out = []
    for j in range(-R, R):
        for i in range(-R, R):
            px, py = (i + 0.5) * s, (j + 0.5) * s
            dd = math.hypot(px, py)
            if inner <= dd <= r and (pred is None or pred(px, py)):
                out.append((i, j))
    return out


def disc_anim(attr, base, pairs, T):
    kt, vals = ["0"], [n(base)]
    for tt, v in pairs:
        kt.append(f"{tt / T:.4f}")
        vals.append(n(v))
    kt.append("1")
    vals.append(n(pairs[-1][1]))
    return (f'<animate attributeName="{attr}" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(kt)}" values="{";".join(vals)}"/>')


REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
BLINK = ".bl{animation:bl 1.2s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
TWINKLE = (".t0{animation:tw 2.6s steps(2) infinite}.t1{animation:tw 3.4s steps(2) infinite}"
           ".t2{animation:tw 4.2s steps(3) infinite}.t3{animation:tw 1.8s steps(2) infinite}"
           "@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}")


def svg(W, H, body, css="", defs="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{label}">'
            f'<title>{label}</title><style>{css}{REDUCED}</style><defs>{defs}</defs>{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name:16s} {len(content) / 1024:6.1f} KB")

# extra glyphs this README needs
FONT['&'] = ".##.. #..#. #.#.. .#... #.#.# #..#. .##.#".split()
FONT['@'] = ".###. #...# #.### #.#.# #.### #.... .####".split()
FONT['★'] = "..#.. ..#.. ##### .###. .#.#. #...# .....".split()


# ------------------------------------------------------------------ palette (kawaii pastel)
PL = "#4a3448"        # plum: outlines and text
INK = "#3a2838"       # eyes
CREAM = "#fff8f0"
PINK, PINK_L, PINK_D = "#ff8fb1", "#ffc6d6", "#e8678f"
MINT, MINT_L, MINT_D = "#a8e6c4", "#dcf7e8", "#6cc79b"
SKY, SKY_L = "#bfe3ff", "#e8f5ff"
LAV, LAV_L = "#cdbbff", "#efe9ff"
BUT, BUT_L, BUT_D = "#ffe08a", "#fff4c7", "#e9b949"
PEACH, PEACH_D = "#ffcfb3", "#e8a07c"
SILVER, SILVER_D = "#e6e9f2", "#a9b0c7"
BLUSH = "#ff9ab5"
WHITE = "#ffffff"

BOB = ".bob{animation:bob 1.2s steps(1) infinite}@keyframes bob{50%{transform:translateY(-5px)}}"
HOP = ".hop{animation:bob .4s steps(1) infinite}"
BLINKS = (".eo{animation:eo 4s steps(1) infinite}@keyframes eo{0%{opacity:1}90%{opacity:0}95%{opacity:1}}"
          ".ec{opacity:0;animation:ec 4s steps(1) infinite}@keyframes ec{0%{opacity:0}90%{opacity:1}95%{opacity:0}}")
RISE = (".rise{opacity:0;animation:rise 3.6s ease-out infinite}"
        "@keyframes rise{0%{transform:translateY(0);opacity:0}15%{opacity:1}80%{opacity:1}100%{transform:translateY(-56px);opacity:0}}")


def card(x, y, w, h, fill, edge=PL, s=4, offs=(3, 1, 1)):
    """Pixel-rounded card: dark outline + inner fill."""
    return (f'<path d="{ppath(x, y, w, h, s, offs)}" fill="{edge}"/>'
            f'<path d="{ppath(x + s, y + s, w - 2 * s, h - 2 * s, s, offs)}" fill="{fill}"/>')


def cmap_svg(cm, x0, y0, sc):
    """cm: {(x, y): colour} → one <path> per colour."""
    layers = {}
    for (x, y), col in cm.items():
        layers.setdefault(col, set()).add((x, y))
    return "".join(f'<path d="{cells_d(c, sc, x0, y0)}" fill="{col}"/>' for col, c in layers.items())


# ------------------------------------------------------------------ mascots (original characters)
# Jelly cats: a soft blob with pointy ears and a wavy bottom, a coloured outline,
# pastel shading with a glossy highlight, tiny upright eyes and pink whiskers.
MW, MH = 28, 21            # canvas grid
OX, OY = 3, 1              # body grid offset (room for the outline and whiskers)


def ell(cx, cy, rx, ry):
    return {(x, y) for x in range(MW) for y in range(MH)
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}


def compose(parts, edge=PL):
    """Paint parts in order, then wrap the union in a 1-pixel outline."""
    cm = {}
    for cells, col in parts:
        for c in cells:
            cm[c] = col
    mask = set(cm)
    for x, y in mask:
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if q not in mask:
                cm[q] = edge
    return cm, mask


def paint(cm, mask, cells, col):
    for c in cells:
        if c in mask:
            cm[c] = col


def local(cells):
    """Body-grid coordinates → canvas coordinates."""
    return {(x + OX, y + OY) for x, y in cells}


def rows_cells(rows, on="#"):
    return {(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch == on}


JELLY = rows_cells(["...##..........##.....",
                    "..####........####....",
                    "..#####......#####....",
                    "..##################..",
                    *[".####################."] * 2,
                    *["######################"] * 8,     # soft bulge at the sides
                    *[".####################."] * 2,
                    "..##################..",
                    "..###..###..###..###.."])
INNER_EAR = {(3, 1), (4, 1), (4, 2), (18, 1), (17, 1), (17, 2)}
HILITE = {(3, 4), (4, 4), (3, 5)}
SHADE = {(x, y) for x, y in JELLY if y >= 15 or (x >= 19 and y >= 5)}
EYES_OPEN = {(7, 8), (7, 9), (14, 8), (14, 9)}
EYES_SHUT = {(6, 9), (7, 9), (8, 9), (13, 9), (14, 9), (15, 9)}
# small ω mouth drawn on a half-size pixel grid (half-cell units) so it stays tiny and centred
MOUTH_HALF = {(18, 21), (20, 21), (21, 21), (23, 21), (19, 22), (22, 22)}
CHEEKS = {(4, 10), (5, 10), (16, 10), (17, 10)}
WHISKERS = {(0, 10), (1, 10), (0, 12), (1, 12), (26, 10), (27, 10), (26, 12), (27, 12)}   # canvas coords
WHISKER_PINK = "#ff9ec4"


def _yume(cm, mask):    # holographic pastel patches
    for (cx, cy, rx, ry), col in [((6.5, 6, 4, 2.8), "#ffd6ef"), ((15, 13, 5, 3.2), "#cfe5ff"),
                                  ((16, 5, 2.6, 1.8), "#d4f6e6"), ((5.5, 14, 3, 2), "#e2dbff")]:
        paint(cm, mask, ell(cx + OX, cy + OY, rx, ry), col)


def _mikan(cm, mask):   # soft tabby stripes
    paint(cm, mask, local({(10, 3), (11, 3), (10, 4), (11, 4), (8, 4), (13, 4),
                           (1, 11), (2, 11), (20, 11), (19, 11), (1, 13), (20, 13)}), "#ffb87a")


CAT_STYLES = {  # base, shade, outline, eyes/mouth, cheeks, pattern, extra parts
    "mochi": ("#f2faff", "#cbe6fa", "#5aa2da", "#36598a", "#ffb3d1", None, ()),
    "yume": ("#fdf6ff", "#dcd6ff", "#7b7fd6", "#4c50a8", "#ffa9d0", _yume, ()),
    "mikan": ("#ffe6cf", "#ffcfa6", "#e2895a", "#7a4632", "#ff9eae", _mikan, ()),
    "dinocat": ("#e6fbf0", "#bdebd4", "#46b487", "#2a6e52", "#ffadc8", None,
                ((local({(10, 1), (11, 1), (9, 2), (10, 2), (11, 2), (12, 2)}), "#ffb0cc"),)),
}
MASCOTS = CAT_STYLES


def build_cat(kind):
    base, shade, edge, eye, cheek, deco, extra = CAT_STYLES[kind]
    cm, mask = compose([*extra, (local(JELLY), base)], edge)
    paint(cm, mask, local(INNER_EAR), "#ffd0e4")
    paint(cm, mask, local(SHADE), shade)
    if deco:
        deco(cm, mask)
    paint(cm, mask, local(HILITE), WHITE)
    for c in WHISKERS:
        cm.setdefault(c, WHISKER_PINK)
    face = {c: cheek for c in local(CHEEKS)}
    return {**cm, **face}, eye


def mascot(kind, x, y, sc, mood="awake", delay=0.0, bob=True):
    """mood: awake (blinks) · sleep (eyes shut)."""
    cm, eye = build_cat(kind)
    eyes = {k: cmap_svg({c: eye for c in local(v)}, x, y, sc)
            for k, v in (("open", EYES_OPEN), ("shut", EYES_SHUT))}
    st = f' style="animation-delay:{delay:.2f}s"'
    if mood == "sleep":
        face = eyes["shut"]
    else:
        face = f'<g class="eo"{st}>{eyes["open"]}</g><g class="ec"{st}>{eyes["shut"]}</g>'
    mouth = cells_d({(hx + 2 * OX, hy + 2 * OY) for hx, hy in MOUTH_HALF}, sc / 2, x, y)
    inner = cmap_svg(cm, x, y, sc) + f'<path d="{mouth}" fill="{eye}"/>' + face
    return f'<g class="bob"{st}>{inner}</g>' if bob else f'<g>{inner}</g>'


# ------------------------------------------------------------------ small sprites
HEART = [".##.##.", "#######", "#h#####", ".#####.", "..###..", "...#..."]
SPARK = ["..#..", "..#..", "##o##", "..#..", "..#.."]
CLOUD = (ell(5, 6, 4.5, 2.8) | ell(10.5, 4.2, 5, 3.6) | ell(16, 6, 4.5, 2.8) | {(x, y) for x in range(3, 19) for y in range(6, 9)})
CLOUD_CM = {**{q: "#f4dce9" for x, y in CLOUD for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))},
            **{c: WHITE for c in CLOUD}}
BERRY = ["....g.g.g...", "...ggggggg..", "..#gggggg#..", ".#rrrrrrrr#.", "#rryrrrryrr#", "#rrrrryrrrr#",
         "#ryrrrrrryr#", ".#rrryrrrr#.", ".#rrrrrrrr#.", "..#ryrrr#...", "...#rrr#....", "....###....."]
FLOWER = [".p.", "pyp", ".p."]
GEM = ["..###..", ".#ooo#.", "#ohooo#", "#ooooo#", ".#ooo#.", "..#o#..", "...#..."]
ICON_LETTER = ["#######", "##...##", "#.#.#.#", "#..#..#", "#.....#", "#######"]
ICON_FLAG = ["#......", "#####..", "#####..", "#######", "#......", "#......", "#......"]
ICON_STAR = ["...#...", "..###..", "#######", ".#####.", "..###..", ".##.##.", "##...##"]
SNEK = ["..####.....", ".#oooo#....", "#oKooKo#...", "#oooooo#...", ".#oBBo#....", "..#oo#..##.", "..#ooo##oo#",
        "...#oooooo#", "....######."]


def heart(x, y, sc, fill=PINK, attrs=""):
    return f'<g{_a(attrs)}>{sprite(HEART, {"#": fill, "h": WHITE}, x, y, sc)}</g>'


def spark(x, y, sc, cls="t0", fill=BUT):
    return f'<g class="{cls}">{sprite(SPARK, {"#": fill, "o": WHITE}, x, y, sc)}</g>'


def flower(x, y, sc, petal=PINK, cls=""):
    a = f' class="{cls}"' if cls else ""
    return (f'<g{a}>{sprite(FLOWER, {"p": petal, "y": BUT}, x, y, sc)}'
            f'{rect(x + sc, y + 3 * sc, sc, 2 * sc, MINT_D)}</g>')


def bubble(x, y, label, attrs=""):
    w, h = tw(label, 2) + 28, 32
    tail = rect(x + 22, y + h - 4, 8, 4, PL) + rect(x + 26, y + h, 4, 4, PL) + rect(x + 24, y + h - 6, 4, 4, CREAM)
    return (f'<g{_a(attrs)}>{card(x, y, w, h, CREAM, PL, s=3, offs=(2, 1))}{tail}'
            f'{text(label, x + 14, y + 9, 2, PL)}</g>')


def zzz(x, y, delay):
    return (f'<g class="rise" style="animation-delay:{delay:.1f}s">{text("z", x, y, 3, LAV)}'
            f'{text("z", x + 16, y - 14, 2, LAV)}</g>')


# ------------------------------------------------------------------ 1 · banner (day + night)
def banner(night=False):
    W, H = 960, 360
    ground_y = 292
    sky = (["#2a2250", "#2f2758", "#352c61", "#3c316a", "#433673", "#4a3b7b"] if night else
           ["#ffe3ee", "#ffe9f2", "#fff0f6", "#f3f3ff", "#e9f4ff", "#e1f1ff"])
    band = ground_y / len(sky)
    body = "".join(rect(0, round(i * band), W, math.ceil(band) + 1, c) for i, c in enumerate(sky))
    # dithered seams between bands
    for i in range(1, len(sky)):
        yy = round(i * band) - 4
        body += f'<path d="{"".join(f"M{x} {yy}h4v4h-4z" for x in range(0 if i % 2 else 4, W, 8))}" fill="{sky[i]}"/>'

    css = BOB + BLINKS + TWINKLE + RISE
    if night:
        body += sprite(["..####..", ".##oo...", "##oo....", "##oo....", "##oo....", "##ooo...", ".##ooo##", "..####.."],
                       {"#": BUT_L, "o": BUT}, 836, 34, 6)                         # crescent moon
        for i, (sx, sy) in enumerate([(70, 40), (160, 150), (300, 30), (620, 24), (720, 140), (900, 160),
                                      (40, 210), (560, 160), (880, 250), (210, 60)]):
            body += spark(sx, sy, 2 if i % 3 else 3, f"t{i % 4}", BUT_L)
        css += (".shoot{opacity:0;animation:shoot 9s linear 2s infinite}@keyframes shoot{0%{transform:translate(0,0);"
                "opacity:0}2%{opacity:1}12%{transform:translate(-240px,110px);opacity:0}100%{opacity:0}}")
        body += (f'<g class="shoot">{rect(700, 40, 8, 8, WHITE)}{rect(708, 36, 8, 4, LAV_L)}'
                 f'{rect(716, 32, 8, 4, LAV)}</g>')
    else:
        css += (".drift{animation:drift 46s linear infinite}@keyframes drift{from{transform:translateX(-260px)}"
                "to{transform:translateX(1000px)}}")
        for i, (cy, d) in enumerate([(18, 0), (150, -15), (64, -31)]):
            body += (f'<g class="drift" style="animation-delay:{d}s">'
                     f'{cmap_svg(CLOUD_CM, 0, cy, 6)}</g>')
        for i, (sx, sy) in enumerate([(80, 60), (880, 90), (130, 200), (840, 220), (40, 130), (920, 30)]):
            body += spark(sx, sy, 3, f"t{i % 4}", BUT if i % 2 else PINK)

    title_fill, title_sh, sub = (("#ffc6da", "#120d24", LAV) if night else (PINK_D, PL, "#6b4a68"))
    body += cstext("HI, I'M SIDAPORN", W // 2, 26, 6, title_fill, title_sh)
    body += ctext("data scientist ♥ data analyst ♥ ai engineer", W // 2, 98, 3, sub)

    # ground
    gtop, gdark = (("#3f7d6f", "#2f5f55") if night else (MINT, MINT_D))
    bumps = "".join(f"M{x} {ground_y - (4 if (x // 24) % 3 == 0 else 0)}h24v8h-24z" for x in range(0, W, 24))
    body += f'<path d="{bumps}" fill="{gdark}"/>' + rect(0, ground_y + 4, W, H - ground_y, gtop)
    body += rect(0, ground_y + 4, W, 4, gdark)
    for i, fx in enumerate(range(28, W, 74)):
        body += flower(fx, ground_y + 20 + (i % 3) * 10, 4, [PINK, LAV, BUT, WHITE][i % 4],
                       f"t{i % 4}" if not night else "")

    # the gang
    cast = [("mochi", 238, 0.0, "meow~"), ("yume", 410, 0.4, "nya!"), ("mikan", 582, 0.8, "purr ♥")]
    for k, (kind, x, d, say) in enumerate(cast):
        body += mascot(kind, x, ground_y - 98, 5, "sleep" if night else "awake", d)
        if night:
            body += zzz(x + 118, ground_y - 104, k * 1.2)
        else:
            body += heart(x + 60, ground_y - 112, 3, PINK, f'class="rise" style="animation-delay:{k * 1.2 + .6:.1f}s"')
            body += bubble(x + 24, 140, say, f'class="say{k}"')
    if not night:
        T, slot = 9, 3
        for k in range(3):
            css += (f".say{k}{{opacity:0;animation:say{k} {T}s steps(1) infinite;animation-delay:{-(T - k * slot)}s}}"
                    f"@keyframes say{k}{{0%{{opacity:1}}{slot / T * 100 * .8:.1f}%{{opacity:0}}}}")
    label = ("Pixel-art banner at night: three kawaii cats asleep under the stars" if night else
             "Pixel-art banner: three kawaii cats saying hi on a sunny hill")
    return svg(W, H, body, css, label=label)


# ------------------------------------------------------------------ 2 · typing line
LINES = ["hi! i'm sidaporn ~ nice to meet you", "data science student at kmitl",
         "i turn messy data into cute insights", "curious about ai, nlp and llms",
         "always learning (and snacking)"]


def typing():
    W, H = 960, 64
    body = card(4, 4, W - 8, H - 8, "#fff3f7", PL)
    body += heart(30, 22, 3, PINK)
    x0, y0, sc = 74, 22, 3
    slot, T = 4.6, 4.6 * len(LINES)
    css = BLINK
    for i, s in enumerate(LINES):
        n_ch, dist = len(s), tw(s, sc) + 8
        vis, typed = slot / T * 100, slot * .45 / T * 100
        css += (f".l{i}{{opacity:0;animation:l{i} {T:.1f}s steps(1) infinite;animation-delay:{-(T - i * slot):.1f}s}}"
                f"@keyframes l{i}{{0%{{opacity:1}}{vis:.2f}%{{opacity:0}}}}"
                f".c{i}{{animation:c{i} {T:.1f}s steps({n_ch}) infinite;animation-delay:{-(T - i * slot):.1f}s}}"
                f"@keyframes c{i}{{0%{{transform:translateX(0)}}{typed:.2f}%,100%{{transform:translateX({dist}px)}}}}")
        body += (f'<g class="l{i}">{text(s, x0, y0, sc, PL)}'
                 f'<g class="c{i}">{rect(x0 - 2, 12, dist + 12, 40, "#fff3f7")}'
                 f'<g class="bl">{rect(x0, y0 - 2, 10, 25, PINK)}</g></g></g>')
    return svg(W, H, body, css, label="Typing: " + " / ".join(LINES))


# ------------------------------------------------------------------ 3 · pixel buttons
BUTTONS = {
    "about": ("ABOUT", HEART, PINK_L, PINK),
    "projects": ("PROJECTS", ICON_STAR, SKY_L, "#7fb8e6"),
    "skills": ("SKILLS", GEM, LAV_L, "#a690ef"), "contact": ("CONTACT", ICON_LETTER, PEACH, PEACH_D),
    "linkedin": ("LINKEDIN", ICON_STAR, SKY_L, "#7fb8e6"), "email": ("EMAIL", ICON_LETTER, PINK_L, PINK),
    "cv": ("MY CV", ICON_FLAG, MINT_L, MINT_D),
}


def button(key, i):
    label, icon, face, deep = BUTTONS[key]
    isc = 2 if len(icon[0]) <= 8 else 1
    w = 26 + len(icon[0]) * isc + 10 + tw(label, 2) + 22
    W, H = max(w, 120), 48
    body = card(2, 6, W - 4, H - 8, deep, PL, s=3, offs=(2, 1))
    body += card(2, 2, W - 4, H - 10, face, PL, s=3, offs=(2, 1))
    iy = 2 + (H - 10 - len(icon) * isc) // 2
    pal = {"#": PL if icon is not HEART else PINK_D, "o": deep, "h": WHITE}
    body += sprite(icon, pal, 18, iy, isc)
    body += text(label, 18 + len(icon[0]) * isc + 10, 2 + (H - 10 - 14) // 2, 2, PL)
    body += spark(W - 16, 6, 1, f"t{i % 4}", WHITE)
    return svg(W, H, body, TWINKLE, label=label.title() + " button")


# ------------------------------------------------------------------ 4 · player card
def player():
    W, H = 960, 250
    body = card(4, 4, W - 8, H - 8, CREAM, PL)
    body += card(26, 26, 196, 198, PINK_L, PL, s=4, offs=(2, 1))
    body += mascot("mochi", 40, 65, 6, "awake", 0.3)
    body += card(92, 206, 64, 30, BUT, PL, s=3, offs=(2, 1)) + text("P1", 112, 214, 2, PL)
    rows = [("PLAYER", "SIDAPORN J."), ("CLASS", "DATA SCIENTIST"), ("GUILD", "KMITL DSBA"), ("QUEST", "AI ENGINEER")]
    for i, (k, v) in enumerate(rows):
        y = 34 + i * 38
        body += text(k, 252, y, 3, PINK_D) + text(v, 400, y, 3, PL)
    body += text("MOVES", 252, 190, 2, "#8a6a87")
    cx = 332
    for j, mv in enumerate(["LLM AGENTS", "RAG EVAL", "CLUSTERING", "DASHBOARDS"]):
        w = tw(mv, 2) + 20
        body += card(cx, 182, w, 30, [MINT_L, SKY_L, LAV_L, BUT_L][j], PL, s=3, offs=(2, 1))
        body += text(mv, cx + 10, 190, 2, PL)
        cx += w + 10
    for k in range(5):                                                            # hearts = HP
        body += heart(732 + k * 34, 34, 3, PINK, 'class="bl"' if k == 4 else "")
    body += text("STATUS", 732, 80, 2, "#8a6a87") + rect(820, 82, 10, 10, MINT_D, 'class="bl"')
    body += text("ONLINE", 838, 80, 2, PL)
    body += spark(900, 120, 3, "t1") + spark(760, 130, 2, "t2", PINK)
    return svg(W, H, body, BOB + BLINKS + BLINK + TWINKLE, label="Player card: Sidaporn, data scientist")


# ------------------------------------------------------------------ 6 · inventory (skills)
INVENTORY = [("PYTHON", 0), ("SQL", 0), ("R", 0), ("JAVASCRIPT", 0), ("HTML", 0), ("CSS", 0),
             ("PYTORCH", 1), ("SCIKIT-LEARN", 1), ("PANDAS", 1), ("NUMPY", 1), ("SCIPY", 1), ("POLARS", 1),
             ("MATPLOTLIB", 1), ("POWER BI", 2), ("EXCEL", 2), ("SPSS", 2), ("NOSQL", 2), ("DOCKER", 2),
             ("NEO4J", 2), ("???", 3)]
CATS = [(PINK_L, PINK_D, "LANGUAGES"), (MINT_L, MINT_D, "ML + DATA LIBS"), (SKY_L, "#6aa9dc", "TOOLS"),
        ("#f3eef5", "#b9a9bd", "NEXT ITEM")]


def inventory():
    cols, sw, sh, gx, gy = 4, 212, 46, 14, 12
    rows = math.ceil(len(INVENTORY) / cols)
    x0, y0 = (960 - (cols * sw + (cols - 1) * gx)) // 2, 76
    W, H = 960, y0 + rows * sh + (rows - 1) * gy + 26
    body = card(4, 4, W - 8, H - 8, "#f7fbff", PL)
    body += text("INVENTORY", 36, 26, 3, PL)
    lx = 330
    for light, dark, name in CATS[:3]:
        body += sprite(GEM, {"#": PL, "o": dark, "h": WHITE}, lx, 26, 2) + text(name, lx + 22, 30, 2, PL)
        lx += 22 + tw(name, 2) + 34
    for i, (item, cat) in enumerate(INVENTORY):
        light, dark, _ = CATS[cat]
        x, y = x0 + (i % cols) * (sw + gx), y0 + (i // cols) * (sh + gy)
        body += card(x, y, sw, sh, light, PL, s=3, offs=(2, 1))
        body += sprite(GEM, {"#": PL, "o": dark, "h": WHITE}, x + 14, y + 9, 4)
        body += text(item, x + 56, y + 16, 2, PL if cat < 3 else "#9a8a9e")
    # roaming selector
    n_s = len(INVENTORY)
    frames = "".join(f"{i / n_s * 100:.2f}%{{transform:translate({(i % cols) * (sw + gx)}px,{(i // cols) * (sh + gy)}px)}}"
                     for i in range(n_s))
    css = (f".sel{{animation:sel {n_s * 0.9:.1f}s steps(1) infinite}}@keyframes sel{{{frames}}}" + BLINK)
    sel = (f'<path d="{ppath(x0 - 6, y0 - 6, sw + 12, sh + 12, 3, (2, 1))}" fill="none" stroke="{PINK_D}" '
           f'stroke-width="4"/>{sprite(["#....", "##...", "###..", "####.", "###..", "##...", "#...."], {"#": PINK_D}, x0 - 22, y0 + 16, 2)}')
    body += f'<g class="sel"><g class="bl">{sel}</g></g>'
    return svg(W, H, body, css, label="Inventory of skills: " + ", ".join(i for i, _ in INVENTORY[:-1]))


# ------------------------------------------------------------------ 7 · project icons
def icon(kind):
    W = H = 120
    body = card(4, 4, W - 8, H - 8, {"dinocat": PINK_L, "snek": BUT_L}[kind], PL,
                s=4, offs=(2, 1))
    if kind in MASCOTS:
        body += mascot(kind, 18, 30, 3, "awake", 0.5)
    else:
        body += f'<g class="bob">{sprite(SNEK, {"#": PL, "o": MINT, "K": INK, "B": BLUSH}, 22, 26, 7)}</g>'
    return svg(W, H, body, BOB + BLINKS, label=f"{kind} icon")


# ------------------------------------------------------------------ 9 · parade + divider
PAW = [".#.#.", "#...#", ".###.", "#####", ".###."]
FLAG = ["#######", ".#####.", "..###..", "...#..."]


def parade():
    W, H = 960, 170
    ground = 132
    body = card(4, 4, W - 8, H - 8, "#fff0f6", PL)
    inner = ""
    # soft pink → lavender → sky bands with dithered seams
    sky = ["#ffeef6", "#fcefff", "#f3f0ff", "#ecf3ff"]
    bh = (ground - 8) / len(sky)
    for i, c in enumerate(sky):
        inner += rect(8, round(8 + i * bh), W - 16, math.ceil(bh) + 1, c)
    for i in range(1, len(sky)):
        yy = round(8 + i * bh) - 3
        inner += f'<path d="{"".join(f"M{x} {yy}h3v3h-3z" for x in range(8 if i % 2 else 11, W - 8, 6))}" fill="{sky[i]}"/>'
    # drifting clouds + sparkles
    for k, (cy, d) in enumerate([(50, 0), (82, -27)]):
        inner += f'<g class="drift2" style="animation-delay:{d}s">{cmap_svg(CLOUD_CM, 0, cy, 3)}</g>'
    for i, (sx, sy) in enumerate([(60, 62), (190, 96), (330, 58), (640, 66), (780, 100), (900, 56), (480, 104)]):
        inner += spark(sx, sy, 2, f"t{i % 4}", [BUT, PINK, LAV][i % 3])
    # bunting: little pastel flags on gently sagging strings
    swag = 160
    for x in range(8, W - 8, 4):
        t = ((x - 8) % swag) / swag
        inner += rect(x, 14 + round(10 * math.sin(math.pi * t)), 4, 2, "#c9a9c6")
    for j, x in enumerate(range(20, W - 30, 32)):
        t = ((x + 10 - 8) % swag) / swag
        y = 15 + round(10 * math.sin(math.pi * t))
        col = [PINK, BUT, MINT, LAV, SKY][j % 5]
        inner += (f'<g class="flut" style="animation-delay:{(j % 4) * .25:.2f}s">'
                  f'{sprite(FLAG, {"#": col}, x, y, 3)}{rect(x + 3, y, 3, 3, WHITE, "opacity=\".6\"")}</g>')
    # title with hearts
    title = "THANKS FOR VISITING ~ SEE YOU AGAIN"
    inner += cstext(title, W // 2, 44, 2, PL, PINK_L, 2)
    inner += heart(W // 2 - tw(title, 2) // 2 - 30, 44, 2, PINK, 'class="bl"')
    inner += heart(W // 2 + tw(title, 2) // 2 + 16, 44, 2, PINK, 'class="bl" style="animation-delay:.6s"')
    # grassy ground with flowers and a paw-print trail
    bumps = "".join(f"M{x} {ground - (4 if (x // 24) % 3 == 0 else 0)}h24v8h-24z" for x in range(8, W - 8, 24))
    inner += f'<path d="{bumps}" fill="{MINT_D}"/>' + rect(8, ground + 4, W - 16, H - ground, MINT)
    inner += rect(8, ground + 4, W - 16, 3, MINT_D)
    for i, fx in enumerate(range(30, W - 20, 86)):
        inner += flower(fx, ground + 12 + (i % 2) * 8, 3, [PINK, LAV, BUT, WHITE][i % 4], f"t{i % 4}")
    for i, px in enumerate(range(60, W - 40, 44)):
        inner += sprite(PAW, {"#": "#8fd8b3"}, px, ground + 14 + (6 if i % 2 else 0), 2)
    # rising hearts
    for i, hx in enumerate([150, 420, 700, 860]):
        inner += heart(hx, ground - 24, 2, [PINK, LAV, PINK_D, BUT_D][i], f'class="rise" style="animation-delay:{i * .9:.1f}s"')
    # the walking cats
    gang = "".join(f'<g class="hop" style="animation-delay:{k * .13:.2f}s">'
                   f'{mascot(kind, k * 96, ground - 56, 3, "awake", k * .3, bob=False)}</g>'
                   for k, kind in enumerate(["mochi", "yume", "mikan"]))
    gang += heart(-34, ground - 40, 2, PINK, 'class="bl"')
    inner += f'<g class="walk">{gang}</g>'
    body += f'<g clip-path="url(#pc)">{inner}</g>'
    css = (BOB + HOP + BLINKS + BLINK + TWINKLE + RISE
           + ".walk{animation:walk 15s linear -6s infinite}"
             "@keyframes walk{from{transform:translateX(-320px)}to{transform:translateX(980px)}}"
             ".drift2{animation:drift2 60s linear infinite}"
             "@keyframes drift2{from{transform:translateX(-160px)}to{transform:translateX(980px)}}"
             ".flut{animation:flut 1.6s steps(1) infinite}@keyframes flut{50%{transform:translateY(1px)}}")
    clip = f'<clipPath id="pc"><rect x="8" y="8" width="{W - 16}" height="{H - 16}"/></clipPath>'
    return svg(W, H, body, css, defs=clip, label="Footer: three kawaii cats walking across a flowery hill under pastel bunting")


def divider():
    W, H = 960, 24
    body = ""
    for i, x in enumerate(range(12, W, 48)):
        if i % 2:
            body += heart(x, 6, 2, [PINK, LAV, MINT_D][i % 3], f'class="t{i % 4}"')
        else:
            body += sprite(FLOWER, {"p": [PINK_L, BUT, LAV][i % 3], "y": BUT_D}, x, 4, 4)
    return svg(W, H, body, TWINKLE, label="divider")


if __name__ == "__main__":
    save("banner_day.svg", banner(False))
    save("banner_night.svg", banner(True))
    save("typing.svg", typing())
    for i, k in enumerate(BUTTONS):
        save(f"btn_{k}.svg", button(k, i))
    save("player.svg", player())
    save("inventory.svg", inventory())
    for k in ("dinocat", "snek"):
        save(f"icon_{k}.svg", icon(k))
    save("parade.svg", parade())
    save("divider.svg", divider())
