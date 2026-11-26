#!/usr/bin/env python3
"""Render the 26 November 2026 front page (1024x1024 PNG) with Pillow.

Run at build time only:  python3 tools/draw_frontpage.py
Writes entry.png next to the repository root. main.ts only copies it.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 24, 22)
RED = (178, 34, 28)
NAVY = (28, 42, 66)
RULE = (120, 110, 95)
MUTED = (90, 84, 72)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = font(f"{FD}/DejaVuSerif-Bold.ttf", 76)
SERIF_H = font(f"{FD}/DejaVuSerif-Bold.ttf", 54)
SERIF_S = font(f"{FD}/DejaVuSerif-Bold.ttf", 29)
SANS = font(f"{FD}/DejaVuSans.ttf", 19)
SANS_B = font(f"{FD}/DejaVuSans-Bold.ttf", 20)
SANS_SM = font(f"{FD}/DejaVuSans.ttf", 18)
SANS_XS = font(f"{FD}/DejaVuSans.ttf", 16)
SERIF_I = font(f"{FL}/LiberationSerif-Italic.ttf", 20)
KICK = font(f"{FD}/DejaVuSans-Bold.ttf", 17)


def wrap(draw, text, fnt, width):
    """Greedy word wrap, returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill=INK, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def rule(draw, y, x0=28, x1=W - 28, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_refinery_scene(draw, x0, y0, x1, y1):
    """Dusk refinery under attack: flare flames, smoke, storage tanks."""
    w, h = x1 - x0, y1 - y0
    # sky gradient: deep amber dusk -> dark red horizon
    top = (62, 32, 48)
    mid = (150, 62, 36)
    bot = (214, 116, 44)
    for yy in range(h):
        t = yy / h
        if t < 0.55:
            s = t / 0.55
            c = tuple(int(top[i] + (mid[i] - top[i]) * s) for i in range(3))
        else:
            s = (t - 0.55) / 0.45
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * s) for i in range(3))
        draw.line([(x0, y0 + yy), (x1, y0 + yy)], fill=c)
    # low sun
    cx, cy, r = x0 + int(w * 0.58), y0 + int(h * 0.42), 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(244, 196, 120))
    draw.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], outline=(244, 196, 120), width=2)
    # smoke trail rising from the flare and drifting right
    smoke = (70, 66, 66)
    for i, (sx, sy, sr) in enumerate([(0.66, 0.30, 15), (0.72, 0.26, 19), (0.79, 0.24, 23)]):
        draw.ellipse([x0 + int(w * sx) - sr, y0 + int(h * sy) - sr,
                      x0 + int(w * sx) + sr, y0 + int(h * sy) + sr], fill=smoke)
    # ground
    gy = y0 + int(h * 0.78)
    draw.rectangle([x0, gy, x1, y1], fill=(32, 26, 24))
    # storage tanks (left cluster)
    for tx, tw, th in [(0.04, 0.13, 0.20), (0.19, 0.11, 0.16), (0.31, 0.12, 0.22)]:
        bx0, bx1 = x0 + int(w * tx), x0 + int(w * (tx + tw))
        draw.rectangle([bx0, gy - int(h * th), bx1, gy], fill=(52, 44, 40))
        draw.ellipse([bx0, gy - int(h * th) - 10, bx1, gy - int(h * th) + 10], fill=(74, 62, 54))
    # distillation columns (centre)
    for tx, tw, th in [(0.48, 0.05, 0.42), (0.55, 0.04, 0.34)]:
        bx0, bx1 = x0 + int(w * tx), x0 + int(w * (tx + tw))
        draw.rectangle([bx0, gy - int(h * th), bx1, gy], fill=(44, 38, 36))
        draw.polygon([(bx0, gy - int(h * th)), (bx1, gy - int(h * th)),
                      ((bx0 + bx1) / 2, gy - int(h * th) - 18)], fill=(44, 38, 36))
    # flare stack (right of centre) with flame
    fx = x0 + int(w * 0.66)
    stack_top = gy - int(h * 0.52)
    draw.rectangle([fx - 5, stack_top, fx + 5, gy], fill=(40, 34, 32))
    for k, (fr, col) in enumerate([(26, (232, 90, 20)), (18, (246, 158, 40)), (10, (252, 214, 90))]):
        draw.polygon([(fx - fr, stack_top + 4), (fx + fr, stack_top + 4),
                      (fx, stack_top - 40 - 8 * k)], fill=col)
    # pipework silhouettes
    draw.rectangle([x0 + int(w * 0.60), gy - 14, x1, gy - 6], fill=(44, 38, 36))
    # oil barrel foreground (left)
    bx, by, bw, bh = x0 + 26, y1 - 74, 46, 64
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(30, 30, 34))
    draw.ellipse([bx, by - 8, bx + bw, by + 8], fill=(58, 58, 64))
    draw.line([(bx, by + 16), (bx + bw, by + 16)], fill=(58, 58, 64), width=3)
    draw.line([(bx, by + 44), (bx + bw, by + 44)], fill=(58, 58, 64), width=3)
    # Brent price chip (top right of the scene), sized to its text
    chip_font = font(f"{FD}/DejaVuSans-Bold.ttf", 20)
    chip_text = "BRENT $94.61  ▲ 3.5%"
    chip_w = int(draw.textlength(chip_text, font=chip_font)) + 28
    chip = (x1 - 16 - chip_w, y0 + 16, x1 - 16, y0 + 60)
    draw.rounded_rectangle(chip, radius=8, fill=(255, 255, 255))
    draw.text((chip[0] + 14, chip[1] + 11), chip_text, font=chip_font, fill=(178, 34, 28))


def story_box(draw, x0, y0, x1, y1, kicker, headline, body, accent=RED):
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    draw.rectangle([x0, y0, x1, y0 + 4], fill=accent)
    draw.text((x0 + 16, y0 + 14), kicker, font=KICK, fill=accent)
    y = y0 + 38
    for line in wrap(draw, headline, SERIF_S, x1 - x0 - 32):
        draw.text((x0 + 16, y), line, font=SERIF_S, fill=INK)
        y += 34
    y += 4
    for line in wrap(draw, body, SANS, x1 - x0 - 32):
        draw.text((x0 + 16, y), line, font=SANS, fill=(52, 48, 42))
        y += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)

    # ---- masthead ----
    centered(d, 34, "THE WORLD TODAY", SERIF_B)
    rule(d, 128, 28, W - 28, 3)
    centered(d, 138, "THURSDAY, 26 NOVEMBER 2026", font(f"{FD}/DejaVuSans-Bold.ttf", 26))
    rule(d, 176, 28, W - 28, 1, RULE)

    # ---- lead story ----
    centered(d, 188, "GULF OIL SHOCK", SERIF_H, fill=RED)
    centered(d, 252, "Houthis claim strike on Saudi Arabia's biggest refinery",
             font(f"{FD}/DejaVuSerif-Bold.ttf", 27))
    draw_refinery_scene(d, 28, 292, W - 28, 560)
    caption = ("Ras Tanura handles 550,000 barrels a day. Riyadh says it shot down four "
               "drones; a second claim hit the capital's financial district.")
    y = 572
    for line in wrap(d, caption, SERIF_I, W - 56):
        d.text((28, y), line, font=SERIF_I, fill=MUTED)
        y += 24
    rule(d, 626, 28, W - 28, 1, RULE)

    # ---- second row ----
    story_box(d, 28, 640, 500, 806, "THE STRAIT",
              "Tankers hit by mines in Hormuz",
              "Two tankers struck in the Strait of Hormuz; "
              "shipping on alert as Gulf tensions spread.")
    story_box(d, 524, 640, 996, 806, "THE TRUCE",
              "Gaza ceasefire under strain",
              "Israel strikes a Hamas official in Gaza; mediators "
              "scramble to save the truce.")

    # ---- third row ----
    story_box(d, 28, 820, 500, 986, "THE WAR",
              "Ukraine hits Russian refineries",
              "Kyiv hits refineries deep in Russia; Putin vows "
              "retaliation as the toll nears 500,000.",
              accent=NAVY)
    story_box(d, 524, 820, 996, 986, "THE TARIFFS",
              "US tariffs: Taiwan faces 15%",
              "Washington unveils tariffs for 14 partners; "
              "markets slide on the eve of Thanksgiving.",
              accent=NAVY)

    out = os.path.join(ROOT, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
