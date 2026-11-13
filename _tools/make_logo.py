import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import uniform_filter1d, gaussian_filter, binary_dilation
F_BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
def font(path, size): return ImageFont.truetype(path, size, index=1)
def make_logo(path, text="GYMTOS"):
    S = 4
    f = font(F_BLACK, 150 * S)
    gap = 14 * S
    widths = [f.getbbox(c)[2] - f.getbbox(c)[0] for c in text]
    pad = 40 * S
    W = sum(widths) + gap * (len(text) - 1) + pad * 2
    H = 260 * S
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    x = pad
    for c, w in zip(text, widths):
        bb = f.getbbox(c)
        d.text((x - bb[0], 20 * S), c, font=f, fill=255)
        x += w + gap
    m = np.asarray(mask, float) / 255.0
    ys, xs = np.nonzero(m > 0.5)
    y0, y1 = ys.min(), ys.max()
    hh = y1 - y0
    rng = np.random.default_rng(11)
    noise = rng.normal(0, 1, (H, W))
    streak = uniform_filter1d(noise, size=121, axis=1)
    streak = gaussian_filter(streak, (0.6, 0))
    streak = (streak - streak.mean()) / (streak.std() + 1e-9)
    yy = (np.arange(H)[:, None] - y0) / max(hh, 1)
    grad = (0.86 - 0.40 * yy
            + 0.20 * np.exp(-((yy - 0.22) / 0.09) ** 2)
            - 0.16 * np.exp(-((yy - 0.58) / 0.07) ** 2)
            + 0.14 * np.exp(-((yy - 0.86) / 0.06) ** 2))
    val = grad + streak * 0.045
    mb = gaussian_filter(m, 3.0 * S / 2)
    gy, gx = np.gradient(mb)
    L = np.array([-0.70, -0.72])
    shade = -(gx * L[0] + gy * L[1])
    val = val + shade * 26
    val = np.clip(val, 0.05, 0.98)
    metal = (val * 255).astype(np.uint8)
    inside = m > 0.02
    outline = binary_dilation(m > 0.5, iterations=5 * S // 2) & ~(m > 0.5)
    shadow = gaussian_filter(binary_dilation(m > 0.5, iterations=4 * S // 2).astype(float), 3 * S)
    shadow = np.roll(np.roll(shadow, 3 * S, axis=0), 3 * S, axis=1)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., 3] = (shadow * 0.30 * 255).astype(np.uint8)
    rgba[outline, 0:3] = 46
    rgba[outline, 3] = 255
    a_m = (np.clip(m, 0, 1) * 255).astype(np.uint8)
    for c in range(3):
        rgba[..., c] = np.where(inside, metal, rgba[..., c])
    rgba[..., 3] = np.maximum(rgba[..., 3], np.where(inside, a_m, 0))
    rgba[outline, 3] = 255
    img = Image.fromarray(rgba, "RGBA")
    bb = img.getbbox()
    img = img.crop((bb[0] - 4, bb[1] - 4, bb[2] + 4, bb[3] + 4))
    img = img.resize((img.width // S * 2, img.height // S * 2), Image.LANCZOS)
    img.save(path)
    return img.size
import sys
print(make_logo(sys.argv[1] if len(sys.argv) > 1 else "assets/logo.png"))
