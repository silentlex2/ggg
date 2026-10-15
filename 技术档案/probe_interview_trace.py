#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""面试进度逐轮诊断：跑到出复盘为止（最多 8 轮），打印每轮进度与题型。
用法：python probe_interview_trace.py <站点码>
"""
import json, os, re, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()

def token(s):
    r = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": s})
    with urllib.request.urlopen(r, context=CTX, timeout=30) as x:
        return json.loads(x.read().decode())["access_token"]

TOK = token(SITE)
H = {"Content-Type": "application/json", "X-App-Code": SITE,
     "Authorization": "Bearer " + TOK, "auth-token": "Bearer " + TOK}

def ask(q, conv=""):
    p = {"response_mode": "streaming", "conversation_id": conv, "query": q,
         "inputs": {"user_input": q}, "parent_message_id": None}
    r = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(p).encode(), headers=H, method="POST")
    a = ""; cid = conv
    with urllib.request.urlopen(r, context=CTX, timeout=300) as x:
        for raw in x:
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"): continue
            try: e = json.loads(line[5:].strip())
            except Exception: continue
            if e.get("event") == "message": a += e.get("answer") or ""
            elif e.get("event") == "message_end": cid = e.get("conversation_id") or cid
    return a, cid

QS = [
 "老师好，我是化学工程与工艺专业大四学生，做过一个精馏塔课程设计，用 Aspen Plus 模拟，也参加过化工设计大赛。",
 "我在课程设计里负责精馏塔的工艺计算，用 Aspen Plus 建了模型，塔板数 22 块，回流比 1.8，做了灵敏度分析。",
 "为什么选 22 块板：我先用简捷法算了个初值，再用严格法校核，考虑到板效率取 0.7，实际需要的理论板就是这个量级。",
 "有一次团队做化工设计大赛，时间只剩三天，我主动把物料衡算和热量衡算拆出来自己做，最后按时交了作品。",
 "我想先在化工工艺岗位上做三年，把生产现场的工艺问题摸熟，再往工艺设计方向转。",
 "好的，我明白了，就按你说的这个方向准备。",
 "嗯，那我回去再补充一下这方面的经历。",
]

def probe(t):
    m = re.findall(r"面试进度：(?:重练 · 第 )?(\d)/5", t)
    prog = m[-1] if m else ("重练" if "重练 · 第" in t else "-")
    kind = "-"
    for k in ["自我介绍", "专业能力", "项目", "行为面试", "岗位理解", "职业规划"]:
        if k in t: kind = k; break
    return prog, kind, ("复盘" if ("🎯 模拟面试复盘" in t) else "出题")

cid = ""
for i, q in enumerate(QS, 1):
    t, cid = ask(q, cid)
    p, k, s = probe(t)
    print("第%d轮  进度=%-4s 题型=%-6s 状态=%-3s 长度=%d" % (i, p, k, s, len(t)))
    if s == "复盘":
        print("  -> 复盘出现在第 %d 轮（用户第 %d 次作答后）" % (i, i))
        break
    time.sleep(1)
