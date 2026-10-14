# -*- coding: utf-8 -*-
"""探测：站点配置（开场白/预置问题/标题）能不能单独改写，而不换站点码。
用已关停的 f2e4f2a5 做写入实验，绝不碰正式站。
"""
import json, os, ssl, urllib.request, urllib.error
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
LAB = "f2e4f2a5-8e96-4a15-972d-4c2d5af57669"   # 已关停的实验应用
PROD = "4a634be6-bb6b-4c80-b8ca-7aa9e02ccede"  # 正式站

def tok(): return open(os.path.join(HERE, "scratch", ".token"), encoding="utf-8").read().strip()
def api(p, m="GET", b=None):
    t = tok(); h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if b is not None:
        data = json.dumps(b).encode(); h["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + p, data=data, headers=h, method=m)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=60) as resp:
            raw = resp.read().decode()
            return resp.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode())
        except Exception: return e.code, None
    except Exception as e:
        return -1, str(e)

print("== 1. 正式站 site 字段结构 ==")
s, a = api("/console/api/apps/%s" % PROD)
site = (a or {}).get("site") or {}
print("  status", s, "| site keys:", sorted(site.keys()))
for k in ["code", "title", "description", "default_language", "chat_color_theme", "prompt_public", "show_workflow_steps"]:
    print("   %-22s = %r" % (k, site.get(k)))
print("   opening_statement len =", len(site.get("opening_statement") or ""))
print("   suggested_questions   =", json.dumps(site.get("suggested_questions"), ensure_ascii=False)[:300])

print()
print("== 2. 各种可能的写入口逐个探（实验应用）==")
probes = [
    ("POST", "/console/api/apps/%s/site" % LAB),
    ("PUT",  "/console/api/apps/%s/site" % LAB),
    ("PATCH","/console/api/apps/%s/site" % LAB),
    ("POST", "/console/api/apps/%s/site/" % LAB),
    ("PUT",  "/console/api/apps/%s/site/" % LAB),
    ("PUT",  "/console/api/apps/%s" % LAB),
]
payload = {"opening_statement": "【PROBE-MARK】探测开场白", "suggested_questions": ["Q1", "Q2"]}
for m, p in probes:
    s, d = api(p, m, payload)
    print("  %-5s %-52s -> %s  %s" % (m, p.split("/console/api")[1], s, json.dumps(d, ensure_ascii=False)[:120] if isinstance(d, (dict, list)) else str(d)[:120]))
