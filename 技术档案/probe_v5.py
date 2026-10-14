# -*- coding: utf-8 -*-
"""v5 四项新设计逐个实测：① 评分可核对 ② 劝退分支 ③ 先定契约 ④ 不脑补条件

用法：python probe_v5.py <站点码>
"""
import json, os, re, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "869gmx6QMfVwBOw7"
RESUME = os.path.join(os.path.dirname(HERE), "参赛方案", "素材", "演示简历样本-化工工艺工程师.md")


def token():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def upload(tok, path):
    boundary = "----zhiyinprobe8f21"
    data = open(path, "rb").read()
    body = b"".join([
        ("--" + boundary + "\r\n").encode(),
        ('Content-Disposition: form-data; name="file"; filename="resume_probe.md"\r\n').encode(),
        b"Content-Type: text/markdown\r\n\r\n", data,
        ("\r\n--" + boundary + "--\r\n").encode()])
    req = urllib.request.Request(
        BASE + "/api/files/upload", data=body, method="POST",
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary,
                 "X-App-Code": SITE, "Authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    with urllib.request.urlopen(req, context=CTX, timeout=90) as r:
        return json.loads(r.read().decode())


def chat(tok, q, cid="", file_id=None):
    inputs = {"user_input": q}
    if file_id:
        inputs["user_file"] = {"type": "document", "transfer_method": "local_file",
                               "upload_file_id": file_id, "filename": "resume_probe.md"}
    body = json.dumps({"response_mode": "streaming", "conversation_id": cid, "query": q,
                       "inputs": inputs, "parent_message_id": None}).encode()
    req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    ans, cid2, chain, failed = "", cid, [], []
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
            chain.append(d.get("title"))
            if d.get("status") == "failed": failed.append(d.get("title"))
    return ans, cid2, chain, failed, time.time() - t0


tok = token()
print("站点:", SITE, "| token OK")

# ---------- ① 评分可核对 ----------
ans, _, chain, fail, cost = chat(tok, "帮我诊断简历，目标岗位是化工工艺工程师", file_id=upload(tok, RESUME)["id"])
print("\n" + "=" * 76); print("① 评分可核对（带 PDF/md 文件简历诊断）  耗时 %.1fs" % cost); print("=" * 76)
print(ans[:1500])
dims = {}
for name in ["项目经历", "技能匹配", "表达规范", "排版格式"]:
    m = re.search(name + r"\s*[█░]*\s*(\d+)", ans)
    dims[name] = int(m.group(1)) if m else None
m = re.search(r"综合匹配度\s*[█░]*\s*(\d+)", ans)
comp = int(m.group(1)) if m else None
print("\n分项:", dims, "| 报告综合分:", comp)
if comp and all(v is not None for v in dims.values()):
    calc = dims["技能匹配"]*0.4 + dims["项目经历"]*0.3 + dims["表达规范"]*0.2 + dims["排版格式"]*0.1
    print("按 40/30/20/10 权重算 = %.1f -> %s" % (calc, "✅ 一致" if abs(round(calc)-comp) <= 1 else "❌ 不一致"))
print("出现「📏 评分口径」行:", "📏 评分口径" in ans)
print("失败节点:", fail or "无")

# ---------- ② 劝退分支 ----------
ans, _, chain, fail, cost = chat(tok, "我是汉语言文学专业大四，想找重庆的校招岗位")
print("\n" + "=" * 76); print("② 劝退分支（完全不对口专业）  耗时 %.1fs" % cost); print("=" * 76)
print(ans[:1200])
print("\n判定 -> 走劝退:", any(k in ans for k in ["先别投", "方向不对", "不建议", "缺什么"]))
print("失败节点:", fail or "无")

# ---------- ③ 先定契约 ----------
cid = ""
turns = ["我想面化工工艺工程师，开始吧",
         "我是重庆理工大学化学工程与工艺专业大四，做过精馏塔课程设计，担任组长，Aspen Plus 熟练。",
         "精馏塔设计我负责工艺计算，塔板数 22 块，回流比 1.8，选筛板塔因为浮阀塔造价高。",
         "我提升了效率，参与了项目，做了很多工作。"]
print("\n" + "=" * 76); print("③ 先定契约（4 轮面试，看第 4 轮怎么追问）"); print("=" * 76)
for i, q in enumerate(turns, 1):
    ans, cid, chain, fail, cost = chat(tok, q, cid)
    print("\n----- 第 %d 轮 [%s]  %.1fs  失败=%s" % (i, q[:30], cost, fail or "无"))
    print(ans[:560])
print("\n（完）")
