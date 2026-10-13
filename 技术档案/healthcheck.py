#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「职引」公开站点健康巡检。

一条命令跑完五个分支，报告：HTTP 状态 / 耗时 / 回答字数 / 是否泄漏 <think> / 是否有失败节点。

用法：
    python healthcheck.py            # 巡检 readysite.txt 里的站点
    python healthcheck.py <站点码>    # 巡检指定站点

退出码：0 = 全部通过；1 = 有分支异常；2 = 站点不可达（凭证/站点码问题）。
"""
import json, os, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

CASES = [
    ("闲聊",     "你好", {}),
    ("政策咨询", "重庆高校毕业生有哪些就业补贴？", {}),
    ("岗位匹配", "我是车辆工程专业，想找重庆的机械设计岗位", {"user_major": "车辆工程", "user_skills": "SolidWorks"}),
    ("模拟面试", "我要开始模拟面试", {}),
    ("简历诊断", "帮我看看简历", {}),
]

MIN_CHARS = {"闲聊": 20, "政策咨询": 300, "岗位匹配": 300, "模拟面试": 100, "简历诊断": 60}


def site_code():
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    p = os.path.join(HERE, "readysite.txt")
    if os.path.exists(p):
        return open(p, encoding="utf-8").read().strip()
    sys.exit("找不到 readysite.txt，请显式传入站点码")


def token(site):
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": site})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def ask(site, tok, query, extra):
    body = json.dumps({
        "response_mode": "streaming", "conversation_id": "", "query": query,
        "inputs": dict({"user_input": query}, **extra), "parent_message_id": None,
    }).encode()
    req = urllib.request.Request(
        BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": site,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=240) as r:
            raw = r.read().decode("utf-8", "replace")
    except Exception as e:
        return {"ok": False, "why": "请求异常: %s" % e}
    cost = time.time() - t0
    if not raw.lstrip().startswith("data:") and '"code"' in raw[:80]:
        try:
            msg = json.loads(raw).get("message", "")
        except Exception:
            msg = raw[:120]
        n = msg.count(")[]")
        return {"ok": False, "why": "HTTP 500 构建失败（%d 个节点）: %s" % (n, msg[:100])}
    ans, failed, wf = "", [], ""
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        d = j.get("data") or {}
        if j.get("event") == "node_finished":
            if d.get("status") == "failed":
                failed.append(d.get("title"))
        elif j.get("event") == "message":
            ans += j.get("answer", "")
        elif j.get("event") == "workflow_finished":
            wf = d.get("workflow_id", "")
    return {"ok": True, "cost": cost, "chars": len(ans), "failed": failed,
            "think": "<think" in ans, "wf": wf, "ans": ans}


def main():
    site = site_code()
    print("巡检站点: %s  (%s/chat/%s)" % (site, BASE, site))
    try:
        tok = token(site)
    except Exception as e:
        print("✗ 无法获取访问令牌，站点可能已关闭或站点码失效: %s" % e)
        return 2
    print("凭证获取: OK\n")
    bad = 0
    for name, q, extra in CASES:
        r = ask(site, tok, q, extra)
        if not r.get("ok"):
            print("✗ %-6s %s" % (name, r["why"]))
            bad += 1
            continue
        flags = []
        if r["chars"] < MIN_CHARS[name]:
            flags.append("字数偏少")
        if r["think"]:
            flags.append("泄漏<think>")
        if r["failed"]:
            flags.append("失败节点:" + ",".join(r["failed"]))
        status = "✓" if not flags else "✗"
        if flags:
            bad += 1
        print("%s %-6s %5.1fs %5d字  wf=%s %s" % (status, name, r["cost"], r["chars"], r["wf"][:8], " ".join(flags)))
        print("    " + r["ans"][:110].replace("\n", " ⏎ "))
    print()
    if bad:
        print("结果: %d/%d 个分支异常 —— 需要人工介入" % (bad, len(CASES)))
        return 1
    print("结果: %d/%d 全部正常" % (len(CASES), len(CASES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
