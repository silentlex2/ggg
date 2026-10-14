# -*- coding: utf-8 -*-
"""把带 v6a（总分挪到分项之后）的草稿复制成新正式站。
用法：python clone_v6.py
"""
import json, os, ssl, urllib.request, urllib.error
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
SRC  = "38c3e937-b888-4564-bb2e-39f2520e28f3"     # 草稿已带 v6a
OLD  = "dbb919fc-23a6-4eb6-8575-676fed9d1207"     # 当前正式站(v5f)，改名为回退

def tok(): return open(os.path.join(HERE, "scratch", ".token"), encoding="utf-8").read().strip()
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

print("== 0. 确认源草稿带 v6a ==")
s, d = api("/console/api/apps/%s/workflows/draft" % SRC)
txt = " ".join(p.get("text","") for n in d["graph"]["nodes"] for p in n.get("data",{}).get("prompt_template",[]))
chek = [
    ("总分不在首行", "综合匹配度  <进度条>  <分数> / 100" not in txt),
    ("总分挪到算式后", "综合匹配度  <进度条>  <把上面的加权和四舍五入取整> / 100" in txt),
    ("不许提前写分", "一个字都不许提前写在别处" in txt),
    ("面试分挪到四维后", "本次得分  <把上面的加权和四舍五入取整> / 100" in txt),
    ("旧首行模板已删", "本次得分 <加权分>/100" not in txt),
    ("v5f 交卷自检已替换", "整份报告写完后，回到第一行那个「综合匹配度」检查一次" not in txt),
]
for k, v in chek: print("   %-22s %s" % (k, "OK" if v else "FAIL"))

print()
print("== 1. 复制成新正式站 ==")
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
             {"marked_name": "", "marked_comment": "v6a 评分口径"})
print("  publish ->", s)

print()
print("== 2. 旧正式站改名 ==")
s, j = api("/console/api/apps/%s" % OLD, "PUT", {
    "name": "职引 · 校园就业智能体（回退 · v5）",
    "description": "回退用：v5 全套提示词（含劝退分支/先定契约），评分口径为 v5f"})
print("  ->", s, (j or {}).get("name"))

print()
print("== 3. 最终清单 ==")
s, a = api("/console/api/apps/%s" % NEW)
CODE = (a.get("site") or {}).get("code")
print("  NEW_APP =", NEW)
print("  SITE    =", CODE)
print("  WF      =", (a.get("workflow") or {}).get("id"))
print("  URL     = https://aiagent.cqut.edu.cn:31134/chat/%s" % CODE)
