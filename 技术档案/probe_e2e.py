# -*- coding: utf-8 -*-
"""端到端闭环回归（v7a 用）：16 个用例，覆盖意图分类 / 岗位匹配 / 异常兜底 / 面试闭环。
用法：python probe_e2e.py <站点码>
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
        return "[HTTP %d] %s" % (e.code, e.read().decode("utf-8", "replace")[:200]), cid
    ans, cid2 = "", cid
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"): continue
        try: j = json.loads(blk[5:].strip())
        except Exception: continue
        if j.get("event") == "message": ans += j.get("answer", "")
        elif j.get("event") == "message_end": cid2 = j.get("conversation_id") or cid
    return ans, cid2

# ---- A 组：意图分类（每条独立会话）----
A = [
 ("帮我看看我的简历有什么问题", ["简历诊断", "简历", "上传"]),
 ("来一场模拟面试", ["第 1 题", "进度"]),
 ("帮我练练化工工艺工程师的面试", ["第 1 题", "进度"]),
 ("三方协议怎么签", ["三方", "协议", "依据"]),
 ("档案毕业后放哪", ["档案", "依据"]),
 ("试用期最长多久", ["试用期", "依据"]),
 ("你好", ["简历", "岗位", "面试", "政策"]),
 ("今天天气怎么样", ["不在", "范围", "简历", "岗位"]),
 ("简历写好了，能帮我投递吗", ["简历", "不能", "不提供", "投递"]),
]
print("#" * 78); print("# A 组 · 意图分类"); print("#" * 78)
pas = 0
for q, kws in A:
    a, _ = ask(q)
    hit = [k for k in kws if k in a]
    ok = "✅" if hit else "❌"
    if hit: pas += 1
    print("%s  %-26s → %s | %d 字 | %s" % (ok, q[:24], hit or "关键词都没命中", len(a), a[:60].replace("\n", " ")))
print("A 组通过 %d/%d" % (pas, len(A)))

# ---- B 组：岗位匹配与异常 ----
B = [
 ("重庆的实习岗位", ["实习", "重庆"]),
 ("我是学会计的，想找会计或者审计的岗位", ["会计", "审计"]),
 ("我想去火星工作", ["火星", "没有", "未命中", "不对口"]),
 ("有什么工作", ["岗位", "方向"]),
]
print(); print("#" * 78); print("# B 组 · 岗位匹配 / 无召回"); print("#" * 78)
pbs = 0
for q, kws in B:
    a, _ = ask(q)
    hit = [k for k in kws if k in a]
    ok = "✅" if hit else "❌"
    if hit: pbs += 1
    print("%s  %-30s → %s | %d 字" % (ok, q[:28], hit, len(a)))
print("B 组通过 %d/%d" % (pbs, len(B)))

# ---- C 组：异常兜底 ----
C = [
 ("   ", ["简历", "岗位", "面试", "政策"]),
 ("帮我诊断简历", ["上传", "简历"]),
]
print(); print("#" * 78); print("# C 组 · 异常兜底"); print("#" * 78)
pcs = 0
for q, kws in C:
    a, _ = ask(q)
    hit = [k for k in kws if k in a]
    ok = "✅" if hit else "❌"
    if hit: pcs += 1
    print("%s  %-16r → %s | %d 字" % (ok, q, hit, len(a)))

# ---- D 组：面试重练闭环 ----
print(); print("#" * 78); print("# D 组 · 面试闭环 + 重练"); print("#" * 78)
cid = ""
seq = ["来一场模拟面试",
       "我叫小李，化工专业，想面工艺岗",
       "我做过精馏塔课程设计，22 块塔板，回流比 1.8，纯度 99.2%",
       "我负责全流程搭建，模拟不收敛时换了收敛方法",
       "和同学有分歧时我提议做对照实验",
       "我想先做三年工艺工程师再转设计"]
for i, q in enumerate(seq, 1):
    a, cid = ask(q, cid)
    prog = [l for l in a.split("\n") if "面试进度" in l]
    print("  第%d轮 %-40s %s | %d 字" % (i, q[:38], prog[0].strip() if prog else "(无进度行)", len(a)))
    if i == 6:
        print("    复盘含'本次得分':", "✅" if "本次得分" in a else "❌",
              "| 算式在得分之前:", "✅" if ("综合算式" in a and a.index("综合算式") < a.index("本次得分")) else "❌")
print()
a, cid = ask("我想重练一下第 3 题", cid)
print("重练请求 →")
print(a[:1300])
