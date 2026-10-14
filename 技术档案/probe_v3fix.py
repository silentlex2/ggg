#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, ssl, sys, time, urllib.request
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1]

def token(site):
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": site})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]

def ask(tok, q):
    body = json.dumps({"response_mode": "streaming", "conversation_id": "", "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        raw = r.read().decode("utf-8", "replace")
    ans, chain, wf = "", [], ""
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        if j.get("event") == "message":
            ans += j.get("answer", "")
        elif j.get("event") == "node_finished":
            chain.append(j.get("data", {}).get("title"))
        elif j.get("event") == "workflow_finished":
            wf = (j.get("data") or {}).get("workflow_id", "")
    return ans, chain, wf, time.time() - t0

tok = token(SITE)
print("站点:", SITE)
for q in ["继续", "美国 OPT 实习签证怎么申请？"]:
    a, c, wf, cost = ask(tok, q)
    print("\n" + "=" * 70)
    print("query=%r  耗时 %.1fs  wf=%s" % (q, cost, wf[:8]))
    print("节点链: " + " -> ".join(c))
    print("-" * 70)
    print(a[:400])
