# -*- coding: utf-8 -*-
"""dataset_id 是去横线 UUID，补上横线后重试详情路由。"""
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

RAW = ["85357644c3d811f183f6a528325d1794", "9178aa02c3d811f1be159fcedc704656",
       "9181323ac3d811f18ed6417ebb96d453", "916f7decc3d811f19c74610e3ad0f451",
       "91897eaec3d811f1bcaee142a16b21be", "85c97abcc3db11f1be159fcedc704656"]


def dash(s):
    return "%s-%s-%s-%s-%s" % (s[0:8], s[8:12], s[12:16], s[16:20], s[20:32])


def get(path):
    req = urllib.request.Request(BASE + path, headers=HDR)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")[:160]
    except Exception as exc:  # noqa: BLE001
        return -1, repr(exc)


for raw in RAW:
    did = dash(raw)
    st, j = get("/console/api/datasets/" + did)
    if st != 200:
        print("[%s] %s" % (st, did))
        continue
    print("[200] %-38s %-28s docs=%s words=%s" % (did, (j.get("name") or "")[:26],
                                                  j.get("document_count"), j.get("word_count")))
    st2, dl = get("/console/api/datasets/%s/documents?page=1&limit=50" % did)
    if st2 != 200:
        print("      docs [%s] %s" % (st2, dl))
        continue
    for d in dl.get("data", []):
        print("      doc=%-38s %-46s words=%s status=%s" % (
            d.get("id"), (d.get("name") or "")[:44], d.get("word_count"),
            (d.get("indexing_status") or d.get("status"))))
