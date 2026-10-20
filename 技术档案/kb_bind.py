# -*- coding: utf-8 -*-
"""从 v19 草稿图里取出知识检索节点绑定的 dataset_id，并逐个回查名称与文档。"""
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


def get(path, raw=False):
    req = urllib.request.Request(BASE + path, headers=HDR)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
            body = r.read().decode("utf-8", "replace")
        return r.status, (body if raw else json.loads(body))
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")[:200]
    except Exception as exc:  # noqa: BLE001
        return -1, repr(exc)


st, graph = get("/console/api/apps/%s/workflows/draft" % APP)
if st != 200:
    print("草稿图获取失败 %s %s" % (st, graph))
    raise SystemExit(1)

nodes = (graph.get("graph") or {}).get("nodes") or []
print("节点 %d 个" % len(nodes))
found = {}
for node in nodes:
    data = node.get("data") or {}
    if data.get("type") != "knowledge-retrieval":
        continue
    cfg = data.get("dataset_ids") or (data.get("retrieval_config") or {})
    ids = data.get("dataset_ids") or []
    if not ids:
        for item in ((data.get("dataset_configs") or {}).get("datasets") or []):
            if isinstance(item, dict) and item.get("dataset", {}).get("id"):
                ids.append(item["dataset"]["id"])
    print("  节点 %-16s %-20s datasets=%s" % (data.get("id"), (data.get("title") or "")[:18], ids))
    for did in ids:
        found[did] = data.get("title")

print("")
for did, title in found.items():
    st, j = get("/console/api/datasets/" + did)
    if st != 200:
        print("[%s] %s  (%s)" % (st, did, title))
        continue
    print("[200] %-34s name=%-24s docs=%s words=%s" % (
        did, (j.get("name") or "")[:22], j.get("document_count"), j.get("word_count")))
    st2, dl = get("/console/api/datasets/%s/documents?page=1&limit=50" % did)
    if st2 == 200:
        for d in dl.get("data", []):
            print("        doc=%-34s %-42s words=%s" % (
                d.get("id"), (d.get("name") or "")[:40], d.get("word_count")))
    else:
        print("        docs ERR %s %s" % (st2, dl))
