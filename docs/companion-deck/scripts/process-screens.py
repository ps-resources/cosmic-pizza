#!/usr/bin/env python3
"""Crop raw browser screenshots into the deck's shot files.

Reads assets/screens/unedited/*.png (full Safari window captures), crops the
region each slide needs, and writes assets/screens/shot-*.png (and .gif for
two-state shots). Originals are never modified.

Crop boxes are in the coordinates of a 2000 px wide preview of the capture, so
they scale automatically for other capture widths.
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
RAW = HERE / "assets/screens/unedited"
OUT = HERE / "assets/screens"
BG = (34, 39, 48)  # GitHub dark page background
RATIO = 1.9  # target frame ratio of the slide's screenshot area
HOLD_MS = 2400

# shot name -> list of (raw file, crop box x0, y0, x1, y1). Two entries make a GIF.
SHOTS = {
    "shot-01-enable-settings": [("01.png", (670, 205, 1605, 735))],
    "shot-02-standard-findings": [
        ("02a.png", (515, 205, 1785, 800)),
        ("02b.png", (390, 205, 1595, 725)),
    ],
    "shot-03-ai-findings": [("03.png", (515, 205, 1785, 735))],
    "shot-04-pr-inline-findings": [("04.png", (1190, 285, 1870, 800))],
    "shot-05-pr-coverage-comment": [("05.png", (390, 370, 1255, 770))],
    "shot-06-ruleset-settings": [
        ("06a.png", (685, 385, 1595, 880)),
        ("06b.png", (685, 385, 1595, 880)),
    ],
    "shot-07-org-dashboard": [("07.png", (495, 385, 1490, 900))],
    "shot-08-assign-to-copilot": [
        ("8a.png", (390, 430, 1265, 975)),
        ("8b.png", (1210, 295, 1850, 745)),
    ],
}


def crop(raw, box):
    im = Image.open(RAW / raw).convert("RGB")
    k = im.width / 2000.0
    return im.crop(tuple(round(v * k) for v in box))


def letterbox(frames):
    w = max(f.width for f in frames)
    h = max(f.height for f in frames)
    cw, ch = w, max(h, round(w / RATIO))
    cw = max(cw, round(ch * RATIO))
    out = []
    for f in frames:
        s = min(cw / f.width, ch / f.height, 1.2)
        g = f.resize((round(f.width * s), round(f.height * s)), Image.LANCZOS) if s != 1 else f
        canvas = Image.new("RGB", (cw, ch), BG)
        canvas.paste(g, ((cw - g.width) // 2, (ch - g.height) // 2))
        out.append(canvas)
    return out


for name, parts in SHOTS.items():
    frames = [crop(raw, box) for raw, box in parts]
    if len(frames) == 1:
        frames[0].save(OUT / f"{name}.png", optimize=True)
        print(name, ".png", frames[0].size)
        continue
    boxed = letterbox(frames)
    boxed[0].save(OUT / f"{name}.png", optimize=True)  # static fallback = first state
    pal = [f.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.NONE) for f in boxed]
    pal[0].save(OUT / f"{name}.gif", save_all=True, append_images=pal[1:],
                duration=HOLD_MS, loop=0, optimize=True, disposal=2)
    print(name, ".png + .gif", boxed[0].size)
