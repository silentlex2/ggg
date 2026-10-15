#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v9 验证：覆盖度统计 / 待确认档 / 岗位原文逐字摘录 / 面试官追问预演 / 政策分档。
用法：python probe_v8.py <站点码>
"""
import json, os, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
RESUME = os.path.join(os.path.dirname(HERE), "参赛方案", "素材", "演示简历样本-化工工艺工程师.md")

SITE = sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()


def token(site):
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": site})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


TOK = token(SITE)
H = {"Content-Type": "application/json", "X-App-Code": SITE,
     "Authorization": "Bearer " + TOK, "auth-token": "Bearer " + TOK}


def upload(path):
    b = "----zhiyinprobev8aa"
    data = open(path, "rb").read()
    parts = [("--" + b + "\r\n").encode(),
             ('Content-Disposition: form-data; name="file"; filename="resume_probe.md"\r\n').encode(),
             b"Content-Type: text/markdown\r\n\r\n", data,
             ("\r\n--" + b + "--\r\n").encode()]
    req = urllib.request.Request(BASE + "/api/files/upload", data=b"".join(parts), method="POST",
        headers={"Content-Type": "multipart/form-data; boundary=" + b,
                 "X-App-Code": SITE, "Authorization": "Bearer " + TOK, "auth-token": "Bearer " + TOK})
    with urllib.request.urlopen(req, context=CTX, timeout=90) as r:
        return json.loads(r.read().decode())


def ask(q, extra=None, conv=""):
    payload = {"response_mode": "streaming", "conversation_id": conv, "query": q,
               "inputs": dict({"user_input": q}, **(extra or {})), "parent_message_id": None}
    req = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(payload).encode(),
                                 headers=H, method="POST")
    t0 = time.time(); ans = ""; cid = conv; failed = []
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        for raw in r:
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"): continue
            try: e = json.loads(line[5:].strip())
            except Exception: continue
            ev = e.get("event")
            if ev == "message": ans += e.get("answer") or ""
            elif ev == "message_end": cid = e.get("conversation_id") or cid
            elif ev == "node_finished" and (e.get("data") or {}).get("status") == "failed":
                failed.append((e.get("data") or {}).get("title"))
    return ans, cid, time.time() - t0, failed


print("=== E1 简历诊断：要求—证据矩阵 + 隐私遮罩 ===")
up = upload(RESUME)
fid = up.get("id")
a, _, cost, failed = ask("帮我诊断这份简历，目标岗位是化工工艺工程师",
    {"user_file": {"type": "document", "transfer_method": "local_file", "upload_file_id": fid}})
print("  耗时 %.1fs 失败节点=%s 长度=%d" % (cost, failed or "无", len(a)))
checks = [
    ("矩阵表头", "岗位原文" in a and "简历里的证据" in a),
    ("判定符号", sum(1 for s in ["✅", "🟡", "🟠", "🔴", "⚪"] if s in a) >= 3),
    ("覆盖度统计行", "覆盖度：" in a),
    # 硬门槛结论有两种合法形态：全部满足 -> 「硬性条件已满足」；有缺口 -> 「硬性条件未全部满足」
    ("硬门槛结论", ("硬性条件" in a) and (("已满足" in a) or ("未全部满足" in a))),
    ("隐私遮罩", "13800000000" not in a),
    ("优先改缺口", "表达缺口" in a or "证据不足" in a),
]
for k, v in checks: print("   %-12s %s" % (k, "OK" if v else "FAIL"))
open(os.path.join(HERE, "scratch", "_v8_resume.txt"), "w", encoding="utf-8").write(a)
print("---- 前 1800 字 ----")
print(a[:1800])

print()
print("=== E2 岗位匹配：不许常识补齐 ===")
a2, _, cost, failed = ask("我是化学工程与工艺专业大四，想找重庆的化工类校招岗位")
print("  耗时 %.1fs 长度=%d" % (cost, len(a2)))
print("   未假定 Aspen:", "OK" if ("如果会用" in a2 or "没提到" in a2 or "Aspen" not in a2) else "CHECK")
print(a2[:1100])

print()
print("=== E3 政策：引用溯源 ===")
a3, _, cost, failed = ask("重庆高校毕业生有哪些就业补贴？")
print("  耗时 %.1fs 长度=%d" % (cost, len(a3)))
print("   无出处话术出现:", "有(需查)" if ("根据相关政策" in a3 or "相关规定" in a3) else "无 OK")
print(a3[:900])
