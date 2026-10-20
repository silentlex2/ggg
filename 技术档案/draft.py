#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「职引」工作流草稿操作四件套。

用法：
    python draft.py pull   [app_id]            # 拉草稿 -> scratch/draft.json
    python draft.py show   [app_id]            # 打印节点清单
    python draft.py push   <body.json> [app_id]# 用 body.json 覆盖保存草稿
    python draft.py publish [app_id]           # 发布草稿
    python draft.py wfid   [app_id]            # 打印 app.workflow.id
    python draft.py savepull [app_id]          # pull 后立刻 publish（同一次调用内）

默认 app_id = 正式站应用（38c3e937-…）。
"""
import json, os, ssl, sys, urllib.request
from tok import token  # 控制台 token 统一入口（见 tok.py）

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "scratch")
DEFAULT_APP = "38c3e937-b888-4564-bb2e-39f2520e28f3"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def token():
    return token()


def api(path, method="GET", body=None):
    t = token()
    h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, context=CTX, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def draft_path(app):
    return os.path.join(SCRATCH, "draft.json")


def pull(app):
    d = api("/console/api/apps/%s/workflows/draft" % app)
    with open(draft_path(app), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("pulled hash=%s nodes=%d" % (d.get("hash"), len(d["graph"]["nodes"])))
    return d


def body_of(d):
    return {"graph": d["graph"], "viewport": d.get("viewport"),
            "features": d.get("features"), "environment_variables": d.get("environment_variables"),
            "conversation_variables": d.get("conversation_variables")}


def push(app, body_file):
    body = json.load(open(body_file, encoding="utf-8"))
    if "graph" not in body:
        body = body_of(body)
    d = api("/console/api/apps/%s/workflows/draft" % app, "POST", body)
    # 保存接口不一定回传 graph（本平台只回简单结构），所以保存后再拉一次确认
    nn = (d.get("graph") or {}).get("nodes")
    if nn is None:
        d = api("/console/api/apps/%s/workflows/draft" % app)
    print("saved hash=%s nodes=%d" % (d.get("hash"), len(d["graph"]["nodes"])))
    return d


def publish(app):
    d = api("/console/api/apps/%s/workflows/publish" % app, "POST",
            {"marked_name": "", "marked_comment": ""})
    print("published workflow_id=%s" % (d.get("id") or d.get("workflow_id")))
    return d


def wfid(app):
    a = api("/console/api/apps/%s" % app)
    print("app=%s name=%s enable_site=%s site=%s wf=%s"
          % (app, a.get("name"), a.get("enable_site"), (a.get("site") or {}).get("code"),
             (a.get("workflow") or {}).get("id")))
    return a


def show(app):
    d = pull(app) if not os.path.exists(draft_path(app)) else json.load(open(draft_path(app), encoding="utf-8"))
    for n in d["graph"]["nodes"]:
        t = n.get("data", {}).get("type")
        print("%-22s %-16s %s" % (t, n["data"].get("title"), n["id"]))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    args = sys.argv[2:]
    app = DEFAULT_APP
    if cmd == "pull":
        if args: app = args[0]
        pull(app)
    elif cmd == "show":
        if args: app = args[0]
        show(app)
    elif cmd == "push":
        if len(args) > 1: app = args[1]
        push(app, args[0])
    elif cmd == "publish":
        if args: app = args[0]
        publish(app)
    elif cmd == "wfid":
        if args: app = args[0]
        wfid(app)
    else:
        print(__doc__)
