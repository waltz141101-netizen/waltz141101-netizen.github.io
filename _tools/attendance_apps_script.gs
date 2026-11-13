// GYMTOS PT 노트 창고 (출석 + 인바디) — 이 코드를 Apps Script에 그대로 붙여넣고 "웹 앱"으로 배포하세요.
// 2026-11-06 인바디 추가: 시트 "인바디" 탭에 숫자, 구글 드라이브 "PT노트 인바디 사진" 폴더에 결과지 사진.
// 2026-11-06 결과지 자동 읽기(OCR): 왼쪽 "서비스 +" 에서 "Drive API"를 추가해야 동작 (없으면 회원이 숫자를 직접 넣으면 됨).
// 2026-11-11 범용 저장소(시트 "저장소" 탭) — 앞으로 새 기능은 이걸 써서 창고를 다시 배포하지 않아도 되게:
//   이름이 pub: 로 시작 = 누구나 읽기·선생님만 쓰기 / mw: = 회원도 쓰기(작은 것만) / 그 밖 = 선생님만 읽기·쓰기.
//   출석 보기(GET) 응답에 kv = pub:all:* + pub:m:<회원>:* + mw:<회원>:* 를 같이 보냄.
// 2026-11-11 전체 공지: 선생님 페이지에서 쓴 공지를 시트 "전체공지" 탭에 저장 → 모든 회원 노트 공지에 같이 나옴(60일 지난 건 안 보냄).
// 2026-11-11 보기(GET)는 잠그지 않게 바꿈 — 여러 명을 한꺼번에 불러도 실패하지 않음.
// 2026-11-13 주간 몸 사진: 시트 "몸사진" 탭 + 구글 드라이브 "PT노트 몸 사진" 폴더. 올리기 POST a=bp_add / 목록 GET a=bp / 보기 a=bp_img / 삭제 a=bp_del.
// 2026-11-10 루틴 고치기: 선생님이 폰에서 고친 루틴을 시트 "루틴" 탭에 저장 → 회원 PT 노트가 열릴 때 바로 바뀜.
//            고칠 때마다 "루틴기록" 탭에 전체 내용이 한 줄씩 쌓임(되살리기용). 선생님 열쇠는 아래 RT_KEY_HASH(열쇠 자체는 여기 없음).
const SHEET = '출석';
const RT_SHEET = '루틴';
const RT_LOG = '루틴기록';
const BN_SHEET = '전체공지';
const KV_SHEET = '저장소';
const RT_KEY_HASH = '6916c86079386c632e39f027f0a8d5d27a2a5852864d18d75ccde332f8928343';
const IB_SHEET = '인바디';
const IB_FOLDER = 'PT노트 인바디 사진';
const BP_SHEET = '몸사진';
const BP_FOLDER = 'PT노트 몸 사진';

function book_() {
  const act = SpreadsheetApp.getActiveSpreadsheet();
  if (act) return act;
  const p = PropertiesService.getScriptProperties();
  const id = p.getProperty('SS');
  if (id) { try { return SpreadsheetApp.openById(id); } catch (e) {} }
  const ss = SpreadsheetApp.create('PT노트 출석');
  p.setProperty('SS', ss.getId());
  return ss;
}

function sheet_() {
  const ss = book_();
  let s = ss.getSheetByName(SHEET);
  if (!s) {
    s = ss.insertSheet(SHEET);
    s.appendRow(['회원주소', '이름', '날짜', '시간', '기록시각']);
    s.setFrozenRows(1);
  }
  return s;
}

function txt_(v, f) {
  return v instanceof Date ? Utilities.formatDate(v, 'Asia/Seoul', f) : String(v);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

/* ---------------- 인바디 */
function ibSheet_() {
  const ss = book_();
  let s = ss.getSheetByName(IB_SHEET);
  if (!s) {
    s = ss.insertSheet(IB_SHEET);
    s.appendRow(['회원주소', '이름', '측정일', '체중', '골격근량', '체지방량', '체지방률', '사진ID', '기록ID', '기록시각']);
    s.setFrozenRows(1);
  }
  return s;
}

function ibFolder_() {
  const p = PropertiesService.getScriptProperties();
  const id = p.getProperty('IBF');
  if (id) { try { return DriveApp.getFolderById(id); } catch (e) {} }
  const f = DriveApp.createFolder(IB_FOLDER);
  p.setProperty('IBF', f.getId());
  return f;
}

function ibList_(m) {
  const v = ibSheet_().getDataRange().getValues();
  const out = [];
  for (let i = 1; i < v.length; i++) {
    if (v[i][0] !== m) continue;
    out.push({ id: String(v[i][8]), d: txt_(v[i][2], 'yyyy-MM-dd'), w: Number(v[i][3]), smm: Number(v[i][4]),
               bfm: Number(v[i][5]), pbf: Number(v[i][6]), img: !!v[i][7] });
  }
  out.sort(function (a, b) { return a.d < b.d ? -1 : a.d > b.d ? 1 : 0; });
  return out;
}

function ibRow_(s, m, id) {
  const v = s.getDataRange().getValues();
  for (let i = 1; i < v.length; i++) if (v[i][0] === m && String(v[i][8]) === id) return { row: i + 1, photo: String(v[i][7] || '') };
  return null;
}

function num_(x, lo, hi) {
  const n = Number(x);
  return isFinite(n) && n >= lo && n <= hi ? Math.round(n * 10) / 10 : null;
}

/* ---------------- 주간 몸 사진 (2026-11-13) */
function bpSheet_() { return rtSheet_(BP_SHEET, ['회원주소', '이름', '날짜', '사진ID', '기록ID', '기록시각']); }
function bpFolder_() {
  const p = PropertiesService.getScriptProperties();
  const id = p.getProperty('BPF');
  if (id) { try { return DriveApp.getFolderById(id); } catch (e) {} }
  const f = DriveApp.createFolder(BP_FOLDER);
  p.setProperty('BPF', f.getId());
  return f;
}
function bpList_(m) {
  const v = bpSheet_().getDataRange().getValues(), out = [];
  for (let i = 1; i < v.length; i++) if (v[i][0] === m) out.push({ id: String(v[i][4]), d: txt_(v[i][2], 'yyyy-MM-dd') });
  out.sort(function (a, b) { return a.d < b.d ? -1 : a.d > b.d ? 1 : 0; });
  return out;
}
function bpRow_(s, m, id) {
  const v = s.getDataRange().getValues();
  for (let i = 1; i < v.length; i++) if (v[i][0] === m && String(v[i][4]) === id) return { row: i + 1, photo: String(v[i][3] || '') };
  return null;
}

function memberOk_(m) { return /^[a-z0-9-]{3,40}$/.test(m); }

/* ---------------- 루틴 (선생님이 폰에서 고친 것) */
function rtSheet_(name, head) {
  const ss = book_();
  let s = ss.getSheetByName(name);
  if (!s) {
    s = ss.insertSheet(name);
    s.appendRow(head);
    s.setFrozenRows(1);
  }
  return s;
}
function rtMain_() { return rtSheet_(RT_SHEET, ['회원주소', '이름', '기준', '루틴(JSON)', '기록시각']); }
function rtLog_() { return rtSheet_(RT_LOG, ['회원주소', '이름', '기록시각', '할일', '루틴(JSON)']); }

function keyOk_(k) {
  if (!k) return false;
  const b = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, String(k), Utilities.Charset.UTF_8);
  const hex = b.map(function (x) { return ('0' + ((x + 256) % 256).toString(16)).slice(-2); }).join('');
  return hex === RT_KEY_HASH;
}

function rtGet_(m) {
  const v = rtMain_().getDataRange().getValues();
  for (let i = 1; i < v.length; i++) {
    if (v[i][0] !== m) continue;
    try { return JSON.parse(String(v[i][3])); } catch (e) { return null; }
  }
  return null;
}

function rtSet_(m, n, rec) {   // rec = null 이면 지움(원래 루틴으로)
  const s = rtMain_();
  const v = s.getDataRange().getValues();
  let row = -1;
  for (let i = 1; i < v.length; i++) if (v[i][0] === m) { row = i + 1; break; }
  const js = rec ? JSON.stringify(rec) : '';
  rtLog_().appendRow([m, n, new Date(), rec ? '저장' : '원래대로', js]);
  if (!rec) { if (row > 0) s.deleteRow(row); return; }
  const line = [m, n, String(rec.base || ''), js, new Date()];
  if (row > 0) s.getRange(row, 1, 1, line.length).setValues([line]);
  else s.appendRow(line);
}

/* ---------------- 전체 공지 (선생님 페이지에서 쓰는 공지 — 모든 회원에게) */
function bnSheet_() { return rtSheet_(BN_SHEET, ['번호', '날짜', '제목', '내용', '바로가기', '기록시각']); }
function bnList_() {
  const v = bnSheet_().getDataRange().getValues(), out = [], lim = Date.now() - 60 * 86400000;
  for (let i = v.length - 1; i >= 1; i--) {
    const at = v[i][5] instanceof Date ? v[i][5].getTime() : Date.now();
    if (at < lim) continue;
    out.push({ id: String(v[i][0]), date: String(v[i][1]), title: String(v[i][2]), body: String(v[i][3]), link: String(v[i][4] || '') });
    if (out.length >= 20) break;
  }
  return out;
}

/* ---------------- 범용 저장소 (이름 → JSON 값) */
function kvSheet_() { return rtSheet_(KV_SHEET, ['이름', '값(JSON)', '기록시각']); }
function kvAll_() {
  const v = kvSheet_().getDataRange().getValues(), o = {};
  for (let i = 1; i < v.length; i++) { try { o[String(v[i][0])] = JSON.parse(String(v[i][1])); } catch (e) {} }
  return o;
}
function kvFor_(m) {   // 회원 노트가 받는 것
  const all = kvAll_(), o = {};
  Object.keys(all).forEach(function (k) {
    if (k.indexOf('pub:all:') === 0 || k.indexOf('pub:m:' + m + ':') === 0 || k.indexOf('mw:' + m + ':') === 0) o[k] = all[k];
  });
  return o;
}
function kvSet_(k, val) {   // val === null 이면 지움
  const s = kvSheet_(), v = s.getDataRange().getValues();
  let row = -1;
  for (let i = 1; i < v.length; i++) if (String(v[i][0]) === k) { row = i + 1; break; }
  if (val === null) { if (row > 0) s.deleteRow(row); return; }
  const line = [k, JSON.stringify(val), new Date()];
  if (row > 0) s.getRange(row, 1, 1, 3).setValues([line]); else s.appendRow(line);
}

/* ---------------- GET: 출석 + 인바디 보기·사진·삭제 */
function doGet(e) {
  const p = (e && e.parameter) || {};
  const m = String(p.m || '').trim();
  if (!memberOk_(m)) return json_({ ok: false, error: 'member' });

  if (p.a === 'inbody') return json_({ ok: true, inbody: ibList_(m) });
  if (p.a === 'bn') return json_({ ok: true, bnotices: bnList_() });
  if (p.a === 'inbody_img') {
    const r = ibRow_(ibSheet_(), m, String(p.id || ''));
    if (!r || !r.photo) return json_({ ok: false, error: 'photo' });
    const blob = DriveApp.getFileById(r.photo).getBlob();
    return json_({ ok: true, data: 'data:' + blob.getContentType() + ';base64,' + Utilities.base64Encode(blob.getBytes()) });
  }
  if (p.a === 'bp') return json_({ ok: true, photos: bpList_(m) });
  if (p.a === 'bp_img') {
    const r = bpRow_(bpSheet_(), m, String(p.id || ''));
    if (!r || !r.photo) return json_({ ok: false, error: 'photo' });
    const blob = DriveApp.getFileById(r.photo).getBlob();
    return json_({ ok: true, data: 'data:' + blob.getContentType() + ';base64,' + Utilities.base64Encode(blob.getBytes()) });
  }
  if (p.a === 'bp_del') {
    const lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      const s = bpSheet_(), r = bpRow_(s, m, String(p.id || ''));
      if (r) { if (r.photo) { try { DriveApp.getFileById(r.photo).setTrashed(true); } catch (err) {} } s.deleteRow(r.row); }
      return json_({ ok: true, photos: bpList_(m) });
    } finally { lock.releaseLock(); }
  }
  if (p.a === 'inbody_del') {
    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      const s = ibSheet_();
      const r = ibRow_(s, m, String(p.id || ''));
      if (r) {
        if (r.photo) { try { DriveApp.getFileById(r.photo).setTrashed(true); } catch (err) {} }
        s.deleteRow(r.row);
      }
      return json_({ ok: true, inbody: ibList_(m) });
    } finally {
      lock.releaseLock();
    }
  }

  /* 2026-11-11: 잠금(lock)은 출석 쓰기(check/uncheck)할 때만. 보기만 할 땐 잠그지 않음
     → 선생님 페이지가 회원 여러 명을 한꺼번에 불러도 줄 서다 실패하지 않고, 루틴 저장도 안 막힘 */
  const s = sheet_();
  if (p.a === 'check' || p.a === 'uncheck') {
    const d = String(p.d || '');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) return json_({ ok: false, error: 'date' });
    const lock = LockService.getScriptLock();
    lock.waitLock(25000);
    try {
      const v = s.getDataRange().getValues();
      let row = -1;
      for (let i = 1; i < v.length; i++) {
        if (v[i][0] === m && txt_(v[i][2], 'yyyy-MM-dd') === d) { row = i + 1; break; }
      }
      if (p.a === 'check' && row < 0) {
        s.appendRow([m, String(p.n || ''), "'" + d, "'" + String(p.t || ''), new Date()]);
      }
      if (p.a === 'uncheck' && row > 0) s.deleteRow(row);
      SpreadsheetApp.flush();
    } finally {
      lock.releaseLock();
    }
  }
  const all = s.getDataRange().getValues();
  const days = {};
  for (let i = 1; i < all.length; i++) {
    if (all[i][0] === m) days[txt_(all[i][2], 'yyyy-MM-dd')] = txt_(all[i][3], 'HH:mm');
  }
  let routine = null, bnotices = [], kv = {};
  try { routine = rtGet_(m); } catch (err) {}
  try { bnotices = bnList_(); } catch (err) {}
  try { kv = kvFor_(m); } catch (err) {}
  return json_({ ok: true, days: days, routine: routine, bnotices: bnotices, kv: kv });
}

/* 결과지 사진 → 글자 (구글 드라이브 OCR: 사진을 구글 문서로 바꿔 글자만 읽고 바로 휴지통) */
function ocr_(b64) {
  const blob = Utilities.newBlob(Utilities.base64Decode(b64), 'image/jpeg', 'inbody_ocr.jpg');
  let id = null;
  try {
    id = Drive.Files.create({ name: 'inbody_ocr_tmp', mimeType: 'application/vnd.google-apps.document' }, blob, { ocrLanguage: 'ko' }).id;   // Drive API v3
  } catch (e3) {
    id = Drive.Files.insert({ title: 'inbody_ocr_tmp', mimeType: 'application/vnd.google-apps.document' }, blob, { ocr: true, ocrLanguage: 'ko' }).id;   // v2
  }
  try {
    return DocumentApp.openById(id).getBody().getText();
  } finally {
    try { DriveApp.getFileById(id).setTrashed(true); } catch (e) {}
  }
}

/* ---------------- POST: 인바디 올리기 · 결과지 읽기 (본문 = JSON 글자) */
function doPost(e) {
  let b;
  try { b = JSON.parse((e && e.postData && e.postData.contents) || '{}'); } catch (err) { return json_({ ok: false, error: 'body' }); }
  const m = String(b.m || '').trim();
  if (!memberOk_(m)) return json_({ ok: false, error: 'member' });
  if (b.a === 'inbody_ocr') {
    if (!b.img || String(b.img).length > 8000000) return json_({ ok: false, error: 'img' });
    try { return json_({ ok: true, text: ocr_(String(b.img)) }); }
    catch (err) { return json_({ ok: false, error: 'ocr', msg: String(err) }); }
  }
  if (b.a === 'kv_get') {   // 선생님: 이름 앞부분(prefix)으로 읽기
    if (!keyOk_(b.key)) return json_({ ok: false, error: 'key' });
    const all = kvAll_(), pre = String(b.prefix || ''), o = {};
    Object.keys(all).forEach(function (k) { if (k.indexOf(pre) === 0) o[k] = all[k]; });
    return json_({ ok: true, kv: o });
  }
  if (b.a === 'kv_set') {   // {k, v} 또는 {items:{k:v,…}} — v가 null이면 지움
    const items = b.items && typeof b.items === 'object' ? b.items : (function () { const o = {}; o[String(b.k || '')] = b.v === undefined ? null : b.v; return o; })();
    const ks = Object.keys(items);
    if (!ks.length || ks.length > 50) return json_({ ok: false, error: 'items' });
    const coach = keyOk_(b.key);
    for (let i = 0; i < ks.length; i++) {
      const k = ks[i];
      if (!/^[a-z0-9:_\-.]{3,120}$/i.test(k)) return json_({ ok: false, error: 'name' });
      if (JSON.stringify(items[k]).length > 40000) return json_({ ok: false, error: 'size' });
      const memberW = k.indexOf('mw:' + m + ':') === 0 && JSON.stringify(items[k]).length <= 4000;
      if (!coach && !memberW) return json_({ ok: false, error: 'key' });
    }
    const lock = LockService.getScriptLock();
    lock.waitLock(25000);
    try {
      ks.forEach(function (k) { kvSet_(k, items[k] === undefined ? null : items[k]); });
      SpreadsheetApp.flush();
      return json_({ ok: true });
    } finally {
      lock.releaseLock();
    }
  }
  if (b.a === 'bn_add' || b.a === 'bn_del') {
    if (!keyOk_(b.key)) return json_({ ok: false, error: 'key' });
    const lock = LockService.getScriptLock();
    lock.waitLock(25000);
    try {
      const s = bnSheet_();
      if (b.a === 'bn_add') {
        const t = String(b.title || '').trim().slice(0, 80), body = String(b.body || '').trim().slice(0, 600);
        if (!t) return json_({ ok: false, error: 'title' });
        const link = /^[a-z0-9-]{0,30}$/.test(String(b.link || '')) ? String(b.link || '') : '';
        const now = new Date();
        s.appendRow([Utilities.getUuid().slice(0, 8), Utilities.formatDate(now, 'Asia/Seoul', 'yyyy. M. d'), t, body, link, now]);
      } else {
        const v = s.getDataRange().getValues();
        for (let i = v.length - 1; i >= 1; i--) if (String(v[i][0]) === String(b.id || '')) { s.deleteRow(i + 1); break; }
      }
      SpreadsheetApp.flush();
      return json_({ ok: true, bnotices: bnList_() });
    } finally {
      lock.releaseLock();
    }
  }
  if (b.a === 'routine_key') return json_({ ok: keyOk_(b.key), error: keyOk_(b.key) ? '' : 'key' });
  if (b.a === 'routine_save' || b.a === 'routine_reset') {
    if (!keyOk_(b.key)) return json_({ ok: false, error: 'key' });
    let rec = null;
    if (b.a === 'routine_save') {
      rec = b.rec;
      if (!rec || typeof rec !== 'object' || !rec.routine || !Array.isArray(rec.routine.days)) return json_({ ok: false, error: 'routine' });
      if (JSON.stringify(rec).length > 45000) return json_({ ok: false, error: 'size' });
      rec.at = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm');
    }
    const lock = LockService.getScriptLock();
    lock.waitLock(25000);
    try {
      rtSet_(m, String(b.n || ''), rec);
      SpreadsheetApp.flush();
      return json_({ ok: true, routine: rec });
    } finally {
      lock.releaseLock();
    }
  }
  if (b.a === 'bp_add') {
    const d = String(b.d || '');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) return json_({ ok: false, error: 'date' });
    if (!b.img || String(b.img).length > 8000000) return json_({ ok: false, error: 'img' });
    const lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      const blob = Utilities.newBlob(Utilities.base64Decode(String(b.img)), 'image/jpeg', m + '_' + d + '_' + Date.now() + '.jpg');
      const photo = bpFolder_().createFile(blob).getId();
      const id = Utilities.getUuid().replace(/-/g, '').slice(0, 10);
      bpSheet_().appendRow([m, String(b.n || ''), "'" + d, photo, id, new Date()]);
      return json_({ ok: true, photos: bpList_(m) });
    } finally { lock.releaseLock(); }
  }
  if (b.a !== 'inbody_add') return json_({ ok: false, error: 'action' });
  const d = String(b.d || '');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) return json_({ ok: false, error: 'date' });
  const w = num_(b.w, 20, 300), smm = num_(b.smm, 3, 90), pbf = num_(b.pbf, 1, 75);
  let bfm = num_(b.bfm, 0.5, 200);
  if (w === null || smm === null || pbf === null) return json_({ ok: false, error: 'number' });
  if (bfm === null) bfm = Math.round(w * pbf) / 100;

  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    let photo = '';
    if (b.img && String(b.img).length < 8000000) {
      const blob = Utilities.newBlob(Utilities.base64Decode(String(b.img)), 'image/jpeg', m + '_' + d + '_' + Date.now() + '.jpg');
      photo = ibFolder_().createFile(blob).getId();
    }
    const id = Utilities.getUuid().replace(/-/g, '').slice(0, 10);
    ibSheet_().appendRow([m, String(b.n || ''), "'" + d, w, smm, bfm, pbf, photo, id, new Date()]);
    return json_({ ok: true, inbody: ibList_(m) });
  } finally {
    lock.releaseLock();
  }
}
