# -*- coding: utf-8 -*-
"""探明 /v1/chat-messages（blocking）的响应结构：是否带 metadata.retriever_resources。"""
import json
import ssl
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://aiagent.cqut.edu.cn:31134"
KEY = "app-8PKbSyrPSFnPGjQ5AQX6u1Zl"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

Q = "我是化学工程与工艺专业大四，想在重庆找校招岗位"
body = {"inputs": {"user_input": Q, "ctx": ""}, "query": Q,
        "response_mode": "blocking", "conversation_id": "", "user": "uprobe" + "1"}
req = urllib.request.Request(BASE + "/v1/chat-messages", data=json.dumps(body).encode(),
                             method="POST",
                             headers={"Authorization": "Bearer " + KEY,
                                      "Content-Type": "application/json"})
with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
    payload = json.loads(r.read().decode("utf-8", "replace"))

print("顶层键：%s" % ", ".join(sorted(payload.keys())))
for key in ("event", "message_id", "conversation_id", "mode"):
    if key in payload:
        print("  %-16s %s" % (key, payload[key]))
print("  answer 长度      %d" % len(payload.get("answer") or ""))

md = payload.get("metadata") or {}
print("")
print("metadata 键：%s" % ", ".join(sorted(md.keys())))
rr = md.get("retriever_resources") or []
print("retriever_resources %d 条" % len(rr))
for item in rr[:6]:
    print("   score=%-6s dataset=%-22s doc=%s" % (
        round(item.get("score") or 0, 3),
        (item.get("dataset_name") or item.get("dataset_id") or "")[:20],
        (item.get("document_name") or "")[:40]))
if rr:
    print("")
    print("首条完整字段：%s" % ", ".join(sorted(rr[0].keys())))
