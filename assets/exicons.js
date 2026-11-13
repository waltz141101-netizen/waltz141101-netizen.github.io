/* 움직이는 운동 아이콘 (2026-11-10 트레이너 "시안D로 가자")
   - 종목마다 관절 좌표(0~100) 두 자세(p0 시작 · p1 끝)만 적어 두면, 사람·기구·자극 부위(분홍)를 SVG로 그리고 두 자세 사이를 반복해서 움직임(SMIL <animate>).
   - window.EXI.has(key) / EXI.svg(key, { sex:"M"|"F", cls, still:true(멈춘 그림) })
   - 여기 없는 아이콘 이름은 app.js가 예전 PNG(assets/icons/M|F/)를 그대로 씀. 종이 루틴일지는 계속 PNG.
   - 새 종목 추가: 아래 EX에 한 칸 추가(비슷한 종목을 복사해서 좌표만 고치기) → _tools/exicons_sheet.html 로 두 자세 확인. */
(function () {
  "use strict";
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]; }
  function off(p, dx, dy) { return [p[0] + dx, p[1] + dy]; }
  function unit(a, b) { var dx = b[0] - a[0], dy = b[1] - a[1], l = Math.sqrt(dx * dx + dy * dy) || 1; return [dx / l, dy / l]; }
  function perp(a, b) { var u = unit(a, b); return [-u[1], u[0]]; }
  function L(k, pts, w) { return { k: k, line: pts, w: w }; }
  function D(k, c, r) { return { k: k, dot: c, r: r }; }
  function R(k, c, r, w) { return { k: k, ring: c, r: r, w: w }; }
  function seg(a, b, f0, f1, w) { return { line: [mix(a, b, f0), mix(a, b, f1)], w: w }; }
  function floor(a, b) { return L("floor", [[a, 95], [b, 95]], 3); }
  function db(c, d, half) {   /* 옆에서 본 덤벨 */
    var a = [c[0] - d[0] * half, c[1] - d[1] * half], b = [c[0] + d[0] * half, c[1] + d[1] * half];
    var a2 = [c[0] - d[0] * (half - 3.2), c[1] - d[1] * (half - 3.2)], b2 = [c[0] + d[0] * (half - 3.2), c[1] + d[1] * (half - 3.2)];
    return [L("eq", [a, b], 2.6), L("eq", [a, a2], 8.5), L("eq", [b, b2], 8.5)];
  }
  function grip(p, h) { return L("eq", [[p[0], p[1] - (h || 6)], [p[0], p[1] + (h || 6)]], 3.6); }
  function mir(o) {   /* 왼쪽(…L)만 적으면 오른쪽(…R)은 좌우 대칭으로 — 이미 있던 오른쪽 값도 항상 왼쪽을 따라감 */
    var r = {}, k;
    for (k in o) r[k] = o[k];
    for (k in o) if (/L$/.test(k)) r[k.slice(0, -1) + "R"] = [100 - o[k][0], o[k][1]];
    return r;
  }
  function ext(a, b) { var r = {}, k; for (k in a) r[k] = a[k]; for (k in b) r[k] = b[k]; return r; }

  /* 기본 자세 */
  function stand(x) { return { head: [x, 13], sh: [x, 28], hip: [x, 56], kn: [x + 1, 75], ft: [x, 90], toe: [x + 8, 91] }; }
  function sit(hx, hy) { return { head: [hx - 1, hy - 43], sh: [hx - 2, hy - 28], hip: [hx, hy], kn: [hx + 19, hy + 1], ft: [hx + 20, hy + 24], toe: [hx + 28, hy + 25] }; }
  var FSTAND = mir({ head: [50, 14], shL: [40, 28], hipL: [44, 56], knL: [43, 74], ftL: [42, 90], toeL: [36, 91] });
  var FSIT = mir({ head: [50, 29], shL: [40, 42], hipL: [44, 70], knL: [36, 78], ftL: [36, 91], toeL: [30, 91] });
  var LIE = { head: [21, 57], sh: [32, 59], hip: [58, 60], kn: [73, 57], ft: [76, 82], toe: [83, 83] };
  var INC = { head: [25, 35], sh: [33, 45], hip: [52, 67], kn: [70, 62], ft: [73, 87], toe: [81, 88] };
  var SQ0 = { head: [49, 12], sh: [48, 26], hip: [48, 55], kn: [50, 74], ft: [48, 90], toe: [57, 91] };
  var SQ1 = { head: [55, 33], sh: [50, 46], hip: [33, 66], kn: [59, 68] };

  /* 뼈대 */
  var SIDE = [{ pts: ["hip", "kn", "ft", "toe"], w: 9 }, { pts: ["sh", "hip"], w: 13 }, { pts: ["sh", "el", "ha"], w: 7.5 }];
  var FLEGS = [{ pts: ["hipL", "knL", "ftL", "toeL"], w: 8 }, { pts: ["hipR", "knR", "ftR", "toeR"], w: 8 }];
  var FTORSO = { poly: ["shL", "shR", "hipR", "hipL"], w: 7 };
  var FARMS = [{ pts: ["shL", "elL", "haL"], w: 7.5 }, { pts: ["shR", "elR", "haR"], w: 7.5 }];
  var FARMS_O = [{ pts: ["shL", "elL", "haL"], w: 7.5, o: 1 }, { pts: ["shR", "elR", "haR"], w: 7.5, o: 1 }];
  var FRONT = FLEGS.concat([FTORSO]).concat(FARMS);
  var FARC = { elL: "shL", haL: "elL", elR: "shR", haR: "elR" };

  /* 기구 */
  function benchEq() { return [floor(8, 92), L("eq2", [[24, 70], [24, 93]], 3), L("eq2", [[56, 70], [56, 93]], 3), L("eq2", [[15, 68.5], [65, 68.5]], 6)]; }
  function inclineEq() { return [floor(10, 92), L("eq2", [[29, 56], [29, 93]], 3), L("eq2", [[53, 78], [53, 93]], 3), L("eq2", [[22.5, 44], [47, 73]], 5.5), L("eq2", [[46, 76.5], [62, 72]], 5.5)]; }
  function seatEq(hx, hy, back) {
    var a = [floor(hx - 16, hx + 40), L("eq2", [[hx + 4, hy + 10], [hx + 4, 93]], 3), L("eq2", [[hx - 7, hy + 7.5], [hx + 15, hy + 7.5]], 5)];
    if (back !== false) a.push(L("eq2", [[hx - 10, hy - 30], [hx - 8, hy + 4]], 5));
    return a;
  }
  function fseatEq() { return [{ k: "eq2", rect: [36.5, 34, 27, 46], r: 5 }, L("eq2", [[50, 80], [50, 93]], 3), L("eq2", [[34, 79.5], [66, 79.5]], 5), floor(24, 76)]; }
  function chestPolys(P) {
    return [{ poly: [[P.shL[0] + 1, P.shL[1] + 2], [48.6, P.shL[1] + 2], [48.6, P.shL[1] + 11], [P.shL[0] + 2.5, P.shL[1] + 11]], w: 2.4 },
      { poly: [[P.shR[0] - 1, P.shR[1] + 2], [51.4, P.shR[1] + 2], [51.4, P.shR[1] + 11], [P.shR[0] - 2.5, P.shR[1] + 11]], w: 2.4 }];
  }
  function latPolys(P) {
    return [{ poly: [[P.shL[0] - 1, P.shL[1] + 3], [P.shL[0] + 7, P.shL[1] + 5], [P.hipL[0] + 3, P.hipL[1] - 7], [P.hipL[0] - .5, P.hipL[1] - 5]], w: 3 },
      { poly: [[P.shR[0] + 1, P.shR[1] + 3], [P.shR[0] - 7, P.shR[1] + 5], [P.hipR[0] - 3, P.hipR[1] - 7], [P.hipR[0] + .5, P.hipR[1] - 5]], w: 3 }];
  }
  function delts(P) { return [{ dot: P.shL, r: 5.4 }, { dot: P.shR, r: 5.4 }]; }

  var EX = {};
  /* ---------- 가슴 ---------- */
  function benchLike(front, back) {
    return { t: 1, p0: ext(LIE, { el: [37, 50], ha: [34, 44] }), p1: { el: [33, 43], ha: [33, 27] }, bones: SIDE,
      hl: function (P) { return [seg(P.sh, P.hip, 0, .42, 13)]; },
      back: function (P) { return benchEq().concat(back ? back(P) : []); }, front: front };
  }
  function plateAt(P) { var c = [P.ha[0], P.ha[1] - 1]; return [R("eq", c, 8.5, 3.6), D("eq", c, 2.4)]; }
  EX.bench_press = benchLike(plateAt);
  EX.smith_bench_press = benchLike(plateAt, function () { return [L("eq2", [[33.5, 7], [33.5, 93]], 2.6)]; });
  EX.db_bench_press = benchLike(function (P) { return db([P.ha[0], P.ha[1] - 1], [1, 0], 8); });
  function inclineLike(front, back) {
    return { t: 1, p0: ext(INC, { el: [43, 43], ha: [37, 33] }), p1: { el: [36, 31], ha: [36, 15] }, bones: SIDE,
      hl: function (P) { return [seg(P.sh, P.hip, 0, .42, 13)]; },
      back: function (P) { return inclineEq().concat(back ? back(P) : []); }, front: front };
  }
  EX.incline_db_press = inclineLike(function (P) { return db([P.ha[0], P.ha[1] - 1], [1, 0], 8); });
  EX.smith_incline_press = inclineLike(plateAt, function () { return [L("eq2", [[36.5, 5], [36.5, 93]], 2.6)]; });
  function pressMachine(p0, p1) {
    return { t: .9, p0: ext(sit(36, 65), p0), p1: p1, bones: SIDE,
      hl: function (P) { return [seg(P.sh, P.hip, 0, .42, 13)]; },
      back: function (P) { return seatEq(36, 65).concat([L("eq2", [[44, 8], P.ha], 3), D("eq2", [44, 8], 3.2)]); },
      front: function (P) { return [grip(P.ha)]; } };
  }
  EX.chest_press = pressMachine({ el: [30, 50], ha: [45, 45] }, { el: [50, 43], ha: [64, 42] });
  /* 뉴텍 체스트 프레스 머신 (2026-11-10 OO님 영상 — 도당점 뉴텍은 누워서 미는 라잉 방식): 벤치에 누워, 머리 뒤 기둥에서 내려온 지렛대 손잡이를 가슴 위로 밀어 올림 */
  EX.lying_chest_press = benchLike(function (P) { return [D("eq", P.ha, 3.6)]; }, function (P) {
    return [L("eq2", [[9, 93], [11, 14]], 3.5), L("eq2", [[11, 14], P.ha], 3.2), D("eq2", [11, 14], 3.2)];
  });
  /* 인클라인 프레스 머신 (2026-11-10 "등받이 각도 45도로"): 등받이·상체 45도로 기대고, 손잡이를 등받이와 직각(위·앞)으로 밀어 올림 */
  EX.incline_machine_press = { t: .9,
    p0: { head: [18.5, 39.5], sh: [28, 50], hip: [48, 70], kn: [67, 70], ft: [68, 91], toe: [76, 92], el: [24, 65], ha: [37, 52] },
    p1: { el: [39, 41], ha: [47.5, 30.5] },
    bones: [{ pts: ["hip", "kn", "ft", "toe"], w: 9 }, { pts: ["sh", "hip"], w: 13 }, { hlHere: 1 }, { pts: ["sh", "el", "ha"], w: 7.5, o: 1 }],
    hl: function (P) { return [seg(P.sh, P.hip, 0, .42, 13)]; },
    back: function (P) { return [floor(8, 90), L("eq2", [[52, 80], [52, 93]], 3), L("eq2", [[41, 77.5], [63, 77.5]], 5.5), L("eq2", [[42.5, 76.5], [16.5, 50.5]], 5.5),
      L("eq2", [[30, 64], [30, 93]], 3), L("eq2", [[9, 93], [11, 8]], 3.5), L("eq2", [[11, 8], [30, 8]], 3), L("eq2", [[30, 8], P.ha], 3), D("eq2", [30, 8], 3.2)]; },
    front: function (P) { return [grip(P.ha)]; } };
  /* 펙덱 · 리버스 펙덱은 위에서 본 모습 (2026-11-10 "더 직관적이게, 헷갈리겠어") — 화면 위쪽이 앞.
     펙덱: 등받이가 등 뒤(아래), 팔을 벌렸다가 앞으로 모음, 가슴(앞쪽) 강조 / 리버스: 가슴 패드가 앞(위), 팔을 앞에서 뒤로 벌림, 등·어깨 뒤(뒤쪽) 강조 */
  function deckTop(rev) {
    var wide = rev ? { haL: [9, 67] } : { haL: [9, 58] }, front = { haL: [44, 20] };
    return { t: rev ? .85 : .8, headR: 9, headO: 1,
      p0: mir(ext({ head: [50, rev ? 58 : 62], tl: [36, 62], tr: [64, 62], shL: [31, 62] }, rev ? front : wide)), p1: mir(rev ? wide : front), arcs: { haL: "shL", haR: "shR" },
      fx: function (P) { P.elL = mix(P.shL, P.haL, .5); P.elR = mix(P.shR, P.haR, .5); },
      bones: [{ pts: ["shL", "elL", "haL"], w: 8 }, { pts: ["shR", "elR", "haR"], w: 8 }, { pts: ["tl", "tr"], w: 22 }],
      hl: function (P) {
        return rev ? [{ line: [[33, 70], [67, 70]], w: 6 }, { dot: [29, 66], r: 4.6 }, { dot: [71, 66], r: 4.6 }]
          : [{ line: [[31, 54.5], [41.5, 53.5]], w: 6 }, { line: [[58.5, 53.5], [69, 54.5]], w: 6 }];
      },
      back: function (P) {
        var pv = rev ? [[40, 40], [60, 40]] : [[25, 82], [75, 82]];
        return [rev ? L("eq2", [[34, 43.5], [66, 43.5]], 8.5) : L("eq2", [[34, 80], [66, 80]], 8), L("eq2", [pv[0], P.haL], 3), L("eq2", [pv[1], P.haR], 3), D("eq2", pv[0], 3.2), D("eq2", pv[1], 3.2)];
      },
      front: function (P) {
        var nl = perp(P.shL, P.haL), nr = perp(P.shR, P.haR);
        return [L("eq", [off(P.haL, -nl[0] * 5.5, -nl[1] * 5.5), off(P.haL, nl[0] * 5.5, nl[1] * 5.5)], 4.4), L("eq", [off(P.haR, -nr[0] * 5.5, -nr[1] * 5.5), off(P.haR, nr[0] * 5.5, nr[1] * 5.5)], 4.4)];
      } };
  }
  EX.pec_deck = deckTop(false);
  EX.reverse_pec_deck = deckTop(true);
  EX.band_push_up = { t: .2,
    p0: { head: [19, 69], sh: [30, 72], hip: [58, 76], ft: [86, 84], toe: [88, 91], el: [41, 66], ha: [30, 87] },
    p1: { head: [19, 53], sh: [30, 58], hip: [58, 68], el: [31, 73] },
    fx: function (P) { P.kn = mix(P.hip, P.ft, .5); }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.hip, 0, .38, 13)]; },
    back: function (P) { return [floor(8, 94), L("eq2", [[10, 6], [10, 93]], 3.5), L("eq2", [[10, 22], [42, 22]], 3), L("eq", [[32, 22], off(P.sh, 2, -5)], 2.6)]; },
    front: function () { return []; } };

  /* ---------- 등 ---------- */
  function pulldown(h0, h1, bar) {
    return { t: .3, p0: mir(ext(FSIT, ext({ head: [50, 33], shL: [40, 47], hipL: [44, 73], knL: [37, 80], ftL: [37, 91], toeL: [31, 91] }, h0))), p1: mir(h1), bones: FRONT, hl: latPolys,
      back: function (P) { var y = P.haL[1] - 1; return [L("eq2", [[50, 6], [50, y]], 2.2), D("eq2", [50, 6], 3), bar(y), L("eq2", [[50, 82], [50, 93]], 3), L("eq2", [[36, 79.5], [64, 79.5]], 6), floor(28, 72)]; },
      front: function () { return []; } };
  }
  EX.lat_pulldown = pulldown({ elL: [31, 33], haL: [27, 19] }, { elL: [25, 57], haL: [28, 42] }, function (y) { return L("eq", [[16, y + 6], [23, y], [77, y], [84, y + 6]], 3.8); });
  EX.underhand_pulldown = pulldown({ elL: [37, 33], haL: [39, 19] }, { elL: [31, 58], haL: [39, 44] }, function (y) { return L("eq", [[28, y], [72, y]], 3.8); });
  /* 뉴텍 버티컬 풀다운(원판식): 옆모습 — 머리 위 손잡이를 당기면 뒤쪽 원판이 올라가는 지렛대 */
  EX.vertical_pulldown = { t: .85, p0: ext(sit(40, 66), { el: [47, 24], ha: [54, 9] }), p1: { el: [48, 55], ha: [54, 39] }, bones: SIDE,
    fx: function (P) { P.pv = [27, 21]; P.bk = [P.pv[0] + (P.pv[0] - P.ha[0]) * .46, P.pv[1] + (P.pv[1] - P.ha[1]) * .46]; },
    hl: function (P) { return [seg(P.sh, P.hip, .06, .56, 13)]; },
    back: function (P) { return seatEq(40, 66, false).concat([L("eq2", [[27, 21], [24, 93]], 3.5), L("eq2", [[52, 60], [61, 60]], 5), L("eq2", [[57, 62], [57, 93]], 3),
      L("eq", [P.bk, P.pv, off(P.ha, 0, -1)], 3.4), D("eq2", P.pv, 3.4), R("eq", P.bk, 6.5, 3.4)]); },
    front: function (P) { return [L("eq", [off(P.ha, -4, -1), off(P.ha, 4, -1)], 3.8)]; } };
  EX.straight_arm_pulldown = { t: .75,
    p0: { head: [36, 15], sh: [38, 30], hip: [34, 57], kn: [37, 75], ft: [35, 90], toe: [43, 91], ha: [66, 20] }, p1: { ha: [44, 59] }, arcs: { ha: "sh" },
    fx: function (P) { P.el = mix(P.sh, P.ha, .5); }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.hip, .08, .6, 13)]; },
    back: function (P) { return [floor(22, 92), L("eq2", [[86, 6], [86, 93]], 3.5), L("eq2", [[84, 9], P.ha], 2), D("eq2", [84, 9], 3.2)]; },
    front: function (P) { var n = perp(P.sh, P.ha); return [L("eq", [[P.ha[0] - n[0] * 5, P.ha[1] - n[1] * 5], [P.ha[0] + n[0] * 5, P.ha[1] + n[1] * 5]], 3.6)]; } };
  /* 케이블 풀오버: 케이블을 등지고 앞을 보고 서서, 머리 위에서 앞·아래로 당김 (2026-11-10 "반대가 됐는데? 앞을 바라보고 땡기는 자세") */
  EX.cable_pullover = { t: .75,
    p0: { head: [52, 16], sh: [48, 30], hip: [42, 57], kn: [46, 75], ft: [43, 90], toe: [51, 91], ha: [41, 4] }, p1: { ha: [66, 51] }, arcs: { ha: "sh" },
    fx: function (P) { P.el = mix(P.sh, P.ha, .5); }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.hip, .08, .6, 13)]; },
    back: function (P) { return [floor(8, 82), L("eq2", [[12, 4], [12, 93]], 3.5), L("eq2", [[14, 8], P.ha], 2), D("eq2", [14, 8], 3.2)]; },
    front: function (P) { return [D("eq", P.ha, 3.6)]; } };
  EX.seated_row_machine = { t: .9, p0: ext(sit(34, 65), { el: [48, 42], ha: [64, 43] }), p1: { el: [24, 49], ha: [45, 46] }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.hip, .04, .52, 13)]; },
    back: function (P) { return seatEq(34, 65, false).concat([L("eq2", [[43, 58], [47, 93]], 3), L("eq2", [[43, 35], [43, 58]], 5.5), L("eq2", [P.ha, [82, 88]], 3), D("eq2", [82, 88], 3.2)]); },
    front: function (P) { return [grip(P.ha)]; } };
  EX.high_row = EX.seated_row_machine; EX.seated_row = EX.seated_row_machine;
  /* 해머스트렝스 로우로우(원판식, 2026-11-10 사진 기준): 가슴 패드에 기대 앉아, 위에서 내려온 지렛대 손잡이를 무릎 앞 낮은 곳에서 골반 쪽으로 당김 */
  EX.low_row = { t: .9,
    p0: { head: [36, 24], sh: [33, 39], hip: [31, 66], kn: [50, 65], ft: [47, 88], toe: [55, 89], el: [47, 51], ha: [62, 60] },
    p1: { head: [31, 22], sh: [29, 37], el: [20, 53], ha: [40, 61] }, bones: SIDE,
    fx: function (P) { P.pv = [70, 9]; P.pl = off(mix(P.pv, P.ha, .7), 8, 1); },
    hl: function (P) { return [seg(P.sh, P.hip, .06, .58, 13)]; },
    back: function (P) { return [floor(8, 94), L("eq2", [[35, 76], [35, 93]], 3), L("eq2", [[22, 73.5], [45, 73.5]], 5), L("eq2", [[43, 62], [47, 93]], 3), L("eq2", [[42.5, 38], [42.5, 62]], 5.5),
      L("eq2", [[70, 9], [78, 93]], 3.5), L("eq2", [[52, 9], [76, 9]], 3), L("eq", [P.pv, P.ha], 3.4), D("eq2", P.pv, 3.4), R("eq", P.pl, 6.5, 3.4)]; },
    front: function (P) { return [grip(P.ha, 5)]; } };
  EX.cable_seated_row = { t: .9,
    p0: { head: [40, 31], sh: [36, 45], hip: [32, 72], kn: [52, 65], ft: [70, 73], toe: [73, 65], el: [50, 54], ha: [63, 56] },
    p1: { head: [31, 29], sh: [31, 44], el: [22, 58], ha: [42, 57] }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.hip, .04, .52, 13)]; },
    back: function (P) { return [floor(10, 94), L("eq2", [[24, 82], [24, 93]], 3), L("eq2", [[42, 82], [42, 93]], 3), L("eq2", [[19, 80], [47, 80]], 5), L("eq2", [[89, 40], [89, 93]], 3.5),
      L("eq2", [P.ha, [87, 60]], 2), D("eq2", [87, 60], 3.2), L("eq", [[77, 59], [77, 80]], 3.8)]; },
    front: function (P) { return [grip(P.ha, 4.5)]; } };
  EX.underhand_seated_row = EX.cable_seated_row;
  EX.one_arm_row = { t: .9,
    p0: { head: [18, 36], sh: [30, 42], hip: [58, 45], sa: [27, 51], ha2: [24, 60], kn: [63, 68], ft: [64, 90], toe: [56, 91], el: [35, 57], ha: [35, 72] },
    p1: { el: [43, 34], ha: [39, 48] },
    bones: [{ pts: ["sh", "sa", "ha2"], w: 7.5 }, { pts: ["hip", "kn", "ft", "toe"], w: 9 }, { pts: ["sh", "hip"], w: 13 }, { pts: ["sh", "el", "ha"], w: 7.5, o: 1 }],
    hl: function (P) { return [seg(P.sh, P.hip, .12, .66, 13)]; },
    back: function () { return [floor(8, 92), L("eq2", [[20, 67], [20, 93]], 3), L("eq2", [[52, 67], [52, 93]], 3), L("eq2", [[13, 65], [60, 65]], 6)]; },
    front: function (P) { return db([P.ha[0], P.ha[1] + 2], [1, 0], 7.5); } };
  EX.smith_row = { t: .9,
    p0: { head: [70, 29], sh: [60, 36], hip: [36, 50], kn: [43, 70], ft: [39, 90], toe: [47, 91], el: [61, 51], ha: [61, 66] }, p1: { el: [50, 43], ha: [61, 54] }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.hip, .08, .6, 13)]; },
    back: function () { return [floor(14, 90), L("eq2", [[61.5, 6], [61.5, 93]], 2.6)]; },
    front: function (P) { return [R("eq", P.ha, 8.5, 3.6), D("eq", P.ha, 2.4)]; } };
  EX.face_pull = { t: .9, p0: ext(sit(34, 65), { el: [46, 33], ha: [60, 30] }), p1: { el: [21, 29], ha: [41, 27] }, bones: SIDE,
    hl: function (P) { return [{ dot: P.sh, r: 5.6 }]; },
    back: function (P) { return seatEq(34, 65, false).concat([L("eq2", [[89, 8], [89, 93]], 3.5), L("eq2", [P.ha, [87, 25]], 2), D("eq2", [87, 25], 3.2)]); },
    front: function (P) { return [D("eq", P.ha, 3.4)]; } };
  function shrug(front, back) {
    return { t: 1, p0: mir(ext(FSTAND, { elL: [35, 42], haL: [35, 56] })), p1: mir({ shL: [40, 23.5], elL: [35, 37.5], haL: [35, 51.5] }), bones: FRONT,
      hl: function (P) { var y = P.shL[1]; return [{ poly: [[P.shL[0] + 2, y - 1.5], [46.5, y - 7], [53.5, y - 7], [P.shR[0] - 2, y - 1.5], [53.5, y + 3], [46.5, y + 3]], w: 2 }]; },
      back: back || function () { return [floor(20, 80)]; }, front: front };
  }
  EX.shrug = shrug(function (P) { return [D("eq", off(P.haL, 0, 4), 5.2), D("eq", off(P.haR, 0, 4), 5.2)]; });
  EX.smith_shrug = shrug(function (P) { var y = P.haL[1] + 3; return [L("eq", [[17, y], [83, y]], 3.4), L("eq", [[17, y - 7], [17, y + 7]], 5), L("eq", [[83, y - 7], [83, y + 7]], 5)]; },
    function () { return [floor(12, 88), L("eq2", [[26, 5], [26, 93]], 2.6), L("eq2", [[74, 5], [74, 93]], 2.6)]; });

  /* ---------- 어깨 ---------- */
  function ohp(front, back) {
    return { t: .75, p0: mir(ext(FSIT, { elL: [28, 51], haL: [28, 36] })), p1: mir({ elL: [31, 29], haL: [34, 13] }), bones: FRONT, hl: delts,
      back: function (P) { return fseatEq().concat(back ? back(P) : []); }, front: front };
  }
  EX.shoulder_press = ohp(function (P) { return db(P.haL, [1, 0], 7).concat(db(P.haR, [1, 0], 7)); });
  EX.smith_shoulder_press = ohp(function () { return []; }, function (P) {
    var y = P.haL[1] - 1; return [L("eq2", [[20, 4], [20, 93]], 2.6), L("eq2", [[80, 4], [80, 93]], 2.6), L("eq", [[14, y], [86, y]], 3.4), L("eq", [[14, y - 7], [14, y + 7]], 5), L("eq", [[86, y - 7], [86, y + 7]], 5)]; });
  function raise(base, seated, machine) {
    function pads(P) {
      var nl = perp(P.elL, P.haL), nr = perp(P.haR, P.elR);
      return [[off(mix(P.elL, P.haL, .1), nl[0] * 6.5, nl[1] * 6.5), off(mix(P.elL, P.haL, .95), nl[0] * 6.5, nl[1] * 6.5)],
        [off(mix(P.elR, P.haR, .1), nr[0] * 6.5, nr[1] * 6.5), off(mix(P.elR, P.haR, .95), nr[0] * 6.5, nr[1] * 6.5)]];
    }
    return { t: .85, p0: mir(ext(base, seated ? { elL: [35, 56], haL: [34, 69] } : { elL: [36, 43], haL: [34, 57] })),
      p1: mir(seated ? { elL: [26, 43], haL: [12, 44] } : { elL: [26, 29], haL: [12, 30] }), arcs: FARC, bones: FRONT, hl: delts,
      back: function (P) {
        if (seated) return [L("eq2", [[50, 80], [50, 93]], 3), L("eq2", [[32, 79.5], [68, 79.5]], 5), floor(24, 76)];   /* 등받이 없는 벤치 */
        if (!machine) return [floor(20, 80)];
        var pd = pads(P);   /* 스탠딩 머신: 뒤에 기둥 + 기둥에서 팔 패드로 가는 지렛대 */
        return [floor(18, 82), L("eq2", [[38, 93.5], [62, 93.5]], 4), L("eq2", [[50, 2], [50, 92]], 5.5), L("eq2", [[50, 25], mix(pd[0][0], pd[0][1], .5)], 3), L("eq2", [[50, 25], mix(pd[1][0], pd[1][1], .5)], 3)];
      },
      front: function (P) {
        if (!machine) return [D("eq", P.haL, 5.2), D("eq", P.haR, 5.2)];
        var pd = pads(P); return [L("eq", pd[0], 4.6), L("eq", pd[1], 4.6)];
      } };
  }
  EX.lateral_raise = raise(FSTAND, false, false);
  EX.seated_lateral_raise = raise(FSIT, true, false);                    /* 시티드 레터럴 레이즈 (덤벨, 벤치에 앉아서) */
  EX.lateral_raise_standing = raise(FSTAND, false, true);                /* 사이드 레터럴 레이즈 머신 — 도당점은 스탠딩 */
  EX.lateral_raise_machine = EX.lateral_raise_standing;                  /* 예전 이름(앉는 머신)도 같은 그림으로 통합 */

  /* ---------- 팔 ---------- */
  EX.db_curl = { t: .7, p0: ext(stand(40), { el: [42, 45], ha: [44, 63] }), p1: { ha: [55, 32.5] }, arcs: { ha: "el" }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.el, .25, 1, 7.5)]; },
    back: function () { return [floor(20, 70)]; },
    front: function (P) { return db(P.ha, perp(P.el, P.ha), 8); } };
  EX.incline_db_curl = { t: .75, p0: ext(INC, { el: [36, 60], ha: [37, 76] }), p1: { ha: [49, 49] }, arcs: { ha: "el" }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.el, .25, 1, 7.5)]; },
    back: function () { return inclineEq(); },
    front: function (P) { return db(P.ha, perp(P.el, P.ha), 7.5); } };
  EX.cable_pushdown = { t: .85, p0: ext(stand(38), { el: [41, 45], ha: [54, 37] }), p1: { ha: [46, 60] }, arcs: { ha: "el" }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.el, .2, 1, 7.5)]; },
    back: function (P) { return [floor(18, 86), L("eq2", [[78, 6], [78, 93]], 3.5), L("eq2", [[62, 8], [78, 8]], 3), L("eq2", [[62, 8], P.ha], 2), D("eq2", [62, 8], 3.2)]; },
    front: function (P) { var n = perp(P.el, P.ha); return [L("eq", [[P.ha[0] - n[0] * 5.5, P.ha[1] - n[1] * 5.5], [P.ha[0] + n[0] * 5.5, P.ha[1] + n[1] * 5.5]], 3.6)]; } };
  EX.overhead_ext = { t: .85,
    p0: { head: [42, 33], sh: [42, 48], hip: [42, 74], kn: [61, 75], ft: [62, 90], toe: [70, 91], el: [47, 31], ha: [34, 38] }, p1: { ha: [49, 15] }, arcs: { ha: "el" },
    bones: [{ pts: ["hip", "kn", "ft", "toe"], w: 9 }, { pts: ["sh", "hip"], w: 13 }, { pts: ["sh", "el", "ha"], w: 7.5 }],
    hl: function (P) { return [seg(P.sh, P.el, .25, 1, 7.5)]; },
    back: function () { return [floor(22, 80), L("eq2", [[46, 84], [46, 93]], 3), L("eq2", [[33, 81.5], [58, 81.5]], 5)]; },
    front: function (P) { return db(P.ha, perp(P.el, P.ha), 7); } };

  /* ---------- 하체 ---------- */
  EX.leg_extension = { t: .9, p0: ext(sit(34, 65), { ft: [55, 88], el: [36, 51], ha: [44, 61] }), p1: { ft: [75, 64] }, arcs: { ft: "kn" },
    fx: function (P) { var u = unit(P.kn, P.ft); P.fd = [u[1], -u[0]]; P.toe = off(P.ft, P.fd[0] * 7, P.fd[1] * 7); P.pad = off(mix(P.kn, P.ft, .82), P.fd[0] * 7, P.fd[1] * 7); },
    bones: SIDE, hl: function (P) { return [seg(P.hip, P.kn, .1, .92, 9)]; },
    back: function (P) { return seatEq(34, 65).concat([L("eq2", [[53, 72], P.pad], 3)]); },
    front: function (P) { return [D("eq", P.pad, 3.8)]; } };
  EX.lying_leg_curl = { t: .85,
    p0: { head: [15, 52], sh: [26, 56], hip: [52, 57], kn: [70, 58], ft: [89, 58], el: [23, 66], ha: [14, 69] }, p1: { ft: [74, 39] }, arcs: { ft: "kn" },
    fx: function (P) { var u = unit(P.kn, P.ft); P.fd = [-u[1], u[0]]; P.toe = off(P.ft, P.fd[0] * 6, P.fd[1] * 6); P.pad = off(mix(P.kn, P.ft, .85), -P.fd[0] * 7, -P.fd[1] * 7); },
    bones: SIDE, hl: function (P) { return [seg(P.hip, P.kn, .1, .92, 9)]; },
    back: function (P) { return [floor(6, 94), L("eq2", [[20, 68], [20, 93]], 3), L("eq2", [[62, 68], [62, 93]], 3), L("eq2", [[9, 66.5], [74, 66.5]], 6), L("eq2", [[70, 66], P.pad], 3)]; },
    front: function (P) { return [D("eq", P.pad, 3.8)]; } };
  EX.seated_leg_curl = EX.lying_leg_curl;
  function thigh(open1, inner) {   /* 이너타이(모으기) · 아웃타이(벌리기) */
    var open = { knL: [27, 75], ftL: [22, 91], toeL: [16, 91] }, close = { knL: [43, 77], ftL: [42, 91], toeL: [36, 91] };
    return { t: .85, p0: mir(ext(FSIT, ext(open1 ? close : open, { elL: [35, 54], haL: [37, 66] }))), p1: mir(open1 ? open : close), bones: FRONT,
      hl: function (P) { return inner ? [seg(P.hipL, P.knL, .3, .92, 8), seg(P.hipR, P.knR, .3, .92, 8)] : [{ dot: off(P.hipL, -3.5, 1), r: 5.4 }, { dot: off(P.hipR, 3.5, 1), r: 5.4 }]; },
      back: function () { return fseatEq(); },
      front: function (P) { var s = inner ? 6 : -6; return [L("eq", [off(P.knL, s, -7), off(P.knL, s, 4)], 4.4), L("eq", [off(P.knR, -s, -7), off(P.knR, -s, 4)], 4.4)]; } };
  }
  EX.inner_thigh = thigh(false, true);
  EX.outer_thigh = EX.outer_thigh_pin = EX.outer_thigh_plate = thigh(true, false);
  EX.leg_press = { t: .85,
    p0: { head: [15, 44], sh: [22, 56], hip: [38, 80], kn: [40, 58], ft: [60, 64], el: [30, 69], ha: [39, 73] }, p1: { kn: [54, 65], ft: [73, 55] },
    fx: function (P) { P.toe = off(P.ft, -4.1, -5.7); P.pl = off(P.ft, 4.6, -3.3); },
    bones: [{ pts: ["sh", "el", "ha"], w: 7.5 }, { pts: ["sh", "hip"], w: 13 }, { pts: ["hip", "kn", "ft", "toe"], w: 9 }],
    hl: function (P) { return [seg(P.hip, P.kn, .1, .92, 9)]; },
    back: function (P) { return [floor(6, 94), L("eq2", [[30, 93], [93, 47]], 3), L("eq2", [[12.5, 57.5], [33, 88]], 5.5), L("eq2", [[33, 89], [47, 86]], 5)]; },
    front: function (P) { return [L("eq", [off(P.pl, -5.9, -8.1), off(P.pl, 5.9, 8.1)], 4.6)]; } };
  EX.hack_squat = { t: .15,
    p0: { head: [26, 28], sh: [30, 42], hip: [39, 68], kn: [59, 67], ft: [66, 86], toe: [74, 83] }, p1: { head: [34, 10], sh: [38, 24], hip: [47, 50], kn: [56, 68] },
    fx: function (P) { P.el = off(P.sh, 9, 7); P.ha = off(P.sh, 7, -3); }, bones: SIDE,
    hl: function (P) { return [seg(P.hip, P.kn, .1, .92, 9)]; },
    back: function (P) { return [floor(8, 92), L("eq2", [[9, 82], [33, 10]], 3), L("eq2", [off(P.sh, -7.5, 2.5), off(P.hip, -7.5, 2.5)], 5.5), L("eq", [[57, 93], [79, 84]], 4.6)]; },
    front: function (P) { return [L("eq", [off(P.sh, -5, -8), off(P.sh, 5, -10)], 4.6)]; } };
  function squat(arm, front, back) {
    return { t: .85, p0: SQ0, p1: SQ1, fx: arm, bones: SIDE,
      hl: function (P) { return [seg(P.hip, P.kn, .12, .92, 9)]; },
      back: function (P) { return [floor(18, 82)].concat(back ? back(P) : []); }, front: front };
  }
  function barArm(P) { P.el = off(P.sh, 6, 7); P.ha = off(P.sh, -2, -3); P.bar = off(P.sh, -6, -5); }
  EX.squat = squat(barArm, function (P) { return [D("eq", P.bar, 2.5)]; }, function (P) { return [R("eq", P.bar, 9, 3.6)]; });
  EX.smith_squat = squat(barArm, function (P) { return [D("eq", P.bar, 2.5)]; }, function (P) { return [L("eq2", [[43, 4], [43, 93]], 2.6), R("eq", P.bar, 9, 3.6)]; });
  EX.goblet_squat = squat(function (P) { P.el = off(P.sh, 6, 11); P.ha = off(P.sh, 10, 2); }, function (P) { return db(off(P.ha, 1.5, -1), [0, 1], 6.5); });
  EX.hip_thrust = { t: .9,
    p0: { head: [13, 47], sh: [24, 53], hip: [44, 73], kn: [66, 67], ft: [74, 89], toe: [82, 90] }, p1: { hip: [52, 56], kn: [72, 62] },
    fx: function (P) { P.bar = off(P.hip, 3, -7); P.ha = off(P.hip, 0, -8); P.el = off(mix(P.sh, P.ha, .5), -2, 5); }, bones: SIDE,
    hl: function (P) { return [{ dot: off(P.hip, -2, 3), r: 6 }]; },
    back: function () { return [floor(6, 94), L("eq2", [[12, 64], [12, 93]], 3), L("eq2", [[25, 64], [25, 93]], 3), L("eq2", [[7, 61.5], [29, 61.5]], 6)]; },
    front: function (P) { return [R("eq", P.bar, 8, 3.6), D("eq", P.bar, 2.4)]; } };
  EX.db_rdl = { t: .85, p0: ext(stand(44), { el: [45, 43], ha: [46, 57] }), p1: { head: [69, 32], sh: [58, 38], hip: [36, 56], kn: [42, 75], el: [58, 53], ha: [58, 67] }, bones: SIDE,
    hl: function (P) { return [seg(P.hip, P.kn, .05, .9, 9), { dot: P.hip, r: 5.6 }]; },
    back: function () { return [floor(18, 82)]; },
    front: function (P) { return db(off(P.ha, 0, 2.5), [1, 0], 7.5); } };
  EX.back_extension = { t: .9,
    p0: { ft: [24, 85], toe: [18.4, 80.8], kn: [36, 69.5], hip: [48, 54], sh: [70, 70], head: [81, 79] }, p1: { sh: [65, 32], head: [73.7, 20.4] }, arcs: { sh: "hip", head: "hip" },
    bones: [{ pts: ["hip", "kn", "ft", "toe"], w: 9 }, { pts: ["sh", "hip"], w: 13 }],
    hl: function (P) { return [seg(P.hip, P.sh, .04, .42, 13), { dot: off(P.hip, -3, 1), r: 5.8 }]; },
    back: function () { return [L("floor", [[10, 95], [72, 95]], 3), L("eq2", [[56, 61], [61, 93]], 3), L("eq2", [[22, 91], [61, 93]], 3), L("eq", [[50.5, 64], [58.5, 53.5]], 6), L("eq", [[14.5, 85.5], [24, 93]], 4.6)]; },
    front: function () { return []; } };
  EX.cable_kickback = { t: .9,
    p0: { head: [30, 21], sh: [38, 32], hip: [50, 56], kn: [49, 74], ft: [48, 90], toe: [40, 91], el: [28, 41], ha: [16, 38], kn2: [53, 74], ft2: [56, 89] },
    p1: { kn2: [64, 68], ft2: [78, 75] }, arcs: { kn2: "hip", ft2: "kn2" },
    bones: [{ pts: ["hip", "kn2", "ft2"], w: 9 }, { pts: ["hip", "kn", "ft", "toe"], w: 9, o: 1 }, { pts: ["sh", "hip"], w: 13 }, { pts: ["sh", "el", "ha"], w: 7.5 }],
    hl: function (P) { return [{ dot: off(P.hip, 2, 0), r: 6 }]; },
    back: function (P) { return [floor(6, 92), L("eq2", [[12, 6], [12, 93]], 3.5), L("eq2", [[14, 89], P.ft2], 2), D("eq2", [14, 89], 3.2)]; },
    front: function (P) { return [D("eq", P.ft2, 3.4)]; } };
  EX.plank = { t: 0, slow: 1,
    p0: { head: [17, 60], sh: [28, 66], el: [28, 85], ha: [13, 86], hip: [56, 69], kn: [72, 76], ft: [87, 83], toe: [89, 90] }, p1: { hip: [56, 66.5], kn: [72, 74.5] }, bones: SIDE,
    hl: function (P) { return [seg(P.sh, P.hip, .42, 1, 13)]; },
    back: function () { return [floor(6, 94)]; }, front: function () { return []; } };

  /* ---------- 그리기 ---------- */
  var STY = {
    M: { tile: "#F1EEE6", fig: "#1C1C1E", eq: "#9A9384", eq2: "#D6D0C2", floor: "#D6D0C2", hl: "#D4A72C" },
    F: { tile: "#F8EDED", fig: "#A0606A", eq: "#AE9A9C", eq2: "#E6D3D4", floor: "#E6D3D4", hl: "#1C1C1E" }
  };
  function pose(ex, t) {
    var P = {}, k;
    for (k in ex.p0) P[k] = ex.p1[k] ? mix(ex.p0[k], ex.p1[k], t) : ex.p0[k];
    for (k in (ex.arcs || {})) {   /* 관절을 축으로 도는 부위는 각도로 보간 (직선으로 보간하면 팔다리가 짧아 보임) */
      if (!ex.p1[k]) continue;
      var pv = ex.arcs[k], c0 = ex.p0[pv], c1 = ex.p1[pv] || c0, c = P[pv], a = ex.p0[k], b = ex.p1[k];
      var a0 = Math.atan2(a[1] - c0[1], a[0] - c0[0]), l0 = Math.sqrt(Math.pow(a[0] - c0[0], 2) + Math.pow(a[1] - c0[1], 2));
      var a1 = Math.atan2(b[1] - c1[1], b[0] - c1[0]), l1 = Math.sqrt(Math.pow(b[0] - c1[0], 2) + Math.pow(b[1] - c1[1], 2));
      while (a1 - a0 > Math.PI) a1 -= 2 * Math.PI;
      while (a1 - a0 < -Math.PI) a1 += 2 * Math.PI;
      var an = a0 + (a1 - a0) * t, l = l0 + (l1 - l0) * t;
      P[k] = [c[0] + Math.cos(an) * l, c[1] + Math.sin(an) * l];
    }
    if (ex.fx) ex.fx(P);
    return P;
  }
  function f1(n) { return String(Math.round(n * 10) / 10); }
  function dOf(pts, close) { return "M" + pts.map(function (p) { return f1(p[0]) + " " + f1(p[1]); }).join("L") + (close ? "Z" : ""); }
  /* 한 자세의 도형 목록: [{ tag, fix(안 바뀌는 속성), dyn{ 바뀌는 속성 } }] — 자세가 달라도 개수·순서는 같음 */
  function shapes(ex, S, t) {
    var P = pose(ex, t), out = [];
    function add(s, col, grow, hl) {
      var w = (s.w || 0) + (grow || 0), o;
      if (s.line) o = { tag: "path", fix: 'fill="none" stroke="' + col + '" stroke-width="' + f1(w) + '" stroke-linecap="round" stroke-linejoin="round"', dyn: { d: dOf(s.line) } };
      else if (s.poly) o = { tag: "path", fix: 'fill="' + col + '" stroke="' + col + '" stroke-width="' + f1(w) + '" stroke-linejoin="round"', dyn: { d: dOf(s.poly, true) } };
      else if (s.ring) o = { tag: "circle", fix: 'r="' + s.r + '" fill="none" stroke="' + col + '" stroke-width="' + s.w + '"', dyn: { cx: f1(s.ring[0]), cy: f1(s.ring[1]) } };
      else if (s.dot) o = { tag: "circle", fix: 'r="' + f1(s.r + (grow || 0) / 2) + '" fill="' + col + '"', dyn: { cx: f1(s.dot[0]), cy: f1(s.dot[1]) } };
      else o = { tag: "rect", fix: 'x="' + s.rect[0] + '" y="' + s.rect[1] + '" width="' + s.rect[2] + '" height="' + s.rect[3] + '" rx="' + (s.r || 0) + '" fill="' + col + '"', dyn: {} };
      if (hl) o.dyn.opacity = f1(.5 + .5 * t);
      out.push(o);
    }
    ex.back(P).forEach(function (s) { add(s, S[s.k]); });
    var hlDone = false;
    ex.bones.forEach(function (b) {
      if (b.hlHere) { ex.hl(P).forEach(function (s) { add(s, S.hl, 0, true); }); hlDone = true; return; }
      var s = b.poly ? { poly: b.poly.map(function (k) { return P[k]; }), w: b.w } : { line: b.pts.map(function (k) { return P[k]; }), w: b.w };
      if (b.o) add(s, S.tile, 3.2);   /* 몸통 앞을 지나는 팔다리는 옅은 테두리로 구분 */
      add(s, S.fig);
    });
    if (ex.headO) add({ dot: P.head, r: (ex.headR || 7.2) + 1.7 }, S.tile);
    add({ dot: P.head, r: ex.headR || 7.2 }, S.fig);
    if (!hlDone) ex.hl(P).forEach(function (s) { add(s, S.hl, 0, true); });
    ex.front(P).forEach(function (s) { add(s, S[s.k]); });
    return out;
  }
  function ease(x) { return (1 - Math.cos(x * Math.PI)) / 2; }
  /* 움직임 시간표: 잠깐 멈춤 → 힘 줘서 올리기(빠르게) → 멈춤 → 천천히 내리기 */
  var N = 6, FR = [{ kt: 0, t: 0 }, { kt: .1, t: 0 }], i;
  for (i = 1; i <= N; i++) FR.push({ kt: .1 + .32 * i / N, t: ease(i / N) });
  FR.push({ kt: .52, t: 1 });
  for (i = 1; i <= N; i++) FR.push({ kt: .52 + .46 * i / N, t: 1 - ease(i / N) });
  FR.push({ kt: 1, t: 0 });
  var KT = FR.map(function (f) { return f1(f.kt * 100) / 100; }).join(";");
  var cache = {};
  function svg(key, opt) {
    opt = opt || {};
    var ex = EX[key]; if (!ex) return "";
    var sex = opt.sex === "F" ? "F" : "M", still = !!opt.still, ck = key + sex + (still ? "s" : "a");
    if (!cache[ck]) {
      var S = STY[sex], base = shapes(ex, S, still ? ex.t : 0), frames = still ? null : FR.map(function (f) { return shapes(ex, S, f.t); });
      var dur = ex.slow ? "3.6s" : "2.8s";
      var h = '<rect x=".75" y=".75" width="98.5" height="98.5" rx="23" fill="' + S.tile + '"/>';
      base.forEach(function (o, n) {
        var attrs = "", anim = "", k;
        for (k in o.dyn) {
          attrs += " " + k + '="' + o.dyn[k] + '"';
          if (still) continue;
          var vals = frames.map(function (fr) { return fr[n].dyn[k]; }), same = vals.every(function (v) { return v === vals[0]; });
          if (!same) anim += '<animate attributeName="' + k + '" dur="' + dur + '" repeatCount="indefinite" keyTimes="' + KT + '" values="' + vals.join(";") + '"/>';
        }
        h += "<" + o.tag + " " + o.fix + attrs + (anim ? ">" + anim + "</" + o.tag + ">" : "/>");
      });
      cache[ck] = h;
    }
    return '<svg class="' + (opt.cls || "icn") + ' exi" viewBox="0 0 100 100" aria-hidden="true" focusable="false">' + cache[ck] + "</svg>";
  }
  var noMotion = false;
  try { noMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
  window.EXI = { has: function (k) { return !!EX[k]; }, keys: function () { return Object.keys(EX); }, noMotion: noMotion,
    svg: function (k, o) { if (noMotion) { o = o || {}; o.still = true; } return svg(k, o); },
    frame: function (k, t, sex) {   /* 확인용: 특정 순간의 멈춘 그림 */
      var S = STY[sex === "F" ? "F" : "M"], h = '<rect x=".75" y=".75" width="98.5" height="98.5" rx="23" fill="' + S.tile + '"/>';
      shapes(EX[k], S, t).forEach(function (o) { var a = "", d; for (d in o.dyn) a += " " + d + '="' + o.dyn[d] + '"'; h += "<" + o.tag + " " + o.fix + a + "/>"; });
      return '<svg viewBox="0 0 100 100">' + h + "</svg>";
    } };
})();
