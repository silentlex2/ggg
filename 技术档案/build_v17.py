# -*- coding: utf-8 -*-
"""v17：修正 v16 的历史上下文块 —— 改成「仅当 ctx 非空才生效」。

v16 实测回归（40 条黄金集 0.975 -> 0.850）：
  E1/E2/E3/E7 全部从 PASS 变 FAIL，进度出现倒退 [1,2,1,0]，
  模型开始说「历史里没有出现过任何第 N 题标记，这场面试还没开始」。
原因：那段纪律把「看不到上文」当成了默认结论，ctx 为空（平台自带页面 / 评测走 /api）时
      模型反而主动判定"没有历史"，把本来能用的上下文也否掉了。

v17 写法：把条件写在最前面，空值时必须"忽略本节、照常作答"。
"""
import argparse, json, os, ssl, sys, time, urllib.error, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SRC = "6a8a65c0-aebe-4229-80d8-7f54544d867e"     # v16（含 ctx 变量与旧纪律块）
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
START = "1791542455112"
MARK = "〔v16 历史上下文〕"

NEW_BLOCK = """

## 历史上下文〔v17 有条件生效〕

本节**只在下面的「本轮历史上下文」非空时生效**。为空时请完全忽略本节，按你实际能看到的信息照常作答，
不要主动声明"我没有上文""咱们这是刚聊上"之类的话。

当它非空时：那些文字是**用户此前亲口说过的话**，等同于上文，用来理解指代（"这两个城市""继续""重练第 3 题"），
能据此直接回答就直接回答。
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


def rewrite(graph):
    log = []
    for n in graph["nodes"]:
        d = n.get("data") or {}
        for p in (d.get("prompt_template") or []):
            t = p.get("text") or ""
            if MARK not in t:
                continue
            head = t.split(MARK)[0]
            # 上一段以 "## 历史上下文〔v16" 开头，连同它一起切掉
            idx = head.rfind("## 历史上下文")
            if idx > 0:
                head = head[:idx]
            p["text"] = head.rstrip() + NEW_BLOCK + "\n【本轮历史上下文】\n{{#%s.ctx#}}\n" % START
            log.append("%s 重写历史上下文块" % d.get("title"))
    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--name", default="职引 · 校园就业智能体 v17")
    a = ap.parse_args()
    if not a.apply:
        print(__doc__); return 0

    s, draft = api("/console/api/apps/%s/workflows/draft" % SRC)
    print("源草稿 nodes=%d" % len(draft["graph"]["nodes"]))
    for line in rewrite(draft["graph"]):
        print("  -", line)

    body = {"graph": draft["graph"], "viewport": draft.get("viewport"),
            "features": draft.get("features"),
            "environment_variables": draft.get("environment_variables"),
            "conversation_variables": draft.get("conversation_variables")}
    s, _ = api("/console/api/apps/%s/workflows/draft" % SRC, "POST", body); print("save ->", s)
    if s != 200: raise SystemExit("保存失败")
    s, _ = api("/console/api/apps/%s/workflows/publish" % SRC, "POST",
               {"marked_name": "", "marked_comment": "v17 历史上下文改为条件生效"}); print("publish ->", s)
    if s != 200: raise SystemExit("发布失败")

    s, j = api("/console/api/apps/%s/copy" % SRC, "POST",
               {"name": a.name, "icon_type": None, "icon": None,
                "icon_background": None, "mode": "advanced-chat"})
    if s not in (200, 201): raise SystemExit("copy 失败 %s" % s)
    app = j["id"]; code = (j.get("site") or {}).get("code")
    print("NEW_APP =", app, "| SITE =", code)
    api("/console/api/apps/%s" % app, "PUT", {
        "name": "职引 · 校园就业智能体",
        "description": "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询 · 重庆理工大学",
        "icon_type": "image", "icon": ICON, "icon_background": "", "use_icon_as_answer_icon": True})
    api("/console/api/apps/%s/workflows/publish" % app, "POST", {"marked_name": "", "marked_comment": "v17 对外发布"})
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
    with open(os.path.join(HERE, "v17-result.json"), "w", encoding="utf-8") as f:
        json.dump({"app": app, "site": code}, f, ensure_ascii=False, indent=1)
    print("SITE =", code)
    return 0


if __name__ == "__main__":
    sys.exit(main())
