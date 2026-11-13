"""PT 노트 식단 탭 그림 (2026-11-05)
python3 make_diet_web.py   → assets/food/<음식>.png (공통) + assets/food/M|F/ic_<끼니>.png (테마색)
음식 그림은 make_food.py(종이 식단표와 같은 그림), 끼니 아이콘은 종이 식단표 make_assets.py의 함수와 같음"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_food as mf

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "food")
SIZE = 160
ORANGE = (242, 162, 58)
AMBER = (217, 140, 30)
GREY = (138, 148, 163)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _canvas(n=256, S=4):
    return Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0)), S, n * S


def _finish(img, S, path):
    img = img.resize((img.width // S, img.height // S), Image.LANCZOS)
    img.resize((SIZE, SIZE), Image.LANCZOS).save(path, optimize=True)


def _dot(d, p, w, col):
    d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=col)


def _stroke(d, pts, w, col):
    d.line(pts, fill=col, width=int(w), joint="curve")
    _dot(d, pts[0], w, col)
    _dot(d, pts[-1], w, col)


def ic_sun(path, theme):
    img, S, N = _canvas()
    d = ImageDraw.Draw(img)
    c = N / 2
    for k in range(8):
        a = k * np.pi / 4
        p1 = (c + np.cos(a) * N * 0.30, c + np.sin(a) * N * 0.30)
        p2 = (c + np.cos(a) * N * 0.43, c + np.sin(a) * N * 0.43)
        _stroke(d, [p1, p2], N * 0.07, ORANGE)
    r = N * 0.21
    d.ellipse((c - r, c - r, c + r, c + r), fill=ORANGE)
    _finish(img, S, path)


def ic_moon(path, theme):
    img, S, N = _canvas()
    m = Image.new("L", img.size, 0)
    dm = ImageDraw.Draw(m)
    dm.ellipse((N * 0.14, N * 0.12, N * 0.80, N * 0.78), fill=255)
    dm.ellipse((N * 0.34, N * 0.02, N * 0.98, N * 0.62), fill=0)
    img.paste(Image.new("RGBA", img.size, hex2rgb(theme) + (255,)), (0, 0), m)
    d = ImageDraw.Draw(img)
    cx, cy, r = N * 0.76, N * 0.74, N * 0.09
    pts = []
    for k in range(10):
        a = -np.pi / 2 + k * np.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + np.cos(a) * rr, cy + np.sin(a) * rr))
    d.polygon(pts, fill=ORANGE)
    _finish(img, S, path)


def _bowl(d, N, body, rice, y_top=0.45):
    d.ellipse((N * 0.20, N * (y_top - 0.17), N * 0.80, N * (y_top + 0.15)), fill=rice)
    d.chord((N * 0.10, N * (y_top - 0.30), N * 0.90, N * (y_top + 0.40)), 0, 180, fill=body)
    d.rectangle((N * 0.10, N * y_top, N * 0.90, N * (y_top + 0.05)), fill=body)
    d.rounded_rectangle((N * 0.36, N * (y_top + 0.37), N * 0.64, N * (y_top + 0.45)), radius=N * 0.03, fill=body)


def ic_tray(path, theme):
    img, S, N = _canvas()
    d = ImageDraw.Draw(img)
    _stroke(d, [(N * 0.56, N * 0.08), (N * 0.86, N * 0.40)], N * 0.045, GREY)
    _stroke(d, [(N * 0.66, N * 0.06), (N * 0.92, N * 0.34)], N * 0.045, GREY)
    _bowl(d, N, hex2rgb(theme), (255, 255, 255), 0.47)
    d.ellipse((N * 0.20, N * 0.30, N * 0.80, N * 0.62), outline=hex2rgb(theme), width=int(N * 0.04))
    _finish(img, S, path)


def ic_shaker(path, theme):
    img, S, N = _canvas()
    d = ImageDraw.Draw(img)
    col = hex2rgb(theme)
    d.rounded_rectangle((N * 0.40, N * 0.04, N * 0.60, N * 0.16), radius=N * 0.03, fill=GREY)
    d.rounded_rectangle((N * 0.26, N * 0.14, N * 0.74, N * 0.30), radius=N * 0.05, fill=GREY)
    d.polygon([(N * 0.28, N * 0.30), (N * 0.72, N * 0.30), (N * 0.66, N * 0.94), (N * 0.34, N * 0.94)], fill=col)
    d.rectangle((N * 0.31, N * 0.50, N * 0.69, N * 0.62), fill=(255, 255, 255, 200))
    _finish(img, S, path)


def ic_water(path, theme):
    img, S, N = _canvas()
    d = ImageDraw.Draw(img)
    col = (91, 141, 214)
    cx = N * 0.5
    d.polygon([(cx, N * 0.06), (N * 0.22, N * 0.56), (N * 0.78, N * 0.56)], fill=col)
    d.ellipse((N * 0.20, N * 0.36, N * 0.80, N * 0.94), fill=col)
    d.arc((N * 0.32, N * 0.50, N * 0.62, N * 0.82), 100, 190, fill=(255, 255, 255), width=int(N * 0.05))
    _finish(img, S, path)


def ic_scale(path, theme):
    img, S, N = _canvas()
    d = ImageDraw.Draw(img)
    col = hex2rgb(theme)
    d.rounded_rectangle((N * 0.08, N * 0.10, N * 0.92, N * 0.92), radius=N * 0.18, fill=col)
    d.chord((N * 0.26, N * 0.22, N * 0.74, N * 0.70), 180, 360, fill=(255, 255, 255))
    _stroke(d, [(N * 0.50, N * 0.46), (N * 0.62, N * 0.32)], N * 0.045, ORANGE)
    _finish(img, S, path)


MEALS = {"sun": ic_sun, "moon": ic_moon, "tray": ic_tray, "shaker": ic_shaker, "water": ic_water, "scale": ic_scale}


def main():
    os.makedirs(ROOT, exist_ok=True)
    for k, fn in mf.FOODS.items():
        p = os.path.join(ROOT, k + ".png")
        fn(p)
        Image.open(p).resize((SIZE, SIZE), Image.LANCZOS).save(p, optimize=True)
    for sex, col in (("M", "#1C1C1E"), ("F", "#A0606A")):
        os.makedirs(os.path.join(ROOT, sex), exist_ok=True)
        for k, fn in MEALS.items():
            fn(os.path.join(ROOT, sex, "ic_" + k + ".png"), col)


if __name__ == "__main__":
    main()
