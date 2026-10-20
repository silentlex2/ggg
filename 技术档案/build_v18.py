# -*- coding: utf-8 -*-
"""v18：ctx 只加给「闲聊引导」和「岗位匹配」，面试官保持 v15 原样。

依据（v16/v17 连续两次回归）：
  · v16 给三个节点加"历史上下文"块 -> 面试多轮全崩（进度倒退），黄金集 0.850
  · v17 改成"仅当非空才生效" -> 仍然 T2 回退到第 1 题，说明**只要动了面试官提示词就会伤到它原有的进度逻辑**
结论：面试官的进度推进靠它自己那套规则，别碰；多轮短板其实只在"省略句指代"这类场景，
      而这类场景落在闲聊/岗位两个分支 —— 把 ctx 只给这两个，收益最大、风险最小。

以 v15 正式站（30b743bd，干净 25 节点）为源，重建一遍。
"""
import argparse, json, os, ssl, sys, time, urllib.error, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SRC = "30b743bd-bdc3-4896-9d22-dac64637755d"     # v15（面试官为原始版本）
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
START = "1791542455112"
MARK = "〔v18 历史上下文〕"
TARGETS = {"1791600000001": "闲聊引导", "1791552000011": "岗位匹配"}   # 只有这两个

BLOCK = """

## 历史上下文〔v18 历史上下文〕

本节只在下面「本轮历史上下文」非空时生效；为空时忽略本节，照常作答，不要主动说"我看不到上文"。

当它非空时：那些文字是用户此前亲口说过的话，等同于上文，用来理解指代（"这两个城市""这个岗位""那要准备什么材料"）。
能据此直接回答就直接回答，不要反问"你指的是哪两个"。
"""


def tok():
    t = os.environ.get("CONSOLE_TOKEN", "").strip()
    if not t:
        raise SystemExit("需要 CONSOLE_TOKEN")
    return t


def api(path, method="GET", body=None):
    t = tok(); h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8"); h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try: return e.code, json.loads(raw)
        except Exception: return e.code, raw[:300]


def patch(graph):
    log = []
    nodes = {n["id"]: n for n in graph["nodes"]}
    st = nodes[START]["data"]
    vs = st.setdefault("variables", [])
    if not any(v.get("variable") == "ctx" for v in vs):
        vs.append({"variable": "ctx", "label": "历史上下文（前端自动填写）", "type": "paragraph",
                   "max_length": 2000, "required": False, "isLongTxtSelected": True,
                   "options": [], "allowed_file_extensions": [], "allowed_file_types": [],
                   "allowed_file_upload_methods": [], "max_length_file": 0})
        log.append("start 新增可选变量 ctx")
    for nid, title in TARGETS.items():
        d = nodes[nid]["data"]
        sys_msg = next((p for p in (d.get("prompt_template") or []) if p.get("role") == "system"), None)
        if sys_msg is None:
            log.append("! %s 无 system 提示词" % title); continue
        if MARK in sys_msg.get("text", ""):
            log.append("%s 已含 v18 块，跳过" % title); continue
        before = len(sys_msg["text"])
        sys_msg["text"] = sys_msg["text"].rstrip() + BLOCK + "\n【本轮历史上下文】\n{{#%s.ctx#}}\n" % START
        log.append("%s system %d -> %d 字" % (title, before, len(sys_msg["text"])))
    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--name", default="职引 · 校园就业智能体 v18")
    ap.add_argument("--src", default=SRC, help="源应用（要干净的 v15 草稿）")
    a = ap.parse_args()
    if not a.apply:
        print(__doc__); return 0

    SRC_APP = a.src
    s, draft = api("/console/api/apps/%s/workflows/draft" % SRC_APP)
    print("源草稿 nodes=%d" % len(draft["graph"]["nodes"]))
    for line in patch(draft["graph"]):
        print("  -", line)

    body = {"graph": draft["graph"], "viewport": draft.get("viewport"),
            "features": draft.get("features"),
            "environment_variables": draft.get("environment_variables"),
            "conversation_variables": draft.get("conversation_variables")}
    s, _ = api("/console/api/apps/%s/workflows/draft" % SRC_APP, "POST", body); print("save ->", s)
    if s != 200: raise SystemExit("保存失败")
    s, _ = api("/console/api/apps/%s/workflows/publish" % SRC_APP, "POST",
               {"marked_name": "", "marked_comment": "v18 ctx 只给闲聊/岗位"}); print("publish ->", s)
    if s != 200: raise SystemExit("发布失败")

    s, j = api("/console/api/apps/%s/copy" % SRC_APP, "POST",
               {"name": a.name, "icon_type": None, "icon": None,
                "icon_background": None, "mode": "advanced-chat"})
    if s not in (200, 201): raise SystemExit("copy 失败 %s" % s)
    app = j["id"]; code = (j.get("site") or {}).get("code")
    print("NEW_APP =", app, "| SITE =", code)
    api("/console/api/apps/%s" % app, "PUT", {
        "name": "职引 · 校园就业智能体",
        "description": "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询 · 重庆理工大学",
        "icon_type": "image", "icon": ICON, "icon_background": "", "use_icon_as_answer_icon": True})
    api("/console/api/apps/%s/workflows/publish" % app, "POST", {"marked_name": "", "marked_comment": "v18 对外发布"})
    api("/console/api/apps/%s/site-enable" % app, "POST", {"enable_site": True})
    for i in range(10):
        time.sleep(8)
        try:
            req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": code})
            with urllib.request.urlopen(req, context=CTX, timeout=20) as r:
                if r.status == 200:
                    print("就绪"); break
        except Exception as e:
            print("  %d: %s" % (i + 1, e))
    with open(os.path.join(HERE, "v18-result.json"), "w", encoding="utf-8") as f:
        json.dump({"app": app, "site": code}, f, ensure_ascii=False, indent=1)
    print("SITE =", code)
    return 0


if __name__ == "__main__":
    sys.exit(main())
