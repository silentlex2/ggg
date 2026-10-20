#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正式切换站点：新站点 jb3VQ96s2Vmv5aP4 / 应用 38c3e937。

做三件事：
  1. 把新应用的 draft 恢复成"只有岗位知识库 rerank"（与线上 18275a06 一致）
  2. 给旧应用 69fa1c02 改名，标注站点已弃用
  3. 打印两个站点的当前状态
"""
import json, os, ssl, sys, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
NEW = "38c3e937-b888-4564-bb2e-39f2520e28f3"
OLD = "69fa1c02-27bf-41fc-a7d2-0c068480c034"
TOK = token()
H = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def call(path, body=None, method=None, timeout=180):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method or ("POST" if data else "GET"), headers=H)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:300]
    except Exception as e:
        return -1, repr(e)


print("=== 1. 把新应用 draft 恢复为「只有岗位知识库 rerank」 ===")
st, body = call("/console/api/apps/%s/workflows/draft" % NEW)
draft = json.loads(body)
for n in draft["graph"]["nodes"]:
    if n["data"].get("type") != "knowledge-retrieval":
        continue
    c = n["data"].get("multiple_retrieval_config") or {}
    want = n["data"]["title"] == "岗位知识库"
    c.update({"enabled": True, "reranking_enable": want,
              "reranking_mode": "reranking_model" if want else "weighted_score",
              "reranking_model": {"provider": "openai_api_compatible", "model": "bge-reranker-v2-m3"},
              "top_k": 8 if want else 5, "retrieval_model": "multiple",
              "search_method": "hybrid_search", "score_threshold_enabled": True, "score_threshold": 0.1})
    if not want:
        c["weights"] = {"weight_type": "customized",
                        "vector_setting": {"vector_weight": 0.6, "embedding_provider_name": "", "embedding_model_name": ""},
                        "keyword_setting": {"keyword_weight": 0.4}}
    n["data"]["multiple_retrieval_config"] = c
    print("  %-8s rerank=%s top_k=%s" % (n["data"]["title"], c["reranking_enable"], c["top_k"]))
st, body = call("/console/api/apps/%s/workflows/draft" % NEW, {
    "graph": draft["graph"], "features": draft.get("features"),
    "environment_variables": draft.get("environment_variables") or {},
    "conversation_variables": draft.get("conversation_variables") or [],
    "hash": draft.get("hash")})
print("SAVE ->", st, body[:140])

print("\n=== 2. 旧应用改名（标注站点已弃用） ===")
st, body = call("/console/api/apps/%s" % OLD, {
    "name": "职引 · 校园就业智能体（旧版 · 站点已弃用）",
    "description": "简历诊断 · 岗位匹配 · 模拟面试 · 政策咨询。本应用的站点已弃用，正式站点见新应用。",
    "icon_type": "image", "icon": "ff8cb252-6223-4c43-9eb7-22844fd9adfa", "icon_background": ""},
    method="PUT")
print("PUT 旧应用 ->", st, body[:120])

print("\n=== 3. 两个应用状态 ===")
for tag, aid in [("新（正式）", NEW), ("旧（备份）", OLD)]:
    st, body = call("/console/api/apps/%s" % aid)
    a = json.loads(body)
    site = a.get("site") or {}
    print("%s  name=%s" % (tag, a.get("name")))
    print("     app_id=%s  workflow=%s  site_code=%s  enable_site=%s" %
          (aid, (a.get("workflow") or {}).get("id", "")[:8], site.get("access_token"), a.get("enable_site")))
