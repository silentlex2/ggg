# -*- coding: utf-8 -*-
"""探测：这个账号能否创建数据集 / 上传文档（用于判断 KB4 v2 能不能走接口上传）。

只做最小动作，写完立刻删，避免在工作空间留垃圾。
"""
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

sys.path.insert(0, HERE)
from tok import token  # noqa: E402

TOK = token()


def api(path, method="GET", body=None, raw=None, ctype=None):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    headers = {"Authorization": "Bearer " + TOK, "OperToken": TOK}
    if data is not None:
        headers["Content-Type"] = ctype or "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=120) as r:
            txt = r.read().decode("utf-8", "replace")
            code = r.status
    except urllib.error.HTTPError as e:
        txt, code = e.read().decode("utf-8", "replace"), e.code
    except Exception as e:  # noqa: BLE001
        return -1, {"error": repr(e)}
    try:
        return code, json.loads(txt) if txt.strip() else None
    except ValueError:
        return code, txt[:300]


print("== 1) 创建探针数据集 ==")
body = {"name": "zz-probe-delete-me", "description": "路由探测用，稍后删除",
        "indexing_technique": "high_quality", "permission": "only_me",
        "provider": "vendor", "embedding_model": "bge-m3",
        "embedding_model_provider": "langgenius/azure_openai/azure_openai"}
code, obj = api("/console/api/datasets", "POST", body)
print("  POST /console/api/datasets ->", code, str(obj)[:300])
ds_id = ""
if code in (200, 201) and isinstance(obj, dict):
    ds_id = obj.get("id") or ""

if not ds_id:
    print("\n创建失败或未返回 id，试试不带 embedding 的最小 body：")
    code2, obj2 = api("/console/api/datasets", "POST",
                      {"name": "zz-probe-delete-me", "indexing_technique": "economy",
                       "permission": "only_me"})
    print("  ->", code2, str(obj2)[:300])
    if code2 in (200, 201) and isinstance(obj2, dict):
        ds_id = obj2.get("id") or ""

if not ds_id:
    print("\n结论：当前账号无法通过接口创建数据集。")
    sys.exit(2)

print("  数据集 id =", ds_id)

print("\n== 2) 往这个数据集写一条文本 ==")
doc = {"name": "probe.md", "text": "# 探针\n\n岗位编号 999 测试条目。\n",
       "indexing_technique": "economy", "process_rule": {"mode": "automatic"}}
code, obj = api("/console/api/datasets/%s/documents/create-by-text" % ds_id, "POST", doc)
print("  create-by-text ->", code, str(obj)[:300])

print("\n== 3) 列文档 ==")
code, obj = api("/console/api/datasets/%s/documents?page=1&limit=10" % ds_id)
print("  ->", code, str(obj)[:300])

print("\n== 4) 删除探针数据集 ==")
code, obj = api("/console/api/datasets/%s" % ds_id, "DELETE")
print("  DELETE ->", code, str(obj)[:200])