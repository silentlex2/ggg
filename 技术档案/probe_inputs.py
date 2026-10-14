# -*- coding: utf-8 -*-
"""探测：岗位匹配节点的检索注入方式 + 各 LLM 节点的变量引用。"""
import json, os, ssl, urllib.request
BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

nd = json.load(open(os.path.join(HERE, "scratch", "draft.json"), encoding="utf-8"))["graph"]["nodes"]

print("== 岗位匹配节点检索注入方式 ==")
job = [n for n in nd if n["id"] == "1791552000011"][0]
print("dataset_configs:", json.dumps(job["data"].get("dataset_configs"), ensure_ascii=False)[:900])
print("database_configs:", json.dumps(job["data"].get("database_configs"), ensure_ascii=False)[:200])

print()
print("== 4 个知识库检索节点的 query 变量 ==")
for n in nd:
    if n["data"].get("type") != "knowledge-retrieval": continue
    d = n["data"]
    mrc = d.get("multiple_retrieval_config") or {}
    print("  %-16s query=%-42s rerank=%-5s top_k=%s" % (d["title"][:14], d.get("query_variable_selector"), mrc.get("reranking_enable"), mrc.get("top_k")))

print()
print("== 各 LLM 节点 prompt 里的变量引用 ==")
for n in nd:
    if n["data"].get("type") != "llm": continue
    t = "\n".join(x.get("text", "") for x in n["data"].get("prompt_template", []))
    refs = [r for r in ["{{#sys.query#}}", "{{sys.query}}", "{{#sys.files#}}", "{{user_major}}", "{{user_skills}}", "{{#1791544765658.text#}}"] if r in t]
    print("  %-16s len=%-5d refs=%s" % (n["data"]["title"][:12], len(t), refs or "无"))

print()
print("== 9 个参数提取节点 ==")
for n in nd:
    if n["data"].get("type") != "parameter-extractor": continue
    d = n["data"]
    print("  %-16s query=%-34s params=%s" % (d["title"][:14], json.dumps(d.get("query"), ensure_ascii=False), [p["name"] for p in d.get("parameters", [])]))
