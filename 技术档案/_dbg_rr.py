# -*- coding: utf-8 -*-
"""把 message / message_end 的完整 payload 打出来，定位 retriever_resources 到底在哪。"""
import json, os, ssl, sys, time, urllib.request
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "j5qWmoi0m0UYWDpj"

req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
    TOK = json.loads(r.read().decode())["access_token"]

q = "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"
body = json.dumps({"response_mode": "streaming", "conversation_id": "", "query": q,
                   "inputs": {"user_input": q}, "parent_message_id": None}).encode()
r = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
    headers={"Content-Type": "application/json", "X-App-Code": SITE,
             "authorization": "Bearer " + TOK, "auth-token": "Bearer " + TOK})
with urllib.request.urlopen(r, context=CTX, timeout=400) as resp:
    raw = resp.read().decode("utf-8", "replace")

seen = {}
for blk in raw.replace("\r\n", "\n").split("\n\n"):
    if not blk.startswith("data:"): continue
    try: j = json.loads(blk[5:].strip())
    except Exception: continue
    e = j.get("event")
    seen.setdefault(e, j)

print("事件种类:", sorted(seen.keys()))
for e in ["message_end", "workflow_finished"]:
    if e in seen:
        j = seen[e]
        print("\n=== %s 顶层 keys: %s" % (e, sorted(j.keys())))
        d = j.get("data") or {}
        print("    data keys:", sorted(d.keys()))
        md = d.get("metadata")
        if md is not None:
            print("    metadata type:", type(md).__name__, "| keys:", sorted(md.keys()) if isinstance(md, dict) else str(md)[:200])
            if isinstance(md, dict):
                rrl = md.get("retriever_resources")
                print("    retriever_resources:", type(rrl).__name__, len(rrl) if isinstance(rrl, list) else rrl)
        for k in ["retriever_resources", "citations", "files", "annotations"]:
            if k in d: print("    data.%s:" % k, json.dumps(d[k], ensure_ascii=False)[:200])
# message 事件里也可能带
if "message" in seen:
    print("\n=== message 事件 keys:", sorted(seen["message"].keys()))
    for k in ["retriever_resources", "metadata", "citations"]:
        if k in seen["message"]: print("    message.%s:" % k, json.dumps(seen["message"][k], ensure_ascii=False)[:300])
