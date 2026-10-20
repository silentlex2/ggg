# -*- coding: utf-8 -*-
"""定位 v19 应用与知识库所属租户，判断知识库是否可写。"""
import json
import ssl
import sys
import urllib.error
import urllib.request

from tok import token

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://aiagent.cqut.edu.cn:31134"
TOK = token()
HDR = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
APP = "214d5f6b-c1ca-4bc8-9ee7-02be1f1ecbf4"


def get(path):
    req = urllib.request.Request(BASE + path, headers=HDR)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")[:200]
    except Exception as exc:  # noqa: BLE001
        return -1, repr(exc)


st, app = get("/console/api/apps/" + APP)
if st != 200:
    print("app [%s] %s" % (st, app))
    raise SystemExit(1)
print("app 字段: %s" % ", ".join(sorted(app.keys())))
for key in ("tenant_id", "workspace_id", "created_by", "status", "enable_site"):
    if key in app:
        val = app[key]
        shown = val if isinstance(val, str) else json.dumps(val, ensure_ascii=False)[:120]
        print("   %-14s %s" % (key, shown))
print("")

for path in ["/console/api/workspaces",
             "/console/api/datasets?page=1&limit=100&tag_ids=",
             "/console/api/datasets?page=1&limit=100&ids=9178aa02c3d811f1be159fcedc704656"]:
    st, body = get(path)
    txt = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
    print("[%s] %s" % (st, path))
    print("     " + txt[:260])
    print("")
