# -*- coding: utf-8 -*-
"""面试复盘评分口径回归：走完一场面试，看四维与本次得分是否一致。用法：python probe_v6i.py <站点码>"""
import json, os, re, ssl, sys, time, urllib.request
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "g2XDtP2IvbgTKh8k"

def token():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]

def chat(tok, q, cid=""):
    body = json.dumps({"response_mode": "streaming", "conversation_id": cid, "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    ans, cid2, failed = "", cid, []
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=400) as r:
        raw = r.read().decode("utf-8", "replace")
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"): continue
        try: j = json.loads(blk[5:].strip())
        except Exception: continue
        e = j.get("event")
        if e == "message": ans += j.get("answer", "")
        elif e == "message_end": cid2 = j.get("conversation_id") or cid
        elif e == "node_finished":
            d = j.get("data") or {}
            if d.get("status") == "failed": failed.append(d.get("title"))
    return ans, cid2, failed, time.time() - t0

tok = token()
print("站点:", SITE, "| token OK")
turns = ["我想面化工工艺工程师，开始吧",
         "我是重庆理工大学化学工程与工艺专业大四，做过精馏塔课程设计，担任组长，塔板数22块，回流比1.8，用Aspen Plus做的，选筛板塔因为浮阀塔造价高。",
         "物性方法选的NRTL，因为体系是极性非理想体系；进料位置第12块；塔顶纯度99.5%；中途不收敛我改了收敛方法和迭代次数。",
         "当时组里对回流比取值有分歧，我用Aspen做了两组灵敏度分析，把数据摆出来，最后大家同意按能耗更低的方案走，结果设计说明书的能耗章节由我重写。",
         "我最大的短板是没做过中试放大，只有课程设计规模。",
         "好的，复盘一下。"]
cid, final = "", ""
for i, q in enumerate(turns, 1):
    ans, cid, fail, cost = chat(tok, q, cid)
    final = ans
    print("----- 第 %d 轮 %.1fs 失败=%s" % (i, cost, fail or "无"))
for line in final.splitlines():
    if any(k in line for k in ["本次得分", "综合算式", "四维", "逻辑", "专业度", "表达", "态度", "📏"]):
        print("   |", line.strip()[:160])
dims = {}
for name, pat in [("逻辑","逻辑[性能]?\s*[█░:：\s]*?(\d+)"),("专业","专业度?\s*[█░:：\s]*?(\d+)"),
                  ("表达","表达\s*[█░:：\s]*?(\d+)"),("态度","态度\s*[█░:：\s]*?(\d+)")]:
    m = re.search(pat, final)
    dims[name] = int(m.group(1)) if m else None
m = re.search(r"本次得分\s*[█░]*\s*(\d+)", final)
sc = int(m.group(1)) if m else None
print("\n四维:", dims, "| 本次得分:", sc)
if sc and all(dims.values()):
    calc = dims["逻辑"]*0.35 + dims["专业"]*0.35 + dims["表达"]*0.2 + dims["态度"]*0.1
    print("按 35/35/20/10 算 = %.1f -> %s" % (calc, "OK 一致" if abs(round(calc)-sc) <= 1 else "FAIL 不一致"))
print("出现综合算式:", "综合算式" in final)
