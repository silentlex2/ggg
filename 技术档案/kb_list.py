# -*- coding: utf-8 -*-
"""列出数据集与文档，定位 KB1~KB6 对应的 dataset_id 与文档 id。"""
import json
import os
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
    with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def main():
    data = get("/console/api/datasets?page=1&limit=100")
    items = data.get("data") or data.get("items") or []
    print("数据集 %d 个" % len(items))
    for it in items:
        print("  %-34s %-28s docs=%s words=%s" % (
            it.get("id"), (it.get("name") or "")[:26],
            it.get("document_count"), it.get("word_count")))
    print("")
    for it in items:
        did = it.get("id")
        try:
            docs = get("/console/api/datasets/%s/documents?page=1&limit=50" % did)
        except Exception as exc:  # noqa: BLE001
            print("  [ERR] %s %r" % (did, exc))
            continue
        dl = docs.get("data") or []
        print("== %s  (%d docs)" % (it.get("name"), len(dl)))
        for d in dl:
            print("     doc=%-34s %-40s words=%s" % (
                d.get("id"), (d.get("name") or "")[:38],
                (d.get("word_count") if d.get("word_count") is not None else d.get("tokens"))))
        print("")


if __name__ == "__main__":
    main()
