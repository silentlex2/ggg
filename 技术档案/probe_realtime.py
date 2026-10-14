#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 v2 版本的实时政策源与官方文号引用。

用法：python probe_realtime.py <站点码>
"""
import json, os, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def site_code():
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    p = os.path.join(HERE, "readysite.txt")
    if os.path.exists(p):
        return open(p, encoding="utf-8").read().strip()
    sys.exit("缺少站点码")


def token(site):
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": site})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def ask(site, tok, query, extra=None):
    body = json.dumps({
        "response_mode": "streaming", "conversation_id": "", "query": query,
        "inputs": dict({"user_input": query}, **(extra or {})), "parent_message_id": None,
    }).encode()
    req = urllib.request.Request(
        BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": site,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        raw = r.read().decode("utf-8", "replace")
    cost = time.time() - t0
    ans, chain, wf, failed = "", [], "", []
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        ev = j.get("event")
        if ev == "message":
            ans += j.get("answer", "")
        elif ev == "node_finished":
            d = j.get("data", {})
            chain.append("%s[%s]" % (d.get("title"), d.get("status")))
            if d.get("status") == "failed":
                failed.append(d.get("title"))
        elif ev == "workflow_finished":
            wf = (j.get("data") or {}).get("workflow_id", "")
    return {"cost": cost, "answer": ans, "chain": chain, "wf": wf, "failed": failed}


CASES = [
    ("实时政策动态", "最近有什么新的就业政策动态？"),
    ("补贴官方文号", "重庆高校毕业生有哪些就业补贴？"),
]


def main():
    site = site_code()
    tok = token(site)
    print("站点:", site, " 凭证: OK")
    for name, q in CASES:
        r = ask(site, tok, q)
        print("\n" + "=" * 72)
        print("【%s】%s" % (name, q))
        print("耗时 %.1fs   wf=%s   失败节点=%s" % (r["cost"], r["wf"][:8], r["failed"] or "无"))
        print("节点链: " + " -> ".join(r["chain"]))
        print("-" * 72)
        print(r["answer"])


if __name__ == "__main__":
    main()
