"""스미스 머신 아이콘 등 추가분 (2026-11-05, OO·OO 그룹 PT): 스미스 벤치·로우·숄더, 스미스 슈러그, 밴드 푸쉬업
python3 make_icons_smith.py <폴더> "#1F3864"   — make_icons.py와 같은 그림 규칙, 새 아이콘만 저장"""
import sys, math
import make_icons as mi
from make_icons import Canvas, fk, side, draw_side, draw_front, floor, pill, dumbbell, FAR, GRAY, GRAYL, WHITE, LW, TH, SH, FT, UA, FA, NECKH, TORSO
from PIL import Image


def BODYC():
    return mi.BODY


def _bar(c, W):
    c.circle((W[0], W[1] + 1), 6.6, fill=GRAY)
    c.circle((W[0], W[1] + 1), 2.0, fill=WHITE)
    c.stroke([fk(W, 270, 1), fk(W, 90, 2)], LW, mi.BODY)


def smith_bench_press(c):
    S, H = (34, 39), (59, 39)
    K = fk(H, 10, TH)
    A = fk(K, -85, SH)
    floor(c, 21.5, 4, 96)
    c.rrect(10, 31, 66, 35.6, 2.2, fill=GRAY)
    c.stroke([(16, 31), (16, 21.5)], 2.6, GRAY)
    c.stroke([(60, 31), (60, 21.5)], 2.6, GRAY)
    E = fk(S, 92, UA)
    W = fk(E, 90, FA)
    c.stroke([(W[0] - 8, 21.5), (W[0] - 8, 96)], 2.6, GRAYL)
    p = {"H": H, "S": S, "head": fk(S, 180, NECKH), "arm": [E, W], "leg": [K, A, fk(A, 0, FT)]}
    draw_side(c, p)
    _bar(c, W)
    c.arrow((50, 58), (50, 74))


def smith_row(c):
    H = (58, 45)
    K = fk(H, -110, TH)
    A = fk(K, -78, SH)
    S = fk(H, 158, TORSO)
    E = fk(S, -95, UA)
    W = fk(E, -88, FA)
    floor(c, A[1] - 2.6, 8, 92)
    c.stroke([(W[0] + 9, A[1] - 2.6), (W[0] + 9, 96)], 2.6, GRAYL)
    p = {"H": H, "S": S, "head": fk(S, 165, NECKH), "arm": [E, W], "leg": [K, A, fk(A, 180, FT)]}
    draw_side(c, p)
    _bar(c, (W[0], W[1] - 1))
    c.arrow((W[0] - 12, W[1] + 2), (W[0] - 12, W[1] + 17))


def smith_shoulder_press(c):
    c.oy = -4
    H = (56, 30)
    S = fk(H, 90, TORSO)
    floor(c, 6, 14, 86)
    pill(c, (50, 25.4), (68, 25.4), 5.2)
    pill(c, (66, 28), (66, 64), 5.2)
    c.stroke([(60, 25), (60, 6)], 3, GRAY)
    K = fk(H, 180, TH)
    A = fk(K, -90, SH - 1)
    E = fk(S, 128, UA)
    W = fk(E, 78, FA)
    c.stroke([(W[0] - 9, 6), (W[0] - 9, 104)], 2.6, GRAYL)
    p = {"H": H, "S": S, "head": fk(S, 92, NECKH), "arm": [E, W], "leg": [K, A, fk(A, 180, FT)]}
    draw_side(c, p)
    _bar(c, W)
    c.arrow((W[0] - 18, W[1] - 16), (W[0] - 18, W[1] - 1))


def smith_shrug(c):
    # 앞모습, 어깨를 귀 쪽으로 으쓱 (2026-11-05 다시 그림): 레일 2개 + 봉 + 원판, 팔은 쭉 편 채
    floor(c, 5, 6, 94)
    for x in (12, 88):
        c.stroke([(x, 5), (x, 99)], 3.0, GRAYL)
    head = (50, 85)
    Ls, Rs, Lh, Rh = (40.5, 74.5), (59.5, 74.5), (44, 47), (56, 47)
    arms = [((37.4, 59.5), (36.6, 45.2)), ((62.6, 59.5), (63.4, 45.2))]
    legs = [((43.5, 27.5), (43, 9.5), (37.8, 9)), ((56.5, 27.5), (57, 9.5), (62.2, 9))]
    c.stroke([(12, 44), (88, 44)], 3.0, GRAY)
    for x in (21, 79):
        c.rrect(x - 3.2, 33, x + 3.2, 55, 1.6, fill=GRAY)
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    c.arrow((28.5, 66), (28.5, 82))
    c.arrow((71.5, 66), (71.5, 82))


def incline_db_curl(c):
    # 인클라인 벤치에 등 기대고 앉아, 팔을 바닥 쪽으로 쭉 늘어뜨린 데서 감아 올리기 (2026-11-05)
    c.ox, c.oy = -2, 10
    p = side((54, 30), 132, 125, leg=(0, -90, 0))
    S = p["S"]
    floor(c, 6, 8, 88)
    hb, sb = fk(p["H"], 222, 6.6), fk(S, 222, 6.6)
    pill(c, fk(hb, 132, -3), fk(sb, 132, 6), 5.2)
    pill(c, (45, 23.4), (65, 23.4), 5.2)
    c.stroke([(54, 23), (54, 6)], 3, GRAY)
    E = fk(S, -90, UA)
    W = fk(E, -90, FA)
    p["arm"] = [E, W]
    draw_side(c, p)
    dumbbell(c, (W[0], W[1] - 0.8), 0, 12)
    c.arc_arrow(E, 19, -100, -8)


def band_push_up(c):
    # 스쿼트 랙 안전바에 밴드를 걸고, 밴드 끝을 양손에 쥔 채 바닥 푸쉬업 (2026-11-05 다시 그림 — 등에 거는 게 아님)
    c.oy = 6
    fy = 8.4
    W = (66, fy + 1.4)
    E = (66, W[1] + FA)
    S = (66, E[1] + UA)
    A = (12, fy + 4.6)
    ux, uy = A[0] - S[0], A[1] - S[1]
    L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    H = (S[0] + TORSO * ux, S[1] + TORSO * uy)
    K = (H[0] + TH * ux, H[1] + TH * uy)
    T = (16.5, fy + 0.2)
    floor(c, fy - 1.4, 4, 96)
    # 랙 기둥 + 낮게 건 안전바 (머리 앞쪽)
    c.stroke([(95, fy - 1.4), (95, 92)], 3.0, GRAYL)
    c.stroke([(84, fy - 1.4), (84, 92)], 3.0, GRAYL)
    bar = (89, fy + 17)
    c.stroke([(80, bar[1]), (98, bar[1])], 3.4, GRAY)
    # 밴드: 안전바에 감아서 두 가닥이 손으로
    c.stroke([(W[0] + 1.5, W[1] + 1), (bar[0] - 2.4, bar[1] - 1.6)], 2.4, mi.ARROW)
    c.stroke([(W[0] + 2.5, W[1] - 0.5), (bar[0] + 0.6, bar[1] - 2.4)], 2.4, mi.ARROW)
    c.circle(bar, 2.6, outline=mi.ARROW, w=1.8)
    p = {"H": H, "S": S, "head": fk(S, 17, NECKH), "arm": [E, W], "leg": [K, A, T]}
    draw_side(c, p)
    c.circle(W, 2.6, fill=mi.BODY)
    c.arrow((38, 42), (38, 57))


NEW = {"smith_bench_press": smith_bench_press, "smith_row": smith_row, "smith_shoulder_press": smith_shoulder_press,
       "smith_shrug": smith_shrug, "band_push_up": band_push_up,
       "incline_db_curl": incline_db_curl}


if __name__ == "__main__":
    out = sys.argv[1]
    for name, fn in NEW.items():
        c = Canvas()
        fn(c)
        path = f"{out}/{name}.png"
        c.save(path, tile=mi.TILE)
        Image.open(path).resize((192, 192), Image.LANCZOS).save(path, optimize=True)
