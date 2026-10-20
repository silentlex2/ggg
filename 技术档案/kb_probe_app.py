# -*- coding: utf-8 -*-
"""核对 v19 应用 ID 是否仍在当前账号可见：应用详情 + 站点可用性双检。"""
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

TARGETS = {
    "v19": "214d5f6b-c1ca-4bc8-9ee7-02be1f1ecbf4",
    "list-a": "f2e4f2a5-8e96-4a15-972d-4c2d5af57669",
    "list-b": "bdd594c0-fe36-46bb-bc64-d3633212cde0",
}

for label, app_id in TARGETS.items():
    req = urllib.request.Request(BASE + "/console/api/apps/" + app_id, headers=HDR)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
            j = json.loads(r.read().decode("utf-8", "replace"))
        print("[200] %-7s %s  name=%s  updated=%s" % (label, app_id, j.get("name"), j.get("updated_at")))
        wf = j.get("workflow") or {}
        print("        workflow=%s" % wf.get("id"))
    except urllib.error.HTTPError as exc:
        print("[%d] %-7s %s" % (exc.code, label, app_id))
    except Exception as exc:  # noqa: BLE001
        print("[ERR] %-7s %s %r" % (label, app_id, exc))

print("")
site = open("readysite.txt", encoding="utf-8").read().strip()
print("readysite.txt = %s" % site)
req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": site})
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        print("[%d] passport ok" % r.status)
except Exception as exc:  # noqa: BLE001
    print("[ERR] passport %r" % exc)
