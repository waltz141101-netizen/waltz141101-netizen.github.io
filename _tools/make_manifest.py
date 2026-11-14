"""회원 PT 노트를 '앱으로 설치'되게 하는 manifest 만들기 (2026-11-13)
python3 _tools/make_manifest.py m/<주소> "이름" M|F      → m/<주소>/manifest.webmanifest
회원 index.html 머리에 <link rel="manifest" href="manifest.webmanifest"> 가 있어야 함(_tools/member_template 에 들어 있음)"""
import json, os, sys
d, name, sex = sys.argv[1].rstrip("/"), sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "M")
slug = os.path.basename(d)
tag = "F" if sex == "F" else "M"
color = "#A0606A" if tag == "F" else "#1C1C1E"
short = name.replace(" · ", "·")
m = {
    "id": "/m/%s/" % slug,
    "name": "%s 회원님 PT 노트" % short,
    "short_name": ("%s PT노트" % short)[:12],
    "start_url": "/m/%s/" % slug,
    "scope": "/m/%s/" % slug,
    "display": "standalone",
    "background_color": "#F5F4F0",
    "theme_color": color,
    "icons": [
        {"src": "/assets/icon-note-%s-192.png" % tag, "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "/assets/icon-note-%s-512.png" % tag, "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "/assets/icon-note-%s-512.png" % tag, "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
open(os.path.join(d, "manifest.webmanifest"), "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
print("ok", d)
