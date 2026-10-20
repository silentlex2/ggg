# -*- coding: utf-8 -*-
"""原始探测：打印 /console/api/datasets 的完整响应，确认返回结构。"""
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

for path in ["/console/api/datasets?page=1&limit=100",
             "/console/api/datasets",
             "/console/api/apps?page=1&limit=5"]:
    req = urllib.request.Request(BASE + path, headers=HDR)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
            body = r.read().decode("utf-8", "replace")
        print("[%s] %s" % (path, body[:900]))
    except Exception as exc:  # noqa: BLE001
        print("[%s] ERR %r" % (path, exc))
    print("")
