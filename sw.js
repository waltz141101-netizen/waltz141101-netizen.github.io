/* PT 노트 서비스 워커 (2026-11-13 트레이너 "회원님들 앱으로 다운받기가 안 되고 바로가기만 돼")
   안드로이드 크롬이 '앱 설치'를 띄우려면 manifest + 서비스 워커가 필요해서 넣음.
   캐시는 하지 않고 늘 인터넷에서 새로 받음(복습지·루틴이 바로 바뀌어야 하니까). 인터넷이 끊겼을 때만 마지막 화면을 보여 줌 */
var CACHE = "ptnote-shell-v3";
self.addEventListener("install", function () { self.skipWaiting(); });
self.addEventListener("activate", function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener("fetch", function (e) {
  var r = e.request;
  if (r.method !== "GET") return;
  var u = new URL(r.url);
  /* 2026-11-14 "아직 안 됐는데?" — 폰이 예전 app.js·style.css를 10분 캐시로 들고 있어서 새 화면이 안 나왔음 → 우리 사이트 js·css는 늘 서버에 확인(no-cache) */
  if (u.origin === location.origin && /\/assets\/[^\/]+\.(js|css)$/.test(u.pathname)) {
    e.respondWith(fetch(r.url, { cache: "no-cache" }).catch(function () { return fetch(r); }));
    return;
  }
  if (r.mode !== "navigate") return;   /* 화면(페이지)만 — 그림·영상·창고 요청은 그대로 */
  /* 2026-11-17 "앱이 왜 안 켜지냐" — 예전엔 인터넷이 잠깐 끊기거나(캐시 없음 → 빈 응답) 주소가 넘어가면(redirected 응답) 앱이 하얀/오류 화면이 될 수 있었음.
     → 넘어간 응답은 그 주소로 다시 보내고, 실패하면 마지막 화면 → 그것도 없으면 브라우저 기본 요청으로 */
  e.respondWith(fetch(r.url, { cache: "no-cache", credentials: "same-origin" }).then(function (res) {
    if (res.redirected) return Response.redirect(res.url, 302);
    if (res.ok) { var copy = res.clone(); caches.open(CACHE).then(function (c) { c.put(r, copy); }).catch(function () {}); }
    return res;
  }).catch(function () {
    return caches.match(r).then(function (hit) { return hit || fetch(r); });
  }));
});
