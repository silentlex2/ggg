#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 draft 运行端点 + 应用绑定的 workflow 版本。"""
import json, os, ssl, sys, time, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
APP = "69fa1c02-27bf-41fc-a7d2-0c068480c034"
TOK = token()
H = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def call(path, body=None, method=None, timeout=180):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method or ("POST" if data else "GET"), headers=H)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:400]
    except Exception as e:
        return -1, repr(e)


st, body = call("/console/api/apps/" + APP)
print("GET app -> %d" % st)
if st == 200:
    a = json.loads(body)
    print("  name =", a.get("name"))
    print("  workflow =", json.dumps(a.get("workflow"), ensure_ascii=False)[:300])
    print("  关联字段 keys =", [k for k in a if "work" in k.lower() or "version" in k.lower()])

q = "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"
for path in ["/console/api/apps/%s/workflows/draft/run" % APP,
             "/console/api/apps/%s/workflows/draft/run-node" % APP]:
    st, body = call(path, {"inputs": {"user_input": q}, "files": []})
    print("\nPOST %s -> %d  %d 字节" % (path.split("/")[-1], st, len(body)))
    if st == 200:
        cnt = {}
        rr = None
        for blk in body.replace("\r\n", "\n").split("\n\n"):
            if not blk.startswith("data:"):
                continue
            try:
                j = json.loads(blk[5:].strip())
            except Exception:
                continue
            ev = j.get("event", "?")
            cnt[ev] = cnt.get(ev, 0) + 1
            if ev == "workflow_finished":
                print("  workflow_finished.workflow_id =", j.get("data", {}).get("workflow_id"))
            if ev == "node_finished" and j.get("data", {}).get("title") == "岗位知识库":
                o = j["data"].get("outputs") or {}
                print("  岗位知识库 outputs keys =", list(o))
                res = o.get("result")
                if isinstance(res, list):
                    print("  result = %d 条" % len(res))
                    for i, it in enumerate(res[:5]):
                        if isinstance(it, dict):
                            print("    [%d] score=%s %s" % (i, it.get("score"), (it.get("content") or "")[:150].replace("\n", " ")))
        print("  事件统计:", cnt)
        break
    else:
        print("  ", body[:200])
