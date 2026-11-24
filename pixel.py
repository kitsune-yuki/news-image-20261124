#!/usr/bin/env python3
"""Draw the lead illustration as pixel art and save it as scene.png.

The scene is Benghazi harbour at dusk on 24 November 2026: a Russian
corvette, hit by Ukrainian naval drones, listing and burning at its
berth while the drones race away across the water. It is drawn on a
tiny 234x48 grid, one pixel at a time, with a small dusk palette, then
scaled up with NEAREST so every pixel stays crisp. Deterministic: a
fixed seed, no network, no clock.

Run:  python3 pixel.py
Writes scene.png beside this file: 936x192.
"""
import random

from PIL import Image, ImageDraw

GW, GH = 234, 48
PX = 4

INDIGO = (20, 26, 58)
VIOLET = (52, 44, 92)
MAGENTA = (118, 58, 104)
EMBER = (214, 104, 54)
HORIZON = (255, 146, 52)
SUN = (255, 222, 128)
GLOW = (255, 158, 62)
SEA_TOP = (56, 98, 128)
SEA_MID = (38, 70, 102)
SEA_DEEP = (12, 28, 50)
FOAM = (158, 204, 232)
WAKE = (220, 236, 244)
CLOUD_D = (32, 36, 60)
CLOUD_L = (44, 46, 74)
ROCK = (24, 30, 44)
CRANE = (16, 20, 34)
STEEL = (96, 104, 116)
STEEL_D = (58, 64, 76)
STEEL_L = (150, 158, 168)
HULL_D = (44, 50, 60)
HULL_L = (84, 90, 100)
DECK = (120, 116, 106)
RUST = (150, 76, 34)
WIN_LIT = (255, 214, 104)
WIN_DARK = (22, 34, 50)
FUNNEL = (168, 52, 40)
BLACK = (14, 14, 14)
SMOKE_D = (30, 30, 32)
SMOKE_M = (56, 56, 58)
SMOKE_L = (88, 88, 90)
SMOKE_T = (124, 124, 126)
FLAME_D = (255, 88, 0)
FLAME_M = (255, 152, 30)
FLAME_L = (255, 208, 58)
FLAME_W = (255, 248, 208)


def main():
    img = Image.new("RGB", (GW, GH), INDIGO)
    d = ImageDraw.Draw(img)
    rnd = random.Random(7)

    def px(x, y, c):
        if 0 <= x < GW and 0 <= y < GH:
            img.putpixel((x, y), c)

    def band(y0, y1, c):
        d.rectangle([0, y0, GW - 1, y1], fill=c)

    def dither(y, c1, c2):
        for x in range(GW):
            px(x, y, c1 if (x + y) % 2 == 0 else c2)

    # Sky: indigo at the top, violet, magenta, ember, amber horizon.
    band(0, 4, INDIGO)
    band(5, 9, VIOLET)
    dither(9, VIOLET, MAGENTA)
    band(10, 14, MAGENTA)
    dither(14, MAGENTA, EMBER)
    band(15, 18, EMBER)
    dither(18, EMBER, HORIZON)
    band(19, 20, HORIZON)

    # Sun low on the right, half sunk behind the smoke.
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            if abs(dx) + abs(dy) <= 8:
                px(198 + dx, 14 + dy, GLOW)
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            if abs(dx) + abs(dy) <= 5:
                px(198 + dx, 14 + dy, SUN)
    px(198, 14, FLAME_W)

    # Dark clouds with dithered edges.
    for cx, cy, rx, ry, c in [
        (48, 5, 24, 3, CLOUD_D), (120, 4, 28, 3, CLOUD_L),
        (170, 7, 18, 2, CLOUD_D), (24, 8, 14, 2, CLOUD_L),
        (88, 8, 20, 2, CLOUD_D),
    ]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c)
    for _ in range(36):
        x = rnd.randint(0, GW - 1)
        y = rnd.randint(2, 10)
        px(x, y, CLOUD_D if (x + y) % 2 else VIOLET)

    # Birds over the harbour.
    for bx, by in [(60, 5), (66, 4), (150, 6)]:
        px(bx, by, BLACK)
        px(bx + 1, by + 1, BLACK)
        px(bx + 2, by, BLACK)

    # Breakwater rocks on the left, with a small lighthouse.
    for x in range(0, 30):
        h = 20 - (x % 5) // 2
        for y in range(h, 21):
            px(x, y, ROCK)
    d.rectangle([10, 12, 15, 20], fill=(226, 220, 204))
    d.rectangle([10, 12, 15, 13], fill=(178, 34, 34))
    d.rectangle([11, 10, 14, 11], fill=BLACK)
    px(12, 9, WIN_LIT)
    px(13, 9, WIN_LIT)
    # Lighthouse beam sweeping right across the dusk.
    for i in range(1, 26):
        px(16 + i, 9 + i // 6, WIN_LIT if i % 3 else FLAME_L)

    # Port cranes silhouetted on the right horizon.
    for cx in (216, 226):
        d.rectangle([cx, 10, cx + 1, 20], fill=CRANE)
        for i in range(9):
            px(cx + 2 + i, 11 - i // 2, CRANE)
        px(cx + 10, 6, CRANE)
    d.rectangle([206, 18, 232, 20], fill=ROCK)

    # A distant freighter on the horizon.
    d.rectangle([176, 19, 190, 20], fill=(13, 22, 36))
    px(180, 18, (13, 22, 36))
    px(185, 17, (13, 22, 36))

    # Sea: three bands, darker toward the bottom, with wave flecks.
    band(21, 26, SEA_TOP)
    band(27, 35, SEA_MID)
    band(36, GH - 1, SEA_DEEP)
    for _ in range(140):
        x = rnd.randint(0, GW - 1)
        y = rnd.randint(22, 46)
        px(x, y, FOAM)
        if rnd.random() < 0.5:
            px(x + 1, y, FOAM)

    # Naval drones racing in from the left, low wakes behind them.
    for dx, dy in [(28, 40), (44, 42), (58, 39)]:
        d.rectangle([dx, dy, dx + 3, dy + 1], fill=BLACK)
        px(dx + 1, dy - 1, STEEL_D)
        for i in range(1, 9):
            px(dx - i, dy + 1, WAKE if i % 2 else FOAM)
            if i % 3 == 0:
                px(dx - i, dy + 2, FOAM)

    # The corvette, listing to starboard: bow rides high on the left,
    # stern settles low on the right. Each hull row steps down.
    hull_rows = [
        (30, 74, 158), (31, 74, 160), (32, 75, 162), (33, 76, 164),
        (34, 78, 166), (35, 80, 168), (36, 84, 168), (37, 90, 166),
        (38, 100, 162),
    ]
    for y, x0, x1 in hull_rows:
        c = HULL_L if y <= 32 else (HULL_D if y <= 35 else (30, 34, 42))
        d.rectangle([x0, y, x1, y], fill=c)
    # Deck line, sloping with the list.
    for x in range(74, 160):
        px(x, 29 + (x - 74) // 60, DECK)
    # Rust streaks down the hull.
    for sx in (88, 118, 148):
        for y in range(32, 37):
            if (y + sx) % 2 == 0:
                px(sx, y, RUST)
    # Foam where the bow meets the water, spray at the stern.
    for x in (74, 75, 158, 159, 160):
        px(x, 38, WAKE)
    for x in range(76, 156, 8):
        px(x, 39, FOAM)
    for sx, sy in [(164, 37), (166, 36), (162, 39), (168, 38)]:
        px(sx, sy, WAKE)

    # Bridge tower with lit and dark windows, leaning with the ship.
    d.rectangle([96, 23, 112, 28], fill=STEEL_L)
    d.rectangle([96, 28, 112, 28], fill=STEEL_D)
    for wx in (98, 102, 106, 110):
        px(wx, 25, WIN_LIT if wx % 8 == 2 else WIN_DARK)
        px(wx, 27, WIN_DARK if wx % 8 == 2 else WIN_LIT)
    # Mast, tilted by the list, radar turning.
    for i in range(6):
        px(118 + i, 23 - i, STEEL_D)
    px(124, 17, STEEL_D)
    px(125, 17, STEEL_D)
    px(123, 16, WIN_LIT)
    # Funnel with a red band.
    d.rectangle([128, 25, 134, 28], fill=FUNNEL)
    d.rectangle([128, 25, 134, 25], fill=BLACK)
    # Gun turret forward, barrel pointing left.
    d.rectangle([80, 27, 88, 29], fill=STEEL_D)
    for i in range(6):
        px(79 - i, 28, STEEL_D)

    # Fire: layered flames over the midships deck, with glow.
    for dx in range(-16, 17):
        for dy in range(-9, 10):
            if abs(dx) + abs(dy) <= 15 and rnd.random() < 0.5:
                px(146 + dx, 24 + dy, FLAME_M)
    for dx, dy in [(0, 0), (-2, 1), (2, 1), (-4, 2), (4, 2), (-1, -2),
                   (1, -2), (-3, -1), (3, -1), (0, 2), (-5, 3), (5, 3),
                   (-6, 1), (6, 1), (-2, -3), (2, -3), (0, -4)]:
        px(146 + dx, 25 + dy, FLAME_D)
    for dx, dy in [(0, 1), (-2, 2), (2, 2), (0, -1), (-1, 0), (1, 0),
                   (-3, 1), (3, 1), (0, 3)]:
        px(146 + dx, 27 + dy, FLAME_L)
    for dx, dy in [(0, 0), (-1, 1), (1, 1), (0, 2), (-1, 0), (1, 0)]:
        px(146 + dx, 28 + dy, FLAME_W)
    # Warm rim light from the fire along the deck edge.
    for x in range(120, 158, 2):
        px(x, 29 + (x - 74) // 60, FLAME_M)

    # Smoke: a thick column rising from the fire, drifting left.
    for cx, cy, rx, ry, c in [
        (146, 20, 9, 6, SMOKE_D), (142, 16, 10, 6, SMOKE_D),
        (137, 12, 11, 6, SMOKE_M), (131, 8, 10, 5, SMOKE_M),
        (125, 4, 9, 4, SMOKE_L), (119, 1, 7, 3, SMOKE_L),
        (144, 18, 5, 3, SMOKE_M), (138, 14, 5, 3, SMOKE_L),
        (132, 10, 4, 3, SMOKE_T), (126, 6, 4, 2, SMOKE_T),
    ]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c)
    for _ in range(60):
        x = rnd.randint(108, 162)
        y = rnd.randint(0, 20)
        if rnd.random() < 0.6:
            px(x, y, SMOKE_T if rnd.random() < 0.5 else SMOKE_L)
    # Orange rim light on the smoke, on the side facing the fire.
    for x, y in [(150, 20), (151, 18), (149, 16), (147, 14), (145, 12),
                 (152, 22), (150, 24), (143, 10), (141, 8)]:
        px(x, y, FLAME_M if (x + y) % 2 else FLAME_D)

    # Fire reflection on the water, fading downward.
    for y in range(31, 47):
        for x in range(132, 162):
            if rnd.random() < max(0.2, 0.85 - (y - 31) * 0.06):
                px(x, y, FLAME_M if (x + y) % 3 else FLAME_D)

    big = img.resize((GW * PX, GH * PX), Image.NEAREST)
    big.save("scene.png", format="PNG", optimize=True)
    print("wrote scene.png", big.size)


if __name__ == "__main__":
    main()
