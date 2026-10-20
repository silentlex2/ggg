#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rerank 可行性实验（第二步）：对已复制的新应用统一配置 → 发布 → 测检索质量。

用法：python probe_clone_rerank.py [新应用ID]
默认读取 scratch/rerank-app.txt。
"""
import json, os, ssl, sys, time, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
TOK = token()
H = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
RK = {"provider": "openai_api_compatible", "model": "bge-reranker-v2-m3"}


def call(path, body=None, method=None, timeout=180, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method or ("POST" if data else "GET"),
                               headers=headers or H)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:400]
    except Exception as e:
        return -1, repr(e)


NEW = sys.argv[1] if len(sys.argv) > 1 else "38c3e937-b888-4564-bb2e-39f2520e28f3"
open(os.path.join(HERE, "scratch", "rerank-app.txt"), "w", encoding="utf-8").write(NEW)
print("新应用:", NEW)

print("\n=== 2. 检查并统一 rerank 配置 ===")
st, body = call("/console/api/apps/%s/workflows/draft" % NEW)
if st != 200:
    sys.exit("取 draft 失败 %d %s" % (st, body[:300]))
draft = json.loads(body)
for n in draft["graph"]["nodes"]:
    if n["data"].get("type") != "knowledge-retrieval":
        continue
    c = n["data"].get("multiple_retrieval_config") or {}
    print("  改前 [%-8s] rerank=%-5s top_k=%s" % (n["data"]["title"], c.get("reranking_enable"), c.get("top_k")))
    c.update({"enabled": True, "reranking_enable": True, "reranking_mode": "reranking_model",
              "reranking_model": dict(RK), "top_k": 8, "retrieval_model": "multiple",
              "search_method": "hybrid_search", "score_threshold_enabled": True, "score_threshold": 0.1})
    n["data"]["multiple_retrieval_config"] = c
st, body = call("/console/api/apps/%s/workflows/draft" % NEW, {
    "graph": draft["graph"], "features": draft.get("features"),
    "environment_variables": draft.get("environment_variables") or {},
    "conversation_variables": draft.get("conversation_variables") or [],
    "hash": draft.get("hash")})
print("SAVE ->", st, body[:160])

print("\n=== 3. 发布 ===")
st, body = call("/console/api/apps/%s/workflows/publish" % NEW, {})
print("PUBLISH ->", st, body[:220])
pub_wf = json.loads(body).get("workflow_id") if st == 200 else None

print("\n=== 4. 恢复图标与名称 ===")
st, body = call("/console/api/apps/%s" % NEW, {
    "name": "职引 · 校园就业智能体",
    "description": "简历诊断 · 岗位匹配 · 模拟面试 · 政策咨询，把就业中心的一对一辅导做成 7x24 小时可用的智能体",
    "icon_type": "image", "icon": ICON, "icon_background": ""}, method="PUT")
print("PUT app ->", st, body[:100])
st, body = call("/console/api/apps/%s" % NEW)
app = json.loads(body)
code = ((app.get("site") or {}).get("access_token")) or ""
print("新站点码:", repr(code))
if not code:
    sys.exit("新应用没有站点码")
open(os.path.join(HERE, "scratch", "rerank-site.txt"), "w", encoding="utf-8").write(code)

print("\n=== 5. 用新站点跑岗位匹配，验证 rerank 是否可用 ===")
r = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": code})
with urllib.request.urlopen(r, context=CTX, timeout=30) as resp:
    t = json.loads(resp.read().decode())["access_token"]
q = "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"
payload = {"response_mode": "streaming", "conversation_id": "", "query": q,
           "inputs": {"user_input": q}, "parent_message_id": None}
rq = urllib.request.Request(BASE + "/api/chat-messages", data=json.dumps(payload).encode(), method="POST",
                            headers={"Content-Type": "application/json", "X-App-Code": code,
                                     "authorization": "Bearer " + t, "auth-token": "Bearer " + t})
t0 = time.time()
with urllib.request.urlopen(rq, context=CTX, timeout=300) as resp:
    raw = resp.read().decode("utf-8", "replace")
wid, rr, failed, ans = None, [], [], ""
for blk in raw.replace("\r\n", "\n").split("\n\n"):
    if not blk.startswith("data:"):
        continue
    try:
        j = json.loads(blk[5:].strip())
    except Exception:
        continue
    ev = j.get("event")
    if ev == "message":
        ans += j.get("answer", "")
    if ev == "workflow_finished":
        wid = j.get("data", {}).get("workflow_id")
    if ev == "node_finished" and j.get("data", {}).get("status") == "failed":
        failed.append((j["data"].get("title"), str(j["data"].get("error"))[:150]))
    if ev == "message_end":
        rr = ((j.get("data") or {}).get("metadata") or {}).get("retriever_resources") or []
print("线上 workflow_id = %s" % wid)
print("刚发布的是       = %s" % pub_wf)
print("失败节点:", failed or "无")
print("retriever_resources = %d 条  耗时 %.1fs" % (len(rr), time.time() - t0))
for i, it in enumerate(rr):
    print("  [%d] score=%.6f  %s" % (i, it.get("score") or 0, (it.get("content") or "")[:140].replace("\n", " ")))
print("\n--- 回答前 600 字 ---")
print(ans[:600])
