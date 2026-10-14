# -*- coding: utf-8 -*-
"""把 v6 应用的 features.opening_statement 恢复干净（去掉热更新探测标记）。"""
import json, os, ssl, urllib.request, urllib.error
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
V6APP = "9fd8b002-1a55-456e-90b9-991e7ff8a621"
MARK = "【热更新探测20261014】"

def tok(): return open(os.path.join(HERE, "scratch", ".token"), encoding="utf-8").read().strip()
def api(p, m="GET", b=None):
    t = tok(); h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if b is not None:
        data = json.dumps(b).encode(); h["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + p, data=data, headers=h, method=m)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=90) as resp:
            raw = resp.read().decode()
            return resp.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode())
        except Exception: return e.code, None

s, dr = api("/console/api/apps/%s/workflows/draft" % V6APP)
op = dr["features"].get("opening_statement") or ""
print("恢复前前 30 字:", op[:30].replace("\n", "⏎"))
if op.startswith(MARK):
    dr["features"]["opening_statement"] = op[len(MARK):].lstrip("\n")
    s2, r2 = api("/console/api/apps/%s/workflows/draft" % V6APP, "POST", dr)
    print("save ->", s2, (r2 or {}).get("hash", "")[:16])
    s3, r3 = api("/console/api/apps/%s/workflows/publish" % V6APP, "POST", {"marked_name": "", "marked_comment": "恢复 features 探测标记"})
    print("publish ->", s3)
    s4, d4 = api("/console/api/apps/%s/workflows/draft" % V6APP)
    print("恢复后前 30 字:", (d4["features"].get("opening_statement") or "")[:30].replace("\n", "⏎"))
    print("残留标记:", "有" if MARK in (d4["features"].get("opening_statement") or "") else "无 ✅")
else:
    print("无标记，无需恢复")
