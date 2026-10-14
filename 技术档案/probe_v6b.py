# -*- coding: utf-8 -*-
"""v6b 四项新设计逐个实测：
① 技能证据纪律 —— 用户只报专业不报技能，看模型会不会替他推断技能
② 岗位库时效说明 —— 依据行末尾是否固定带「岗位库数据截至 2026-09」
③ 来源冲突裁决 —— 速查表与召回打架时是否只取一边，不揉数字
④ 简历专业兜底 —— user_major / user_skills 为空时是否仍给【专业适配度】并写明判断依据

用法：python probe_v6b.py <站点码>
"""
import json, os, re, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "j5qWmoi0m0UYWDpj"
RESUME = os.path.join(os.path.dirname(HERE), "参赛方案", "素材", "演示简历样本-化工工艺工程师.md")


def token():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def upload(tok, path):
    boundary = "----zhiyinprobe6b41"
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

# ---------- ①② 技能证据纪律 + 时效说明 ----------
Q1 = "我是重庆理工大学机械设计制造及其自动化专业大四，想找重庆的校招岗位"
ans, _, chain, fail, cost = chat(tok, Q1)
print("\n" + "=" * 76); print("①② 技能证据纪律 + 时效说明  耗时 %.1fs" % cost); print("=" * 76)
print(ans[:1600])

skill_words = ["CAD", "SolidWorks", "UG", "NX", "CATIA", "ProE", "Pro/E", "ANSYS", "MATLAB", "PLC", "数控"]
claimed = []
for w in skill_words:
    # 找「你会/你掌握/具备 + 技能」这类断言
    for m in re.finditer(r"[^。；\n]{0,24}" + re.escape(w) + r"[^。；\n]{0,24}", ans):
        seg = m.group(0)
        if re.search(r"(你会|你已(?:经)?掌握|你掌握|你具备|你的" + re.escape(w) + r"|掌握" + re.escape(w) + r"|熟悉" + re.escape(w) + r"|精通" + re.escape(w) + r")", seg):
            claimed.append(seg.strip())
print("\n→ 疑似把「专业」推断成「会某技能」的句子:", claimed or "无 ✅")
print("→ 依据行带时效说明:", ("岗位库数据截至 2026-09" in ans) and "✅" or "❌")
print("失败节点:", fail or "无")

# ---------- ③ 来源冲突裁决 ----------
Q3 = "我是重庆的应届毕业生，想问问一次性求职补贴和就业见习补贴分别能领多少钱"
ans3, _, chain3, fail3, cost3 = chat(tok, Q3)
print("\n" + "=" * 76); print("③ 来源冲突裁决  耗时 %.1fs" % cost3); print("=" * 76)
print(ans3[:1400])
print("\n→ 出现「以最新口径为准」:", ("以最新口径为准" in ans3) and "✅（说明确实走了冲突裁决）" or "—（本轮两来源无冲突，正常）")
print("→ 揉数字嫌疑:", ("约 1000" in ans3 or "左右" in ans3.replace("各地各校执行细则", "")) and "⚠️ 有" or "无 ✅")
print("失败节点:", fail3 or "无")

# ---------- ④ 简历专业兜底 ----------
ans4, _, chain4, fail4, cost4 = chat(tok, "帮我诊断简历，目标岗位是化工工艺工程师", file_id=upload(tok, RESUME)["id"])
print("\n" + "=" * 76); print("④ 简历专业兜底（user_major/user_skills 为空）  耗时 %.1fs" % cost4); print("=" * 76)
sec = re.search(r"【专业适配度】([\s\S]{0,400})", ans4)
print(sec.group(0) if sec else ans4[:1200])
print("\n→ 有【专业适配度】段:", bool(sec) and "✅" or "❌")
print("→ 写明按简历判断:", (("以简历中的教育背景判断" in ans4) or ("简历中的教育背景" in ans4)) and "✅" or "—")
print("失败节点:", fail4 or "无")
print("\n（完）")
