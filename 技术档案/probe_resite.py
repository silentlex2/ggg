#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""恢复站点并读取线上版本。"""
import json, os, ssl, sys, time, urllib.request, urllib.error
sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
APP = "69fa1c02-27bf-41fc-a7d2-0c068480c034"
SITE = open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()
TOK = open(os.path.join(HERE, "scratch", ".token"), encoding="utf-8").read().strip()
H = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def call(path, body=None, timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method="POST" if data else "GET", headers=H)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:200]
    except Exception as e:
        return -1, repr(e)


st, body = call("/console/api/apps/%s/site-enable" % APP, {"enable_site": True})
ok = False
if st == 200:
    j = json.loads(body)
    ok = j.get("enable_site") is True
    print("站点已开启: enable_site=%s  site=%s" % (j.get("enable_site"), (j.get("site") or {}).get("code")))
else:
    print("开启返回 %d %s" % (st, body[:200]))

# 确认站点可访问
time.sleep(2)
req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        t = json.loads(r.read().decode())["access_token"]
    print("passport OK, 站点可访问")
except Exception as e:
    print("passport 失败:", repr(e)); sys.exit(1)

q = "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"
payload = {"response_mode": "streaming", "conversation_id": "", "query": q,
           "inputs": {"user_input": q}, "parent_message_id": None}
rq = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(payload).encode(), method="POST",
                            headers={"Content-Type": "application/json", "X-App-Code": SITE,
                                     "authorization": "Bearer " + t, "auth-token": "Bearer " + t})
t0 = time.time()
with urllib.request.urlopen(rq, context=CTX, timeout=300) as r:
    raw = r.read().decode("utf-8", "replace")
wid, n_rr, scores = None, None, []
for blk in raw.replace("\r\n", "\n").split("\n\n"):
    if not blk.startswith("data:"):
        continue
    try:
        j = json.loads(blk[5:].strip())
    except Exception:
        continue
    if j.get("event") == "workflow_finished":
        wid = j.get("data", {}).get("workflow_id")
    if j.get("event") == "message_end":
        rr = ((j.get("data") or {}).get("metadata") or {}).get("retriever_resources") or []
        n_rr = len(rr)
        scores = [it.get("score") for it in rr]
print("\n线上 workflow_id = %s" % wid)
print("retriever_resources = %s 条  scores=%s" % (n_rr, scores))
print("目标版本 = e6c5f433-0800-4a34-a051-2f722aa9960f")
print("耗时 %.1fs" % (time.time() - t0))
