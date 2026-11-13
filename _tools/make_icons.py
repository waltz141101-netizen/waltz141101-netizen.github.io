import math, os, sys
from PIL import Image, ImageDraw, ImageFont

WHITE = (255, 255, 255)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(c1, c2, t):
    return tuple(int(round(a * (1 - t) + b * t)) for a, b in zip(c1, c2))


THEME = hex2rgb(sys.argv[2] if len(sys.argv) > 2 else "#C2185B")
TILE = mix(THEME, WHITE, 0.89)
BODY = THEME
FAR = mix(THEME, WHITE, 0.50)
GRAY = hex2rgb("#8A94A3")
GRAYL = mix(GRAY, WHITE, 0.58)
ARROW = hex2rgb("#F2A23A")

TORSO, NECKH, HR = 25.0, 10.8, 6.8
UA, FA = 15.0, 14.0
TH, SH, FT = 20.0, 19.0, 6.5
LW, TW, FW = 6.4, 9.0, 5.2


def fk(p, ang, L):
    return (p[0] + L * math.cos(math.radians(ang)), p[1] + L * math.sin(math.radians(ang)))


def ik(P, Q, L1, L2, bend=1):
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    d = min(math.hypot(dx, dy), L1 + L2 - 1e-3)
    a = math.atan2(dy, dx)
    c = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)
    A = math.acos(max(-1, min(1, c)))
    return (P[0] + L1 * math.cos(a + bend * A), P[1] + L1 * math.sin(a + bend * A))


class Canvas:
    def __init__(self, n=320, ss=4):
        self.n, self.ss, self.N = n, ss, n * ss
        self.ox, self.oy = 0.0, 0.0
        self.img = Image.new("RGBA", (self.N, self.N), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def P(self, p):
        return ((p[0] + self.ox) / 100 * self.N, (1 - (p[1] + self.oy) / 100) * self.N)

    def u(self, v):
        return v / 100 * self.N

    def stroke(self, pts, w, col):
        wp = self.u(w)
        Q = [self.P(p) for p in pts]
        if len(Q) > 1:
            self.d.line(Q, fill=col, width=max(1, int(round(wp))), joint="curve")
        r = wp / 2
        for q in Q:
            self.d.ellipse((q[0] - r, q[1] - r, q[0] + r, q[1] + r), fill=col)

    def circle(self, c, r, fill=None, outline=None, w=0):
        x, y = self.P(c)
        R = self.u(r)
        self.d.ellipse((x - R, y - R, x + R, y + R), fill=fill, outline=outline,
                       width=int(self.u(w)) if w else 0)

    def poly(self, pts, fill):
        self.d.polygon([self.P(p) for p in pts], fill=fill)

    def rrect(self, x0, y0, x1, y1, r, fill=None, outline=None, w=0):
        a, b = self.P((x0, y1)), self.P((x1, y0))
        self.d.rounded_rectangle((a[0], a[1], b[0], b[1]), radius=self.u(r), fill=fill,
                                 outline=outline, width=int(self.u(w)) if w else 0)

    def _head(self, tip, ang, size, col):
        L, W = size, size * 0.78
        ca, sa = math.cos(ang), math.sin(ang)
        base = (tip[0] - ca * L, tip[1] - sa * L)
        self.poly([tip, (base[0] - sa * W, base[1] + ca * W), (base[0] + sa * W, base[1] - ca * W)], col)

    def arrow(self, p0, p1, w=2.8, col=ARROW, head=None):
        head = head or w * 2.4
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        b = (p1[0] - math.cos(ang) * head * 0.7, p1[1] - math.sin(ang) * head * 0.7)
        self.stroke([p0, b], w, col)
        self._head(p1, ang, head, col)

    def arc_arrow(self, c, r, a0, a1, w=2.8, col=ARROW, head=None):
        head = head or w * 2.4
        sgn = 1 if a1 > a0 else -1
        a1s = a1 - sgn * math.degrees(head * 0.7 / r)
        n = 40
        pts = [fk(c, a0 + (a1s - a0) * i / n, r) for i in range(n + 1)]
        self.stroke(pts, w, col)
        tip = fk(c, a1, r)
        self._head(tip, math.radians(a1) + sgn * math.pi / 2, head, col)

    def save(self, path, tile=TILE):
        base = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        if tile:
            ImageDraw.Draw(base).rounded_rectangle((0, 0, self.N - 1, self.N - 1),
                                                   radius=int(self.N * 0.2), fill=tuple(tile) + (255,))
        base.alpha_composite(self.img)
        base.resize((self.n, self.n), Image.LANCZOS).save(path)


# 사람 옆모습. 각도: 0=오른쪽, 90=위. arm=(어깨→팔꿈치, 팔꿈치→손), leg=(엉덩이→무릎, 무릎→발목, 발)
def side(H, at, head_at=None, arm=None, leg=None, far_arm=None, far_leg=None, s=1.0):
    p = {"H": H}
    p["S"] = fk(H, at, TORSO * s)
    p["head"] = fk(p["S"], head_at if head_at is not None else at, NECKH * s)
    for key, a in (("arm", arm), ("far_arm", far_arm)):
        if a:
            E = fk(p["S"], a[0], UA * s)
            p[key] = [E, fk(E, a[1], FA * s)]
    for key, l in (("leg", leg), ("far_leg", far_leg)):
        if l:
            K = fk(H, l[0], TH * s)
            A = fk(K, l[1], SH * s)
            p[key] = [K, A, fk(A, l[2], FT * s)]
    p["s"] = s
    return p


def draw_side(c, p, between=None):
    s = p.get("s", 1.0)
    H, S = p["H"], p["S"]
    if p.get("far_leg"):
        K, A, T = p["far_leg"]
        c.stroke([H, K, A], LW * s, FAR)
        c.stroke([A, T], FW * s, FAR)
    if p.get("far_arm"):
        E, W = p["far_arm"]
        c.stroke([S, E, W], LW * s, FAR)
    c.stroke([H, S], TW * s, BODY)
    c.circle(p["head"], HR * s, fill=BODY)
    if p.get("leg"):
        K, A, T = p["leg"]
        c.stroke([H, K, A], LW * s, BODY)
        c.stroke([A, T], FW * s, BODY)
    if between:
        between()
    if p.get("arm"):
        E, W = p["arm"]
        c.stroke([S, E, W], LW * s, BODY)


def draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs, s=1.0):
    for (E, W), Sh in zip(arms, (Ls, Rs)):
        c.stroke([Sh, E, W], LW * s, BODY)
    for (K, A, T), Hp in zip(legs, (Lh, Rh)):
        c.stroke([Hp, K, A], LW * s, BODY)
        c.stroke([A, T], FW * s, BODY)
    c.poly([Ls, Rs, Rh, Lh], BODY)
    c.stroke([Ls, Rs, Rh, Lh, Ls], 4.0 * s, BODY)
    c.circle(head, HR * s, fill=BODY)


def pill(c, a, b, w, col=GRAY):
    c.stroke([a, b], w, col)


def floor(c, y, x0=6, x1=94):
    c.stroke([(x0, y), (x1, y)], 2.6, GRAY)


def dumbbell(c, center, ang=0, L=12, col=GRAY):
    a = fk(center, ang + 180, L / 2)
    b = fk(center, ang, L / 2)
    c.stroke([a, b], 2.6, col)
    for q in (a, b):
        c.stroke([fk(q, ang + 90, 3.6), fk(q, ang - 90, 3.6)], 3.8, col)


def pulley(c, center, r=3.4):
    c.circle(center, r, fill=GRAY)
    c.circle(center, r * 0.38, fill=WHITE)


def leg_press(c):
    p = side((37, 27), 140, 135, arm=(-45, -15), leg=(58, -12, 105))
    K, A, T = p["leg"]
    floor(c, 6)
    c.stroke([(26, 6), (26, 21)], 3, GRAY)
    c.stroke([(24, 14), (92, 32.2)], 3, GRAY)
    hb, sb = fk(p["H"], 230, 6.6), fk(p["S"], 230, 6.6)
    pill(c, fk(hb, 140, -4), fk(sb, 140, 4), 5.2)
    mid = ((A[0] + T[0]) / 2, (A[1] + T[1]) / 2)
    pc = fk(mid, 15, 4.6)
    c.stroke([pc, fk(pc, -75, 13)], 3, GRAY)
    pill(c, fk(pc, 105, 10), fk(pc, -75, 10), 4.6)
    c.circle(p["arm"][1], 2.6, fill=GRAY)
    draw_side(c, p)
    c.arrow(fk(pc, 105, 13), fk(fk(pc, 105, 13), 15, 14))


def goblet_squat(c):
    p = side((37.6, 33.6), 70, 80, arm=(-70, 75), leg=(-15, -105, 0))
    floor(c, 6, 26, 78)

    def db():
        dumbbell(c, (57.8, 52.5), 90, 12)
    draw_side(c, p, between=db)


def leg_extension(c):
    p = side((36, 34), 98, 95, arm=(-78, -25), leg=(0, -12, 75))
    K, A, T = p["leg"]
    floor(c, 6, 14, 92)
    c.stroke([(40, 27), (40, 6)], 3, GRAY)
    pill(c, (26, 28.6), (56, 28.6), 5.2)
    pill(c, (26.6, 30), (24.4, 60), 5.2)
    W = p["arm"][1]
    pill(c, (W[0], W[1] - 5), (W[0], W[1] + 0.5), 3.2)
    draw_side(c, p)
    pad = fk(fk(A, 168, 3.5), 78, 6.4)
    c.stroke([pad, (56, 40)], 2.6, GRAY)
    c.circle((56, 40), 2.4, fill=GRAY)
    c.circle(pad, 4.3, fill=GRAY)
    c.arc_arrow(K, 29, -58, -24)


def _front_seated_base(hip_y=40, sh_y=64, head_y=77):
    return dict(head=(50, head_y), Ls=(40, sh_y), Rs=(60, sh_y), Lh=(43.5, hip_y), Rh=(56.5, hip_y))


def inner_thigh(c):
    b = _front_seated_base()
    floor(c, 7, 12, 88)
    c.rrect(35, 37, 65, 67.5, 3.5, fill=GRAYL)
    pill(c, (36, 36), (64, 36), 5)
    arms = [((33, 52), (35, 41.5)), ((67, 52), (65, 41.5))]
    legs = [((28.5, 32.5), (26.5, 13), (20.5, 12.4)), ((71.5, 32.5), (73.5, 13), (79.5, 12.4))]
    pill(c, (31.5, 41.5), (38, 41.5), 3)
    pill(c, (62, 41.5), (68.5, 41.5), 3)
    draw_front(c, b["head"], b["Ls"], b["Rs"], b["Lh"], b["Rh"], arms, legs)
    pill(c, (35.6, 26.5), (35.6, 35.5), 4.6)
    pill(c, (64.4, 26.5), (64.4, 35.5), 4.6)
    c.arrow((35.5, 21), (46.5, 21))
    c.arrow((64.5, 21), (53.5, 21))


def outer_thigh(c):
    b = _front_seated_base()
    floor(c, 7, 12, 88)
    c.rrect(35, 37, 65, 67.5, 3.5, fill=GRAYL)
    pill(c, (36, 36), (64, 36), 5)
    arms = [((33, 52), (35, 41.5)), ((67, 52), (65, 41.5))]
    legs = [((40.5, 32), (40, 13), (34.5, 12.4)), ((59.5, 32), (60, 13), (65.5, 12.4))]
    pill(c, (31.5, 41.5), (38, 41.5), 3)
    pill(c, (62, 41.5), (68.5, 41.5), 3)
    draw_front(c, b["head"], b["Ls"], b["Rs"], b["Lh"], b["Rh"], arms, legs)
    pill(c, (33.2, 25.5), (33.2, 35.5), 4.6)
    pill(c, (66.8, 25.5), (66.8, 35.5), 4.6)
    c.arrow((31, 20), (18.5, 20))
    c.arrow((69, 20), (81.5, 20))


def back_extension(c):
    p = side((49.9, 39.1), 40, 40, arm=(-60, 150), leg=(220, 220, -50))
    K, A, T = p["leg"]
    floor(c, 4, 8, 70)
    c.stroke([(19, 4), (56, 30)], 3, GRAY)
    hp = fk(p["H"], -50, 6.8)
    pill(c, fk(hp, 220, 7.5), fk(hp, 40, 7.5), 6)
    mid = ((A[0] + T[0]) / 2, (A[1] + T[1]) / 2)
    fp = fk(mid, 220, 3.8)
    pill(c, fk(fp, 130, 6.5), fk(fp, -50, 6.5), 4.2)
    draw_side(c, p)
    c.circle(fk(fk(A, 40, 4.5), 130, 6.3), 4.2, fill=GRAY)


def lat_pulldown(c):
    head, Ls, Rs, Lh, Rh = (50, 61), (40.5, 49), (59.5, 49), (44, 28), (56, 28)
    pulley(c, (50, 94.5))
    c.stroke([(50, 84), (50, 92)], 1.8, GRAY)
    c.stroke([(14, 80.5), (21, 84), (79, 84), (86, 80.5)], 3.2, GRAY)
    arms = [((32.5, 65), (27, 82)), ((67.5, 65), (73, 82))]
    legs = [((37.5, 21.5), (37.5, 7), (32.5, 6.4)), ((62.5, 21.5), (62.5, 7), (67.5, 6.4))]
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    pill(c, (30.5, 24.5), (69.5, 24.5), 5.4)
    c.arrow((13, 71), (13, 58))
    c.arrow((87, 71), (87, 58))


def underhand_pulldown(c):
    head, Ls, Rs, Lh, Rh = (50, 61), (40.5, 49), (59.5, 49), (44, 28), (56, 28)
    pulley(c, (50, 94.5))
    c.stroke([(50, 84), (50, 92)], 1.8, GRAY)
    c.stroke([(14, 80.5), (21, 84), (79, 84), (86, 80.5)], 3.2, GRAY)
    arms = [((36, 66), (37, 83)), ((64, 66), (63, 83))]
    legs = [((37.5, 21.5), (37.5, 7), (32.5, 6.4)), ((62.5, 21.5), (62.5, 7), (67.5, 6.4))]
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    pill(c, (30.5, 24.5), (69.5, 24.5), 5.4)
    c.arrow((18, 71), (18, 58))
    c.arrow((82, 71), (82, 58))


def seated_row(c):
    p = side((36, 30), 92, 92, arm=(-4, 0), leg=(5, -62, 62))
    K, A, T = p["leg"]
    W = p["arm"][1]
    floor(c, 6, 12, 96)
    c.stroke([(37, 23), (37, 6)], 3, GRAY)
    pill(c, (27, 25.3), (46, 25.3), 5.2)
    c.stroke([(88.5, 6), (88.5, 66)], 3.2, GRAY)
    c.stroke([(W[0] + 2, W[1]), (85, W[1])], 1.8, GRAY)
    pulley(c, (88.5, W[1]))
    mid = ((A[0] + T[0]) / 2, (A[1] + T[1]) / 2)
    fp = fk(mid, -28, 4.2)
    pill(c, fk(fp, 62, 7.5), fk(fp, -118, 7.5), 4.4)
    pill(c, (42.6, 37), (42.6, 49.5), 5)
    pill(c, (W[0] + 0.6, W[1] - 5.2), (W[0] + 0.6, W[1] + 5.2), 3.4)
    draw_side(c, p)
    c.arrow((80, 64), (63, 64))


def shoulder_press(c):
    head, Ls, Rs, Lh, Rh = (50, 61), (40.5, 49), (59.5, 49), (44, 27), (56, 27)
    c.rrect(35.5, 25, 64.5, 52.5, 3.5, fill=GRAYL)
    pill(c, (35, 24.5), (65, 24.5), 4.6)
    floor(c, 4, 20, 80)
    pill(c, (23.5, 75), (33.5, 75), 3.4)
    pill(c, (66.5, 75), (76.5, 75), 3.4)
    arms = [((29.5, 58.5), (28.5, 75)), ((70.5, 58.5), (71.5, 75))]
    legs = [((37.5, 21), (37.5, 7), (32.5, 6.4)), ((62.5, 21), (62.5, 7), (67.5, 6.4))]
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    c.arrow((28.5, 81), (28.5, 94))
    c.arrow((71.5, 81), (71.5, 94))


def lateral_raise(c):
    head, Ls, Rs, Lh, Rh = (50, 84), (40.5, 72), (59.5, 72), (44, 46), (56, 46)
    floor(c, 5, 24, 76)
    arms = [((27, 71.5), (13.5, 71)), ((73, 71.5), (86.5, 71))]
    legs = [((43.5, 27.5), (43, 9.5), (37.8, 9)), ((56.5, 27.5), (57, 9.5), (62.2, 9))]
    dumbbell(c, (13.5, 71), 90, 11)
    dumbbell(c, (86.5, 71), 90, 11)
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    c.arrow((13.5, 50), (13.5, 61))
    c.arrow((86.5, 50), (86.5, 61))


def plank(c):
    c.oy = 22
    S, E, W = (76, 28.5), (76, 13.6), (90, 13.6)
    A = (13, 17.4)
    ux, uy = (A[0] - S[0]), (A[1] - S[1])
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    H = (S[0] + TORSO * ux, S[1] + TORSO * uy)
    K = (H[0] + TH * ux, H[1] + TH * uy)
    T = (17.5, 12.6)
    pill(c, (6, 8.4), (96, 8.4), 3.0, GRAYL)
    p = {"H": H, "S": S, "head": fk(S, 17, NECKH), "arm": [E, W], "leg": [K, A, T]}
    draw_side(c, p)


def hip_thrust(c):
    S = (28, 42)
    H = fk(S, 8, TORSO)
    K = fk(H, 0, TH)
    A = fk(K, -90, SH)
    T = fk(A, 0, FT)
    floor(c, 21.5, 4, 96)
    c.rrect(4, 32.6, 31, 37.6, 2.2, fill=GRAY)
    c.stroke([(8, 32.6), (8, 21.5)], 2.6, GRAY)
    c.stroke([(27, 32.6), (27, 21.5)], 2.6, GRAY)
    pill(c, (45.5, 51.8), (60.5, 51.8), 5.4)
    E = fk(S, 50, UA)
    W = fk(E, -10, FA)
    p = {"H": H, "S": S, "head": fk(S, 160, NECKH), "arm": [E, W], "leg": [K, A, T]}
    draw_side(c, p)
    c.arrow((53, 59), (53, 72))


def db_rdl(c):
    p = side((40, 52), 25, 15, arm=(-90, -90), leg=(-80, -95, 0))
    floor(c, 9, 22, 82)
    draw_side(c, p)
    W = p["arm"][1]
    dumbbell(c, (W[0], W[1] - 0.5), 0, 12)
    c.circle(W, LW / 2, fill=BODY)
    c.arc_arrow(p["H"], 30, 48, 80)


def lying_leg_curl(c):
    S, H = (66, 38.5), (41, 38.5)
    K = fk(H, 180, TH)
    A = fk(K, 100, SH)
    T = fk(A, 160, FT)
    floor(c, 7, 4, 96)
    c.stroke([(12, 31), (12, 7)], 2.6, GRAY)
    c.stroke([(78, 31), (78, 7)], 2.6, GRAY)
    c.rrect(4, 31, 86, 35.6, 2.2, fill=GRAY)
    E = fk(S, -45, UA)
    W = fk(E, 10, FA)
    pill(c, (86, 33), (W[0] + 1, W[1] - 1), 3)
    p = {"H": H, "S": S, "head": fk(S, 15, NECKH), "arm": [E, W], "leg": [K, A, T]}
    draw_side(c, p)
    roller = fk(fk(A, 280, 3.6), 10, 6.2)
    c.stroke([roller, (23.5, 40)], 2.6, GRAY)
    c.circle(roller, 4.3, fill=GRAY)
    c.arc_arrow(K, 17, 166, 122)


def cable_kickback(c):
    p = side((45, 48), 55, 50, arm=(-12, -25), leg=(200, 195, -80), far_leg=(-85, -92, 0))
    K2, A2, T2 = p["leg"]
    floor(c, 4, 30, 96)
    c.stroke([(91, 4), (91, 86)], 3.2, GRAY)
    c.stroke([(A2[0] + 0.5, A2[1] - 0.5), (88.5, 10.5)], 1.6, GRAY)
    pulley(c, (91, 10.2))
    W = p["arm"][1]
    pill(c, (W[0] + 0.5, W[1] - 4), (W[0] + 0.5, W[1] + 4), 3.2)
    c.stroke([(W[0] + 0.5, W[1]), (91, W[1])], 2.6, GRAY)
    draw_side(c, p)
    cuff = fk(A2, 15, 1.8)
    c.stroke([fk(cuff, 105, 3.6), fk(cuff, 285, 3.6)], 3.2, GRAY)
    c.arc_arrow(p["H"], 31, 243, 207)


def chest_press(c):
    p = side((36, 30), 96, 94, arm=(-2, 0), leg=(0, -90, 0))
    W = p["arm"][1]
    floor(c, 6.5, 12, 92)
    c.stroke([(37, 23), (37, 6.5)], 3, GRAY)
    pill(c, (26, 25.3), (46, 25.3), 5.2)
    pill(c, (26.6, 28), (24, 61), 5.2)
    c.stroke([(W[0] + 0.6, W[1] + 5), (W[0] - 6, W[1] + 19)], 2.6, GRAY)
    c.circle((W[0] - 6, W[1] + 19), 2.4, fill=GRAY)
    pill(c, (W[0] + 0.6, W[1] - 5.2), (W[0] + 0.6, W[1] + 5.2), 3.4)
    draw_side(c, p)
    c.arrow((70, 64), (86, 64))


def one_arm_row(c):
    H = (40, 53.7)
    S = fk(H, 20, TORSO)
    floor(c, 10, 4, 96)
    c.stroke([(14, 26), (14, 10)], 2.6, GRAY)
    c.stroke([(86, 26), (86, 10)], 2.6, GRAY)
    c.rrect(6, 26, 92, 30.6, 2.2, fill=GRAY)
    Kf = (40, 33.7)
    Af = (21, 33.7)
    Ef = fk(S, -70, UA)
    Wf = fk(Ef, -80, FA)
    K = fk(H, -95, TH)
    A = fk(K, -88, SH)
    E = fk(S, 165, UA)
    W = fk(E, -85, FA)
    p = {"H": H, "S": S, "head": fk(S, 22, NECKH), "leg": [K, A, fk(A, 0, FT)],
         "arm": [E, W], "far_leg": [Kf, Af, fk(Af, 200, FT)], "far_arm": [Ef, Wf]}

    def db():
        dumbbell(c, (W[0], W[1] - 0.6), 0, 11)
    draw_side(c, p, between=db)
    c.arrow((40, 60), (40, 73))


def reverse_pec_deck(c):
    c.oy = -12
    GHOST = mix(BODY, WHITE, 0.72)
    SL, SR = (33, 46), (67, 46)
    c.rrect(30, 66, 70, 73, 3.5, fill=GRAY)
    for Sh, Hd in ((SL, (43, 84)), (SR, (57, 84))):
        c.stroke([Sh, Hd], LW * 0.9, GHOST)
        c.circle(Hd, 3.0, fill=GHOST)
    c.rrect(28, 30, 72, 56, 11, fill=BODY)
    c.circle((50, 59), 8.6, fill=BODY)
    for Sh, Hd in ((SL, (9, 47)), (SR, (91, 47))):
        c.stroke([Sh, Hd], LW, BODY)
        pill(c, (Hd[0], Hd[1] - 6.5), (Hd[0], Hd[1] + 6.5), 3.8)
    c.arc_arrow(SL, 27, 72, 160, w=3.2)
    c.arc_arrow(SR, 27, 108, 20, w=3.2)


def foam_roller(c):
    c.oy = 10
    floor(c, 18, 4, 96)
    R = 6.5
    roll = (34, 18 + R)
    c.circle(roll, R, fill=GRAY)
    c.circle(roll, R * 0.42, fill=WHITE)
    S = (roll[0] - 3, roll[1] + R + 3.8)
    H = fk(S, -12, TORSO)
    A = (H[0] + 24, 19.5)
    K = ik(H, A, TH, SH, bend=1)
    E = fk(S, 120, UA)
    W = fk(E, 20, FA)
    p = {"H": H, "S": S, "head": fk(S, 172, NECKH), "arm": [E, W], "leg": [K, A, fk(A, 0, FT)],
         "far_leg": [K, A, fk(A, 0, FT)]}
    draw_side(c, p)
    c.arrow((40, 58), (24, 58), w=2.6)
    c.arrow((44, 58), (60, 58), w=2.6)


def cable_pushdown(c):
    p = side((40, 46), 86, 86, arm=(-93, -50), leg=(-88, -91, 0))
    W = p["arm"][1]
    floor(c, 3.2, 26, 92)
    c.stroke([(82, 3.2), (82, 94)], 3.2, GRAY)
    c.stroke([(82, 92.5), (70, 92.5)], 3, GRAY)
    pulley(c, (70, 89))
    c.stroke([(W[0] + 1, W[1] + 1), (67.6, 87)], 1.6, GRAY)
    pill(c, (W[0] - 4.5, W[1]), (W[0] + 4.5, W[1]), 3.4)
    draw_side(c, p)
    c.arrow((61, 47), (61, 32))


def dead_bug(c):
    c.oy = 21
    S, H = (27, 14.6), (52, 14.6)
    p = {"H": H, "S": S, "head": (16.4, 16.6),
         "arm": [fk(S, 90, UA), fk(fk(S, 90, UA), 90, FA)]}
    Ef = fk(S, 140, UA)
    p["far_arm"] = [Ef, fk(Ef, 150, FA)]
    K = fk(H, 12, TH)
    A = fk(K, 6, SH)
    p["leg"] = [K, A, fk(A, 80, FT)]
    Kf = fk(H, 90, TH)
    Af = fk(Kf, 0, SH)
    p["far_leg"] = [Kf, Af, fk(Af, 90, FT)]
    pill(c, (4, 8.6), (96, 8.6), 3.0, GRAYL)
    draw_side(c, p)


def smith_squat(c):
    p = side((40, 38), 72, 80, arm=(-125, 72), leg=(-20, -108, 0))
    S = p["S"]
    floor(c, 6, 20, 80)
    bar = fk(S, 160, 3.5)
    c.stroke([(bar[0], 6), (bar[0], 94)], 2.6, GRAY)
    draw_side(c, p)
    c.circle(bar, 4.2, fill=GRAY)
    c.circle(bar, 1.6, fill=WHITE)
    c.arrow((70, 50), (70, 64))


def lateral_raise_machine(c):
    head, Ls, Rs, Lh, Rh = (50, 61), (40.5, 49), (59.5, 49), (44, 27), (56, 27)
    c.rrect(35.5, 25, 64.5, 52.5, 3.5, fill=GRAYL)
    pill(c, (35, 24.5), (65, 24.5), 4.6)
    floor(c, 4, 20, 80)
    arms = [((26, 51), (24.5, 45)), ((74, 51), (75.5, 45))]
    legs = [((37.5, 21), (37.5, 7), (32.5, 6.4)), ((62.5, 21), (62.5, 7), (67.5, 6.4))]
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    pill(c, (25, 47.5), (25, 55.5), 5)
    pill(c, (75, 47.5), (75, 55.5), 5)
    c.arrow((16, 54), (16, 66))
    c.arrow((84, 54), (84, 66))


def seated_leg_curl(c):
    p = side((36, 34), 98, 95, arm=(-78, -25), leg=(0, -112, 60))
    K, A, T = p["leg"]
    floor(c, 6, 14, 92)
    c.stroke([(40, 27), (40, 6)], 3, GRAY)
    pill(c, (26, 28.6), (56, 28.6), 5.2)
    pill(c, (26.6, 30), (24.4, 60), 5.2)
    W = p["arm"][1]
    pill(c, (W[0], W[1] - 5), (W[0], W[1] + 0.5), 3.2)
    draw_side(c, p)
    pill(c, (44, 40.5), (58, 40.5), 4.6)
    pad = fk(fk(A, 68, 3), 158, 6.2)
    c.stroke([pad, (58, 34)], 2.6, GRAY)
    c.circle(pad, 4.3, fill=GRAY)
    c.arc_arrow(K, 23, -40, -95)


def high_row(c):
    p = side((36, 30), 92, 92, arm=(28, 40), leg=(5, -62, 62))
    K, A, T = p["leg"]
    W = p["arm"][1]
    floor(c, 6, 12, 96)
    c.stroke([(37, 23), (37, 6)], 3, GRAY)
    pill(c, (27, 25.3), (46, 25.3), 5.2)
    pill(c, (42.6, 37), (42.6, 50), 5)
    c.stroke([(W[0] + 1, W[1] + 4), (84, 86)], 2.8, GRAY)
    c.circle((84, 86), 2.6, fill=GRAY)
    c.stroke([(84, 86), (88, 86), (88, 6)], 3.2, GRAY)
    mid = ((A[0] + T[0]) / 2, (A[1] + T[1]) / 2)
    fp = fk(mid, -28, 4.2)
    pill(c, fk(fp, 62, 7.5), fk(fp, -118, 7.5), 4.4)
    pill(c, (W[0] - 0.5, W[1] - 5), (W[0] + 0.5, W[1] + 5), 3.4)
    draw_side(c, p)
    c.arrow((W[0] + 4, W[1] - 9), (W[0] - 9, W[1] - 21))


def bench_press(c):
    S, H = (34, 39), (59, 39)
    K = fk(H, 10, TH)
    A = fk(K, -85, SH)
    floor(c, 21.5, 4, 96)
    c.rrect(10, 31, 66, 35.6, 2.2, fill=GRAY)
    c.stroke([(16, 31), (16, 21.5)], 2.6, GRAY)
    c.stroke([(60, 31), (60, 21.5)], 2.6, GRAY)
    c.stroke([(22, 21.5), (22, 70)], 2.6, GRAYL)
    E = fk(S, 92, UA)
    W = fk(E, 90, FA)
    p = {"H": H, "S": S, "head": fk(S, 180, NECKH), "arm": [E, W], "leg": [K, A, fk(A, 0, FT)]}
    draw_side(c, p)
    c.circle((W[0], W[1] + 1), 7.2, fill=GRAY)
    c.circle((W[0], W[1] + 1), 2.2, fill=WHITE)
    c.stroke([fk(W, 270, 1), fk(W, 90, 2)], LW, BODY)
    c.arrow((50, 58), (50, 74))


def incline_db_press(c):
    p = side((45, 32), 128, 125, arm=(78, 86), leg=(0, -90, 0))
    floor(c, 12, 14, 86)
    hb, sb = fk(p["H"], 218, 6.6), fk(p["S"], 218, 6.6)
    pill(c, fk(hb, 128, -3), fk(sb, 128, 5), 5.2)
    pill(c, (36, 25.4), (56, 25.4), 5.2)
    c.stroke([(44, 25), (44, 12)], 3, GRAY)
    W = p["arm"][1]
    draw_side(c, p)
    dumbbell(c, (W[0], W[1] + 1.5), 0, 12)
    c.arrow((54, 66), (54, 81))


def smith_incline_press(c):
    c.oy = -8
    p = side((45, 32), 128, 125, arm=(78, 86), leg=(0, -90, 0))
    floor(c, 12, 14, 86)
    hb, sb = fk(p["H"], 218, 6.6), fk(p["S"], 218, 6.6)
    pill(c, fk(hb, 128, -3), fk(sb, 128, 5), 5.2)
    pill(c, (36, 25.4), (56, 25.4), 5.2)
    c.stroke([(44, 25), (44, 12)], 3, GRAY)
    W = p["arm"][1]
    rail_x = W[0] + 9
    c.stroke([(rail_x, 12), (rail_x, 100)], 2.6, GRAYL)
    draw_side(c, p)
    c.circle((W[0], W[1] + 1), 6.6, fill=GRAY)
    c.circle((W[0], W[1] + 1), 2.0, fill=WHITE)
    c.stroke([fk(W, 270, 1), fk(W, 90, 2)], LW, BODY)
    c.arrow((W[0] + 20, 64), (W[0] + 20, 79))


def outer_thigh_pin(c):
    c.ox = -9
    outer_thigh(c)
    x0, x1, y0, y1 = 89, 97, 9, 70
    c.stroke([(x0 - 1.5, 7), (x0 - 1.5, 93)], 2.2, GRAYL)
    c.stroke([(x1 + 1.5, 7), (x1 + 1.5, 93)], 2.2, GRAYL)
    for i in range(9):
        y = y0 + i * (y1 - y0) / 9
        c.rrect(x0, y + 0.8, x1, y + (y1 - y0) / 9 - 0.8, 1.0, fill=GRAY)
    py = y0 + 5.5 * (y1 - y0) / 9
    c.stroke([(x0 - 6, py), (x0 + 2, py)], 2.6, ARROW)
    c.circle((x0 - 6.5, py), 2.4, fill=ARROW)
    c.stroke([((x0 + x1) / 2, y1), ((x0 + x1) / 2, 90)], 1.6, GRAY)


def outer_thigh_plate(c):
    b = _front_seated_base()
    floor(c, 7, 12, 88)
    c.rrect(35, 37, 65, 67.5, 3.5, fill=GRAYL)
    pill(c, (36, 36), (64, 36), 5)
    arms = [((33, 52), (35, 41.5)), ((67, 52), (65, 41.5))]
    legs = [((40.5, 32), (40, 13), (34.5, 12.4)), ((59.5, 32), (60, 13), (65.5, 12.4))]
    for sx in (-1, 1):
        px = 50 + sx * 16.8
        hx = 50 + sx * 33
        c.stroke([(px, 33), (hx, 46)], 3.0, GRAY)
        c.stroke([(hx, 46), (hx, 52)], 3.0, GRAY)
        c.circle((hx, 54), 11.5, fill=GRAY)
        c.circle((hx, 54), 7.6, fill=GRAYL)
        c.circle((hx, 54), 2.4, fill=WHITE)
    pill(c, (31.5, 41.5), (38, 41.5), 3)
    pill(c, (62, 41.5), (68.5, 41.5), 3)
    draw_front(c, b["head"], b["Ls"], b["Rs"], b["Lh"], b["Rh"], arms, legs)
    pill(c, (33.2, 25.5), (33.2, 35.5), 4.6)
    pill(c, (66.8, 25.5), (66.8, 35.5), 4.6)
    c.arrow((31, 20), (18.5, 20))
    c.arrow((69, 20), (81.5, 20))


def pec_deck(c):
    c.oy = -4
    GHOST = mix(BODY, WHITE, 0.72)
    SL, SR = (33, 46), (67, 46)
    c.rrect(30, 22, 70, 28.5, 3.2, fill=GRAY)
    for Sh, Hd in ((SL, (9, 47)), (SR, (91, 47))):
        c.stroke([Sh, Hd], LW * 0.9, GHOST)
        c.circle(Hd, 3.0, fill=GHOST)
    c.rrect(28, 30, 72, 56, 11, fill=BODY)
    c.circle((50, 53), 8.6, fill=BODY)
    for Sh, Hd in ((SL, (45.5, 84)), (SR, (54.5, 84))):
        c.stroke([Sh, Hd], LW, BODY)
        pill(c, (Hd[0], Hd[1] - 6.5), (Hd[0], Hd[1] + 6.5), 3.8)
    c.arc_arrow(SL, 27, 168, 82, w=3.2)
    c.arc_arrow(SR, 27, 12, 98, w=3.2)


def db_curl(c):
    p = side((42, 46), 90, 90, arm=(-95, 22), leg=(-90, -90, 0), far_leg=(-96, -88, 0), far_arm=(-88, -86))
    floor(c, 5.5, 24, 76)
    draw_side(c, p)
    W = p["arm"][1]
    dumbbell(c, (W[0] + 0.5, W[1]), 90, 11)
    c.circle(W, LW / 2, fill=BODY)
    c.arc_arrow(p["arm"][0], 24, -35, 55)


def overhead_ext(c):
    head, Ls, Rs, Lh, Rh = (50, 66), (40.5, 54), (59.5, 54), (44, 31), (56, 31)
    floor(c, 4, 22, 78)
    arms = [((37.5, 68.5), (47, 81)), ((62.5, 68.5), (53, 81))]
    legs = [((43, 17.5), (42.6, 6), (37.6, 5.6)), ((57, 17.5), (57.4, 6), (62.4, 5.6))]
    dumbbell(c, (50, 87), 90, 11)
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    c.stroke([(47, 81), (53, 81)], LW, BODY)
    c.arrow((26, 72), (26, 87))
    c.arrow((74, 72), (74, 87))


def shrug(c):
    head, Ls, Rs, Lh, Rh = (50, 84), (40.5, 72), (59.5, 72), (44, 46), (56, 46)
    floor(c, 5, 24, 76)
    arms = [((36.5, 57.5), (35.5, 44)), ((63.5, 57.5), (64.5, 44))]
    legs = [((43.5, 27.5), (43, 9.5), (37.8, 9)), ((56.5, 27.5), (57, 9.5), (62.2, 9))]
    dumbbell(c, (35.5, 42), 0, 11)
    dumbbell(c, (64.5, 42), 0, 11)
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    c.arrow((22, 66), (22, 80))
    c.arrow((78, 66), (78, 80))


def straight_arm_pulldown(c):
    p = side((40, 46), 76, 76, arm=(-58, -58), leg=(-88, -91, 0))
    W = p["arm"][1]
    floor(c, 3.2, 26, 92)
    c.stroke([(84, 3.2), (84, 94)], 3.2, GRAY)
    c.stroke([(84, 92.5), (74, 92.5)], 3, GRAY)
    pulley(c, (74, 89))
    c.stroke([(W[0] + 1, W[1] + 1), (71.6, 87)], 1.6, GRAY)
    pill(c, (W[0] - 4.5, W[1]), (W[0] + 4.5, W[1]), 3.4)
    draw_side(c, p)
    c.arc_arrow(p["S"], 25, 18, -42)


def treadmill(c):
    H = (42, 52)
    pill(c, (8, 6), (78, 12), 5)
    c.stroke([(76, 11), (85, 60)], 3.2, GRAY)
    pill(c, (81, 63), (95, 65.5), 6)
    c.stroke([(84.5, 57.5), (60, 57.5)], 2.6, GRAY)
    p = side(H, 86, 86, arm=(-112, -78), leg=(-68, -96, 5), far_arm=(-62, -10), far_leg=(-108, -125, -35))
    draw_side(c, p)


def stair_climber(c):
    floor(c, 4, 4, 96)
    c.stroke([(8, 4), (8, 12), (30, 12), (30, 20), (52, 20), (52, 28), (92, 28), (92, 4)], 3, GRAY)
    s = 0.88
    Ar, Af = (38, 23.0), (60, 31.0)
    H = (47, 56)
    Kf = ik(H, Af, TH * s, SH * s, bend=1)
    Kr = ik(H, Ar, TH * s, SH * s, bend=1)
    S = fk(H, 82, TORSO * s)
    p = {"H": H, "S": S, "head": fk(S, 84, NECKH * s), "s": s,
         "leg": [Kf, Af, fk(Af, 0, FT * s)], "far_leg": [Kr, Ar, fk(Ar, -10, FT * s)]}
    E = fk(S, -100, UA * s)
    p["arm"] = [E, fk(E, -20, FA * s)]
    Ef = fk(S, -60, UA * s)
    p["far_arm"] = [Ef, fk(Ef, -5, FA * s)]
    c.stroke([(56, 28), (72, 60), (88, 60)], 2.6, GRAY)
    draw_side(c, p)
    c.arrow((70, 36), (78, 46), w=2.4)


def bike(c):
    floor(c, 5, 14, 90)
    c.circle((70, 22), 12.5, outline=GRAY, w=3)
    c.circle((70, 22), 2.4, fill=GRAY)
    c.stroke([(26, 5), (38, 40)], 3.2, GRAY)
    c.stroke([(33, 22), (52, 22), (70, 22)], 3.2, GRAY)
    c.stroke([(70, 22), (76, 55)], 3.2, GRAY)
    pill(c, (73, 57), (84, 58.5), 3.6)
    pill(c, (30, 43.5), (44, 43.5), 4.6)
    crank = (52, 22)
    c.circle(crank, 2.6, fill=GRAY)
    H = (38, 49)
    Pn, Pf = fk(crank, -40, 9), fk(crank, 140, 9)
    An, Af = (Pn[0] - 3, Pn[1] + 1.8), (Pf[0] - 3, Pf[1] + 1.8)
    Kn = ik(H, An, TH, SH, bend=1)
    Kf = ik(H, Af, TH, SH, bend=1)
    S = fk(H, 58, TORSO)
    grip = (77, 59.5)
    E = ik(S, grip, UA, FA, bend=-1)
    Ef = ik(S, (75.5, 60.5), UA, FA, bend=-1)
    p = {"H": H, "S": S, "head": fk(S, 56, NECKH), "leg": [Kn, An, fk(An, 0, FT)],
         "far_leg": [Kf, Af, fk(Af, 0, FT)], "arm": [E, grip], "far_arm": [Ef, (75.5, 60.5)]}
    draw_side(c, p)


def walk(c):
    floor(c, 6, 8, 92)
    p = side((48, 48.5), 86, 86, arm=(-112, -78), leg=(-66, -97, 5), far_arm=(-62, -10), far_leg=(-110, -128, -35))
    draw_side(c, p)
    for x, y in [(14, 40), (20, 34), (14, 28)]:
        c.stroke([(x, y), (x + 8, y)], 2.4, GRAYL)


def rest(c):
    m = Image.new("L", c.img.size, 0)
    dm = ImageDraw.Draw(m)
    cx, cy, R = c.P((46, 50)) + (c.u(25),)
    dm.ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
    ox, oy = c.u(12), c.u(-9)
    dm.ellipse((cx - R + ox, cy - R + oy, cx + R + ox, cy + R + oy), fill=0)
    layer = Image.new("RGBA", c.img.size, BODY + (255,))
    c.img.paste(layer, (0, 0), m)
    f = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc", int(c.u(16)), index=1)
    f2 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc", int(c.u(11)), index=1)
    c.d.text(c.P((66, 80)), "Z", font=f, fill=GRAY)
    c.d.text(c.P((80, 64)), "z", font=f2, fill=GRAY)


def dumbbell_icon(c):
    c.stroke([(26, 50), (74, 50)], 6, GRAY)
    for x in (24, 76):
        c.stroke([(x, 34), (x, 66)], 9, BODY)
    for x in (14, 86):
        c.stroke([(x, 40), (x, 60)], 8, BODY)


def pencil(c):
    a, b = (24, 22), (72, 70)
    c.stroke([a, b], 13, BODY)
    c.stroke([fk(b, 225, 2), fk(b, 225, 0.5)], 13, mix(BODY, WHITE, 0.55))
    tip = fk(a, 225, 10)
    c.poly([fk(a, 135, 6.5), fk(a, -45, 6.5), tip], (233, 196, 160))
    c.poly([fk(tip, 45, 3.6), tip, fk(fk(tip, 45, 3.6), 0, 0.01)], GRAY)
    c.circle(tip, 2.2, fill=hex2rgb("#5B6170"))
    c.stroke([(18, 12), (52, 12)], 2.6, GRAYL)


def heart(c):
    m = Image.new("L", c.img.size, 0)
    dm = ImageDraw.Draw(m)
    for cx in (37, 63):
        x, y = c.P((cx, 60))
        R = c.u(17)
        dm.ellipse((x - R, y - R, x + R, y + R), fill=255)
    dm.polygon([c.P((21.5, 54)), c.P((78.5, 54)), c.P((50, 20))], fill=255)
    layer = Image.new("RGBA", c.img.size, BODY + (255,))
    c.img.paste(layer, (0, 0), m)
    c.stroke([(22, 50), (36, 50), (42, 62), (50, 36), (56, 56), (61, 50), (78, 50)], 4.2, WHITE)


def face_pull(c):
    p = side((36, 28), 92, 92, arm=(155, 15), leg=(5, -62, 62))
    K, A, T = p["leg"]
    E, W = p["arm"]
    floor(c, 6, 12, 96)
    c.stroke([(37, 21), (37, 6)], 3, GRAY)
    pill(c, (27, 23.3), (46, 23.3), 5.2)
    c.stroke([(88.5, 6), (88.5, 92)], 3.2, GRAY)
    knot = (W[0] + 11, W[1])
    c.stroke([knot, (85, knot[1])], 1.8, GRAY)
    pulley(c, (88.5, knot[1]))
    mid = ((A[0] + T[0]) / 2, (A[1] + T[1]) / 2)
    fp = fk(mid, -28, 4.2)
    pill(c, fk(fp, 62, 7.5), fk(fp, -118, 7.5), 4.4)
    draw_side(c, p)
    for dy in (3.2, -3.2):
        c.stroke([(W[0] + 1, W[1] + dy), knot], 2.0, GRAY)
    c.circle(W, LW / 2, fill=BODY)
    c.arrow((78, knot[1] + 11), (60, knot[1] + 11))


def lateral_raise_standing(c):
    GHOST = mix(BODY, WHITE, 0.72)
    head, Ls, Rs, Lh, Rh = (50, 82), (40.5, 70), (59.5, 70), (44, 44), (56, 44)
    c.rrect(28, 3.5, 72, 8, 2, fill=GRAY)
    c.stroke([(50, 8), (50, 97)], 4.2, GRAY)
    hub = (50, 76)
    for sx in (-1, 1):
        c.stroke([hub, (50 + sx * 27, 75)], 3.0, GRAY)
    c.circle(hub, 3.6, fill=GRAY)
    for Sh, E, W in ((Ls, (34, 57), (33, 46)), (Rs, (66, 57), (67, 46))):
        c.stroke([Sh, E, W], LW * 0.9, GHOST)
    arms = [((26, 72), (15, 76)), ((74, 72), (85, 76))]
    legs = [((43.5, 26), (43, 9.5), (37.8, 9)), ((56.5, 26), (57, 9.5), (62.2, 9))]
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    for x in (23, 77):
        pill(c, (x, 68.5), (x, 79.5), 5)
    c.arrow((15, 56), (15, 68))
    c.arrow((85, 56), (85, 68))


def low_row(c):
    GHOST = mix(BODY, WHITE, 0.72)
    p = side((34, 30), 86, 88, arm=(-150, -15), leg=(4, -64, 64))
    S = p["S"]
    W = p["arm"][1]
    floor(c, 6, 10, 96)
    c.stroke([(35, 23), (35, 6)], 3, GRAY)
    pill(c, (24, 25.3), (44, 25.3), 5.2)
    c.stroke([(88, 6), (88, 94)], 3.2, GRAY)
    pivot = (80, 90)
    c.stroke([(70, 94), (90, 94)], 3.2, GRAY)
    c.circle(pivot, 3.2, fill=GRAY)
    c.stroke([(47, 30), (55, 30), (88, 30)], 2.4, GRAYL)
    K, A, T = p["leg"]
    mid = ((A[0] + T[0]) / 2, (A[1] + T[1]) / 2)
    fp = fk(mid, -28, 4.2)
    pill(c, fk(fp, 62, 7.5), fk(fp, -118, 7.5), 4.4)
    Wg = fk(fk(S, -32, UA), -32, FA)
    c.stroke([S, fk(S, -32, UA), Wg], LW * 0.85, GHOST)
    c.stroke([pivot, Wg], 2.2, GRAYL)
    draw_side(c, p)
    pill(c, (S[0] + 9.5, 36), (S[0] + 9.5, 60), 6.0)
    c.stroke([pivot, (W[0] + 1.5, W[1] + 2)], 3.0, GRAY)
    pl = (pivot[0] + (W[0] - pivot[0]) * 0.42, pivot[1] + (W[1] - pivot[1]) * 0.42)
    c.circle(pl, 8.5, fill=GRAY)
    c.circle(pl, 5.6, fill=GRAYL)
    c.circle(pl, 1.8, fill=WHITE)
    c.stroke([S, p["arm"][0], W], LW, BODY)
    pill(c, (W[0] + 1.2, W[1] - 4.5), (W[0] + 1.2, W[1] + 3.5), 3.4)
    c.arrow((86, 47), (67, 47))


def hack_squat(c):
    p = side((42, 42), 110, 100, arm=(-60, 55), leg=(10, -100, 0))
    H, S = p["H"], p["S"]
    floor(c, 6, 8, 92)
    c.stroke([fk(H, 110, -22), fk(S, 110, 30)], 2.6, GRAYL)
    c.stroke([fk(H, 110, -22), (18, 6)], 2.6, GRAY)
    hb, sb = fk(H, 200, 6.6), fk(S, 200, 6.6)
    pill(c, fk(hb, 110, -4), fk(sb, 110, 4), 5.2)
    pill(c, (50, 23.5), (76, 23.5), 4.2)
    c.stroke([(70, 23.5), (70, 6)], 2.6, GRAY)
    draw_side(c, p)
    sp = fk(S, 40, 4.2)
    pill(c, fk(sp, 200, 4), fk(sp, 20, 6.5), 4.6)
    W = p["arm"][1]
    pill(c, fk(W, 110, 3.5), fk(W, -70, 3.5), 3.2)
    a0 = (82, 50)
    c.arrow(a0, fk(a0, 110, 16))


def incline_machine_press(c):
    p = side((36, 30), 112, 105, arm=(20, 25), leg=(0, -90, 0))
    H, S = p["H"], p["S"]
    W = p["arm"][1]
    floor(c, 6.5, 12, 92)
    c.stroke([(37, 23), (37, 6.5)], 3, GRAY)
    pill(c, (26, 25.3), (46, 25.3), 5.2)
    hb, sb = fk(H, 202, 6.6), fk(S, 202, 6.6)
    pill(c, fk(hb, 112, -3), fk(sb, 112, 5), 5.2)
    piv = (40, 90)
    c.stroke([W, piv], 2.6, GRAY)
    c.circle(piv, 2.6, fill=GRAY)
    draw_side(c, p)
    pill(c, fk(W, 115, 5), fk(W, -65, 5), 3.4)
    a0 = (66, 60)
    c.arrow(a0, fk(a0, 25, 16))


def cable_pullover(c):
    GHOST = mix(BODY, WHITE, 0.72)
    GBAR = mix(GRAY, WHITE, 0.55)
    head, Ls, Rs, Lh, Rh = (50, 61), (40.5, 49), (59.5, 49), (44, 27), (56, 27)
    floor(c, 4, 22, 78)
    c.stroke([(36, 97), (64, 97)], 3.0, GRAY)
    pulley(c, (50, 93.5))

    def ez(y, col, w=3.0):
        pts = [(23, y), (31, y), (35, y + 2.6), (39.5, y - 2.0), (44, y), (56, y),
               (60.5, y - 2.0), (65, y + 2.6), (69, y), (77, y)]
        c.stroke(pts, w, col)
    ez(31, GBAR, 2.6)
    for Sh, Hd in ((Ls, (39, 31.5)), (Rs, (61, 31.5))):
        c.stroke([Sh, Hd], LW * 0.85, GHOST)
    c.stroke([(50, 82.5), (50, 91)], 1.8, GRAY)
    arms = [((36.5, 64.5), (33, 80)), ((63.5, 64.5), (67, 80))]
    legs = [((43.5, 16), (43, 5.5), (37.8, 5)), ((56.5, 16), (57, 5.5), (62.2, 5))]
    draw_front(c, head, Ls, Rs, Lh, Rh, arms, legs)
    ez(81.5, GRAY)
    c.arrow((15, 74), (15, 52))
    c.arrow((85, 74), (85, 52))


# ---------------------------------------------------------------- 2/2 (2026-10-26~)
def seated_row_machine(c):
    GHOST = mix(BODY, WHITE, 0.72)
    p = side((32, 30), 86, 88, arm=(-150, -15), leg=(4, -64, 64))
    S = p["S"]
    W = p["arm"][1]
    floor(c, 6, 8, 96)
    c.stroke([(33, 23), (33, 6)], 3, GRAY)
    pill(c, (22, 25.3), (42, 25.3), 5.2)
    x0, x1, y0, y1 = 85, 94, 9, 66
    c.stroke([(x0 - 1.5, 6), (x0 - 1.5, 90)], 2.2, GRAYL)
    c.stroke([(x1 + 1.5, 6), (x1 + 1.5, 90)], 2.2, GRAYL)
    for i in range(8):
        y = y0 + i * (y1 - y0) / 8
        c.rrect(x0, y + 0.8, x1, y + (y1 - y0) / 8 - 0.8, 1.0, fill=GRAY)
    py = y0 + 5.5 * (y1 - y0) / 8
    c.stroke([(x0 - 5, py), (x0 + 2, py)], 2.4, ARROW)
    c.circle((x0 - 5.5, py), 2.2, fill=ARROW)
    c.stroke([((x0 + x1) / 2, y1), ((x0 + x1) / 2, 88), (70, 88)], 1.6, GRAY)
    K, A, T = p["leg"]
    mid = ((A[0] + T[0]) / 2, (A[1] + T[1]) / 2)
    fp = fk(mid, -28, 4.2)
    pill(c, fk(fp, 62, 7.5), fk(fp, -118, 7.5), 4.4)
    piv = (70, 84)
    Wg = fk(fk(S, -20, UA), -20, FA)
    c.stroke([S, fk(S, -20, UA), Wg], LW * 0.85, GHOST)
    c.stroke([piv, Wg], 2.2, GRAYL)
    draw_side(c, p)
    pill(c, (S[0] + 9.5, 36), (S[0] + 9.5, 60), 6.0)
    c.stroke([piv, (W[0] + 1.5, W[1] + 2)], 3.0, GRAY)
    c.circle(piv, 2.8, fill=GRAY)
    c.stroke([S, p["arm"][0], W], LW, BODY)
    pill(c, (W[0] + 1.2, W[1] - 4.5), (W[0] + 1.2, W[1] + 3.5), 3.4)
    c.arrow((80, 74), (62, 74))


def _cable_seated_row(c, grip):
    GHOST = mix(BODY, WHITE, 0.72)
    H = (28, 26)
    p = side(H, 88, 90, arm=(-122, -2), leg=(-4, -22, 80))
    S = p["S"]
    W = p["arm"][1]
    floor(c, 6, 6, 96)
    c.rrect(10, 18, 62, 22.5, 2.2, fill=GRAY)
    c.stroke([(16, 18), (16, 6)], 2.6, GRAY)
    c.stroke([(56, 18), (56, 6)], 2.6, GRAY)
    c.stroke([(90, 6), (90, 40)], 3.2, GRAY)
    K, A, T = p["leg"]
    c.stroke([(A[0] + 3, A[1] - 6), (A[0] + 6, A[1] + 9)], 4.2, GRAY)
    pul = (85, 16)
    c.stroke([(90, 16), pul], 3, GRAY)
    pulley(c, pul)
    Wg = fk(fk(S, -24, UA), -24, FA)
    c.stroke([S, fk(S, -24, UA), Wg], LW * 0.85, GHOST)
    draw_side(c, p)
    c.stroke([(W[0] + 2, W[1] - 1), (pul[0] - 2.5, pul[1] + 1.5)], 1.6, GRAY)
    if grip == "v":
        c.poly([(W[0] + 0.5, W[1] + 3.5), (W[0] + 0.5, W[1] - 3.5), (W[0] + 6, W[1] - 1)], GRAY)
        c.stroke([S, p["arm"][0], W], LW, BODY)
    else:
        c.stroke([S, p["arm"][0], W], LW, BODY)
        c.circle((W[0] + 1.5, W[1] + 2.6), 3.4, fill=GRAY)
        c.circle((W[0] + 1.5, W[1] + 2.6), 1.2, fill=WHITE)
    c.arrow((80, 52), (62, 52))


def cable_seated_row(c):
    _cable_seated_row(c, "v")


def underhand_seated_row(c):
    _cable_seated_row(c, "bar")


def vertical_pulldown(c):
    p = side((50, 30), 92, 90, leg=(4, -70, 70))
    S = p["S"]
    Ef = fk(S, -135, UA)
    Wf = fk(Ef, 50, FA)
    p["far_arm"] = [Ef, Wf]
    Wn = (60, 85)
    En = ((S[0] + Wn[0]) / 2 - 0.8, (S[1] + Wn[1]) / 2)
    floor(c, 4, 4, 96)
    c.stroke([(51, 23), (51, 4)], 3, GRAY)
    pill(c, (40, 25.3), (62, 25.3), 5.2)
    c.stroke([(80, 4), (80, 38), (73, 40)], 2.6, GRAY)
    c.circle((71, 38.5), 4.0, fill=GRAY)
    piv = (22, 52)
    c.stroke([(22, 4), piv], 3.4, GRAY)
    c.stroke([(10, 4), (34, 4)], 3.4, GRAY)
    tail = (11, 38)

    def bz(p0, p1, p2, p3, n=30):
        return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * cc + t ** 3 * d
                      for a, b, cc, d in zip(p0, p1, p2, p3)) for t in (i / n for i in range(n + 1))]
    c.stroke(bz(piv, (20, 90), (44, 94), (Wf[0] + 3, Wf[1] + 5)), 2.2, GRAYL)
    c.stroke([piv, tail], 3.0, GRAY)
    c.circle(tail, 8.5, fill=GRAY)
    c.circle(tail, 5.6, fill=GRAYL)
    c.circle(tail, 1.8, fill=WHITE)
    draw_side(c, p)
    pill(c, (S[0] + 9, 38), (S[0] + 9, 56), 6.0)
    c.stroke(bz(piv, (18, 104), (52, 110), (Wn[0] + 2.5, Wn[1] + 4)), 3.0, GRAY)
    c.circle(piv, 3.2, fill=GRAY)
    c.stroke([S, En, Wn], LW, BODY)
    pill(c, (Wn[0] + 1, Wn[1] - 1), (Wn[0] + 4.5, Wn[1] + 6), 3.4)
    c.arrow((86, 86), (86, 66))


def db_bench_press(c):
    S, H = (34, 39), (59, 39)
    K = fk(H, 10, TH)
    A = fk(K, -85, SH)
    floor(c, 21.5, 4, 96)
    c.rrect(10, 31, 66, 35.6, 2.2, fill=GRAY)
    c.stroke([(16, 31), (16, 21.5)], 2.6, GRAY)
    c.stroke([(60, 31), (60, 21.5)], 2.6, GRAY)
    E = fk(S, 92, UA)
    W = fk(E, 90, FA)
    p = {"H": H, "S": S, "head": fk(S, 180, NECKH), "arm": [E, W], "leg": [K, A, fk(A, 0, FT)]}
    draw_side(c, p)
    dumbbell(c, (W[0], W[1] + 1.5), 0, 12)
    c.arrow((50, 58), (50, 74))


ICONS = {
    "face_pull": face_pull, "low_row": low_row, "cable_pullover": cable_pullover, "hack_squat": hack_squat,
    "incline_machine_press": incline_machine_press, "lateral_raise_standing": lateral_raise_standing,
    "leg_press": leg_press, "goblet_squat": goblet_squat, "leg_extension": leg_extension,
    "inner_thigh": inner_thigh, "back_extension": back_extension,
    "lat_pulldown": lat_pulldown, "underhand_pulldown": underhand_pulldown, "seated_row": seated_row,
    "shoulder_press": shoulder_press, "lateral_raise": lateral_raise, "plank": plank,
    "hip_thrust": hip_thrust, "db_rdl": db_rdl, "lying_leg_curl": lying_leg_curl,
    "outer_thigh": outer_thigh, "cable_kickback": cable_kickback,
    "chest_press": chest_press, "one_arm_row": one_arm_row, "reverse_pec_deck": reverse_pec_deck,
    "cable_pushdown": cable_pushdown, "dead_bug": dead_bug,
    "treadmill": treadmill, "stair_climber": stair_climber, "bike": bike, "walk": walk, "rest": rest,
    "smith_squat": smith_squat, "lateral_raise_machine": lateral_raise_machine,
    "seated_leg_curl": seated_leg_curl, "high_row": high_row,
    "bench_press": bench_press, "incline_db_press": incline_db_press, "pec_deck": pec_deck,
    "db_curl": db_curl, "overhead_ext": overhead_ext, "shrug": shrug,
    "straight_arm_pulldown": straight_arm_pulldown, "foam_roller": foam_roller,
    "smith_incline_press": smith_incline_press,
    "outer_thigh_pin": outer_thigh_pin, "outer_thigh_plate": outer_thigh_plate,
    "seated_row_machine": seated_row_machine, "cable_seated_row": cable_seated_row,
    "underhand_seated_row": underhand_seated_row, "vertical_pulldown": vertical_pulldown,
    "db_bench_press": db_bench_press,
    "dumbbell": dumbbell_icon, "pencil": pencil, "heart": heart,
}


def main(out_dir, size=192):
    """웹용: 연한 테마색 타일 버전만, size px로 저장"""
    os.makedirs(out_dir, exist_ok=True)
    for name, fn in ICONS.items():
        c = Canvas()
        fn(c)
        path = f"{out_dir}/{name}.png"
        c.save(path, tile=TILE)
        Image.open(path).resize((size, size), Image.LANCZOS).save(path, optimize=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets")
