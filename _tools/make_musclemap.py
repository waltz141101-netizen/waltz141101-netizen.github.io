"""PT 노트 '이번 달 근육 지도' 그림 (2026-11-08)

인체모형 v3(anatomy_v3.py)로 바탕 그림 1장 + 부위별 덧칠 그림 8장을 만든다.
덧칠 그림은 투명 PNG(그 부위만 진핑크 #C9A227)라서, 화면에서 겹쳐 놓고
투명도(1~2회 .4 / 3~4회 .72 / 5회 이상 1)로 진하기를 바꾼다.

    python3 _tools/make_musclemap.py          → assets/muscle/M|F/base.png, <부위>.png
"""
import os, sys
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
import anatomy_v3 as A

PINK, PINK_E = "#C9A227", "#8C6D10"
A.EDGE[PINK] = PINK_E
A.LAYER[PINK] = 3.4

# 부위 → (앞모습, 뒷모습) 근육 이름
GROUPS = {
    "chest":    (["pec"], []),
    "shoulder": (["delt_ant", "delt_lat"], ["delt_lat", "delt_post"]),
    "back":     ([], ["lat", "trap", "rhomboid", "teres", "erector"]),
    "arm":      (["biceps", "forearm"], ["triceps", "forearm"]),
    "core":     (["abs", "oblique"], []),
    "thigh":    (["quad", "adductor", "tfl"], ["hamstring", "adductor"]),
    "glute":    ([], ["glute"]),
    "calf":     (["calf"], ["calf"]),
}

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets", "muscle")
DPI = 150


def render(path, front, back, labels):
    fig, ax = plt.subplots(figsize=(5.4, 5.1), dpi=DPI)
    A._draw_view(ax, -2.35, "F", {k: PINK for k in front}, sex)
    A._draw_view(ax, 2.35, "B", {k: PINK for k in back}, sex)
    if labels:
        ax.text(-2.35, -0.62, "앞모습", ha="center", color="#7A756E", fontsize=9)
        ax.text(2.35, -0.62, "뒷모습", ha="center", color="#7A756E", fontsize=9)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-0.9, 7.9)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.subplots_adjust(0, 0, 1, 1)
    plt.savefig(path, facecolor="white")
    plt.close(fig)


for sex in ("M", "F"):
    out = os.path.join(ROOT, sex)
    os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, "_base_nolab.png")
    render(os.path.join(out, "base.png"), [], [], True)
    render(tmp, [], [], False)
    base = np.asarray(Image.open(tmp).convert("RGB")).astype(int)
    for g, (fr, bk) in GROUPS.items():
        t2 = os.path.join(out, "_tmp.png")
        render(t2, fr, bk, False)
        hi = np.asarray(Image.open(t2).convert("RGB")).astype(int)
        diff = np.abs(hi - base).sum(axis=2)
        alpha = np.clip(diff * 3, 0, 255).astype(np.uint8)
        rgba = np.dstack([hi.astype(np.uint8), alpha])
        rgba[alpha == 0, :3] = 0   # 투명한 곳은 색을 비워 용량 줄이기
        Image.fromarray(rgba, "RGBA").quantize(48, method=Image.Quantize.FASTOCTREE) \
            .save(os.path.join(out, g + ".png"), optimize=True)
        os.remove(t2)
    os.remove(tmp)
    # 바탕 그림은 용량을 줄여서
    Image.open(os.path.join(out, "base.png")).convert("RGB").quantize(64).save(os.path.join(out, "base.png"), optimize=True)
    print(sex, "done")
