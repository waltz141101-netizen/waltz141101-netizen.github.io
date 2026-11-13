"""선생님 열쇠 만들기 — python3 _tools/make_key.py
열쇠(16자)와 지문(SHA-256)을 보여줌. 지문만 _tools/attendance_apps_script.gs 의 RT_KEY_HASH 에 넣고,
열쇠는 선생님께만 전달(저장소·채팅 기록에 남기지 말 것 — 공개 저장소). 선생님 폰: https://<사이트>/<coach 폴더>/#key=<열쇠> 를 한 번 열기."""
import secrets, string, hashlib
k = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(16))
print("열쇠(선생님께만):", k)
print("RT_KEY_HASH(코드에):", hashlib.sha256(k.encode()).hexdigest())
