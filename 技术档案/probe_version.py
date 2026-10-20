#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""确认 rerank 配置是否落盘、以及站点跑的是哪个 workflow 版本。"""
import json, os, ssl, sys, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
APP = "69fa1c02-27bf-41fc-a7d2-0c068480c034"
SITE = open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()
TOK = token()
H = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def get(path, headers=None, timeout=90):
    req = urllib.request.Request(BASE + path, headers=headers or H)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:400]
    except Exception as e:
        return -1, repr(e)


st, body = get("/console/api/apps/%s/workflows/draft" % APP)
print("GET draft -> %d" % st)
if st == 200:
    d = json.loads(body)
    print("draft hash =", d.get("hash"))
    for n in d["graph"]["nodes"]:
        if n["data"].get("type") == "knowledge-retrieval":
            c = n["data"].get("multiple_retrieval_config") or {}
            print("  [draft] %-8s rerank=%-5s mode=%-16s top_k=%s model=%s" %
                  (n["data"].get("title"), c.get("reranking_enable"), c.get("reranking_mode"),
                   c.get("top_k"), (c.get("reranking_model") or {}).get("model")))

st, body = get("/console/api/apps/%s/workflows/publish" % APP)
print("\nGET published -> %d  %s" % (st, body[:120]))
if st == 200:
    d = json.loads(body)
    print("published hash =", d.get("hash"), " graph.nodes =", len((d.get("graph") or {}).get("nodes", [])))
    for n in (d.get("graph") or {}).get("nodes", []):
        if n["data"].get("type") == "knowledge-retrieval":
            c = n["data"].get("multiple_retrieval_config") or {}
            print("  [published] %-8s rerank=%-5s mode=%-16s top_k=%s" %
                  (n["data"].get("title"), c.get("reranking_enable"), c.get("reranking_mode"), c.get("top_k")))

st, body = get("/console/api/apps/%s/workflows" % APP)
print("\nGET workflows -> %d  %s" % (st, body[:300]))


def tok():
    r = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(r, context=CTX, timeout=30) as resp:
        return json.loads(resp.read().decode())["access_token"]


t = tok()
q = "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"
payload = {"response_mode": "streaming", "conversation_id": "", "query": q,
           "inputs": {"user_input": q}, "parent_message_id": None}
req = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(payload).encode(), method="POST",
                             headers={"Content-Type": "application/json", "X-App-Code": SITE,
                                      "authorization": "Bearer " + t, "auth-token": "Bearer " + t})
with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
    raw = r.read().decode("utf-8", "replace")
print("\n--- 线上实际跑的版本 ---")
for blk in raw.replace("\r\n", "\n").split("\n\n"):
    if not blk.startswith("data:"):
        continue
    try:
        j = json.loads(blk[5:].strip())
    except Exception:
        continue
    if j.get("event") == "workflow_started":
        print("workflow_started.workflow_id =", j.get("data", {}).get("workflow_id"))
        print("  app_id =", j.get("data", {}).get("app_id"))
    if j.get("event") == "workflow_finished":
        print("workflow_finished.workflow_id =", j.get("data", {}).get("workflow_id"))
    if j.get("event") == "message_end":
        md = (j.get("data") or {}).get("metadata") or {}
        rr = md.get("retriever_resources") or []
        print("retriever_resources = %d 条" % len(rr))
