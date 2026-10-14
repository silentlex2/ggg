# -*- coding: utf-8 -*-
"""单轮探测：打印完整 HTTP 错误体。"""
import json, ssl, sys, urllib.request, urllib.error
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "j5qWmoi0m0UYWDpj"
req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
    TOK = json.loads(r.read().decode())["access_token"]

q = sys.argv[2] if len(sys.argv) > 2 else "我想练一下化工工艺工程师的面试"
body = json.dumps({"response_mode": "streaming", "conversation_id": "", "query": q,
                   "inputs": {"user_input": q}, "parent_message_id": None}).encode()
r = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
    headers={"Content-Type": "application/json", "X-App-Code": SITE,
             "authorization": "Bearer " + TOK, "auth-token": "Bearer " + TOK})
try:
    with urllib.request.urlopen(r, context=CTX, timeout=400) as resp:
        raw = resp.read().decode("utf-8", "replace")
except urllib.error.HTTPError as e:
    print("HTTP", e.code)
    print(e.read().decode("utf-8", "replace")[:2000])
    sys.exit(1)
ans = ""
for blk in raw.replace("\r\n", "\n").split("\n\n"):
    if not blk.startswith("data:"): continue
    try: j = json.loads(blk[5:].strip())
    except Exception: continue
    if j.get("event") == "message": ans += j.get("answer", "")
print("OK, 回答 %d 字" % len(ans))
print(ans[:900])
