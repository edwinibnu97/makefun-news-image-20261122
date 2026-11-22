# generate.py — draws entry.png (1024x1024) for make.fun news-image-20261122.
# A front page for Sunday 22 November 2026, rendered with Pillow only.
# No network, no randomness, no clock: running it twice gives identical bytes.
# main.ts ships the resulting file to /output/entry.png.
import math
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

PAGE = (1024, 1024)
BG = (246, 241, 231)
FG = (20, 20, 20)
GREY = (90, 90, 90)
CRIMSON = (180, 35, 24)
DEEP = (11, 42, 74)
AMBER = (232, 193, 90)
WHITE = (255, 255, 255)
EDGE = (200, 192, 175)
SOFT = (40, 40, 40)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def face(filename, px):
    return ImageFont.truetype(os.path.join(FONTS, filename), px)


def serif_b(px):
    return face("DejaVuSerif-Bold.ttf", px)


def sans_b(px):
    return face("DejaVuSans-Bold.ttf", px)


def sans(px):
    return face("DejaVuSans.ttf", px)


def fit_lines(g, text, fnt, width):
    """Greedy word wrap measured with the real font; returns a list of lines."""
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if g.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def spaced(g, x, y, text, fnt, color, gap=2):
    """Draw text with extra tracking between characters."""
    for ch in text:
        g.text((x, y), ch, font=fnt, fill=color)
        x += g.textlength(ch, font=fnt) + gap
    return x


def block(g, x, y, lines, fnt, color, step):
    for ln in lines:
        g.text((x, y), ln, font=fnt, fill=color)
        y += step
    return y


def quad(p0, p1, p2, n=40):
    """Points along a quadratic Bezier curve."""
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((
            (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1],
        ))
    return pts


def glyph_star(g, cx, cy, r):
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=DEEP, width=3)
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = 20 if i % 2 == 0 else 9
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    g.polygon(pts, fill=AMBER, outline=DEEP)


def glyph_tick(g, cx, cy, r):
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=DEEP, width=3)
    g.line([(cx - 14, cy + 1), (cx - 3, cy + 12), (cx + 16, cy - 12)],
           fill=CRIMSON, width=5, joint="curve")


def glyph_ship(g, cx, cy, r):
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=DEEP, width=3)
    g.polygon([(cx - 20, cy - 2), (cx + 20, cy - 2), (cx + 14, cy + 12),
               (cx - 14, cy + 12)], fill=DEEP)
    g.line([(cx, cy - 2), (cx, cy - 18)], fill=DEEP, width=3)
    g.line([(cx, cy - 18), (cx + 10, cy - 14)], fill=CRIMSON, width=3)
    g.line([(cx - 22, cy + 20), (cx - 10, cy + 16), (cx, cy + 20),
            (cx + 10, cy + 16), (cx + 22, cy + 20)], fill=CRIMSON, width=3,
           joint="curve")


def glyph_burst(g, cx, cy, r):
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=DEEP, width=3)
    for k in range(8):
        a = math.radians(k * 45)
        g.line([(cx, cy), (cx + 18 * math.cos(a), cy + 18 * math.sin(a))],
               fill=CRIMSON, width=4)
    g.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=AMBER, outline=DEEP)


STORIES = [
    dict(kicker="CRIME  ·  SINALOA",
         head=("CARTEL KINGPIN CAUGHT", "11 KILLED IN BACKLASH"),
         body="Mexican forces seize 'El Chapo Isidro' in Sinaloa; gunmen "
              "hit back across the north.",
         glyph=glyph_star),
    dict(kicker="TRADE  ·  BRUSSELS",
         head=("EU AND INDONESIA SIGN", "MEGA TRADE DEAL"),
         body="After 10 years of talks: duties scrapped on 98.5% of EU "
              "goods; 600m euros a year saved.",
         glyph=glyph_tick),
    dict(kicker="WAR AT SEA  ·  BALTIC",
         head=("DRONES HIT RUSSIAN", "SHIP IN BALTIC"),
         body="Cargo ship bound for Kaliningrad burns and drifts into "
              "Finnish waters; Kyiv suspected.",
         glyph=glyph_ship),
    dict(kicker="MIDDLE EAST  ·  GULF",
         head=("GULF ON EDGE AS", "IRAN STRIKES SPREAD"),
         body="Iran hits a US base in Kuwait and targets Bahrain; tankers "
              "struck off Oman.",
         glyph=glyph_burst),
]

canvas = Image.new("RGB", PAGE, BG)
g = ImageDraw.Draw(canvas)

# Page frame.
g.rectangle([12, 12, 1011, 1011], outline=DEEP, width=3)

# Masthead.
g.rectangle([24, 24, 999, 118], fill=DEEP)
g.text((44, 38), "THE WORLD TODAY", font=serif_b(52), fill=WHITE)
g.text((999 - 44 - g.textlength("SUNDAY", font=sans_b(24)), 34),
       "SUNDAY", font=sans_b(24), fill=AMBER)
g.text((999 - 44 - g.textlength("22 NOVEMBER 2026", font=sans_b(26)), 62),
       "22 NOVEMBER 2026", font=sans_b(26), fill=WHITE)
g.rectangle([24, 118, 999, 124], fill=CRIMSON)

# Lead story.
g.rectangle([24, 140, 999, 448], fill=WHITE, outline=EDGE, width=2)
g.rectangle([24, 140, 34, 448], fill=CRIMSON)
spaced(g, 56, 158, "LEAD STORY  ·  WAR IN EUROPE", sans_b(19), CRIMSON)
g.text((56, 186), "NATO RALLIES", font=sans_b(54), fill=FG)
g.text((56, 246), "BEHIND POLAND", font=sans_b(54), fill=FG)
lead = ("NATO vows to defend every inch of Polish territory after Russian "
        "missiles hit its soil. Warsaw wants AWACS and F-35s; the "
        "alliance council meets Monday.")
block(g, 56, 312, fit_lines(g, lead, sans(22), 616), sans(22), SOFT, 29)
g.text((56, 404), "WARSAW — No injuries reported.", font=sans(18), fill=GREY)
g.text((56, 426), "UK calls it an 'outrageous provocation'.",
       font=sans(18), fill=GREY)

# Lead artwork: night sky over a skyline, two missile arcs, one burst.
ax0, ay0, ax1, ay1 = 700, 156, 984, 432
g.rectangle([ax0, ay0, ax1, ay1], fill=DEEP)
g.rectangle([ax0, ay1 - 46, ax1, ay1], fill=(7, 28, 52))
for bx, bw, bh in [(0, 34, 26), (44, 26, 38), (80, 40, 20), (130, 30, 32),
                   (170, 36, 24), (216, 28, 36), (254, 28, 22)]:
    g.rectangle([ax0 + bx, ay1 - 46 - bh, ax0 + bx + bw, ay1 - 46],
                fill=(16, 54, 96))
for p0, p1, p2 in [((ax0 + 18, ay1 - 52), (ax0 + 120, ay0 + 60), (ax0 + 238, ay1 - 60)),
                   ((ax0 + 60, ay1 - 52), (ax0 + 170, ay0 + 90), (ax0 + 252, ay1 - 66))]:
    pts = quad(p0, p1, p2)
    g.line(pts, fill=(232, 193, 90, 90), width=7)
    g.line(pts, fill=AMBER, width=3)
    g.ellipse([p2[0] - 5, p2[1] - 5, p2[0] + 5, p2[1] + 5], fill=WHITE)
bx, by = ax0 + 238, ay1 - 60
for k in range(12):
    a = math.radians(k * 30)
    g.line([(bx, by), (bx + 26 * math.cos(a), by + 26 * math.sin(a))],
           fill=(255, 220, 120), width=3)
g.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 240, 180))
g.text((ax0 + 14, ay0 + 10), "POLAND", font=sans_b(22), fill=WHITE)
g.text((ax0 + 14, ay0 + 38), "NATO AIRSPACE", font=sans_b(15),
       fill=(190, 205, 225))

# Four stories in a 2x2 grid.
CW, CH, GX, GY = 472, 172, 24, 468
for i, s in enumerate(STORIES):
    x0 = GX + (i % 2) * (CW + 16)
    y0 = GY + (i // 2) * (CH + 16)
    g.rectangle([x0, y0, x0 + CW, y0 + CH], fill=WHITE, outline=EDGE, width=2)
    s["glyph"](g, x0 + 52, y0 + 52, 34)
    spaced(g, x0 + 100, y0 + 14, s["kicker"], sans_b(14), CRIMSON, 1)
    g.text((x0 + 100, y0 + 34), s["head"][0], font=sans_b(25), fill=FG)
    g.text((x0 + 100, y0 + 64), s["head"][1], font=sans_b(25), fill=FG)
    block(g, x0 + 100, y0 + 98,
          fit_lines(g, s["body"], sans(18), CW - 116)[:3],
          sans(18), SOFT, 24)

# Also-today strip.
g.rectangle([24, 848, 999, 958], fill=DEEP)
g.text((44, 860), "ALSO TODAY", font=sans_b(21), fill=AMBER)
strip = ("COP31 draft text offers decisions, not a new treaty, as talks drag on  ·  "
         "Japan and India agree live-fire training pact  ·  Russia, Ukraine and the "
         "US open trilateral peace talks in Abu Dhabi  ·  TikTok launches a global "
         "deepfake-detection tool")
block(g, 44, 886, fit_lines(g, strip, sans(17), 934)[:3], sans(17),
      (235, 235, 235), 23)

# Footer.
foot = ("World news of Sunday 22 November 2026  ·  As reported by Reuters, AP, "
        "BBC, NYT and Al Jazeera")
g.text(((1024 - g.textlength(foot, font=sans(16))) / 2, 970), foot,
       font=sans(16), fill=GREY)

here = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(here, "entry.png")
canvas.save(target, "PNG", optimize=True, compress_level=9)
print("saved", target, os.path.getsize(target), "bytes", canvas.size)
