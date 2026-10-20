#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识库归属与命中诊断：dataset 端点探测 + hit-testing + 引用来源抓取。"""
import json, os, ssl, sys, time, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
TOK = token()
CH = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}

DS = {
    "85357644c3d811f183f6a528325d1794": "?",
    "9178aa02c3d811f1be159fcedc704656": "?",
    "9181323ac3d811f18ed6417ebb96d453": "?",
    "91897eaec3d811f1bcaee142a16b21be": "?",
    "85c97abcc3db11f1be159fcedc704656": "?",
    "916f7decc3d811f19c74610e3ad0f451": "?",
}


def call(url, body=None, headers=None, timeout=60, method=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"), headers=headers or {})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:300]
    except Exception as e:
        return -1, repr(e)


print("=" * 78)
print("A. dataset 端点探测")
print("=" * 78)
for path in ["/console/api/datasets?page=1&limit=50",
             "/console/api/datasets/9178aa02c3d811f1be159fcedc704656",
             "/console/api/datasets/9178aa02c3d811f1be159fcedc704656/documents?page=1&limit=3"]:
    st, body = call(BASE + path, headers=CH)
    print("[%d] %s\n     %s" % (st, path, body[:280].replace("\n", " ")))

print("\n" + "=" * 78)
print("B. hit-testing（直接问知识库要结果）")
print("=" * 78)
RM = {"search_method": "hybrid_search", "reranking_enable": False, "reranking_mode": None,
      "reranking_model": {"provider": "openai_api_compatible", "model": "bge-reranker-v2-m3"},
      "weights": {"weight_type": "customized",
                  "vector_setting": {"vector_weight": 0.6, "embedding_provider_name": "", "embedding_model_name": ""},
                  "keyword_setting": {"keyword_weight": 0.4}},
      "top_k": 5, "score_threshold_enabled": True, "score_threshold": 0.1}
for did in DS:
    for body in [{"query": "化工工艺工程师 重庆 校招", "retrieval_model": RM},
                 {"query": "化工工艺工程师 重庆 校招", "retrieval_model": {}}]:
        st, out = call(BASE + "/console/api/datasets/" + did + "/hit-testing", body=body, headers=CH, timeout=90)
        print("\n[%d] dataset %s  keys=%s" % (st, did[:10], list(body["retrieval_model"])[:2]))
        print("     " + out[:600].replace("\n", " "))
        if st == 200:
            break

print("\n" + "=" * 78)
print("C. 对话抓 retriever_resources（引用来源）")
print("=" * 78)


def tok():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


t = tok()
q = "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"
payload = {"response_mode": "streaming", "conversation_id": "", "query": q,
           "inputs": {"user_input": q}, "parent_message_id": None}
req = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(payload).encode(), method="POST",
                             headers={"Content-Type": "application/json", "X-App-Code": SITE,
                                      "authorization": "Bearer " + t, "auth-token": "Bearer " + t})
with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
    raw = r.read().decode("utf-8", "replace")
for blk in raw.replace("\r\n", "\n").split("\n\n"):
    if not blk.startswith("data:"):
        continue
    try:
        j = json.loads(blk[5:].strip())
    except Exception:
        continue
    if j.get("event") == "message_end":
        md = j.get("data", j).get("metadata", {}) or {}
        rr = md.get("retriever_resources") or []
        print("retriever_resources: %d 条" % len(rr))
        for i, it in enumerate(rr):
            print("  [%d] score=%s  dataset=%s  doc=%s" % (i, it.get("score"), it.get("dataset_name") or it.get("dataset_id", "")[:8],
                                                           (it.get("document_name") or "")[:40]))
            print("      %s" % (it.get("content") or "")[:220].replace("\n", " "))
    elif j.get("event") == "node_finished":
        d = j.get("data", {})
        if d.get("title") in ("求职意向提取", "岗位知识库"):
            print("\n▶ %s inputs=%s outputs=%s" % (d.get("title"),
                  json.dumps(d.get("inputs"), ensure_ascii=False)[:300],
                  json.dumps(d.get("outputs"), ensure_ascii=False)[:400]))
