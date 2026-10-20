# -*- coding: utf-8 -*-
"""A 组探针：参数提取节点在「信息缺失」时会吐出什么？
关键问题：retrieval_query 一旦为空，下游知识库检索会拿空串去检索。
用法：python probe_empty.py
"""
import json, os, ssl, urllib.request
from tok import token  # 控制台 token 统一入口（见 tok.py）
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
TOK = token()
APP = "38c3e937-b888-4564-bb2e-39f2520e28f3"

def run_node(nid, query):
    body = json.dumps({"inputs": {"query": query}}).encode()
    r = urllib.request.Request(BASE + "/console/api/apps/%s/workflows/draft/nodes/%s/run" % (APP, nid),
        data=body, method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + TOK, "OperToken": TOK})
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"_err": e.code, "_body": e.read().decode()[:400]}

CASES = ["有什么岗位", "你好", "帮我找工作", "我想找机械的工作", "   ", "工作"]
NID = "1791600000030"  # 求职意向提取
for q in CASES:
    d = run_node(NID, q)
    if "_err" in d:
        print("[%r] 错误 %s %s" % (q, d["_err"], d["_body"])); continue
    out = (d.get("data") or {}).get("outputs") or d.get("outputs") or {}
    print("[%-14r] -> %s" % (q, json.dumps(out, ensure_ascii=False)))
    print("    status=%s elapsed=%.2f" % ((d.get("data") or {}).get("status"), (d.get("data") or {}).get("elapsed_time") or -1))
