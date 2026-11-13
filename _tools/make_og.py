"""회원 og.jpg (카톡 미리보기 1200×630) 만들기 — 테마색 배경 + 로고 + 'MY PT NOTE' + 'OOO 회원님' + 아래 띠
python3 _tools/make_og.py m/<주소>/og.jpg "홍길동" M            (여 회원은 F, 그룹 PT는 이름에 "A · B")
트레이너·센터 이름은 assets/site.js 에서 읽음. 테마 색은 아래 THEME (테마를 바꾸면 여기도)"""
import os, re, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
F_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
F_BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
# (배경, 아래 띠, 작은 글씨, 금색 줄)
THEME = {"M": ("#1C1C1E", "#0B0B0C", "#CFC3A1", "#C9A227"),
         "F": ("#A0606A", "#6E3C45", "#F7DDE0", "#E3C568")}


def site_info():
    t = open(os.path.join(ROOT, "assets", "site.js"), encoding="utf-8").read()
    g = lambda k, d: (re.search(k + r'\s*:\s*"([^"]*)"', t) or [None, d])[1]
    return g("trainer", "OOO"), g("brand", "GYMTOS"), g("branch", "")


def font(p, s):
    return ImageFont.truetype(p, s, index=1)


def make(out, name, sex="M", title=None):
    bg, band, sub, gold = THEME["F" if sex == "F" else "M"]
    trn, brand, branch = site_info()
    W, H, S = 1200, 630, 2
    img = Image.new("RGB", (W * S, H * S), bg)
    d = ImageDraw.Draw(img)
    logo = Image.open(os.path.join(ROOT, "assets", "logo.png")).convert("RGBA")
    lh = 52 * S
    logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
    img.paste(logo, (80 * S, 68 * S), logo)
    group = "·" in name
    d.text((82 * S, 232 * S), "MY PT NOTE · " + ("함께하는 그룹 PT 노트" if group else "나만의 운동 노트"), font=font(F_BOLD, 34 * S), fill=sub)
    title = title or (name.replace(" · ", "·") + " 회원님")
    fs = 84
    while fs > 48 and d.textlength(title, font=font(F_BLACK, fs * S)) > (W - 160) * S:
        fs -= 4
    d.text((78 * S, 300 * S), title, font=font(F_BLACK, fs * S), fill="#FFFFFF")
    d.rectangle((80 * S, 452 * S, 200 * S, 458 * S), fill=gold)
    d.rectangle((0, 540 * S, W * S, H * S), fill=band)
    d.text((82 * S, 566 * S), f"{brand}{(' ' + branch) if branch else ''} · 담당 {trn} 트레이너", font=font(F_BOLD, 28 * S), fill=sub)
    img.resize((W, H), Image.LANCZOS).save(out, quality=88, optimize=True)


if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "홍길동", sys.argv[3] if len(sys.argv) > 3 else "M", sys.argv[4] if len(sys.argv) > 4 else None)
    # 앱에서 추가한 회원 공용(n/og.jpg): python3 _tools/make_og.py n/og.jpg - M "회원님 PT 노트"
