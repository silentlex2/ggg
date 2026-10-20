# -*- coding: utf-8 -*-
"""documents 列表路由参数矩阵，找能返回 200 的组合。"""
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

RAW = "9178aa02c3d811f1be159fcedc704656"
DASH = "9178aa02-c3d8-11f1-be15-9fcedc704656"

SUFFIXES = [
    "",
    "?page=1&limit=20",
    "?page=1&limit=20&keyword=",
    "?page=1&limit=20&keyword=&status=all",
    "?page=1&limit=20&keyword=&status=completed",
    "?page=1&limit=5&keyword=&sort_by=created_at&sort_order=desc",
]


def get(path):
    req = urllib.request.Request(BASE + path, headers=HDR)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=45) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")[:140]
    except Exception as exc:  # noqa: BLE001
        return -1, repr(exc)


for ds in (RAW, DASH):
    for suf in SUFFIXES:
        path = "/console/api/datasets/%s/documents%s" % (ds, suf)
        st, body = get(path)
        print("[%s] %s" % (st, path))
        if st == 200:
            try:
                j = json.loads(body)
                print("     total=%s docs=%s" % (j.get("total"), len(j.get("data") or [])))
                for d in (j.get("data") or [])[:6]:
                    print("     doc=%-38s %-44s status=%s words=%s" % (
                        d.get("id"), (d.get("name") or "")[:42],
                        d.get("indexing_status") or d.get("status"), d.get("word_count")))
            except Exception:  # noqa: BLE001
                print("     " + body[:200])
        else:
            print("     " + body.replace(chr(10), " ")[:140])
    print("")
