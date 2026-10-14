# -*- coding: utf-8 -*-
"""v7d 验证：面试收尾硬规则 / 重练分支不打折 / 政策拒答给路径。用法：python probe_v7d.py <站点码>"""
import json, os, ssl, sys, time, urllib.request, urllib.error, re
BASE = "https://aiagent.cqut.edu.cn:31134"
SITE = sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "readysite.txt"), encoding="utf-8").read().strip()
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

def http(p, m="GET", b=None, h=None):
    h = dict(h or {}); data = None
    if b is not None:
        data = json.dumps(b).encode(); h["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + p, data=data, headers=h, method=m)
    with urllib.request.urlopen(r, context=CTX, timeout=180) as resp:
        return resp.status, resp.read().decode()

_, j = http("/api/passport", h={"X-App-Code": SITE})
TOK = json.loads(j)["access_token"]
H = {"Authorization": "Bearer " + TOK, "X-App-Code": SITE, "Content-Type": "application/json"}

def ask(q, cid=None):
    body = {"inputs": {}, "query": q, "response_mode": "streaming", "user": "probe-v7d"}
    if cid: body["conversation_id"] = cid
    r = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(body).encode(), headers=H, method="POST")
    txt = ""; cid2 = None; nodes = []; wf = None
    with urllib.request.urlopen(r, context=CTX, timeout=300) as resp:
        for raw in resp:
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"): continue
            try: e = json.loads(line[5:].strip())
            except Exception: continue
            ev = e.get("event")
            if ev == "message": txt += e.get("answer") or ""
            elif ev == "node_finished": nodes.append(e.get("data", {}).get("title"))
            elif ev == "workflow_finished": wf = (e.get("data") or {}).get("workflow_id")
            elif ev == "message_end": cid2 = e.get("conversation_id") or cid2
    return txt, cid2, nodes, wf

def prog(t):
    m = re.findall(r"(\d)/5", t)
    return m[-1] if m else "?"

ANSWERS = [
 "老师好，我是化学工程与工艺专业大四学生，做过一个精馏塔课程设计，用 Aspen Plus 模拟，也参加过化工设计大赛。",
 "我在课程设计里负责精馏塔的工艺计算，用 Aspen Plus 建了模型，塔板数 22 块，回流比 1.8，做了灵敏度分析。",
 "为什么选 22 块板：我先用简捷法算了个初值，再用严格法校核，考虑到板效率取 0.7，实际需要的理论板就是这个量级。",
 "有一次团队做化工设计大赛，时间只剩三天，我主动把物料衡算和热量衡算拆出来自己做，最后按时交了作品。",
 "我想先在化工工艺岗位上做三年，把生产现场的工艺问题摸熟，再往工艺设计方向转。",
]

print("=== D1 面试五题收尾（第 6 轮必须出复盘）===")
cid = None; last = None
for i, a in enumerate(ANSWERS):
    t, cid, nodes, wf = ask(a, cid)
    last = t
    print("  第%d轮 进度=%s 长度=%d" % (i + 1, prog(t), len(t)))
    time.sleep(1)
has_report = ("四维表现" in last) or ("本次得分" in last) or ("综合算式" in last)
print("  收尾复盘 =", "OK" if has_report else "FAIL", "| 复盘长度", len(last))
print("---- 末轮输出 ----")
print(last[:1600])
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratch", "_v7d_report.txt"), "w", encoding="utf-8").write(last)

print()
print("=== D2 重练第 3 题（不许打折）===")
t, cid, nodes, wf = ask("重练第 3 题", cid)
print("  长度=%d | 含「重练」=%s | 含打折话术=%s" % (len(t), "重练" in t, ("题号只能往前走" in t) or ("换个角度再压一遍" in t) or ("我接着往下走" in t)))
print(t[:1200])

print()
print("=== D3 重练后作答 → 必须重出复盘 ===")
t, cid, nodes, wf = ask("我当时其实对比过 18 块板和 22 块板两套方案，最后按能耗最低选的 22 块，能耗差了大概 8%。", cid)
print("  长度=%d | 含复盘=%s | 含算式=%s" % (len(t), ("四维表现" in t) or ("本次得分" in t), "综合算式" in t))
print(t[:1400])

print()
print("=== D4 政策拒答给路径 ===")
for q in ["试用期最长多久", "就业报到证还需要办吗"]:
    t, c2, nodes, wf = ask(q)
    print("  Q: %s -> 长度=%d | 含边界=%s | 含12333=%s | 含就业指导中心=%s" % (
        q, len(t), ("没有覆盖" in t) or ("没找到" in t) or ("没有找到" in t), "12333" in t, "就业指导中心" in t))
    print("   ", t[:700].replace("\n", " / "))
    print()
