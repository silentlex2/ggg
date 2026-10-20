# -*- coding: utf-8 -*-
"""v15：只加可用性兜底 —— 实时政策源失败时不拖垮政策分支。

背景：ncss.cn 抖动时，实时政策源节点失败会让整条政策分支 500。
2026-10-20 在已下线的 v14 试验应用上验证：本 fork 的 HTTP 节点支持
error_strategy（continue / fail-branch / default-value）与 retry_config，且能持久化。
取 default-value（body 置空）：失败时政策顾问只拿知识库内容作答，用户仍能拿到答案。

顺序遵循实测结论：改源草稿 -> 发布源 -> 再 copy 出新站（站点绑复制瞬间的草稿快照）。

用法：
    python build_v15.py --apply
"""
import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

SRC = "894016f2-1cfa-4254-9cde-b09752d09628"     # v13 正式站（25 节点、干净口径）
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
HTTP_NODE = "1791600200001"                       # 实时政策源


def tok():
    t = os.environ.get("CONSOLE_TOKEN", "").strip()
    if not t:
        raise SystemExit("需要 CONSOLE_TOKEN")
    return t


def api(path, method="GET", body=None):
    t = tok()
    h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw[:300]


def patch_http(graph):
    report = []
    node = next((n for n in graph["nodes"] if n["id"] == HTTP_NODE), None)
    if node is None:
        raise SystemExit("找不到实时政策源节点")
    d = node["data"]
    d["error_strategy"] = "default-value"
    d["default_value"] = [{"key": "body", "type": "string", "value": ""}]
    d["retry_config"] = {"retry_enabled": True, "max_retries": 2, "retry_interval": 1000}
    d["timeout"] = {"max_connect_timeout": 6, "max_read_timeout": 6, "max_write_timeout": 6}
    report.append("实时政策源：error_strategy=default-value（body 置空）+ 重试 2 次 / 间隔 1s + 超时 6s")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--name", default="职引 · 校园就业智能体 v15")
    a = ap.parse_args()
    if not a.apply:
        print(__doc__)
        return 0

    print("== 1. 拉源草稿 ==")
    s, draft = api("/console/api/apps/%s/workflows/draft" % a.src)
    print("   nodes=%d edges=%d" % (len(draft["graph"]["nodes"]), len(draft["graph"]["edges"])))
    for line in patch_http(draft["graph"]):
        print("   -", line)

    print("== 2. 保存并发布源应用 ==")
    body = {"graph": draft["graph"], "viewport": draft.get("viewport"),
            "features": draft.get("features"),
            "environment_variables": draft.get("environment_variables"),
            "conversation_variables": draft.get("conversation_variables")}
    s, _ = api("/console/api/apps/%s/workflows/draft" % a.src, "POST", body)
    print("   save ->", s)
    if s != 200:
        raise SystemExit("保存失败")
    s, _ = api("/console/api/apps/%s/workflows/publish" % a.src, "POST",
               {"marked_name": "", "marked_comment": "v15 实时政策源兜底"})
    print("   publish ->", s)
    if s != 200:
        raise SystemExit("发布失败")

    print("== 3. 复制成新对外应用 ==")
    s, j = api("/console/api/apps/%s/copy" % a.src, "POST",
               {"name": a.name, "icon_type": None, "icon": None,
                "icon_background": None, "mode": "advanced-chat"})
    if s not in (200, 201):
        raise SystemExit("copy 失败 %s" % s)
    app = j["id"]; code = (j.get("site") or {}).get("code")
    print("   NEW_APP =", app, "| SITE =", code)
    s, _ = api("/console/api/apps/%s" % app, "PUT", {
        "name": "职引 · 校园就业智能体",
        "description": "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询 · 重庆理工大学",
        "icon_type": "image", "icon": ICON, "icon_background": "",
        "use_icon_as_answer_icon": True})
    print("   改名+图标 ->", s)
    s, _ = api("/console/api/apps/%s/workflows/publish" % app, "POST",
               {"marked_name": "", "marked_comment": "v15 对外发布"})
    print("   publish new ->", s)
    s, _ = api("/console/api/apps/%s/site-enable" % app, "POST", {"enable_site": True})
    print("   site-enable ->", s)

    print("== 4. 等站点可用 ==")
    for i in range(10):
        time.sleep(8)
        try:
            req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": code})
            with urllib.request.urlopen(req, context=CTX, timeout=20) as r:
                if r.status == 200:
                    print("   就绪"); break
        except Exception as e:
            print("   第 %d 次：%s" % (i + 1, e))

    print()
    print("NEW_APP =", app)
    print("SITE    =", code)
    with open(os.path.join(HERE, "v15-result.json"), "w", encoding="utf-8") as f:
        json.dump({"app": app, "site": code}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
