# -*- coding: utf-8 -*-
"""重练闭环隔离测试：开面 -> 答满 5 题 -> 出复盘 -> 重练第 3 题 -> 重答。
判定：重答后必须重新出完整复盘（含四维表现 / 综合算式）。
用法：python probe_retry.py <站点码>"""
import json, os, ssl, sys, time, urllib.request
BASE = "https://aiagent.cqut.edu.cn:31134"
SITE = sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "readysite.txt"), encoding="utf-8").read().strip()
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
_resp = urllib.request.urlopen(urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE}), context=CTX, timeout=30)
TOK = json.loads(_resp.read().decode())["access_token"]
H = {"Authorization": "Bearer " + TOK, "X-App-Code": SITE, "Content-Type": "application/json"}

def ask(q, cid=None):
    body = {"inputs": {}, "query": q, "response_mode": "streaming", "user": "probe-retry"}
    if cid: body["conversation_id"] = cid
    r = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(body).encode(), headers=H, method="POST")
    txt = ""; cid2 = cid
    with urllib.request.urlopen(r, context=CTX, timeout=300) as resp:
        for raw in resp:
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"): continue
            try: e = json.loads(line[5:].strip())
            except Exception: continue
            if e.get("event") == "message": txt += e.get("answer") or ""
            elif e.get("event") == "message_end": cid2 = e.get("conversation_id") or cid2
    return txt, cid2

def rep(t):
    return ("四维表现" in t) or ("本次得分" in t) or ("综合算式" in t)

SEQ = [
 ("开面", "来一场模拟面试，目标岗位是化工工艺工程师"),
 ("答1", "老师好，我是化学工程与工艺专业大四，做过精馏塔课程设计，用 Aspen Plus 建模，塔板 22 块、回流比 1.8。"),
 ("答2", "我负责全流程搭建，模拟不收敛时先查初值再换收敛方法，最后物料平衡误差压到 1% 以内。"),
 ("答3", "有一次化工设计大赛只剩三天，我主动把物料衡算和热量衡算拆出来自己做，最后按时交了作品。"),
 ("答4", "和同学对合成压力有分歧时，我提议做对照实验，用数据说话，最后按能耗最低的方案走。"),
 ("答5", "我想先在化工工艺岗做三年把现场摸熟，再往工艺设计方向转。"),
]
print("=== 阶段 1：开面并答满 5 题 ===")
cid = None
for tag, q in SEQ:
    t, cid = ask(q, cid)
    print("  %-4s 复盘=%s 长度=%d" % (tag, "是" if rep(t) else "否", len(t)))
    time.sleep(1)
print()
print("=== 阶段 2：重练第 3 题 ===")
t, cid = ask("重练第 3 题", cid)
print("  长度=%d 含重练=%s 含复盘=%s" % (len(t), "重练" in t, rep(t)))
print("  ", t[:300].replace(chr(10), " / "))
print()
print("=== 阶段 3：重答 -> 必须重出完整复盘 ===")
t, cid = ask("我当时对比过 18 块板和 22 块板两套方案，最后按能耗最低选了 22 块，能耗差大概 8%。", cid)
print("  长度=%d 含四维=%s 含算式=%s" % (len(t), "四维表现" in t, "综合算式" in t))
print("  判定：", "OK 立刻重出复盘" if rep(t) else "FAIL 未重出复盘")
print(t[:1200])