# -*- coding: utf-8 -*-
"""节点级耗时剖析：把一次回答的耗时拆到每个节点，找出真正的串行瓶颈。

用法：
    python probe_latency.py                # 默认跑政策 / 岗位 / 面试三条重链路
    python probe_latency.py "自定义问题"     # 只跑一条

读站点码同 readysite.txt（单一真源），只要公开站点权限，不需要控制台 token。
输出：按分支列出 节点标题 -> elapsed_time，并单独标出 LLM / 检索 / HTTP 的耗时占比。
"""
import json
import os
import ssl
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

with open(os.path.join(HERE, "readysite.txt"), encoding="utf-8") as f:
    SITE = f.read().strip()

CASES = [
    ("政策咨询", "重庆应届生有哪些就业补贴可以领"),
    ("岗位匹配", "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"),
    ("模拟面试", "来一场模拟面试，我目标岗位是化工工艺工程师"),
]
if len(sys.argv) > 1:
    CASES = [("自定义", sys.argv[1])]


def passport():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def run(q, tok):
    body = json.dumps({"response_mode": "streaming", "conversation_id": "", "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=400) as resp:
        raw = resp.read().decode("utf-8", "replace")
    total = time.time() - t0
    nodes, ans = [], ""
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        if j.get("event") == "message":
            ans += j.get("answer", "")
        if j.get("event") == "node_finished":
            d = j.get("data") or {}
            nodes.append((d.get("title") or d.get("node_id", "?"),
                          d.get("node_type") or "", round(float(d.get("elapsed_time") or 0), 2)))
    return total, nodes, ans


def main():
    tok = passport()
    print("站点 %s" % SITE)
    for name, q in CASES:
        total, nodes, ans = run(q, tok)
        print()
        print("=" * 70)
        print("%s  |  总耗时 %.1fs  |  答案 %d 字" % (name, total, len(ans)))
        print("-" * 70)
        accounted = 0.0
        for title, ntype, sec in nodes:
            accounted += sec
            bar = "#" * min(40, int(sec * 4))
            print("  %-14s %-22s %6.2fs %s" % (title, ntype, sec, bar))
        print("  %-14s %-22s %6.2fs   (节点合计 / 总耗时 = %.0f%%)" % (
            "", "合计", accounted, 100.0 * accounted / total if total else 0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
