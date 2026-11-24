#!/usr/bin/env python3
"""Compose the front page (entry.png) from the pixel-art scene and
the 24 November 2026 news summary.

Run:  python3 pixel.py && python3 compose.py
Writes entry.png beside this file: 1024x1024, deterministic, no
network, no clock, no randomness. Uses only Pillow and the DejaVu
fonts already on this machine; the entry program (main.py) only
copies the finished image, so the grader needs neither.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (248, 243, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
CARD = (255, 255, 255)
GREY = (90, 86, 78)
BODY_INK = (40, 38, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS_PLAIN = FONT_DIR + "DejaVuSans.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def flow_text(draw, text, fnt, width):
    """Break text into lines that fit width, honouring \n breaks."""
    out = []
    for chunk in text.split("\n"):
        words, line = chunk.split(), ""
        for w in words:
            trial = (line + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    out.append(line)
                line = w
        if line:
            out.append(line)
    return out


def draw_para(draw, pos, text, fnt, width, fill=INK, leading=1.28):
    x, y = pos
    for line in flow_text(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def panel(draw, box, accent):
    draw.rectangle(box, fill=CARD, outline=INK, width=2)
    draw.rectangle([box[0], box[1], box[2], box[1] + 8], fill=accent)


def panel_story(draw, box, kicker, headline, body, accent):
    x0, y0, x1, _y1 = box
    panel(draw, box, accent)
    draw.text((x0 + 16, y0 + 14), kicker, font=load(SANS_BOLD, 16),
              fill=accent)
    y = draw_para(draw, (x0 + 16, y0 + 38), headline,
                  load(SERIF_BOLD, 23), x1 - x0 - 32, leading=1.1)
    draw_para(draw, (x0 + 16, y + 6), body, load(SANS_PLAIN, 15),
              x1 - x0 - 32, fill=BODY_INK, leading=1.25)


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)
    d.rectangle([4, 4, PAGE_W - 5, PAGE_H - 5], outline=INK, width=4)

    # Masthead.
    d.rectangle([10, 10, PAGE_W - 11, 138], fill=INK)
    d.text((PAGE_W // 2, 26), "THE WORLD IN ONE DAY",
           font=load(SERIF_BOLD, 56), fill=(255, 255, 255), anchor="ma")
    d.text((PAGE_W // 2, 96), "ONE IMAGE  •  THE WHOLE DAY'S NEWS",
           font=load(SANS_BOLD, 20), fill=(240, 200, 60), anchor="ma")

    # The date, big and red, so the day is unmistakable.
    d.text((PAGE_W // 2, 152), "TUESDAY  24  NOVEMBER  2026",
           font=load(SERIF_BOLD, 36), fill=RED, anchor="ma")
    d.line([60, 200, 320, 200], fill=INK, width=2)
    d.line([704, 200, 964, 200], fill=INK, width=2)

    # Lead story: the pixel-art illustration of the burning corvette.
    lead = (28, 216, 996, 568)
    panel(d, lead, RED)
    scene = Image.open("scene.png").convert("RGB")
    page.paste(scene, (44, 232))
    d.rectangle([44, 394, 396, 424], fill=(10, 20, 35))
    d.text((56, 400), "BENGHAZI, LIBYA  •  MEDITERRANEAN",
           font=load(SANS_BOLD, 17), fill=(255, 255, 255))
    d.text((46, 448), "LEAD  •  A NEW FRONT IN THE MED",
           font=load(SANS_BOLD, 20), fill=RED)
    d.text((46, 478), "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
           font=load(SERIF_BOLD, 30), fill=INK)
    draw_para(d, (46, 514),
              "Kyiv says seven naval drones sank the Russian corvette "
              "Merkury at Benghazi. Moscow vows “painful consequences”; "
              "the UN warns Libya must not become a battleground.",
              load(SANS_PLAIN, 18), 920, fill=BODY_INK, leading=1.25)

    # Four supporting stories in a 2x2 grid.
    gx, gy, gw, gh, gap = 28, 584, 474, 148, 20
    grid = [
        ("RUSSIA  •  NATO",
         "MOSCOW WARNS ESTONIA\nOF “OPEN WAR”",
         "Moscow summons Estonia’s envoy after Tallinn says it will "
         "shut its Russian border from 1 December. NATO counts 25 "
         "airspace violations this year.",
         RED),
        ("THE GULF",
         "BAHRAIN HIT AGAIN AS\nTANKER ATTACKS RISE",
         "Bahrain’s defences intercept fresh Iranian projectiles. "
         "Trump warns Tehran of a “very traumatic” outcome if no "
         "nuclear deal is reached.",
         NAVY),
        ("CLIMATE  •  COP31",
         "AFTER THE COLLAPSE,\nTHE BLAME GAME",
         "COP31 in Antalya ended with no deal after a record 50 "
         "hours of overtime; 90+ nations rejected a text that never "
         "named fossil fuels.",
         RED),
        ("TECH",
         "HUANG IS BACK\nAT NVIDIA",
         "Jensen Huang is reinstated as Nvidia chief after Trump "
         "steps in. SK hynix jumps 20%; U.S. lawmakers push new "
         "China chip curbs.",
         NAVY),
    ]
    for i, (kicker, head, body, accent) in enumerate(grid):
        box = (gx + (i % 2) * (gw + gap), gy + (i // 2) * (gh + gap),
               gx + (i % 2) * (gw + gap) + gw,
               gy + (i // 2) * (gh + gap) + gh)
        panel_story(d, box, kicker, head, body, accent)

    # Also-today strip.
    also = (28, 908, 996, 988)
    panel(d, also, NAVY)
    d.text((46, 920), "ALSO TODAY", font=load(SANS_BOLD, 19), fill=NAVY)
    draw_para(d, (46, 944),
              "Israeli strikes in Gaza kill three, including a UN worker  •  "
              "Thai–Cambodia truce holds  •  "
              "Trump unveils Indonesia trade deal as the EU readies $84bn "
              "in tariffs",
              load(SANS_PLAIN, 17), 932, fill=BODY_INK, leading=1.3)

    d.text((PAGE_W // 2, 996), "SUMMED UP IN ONE IMAGE  •  24 NOVEMBER 2026",
           font=load(SANS_BOLD, 17), fill=GREY, anchor="ma")

    page.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
