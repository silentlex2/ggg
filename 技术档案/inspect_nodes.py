# -*- coding: utf-8 -*-
"""列出 v19 草稿图的全部节点、类型与关键变量，重点看简历分支怎么取文件。"""
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
APP = "214d5f6b-c1ca-4bc8-9ee7-02be1f1ecbf4"

req = urllib.request.Request(BASE + "/console/api/apps/%s/workflows/draft" % APP, headers=HDR)
with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
    graph = json.loads(r.read().decode("utf-8", "replace"))

nodes = (graph.get("graph") or {}).get("nodes") or []
print("节点 %d 个" % len(nodes))
for node in nodes:
    data = node.get("data") or {}
    kind = data.get("type")
    title = data.get("title") or ""
    nid = data.get("id") or node.get("id")
    extra = ""
    if kind == "document-extractor":
        extra = "  variable_selector=%s" % data.get("variable_selector")
    elif kind == "start":
        extra = "  variables=%s" % [
            (v.get("variable"), v.get("type"), v.get("required")) for v in (data.get("variables") or [])]
    elif kind in ("end", "answer"):
        pass
    print("  %-22s %-20s %s%s" % (str(nid)[:20], kind, title[:18], extra))

print("")
print("start 节点完整配置：")
for node in nodes:
    data = node.get("data") or {}
    if data.get("type") == "start":
        print(json.dumps(data, ensure_ascii=False)[:1200])
