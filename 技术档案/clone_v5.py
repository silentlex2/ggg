# -*- coding: utf-8 -*-
"""把 v5 提示词推上线：
   站点钉死在复制时刻的版本 -> 只能复制应用、换站点码。
   本脚本：探站点端点 -> 复制 -> 修图标/名字 -> 发布 -> 打印新站点码。
"""
import json, os, ssl, sys, urllib.request, urllib.error

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "38c3e937-b888-4564-bb2e-39f2520e28f3"
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

def tok():
    return open(os.path.join(HERE, "scratch", ".token"), encoding="utf-8").read().strip()

def api(path, method="GET", body=None, ok=(200, 201)):
    t = tok()
    h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8"); h["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=180) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode("utf-8"))
        except Exception: return e.code, None

print("== 0. 先探一圈站点端点（找有没有能不换站点码就重新绑定的路）==")
for p, m in [("/console/api/apps/%s/site" % SRC, "GET"),
             ("/console/api/apps/%s/site" % SRC, "PUT"),
             ("/console/api/apps/%s/site" % SRC, "POST"),
             ("/console/api/apps/%s/site/publish" % SRC, "POST"),
             ("/console/api/apps/%s/workflows/publish" % SRC, "POST")]:
    if p.endswith("workflows/publish"): continue
    s, j = api(p, m, {} if m != "GET" else None)
    print("  %-6s %-52s -> %s %s" % (m, p.replace(SRC, "{id}"), s, str(j)[:70]))

print()
print("== 1. 复制源应用（复制后站点即钉在此刻的版本）==")
s, j = api("/console/api/apps/%s/copy" % SRC, "POST", {"name": "职引 · 校园就业智能体", "icon_type": None, "icon": None,
                                                       "icon_background": None, "mode": "advanced-chat"})
if s not in (200, 201):
    print("  复制失败:", s, str(j)[:200]); sys.exit(1)
NEW = j["id"]
print("  新应用 =", NEW)

print()
print("== 2. 修正名字 / 图标 / 简介 ==")
s, j = api("/console/api/apps/%s" % NEW, "PUT", {
    "name": "职引 · 校园就业智能体",
    "description": "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询，重庆理工大学",
    "icon_type": "image", "icon": ICON, "icon_background": ""})
print("  PUT ->", s, (j or {}).get("name"), (j or {}).get("icon_type"))

print()
print("== 3. 确认草稿里带 v5 提示词 + 发布 ==")
s, d = api("/console/api/apps/%s/workflows/draft" % NEW)
txt = " ".join(p.get("text", "") for n in d["graph"]["nodes"] for p in n.get("data", {}).get("prompt_template", []))
for k in ["第 2 步：按 技能匹配×40%", "综合算式：技能匹配", "劝退分支", "出题前先定契约",
          "严禁补充资料里没有出现过的限制条件", "措辞纪律", "风险点复核",
          "综合算式：逻辑性", "用原文里的原词", "可照抄的话术"]:
    print("   %-28s %s" % (k, "✅" if k in txt else "❌"))
s, pub = api("/console/api/apps/%s/workflows/publish" % NEW, "POST", {"marked_name": "", "marked_comment": "v5 提示词：评分可核对 / 劝退分支 / 先定契约 / 不脑补条件 / 措辞纪律 / 风险复核"})
print("  publish ->", s, (pub or {}).get("id"))

print()
print("== 4. 结果 ==")
s, a = api("/console/api/apps/%s" % NEW)
print("  app_id   =", NEW)
print("  name     =", a.get("name"))
print("  enable_site =", a.get("enable_site"))
print("  site_code=", (a.get("site") or {}).get("code"))
print("  workflow =", (a.get("workflow") or {}).get("id"))
print("  URL      = https://aiagent.cqut.edu.cn:31134/chat/%s" % (a.get("site") or {}).get("code"))
