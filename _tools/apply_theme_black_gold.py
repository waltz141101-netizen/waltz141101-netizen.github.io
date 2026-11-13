"""블랙+골드 테마 적용 (처음 세팅 5단계) — 원래 키트 색(남 네이비 #1F3864 / 여 핑크 #C2185B)을 한 번에 바꿈
남 = 블랙 + 골드, 여 = 로즈골드 + 블랙 포인트.  python3 _tools/apply_theme_black_gold.py  (사이트 폴더에서, 한 번만)"""
import os, re, sys, glob

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
COACH = [d for d in glob.glob(os.path.join(ROOT, "coach-*")) if os.path.isdir(d)][0]

# 모든 파일 공통: 네이비 → 블랙, 분홍 포인트 → 골드
BRAND = {
    "1F3864": "1C1C1E", "17294B": "0F0F10", "0F1B33": "121212",
    "22406F": "2C2C2E", "0F1D38": "101011", "1C2F5E": "1E1E20", "24406F": "2E2E30",
    "4C6696": "4A453C", "6582B6": "6B6455", "DCE3F0": "ECE5D3", "E8EDF7": "F3EEE2", "D3DCEC": "E3DBC8",
    "8796B5": "9C9583", "B9C8E6": "CFC3A1",
    "EDF2FA": "F4F0E6", "DCE5F3": "E8DFC9", "D5DCE8": "E0D9C8",
    "C9D2E3": "E3DAC4", "A9B7D2": "D2C39A", "7E92BA": "B9A26A",
    "DB4C8C": "C9A227", "F27BB0": "E3C568", "A0407E": "B08A2A", "E0508F": "D4A72C", "A82E63": "8C6D10",
    "F4B3CE": "EAD89A", "F1B7D1": "EEDFAE", "E57EAC": "DCBB55", "FFD1E4": "FFF0C2", "F7B3D0": "F3E2A8",
    "F3F5F9": "F5F4F0", "E3E6EC": "E6E3DC",
    "0D1424": "0D0D0D", "26385E": "333336", "C9D6F0": "E8DDB8", "0B1322": "0A0A0A", "C9D4EA": "D9CFB2",
    "D3DCEE": "DDD5C2", "E6ECF7": "EEE9DD", "0D1626": "0D0D0D", "2E4E87": "3A3A3D",
}
RGBA = {
    "31,56,100": "28,28,30", "242,123,176": "227,197,104", "219,76,140": "201,162,39",
    "12,20,38": "10,10,10", "15,27,51": "18,18,18", "23,41,75": "15,15,16",
}
# 여 테마(회원 화면·선생님 페이지): 핑크 → 로즈골드
FEMALE = {
    "C2185B": "A0606A", "A3134B": "874C56", "9C1149": "8C505A", "6E0B34": "5E333B", "A8144F": "9A5862",
    "7A0E3A": "1C1C1E", "FCE4EC": "F7ECEC", "F8D3E0": "EFD9DA", "FAD0DF": "F3D6D9", "EBD3DC": "E9D6D6",
}
RGBA_F = {"194,24,91": "160,96,106"}
# PT 안내서(손님에게 보이는 트레이너 소개): 분홍 포인트 칸 → 골드 칸 + 검은 글씨
GUIDE = {"C2185B": "B8922A", "FCE4EC": "F6EDD2", "FFF6FA": "121212", "FFE0EC": "3A2E10"}
RGBA_G = {"194,24,91": "184,146,42"}
# 움직이는 운동 아이콘 타일·기구색
EXI = {"ECEFF5": "F1EEE6", "8792A8": "9A9384", "C5CCDA": "D6D0C2", "FBEAF1": "F8EDED", "A9909C": "AE9A9C", "E3C9D4": "E6D3D4"}


def sub_hex(t, table):
    for a, b in table.items():
        t = re.sub("#" + a + r"(?![0-9a-fA-F])", lambda m: "#" + (b.lower() if any(c.islower() for c in m.group(0)) else b), t, flags=re.I)
    return t


def sub_rgba(t, table):
    for a, b in table.items():
        pat = r"rgba?\(\s*" + r",\s*".join(a.split(",")) + r"(?=\s*[,)])"
        t = re.sub(pat, lambda m: m.group(0).split("(")[0] + "(" + b.replace(",", ", "), t)
    return t


def run(path, *tables, rgba=()):
    p = os.path.join(ROOT, path) if not os.path.isabs(path) else path
    t0 = open(p, encoding="utf-8").read()
    t = t0
    for tb in tables:
        t = sub_hex(t, tb)
    for tb in rgba:
        t = sub_rgba(t, tb)
    if t != t0:
        open(p, "w", encoding="utf-8").write(t)
    print(f"{os.path.relpath(p, ROOT):40s} {'바뀜' if t != t0 else '그대로'}")


# style.css에만 있는 분홍 빛(LED·리포트 칸 글씨 등)
STYLE_EXTRA = {"FF3D8B": "E07A8C", "6B0D35": "5E333B", "FFE0EC": "3A2E10", "FFF4F8": "FFF9E8"}
run("assets/style.css", FEMALE, STYLE_EXTRA, BRAND, rgba=(RGBA_F, RGBA))
run("assets/app.js", FEMALE, BRAND, rgba=(RGBA_F, RGBA))
run("assets/exicons.js", FEMALE, EXI, BRAND)
run(os.path.join(COACH, "index.html"), FEMALE, BRAND, rgba=(RGBA_F, RGBA))
run(os.path.join(COACH, "guide.html"), GUIDE, BRAND, rgba=(RGBA_G, RGBA))
run(os.path.join(COACH, "intro.html"), GUIDE, BRAND, rgba=(RGBA_G, RGBA))
run(os.path.join(COACH, "manifest.webmanifest"), BRAND)
for p in glob.glob(os.path.join(ROOT, "m", "*", "index.html")):
    run(p, FEMALE, BRAND)
# 그림 만드는 도구의 색도 (다시 그릴 때 같은 테마로)
run("_tools/make_food.py", BRAND)
run("_tools/make_diet_web.py", FEMALE, BRAND)
run("_tools/make_musclemap.py", {"B8306F": "8C6D10"}, BRAND)
