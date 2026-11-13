# 식단표 음식 그림 + 양 배지(알약 모양) + 1종 금색 배지
# 사용: python3 make_food.py spec.json  (make_assets.py를 먼저 돌려 sizes.json이 있어야 함)
# 종이 식단표와 같은 코드 (메모리 diet-log-code-2). PT 노트 웹용은 make_diet_web.py가 이 파일의 음식 함수를 씀
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/opentype/noto"
F_BOLD = f"{FONT_DIR}/NotoSansCJK-Bold.ttc"
F_BLACK = f"{FONT_DIR}/NotoSansCJK-Black.ttc"
OUT = (47, 58, 79, 255)
S = 4
N = 256 * S
OW = int(N * 0.022)        # 외곽선 두께


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def new():
    return Image.new("RGBA", (N, N), (0, 0, 0, 0))


def save(img, path):
    img.resize((256, 256), Image.LANCZOS).save(path)


def E(d, box, fill, w=OW):
    d.ellipse([v * N for v in box], fill=fill, outline=OUT, width=w)


def P(d, pts, fill, w=OW):
    pts = [(x * N, y * N) for x, y in pts]
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=OUT, width=w, joint="curve")


def L(d, pts, col=OUT, w=OW):
    pts = [(x * N, y * N) for x, y in pts]
    d.line(pts, fill=col, width=int(w), joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=col)


def RR(d, box, r, fill, w=OW):
    d.rounded_rectangle([v * N for v in box], radius=r * N, fill=fill, outline=OUT, width=w)


def blob(cx, cy, rx, ry, wob=0.06, k=5, seed=0, n=120):
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6.28, 3)
    out = []
    for i in range(n):
        a = i / n * 2 * np.pi
        r = 1 + wob * (np.sin(k * a + ph[0]) * 0.6 + np.sin((k + 2) * a + ph[1]) * 0.4)
        out.append((cx + np.cos(a) * rx * r, cy + np.sin(a) * ry * r))
    return out


def rotate(img, deg):
    return img.rotate(deg, resample=Image.BICUBIC, center=(N / 2, N / 2))


# ---- 탄수화물
def sweet_potato(path):
    img = new(); d = ImageDraw.Draw(img)
    pts = []
    for i in range(80):
        tt = i / 79
        pts.append((0.06 + 0.88 * tt, 0.5 - 0.22 * np.sin(np.pi * tt) ** 0.75))
    for i in range(80):
        tt = 1 - i / 79
        pts.append((0.06 + 0.88 * tt, 0.5 + 0.19 * np.sin(np.pi * tt) ** 0.75))
    P(d, pts, hex2rgb("#A8384F"))
    for x0, y0 in ((0.32, 0.44), (0.50, 0.56), (0.66, 0.42)):
        L(d, [(x0, y0), (x0 + 0.05, y0 - 0.015)], (120, 30, 50, 255), N * 0.016)
    L(d, [(0.93, 0.50), (0.99, 0.47)], OUT, N * 0.02)
    d.ellipse((0.22 * N, 0.40 * N, 0.36 * N, 0.45 * N), fill=(255, 255, 255, 70))
    save(rotate(img, 25), path)


def bowl(d, rice, grain, body="#3E5C9A", band="#2C4475"):
    E(d, (0.18, 0.20, 0.82, 0.62), hex2rgb(rice))
    rng = np.random.default_rng(3)
    for _ in range(14):
        x, y = rng.uniform(0.28, 0.72), rng.uniform(0.27, 0.45)
        d.ellipse((x * N, y * N, (x + 0.035) * N, (y + 0.02) * N), fill=hex2rgb(grain))
    d.chord((0.10 * N, 0.10 * N, 0.90 * N, 0.88 * N), 0, 180, fill=hex2rgb(body), outline=OUT, width=OW)
    L(d, [(0.10, 0.49), (0.90, 0.49)], OUT, OW)
    d.rectangle((0.16 * N, 0.56 * N, 0.84 * N, 0.61 * N), fill=hex2rgb(band))
    RR(d, (0.36, 0.84, 0.64, 0.92), 0.02, hex2rgb(body))


def rice_white(path):
    img = new(); d = ImageDraw.Draw(img); bowl(d, "#FFFFFF", "#E3E7EE"); save(img, path)


def rice_brown(path):
    img = new(); d = ImageDraw.Draw(img); bowl(d, "#E4C99C", "#B88A52", body="#8A6A4A", band="#6E5238"); save(img, path)


def oatmeal(path):
    img = new(); d = ImageDraw.Draw(img)
    L(d, [(0.62, 0.30), (0.88, 0.08)], (160, 168, 182, 255), N * 0.05)
    bowl(d, "#EED9AE", "#C9A56A", body="#F5F4F0", band="#9DB3D6")
    save(img, path)


def potato(path):
    img = new(); d = ImageDraw.Draw(img)
    P(d, blob(0.5, 0.55, 0.36, 0.27, 0.05, 3, 4), hex2rgb("#D8B06A"))
    for x, y in ((0.36, 0.48), (0.55, 0.60), (0.64, 0.45), (0.44, 0.66)):
        d.ellipse((x * N, y * N, (x + 0.035) * N, (y + 0.03) * N), fill=(165, 122, 60, 255))
    d.ellipse((0.28 * N, 0.40 * N, 0.40 * N, 0.46 * N), fill=(255, 255, 255, 80))
    save(img, path)


# ---- 단백질
def chicken(path):
    img = new(); d = ImageDraw.Draw(img)
    P(d, blob(0.5, 0.52, 0.38, 0.22, 0.03, 2, 7), hex2rgb("#F2C39C"))
    for k in range(5):
        x = 0.26 + k * 0.11
        L(d, [(x, 0.62), (x + 0.10, 0.40)], (222, 150, 105, 255), N * 0.022)
    save(rotate(img, 20), path)


def beef(path):
    img = new(); d = ImageDraw.Draw(img)
    P(d, blob(0.5, 0.52, 0.38, 0.26, 0.04, 3, 9), hex2rgb("#C9353F"))
    for pts in (((0.26, 0.48), (0.40, 0.42), (0.52, 0.47)), ((0.50, 0.62), (0.62, 0.56), (0.74, 0.58)),
                ((0.32, 0.62), (0.40, 0.66))):
        L(d, pts, (236, 120, 128, 255), N * 0.022)
    save(rotate(img, -8), path)


def fish(path):
    img = new(); d = ImageDraw.Draw(img)
    P(d, [(0.70, 0.50), (0.94, 0.32), (0.90, 0.50), (0.94, 0.68)], hex2rgb("#7FA3C8"))
    E(d, (0.08, 0.30, 0.78, 0.70), hex2rgb("#A9C4DE"))
    d.arc((0.18 * N, 0.36 * N, 0.40 * N, 0.64 * N), 300, 60, fill=OUT, width=OW)
    E(d, (0.17, 0.43, 0.23, 0.49), OUT, 1)
    for x in (0.46, 0.54, 0.62):
        L(d, [(x, 0.40), (x - 0.03, 0.50), (x, 0.60)], (120, 150, 185, 255), N * 0.016)
    save(img, path)


def egg(path):
    img = new(); d = ImageDraw.Draw(img)
    E(d, (0.52, 0.06, 0.86, 0.50), hex2rgb("#F3E2C2"))
    P(d, blob(0.44, 0.60, 0.36, 0.28, 0.07, 4, 2), hex2rgb("#FFFFFF"))
    E(d, (0.32, 0.48, 0.56, 0.72), hex2rgb("#F7B32B"))
    d.ellipse((0.37 * N, 0.53 * N, 0.44 * N, 0.58 * N), fill=(255, 255, 255, 160))
    save(img, path)


def pork(path):
    img = new(); d = ImageDraw.Draw(img)
    P(d, blob(0.5, 0.52, 0.38, 0.27, 0.04, 3, 5), hex2rgb("#F2AFA8"))
    P(d, blob(0.52, 0.50, 0.22, 0.14, 0.05, 3, 6), hex2rgb("#F8D2CC"), int(OW * 0.6))
    save(rotate(img, 10), path)


def tofu(path):
    img = new(); d = ImageDraw.Draw(img)
    P(d, [(0.18, 0.36), (0.52, 0.50), (0.52, 0.82), (0.18, 0.68)], hex2rgb("#EFEFE6"))
    P(d, [(0.52, 0.50), (0.86, 0.36), (0.86, 0.68), (0.52, 0.82)], hex2rgb("#DCDCCF"))
    P(d, [(0.18, 0.36), (0.52, 0.22), (0.86, 0.36), (0.52, 0.50)], hex2rgb("#FFFFFF"))
    for x, y in ((0.40, 0.33), (0.58, 0.30), (0.54, 0.40)):
        d.ellipse((x * N, y * N, (x + 0.02) * N, (y + 0.012) * N), fill=(205, 205, 192, 255))
    save(img, path)


def shrimp(path):
    img = new(); d = ImageDraw.Draw(img)
    cx, cy, R = 0.50, 0.48, 0.28
    a0, a1 = np.deg2rad(195), np.deg2rad(430)
    ts = np.linspace(0, 1, 90)
    wid = lambda t: 0.22 * (1 - 0.55 * t)
    outer = [(cx + (R + wid(t) / 2) * np.cos(a0 + (a1 - a0) * t), cy + (R + wid(t) / 2) * np.sin(a0 + (a1 - a0) * t)) for t in ts]
    inner = [(cx + (R - wid(t) / 2) * np.cos(a0 + (a1 - a0) * t), cy + (R - wid(t) / 2) * np.sin(a0 + (a1 - a0) * t)) for t in ts[::-1]]
    ae = a1
    ex, ey = cx + R * np.cos(ae), cy + R * np.sin(ae)
    tx, ty = -np.sin(ae), np.cos(ae)
    nx, ny = np.cos(ae), np.sin(ae)
    fan = [(ex - tx * 0.02 + nx * 0.04, ey - ty * 0.02 + ny * 0.04), (ex + tx * 0.13 + nx * 0.11, ey + ty * 0.13 + ny * 0.11),
           (ex + tx * 0.09, ey + ty * 0.09), (ex + tx * 0.13 - nx * 0.11, ey + ty * 0.13 - ny * 0.11),
           (ex - tx * 0.02 - nx * 0.04, ey - ty * 0.02 - ny * 0.04)]
    P(d, fan, hex2rgb("#E8743F"))
    P(d, outer + inner, hex2rgb("#F28C5B"))
    for t in (0.22, 0.38, 0.54, 0.70, 0.84):
        a = a0 + (a1 - a0) * t
        w = wid(t) / 2 * 0.85
        L(d, [(cx + (R - w) * np.cos(a), cy + (R - w) * np.sin(a)), (cx + (R + w) * np.cos(a), cy + (R + w) * np.sin(a))],
          (200, 95, 50, 255), N * 0.014)
    for t in (0.30, 0.45, 0.60):
        a = a0 + (a1 - a0) * t
        r1 = R - wid(t) / 2
        L(d, [(cx + r1 * np.cos(a), cy + r1 * np.sin(a)), (cx + (r1 - 0.06) * np.cos(a + 0.15), cy + (r1 - 0.06) * np.sin(a + 0.15))],
          OUT, N * 0.012)
    a = a0 + 0.06
    hx, hy = cx + (R + 0.03) * np.cos(a), cy + (R + 0.03) * np.sin(a)
    d.ellipse(((hx - 0.022) * N, (hy - 0.022) * N, (hx + 0.022) * N, (hy + 0.022) * N), fill=OUT)
    hx0, hy0 = cx + R * np.cos(a0), cy + R * np.sin(a0)
    L(d, [(hx0, hy0), (hx0 - 0.04, hy0 - 0.20), (hx0 + 0.10, hy0 - 0.30)], OUT, N * 0.011)
    L(d, [(hx0, hy0), (hx0 - 0.10, hy0 - 0.14), (hx0 - 0.06, hy0 - 0.32)], OUT, N * 0.011)
    save(img, path)


# ---- 곁들이·기타
def veg(path):
    img = new(); d = ImageDraw.Draw(img)
    P(d, blob(0.38, 0.42, 0.30, 0.26, 0.10, 7, 1), hex2rgb("#5DBB63"))
    L(d, [(0.30, 0.56), (0.40, 0.36)], (60, 140, 70, 255), N * 0.018)
    E(d, (0.42, 0.42, 0.88, 0.88), hex2rgb("#E5483A"))
    P(d, [(0.58, 0.44), (0.65, 0.38), (0.70, 0.44), (0.76, 0.40), (0.72, 0.48), (0.62, 0.49)], hex2rgb("#4CA654"), int(OW * 0.7))
    d.ellipse((0.52 * N, 0.52 * N, 0.60 * N, 0.58 * N), fill=(255, 255, 255, 120))
    save(img, path)


def shaker(path):
    img = new(); d = ImageDraw.Draw(img)
    RR(d, (0.40, 0.04, 0.60, 0.16), 0.03, hex2rgb("#2C3A55"))
    RR(d, (0.26, 0.14, 0.74, 0.30), 0.05, hex2rgb("#2C3A55"))
    P(d, [(0.28, 0.30), (0.72, 0.30), (0.67, 0.94), (0.33, 0.94)], hex2rgb("#DDE5F1"))
    d.rectangle((0.31 * N, 0.50 * N, 0.69 * N, 0.66 * N), fill=hex2rgb("#3E5C9A"))
    f = ImageFont.truetype(F_BLACK, int(N * 0.09), index=1)
    bb = f.getbbox("PRO")
    d.text((0.5 * N - (bb[0] + bb[2]) / 2, 0.58 * N - (bb[1] + bb[3]) / 2), "PRO", font=f, fill="white")
    save(img, path)


def bagel(path):
    """베이글 (2026-11-05 OO님 식단): 위에서 본 링 + 깨"""
    img = new(); d = ImageDraw.Draw(img)
    P(d, blob(0.5, 0.54, 0.40, 0.34, 0.03, 5, 7), hex2rgb("#D9964A"))
    m = Image.new("L", img.size, 0); dm = ImageDraw.Draw(m)
    dm.polygon([(x * N, y * N) for x, y in blob(0.5, 0.50, 0.34, 0.27, 0.03, 5, 7)], fill=255)
    top = Image.new("RGBA", img.size, hex2rgb("#E8B06A")); img.paste(top, (0, 0), m)
    d = ImageDraw.Draw(img)
    E(d, (0.42, 0.44, 0.58, 0.58), hex2rgb("#B87534"))
    E(d, (0.435, 0.455, 0.565, 0.565), (0, 0, 0, 0), 0)
    d.ellipse((0.44 * N, 0.46 * N, 0.56 * N, 0.56 * N), fill=(0, 0, 0, 0))
    rng = np.random.default_rng(3)
    for _ in range(14):
        a = rng.uniform(0, 6.28); r = rng.uniform(0.15, 0.27)
        x, y = 0.5 + np.cos(a) * r * 1.15, 0.50 + np.sin(a) * r * 0.9
        L(d, [(x - 0.012, y), (x + 0.012, y + 0.006)], hex2rgb("#FFF6E3"), N * 0.018)
    save(img, path)


def carbo(path):
    """카보린 (탄수화물 보충제): 스탠딩 파우치 + CARB 라벨"""
    img = new(); d = ImageDraw.Draw(img)
    P(d, [(0.24, 0.12), (0.76, 0.12), (0.80, 0.90), (0.20, 0.90)], hex2rgb("#F2A23A"))
    d.rectangle((0.26 * N, 0.13 * N, 0.74 * N, 0.20 * N), fill=hex2rgb("#D98C1E"))
    L(d, [(0.25, 0.21), (0.75, 0.21)], OUT, N * 0.014)
    RR(d, (0.28, 0.38, 0.72, 0.66), 0.04, hex2rgb("#FFFFFF"), int(N * 0.014))
    f = ImageFont.truetype(F_BLACK, int(N * 0.12), index=1)
    bb = f.getbbox("CARB")
    d.text((0.5 * N - (bb[0] + bb[2]) / 2, 0.52 * N - (bb[1] + bb[3]) / 2), "CARB", font=f, fill=hex2rgb("#D98C1E"))
    for x in (0.38, 0.5, 0.62):
        d.ellipse(((x - 0.02) * N, 0.74 * N, (x + 0.02) * N, 0.78 * N), fill=(255, 255, 255, 200))
    save(img, path)


def salt(path):
    img = new(); d = ImageDraw.Draw(img)
    RR(d, (0.30, 0.10, 0.70, 0.30), 0.06, hex2rgb("#A8B0BE"))
    for x in (0.40, 0.50, 0.60):
        d.ellipse(((x - 0.02) * N, 0.18 * N, (x + 0.02) * N, 0.22 * N), fill=OUT)
    RR(d, (0.24, 0.28, 0.76, 0.92), 0.10, hex2rgb("#FFFFFF"))
    RR(d, (0.24, 0.52, 0.76, 0.70), 0.0, hex2rgb("#E5483A"), int(OW * 0.8))
    save(img, path)


def talk(path):
    """참고사항 상담: 말풍선 두 개"""
    img = new(); d = ImageDraw.Draw(img)
    RR(d, (0.40, 0.14, 0.94, 0.52), 0.12, hex2rgb("#CFC3A1"))
    P(d, [(0.78, 0.50), (0.86, 0.64), (0.66, 0.50)], hex2rgb("#CFC3A1"))
    RR(d, (0.06, 0.36, 0.64, 0.80), 0.12, hex2rgb("#1C1C1E"))
    P(d, [(0.18, 0.78), (0.14, 0.94), (0.34, 0.78)], hex2rgb("#1C1C1E"))
    for x in (0.20, 0.35, 0.50):
        d.ellipse(((x - 0.035) * N, 0.545 * N, (x + 0.035) * N, 0.615 * N), fill="white")
    save(img, path)


def clipboard(path):
    """참고사항 식단 수정: 클립보드 + 체크 줄"""
    img = new(); d = ImageDraw.Draw(img)
    RR(d, (0.18, 0.12, 0.82, 0.94), 0.08, hex2rgb("#1C1C1E"))
    RR(d, (0.25, 0.22, 0.75, 0.88), 0.04, hex2rgb("#FFFFFF"))
    RR(d, (0.36, 0.06, 0.64, 0.20), 0.04, hex2rgb("#A8B0BE"))
    for y in (0.36, 0.53, 0.70):
        L(d, [(0.31, y), (0.35, y + 0.04), (0.42, y - 0.04)], (46, 139, 87, 255), N * 0.028)
        L(d, [(0.48, y), (0.68, y)], (185, 200, 230, 255), N * 0.03)
    save(img, path)


# ---- 배지
def pill(text, path, fill="#1C1C1E", fg="#FFFFFF", h_px=64):
    """둥근 알약 배지. 돌려주는 값 = [폭pt, 높이pt] — 높이 16pt"""
    sc = 4
    H = h_px * sc
    f = ImageFont.truetype(F_BOLD, int(H * 0.50), index=1)
    bb = f.getbbox(text)
    tw = bb[2] - bb[0]
    W = int(tw + H * 0.95)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), radius=H / 2, fill=hex2rgb(fill))
    d.text(((W - tw) / 2 - bb[0], H / 2 - (bb[1] + bb[3]) / 2), text, font=f, fill=hex2rgb(fg))
    img = img.resize((W // sc, H // sc), Image.LANCZOS)
    img.save(path)
    hp = 16.0
    return [round(img.width / img.height * hp, 2), hp]


def gold_badge(path, text="1종"):
    sc = 4
    n = 128 * sc
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((0, 0, n - 1, n - 1), fill=hex2rgb("#C9961A"))
    f = ImageFont.truetype(F_BLACK, int(n * 0.36), index=1)
    bb = f.getbbox(text)
    d.text((n / 2 - (bb[0] + bb[2]) / 2, n / 2 - (bb[1] + bb[3]) / 2), text, font=f, fill="white")
    img.resize((128, 128), Image.LANCZOS).save(path)


FOODS = {"sweet_potato": sweet_potato, "rice_white": rice_white, "rice_brown": rice_brown, "oatmeal": oatmeal,
         "potato": potato, "chicken": chicken, "beef": beef, "fish": fish, "egg": egg, "pork": pork,
         "tofu": tofu, "shrimp": shrimp, "veg": veg, "shaker": shaker, "salt": salt, "talk": talk, "clipboard": clipboard,
         "bagel": bagel, "carbo": carbo}


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    A = spec["asset_dir"]
    theme = spec["theme_primary"]
    sizes = json.load(open(f"{A}/sizes.json"))
    for k, fn in FOODS.items():
        fn(f"{A}/food_{k}.png")
    pills = {}
    for grp in ("carbs", "prots"):
        for i, it in enumerate(spec[grp]):
            pills[f"{grp}_{i}"] = pill(it["amount"], f"{A}/pill_{grp}_{i}.png", theme)
    for i, it in enumerate(spec.get("extras", [])):
        pills[f"extra_{i}"] = pill(it["tag"], f"{A}/pill_extra_{i}.png", theme)
    gold_badge(f"{A}/gold_1.png")
    sizes["pills"] = pills
    json.dump(sizes, open(f"{A}/sizes.json", "w"))
    print(pills)


if __name__ == "__main__":
    main(sys.argv[1])
