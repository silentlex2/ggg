# -*- coding: utf-8 -*-
"""v6 评分口径回归：① 简历诊断连测 3 次看总分与分项是否每次都一致
② 面试走到复盘，看四维与本次得分是否一致
用法：python probe_v6.py <站点码>
"""
import json, os, re, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "g2XDtP2IvbgTKh8k"
RESUME = os.path.join(os.path.dirname(HERE), "参赛方案", "素材", "演示简历样本-化工工艺工程师.md")


def token():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def upload(tok, path):
    boundary = "----zhiyinprobe6a21"
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

# ---------- ① 简历诊断连测 3 次 ----------
fid = upload(tok, RESUME)["id"]
print("\n" + "=" * 76); print("① 评分可核对：连测 3 次"); print("=" * 76)
for i in range(1, 4):
    ans, _, fail, cost = chat(tok, "帮我诊断简历，目标岗位是化工工艺工程师", file_id=fid)
    dims = {}
    for name in ["项目经历", "技能匹配", "表达规范", "排版格式"]:
        m = re.search(name + r"\s*[█░]*\s*(\d+)", ans)
        dims[name] = int(m.group(1)) if m else None
    m = re.search(r"综合匹配度\s*[█░]*\s*(\d+)", ans)
    comp = int(m.group(1)) if m else None
    # 总分是否出现在分项之前
    pos_dim = ans.find("【分项得分】")
    pos_comp = ans.find("综合匹配度")
    early = pos_comp != -1 and pos_dim != -1 and pos_comp < pos_dim
    line = ""
    if comp and all(v is not None for v in dims.values()):
        calc = dims["技能匹配"]*0.4 + dims["项目经历"]*0.3 + dims["表达规范"]*0.2 + dims["排版格式"]*0.1
        line = "算得 %.1f -> %s" % (calc, "✅" if abs(round(calc)-comp) <= 0 else "❌")
    print("  第%d次 %.1fs | 分项 %s | 报告 %s | %s | 总分提前出现=%s | 失败=%s"
          % (i, cost, dims, comp, line, early, fail or "无"))

# ---------- ② 面试走到复盘 ----------
turns = ["我想面化工工艺工程师，开始吧",
         "我是重庆理工大学化学工程与工艺专业大四，做过精馏塔课程设计，担任组长，塔板数22块，回流比1.8，用Aspen Plus做的，选筛板塔因为浮阀塔造价高。",
         "物性方法选的NRTL，因为体系是极性非理想体系；进料位置第12块；塔顶纯度99.5%；中途不收敛我改了收敛方法和迭代次数。",
         "当时组里对回流比取值有分歧，我用Aspen做了两组灵敏度分析，把数据摆出来，最后大家同意按能耗更低的方案走，结果设计说明书的能耗章节由我重写。",
         "我最大的短板是没做过中试放大，只有课程设计规模。",
         "好的，复盘一下。"]
print("\n" + "=" * 76); print("② 面试复盘：四维与本次得分是否一致"); print("=" * 76)
cid = ""
final = ""
for i, q in enumerate(turns, 1):
    ans, cid, fail, cost = chat(tok, q, cid)
    final = ans
    print("  ----- 第 %d 轮 %.1fs 失败=%s" % (i, cost, fail or "无"))
    if "本次得分" in ans or "[四维表现]" in ans or "综合算式" in ans:
        print(ans[-2000:])
        break
dims = {}
for name in ["逻辑", "专业", "表达", "态度"]:
    m = re.search(name + r"[性能与度]*\s*[█░:：]*\s*(\d+)", final)
    dims[name] = int(m.group(1)) if m else None
m = re.search(r"本次得分\s*[█░]*\s*(\d+)", final)
sc = int(m.group(1)) if m else None
print("\n四维:", dims, "| 本次得分:", sc)
if sc and dims.get("逻辑") and dims.get("专业"):
    calc = dims["逻辑"]*0.35 + dims["专业"]*0.35 + (dims.get("表达") or 0)*0.2 + (dims.get("态度") or 0)*0.1
    print("按 35/35/20/10 算 = %.1f -> %s" % (calc, "✅" if abs(round(calc)-sc) <= 1 else "❌"))
print("出现综合算式:", "综合算式" in final)
