#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多轮追问/省略句兜底探测：验证「这两个城市里哪个更适合」这类省略句是否被接住。

用法：python probe_multiturn.py <站点码>
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


def ask(site, tok, query, conv=""):
    body = json.dumps({
        "response_mode": "streaming", "conversation_id": conv, "query": query,
        "inputs": {"user_input": query}, "parent_message_id": None,
    }).encode()
    req = urllib.request.Request(
        BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": site,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        raw = r.read().decode("utf-8", "replace")
    cost = time.time() - t0
    ans, chain, cid, failed = "", [], conv, []
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
            cid = j.get("conversation_id", cid) or cid
        elif ev == "node_finished":
            d = j.get("data", {})
            chain.append(d.get("title"))
            if d.get("status") == "failed":
                failed.append(d.get("title"))
    return {"cost": cost, "answer": ans, "chain": chain, "cid": cid, "failed": failed}


SCENARIOS = {
    "A": ("省略句追问（岗位匹配后）", [
        "我是车辆工程专业，想找重庆的机械设计岗位",
        "那这两个城市里哪个更适合我？",
    ]),
    "B": ("面试中途短承接", [
        "来一场模拟面试，岗位是化工工艺工程师",
        "我叫张明，重庆理工大学化学化工学院大三。",
        "嗯，好的。",
    ]),
    "C": ("面试中途跑偏到闲聊", [
        "来一场模拟面试，岗位是化工工艺工程师",
        "我叫张明，重庆理工大学化学化工学院大三。",
        "今天天气不错啊",
    ]),
}


def main():
    key = sys.argv[2] if len(sys.argv) > 2 else "A"
    name, turns = SCENARIOS[key]
    site = site_code()
    tok = token(site)
    print("场景 %s: %s   站点: %s" % (key, name, site))
    conv = ""
    for i, q in enumerate(turns, 1):
        r = ask(site, tok, q, conv)
        conv = r["cid"]
        branch = "闲聊" if "闲聊引导" in r["chain"] else ("岗位" if "岗位匹配" in r["chain"] else ("面试" if "模拟面试官" in r["chain"] else "其他"))
        print("\n" + "=" * 72)
        print("第 %d 轮: %s" % (i, q))
        print("耗时 %.1fs  分支=%s  失败=%s" % (r["cost"], branch, r["failed"] or "无"))
        print("节点链: " + " -> ".join(r["chain"]))
        print("-" * 72)
        print(r["answer"][:500])


if __name__ == "__main__":
    main()
