# 인체모형 v3 (짐토스 도당점 PT 자세 복습지) — 2026-10-13
# v2.3 대비: 외곽선·체형 현실화(목·팔·허리·허벅지), 머리(턱선·귀), 소흉근·요방형근·이상근(심부),
# 내전근 세분화(장내전근·대내전근·박근·치골근), 장경인대, 척추 홈·흉요근막·기립근 두 기둥, 둥근 대둔근,
# 심부근 칠하기 순서(진핑크가 연핑크 위)
# 사용: build(path, front_hl, back_hl, title="오늘의 운동 자극 부위", sex="M"/"F")
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
from scipy.interpolate import splprep, splev
from matplotlib import font_manager

_KO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if os.path.exists(_KO):
    font_manager.fontManager.addfont(_KO)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=_KO).get_name()

OUTLINE   = "#8C867E"
LINE      = "#9E978D"
BODY      = "#FFFFFF"
PRIMARY   = "#DB4C8C"
PRIMARY_E = "#A82E63"
SECOND    = "#F4B3CE"
SECOND_E  = "#C97FA4"
LABELBG   = "#6E6A64"

# 외곽선(오른쪽 절반, 남성 기준). HEAD = 정수리→귀→턱각→목 (Catmull-Rom 촘촘한 점으로 그림)
HEAD = [
    (0.000, 8.000), (0.112, 7.988), (0.208, 7.951), (0.281, 7.888),
    (0.328, 7.803), (0.350, 7.700), (0.353, 7.615), (0.347, 7.555),
    (0.360, 7.562), (0.382, 7.558), (0.400, 7.535), (0.411, 7.492),
    (0.411, 7.434), (0.401, 7.378), (0.384, 7.332), (0.364, 7.302),
    (0.343, 7.292),
    (0.324, 7.270), (0.309, 7.236), (0.293, 7.205), (0.277, 7.181),
    (0.261, 7.163), (0.247, 7.146),
]
_NECK_ARM = [
    (0.240, 7.100), (0.238, 7.020), (0.252, 6.945), (0.292, 6.905),
    (0.460, 6.825), (0.650, 6.748), (0.840, 6.652), (0.980, 6.580),
    (1.100, 6.545), (1.205, 6.488), (1.292, 6.375), (1.372, 6.170),
    (1.386, 5.985), (1.368, 5.790), (1.445, 5.560), (1.488, 5.390),
    (1.524, 5.170), (1.622, 4.920), (1.690, 4.610), (1.740, 4.300),
    (1.780, 4.050),
]
_ARM_IN_TO_ANKLE = [
    (1.612, 4.050), (1.500, 4.300), (1.384, 4.600), (1.288, 4.900),
    (1.250, 5.160), (1.118, 5.400), (1.048, 5.600), (0.990, 5.800),
    (0.950, 5.950), (0.919, 6.100),
    (0.890, 5.840), (0.835, 5.580), (0.745, 5.350), (0.672, 5.150),
    (0.655, 4.970), (0.690, 4.730), (0.728, 4.520), (0.752, 4.280),
    (0.770, 4.080),
    (0.786, 3.860), (0.800, 3.520), (0.778, 3.080), (0.698, 2.620),
    (0.600, 2.280), (0.546, 2.070),
    (0.586, 1.850), (0.614, 1.600), (0.580, 1.300), (0.486, 0.960),
    (0.378, 0.620),
]
_LEG_IN = [
    (0.098, 0.780), (0.112, 1.040), (0.110, 1.260), (0.114, 1.480),
    (0.136, 1.680), (0.166, 1.860), (0.188, 1.970),
    (0.184, 2.120), (0.156, 2.280), (0.140, 2.460), (0.136, 2.660),
    (0.118, 2.900), (0.080, 3.350), (0.054, 3.750), (0.048, 3.980),
]
def mirror(P):
    P = np.asarray(P, float).copy()
    P[:, 0] *= -1
    return P

def _dedupe(pts, tol=1e-9):
    out = []
    for q in pts:
        if not out or abs(q[0] - out[-1][0]) > tol or abs(q[1] - out[-1][1]) > tol:
            out.append(tuple(q))
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < tol and abs(out[0][1] - out[-1][1]) < tol:
        out.pop()
    return out

def _arm_contours():
    """남성 기준 팔 바깥/안쪽 곡선 (팔 좌표 A 계산용)"""
    half = [tuple(p) for p in HALF]
    full = _dedupe(half + [(-x, y) for (x, y) in half][::-1])
    p = np.array(full + [full[0]], float)
    tck, u = splprep([p[:, 0], p[:, 1]], s=0, per=True, k=3)
    ao = np.column_stack(splev(np.linspace(u[I_ARM_OUT[0]], u[I_ARM_OUT[1]], 900), tck))
    ai = np.column_stack(splev(np.linspace(u[I_ARM_IN[0]], u[I_ARM_IN[1]], 900), tck))
    return ao, ai

def A(y, t):
    """팔 좌표: y 높이에서 안쪽선(t=0) ~ 바깥선(t=1) 사이 비율 t 지점"""
    xo = float(np.interp(y, _AO[:, 1], _AO[:, 0]))
    xi = float(np.interp(y, _AI[:, 1], _AI[:, 0]))
    return (xi + t * (xo - xi), float(y))

def cr(P, closed=False, step=0.004):
    P = np.asarray(P, float)
    n = len(P)
    if n == 2 and not closed:
        m = max(2, int(np.ceil(np.linalg.norm(P[1] - P[0]) / step)))
        t = np.linspace(0, 1, m + 1)[:, None]
        return P[0] + t * (P[1] - P[0]), [0, m]
    if closed:
        E = np.vstack([P[-1], P, P[0], P[1]])
        nseg = n
    else:
        E = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
        nseg = n - 1
    out = [E[1][None, :]]
    idx = [0]
    total = 1
    for i in range(nseg):
        p0, p1, p2, p3 = E[i], E[i + 1], E[i + 2], E[i + 3]
        t0 = 0.0
        t1 = t0 + max(np.linalg.norm(p1 - p0), 1e-9) ** 0.5
        t2 = t1 + max(np.linalg.norm(p2 - p1), 1e-9) ** 0.5
        t3 = t2 + max(np.linalg.norm(p3 - p2), 1e-9) ** 0.5
        m = max(3, int(np.ceil(np.linalg.norm(p2 - p1) / step)))
        t = np.linspace(t1, t2, m + 1)[1:][:, None]
        a1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
        a2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
        a3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
        b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
        b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3
        c = (t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2
        c[-1] = p2
        out.append(c)
        total += len(c)
        idx.append(total - 1)
    return np.vstack(out), idx

_HW, _HD, _HN = (1.696, 4.05), (0.1961, -0.9805), (0.9805, 0.1961)

def H(u, v):
    return (_HW[0] + u * _HD[0] + v * _HN[0], _HW[1] + u * _HD[1] + v * _HN[1])

HAND_UV = [
    (0.07, 0.110), (0.16, 0.150), (0.26, 0.178), (0.35, 0.190), (0.42, 0.186),
    (0.462, 0.172), (0.478, 0.150), (0.462, 0.132), (0.415, 0.128),
    (0.388, 0.124), (0.376, 0.117), (0.382, 0.110), (0.40, 0.107),
    (0.44, 0.106), (0.53, 0.106), (0.60, 0.106),
    (0.640, 0.103), (0.658, 0.090), (0.664, 0.076), (0.660, 0.058),
    (0.664, 0.049),
    (0.684, 0.044), (0.702, 0.034), (0.709, 0.018), (0.704, 0.001),
    (0.690, -0.009),
    (0.694, -0.020), (0.695, -0.038), (0.688, -0.054), (0.660, -0.064),
    (0.636, -0.068),
    (0.642, -0.092), (0.630, -0.110), (0.60, -0.118),
    (0.56, -0.122), (0.47, -0.126), (0.37, -0.128), (0.26, -0.122),
    (0.15, -0.108), (0.06, -0.090),
]

FOOT = [
    (0.338, 0.49), (0.322, 0.43), (0.334, 0.375), (0.336, 0.345),
    (0.326, 0.30), (0.332, 0.24), (0.350, 0.16), (0.366, 0.09),
    (0.372, 0.045), (0.360, 0.012), (0.30, 0.002), (0.20, 0.0),
    (0.12, 0.002), (0.082, 0.018), (0.066, 0.06), (0.060, 0.14),
    (0.058, 0.23), (0.052, 0.33), (0.047, 0.39), (0.052, 0.44),
    (0.064, 0.50), (0.076, 0.55),
]

def _run(ctrl, nxt, nxt2, step=0.004):
    """머리처럼 굴곡 많은 외곽: 좌우 대칭 Catmull-Rom 촘촘한 점"""
    pts, idx = cr([(-ctrl[1][0], ctrl[1][1])] + list(ctrl) + [nxt, nxt2], step=step)
    return [tuple(map(float, p)) for p in pts[idx[1]:idx[len(ctrl) + 1]]]

def _between(a, mids, b, step=0.004):
    pts = cr([a] + list(mids) + [b], step=step)[0]
    return [tuple(map(float, p)) for p in pts[1:-1]]

_HEADRUN = _run(HEAD, _NECK_ARM[0], _NECK_ARM[1])
_HAND = _between(_NECK_ARM[-1], [H(u, v) for u, v in HAND_UV], _ARM_IN_TO_ANKLE[0])
_FOOT = _between(_ARM_IN_TO_ANKLE[-1], FOOT, _LEG_IN[0])
HALF = _HEADRUN + _NECK_ARM + _HAND + _ARM_IN_TO_ANKLE + _FOOT + _LEG_IN

_nh = len(_HEADRUN)
_n0 = _nh + len(_NECK_ARM) - 1
_n1 = _n0 + len(_HAND) + 1
_n2 = _nh + len(_NECK_ARM) + len(_HAND) + len(_ARM_IN_TO_ANKLE) - 1
_n3 = _n2 + len(_FOOT) + 1
DENSE_RUNS = [(0, _nh), (_n0, _n1), (_n2, _n3)]
I_ARM_OUT = (HALF.index((1.100, 6.545)), HALF.index((1.780, 4.050)))
I_ARM_IN = (HALF.index((1.612, 4.050)), HALF.index((0.919, 6.100)))

ARM_OUT, ARM_IN = _arm_contours()
_AO = ARM_OUT[np.argsort(ARM_OUT[:, 1])]
_AI = ARM_IN[np.argsort(ARM_IN[:, 1])]

PROF_Y = [0.0, 0.70, 2.10, 2.60, 3.60, 4.30, 4.70, 5.30, 5.80, 6.30,
          6.70, 7.05, 8.00]
PROF_S = [0.88, 0.86, 0.92, 0.96, 1.05, 1.16, 1.08, 0.84, 0.90, 0.92,
          0.86, 0.88, 0.92]
SHOULDER_X, SHOULDER_F, ARM_FX = 0.98, 0.86, 0.90
CROTCH, CROTCH_F = 4.00, 4.12

def _fy(y):
    if y <= CROTCH:
        return y * (CROTCH_F / CROTCH)
    return CROTCH_F + (y - CROTCH) * (8.0 - CROTCH_F) / (8.0 - CROTCH)

def _ss(z):
    z = min(max(z, 0.0), 1.0)
    return z * z * (3 - 2 * z)

def femalize(pts):
    """v1 배율 그대로. 단, 겨드랑이 위(y>5.1)에서는 몸통→팔 규칙을
    x 0.70~1.00 구간에 걸쳐 부드럽게 섞어 선이 꺾이지 않게 함"""
    out = []
    for x, y in pts:
        s = 1.0 if x >= 0 else -1.0
        ax = abs(x)
        body = ax * float(np.interp(y, PROF_Y, PROF_S))
        arm = SHOULDER_X * SHOULDER_F + (ax - SHOULDER_X) * ARM_FX
        if 3.30 < y < 6.62:
            w = _ss((ax - 0.70) / 0.30) if y > 5.1 else (1.0 if ax > 0.85 else 0.0)
        else:
            w = 0.0
        out.append((s * ((1 - w) * body + w * arm), _fy(y)))
    return out

class Pt(tuple):
    """이미 대상 체형 좌표로 변환된 점 표시"""

class Space:
    """체형별 좌표계: 제어점을 먼저 변형한 뒤 곡선을 그린다 (v1 방식)"""

    def __init__(self, sex="M"):
        self.sex = sex
        half = [tuple(p) for p in self.f(HALF)]
        n = len(half)
        full = _dedupe(half + [(-x, y) for (x, y) in half][::-1])
        p = np.array(full + [full[0]], float)
        tck, u = splprep([p[:, 0], p[:, 1]], s=0, per=True, k=3)
        m = len(full)

        def hidx(j):
            return j if j < n else 2 * n - 1 - j

        def dense(j):
            a, b = hidx(j), hidx((j + 1) % m)
            return any(lo <= a <= hi and lo <= b <= hi for lo, hi in DENSE_RUNS)

        segs = []
        for j in range(m):
            if dense(j):
                segs.append(p[j][None, :])
            else:
                k = max(2, int(np.ceil(np.linalg.norm(p[j + 1] - p[j]) / 0.002)))
                t = np.linspace(u[j], u[j + 1], k, endpoint=False)
                segs.append(np.column_stack(splev(t, tck)))
        self.body = np.vstack(segs)
        self.rh = np.vstack(segs[:n - 1] + [p[n - 1][None, :]])

    def f(self, P):
        P = [tuple(map(float, q)) for q in P]
        return P if self.sex == "M" else femalize(P)

    def y(self, y):
        return y if self.sex == "M" else _fy(y)

class Net:
    """근육 경계선 네트워크. 이웃한 근육은 같은 선을 공유한다.
    입력 좌표는 남성 기준, 내부 곡선은 대상 체형 좌표."""

    def __init__(self, sp):
        self.sp = sp
        self.c = {}

    def P(self, p):
        if isinstance(p, Pt):
            return tuple(p)
        return tuple(self.sp.f([p])[0])

    def add(self, name, pts):
        Q = [self.P(p) for p in pts]
        d, idx = cr(Q)
        self.c[name] = (d, idx, Q)

    def _ci(self, name, key):
        d, idx, Q = self.c[name]
        if isinstance(key, (int, np.integer)):
            return idx[key]
        k = self.P(key)
        for i, q in enumerate(Q):
            if abs(q[0] - k[0]) < 1e-9 and abs(q[1] - k[1]) < 1e-9:
                return idx[i]
        j = int(np.argmin(((d - np.asarray(k)) ** 2).sum(1)))
        if np.hypot(d[j, 0] - k[0], d[j, 1] - k[1]) < 0.012:
            return j
        raise KeyError(f"{name}: {key} 는 곡선 위의 점이 아님")

    def cut(self, name, p):
        """곡선 name 위에서 p에 가장 가까운 점 (제어점이 아닌 곳에서 가지를 칠 때)"""
        d = self.c[name][0]
        q = np.asarray(self.P(p))
        j = int(np.argmin(((d - q) ** 2).sum(1)))
        return Pt((float(d[j, 0]), float(d[j, 1])))

    def seg(self, name, a, b):
        d = self.c[name][0]
        ia, ib = self._ci(name, a), self._ci(name, b)
        return d[ia:ib + 1] if ia <= ib else d[ib:ia + 1][::-1]

    def snap(self, p):
        q = np.asarray(self.P(p))
        i = int(np.argmin(((self.sp.rh - q) ** 2).sum(1)))
        return Pt((float(self.sp.rh[i, 0]), float(self.sp.rh[i, 1])))

    def out(self, a, b):
        o = self.sp.rh
        ia = int(np.argmin(((o - np.asarray(self.P(a))) ** 2).sum(1)))
        ib = int(np.argmin(((o - np.asarray(self.P(b))) ** 2).sum(1)))
        return o[ia:ib + 1] if ia <= ib else o[ib:ia + 1][::-1]

    def at_y(self, name, y):
        d = self.c[name][0]
        i = int(np.argmin(np.abs(d[:, 1] - self.sp.y(y))))
        return Pt((float(d[i, 0]), float(d[i, 1])))

    def line(self, pts):
        return cr([self.P(p) for p in pts])[0]

    def closed(self, pts):
        return cr([self.P(p) for p in pts], closed=True)[0]

    def region(self, *parts):
        segs = []
        prev_lit = True
        for p in parts:
            lit = p[0] == "P"
            if p[0] == "O":
                s = self.out(p[1], p[2])
            elif lit:
                s = np.asarray([self.P(q) for q in p[1:]], float)
            else:
                s = self.seg(*p)
            if segs and not (lit or prev_lit):
                gap = np.linalg.norm(segs[-1][-1] - s[0])
                if gap > 0.02:
                    raise ValueError(f"경계 끊김 {gap:.3f} @ {p[0]}")
            segs.append(s)
            prev_lit = lit
        P = np.vstack(segs)
        keep = np.ones(len(P), bool)
        keep[1:] = np.linalg.norm(np.diff(P, axis=0), axis=1) > 1e-9
        return P[keep]

def build_front(sex="M"):
    sp = Space(sex)
    N = Net(sp)
    s = N.snap
    R, L, D, C = {}, {}, [], []

    P_SCM_TOP = s((0.250, 7.124))
    P_SCM_M_BOT = (0.039, 6.741)
    P_SCM_CL = (0.124, 6.738)
    P_TR_CL = (0.605, 6.669)
    P_CLAV_DP = (0.683, 6.655)
    P_ACROM = s((1.035, 6.567))
    P_NECK_TR = s((0.252, 6.945))
    N.add("clav", [P_SCM_M_BOT, P_SCM_CL, (0.260, 6.725), (0.428, 6.696),
                   P_TR_CL, P_CLAV_DP, (0.819, 6.629), (0.940, 6.601), P_ACROM])
    N.add("scm_l", [P_SCM_TOP, (0.222, 7.030), (0.180, 6.905), (0.146, 6.790),
                    P_SCM_CL])
    N.add("scm_m", [P_SCM_TOP, (0.193, 7.053), (0.132, 6.943), (0.074, 6.821),
                    P_SCM_M_BOT])
    R["scm"] = [N.region(("scm_l", 0, -1), ("clav", P_SCM_CL, P_SCM_M_BOT),
                         ("scm_m", -1, 0))]
    N.add("trap_fb", [P_NECK_TR, (0.315, 6.798), (0.430, 6.724), P_TR_CL])
    R["trap_up"] = [N.region(("O", P_NECK_TR, P_ACROM),
                             ("clav", P_ACROM, P_TR_CL),
                             ("trap_fb", P_TR_CL, P_NECK_TR))]
    D.append(N.line([(0.284, 7.192), (0.252, 7.130), (0.205, 7.080), (0.140, 7.045),
                     (0.075, 7.028), (0.000, 7.022)]))      # 턱선

    P_PEC_TIP = (1.064, 6.028)
    P_DV = s((1.368, 5.790))
    P_BIC_LAT_TOP = (1.261, 5.845)
    N.add("dp", [P_CLAV_DP, (0.758, 6.527), (0.854, 6.374), (0.953, 6.215),
                 P_PEC_TIP, (1.150, 5.926), P_BIC_LAT_TOP, P_DV])
    P_AXV = s((0.919, 6.100))
    P_TRIF_TOP = (0.969, 6.067)
    P_STERN_LOW = (0.034, 5.866)
    if sex == "F":
        P_SERR_TOP = (0.752, 5.715)
        P_RA_TOP = (0.298, 5.609)
        N.add("pec_low", [P_PEC_TIP, (1.011, 6.052), P_TRIF_TOP, P_AXV,
                          (0.881, 6.001), (0.822, 5.866), P_SERR_TOP, (0.638, 5.616),
                          (0.479, 5.582), P_RA_TOP, (0.184, 5.688), (0.097, 5.789),
                          P_STERN_LOW])
    else:
        P_SERR_TOP = (0.624, 5.893)
        P_RA_TOP = (0.300, 5.830)
        N.add("pec_low", [P_PEC_TIP, (1.011, 6.052), P_TRIF_TOP, P_AXV,
                          (0.871, 6.039), (0.787, 5.972), (0.704, 5.922), P_SERR_TOP,
                          (0.475, 5.849), P_RA_TOP, (0.147, 5.833), P_STERN_LOW])
    P_PEC_DIV_M = (0.042, 6.600)
    N.add("stern", [P_SCM_M_BOT, P_PEC_DIV_M, (0.045, 6.250), P_STERN_LOW])
    N.add("pec_div", [P_PEC_DIV_M, (0.220, 6.520), (0.460, 6.425), (0.702, 6.304),
                      (0.929, 6.139), P_PEC_TIP])
    R["pec_clav"] = [N.region(("clav", P_SCM_M_BOT, P_CLAV_DP),
                              ("dp", P_CLAV_DP, P_PEC_TIP),
                              ("pec_div", P_PEC_TIP, P_PEC_DIV_M),
                              ("stern", P_PEC_DIV_M, P_SCM_M_BOT))]
    R["pec_stern"] = [N.region(("pec_div", P_PEC_DIV_M, P_PEC_TIP),
                               ("pec_low", P_PEC_TIP, P_STERN_LOW),
                               ("stern", P_STERN_LOW, P_PEC_DIV_M))]
    N.add("delt_div", [P_ACROM, (1.120, 6.435), (1.203, 6.246), (1.276, 6.041),
                       (1.338, 5.886), P_DV])
    R["delt_ant"] = [N.region(("clav", P_CLAV_DP, P_ACROM),
                              ("delt_div", P_ACROM, P_DV),
                              ("dp", P_DV, P_CLAV_DP))]
    R["delt_lat"] = [N.region(("delt_div", P_ACROM, P_DV), ("O", P_DV, P_ACROM))]

    P_BRM_TOP = A(5.48, 0.12)
    P_EL_IN = s(A(5.20, 0.0))
    N.add("tri_f", [P_TRIF_TOP, A(5.90, 0.14), A(5.66, 0.14), P_BRM_TOP,
                    A(5.33, 0.06), P_EL_IN])
    R["triceps_long"] = [N.region(("pec_low", P_AXV, P_TRIF_TOP),
                                  ("tri_f", P_TRIF_TOP, P_EL_IN),
                                  ("O", P_EL_IN, P_AXV))]
    P_BIC_TEND = A(5.16, 0.50)
    N.add("bic_med", [P_BRM_TOP, A(5.38, 0.23), A(5.26, 0.37), P_BIC_TEND])
    N.add("bic_lat", [P_BIC_LAT_TOP, A(5.68, 0.80), A(5.48, 0.78),
                      A(5.32, 0.68), P_BIC_TEND])
    N.add("bic_mid", [P_PEC_TIP, A(5.78, 0.47), A(5.54, 0.51), A(5.34, 0.51),
                      P_BIC_TEND])
    R["biceps_short"] = [N.region(("pec_low", P_TRIF_TOP, P_PEC_TIP),
                                  ("bic_mid", P_PEC_TIP, P_BIC_TEND),
                                  ("bic_med", P_BIC_TEND, P_BRM_TOP),
                                  ("tri_f", P_BRM_TOP, P_TRIF_TOP))]
    R["biceps_long"] = [N.region(("dp", P_PEC_TIP, P_BIC_LAT_TOP),
                                 ("bic_lat", P_BIC_LAT_TOP, P_BIC_TEND),
                                 ("bic_mid", P_BIC_TEND, P_PEC_TIP))]
    P_BRR_TOP = s(A(5.48, 1.0))
    N.add("brr_up", [P_BRR_TOP, A(5.34, 0.83), A(5.24, 0.68), P_BIC_TEND])
    N.add("flex_top", [P_EL_IN, A(5.16, 0.22), P_BIC_TEND])
    R["brachialis"] = [
        N.region(("dp", P_BIC_LAT_TOP, P_DV), ("O", P_DV, P_BRR_TOP),
                 ("brr_up", P_BRR_TOP, P_BIC_TEND),
                 ("bic_lat", P_BIC_TEND, P_BIC_LAT_TOP)),
        N.region(("tri_f", P_BRM_TOP, P_EL_IN), ("flex_top", P_EL_IN, P_BIC_TEND),
                 ("bic_med", P_BIC_TEND, P_BRM_TOP)),
    ]

    P_WR_IN = s(A(4.08, 0.0))
    P_WR_M = A(4.075, 0.74)
    P_WR_OUT = s(A(4.09, 1.0))
    N.add("wrist_f", [P_WR_IN, A(4.065, 0.35), P_WR_M, P_WR_OUT])
    N.add("fx_br", [P_BIC_TEND, A(4.95, 0.57), A(4.65, 0.62), A(4.36, 0.68),
                    A(4.18, 0.72), P_WR_M])
    R["forearm_flex"] = [N.region(("flex_top", P_EL_IN, P_BIC_TEND),
                                  ("fx_br", P_BIC_TEND, P_WR_M),
                                  ("wrist_f", P_WR_M, P_WR_IN),
                                  ("O", P_WR_IN, P_EL_IN))]
    R["brachioradialis"] = [N.region(("brr_up", P_BRR_TOP, P_BIC_TEND),
                                     ("fx_br", P_BIC_TEND, P_WR_M),
                                     ("wrist_f", P_WR_M, P_WR_OUT),
                                     ("O", P_WR_OUT, P_BRR_TOP))]
    L["forearm_flex"] = [N.line([A(5.13, 0.08), A(4.95, 0.28), A(4.77, 0.46),
                                N.at_y("fx_br", 4.62)])]

    P_SERR_LOW = (0.763, 5.505)
    P_LATF_BOT = s((0.684, 5.214))
    N.add("latf", [P_AXV, (0.877, 5.945), (0.831, 5.788), (0.799, 5.622), P_SERR_LOW,
                   (0.734, 5.391), (0.707, 5.292), P_LATF_BOT])
    if sex == "F":
        zig = [P_SERR_TOP, (0.762, 5.610), P_SERR_LOW]
    else:
        zig = [P_SERR_TOP, (0.561, 5.815), (0.663, 5.804), (0.599, 5.722),
               (0.703, 5.711), (0.645, 5.629), (0.738, 5.616), (0.690, 5.543),
               P_SERR_LOW]
    N.add("so_zig", zig)
    R["serratus"] = [N.region(("pec_low", P_AXV, P_SERR_TOP),
                              ("so_zig", P_SERR_TOP, P_SERR_LOW),
                              ("latf", P_SERR_LOW, P_AXV))]
    R["lat"] = [N.region(("latf", P_AXV, P_LATF_BOT), ("O", P_LATF_BOT, P_AXV))]

    P_ASIS = (0.571, 4.708)
    P_ILC_F = s((0.676, 4.860))
    P_RA_VL = (0.155, 4.215)
    P_PUBT = (0.085, 4.135)
    N.add("vline", [P_ILC_F, P_ASIS, (0.464, 4.588), (0.356, 4.456), (0.252, 4.325),
                    P_RA_VL, P_PUBT])
    if sex == "F":
        N.add("ra_lat", [P_RA_TOP, (0.321, 5.421), (0.341, 5.218), (0.318, 5.050),
                         (0.285, 4.780), (0.230, 4.500), P_RA_VL])
    else:
        N.add("ra_lat", [P_RA_TOP, (0.322, 5.600), (0.330, 5.330), (0.318, 5.050),
                         (0.285, 4.780), (0.230, 4.500), P_RA_VL])
    N.add("pubis", [P_PUBT, (0.040, 4.118), (0.000, 4.112)])
    R["abs"] = [N.region(("P", (0.000, 5.866)),
                         ("pec_low", P_STERN_LOW, P_RA_TOP),
                         ("ra_lat", P_RA_TOP, P_RA_VL),
                         ("vline", P_RA_VL, P_PUBT),
                         ("pubis", P_PUBT, (0.000, 4.112)))]
    L["abs"] = []
    for y0 in ((5.345, 5.070) if sex == "F" else (5.600, 5.325, 5.050)):
        e = N.at_y("ra_lat", y0 + 0.022)
        L["abs"].append(N.line([(0.0, y0), (0.13, y0 + 0.012), (0.24, y0 + 0.02), e]))
    C.append(N.closed([(0.000, 4.985), (0.018, 4.955), (0.000, 4.922),
                           (-0.018, 4.955)]))
    R["oblique"] = [N.region(("pec_low", P_RA_TOP, P_SERR_TOP),
                             ("so_zig", P_SERR_TOP, P_SERR_LOW),
                             ("latf", P_SERR_LOW, P_LATF_BOT),
                             ("O", P_LATF_BOT, P_ILC_F),
                             ("vline", P_ILC_F, P_RA_VL),
                             ("ra_lat", P_RA_VL, P_RA_TOP))]

    P_TFL_BOT = s((0.784, 3.803))
    N.add("tfl_med", [P_ASIS, (0.583, 4.451), (0.642, 4.200), (0.707, 3.980), P_TFL_BOT])
    R["tfl"] = [N.region(("vline", P_ILC_F, P_ASIS), ("tfl_med", P_ASIS, P_TFL_BOT),
                         ("O", P_TFL_BOT, P_ILC_F))]
    P_RF_BOT = (0.377, 2.350)
    P_FT_APEX = (0.386, 3.781)
    P_VM_TOP = (0.337, 3.262)
    N.add("rf_lat", [P_ASIS, (0.557, 4.401), (0.563, 3.950), (0.540, 3.461),
                     (0.503, 2.959), (0.442, 2.588), P_RF_BOT])
    N.add("rf_med", [P_ASIS, (0.499, 4.431), (0.444, 4.120), P_FT_APEX, (0.348, 3.454),
                     P_VM_TOP, (0.312, 2.948), (0.311, 2.682), (0.327, 2.484), P_RF_BOT])
    R["rectus_fem"] = [N.region(("rf_lat", P_ASIS, P_RF_BOT), ("rf_med", P_RF_BOT, P_ASIS))]
    P_VL_KNEE = s((0.588, 2.218))
    N.add("vl_low", [P_RF_BOT, (0.441, 2.318), (0.509, 2.273), P_VL_KNEE])
    # 장경인대: 대퇴근막장근 끝에서 무릎 바깥까지
    P_ITB_F = N.cut("vl_low", (0.545, 2.250))
    N.add("itb_f", [P_TFL_BOT, (0.752, 3.550), (0.740, 3.200), (0.700, 2.850),
                    (0.630, 2.500), P_ITB_F])
    R["itb"] = [N.region(("itb_f", P_TFL_BOT, P_ITB_F),
                         ("vl_low", P_ITB_F, P_VL_KNEE),
                         ("O", P_VL_KNEE, P_TFL_BOT))]
    R["vastus_lat"] = [N.region(("tfl_med", P_ASIS, P_TFL_BOT),
                                ("itb_f", P_TFL_BOT, P_ITB_F),
                                ("vl_low", P_ITB_F, P_RF_BOT),
                                ("rf_lat", P_RF_BOT, P_ASIS))]
    P_VM_IN = s((0.123, 2.870))
    P_VM_KNEE = s((0.185, 2.140))
    N.add("vm_med", [P_VM_TOP, (0.266, 3.118), (0.190, 2.989), P_VM_IN])
    N.add("vm_low", [P_RF_BOT, (0.313, 2.291), (0.249, 2.214), P_VM_KNEE])
    R["vastus_med"] = [N.region(("rf_med", P_VM_TOP, P_RF_BOT),
                                ("vm_low", P_RF_BOT, P_VM_KNEE),
                                ("O", P_VM_KNEE, P_VM_IN),
                                ("vm_med", P_VM_IN, P_VM_TOP))]
    P_CROTCH = s((0.048, 3.980))
    P_PEC_UP = (0.252, 4.325)
    P_AL_TOP = (0.062, 4.060)
    P_AL_END = (0.348, 3.454)
    P_GR_END = (0.190, 2.989)
    N.add("add_lat", [P_PUBT, (0.170, 4.000), (0.268, 3.875), P_FT_APEX])
    N.add("groin", [P_CROTCH, P_AL_TOP, P_PUBT])
    P_PEC_LO = N.cut("add_lat", (0.325, 3.830))
    N.add("pect_l", [P_PEC_UP, (0.286, 4.080), P_PEC_LO])
    N.add("addl_m", [P_AL_TOP, (0.120, 3.880), (0.200, 3.690), (0.280, 3.535), P_AL_END])
    N.add("grac_f", [P_AL_TOP, (0.082, 3.800), (0.118, 3.470), (0.150, 3.180), P_GR_END])
    R["iliopsoas"] = [N.region(("vline", P_ASIS, P_PEC_UP),
                               ("pect_l", P_PEC_UP, P_PEC_LO),
                               ("add_lat", P_PEC_LO, P_FT_APEX),
                               ("rf_med", P_FT_APEX, P_ASIS))]
    R["pectineus"] = [N.region(("vline", P_PEC_UP, P_PUBT),
                               ("add_lat", P_PUBT, P_PEC_LO),
                               ("pect_l", P_PEC_LO, P_PEC_UP))]
    R["add_long"] = [N.region(("groin", P_AL_TOP, P_PUBT),
                              ("add_lat", P_PUBT, P_FT_APEX),
                              ("rf_med", P_FT_APEX, P_AL_END),
                              ("addl_m", P_AL_END, P_AL_TOP))]
    R["add_mag"] = [N.region(("addl_m", P_AL_TOP, P_AL_END),
                             ("rf_med", P_AL_END, P_VM_TOP),
                             ("vm_med", P_VM_TOP, P_GR_END),
                             ("grac_f", P_GR_END, P_AL_TOP))]
    R["gracilis"] = [N.region(("groin", P_CROTCH, P_AL_TOP),
                              ("grac_f", P_AL_TOP, P_GR_END),
                              ("vm_med", P_GR_END, P_VM_IN),
                              ("O", P_VM_IN, P_CROTCH))]
    D.append(N.closed([(0.364, 2.303), (0.431, 2.261), (0.450, 2.156),
                           (0.421, 2.043), (0.364, 1.998), (0.308, 2.043),
                           (0.278, 2.149), (0.294, 2.255)]))

    P_TIB_TOP = (0.347, 1.882)
    P_TIB_LAT_TOP = (0.474, 1.927)
    P_TIB_BOT = (0.190, 0.440)
    P_TIB_BOT2 = (0.240, 0.450)
    N.add("tib_med", [P_TIB_TOP, (0.336, 1.624), (0.314, 1.303), (0.278, 0.959),
                      (0.230, 0.660), P_TIB_BOT])
    N.add("tib_lat", [P_TIB_LAT_TOP, (0.472, 1.649), (0.440, 1.310), (0.384, 0.979),
                      (0.315, 0.680), P_TIB_BOT2])
    N.add("tib_top", [P_TIB_TOP, (0.408, 1.932), P_TIB_LAT_TOP])
    N.add("tib_bot", [P_TIB_BOT, P_TIB_BOT2])
    R["tibialis"] = [N.region(("tib_top", P_TIB_TOP, P_TIB_LAT_TOP),
                              ("tib_lat", P_TIB_LAT_TOP, P_TIB_BOT2),
                              ("tib_bot", P_TIB_BOT2, P_TIB_BOT),
                              ("tib_med", P_TIB_BOT, P_TIB_TOP))]
    P_FIB = s((0.562, 1.955))
    P_ANK_OUT = s((0.325, 0.440))
    N.add("per_top", [P_TIB_LAT_TOP, (0.516, 1.959), P_FIB])
    N.add("per_bot", [P_TIB_BOT2, (0.285, 0.445), P_ANK_OUT])
    R["peroneus"] = [N.region(("per_top", P_TIB_LAT_TOP, P_FIB),
                              ("O", P_FIB, P_ANK_OUT),
                              ("per_bot", P_ANK_OUT, P_TIB_BOT2),
                              ("tib_lat", P_TIB_BOT2, P_TIB_LAT_TOP))]
    P_TMB_TOP = s((0.188, 1.975))
    P_GSF_M = (0.169, 1.139)
    P_GSF_O = s((0.115, 1.020))
    P_TMB_BOT = (0.118, 0.520)
    P_SOLF_BOT = s((0.080, 0.570))
    N.add("tibia_mb", [P_TMB_TOP, (0.204, 1.800), (0.190, 1.551), (0.174, 1.300),
                       P_GSF_M, (0.160, 0.920), (0.140, 0.700), P_TMB_BOT])
    N.add("gs_f", [P_GSF_M, (0.140, 1.075), P_GSF_O])
    N.add("solf_bot", [P_TMB_BOT, P_SOLF_BOT])
    R["gastroc_med"] = [N.region(("tibia_mb", P_TMB_TOP, P_GSF_M),
                                 ("gs_f", P_GSF_M, P_GSF_O),
                                 ("O", P_GSF_O, P_TMB_TOP))]
    R["soleus_f"] = [N.region(("tibia_mb", P_GSF_M, P_TMB_BOT),
                              ("solf_bot", P_TMB_BOT, P_SOLF_BOT),
                              ("O", P_SOLF_BOT, P_GSF_O),
                              ("gs_f", P_GSF_O, P_GSF_M))]

    DEEP = {"subscapularis": [N.closed([(0.352, 6.580), (0.600, 6.543), (0.858, 6.451),
                                        (1.017, 6.378), (1.073, 6.359), (1.068, 6.308),
                                        (0.977, 6.291), (0.843, 6.203), (0.653, 6.073),
                                        (0.438, 5.977), (0.373, 6.103), (0.345, 6.350)])],
            "pec_minor": [N.closed([(0.865, 6.455), (0.760, 6.410), (0.620, 6.330),
                                    (0.505, 6.262), (0.470, 6.180), (0.468, 6.080),
                                    (0.500, 5.985), (0.548, 5.955), (0.640, 6.060),
                                    (0.745, 6.230), (0.825, 6.380)])]}
    return dict(R=R, L=L, D=D, C=C, DEEP=DEEP, body=sp.body)

def build_back(sex="M"):
    sp = Space(sex)
    N = Net(sp)
    s = N.snap
    R, L, D, C = {}, {}, [], []
    DEEP = {}

    P_NECK_TR = s((0.252, 6.945))
    P_ACROM = s((1.035, 6.567))
    P_DV = s((1.368, 5.790))

    P_OCC = (0.000, 7.218)
    P_OCC_L = (0.095, 7.226)
    P_DIA_T = (0.000, 6.964)
    P_DIA_L = (0.092, 6.797)
    P_DIA_B = (0.000, 6.640)
    N.add("nuchal", [P_OCC, (0.048, 7.225), P_OCC_L])
    N.add("tb_neck", [P_OCC_L, (0.160, 7.160), (0.214, 7.060), (0.240, 6.990),
                      P_NECK_TR])
    N.add("dia_up", [P_DIA_L, (0.046, 6.884), P_DIA_T])
    N.add("dia_lo", [P_DIA_B, (0.039, 6.707), P_DIA_L])

    N.add("trap_ud", [P_DIA_L, (0.291, 6.741), (0.526, 6.663), (0.779, 6.607), P_ACROM])
    R["trap_up"] = [N.region(("nuchal", P_OCC, P_OCC_L),
                             ("tb_neck", P_OCC_L, P_NECK_TR),
                             ("O", P_NECK_TR, P_ACROM),
                             ("trap_ud", P_ACROM, P_DIA_L),
                             ("dia_up", P_DIA_L, P_DIA_T))]
    P_ROOT = (0.289, 6.399)
    P_T4 = (0.000, 6.350)
    P_PD_ORG = (0.560, 6.472)
    P_LT_TA = (0.221, 6.389)
    N.add("sspine", [P_ROOT, (0.420, 6.435), P_PD_ORG, (0.719, 6.516), (0.879, 6.555),
                     P_ACROM])

    N.add("trap_ml", [P_T4, (0.139, 6.372), P_LT_TA, P_ROOT])
    R["trap_mid"] = [N.region(("trap_ud", P_DIA_L, P_ACROM),
                              ("sspine", P_ACROM, P_ROOT),
                              ("trap_ml", P_ROOT, P_T4),
                              ("P", P_DIA_B),
                              ("dia_lo", P_DIA_B, P_DIA_L))]
    P_LT_LAT = (0.203, 5.899)
    P_LT_ERE = (0.073, 5.540)
    P_T12 = (0.000, 5.450)
    P_LT_TB = (0.280, 6.300)
    N.add("trap_lb", [P_ROOT, P_LT_TB, (0.265, 6.161), P_LT_LAT, (0.135, 5.699),
                      P_LT_ERE, P_T12])

    N.add("lt_tend", [P_LT_TA, (0.256, 6.338), P_LT_TB])
    R["trap_low"] = [N.region(("trap_ml", P_T4, P_LT_TA),
                              ("lt_tend", P_LT_TA, P_LT_TB),
                              ("trap_lb", P_LT_TB, P_T12))]

    P_IL_M = (0.343, 6.023)
    P_INF = (0.401, 5.940)
    N.add("scap_m", [P_ROOT, (0.309, 6.181), P_IL_M, P_INF])
    P_TMIN_M = (0.509, 6.078)
    P_TMIN_A = (0.861, 6.269)
    P_TMIN_B = (0.953, 6.202)
    P_LH_TOP = (0.996, 6.166)
    P_AXV = s((0.919, 6.100))
    P_TRI_TOP = (1.111, 6.039)
    N.add("pd_low", [P_PD_ORG, (0.680, 6.389), (0.781, 6.322), P_TMIN_A, P_TMIN_B,
                     P_LH_TOP, P_TRI_TOP, (1.239, 5.897), P_DV])
    N.add("inf_low", [P_IL_M, (0.436, 6.056), P_TMIN_M, (0.630, 6.134), (0.756, 6.196),
                      P_TMIN_A])
    N.add("tmin_low", [P_TMIN_M, (0.613, 6.062), (0.732, 6.087), (0.855, 6.134), P_TMIN_B])
    N.add("lh_med", [P_AXV, (0.957, 6.130), P_LH_TOP])
    P_LAT_TS = s((0.902, 5.998))
    N.add("lat_top", [P_LT_LAT, (0.301, 5.906), P_INF, (0.566, 5.964), (0.739, 5.985),
                      P_LAT_TS])
    R["infraspinatus"] = [N.region(("sspine", P_ROOT, P_PD_ORG),
                                   ("pd_low", P_PD_ORG, P_TMIN_A),
                                   ("inf_low", P_TMIN_A, P_IL_M),
                                   ("scap_m", P_IL_M, P_ROOT))]
    R["teres_minor"] = [N.region(("inf_low", P_TMIN_M, P_TMIN_A),
                                 ("pd_low", P_TMIN_A, P_TMIN_B),
                                 ("tmin_low", P_TMIN_B, P_TMIN_M))]
    R["teres_major"] = [N.region(("scap_m", P_IL_M, P_INF),
                                 ("lat_top", P_INF, P_LAT_TS),
                                 ("O", P_LAT_TS, P_AXV),
                                 ("lh_med", P_AXV, P_LH_TOP),
                                 ("pd_low", P_LH_TOP, P_TMIN_B),
                                 ("tmin_low", P_TMIN_B, P_TMIN_M),
                                 ("inf_low", P_TMIN_M, P_IL_M))]
    R["rhomboid"] = [N.region(("trap_lb", P_ROOT, P_LT_LAT),
                              ("lat_top", P_LT_LAT, P_INF),
                              ("scap_m", P_INF, P_ROOT))]
    N.add("delt_div", [P_ACROM, (1.120, 6.435), (1.203, 6.246), (1.276, 6.041),
                       (1.338, 5.886), P_DV])
    R["delt_post"] = [N.region(("sspine", P_PD_ORG, P_ACROM),
                               ("delt_div", P_ACROM, P_DV),
                               ("pd_low", P_DV, P_PD_ORG))]
    R["delt_lat"] = [N.region(("delt_div", P_ACROM, P_DV), ("O", P_DV, P_ACROM))]

    P_SUP = (0.313, 6.626)
    N.add("scap_up", [P_ROOT, (0.296, 6.510), P_SUP])

    P_GT_S1 = (1.104, 6.500)
    P_GT_S2 = (1.146, 6.458)
    P_GT_I2 = (1.171, 6.395)
    P_GT_M2 = (1.164, 6.332)
    P_SSP88 = (0.879, 6.555)
    N.add("gt_cap", [P_GT_S1, P_GT_S2, P_GT_I2, P_GT_M2])
    N.add("supra_top", [P_SUP, (0.504, 6.634), (0.721, 6.615), (0.920, 6.589),
                        (1.019, 6.543), P_GT_S1])
    N.add("supra_low", [P_SSP88, (0.998, 6.515), P_GT_S2])
    DEEP["supraspinatus"] = [N.region(("supra_top", P_SUP, P_GT_S1),
                                      ("gt_cap", P_GT_S1, P_GT_S2),
                                      ("supra_low", P_GT_S2, P_SSP88),
                                      ("sspine", P_SSP88, P_ROOT),
                                      ("scap_up", P_ROOT, P_SUP))]
    N.add("inf_deep_top", [P_PD_ORG, (0.758, 6.495), (0.918, 6.496), (1.048, 6.473), P_GT_S2])
    N.add("inf_deep_mid", [P_TMIN_A, (0.977, 6.312), (1.078, 6.362), P_GT_I2])
    N.add("tmin_deep_low", [P_TMIN_B, (1.037, 6.240), (1.109, 6.288), P_GT_M2])
    DEEP["infraspinatus"] = [N.region(("pd_low", P_PD_ORG, P_TMIN_A),
                                      ("inf_deep_mid", P_TMIN_A, P_GT_I2),
                                      ("gt_cap", P_GT_I2, P_GT_S2),
                                      ("inf_deep_top", P_GT_S2, P_PD_ORG))]
    DEEP["teres_minor"] = [N.region(("pd_low", P_TMIN_A, P_TMIN_B),
                                    ("tmin_deep_low", P_TMIN_B, P_GT_M2),
                                    ("gt_cap", P_GT_M2, P_GT_I2),
                                    ("inf_deep_mid", P_GT_I2, P_TMIN_A))]
    DEEP["rhomboid"] = [N.region(("P", (0.033, 6.800)), ("scap_up", P_SUP, P_ROOT),
                                 ("trap_lb", P_ROOT, (0.265, 6.161)),
                                 ("P", (0.028, 6.270)))]
    DEEP["levator"] = [N.closed([(0.137, 7.092), (0.205, 7.083), (0.249, 6.907),
                                     (0.306, 6.674), P_SUP, (0.273, 6.650),
                                     (0.196, 6.821), (0.154, 7.009)])]
    DEEP["erector_thoracic"] = [N.closed([(0.031, 6.741), (0.135, 6.743),
                                              (0.171, 6.400), (0.187, 6.000),
                                              (0.164, 5.639), (0.098, 5.500),
                                              (0.028, 5.480)])]

    P_LSIDE = s((0.763, 5.412))
    P_LAT_ILC = (0.564, 4.809)
    P_ILC_B = s((0.685, 4.850))
    P_TLF_C = (0.441, 4.750)          # 흉요근막 다이아몬드 바깥 꼭짓점 (장골능 위)
    P_GMX_TOP = (0.233, 4.645)
    P_PSIS = (0.162, 4.605)
    N.add("lat_side", [P_LSIDE, (0.715, 5.253), (0.643, 5.097), (0.584, 4.958),
                       P_LAT_ILC])
    N.add("crest", [P_ILC_B, P_LAT_ILC, P_TLF_C, (0.323, 4.689), P_GMX_TOP,
                    P_PSIS])
    N.add("ere_lat", [P_LT_ERE, (0.145, 5.380), (0.190, 5.150), (0.205, 4.920),
                      (0.192, 4.739), P_PSIS])
    N.add("tlf", [P_LT_ERE, (0.185, 5.330), (0.265, 5.120), (0.345, 4.920), P_TLF_C])
    R["lat"] = [N.region(("trap_lb", P_LT_ERE, P_LT_LAT),
                         ("lat_top", P_LT_LAT, P_LAT_TS),
                         ("O", P_LAT_TS, P_LSIDE),
                         ("lat_side", P_LSIDE, P_LAT_ILC),
                         ("crest", P_LAT_ILC, P_TLF_C),
                         ("tlf", P_TLF_C, P_LT_ERE))]
    R["oblique"] = [N.region(("lat_side", P_LSIDE, P_LAT_ILC),
                             ("crest", P_LAT_ILC, P_ILC_B),
                             ("O", P_ILC_B, P_LSIDE))]
    P_SAC_TOP = (0.000, 4.550)
    N.add("sac_top", [P_PSIS, (0.079, 4.563), P_SAC_TOP])
    # 척추 가운데 홈: 기립근 두 기둥 사이 흰 띠
    P_GR_T = N.cut("trap_lb", (0.022, 5.477))
    P_GR_B = N.cut("sac_top", (0.022, 4.552))
    N.add("groove", [P_GR_T, (0.023, 5.200), (0.023, 4.850), P_GR_B])
    R["erector"] = [N.region(("trap_lb", P_GR_T, P_LT_ERE),
                             ("ere_lat", P_LT_ERE, P_PSIS),
                             ("sac_top", P_PSIS, P_GR_B),
                             ("groove", P_GR_B, P_GR_T))]
    DEEP["ql"] = [N.closed([(0.080, 5.470), (0.200, 5.452), (0.315, 5.420),
                            (0.345, 5.250), (0.375, 5.050), (0.410, 4.850),
                            (0.430, 4.758), (0.330, 4.702), (0.215, 4.660),
                            (0.120, 4.655), (0.092, 4.880), (0.084, 5.180)])]

    P_GMX_LAT = s((0.775, 4.000))
    N.add("gmx_top", [P_GMX_TOP, (0.380, 4.560), (0.520, 4.440), (0.640, 4.290),
                      (0.725, 4.130), P_GMX_LAT])
    R["glute_med"] = [N.region(("crest", P_ILC_B, P_GMX_TOP),
                               ("gmx_top", P_GMX_TOP, P_GMX_LAT),
                               ("O", P_GMX_LAT, P_ILC_B))]
    P_COCCYX = (0.000, 4.240)
    N.add("sac_edge", [P_PSIS, (0.119, 4.470), (0.065, 4.330), P_COCCYX])
    # 대둔근 아래선: 가운데가 가장 낮고 바깥으로 올라가는 둥근 곡선
    P_GMX_LOW = s((0.780, 3.950))
    P_BF_TOP = (0.600, 3.815)
    P_HS = (0.358, 3.756)
    P_ST_TOP = (0.162, 3.786)
    P_GF_IN = s((0.059, 3.860))
    N.add("gfold", [P_GMX_LOW, (0.725, 3.915), (0.665, 3.858), P_BF_TOP, (0.487, 3.772),
                    P_HS, (0.253, 3.762), P_ST_TOP, P_GF_IN])
    P_CROTCH = s((0.048, 3.980))
    R["glute_max"] = [N.region(("crest", P_GMX_TOP, P_PSIS),
                               ("sac_edge", P_PSIS, P_COCCYX),
                               ("P", (0.000, 3.978)),
                               ("O", P_CROTCH, P_GF_IN),
                               ("gfold", P_GF_IN, P_GMX_LOW),
                               ("O", P_GMX_LOW, P_GMX_LAT),
                               ("gmx_top", P_GMX_LAT, P_GMX_TOP))]
    DEEP["piriformis"] = [N.closed([(0.072, 4.470), (0.180, 4.430), (0.340, 4.350),
                                    (0.500, 4.250), (0.640, 4.140), (0.722, 4.075),
                                    (0.715, 4.030), (0.630, 4.075), (0.480, 4.165),
                                    (0.320, 4.255), (0.170, 4.330), (0.065, 4.370)])]

    P_BF_BOT = (0.506, 2.109)
    P_POP_TOP = (0.405, 2.556)
    N.add("bf_lat", [P_BF_TOP, (0.671, 3.467), (0.670, 3.078), (0.620, 2.677),
                     (0.554, 2.356), P_BF_BOT])
    N.add("ham_mid", [P_HS, (0.390, 3.355), (0.402, 2.951), P_POP_TOP])
    N.add("pop_lat", [P_POP_TOP, (0.441, 2.369), (0.473, 2.219), P_BF_BOT])
    R["ham_bf"] = [N.region(("gfold", P_BF_TOP, P_HS), ("ham_mid", P_HS, P_POP_TOP),
                            ("pop_lat", P_POP_TOP, P_BF_BOT),
                            ("bf_lat", P_BF_BOT, P_BF_TOP))]
    P_ST_BOT = (0.256, 2.082)
    N.add("st_med", [P_ST_TOP, (0.191, 3.451), (0.203, 3.048), (0.207, 2.680),
                     (0.224, 2.340), P_ST_BOT])
    N.add("pop_med", [P_POP_TOP, (0.353, 2.364), (0.299, 2.199), P_ST_BOT])
    R["ham_st"] = [N.region(("gfold", P_HS, P_ST_TOP), ("st_med", P_ST_TOP, P_ST_BOT),
                            ("pop_med", P_ST_BOT, P_POP_TOP),
                            ("ham_mid", P_POP_TOP, P_HS))]
    P_GL_TOP_O = s((0.558, 2.039))
    P_GM_TOP_M = s((0.188, 1.984))
    N.add("kn_lat", [P_BF_BOT, P_GL_TOP_O])
    N.add("kn_med", [P_ST_BOT, P_GM_TOP_M])
    # 장경인대: 대둔근 바깥 끝에서 무릎 바깥까지 가는 띠
    P_ITB_B = s((0.590, 2.230))
    N.add("itb_b", [P_GMX_LOW, (0.742, 3.700), (0.736, 3.350), (0.700, 2.950),
                    (0.648, 2.580), P_ITB_B])
    R["itb"] = [N.region(("itb_b", P_GMX_LOW, P_ITB_B), ("O", P_ITB_B, P_GMX_LOW))]
    R["vastus_lat"] = [N.region(("gfold", P_GMX_LOW, P_BF_TOP),
                                ("bf_lat", P_BF_TOP, P_BF_BOT),
                                ("kn_lat", P_BF_BOT, P_GL_TOP_O),
                                ("O", P_GL_TOP_O, P_ITB_B),
                                ("itb_b", P_ITB_B, P_GMX_LOW))]
    # 내전근: 대내전근(가운데) / 박근(안쪽 띠)
    P_GB_TOP = N.cut("gfold", (0.105, 3.822))
    P_AM_END = (0.224, 2.340)
    N.add("grac_b", [P_GB_TOP, (0.125, 3.500), (0.155, 3.100), (0.190, 2.700),
                     P_AM_END])
    R["add_mag"] = [N.region(("gfold", P_ST_TOP, P_GB_TOP),
                             ("grac_b", P_GB_TOP, P_AM_END),
                             ("st_med", P_AM_END, P_ST_TOP))]
    R["gracilis"] = [N.region(("gfold", P_GB_TOP, P_GF_IN),
                              ("O", P_GF_IN, P_GM_TOP_M),
                              ("kn_med", P_GM_TOP_M, P_ST_BOT),
                              ("st_med", P_ST_BOT, P_AM_END),
                              ("grac_b", P_AM_END, P_GB_TOP))]

    P_POP_BOT = (0.372, 1.933)
    N.add("gm_top", [P_ST_BOT, (0.302, 2.014), P_POP_BOT])
    N.add("gl_top", [P_BF_BOT, (0.444, 2.019), P_POP_BOT])
    P_GL_END = (0.342, 1.304)
    N.add("gc_mid", [P_POP_BOT, (0.384, 1.684), (0.368, 1.467), P_GL_END])
    P_ACH_TOP = (0.267, 1.049)
    P_GM_BOT_M = s((0.115, 1.140))
    N.add("gm_low", [P_GL_END, (0.330, 1.150), P_ACH_TOP, (0.194, 1.054), P_GM_BOT_M])
    P_GL_BOT_O = s((0.590, 1.439))
    N.add("gl_low", [P_GL_END, (0.401, 1.256), (0.481, 1.277), (0.547, 1.348), P_GL_BOT_O])
    R["gastroc_med"] = [N.region(("gm_top", P_ST_BOT, P_POP_BOT),
                                 ("gc_mid", P_POP_BOT, P_GL_END),
                                 ("gm_low", P_GL_END, P_GM_BOT_M),
                                 ("O", P_GM_BOT_M, P_GM_TOP_M),
                                 ("kn_med", P_GM_TOP_M, P_ST_BOT))]
    R["gastroc_lat"] = [N.region(("gl_top", P_BF_BOT, P_POP_BOT),
                                 ("gc_mid", P_POP_BOT, P_GL_END),
                                 ("gl_low", P_GL_END, P_GL_BOT_O),
                                 ("O", P_GL_BOT_O, P_GL_TOP_O),
                                 ("kn_lat", P_GL_TOP_O, P_BF_BOT))]
    P_ACHM_SOL = (0.218, 0.620)
    P_ACHL_SOL = (0.293, 0.640)
    P_HEEL_M = (0.205, 0.300)
    P_HEEL_L = (0.285, 0.300)
    N.add("ach_m", [P_ACH_TOP, (0.239, 0.850), P_ACHM_SOL, (0.210, 0.450), P_HEEL_M])
    N.add("ach_l", [P_ACH_TOP, (0.297, 0.849), P_ACHL_SOL, (0.288, 0.450), P_HEEL_L])
    P_SOL_IN = s((0.085, 0.600))
    P_SOL_OUT = s((0.400, 0.700))
    N.add("sol_bm", [P_SOL_IN, (0.150, 0.585), P_ACHM_SOL])
    N.add("sol_bl", [P_ACHL_SOL, (0.340, 0.655), P_SOL_OUT])
    R["soleus"] = [
        N.region(("gm_low", P_ACH_TOP, P_GM_BOT_M), ("O", P_GM_BOT_M, P_SOL_IN),
                 ("sol_bm", P_SOL_IN, P_ACHM_SOL), ("ach_m", P_ACHM_SOL, P_ACH_TOP)),
        N.region(("gl_low", P_GL_BOT_O, P_GL_END), ("gm_low", P_GL_END, P_ACH_TOP),
                 ("ach_l", P_ACH_TOP, P_ACHL_SOL), ("sol_bl", P_ACHL_SOL, P_SOL_OUT),
                 ("O", P_SOL_OUT, P_GL_BOT_O)),
    ]
    D.append(N.seg("ach_m", P_ACHM_SOL, P_HEEL_M))
    D.append(N.seg("ach_l", P_ACHL_SOL, P_HEEL_L))

    P_TT_TOP = A(5.50, 0.52)
    N.add("tri_split", [P_TRI_TOP, A(5.75, 0.50), A(5.62, 0.51), P_TT_TOP])
    P_TLM = A(5.40, 0.40)
    P_TLL = A(5.32, 0.655)
    P_OLEC_M = A(5.17, 0.40)
    P_OLEC_L = A(5.17, 0.61)
    P_OLEC_B = A(5.145, 0.505)
    N.add("tt_m", [P_TT_TOP, P_TLM, A(5.28, 0.37), P_OLEC_M])
    N.add("tt_l", [P_TT_TOP, A(5.42, 0.645), P_TLL, P_OLEC_L])
    N.add("olec", [P_OLEC_M, P_OLEC_B, P_OLEC_L])
    P_LH_IN = s(A(5.52, 0.0))
    N.add("lh_low", [P_TLM, A(5.43, 0.22), A(5.475, 0.08), P_LH_IN])
    P_MH_IN = s(A(5.19, 0.0))
    N.add("mh_low", [P_OLEC_M, A(5.16, 0.22), P_MH_IN])
    P_LATH_OUT = s(A(5.45, 1.0))
    N.add("lath_low", [P_LATH_OUT, A(5.37, 0.80), P_TLL])
    R["triceps_long"] = [N.region(("pd_low", P_LH_TOP, P_TRI_TOP),
                                  ("tri_split", P_TRI_TOP, P_TT_TOP),
                                  ("tt_m", P_TT_TOP, P_TLM),
                                  ("lh_low", P_TLM, P_LH_IN),
                                  ("O", P_LH_IN, P_AXV),
                                  ("lh_med", P_AXV, P_LH_TOP))]
    R["triceps_med"] = [N.region(("lh_low", P_LH_IN, P_TLM),
                                 ("tt_m", P_TLM, P_OLEC_M),
                                 ("mh_low", P_OLEC_M, P_MH_IN),
                                 ("O", P_MH_IN, P_LH_IN))]
    R["triceps_lat"] = [N.region(("pd_low", P_TRI_TOP, P_DV),
                                 ("O", P_DV, P_LATH_OUT),
                                 ("lath_low", P_LATH_OUT, P_TLL),
                                 ("tt_l", P_TLL, P_TT_TOP),
                                 ("tri_split", P_TT_TOP, P_TRI_TOP))]

    P_BRB_END = s(A(4.35, 1.0))
    N.add("brr_b", [P_LATH_OUT, A(5.26, 0.80), A(5.00, 0.81), A(4.76, 0.86),
                    A(4.54, 0.93), P_BRB_END])
    P_WR_IN_B = s(A(4.08, 0.0))
    P_WR_BM = A(4.075, 0.18)
    P_WR_BO = s(A(4.09, 1.0))
    N.add("wrist_b", [P_WR_IN_B, P_WR_BM, A(4.065, 0.55), P_WR_BO])
    N.add("ext_flex", [P_OLEC_B, A(4.92, 0.40), A(4.62, 0.30), A(4.32, 0.22), P_WR_BM])
    R["brachioradialis"] = [N.region(("brr_b", P_LATH_OUT, P_BRB_END),
                                     ("O", P_BRB_END, P_LATH_OUT))]
    R["forearm_flex"] = [N.region(("mh_low", P_MH_IN, P_OLEC_M),
                                  ("olec", P_OLEC_M, P_OLEC_B),
                                  ("ext_flex", P_OLEC_B, P_WR_BM),
                                  ("wrist_b", P_WR_BM, P_WR_IN_B),
                                  ("O", P_WR_IN_B, P_MH_IN))]
    R["forearm_ext"] = [N.region(("olec", P_OLEC_B, P_OLEC_L),
                                 ("tt_l", P_OLEC_L, P_TLL),
                                 ("lath_low", P_TLL, P_LATH_OUT),
                                 ("brr_b", P_LATH_OUT, P_BRB_END),
                                 ("O", P_BRB_END, P_WR_BO),
                                 ("wrist_b", P_WR_BO, P_WR_BM),
                                 ("ext_flex", P_WR_BM, P_OLEC_B))]
    L["forearm_ext"] = [N.line([A(5.08, 0.66), A(4.80, 0.64), A(4.50, 0.62),
                               A(4.25, 0.62), A(4.11, 0.63)])]
    return dict(R=R, L=L, D=D, C=C, DEEP=DEEP, body=sp.body)

EDGE = {PRIMARY: PRIMARY_E, SECOND: SECOND_E}
LAYER = {SECOND: 3.0, PRIMARY: 3.4}

ALIAS = {
    "delt": ["delt_ant", "delt_lat", "delt_post"],
    "trap": ["trap_up", "trap_mid", "trap_low"],
    "pec": ["pec_clav", "pec_stern"],
    "biceps": ["biceps_long", "biceps_short"],
    "triceps": ["triceps_long", "triceps_lat", "triceps_med"],
    "forearm": ["forearm_flex", "forearm_ext", "brachioradialis"],
    "quad": ["rectus_fem", "vastus_lat", "vastus_med"],
    "glute": ["glute_max", "glute_med"],
    "hamstring": ["ham_bf", "ham_st"],
    "calf": ["gastroc_med", "gastroc_lat", "soleus", "soleus_f", "peroneus"],
    "teres": ["teres_major", "teres_minor"],
    "rotator": ["supraspinatus", "infraspinatus", "teres_minor", "subscapularis"],
    "rotator_cuff": ["supraspinatus", "infraspinatus", "teres_minor", "subscapularis"],
    "erector": ["erector", "erector_thoracic"],
    "scapula": ["rhomboid", "trap_mid", "trap_low"],
    "core": ["abs", "oblique"],
    "neck": ["scm"],
    "hip_flexor": ["iliopsoas"],
    "abductor": ["glute_med", "tfl"],
    "adductor": ["add_long", "add_mag", "gracilis", "pectineus"],
    "it_band": ["itb"],
    "hip_rotator": ["piriformis"],
    "quadratus_lumborum": ["ql"],
}

_DETAIL_BOTH = [
    [(0.350, 7.545), (0.357, 7.490), (0.358, 7.410), (0.351, 7.330)],
    [H(0.664, 0.049), H(0.55, 0.051), H(0.43, 0.053)],
    [H(0.690, -0.009), H(0.56, -0.009), H(0.43, -0.007)],
    [H(0.636, -0.068), H(0.55, -0.067), H(0.45, -0.066)],
]
_DETAIL_FRONT = [
    [H(0.377, 0.117), H(0.29, 0.082), H(0.19, 0.050), H(0.09, 0.024), H(0.03, 0.012)],
    [(0.185, 0.012), (0.183, 0.060), (0.179, 0.098)],
    [(0.235, 0.010), (0.234, 0.050), (0.231, 0.090)],
    [(0.280, 0.010), (0.280, 0.050), (0.278, 0.080)],
    [(0.322, 0.012), (0.323, 0.045), (0.322, 0.068)],
    [(0.072, 0.075), (0.125, 0.112), (0.179, 0.098)],
]
_DETAIL_BACK = [
    [H(0.377, 0.117), H(0.27, 0.112), H(0.17, 0.100)],
    [(0.150, 0.250), (0.158, 0.120), (0.195, 0.045), (0.245, 0.028), (0.292, 0.048),
     (0.318, 0.130), (0.318, 0.230)],
]
_GEO = {}

def _geo(view, sex):
    key = (view, sex)
    if key not in _GEO:
        g = build_front(sex) if view == "F" else build_back(sex)
        sp = Space(sex)
        dets = _DETAIL_BOTH + (_DETAIL_FRONT if view == "F" else _DETAIL_BACK)
        g["D"] = list(g["D"]) + [cr(sp.f(p))[0] for p in dets]
        _GEO[key] = g
    return _GEO[key]

def _expand(hl):
    out = {}
    for k, col in (hl or {}).items():
        for n in ALIAS.get(k, [k]):
            out[n] = col
    return out

def _both(P):
    P = np.asarray(P, float)
    return (P, mirror(P))

def _draw_view(ax, dx, view, hl, sex):
    g = _geo(view, sex)
    hl = _expand(hl)
    sh = np.array([dx, 0.0])
    body = g["body"] + sh
    bp = Polygon(body, closed=True, fc=BODY, ec="none", zorder=1)
    ax.add_patch(bp)

    def put(P, **kw):
        p = Polygon(P + sh, closed=True, joinstyle="round", capstyle="round", **kw)
        ax.add_patch(p)
        p.set_clip_path(bp)

    def line(P, **kw):
        q = P + sh
        l, = ax.plot(q[:, 0], q[:, 1], solid_joinstyle="round",
                     solid_capstyle="round", **kw)
        l.set_clip_path(bp)

    for name, polys in g["R"].items():
        col = hl.get(name)
        for P in polys:
            for Q in _both(P):
                if col:
                    put(Q, fc=col, ec=EDGE[col], lw=0.98, zorder=LAYER[col])
                else:
                    put(Q, fc="none", ec=LINE, lw=0.82, zorder=2)

    for name, lines in g["L"].items():
        col = hl.get(name)
        for P in lines:
            for Q in _both(P):
                line(Q, color=EDGE[col] if col else LINE,
                     lw=0.82 if col else 0.7, zorder=4)

    # 심부근: 칠하기는 색 순서대로(진핑크가 연핑크 위), 점선 테두리는 맨 위
    for name, polys in g["DEEP"].items():
        col = hl.get(name)
        if not col:
            continue
        for P in polys:
            for Q in _both(P):
                put(Q, fc=col, ec="none", alpha=0.92, zorder=LAYER[col] + 0.2)
                put(Q, fc="none", ec=EDGE[col], lw=0.98, ls="--", zorder=6)

    for P in g["D"]:
        for Q in _both(P):
            line(Q, color=LINE, lw=0.7, zorder=4)
    for P in g["C"]:
        line(P, color=LINE, lw=0.7, zorder=4)

    ax.add_patch(Polygon(body, closed=True, fc="none", ec=OUTLINE, lw=1.75,
                         joinstyle="round", zorder=5))

def build(path, front_hl=None, back_hl=None, title="오늘의 운동 자극 부위", sex="M"):
    fig, ax = plt.subplots(figsize=(5.4, 5.4), dpi=250)
    _draw_view(ax, -2.35, "F", front_hl, sex)
    _draw_view(ax, 2.35, "B", back_hl, sex)
    ax.add_patch(FancyBboxPatch((-1.85, 8.10), 3.7, 0.62,
                                boxstyle="round,pad=0.02,rounding_size=0.30",
                                facecolor=LABELBG, edgecolor="none", zorder=20))
    ax.text(0, 8.41, title, ha="center", va="center", color="white",
            fontsize=12, zorder=21)
    ax.text(-2.35, -0.62, "앞모습", ha="center", color="#7A756E", fontsize=9)
    ax.text(2.35, -0.62, "뒷모습", ha="center", color="#7A756E", fontsize=9)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-0.95, 8.8)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.subplots_adjust(0, 0, 1, 1)
    plt.savefig(path, facecolor="white", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    return path
