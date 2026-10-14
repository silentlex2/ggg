# -*- coding: utf-8 -*-
"""面试闭环实测（带错误捕获）：走完 5 题+复盘，然后测「重练某一题」。
用法：python probe_interview2.py <站点码>
"""
import json, ssl, sys, time, urllib.request, urllib.error
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "j5qWmoi0m0UYWDpj"
req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
    TOK = json.loads(r.read().decode())["access_token"]

def ask(q, cid=""):
    body = json.dumps({"response_mode": "streaming", "conversation_id": cid, "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    r = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + TOK, "auth-token": "Bearer " + TOK})
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=400) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return "[HTTP %d] %s" % (e.code, e.read().decode("utf-8", "replace")[:300]), cid
    ans, cid2, err = "", cid, None
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"): continue
        try: j = json.loads(blk[5:].strip())
        except Exception: continue
        e = j.get("event"); d = j.get("data") or {}
        if e == "message": ans += j.get("answer", "")
        elif e == "message_end": cid2 = j.get("conversation_id") or cid
        elif e == "error": err = j.get("message") or j
        elif e == "workflow_finished" and d.get("status") == "failed": err = d.get("error")
    if not ans and err: ans = "[工作流失败] %s" % json.dumps(err, ensure_ascii=False)[:400]
    return ans, cid2

TURNS = [
 "我想练一下化工工艺工程师的面试",
 "我叫小李，重庆理工大学化学工程与工艺专业大四，做过一个精馏塔的课程设计，想在重庆找化工工艺岗。",
 "我做的课程设计是分离苯和甲苯，塔板数 22 块，回流比 1.8，用 Aspen Plus 做的模拟，最后塔顶纯度做到 99.2%。",
 "我负责的是整个流程的搭建和参数调试，遇到的问题是模拟不收敛，我把收敛方法从 Wegstein 换成 Newton 就好了。",
 "有一次小组做实验，我和同学对取样方案有分歧，我提议先做一组对照实验，最后用数据说服了他。",
 "我觉得化工工艺岗最重要的是把工艺参数吃透，能现场解决问题。未来三年我想先做两三年工艺工程师，再往工艺设计方向走。",
]
cid = ""
for i, q in enumerate(TURNS, 1):
    t0 = time.time()
    ans, cid = ask(q, cid)
    print("=" * 74)
    print("第 %d 轮  %.1fs  用户: %s" % (i, time.time() - t0, q[:36]))
    print("=" * 74)
    print(ans[:1400])
    print()
    if ans.startswith("[HTTP") or ans.startswith("[工作流失败]"): break

print("#" * 74)
print("# 复盘之后：重练某一题")
print("#" * 74)
a, cid = ask("我想重练一下第 3 题", cid)
print(a[:2200])
