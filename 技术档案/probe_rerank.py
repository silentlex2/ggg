#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探测平台可用的 rerank 模型与 provider 配置。"""
import json, os, ssl, sys, urllib.request, urllib.error
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
TOK = open(os.path.join(HERE, "scratch", ".token"), encoding="utf-8").read().strip()
H = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def get(path, timeout=60):
    req = urllib.request.Request(BASE + path, headers=H)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:400]
    except Exception as e:
        return -1, repr(e)


for path in ["/console/api/workspaces/current/models/model-types/rerank",
             "/console/api/workspaces/current/model-providers",
             "/console/api/workspaces/current/models/model-types/text-embedding",
             "/console/api/datasets/retrieval-setting"]:
    st, body = get(path)
    print("\n[%d] %s" % (st, path))
    try:
        j = json.loads(body)
        print(json.dumps(j, ensure_ascii=False, indent=1)[:2500])
    except Exception:
        print(body[:600])
