#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""模拟面试全流程多轮回归（验证 memory 窗口 8 是否够用、进度是否单调）。

用法：python probe_interview.py <站点码>
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


TURNS = [
    "我要来一场模拟面试，岗位是化工工艺工程师",
    "我叫张明，是重庆理工大学化学化工学院大三学生，专业是化学工程与工艺。",
    "我做过一个 Aspen Plus 的课程设计，模拟了一套甲醇精制流程，负责建模和参数优化。",
    "我在学生会待过两年，组织过一次 200 人的活动，中间和另一个部门有过分工上的冲突。",
    "我打算先在化工行业做技术岗，三到五年内考注册化工工程师。",
    "期望薪资我希望在 8000 左右，主要是看重成长空间。",
]


def progress(ans):
    import re
    m = re.search(r"(\d+)\s*/\s*5", ans)
    return m.group(1) + "/5" if m else "?"


def main():
    site = site_code()
    tok = token(site)
    print("站点:", site, " 凭证: OK")
    conv = ""
    seq = []
    for i, q in enumerate(TURNS, 1):
        r = ask(site, tok, q, conv)
        conv = r["cid"]
        seq.append(progress(r["answer"]))
        print("\n" + "=" * 72)
        print("第 %d 轮: %s" % (i, q))
        print("耗时 %.1fs  进度=%s  失败节点=%s" % (r["cost"], seq[-1], r["failed"] or "无"))
        print("节点链: " + " -> ".join(r["chain"]))
        print("-" * 72)
        print(r["answer"][:420])
    print("\n" + "#" * 72)
    print("进度序列:", " -> ".join(seq))
    print("走到了复盘报告:", "复盘" in TURNS and any("复盘" in ask(site, tok, "继续", conv)["answer"] for _ in [0]))
    print("会话ID:", conv)


if __name__ == "__main__":
    main()
