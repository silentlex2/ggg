# -*- coding: utf-8 -*-
"""探测 2：站点开场白/预置问题存在哪、能不能热更新。"""
import json, os, ssl, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
V6APP = "9fd8b002-1a55-456e-90b9-991e7ff8a621"
V6SITE = "g2XDtP2IvbgTKh8k"
V7SITE = "j5qWmoi0m0UYWDpj"


def tok(): return token()


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
    except Exception as e:
        return -1, str(e)


def pub(path, site, auth=None):
    h = {"X-App-Code": site}
    if auth: h["Authorization"] = "Bearer " + auth
    r = urllib.request.Request(BASE + path, headers=h)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=30) as resp:
            raw = resp.read().decode()
            return resp.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode())
        except Exception: return e.code, None
    except Exception as e:
        return -1, str(e)

# 拿 access_token
s, d = pub("/api/passport", V7SITE)
TOK = d["access_token"] if isinstance(d, dict) else None
print("passport ->", s, "| token", (TOK or "")[:12] + "...")

print()
print("== 1. /api/parameters（带 token）==")
s, d = pub("/api/parameters", V7SITE, TOK)
if isinstance(d, dict):
    print("  status", s, "| keys:", sorted(d.keys()))
    op = (d.get("opening_statement") or "")
    print("  opening_statement:", op[:70].replace("\n", "⏎"))
    print("  suggested_questions:", json.dumps(d.get("suggested_questions"), ensure_ascii=False)[:240])
    print("  file_upload:", json.dumps(d.get("file_upload"), ensure_ascii=False)[:200])
else:
    print("  status", s, d)

print()
print("== 2. v6 应用 draft 顶层结构 ==")
s, dr = api("/console/api/apps/%s/workflows/draft" % V6APP)
print("  status", s, "| 顶层 keys:", sorted(dr.keys()) if isinstance(dr, dict) else dr)
if isinstance(dr, dict):
    feat = dr.get("features") or {}
    op = feat.get("opening_statement") or ""
    print("  features.opening_statement 前 50:", op[:50].replace("\n", "⏎"))
    print("  features.suggested_questions:", json.dumps(feat.get("suggested_questions"), ensure_ascii=False)[:200])
    print("  graph keys:", sorted(dr.get("graph", {}).keys()))

print()
print("== 3. 给 v6 features 加标记 → push → publish → 看站点 ==")
MARK = "【热更新探测20261014】"
if isinstance(dr, dict) and "features" in dr:
    op0 = dr["features"].get("opening_statement") or ""
    dr["features"]["opening_statement"] = MARK + "\n" + op0
    s2, r2 = api("/console/api/apps/%s/workflows/draft" % V6APP, "POST", dr)
    print("  save ->", s2, (r2 or {}).get("hash", "")[:16] if isinstance(r2, dict) else str(r2)[:80])
    s3, r3 = api("/console/api/apps/%s/workflows/publish" % V6APP, "POST", {"marked_name": "", "marked_comment": "features 热更新探测"})
    print("  publish ->", s3, (r3 or {}).get("workflow_id") if isinstance(r3, dict) else str(r3)[:80])
    s4, d4 = pub("/api/parameters", V6SITE, TOK)
    o4 = (d4.get("opening_statement") or "") if isinstance(d4, dict) else ""
    print("  站点现在的前 40 字:", o4[:40].replace("\n", "⏎"))
    print("  →", "✅ features 可热更新！" if MARK in o4 else "❌ features 也被钉死")
