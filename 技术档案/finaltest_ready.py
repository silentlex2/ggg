#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, ssl, re, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
SITE = "j5qWmoi0m0UYWDpj"  # 2026-10-14 v7 正式站（v6b：技能证据纪律 / 时效说明 / 专业兜底 / 来源冲突裁决）
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
    TOK = json.loads(r.read().decode())["access_token"]

IV, CH, POL, JOB = '1791600000050', '1791600000001', '1791600000060', '1791600000030'


def run(q, convo=""):
    for a in range(4):
        body = json.dumps({"response_mode": "streaming", "conversation_id": convo, "query": q,
                           "inputs": {"user_input": q}, "parent_message_id": None}).encode()
        req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
            headers={"Content-Type": "application/json", "authorization": "Bearer " + TOK, "auth-token": "Bearer " + TOK})
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=240) as r:
                raw = r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(4); continue
        raw = raw.replace("\r\n", "\n")
        ans, nodes, cid = "", [], ""
        for blk in raw.split("\n\n"):
            if not blk.startswith("data:"): continue
            try: j = json.loads(blk[5:].strip())
            except Exception: continue
            d = j.get("data") or {}
            if d.get("conversation_id"): cid = d["conversation_id"]
            if j.get("event") == "message": ans += j.get("answer", "")
            if j.get("event") == "node_finished": nodes.append(d.get("node_id", "?"))
        if len(ans) >= 15 or a == 3: return ans, nodes, cid
        time.sleep(4)
    return ans, nodes, cid


def branch(nodes):
    if IV in nodes: return "面试"
    if POL in nodes: return "政策"
    if JOB in nodes: return "岗位"
    if CH in nodes: return "闲聊"
    return "简历/其他"


def prog(ans):
    m = re.search(r"面试进度：(\d)\s*/\s*5", ans)
    return m.group(1) if m else "-"


CASES = [
    ("场景1 面试全流程+换话题+续答", [
        "来一场模拟面试吧，我找重庆的机械设计工程师岗位",
        "嗯，我知道",
        "先不面了，三方协议违约了怎么办？",
        "那继续面试吧，下一题是什么",
        "各位面试官好，我是重庆理工大学机械设计制造及其自动化专业2026届本科生，GPA3.4，做过二级减速器课程设计和智能搬运小车结构设计，熟练使用SolidWorks和AutoCAD，希望应聘机械设计工程师岗位。",
        "设计齿轮时我按传动比分配齿数，模数按齿根弯曲强度初选再校核接触强度，轴径按弯扭合成强度算。",
        "我做过最有成就感的事是智能搬运小车，我负责结构件和装配，最后负载3kg稳定循迹。",
        "我期望薪资8k到10k，能接受加班和出差。",
        "我认为机械设计工程师的核心是把需求变成可制造的图纸，我愿意从画图做起。",
    ]),
    ("场景2 无面试时不要说面试话", [
        "重庆应届生有哪些补贴政策？",
        "然后呢",
        "档案和报到证有什么区别？",
    ]),
    ("场景3 岗位匹配与闲聊", [
        "我是机械设计制造及其自动化专业大四，会SolidWorks，想找重庆的校招岗位",
        "谢谢啦",
    ]),
]

fails = []
for title, turns in CASES:
    print("=" * 78)
    print(title)
    convo = ""
    for i, q in enumerate(turns):
        ans, nodes, cid = run(q, convo)
        if cid: convo = cid
        gs = "1791544053269" not in nodes
        print("  T%d %-28s -> %-6s 守卫短路=%-5s 进度=%s" % (i + 1, q[:28], branch(nodes), gs, prog(ans)))
        print("       %s" % ans[:120].replace("\n", " "))
        time.sleep(1)

print("=" * 78)
print("关键判定：场景1 的 T2「嗯，我知道」必须进面试分支且守卫短路")
PYEOF_MARK = None
