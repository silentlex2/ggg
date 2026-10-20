# -*- coding: utf-8 -*-
"""确认当前 token 所属账号、工作区与可见应用，排除串号。"""
import json
import ssl
import sys
import urllib.request

from tok import token

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://aiagent.cqut.edu.cn:31134"
TOK = token()
HDR = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def get(path):
    req = urllib.request.Request(BASE + path, headers=HDR)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001
        return -1, repr(exc)


for path in ["/console/api/account/profile",
             "/console/api/workspaces/current",
             "/console/api/apps?page=1&limit=100"]:
    st, body = get(path)
    print("[%d] %s" % (st, path))
    if path.endswith("apps?page=1&limit=100"):
        try:
            j = json.loads(body)
            for a in j.get("data", []):
                print("    app %s  %s  mode=%s" % (a.get("id"), a.get("name"), a.get("mode")))
        except Exception:  # noqa: BLE001
            print("    " + body[:400])
    else:
        print("    " + body[:500])
    print("")
