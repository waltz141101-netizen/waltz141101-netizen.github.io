/* 기본 루틴 (2026-11-13 트레이너 "여자는 3분할 주6일, 남자는 4분할 루틴 집어넣어")
   루틴이 없는 회원(앱에서 추가한 회원·data.js routine:null)은 성별에 맞는 이 루틴이 자동으로 보임.
   선생님 폰 '루틴 고치기'로 고치면 그 회원만 바뀜(기준 base = version|updated — 여기 version·updated를 바꾸면 폰에서 고친 루틴이 꺼지니 주의).
   여 = 3분할 주 6일(등·하체·어깨 A/B, 일 휴식) / 남 = 4분할 순환(DAY 1~4, 순서대로 — 시작 = 회원 PT 시작일)
   탑세트 = 20 → 15 → 10(가장 무겁게) → 12회. 무게 칸 "" = 회원님께 맞춰 정하기(화면엔 "—") */
(function () {
  var W = "";
  function top() { return [[20, W], [15, W], [10, W], [12, W]]; }
  function n(sets, reps) { var a = []; for (var i = 0; i < sets; i++) a.push([reps, W]); return a; }
  function it(name, en, sets, tip, tag, icon) { var o = { name: name, en: en, tip: tip, sets: sets }; if (tag) o.tag = tag; if (icon) o.icon = icon; return o; }
  var T = "메인", P = "선행";

  var F = {
    version: "v1", updated: "2026. 11. 13", title: "3분할 · 그날 골라서 하는 루틴",
    rotation: true, free: true, rest_label: "쉬고 싶은 날",
    plan: ["요일 상관없이 그날 컨디션에 맞는 운동을 골라요", "등 · 하체 · 어깨 A · B 6가지를 골고루", "탑세트 = 20 → 15 → 10(가장 무겁게) → 12회 · 주 1일은 휴식"],
    key_point: "모든 운동은 내릴 때 2~3초 천천히! 무게보다 자세가 먼저예요",
    note: "세트 사이 휴식은 60~90초, 위에서부터 순서대로 · 마지막 2~3회가 힘든 무게로",
    cardio: null,
    days: [
      { day: "DAY 1", part: "등 A", en: "Back A", cardio: false, items: [
        it("어시스트풀업", "Assisted Pull-up", n(4, "10~12"), "어깨는 귀에서 멀리, 팔꿈치로 끌어내리기", "", "assisted_pullup"),
        it("투암 덤벨로우", "Two-arm DB Row", n(4, 12), "상체 숙이고 양 팔꿈치를 골반 쪽으로", "", "db_row"),
        it("데드리프트", "Deadlift", n(3, "10~12"), "엉덩이를 위로 빼고, 무게중심은 앞꿈치", "", "deadlift"),
        it("로우로우", "Low Row", top(), "가슴은 패드에 붙이고 팔꿈치로 당기기", T)] },
      { day: "DAY 2", part: "하체 A", en: "Legs A", cardio: false, items: [
        it("아웃타이", "Outer Thigh", n(4, "15~20"), "손잡이 잡고 밀어서 상체 세우기", P),
        it("힙쓰러스트", "Hip Thrust", top(), "턱 당기고, 위에서 엉덩이 꽉 조이기", T),
        it("스플릿 스쿼트", "Split Squat", n(3, "좌우 12회"), "뒷발은 벤치에, 앞발 뒤꿈치로 밀기", "", "split_squat"),
        it("핵스쿼트", "Hack Squat", top(), "등은 패드에 붙이고 무릎은 발끝 방향", T)] },
      { day: "DAY 3", part: "어깨 A", en: "Shoulders A", cardio: false, items: [
        it("페이스풀", "Face Pull", n(4, 15), "로프는 얼굴 쪽으로, 팔꿈치 높게"),
        it("덤벨 숄더 프레스", "DB Shoulder Press", top(), "덤벨은 귀 옆에서, 허리 꺾지 않기", T),
        it("사이드 레터럴 레이즈", "DB Lateral Raise", n(4, 15), "어깨 높이까지만, 으쓱하지 않기"),
        it("원판 프론트 레이즈", "Plate Front Raise", n(3, 15), "원판은 눈높이까지, 반동 없이", "", "front_raise")] },
      { day: "DAY 4", part: "등 B", en: "Back B", cardio: false, items: [
        it("랫풀다운", "Lat Pulldown", top(), "가슴 펴고 팔꿈치를 옆구리 쪽으로", T),
        it("언더그립 시티드 로우", "Underhand Seated Row", n(4, 12), "손바닥 위로, 팔꿈치 붙여 배꼽 쪽으로"),
        it("데드리프트", "Deadlift", n(3, "10~12"), "등은 일자, 바는 몸에 붙여서 내리기", "", "deadlift"),
        it("롱풀", "Long Pull", n(3, "12~15"), "상체 반동 없이 팔꿈치만 뒤로", "", "cable_seated_row")] },
      { day: "DAY 5", part: "하체 B", en: "Legs B", cardio: false, items: [
        it("이너타이", "Inner Thigh", n(4, "15~20"), "허벅지 안쪽으로 천천히 모으기", P),
        it("레그컬", "Leg Curl", top(), "골반은 패드에 붙이고 3초 내리기", T, "lying_leg_curl"),
        it("레그프레스", "Leg Press", top(), "허리는 등받이에, 무릎 끝까지 펴지 않기", T),
        it("핵프레스", "Hack Press", n(4, 12), "무릎은 발끝 방향, 내릴 땐 천천히", "", "hack_squat")] },
      { day: "DAY 6", part: "어깨 B", en: "Shoulders B", cardio: false, items: [
        it("리버스 펙덱", "Reverse Pec Deck Fly", n(4, 15), "가슴은 패드에, 팔꿈치 살짝 굽히기"),
        it("덤벨 숄더 프레스", "DB Shoulder Press", n(4, 12), "등받이에 붙이고 귀 높이까지 내리기"),
        it("숄더 프레스 머신", "Shoulder Press Machine", top(), "손잡이는 귀 높이에서 시작해 밀기", T),
        it("사이드 레터럴 레이즈 머신", "Lateral Raise Machine", n(4, 15), "팔꿈치로 밀어 올리듯 어깨 높이까지")] }
    ]
  };

  var M = {
    version: "v1", updated: "2026. 11. 13", title: "4분할 · 그날 골라서 하는 루틴",
    rotation: true, free: true, rest_label: "쉬고 싶은 날",
    plan: ["요일 상관없이 그날 컨디션에 맞는 운동을 골라요", "등 · 가슴 · 하체 · 어깨를 골고루, '또는'은 둘 중 하나", "탑세트 = 20 → 15 → 10(가장 무겁게) → 12회 · 주 1일은 휴식"],
    key_point: "오늘 할 운동은 홈에서 골라요! 고르지 않으면 다음 순서를 추천해요",
    note: "세트 사이 휴식 60~90초, 위에서부터 순서대로 · 마지막 2~3회가 힘든 무게로",
    cardio: null,
    days: [
      { day: "DAY 1", part: "등 · 승모 · 복근", en: "Back · Traps · Abs", cardio: false, items: [
        it("랫풀다운 또는 어시스트풀업", "Lat Pulldown / Assisted Pull-up", top(), "가슴 펴고 팔꿈치로 끌어내리기", T, "lat_pulldown"),
        it("바벨로우 또는 티바로우", "Barbell Row / T-bar Row", n(4, "10~12"), "상체 숙이고 배꼽 쪽으로 당기기", "", "db_row"),
        it("원암 덤벨로우 또는 시티드로우 언더그립", "One-arm DB Row / Underhand Seated Row", n(3, 12), "팔꿈치를 골반 쪽으로 당기기", "", "one_arm_row"),
        it("로우로우", "Low Row", n(3, 12), "가슴은 패드에, 팔꿈치로 당기기"),
        it("데드리프트", "Deadlift", n(3, "8~10"), "엉덩이 위로 빼고 무게는 앞꿈치", "", "deadlift"),
        it("슈러그", "Shrug", n(4, 15), "어깨를 귀 쪽으로, 1초 멈춤", "", "shrug"),
        it("크런치", "Crunch", n(3, 20), "배꼽 보며 말아 올리기", "", "crunch")] },
      { day: "DAY 2", part: "가슴 · 이두", en: "Chest · Biceps", cardio: false, items: [
        it("플라이 또는 케이블 크로스오버", "Fly / Cable Crossover", n(3, 15), "가슴으로 모으며 1초 쥐어짜기", "", "pec_deck"),
        it("벤치프레스", "Bench Press", top(), "날개뼈 모으고 가슴 중앙으로", T),
        it("인클라인 덤벨 프레스", "Incline DB Press", n(4, "10~12"), "벤치 30도, 윗가슴으로 밀기"),
        it("딥스 또는 푸쉬업", "Dips / Push-up", [["최대", null], ["최대", null], ["최대", null]], "상체 살짝 숙이고 가슴으로 밀기", "", "push_up"),
        it("인클라인 덤벨컬 또는 바벨컬", "Incline DB Curl / Barbell Curl", n(4, 12), "팔꿈치 고정, 반동 없이", "", "incline_db_curl"),
        it("해머 컬", "Hammer Curl", n(3, 12), "엄지가 위로, 천천히 내리기")] },
      { day: "DAY 3", part: "하체", en: "Legs", cardio: false, items: [
        it("이너타이", "Inner Thigh", n(3, "15~20"), "허벅지 안쪽으로 천천히 모으기", P),
        it("레그컬", "Leg Curl", n(4, 12), "골반은 패드에, 3초 내리기", "", "lying_leg_curl"),
        it("스쿼트 또는 핵스쿼트", "Squat / Hack Squat", top(), "엉덩이 뒤로, 무릎은 발끝 방향", T, "hack_squat"),
        it("레그프레스", "Leg Press", top(), "허리는 등받이에, 무릎 잠그지 않기", T),
        it("런지 또는 스플릿 스쿼트", "Lunge / Split Squat", n(3, "좌우 12회"), "뒷무릎은 바닥 쪽으로 곧게", "", "split_squat"),
        it("레그 익스텐션", "Leg Extension", n(3, 15), "끝까지 펴서 1초 멈추기")] },
      { day: "DAY 4", part: "어깨 · 삼두", en: "Shoulders · Triceps", cardio: false, items: [
        it("리버스 펙덱 또는 페이스풀", "Reverse Pec Deck / Face Pull", n(3, 15), "어깨 뒤로 당기며 날개뼈 모으기", "", "reverse_pec_deck"),
        it("덤벨 숄더 프레스 또는 스미스 숄더 프레스", "DB / Smith Shoulder Press", top(), "귀 옆에서 시작, 허리 꺾지 않기", T, "shoulder_press"),
        it("사이드 레터럴 레이즈", "Lateral Raise", n(4, 15), "어깨 높이까지, 으쓱하지 않기"),
        it("숄더 프레스 머신", "Shoulder Press Machine", n(3, 12), "손잡이는 귀 높이에서 밀기"),
        it("프론트 레이즈", "Front Raise", n(3, 15), "눈높이까지, 반동 없이", "", "front_raise"),
        it("푸쉬다운 또는 덤벨 라잉 트라이셉스 익스텐션", "Pushdown / DB Lying Triceps Ext.", n(3, 12), "팔꿈치 고정, 끝까지 펴기", "", "cable_pushdown"),
        it("로프 푸쉬다운", "Rope Pushdown", n(3, 15), "끝에서 로프를 벌리며 펴기", "", "cable_pushdown")] }
    ]
  };

  window.RT_TPL = { F: F, M: M };
  /* 회원(MEMBER 모양)에 맞는 기본 루틴 — 순환 루틴 시작 = PT 시작일 */
  window.rtTplFor = function (mem) {
    if (!mem) return null;
    var r = JSON.parse(JSON.stringify(mem.sex === "F" ? F : M));
    if (r.rotation) r.rotation_start = (mem.journey && mem.journey.start) || "2026-11-13";
    return r;
  };
})();
