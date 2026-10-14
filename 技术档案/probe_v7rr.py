# -*- coding: utf-8 -*-
"""修正版：从 message_end 顶层取 metadata.retriever_resources。"""
import json, ssl, sys, time, urllib.request
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "j5qWmoi0m0UYWDpj"

req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
    TOK = json.loads(r.read().decode())["access_token"]

def ask(q):
    body = json.dumps({"response_mode": "streaming", "conversation_id": "", "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    r = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + TOK, "auth-token": "Bearer " + TOK})
    with urllib.request.urlopen(r, context=CTX, timeout=400) as resp:
        raw = resp.read().decode("utf-8", "replace")
    ans, rr, chain, md_keys = "", [], [], None
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"): continue
        try: j = json.loads(blk[5:].strip())
        except Exception: continue
        e = j.get("event")
        if e == "message": ans += j.get("answer", "")
        elif e == "message_end":
            md = j.get("metadata")
            md_keys = sorted(md.keys()) if isinstance(md, dict) else None
            rr = (md or {}).get("retriever_resources") or []
        elif e == "node_finished":
            chain.append((j.get("data") or {}).get("title"))
    return ans, rr, chain, md_keys

cases = [("岗位匹配", "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"),
         ("政策咨询", "重庆高校毕业生有什么求职补贴"),
         ("模拟面试", "我想练一下化工工艺工程师的面试")]
for name, q in cases:
    t0 = time.time(); ans, rr, chain, mk = ask(q); cost = time.time() - t0
    sc = [round((x.get("score") or 0), 4) for x in rr]
    docs = sorted({(x.get("document_name") or "")[:24] for x in rr})
    print("=" * 76)
    print("%s  %.1fs  条数=%d" % (name, cost, len(rr)))
    print("  metadata keys:", mk)
    print("  scores:", sc)
    print("  docs  :", docs)
    if sc:
        mx = max(sc)
        print("  ★ 形态:", "reranker 分" if mx > 0.75 else "加权混合分")
    print("  节点链:", " → ".join(chain))
