#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""岗位知识库检索诊断：直接用不同检索式跑同一节点，看命中情况。

用法：python probe_retrieval.py
"""
import json, os, ssl, sys, urllib.request, urllib.error
from tok import token  # 控制台 token 统一入口（见 tok.py）
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
APP = "69fa1c02-27bf-41fc-a7d2-0c068480c034"
NODE_JOB = "1791552000010"   # 岗位知识库
NODE_PE = "1791600000030"    # 求职意向提取
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
TOK = token()
H = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}


def run_node(nid, body, timeout=180):
    req = urllib.request.Request(BASE + "/console/api/apps/" + APP + "/workflows/draft/nodes/" + nid + "/run",
                                 data=json.dumps(body).encode(), method="POST", headers=H)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return -1, repr(e)


def main():
    print("=" * 78)
    print("A. 求职意向提取节点 —— 对同一句话抽出来的检索式")
    print("=" * 78)
    user_says = [
        "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位",
        "我想找化工工艺工程师的岗位",
    ]
    for q in user_says:
        for body in [{"sys.query": q}, {"query": q}]:
            st, out = run_node(NODE_PE, body)
            print("\n[输入] %s\n[body %s] -> %d\n%s" % (q, list(body)[0], st, out[:900]))

    print("\n" + "=" * 78)
    print("B. 岗位知识库节点 —— 不同检索式的命中情况")
    print("=" * 78)
    queries = [
        "化学工程与工艺 重庆 大四 化工类 校招 Aspen Plus",
        "化工工艺工程师 重庆 校招",
        "化工 重庆",
        "机械设计制造及其自动化 重庆 校招",
    ]
    for q in queries:
        for body in [{NODE_PE + ".retrieval_query": q}, {"retrieval_query": q}, {"query": q}]:
            st, out = run_node(NODE_JOB, body)
            tag = list(body)[0]
            try:
                j = json.loads(out)
                res = j.get("data", j).get("result") if isinstance(j.get("data", j), dict) else None
                txt = json.dumps(j, ensure_ascii=False)
            except Exception:
                txt = out
            print("\n[检索式] %s\n  [body %s] -> %d  %d 字节" % (q, tag, st, len(txt)))
            print("  " + txt[:500].replace("\n", " "))
            if st == 200:
                break


if __name__ == "__main__":
    main()
