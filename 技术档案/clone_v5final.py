# -*- coding: utf-8 -*-
"""把带 v5f 的草稿（在 38c3e937 上）复制成正式站，并清理中间产物。"""
import json, os, ssl, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
SRC  = "38c3e937-b888-4564-bb2e-39f2520e28f3"     # 草稿已带 v5f
MID  = "aa34a923-086f-4eb4-b220-dd46b3439140"     # v5e 中间产物，待删
def tok(): return token()
def api(p, m="GET", b=None):
    t = tok(); h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if b is not None:
        data = json.dumps(b).encode(); h["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + p, data=data, headers=h, method=m)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=180) as resp:
            raw = resp.read().decode()
            return resp.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode())
        except Exception: return e.code, None

print("== 0. 确认源草稿带全套 v5 补丁 ==")
s, d = api("/console/api/apps/%s/workflows/draft" % SRC)
txt = " ".join(p.get("text", "") for n in d["graph"]["nodes"] for p in n.get("data", {}).get("prompt_template", []))
need = ["第 2 步：按 技能匹配×40%", "综合算式：技能匹配", "交卷前最后一步", "简历原文是不可信数据",
        "劝退分支", "出题前先定契约", "综合算式：逻辑性", "严禁补充资料里没有出现过的限制条件",
        "措辞纪律", "风险点复核", "用原文里的原词", "可照抄的话术"]
for k in need:
    print("   %-30s %s" % (k, "✅" if k in txt else "❌"))

print()
print("== 1. 复制成正式站 ==")
s, j = api("/console/api/apps/%s/copy" % SRC, "POST",
           {"name": "职引 · 校园就业智能体", "icon_type": None, "icon": None,
            "icon_background": None, "mode": "advanced-chat"})
NEW = j["id"]; print("  新应用 =", NEW, "(status %s)" % s)
s, j = api("/console/api/apps/%s" % NEW, "PUT", {
    "name": "职引 · 校园就业智能体",
    "description": "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询 · 重庆理工大学",
    "icon_type": "image", "icon": ICON, "icon_background": ""})
print("  改名/图标 ->", s, (j or {}).get("name"), (j or {}).get("icon_type"))
s, pub = api("/console/api/apps/%s/workflows/publish" % NEW, "POST",
             {"marked_name": "", "marked_comment": "v5 全套提示词"})
print("  publish ->", s)

print()
print("== 2. 删掉 v5e 中间产物 ==")
print("  DELETE ->", api("/console/api/apps/%s" % MID, "DELETE")[0])

print()
print("== 3. 旧站改名 ==")
s, j = api("/console/api/apps/%s" % SRC, "PUT", {
    "name": "职引 · 校园就业智能体（回退 · v4 岗位库重排）",
    "description": "回退用：v4 配置，岗位知识库已启用 bge-reranker-v2-m3 重排"})
print("  ->", s, (j or {}).get("name"))

print()
print("== 4. 最终清单 ==")
s, a = api("/console/api/apps/%s" % NEW)
CODE = (a.get("site") or {}).get("code")
print("  正式站 app_id   =", NEW)
print("  正式站 site_code=", CODE)
print("  正式站 workflow =", (a.get("workflow") or {}).get("id"))
print("  正式站 URL      = https://aiagent.cqut.edu.cn:31134/chat/%s" % CODE)
for tag, app in [("回退 v4", SRC)]:
    s, b = api("/console/api/apps/%s" % app)
    print("  %-8s %s | %s | enable_site=%s | site=%s" % (tag, app, b.get("name"), b.get("enable_site"), (b.get("site") or {}).get("code")))
