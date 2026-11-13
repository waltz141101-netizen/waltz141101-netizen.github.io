"""홈 화면 아이콘 — assets/icon.png(회원 노트) · icon-coach-180/192/512.png(선생님 페이지 앱 "PT노트 쌤")
python3 _tools/make_appicon.py   (테마를 바꾸면 BG·GOLD만 고쳐서 다시)"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
F_BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
F_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG, GOLD, GOLD_L = "#1C1C1E", "#C9A227", "#E3C568"


def icon(sub, n=1024):
    img = Image.new("RGB", (n, n), BG)
    d = ImageDraw.Draw(img)
    d.ellipse((n * .1, n * .1, n * .9, n * .9), outline=GOLD, width=int(n * .025))
    f = ImageFont.truetype(F_BLACK, int(n * .36), index=1)
    bb = d.textbbox((0, 0), "PT", font=f)
    d.text((n / 2 - (bb[0] + bb[2]) / 2, n * .46 - (bb[1] + bb[3]) / 2), "PT", font=f, fill="#FFFFFF")
    f2 = ImageFont.truetype(F_BOLD, int(n * .085), index=1)
    bb = d.textbbox((0, 0), sub, font=f2)
    d.text((n / 2 - (bb[0] + bb[2]) / 2, n * .70 - (bb[1] + bb[3]) / 2), sub, font=f2, fill=GOLD_L)
    return img


icon("NOTE").resize((192, 192), Image.LANCZOS).save(os.path.join(ROOT, "icon.png"), optimize=True)
c = icon("COACH")
for s in (180, 192, 512):
    c.resize((s, s), Image.LANCZOS).save(os.path.join(ROOT, f"icon-coach-{s}.png"), optimize=True)
print("ok")
