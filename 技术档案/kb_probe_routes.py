# -*- coding: utf-8 -*-
"""探明数据集相关路由：哪些路径可用、返回什么，定位知识库读写入口。"""
import json
import ssl
import sys
import urllib.error
import urllib.request

from tok import token

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://aiagent.cqut.edu.cn:31134"
TOK = token()
HDR = {"Authorization": "Bearer " + TOK, "OperToken": TOK, "Content-Type": "application/json"}
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
DS = "9178aa02c3d811f1be159fcedc704656"


def call(path, body=None, method=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=HDR,
                                method=method or ("POST" if data is not None else "GET"))
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=90) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")[:180]
    except Exception as exc:  # noqa: BLE001
        return -1, repr(exc)


CASES = [
    ("GET", "/console/api/datasets/%s" % DS, None),
    ("GET", "/console/api/datasets/%s/documents?page=1&limit=5" % DS, None),
    ("GET", "/console/api/datasets/%s/process-documents" % DS, None),
    ("GET", "/console/api/datasets?page=1&limit=100&keyword=" % (), None),
    ("GET", "/console/api/datasets?page=1&limit=100&include_all=true" % (), None),
    ("GET", "/console/api/datasets/retrieval?page=1&limit=20" % (), None),
    ("POST", "/console/api/datasets/%s/hit-testing" % DS,
     {"query": "化工工艺工程师 重庆", "retrieval_model": {"search_method": "hybrid_search", "reranking_enable": False,
      "reranking_model": {"provider": "openai_api_compatible", "model": "bge-reranker-v2-m3"},
      "weights": {"weight_type": "customized",
                  "vector_setting": {"vector_weight": 0.6, "embedding_provider_name": "", "embedding_model_name": ""},
                  "keyword_setting": {"keyword_weight": 0.4}},
      "top_k": 3, "score_threshold_enabled": False}}),
]

for method, path, body in CASES:
    st, out = call(path, body, method)
    print("[%s] %s %s" % (st, method, path))
    print("     " + out[:320].replace("\n", " "))
    print("")
