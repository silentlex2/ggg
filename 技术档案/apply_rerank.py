#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给知识库检索节点启用 rerank 重排模型（先只改岗位知识库做验证）。

用法：
    python apply_rerank.py            # 只改「岗位知识库」，发布并验证
    python apply_rerank.py --all      # 四个知识库节点一起改
    python apply_rerank.py --rollback <备份文件>
"""
import json, os, ssl, sys, time, urllib.request, urllib.error
sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
BK = os.path.join(HERE, "scratch", "backup-20261014")
APP = "69fa1c02-27bf-41fc-a7d2-0c068480c034"
SITE = open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()
TOK = open(os.path.join(HERE, "scratch", ".token"), encoding="utf-8").read().strip()
H = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

RK = {"provider": "openai_api_compatible", "model": "bge-reranker-v2-m3"}
KR_NODES = {
    "1791547535170": "知识库",
    "1791552000010": "岗位知识库",
    "1791552000020": "面试题库",
    "1791552000030": "政策知识库",
}


def api(path, body=None, method=None, timeout=120, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method or ("POST" if data else "GET"),
                               headers=headers or H)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:500]
    except Exception as e:
        return -1, repr(e)


def save_and_publish(draft, tag):
    st, out = api("/console/api/apps/%s/workflows/draft" % APP, {
        "graph": draft["graph"], "features": draft.get("features"),
        "environment_variables": draft.get("environment_variables") or {},
        "conversation_variables": draft.get("conversation_variables") or [],
        "hash": draft.get("hash")}, timeout=180)
    print("SAVE  -> %d %s" % (st, out[:200]))
    st2, out2 = api("/console/api/apps/%s/workflows/publish" % APP, {}, timeout=180)
    print("PUBLISH -> %d %s" % (st2, out2[:300]))
    return st, st2


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--rollback":
        draft = json.load(open(sys.argv[2], encoding="utf-8"))
        print("回滚到", sys.argv[2])
        save_and_publish(draft, "rollback")
        return

    all_nodes = "--all" in sys.argv
    st, body = api("/console/api/apps/%s/workflows/draft" % APP, timeout=180)
    if st != 200:
        sys.exit("取 draft 失败 %d %s" % (st, body[:300]))
    draft = json.loads(body)
    os.makedirs(BK, exist_ok=True)
    bpath = os.path.join(BK, "prod-draft-v4-before-rerank.json")
    with open(bpath, "w", encoding="utf-8") as f:
        json.dump(draft, f, ensure_ascii=False)
    print("已备份:", bpath)

    targets = KR_NODES if all_nodes else {"1791552000010": "岗位知识库"}
    changed = 0
    for n in draft["graph"]["nodes"]:
        nid = n.get("id")
        if nid not in targets:
            continue
        d = n["data"]
        cfg = d.get("multiple_retrieval_config") or {}
        print("\n[%s] 改前: rerank=%s mode=%s top_k=%s score_th=%s" %
              (d.get("title"), cfg.get("reranking_enable"), cfg.get("reranking_mode"),
               cfg.get("top_k"), cfg.get("score_threshold")))
        cfg["reranking_enable"] = True
        cfg["reranking_mode"] = "reranking_model"
        cfg["reranking_model"] = dict(RK)
        cfg["top_k"] = 8
        cfg.setdefault("retrieval_model", "multiple")
        cfg.setdefault("search_method", "hybrid_search")
        cfg.setdefault("score_threshold_enabled", True)
        cfg.setdefault("score_threshold", 0.1)
        cfg["enabled"] = True
        d["multiple_retrieval_config"] = cfg
        changed += 1
        print("[%s] 改后: rerank=%s mode=%s model=%s top_k=%s" %
              (d.get("title"), cfg.get("reranking_enable"), cfg.get("reranking_mode"),
               cfg.get("reranking_model"), cfg.get("top_k")))
    if not changed:
        sys.exit("没有匹配到节点，未保存")
    save_and_publish(draft, "rerank")
    print("\n改完。下一步：python probe_kb.py 验证检索排序。")


if __name__ == "__main__":
    main()
