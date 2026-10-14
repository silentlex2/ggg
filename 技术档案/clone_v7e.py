# -*- coding: utf-8 -*-
"""把带 v7a/b/c/e（面试进度 max(M+1,C) + 重练只走一轮带硬锚点）的草稿复制成新正式站。
用法：python clone_v7.py
"""
import json, os, ssl, urllib.request, urllib.error
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
SRC  = "38c3e937-b888-4564-bb2e-39f2520e28f3"     # 草稿已带 v6b（wf d4ba2031）
OLD  = "765db33f-c425-4c7a-a0b1-d945f17af540"     # 当前正式站(v7d)，改名为回退

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

print("== 0. 确认源草稿带 v7a/b/c/e ==")
s, d = api("/console/api/apps/%s/workflows/draft" % SRC)
txt = " ".join(p.get("text","") for n in d["graph"]["nodes"] for p in n.get("data",{}).get("prompt_template",[]))
chek = [
    ("v6a 总分挪到算式后", "综合匹配度  <进度条>  <把上面的加权和四舍五入取整> / 100" in txt),
    ("v6a 不许提前写分", "一个字都不许提前写在别处" in txt),
    ("v6b 技能证据纪律", "技能证据纪律" in txt),
    ("v7a 重练分支", "重练分支" in txt),
    ("v7b 重练不打折", "绝对不要输出「题号只能往前走」" in txt),
    ("v7c 政策拒答给路径", "12333 人社服务热线" in txt),
    ("v7c 面试收尾硬规则", "已出现「第 5 题」标记" in txt),
    ("v7e 进度取max", "N = max(M ＋ 1, C)" in txt),
    ("v7e 重练只走一轮", "重练只走一轮" in txt),
    ("v6b 岗位库时效说明", "岗位库数据截至 2026-09" in txt),
    ("v6b 简历专业兜底", "公开站点上通常为空" in txt),
    ("v6b 来源冲突裁决", "两个来源打架时以召回内容为准" in txt),
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
             {"marked_name": "", "marked_comment": "v7a/b/c/e 面试进度与重练闭环"})
print("  publish ->", s)

print()
print("== 2. 旧正式站改名 ==")
s, j = api("/console/api/apps/%s" % OLD, "PUT", {
    "name": "职引 · 校园就业智能体（回退 · v7d）",
    "description": "回退用：v7d 版（v7a/b/c 重练分支 + 收尾硬规则 + 政策拒答给路径）"})
print("  ->", s, (j or {}).get("name"))

print()
print("== 3. 最终清单 ==")
s, a = api("/console/api/apps/%s" % NEW)
CODE = (a.get("site") or {}).get("code")
print("  NEW_APP =", NEW)
print("  SITE    =", CODE)
print("  WF      =", (a.get("workflow") or {}).get("id"))
print("  URL     = https://aiagent.cqut.edu.cn:31134/chat/%s" % CODE)