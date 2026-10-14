# -*- coding: utf-8 -*-
"""多轮闭环实测：① 岗位匹配编号下钻 ② 条件收窄 ③ 面试复盘后重练某一题
用法：python probe_multiturn2.py <站点码>
"""
import json, ssl, sys, time, urllib.request
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
    with urllib.request.urlopen(r, context=CTX, timeout=400) as resp:
        raw = resp.read().decode("utf-8", "replace")
    ans, cid2, chain = "", cid, []
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"): continue
        try: j = json.loads(blk[5:].strip())
        except Exception: continue
        e = j.get("event")
        if e == "message": ans += j.get("answer", "")
        elif e == "message_end": cid2 = j.get("conversation_id") or cid
        elif e == "node_finished": chain.append((j.get("data") or {}).get("title"))
    return ans, cid2, chain

print("#" * 78)
print("# 场景一：岗位匹配 → 编号下钻")
print("#" * 78)
a1, cid, ch1 = ask("我是化学工程与工艺专业大四，想找重庆的校招岗位")
print("\n--- 第 1 轮（%s）---" % " → ".join(ch1))
print(a1[:1400])
a2, cid, ch2 = ask("第 2 个岗位能详细说说吗，我该怎么准备", cid)
print("\n--- 第 2 轮 · 下钻（%s）---" % " → ".join(ch2))
print(a2[:1800])

print()
print("#" * 78)
print("# 场景二：岗位匹配 → 条件收窄")
print("#" * 78)
a3, cid2, ch3 = ask("我想找机械设计制造及其自动化相关的岗位")
print("\n--- 第 1 轮（%s）---" % " → ".join(ch3))
print(a3[:900])
a4, cid2, ch4 = ask("我不想去外地，只想留在重庆主城", cid2)
print("\n--- 第 2 轮 · 收窄（%s）---" % " → ".join(ch4))
print(a4[:1800])
