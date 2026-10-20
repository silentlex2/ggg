# -*- coding: utf-8 -*-
"""线上实测：知识检索节点是否真的命中，retriever_resources 是否为空。"""
import json
import ssl
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
SITE = open("readysite.txt", encoding="utf-8").read().strip()

Q = "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"


def passport():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


tok = passport()
payload = {"response_mode": "streaming", "conversation_id": "", "query": Q,
           "inputs": {"user_input": Q}, "parent_message_id": None}
req = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(payload).encode(),
                             method="POST",
                             headers={"Content-Type": "application/json", "X-App-Code": SITE,
                                      "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
    raw = r.read().decode("utf-8", "replace")

answer = []
for blk in raw.replace("\r\n", "\n").split("\n\n"):
    if not blk.startswith("data:"):
        continue
    try:
        j = json.loads(blk[5:].strip())
    except Exception:  # noqa: BLE001
        continue
    ev = j.get("event")
    if ev == "node_finished":
        d = j.get("data", {})
        title = d.get("title") or ""
        if "知识" in title or "检索" in title:
            outs = d.get("outputs") or {}
            res = outs.get("result") or outs.get("result_str") or []
            n = len(res) if isinstance(res, list) else -1
            print("▶ 节点 %-12s status=%s 命中=%s" % (title, d.get("status"), n))
            if isinstance(res, list) and res:
                for it in res[:3]:
                    print("     score=%s doc=%s" % (it.get("score"), (it.get("title") or "")[:30]))
                    print("     %s" % (it.get("content") or "")[:160].replace("\n", " "))
    elif ev == "message_end":
        md = j.get("data", j).get("metadata", {}) or {}
        rr = md.get("retriever_resources") or []
        print("")
        print("retriever_resources: %d 条" % len(rr))
        for it in rr[:5]:
            print("   score=%s doc=%s" % (it.get("score"), (it.get("document_name") or "")[:40]))
    elif ev == "message":
        answer.append(j.get("answer") or "")

text = "".join(answer)
print("")
print("回答 %d 字" % len(text))
print(text[:700])
