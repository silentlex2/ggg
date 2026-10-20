# -*- coding: utf-8 -*-
"""v13 验收：五分支 + think 泄漏 + 截断 + 耗时，一条命令看完。

用法：
    python verify_v13.py <站点码>
    python verify_v13.py            # 读 readysite.txt
"""
import json, os, re, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

SITE = sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()

CASES = [
    ("闲聊", "你好", ["简历", "岗位", "面试", "政策"]),
    ("简历诊断", "帮我看看我的简历有什么问题", ["简历"]),
    ("岗位匹配", "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位", ["岗位"]),
    ("模拟面试", "来一场模拟面试，我目标岗位是化工工艺工程师", ["第 1 题"]),
    ("政策咨询", "重庆应届生有哪些就业补贴可以领", ["补贴"]),
]


def passport():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def ask(q, tok):
    body = json.dumps({"response_mode": "streaming", "conversation_id": "", "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=400) as r:
        raw = r.read().decode("utf-8", "replace")
    sec = time.time() - t0
    ans, nodes, wf = "", [], ""
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
            nodes.append((j.get("data") or {}).get("title"))
        if j.get("event") == "workflow_finished":
            wf = (j.get("data") or {}).get("workflow_id") or wf
    return ans, nodes, sec, wf


def main():
    tok = passport()
    print("站点 %s | 节点数（首轮）待看" % SITE)
    print("%-8s %-6s %6s %6s %-6s %-6s %s" % ("分支", "字数", "耗时", "节点", "think", "截断", "关键字"))
    bad = 0
    for name, q, must in CASES:
        ans, nodes, sec, wf = ask(q, tok)
        think = ("<think" in ans.lower()) or ("</think>" in ans.lower())
        tail = ans.rstrip()[-1:] if ans.strip() else ""
        trunc = len(ans) > 300 and tail not in "。！？…”）】》!?."
        miss = [m for m in must if m not in ans]
        ok = (not think) and (not trunc) and (not miss)
        bad += 0 if ok else 1
        print("%-8s %-6d %6.1fs %6d %-6s %-6s %s  wf=%s" % (
            name, len(ans), sec, len(nodes), "LEAK" if think else "ok",
            "YES" if trunc else "no", ("缺 " + ",".join(miss)) if miss else "ok", (wf or "?")[:8]))
        if think:
            i = ans.lower().find("<think")
            print("       泄漏片段: %r" % ans[max(0, i - 30):i + 120])
        if trunc:
            print("       末尾: %r" % ans[-60:])
    print()
    print("---VERIFY_SUMMARY---")
    print("SITE: %s" % SITE)
    print("FAILED: %d / %d" % (bad, len(CASES)))
    print("---END---")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
