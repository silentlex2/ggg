# -*- coding: utf-8 -*-
"""v16：给工作流加一个 ctx 变量，让外部前端可以把「历史」带进来。

背景（2026-10-20 实测）：
  · 平台不向任何 LLM 节点注入会话历史（三组探针确认），多轮上下文丢失。
  · 但 /v1 API 的 inputs 支持任意字段透传，且 CORS 为 *（外部静态页可直接调用）。
  → 让前端当"记忆"：每轮把用户此前说过的话压成一段〔历史〕塞进 inputs.ctx，
    工作流 start 节点加一个可选变量 ctx，相关提示词按"这就是上下文"来用。

顺序遵循实测结论：改源草稿 -> 发布源 -> 再 copy 出新站。

用法：python build_v16.py --apply
"""
import argparse, json, os, ssl, sys, time, urllib.error, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SRC = "30b743bd-bdc3-4896-9d22-dac64637755d"     # v15 正式站
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
START = "1791542455112"
MARK = "〔v16 历史上下文〕"

BLOCK = """

## 历史上下文〔v16 历史上下文〕

输入里若有一段以〔历史〕开头的内容，那是**用户此前亲口说过的话**，等同于你知道的上下文。
1. 能据此直接回答就直接回答；**禁止**再说「我这边看不到上文」「你指的是哪两个」「咱们这是刚聊上」。
2. 用户用省略句追问（「那这两个城市哪个更适合我」「这两个岗位选哪个」「继续」「重练第 3 题」）时，
   先到〔历史〕里找指代对象或原题，再作答。
3. 只有〔历史〕为空时，才按"没有上文"处理。
"""

TARGETS = ["1791600000001", "1791552000011", "1791552000021"]   # 闲聊引导 / 岗位匹配 / 模拟面试官


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
    vars_ = st.setdefault("variables", [])
    if not any(v.get("variable") == "ctx" for v in vars_):
        vars_.append({
            "variable": "ctx", "label": "历史上下文（前端自动填写）", "type": "paragraph",
            "max_length": 2000, "required": False, "isLongTxtSelected": True,
            "options": [], "allowed_file_extensions": [],
            "allowed_file_types": [], "allowed_file_upload_methods": [], "max_length_file": 0,
        })
        log.append("start 节点新增可选变量 ctx")
    for nid in TARGETS:
        d = nodes[nid]["data"]
        pt = d.get("prompt_template") or []
        sys_msg = next((p for p in pt if p.get("role") == "system"), None)
        if sys_msg is None:
            log.append("! %s 没有 system 提示词，跳过" % d.get("title"))
            continue
        if MARK in sys_msg.get("text", ""):
            log.append("%s 已含 v16 块，跳过" % d.get("title"))
            continue
        before = len(sys_msg["text"])
        sys_msg["text"] = sys_msg["text"].rstrip() + BLOCK
        # 让提示词真的引用 ctx 变量
        if "{{#%s.ctx#}}" % START not in sys_msg["text"]:
            sys_msg["text"] += "\n【本轮历史上下文】\n{{#%s.ctx#}}\n" % START
        log.append("%s system %d -> %d 字" % (d.get("title"), before, len(sys_msg["text"])))
    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--name", default="职引 · 校园就业智能体 v16")
    a = ap.parse_args()
    if not a.apply:
        print(__doc__); return 0

    print("== 1. 拉源草稿 ==")
    s, draft = api("/console/api/apps/%s/workflows/draft" % SRC)
    print("   nodes=%d" % len(draft["graph"]["nodes"]))
    for line in patch(draft["graph"]):
        print("   -", line)

    print("== 2. 保存 + 发布源 ==")
    body = {"graph": draft["graph"], "viewport": draft.get("viewport"),
            "features": draft.get("features"),
            "environment_variables": draft.get("environment_variables"),
            "conversation_variables": draft.get("conversation_variables")}
    s, _ = api("/console/api/apps/%s/workflows/draft" % SRC, "POST", body); print("   save ->", s)
    if s != 200: raise SystemExit("保存失败")
    s, _ = api("/console/api/apps/%s/workflows/publish" % SRC, "POST",
               {"marked_name": "", "marked_comment": "v16 ctx 历史上下文"}); print("   publish ->", s)
    if s != 200: raise SystemExit("发布失败")

    print("== 3. 复制新站 ==")
    s, j = api("/console/api/apps/%s/copy" % SRC, "POST",
               {"name": a.name, "icon_type": None, "icon": None,
                "icon_background": None, "mode": "advanced-chat"})
    if s not in (200, 201): raise SystemExit("copy 失败 %s" % s)
    app = j["id"]; code = (j.get("site") or {}).get("code")
    print("   NEW_APP =", app, "| SITE =", code)
    api("/console/api/apps/%s" % app, "PUT", {
        "name": "职引 · 校园就业智能体",
        "description": "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询 · 重庆理工大学",
        "icon_type": "image", "icon": ICON, "icon_background": "",
        "use_icon_as_answer_icon": True})
    api("/console/api/apps/%s/workflows/publish" % app, "POST", {"marked_name": "", "marked_comment": "v16 对外发布"})
    api("/console/api/apps/%s/site-enable" % app, "POST", {"enable_site": True})
    print("== 4. 等站点 ==")
    for i in range(10):
        time.sleep(8)
        try:
            req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": code})
            with urllib.request.urlopen(req, context=CTX, timeout=20) as r:
                if r.status == 200:
                    print("   就绪"); break
        except Exception as e:
            print("   %d: %s" % (i + 1, e))
    print("SITE =", code)
    with open(os.path.join(HERE, "v16-result.json"), "w", encoding="utf-8") as f:
        json.dump({"app": app, "site": code}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
