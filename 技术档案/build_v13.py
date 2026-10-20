# -*- coding: utf-8 -*-
"""v13 图改造：删 6 个「正文提取」节点、给 LLM 设 max_tokens、调检索与 HTTP 超时。

设计原则：
  * 纯函数（patch_graph 只吃图、吐图），可离线跑、可单测，不碰网络。
  * 每一步改动都写进 report，便于人工复查「到底改了什么」。
  * 改完做图完整性断言：不能留悬空边、不能留引用已删节点的变量、answer 节点必须能取到上游。

用法：
    python build_v13.py --local <draft.json> --out <patched.json>   # 只做离线改造与校验
    python build_v13.py --apply --name "职引 v13"                     # 真实执行（需 CONSOLE_TOKEN）
"""
import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

SRC_APP = "0c194407-f53c-4f7b-82df-2a2446b5ecfa"   # v12 正式站（草稿即 v12）

# LLM 节点 -> 它下游的「正文提取」-> 再下游的「回复」
BRANCHES = [
    ("1791552000031", "1791600100001", "1791552000033", "政策顾问"),
    ("1791552000021", "1791600100005", "1791552000023", "模拟面试官"),
    ("1791552000011", "1791600100004", "1791552000013", "岗位匹配"),
    ("1791552000001", "1791600100003", "1791552000003", "提示上传简历"),
    ("1791550106443", "1791600100002", "1791552000040", "大模型（简历诊断）"),
    ("1791600000001", "1791600100006", "1791600000003", "闲聊引导"),
]

# 显式 max_tokens：按分支最长答案定，留 15% 余量（原值全部未设，靠平台默认，实测会截断）
MAX_TOKENS = {
    "1791552000031": 1600,   # 政策顾问：实测 1900 字答案
    "1791552000021": 1400,   # 模拟面试官：复盘 + 追问预演
    "1791552000011": 1100,   # 岗位匹配：实测 1000 字左右
    "1791550106443": 1400,   # 简历诊断：四维报告
    "1791552000001": 400,    # 提示上传简历：短话术
    "1791600000001": 600,    # 闲聊引导
}

JOB_KB = "1791552000010"     # 岗位知识库（唯一开 rerank 的检索节点）
JOB_TOP_K = 5                # 原 8，实测检索 3.4s，降到 5
HTTP_NODE = "1791600200001"  # 实时政策源
HTTP_TIMEOUT = 6             # 原 15/15/15，外网抖动时会拖死政策分支


def patch_graph(graph, keep_extractors=False):
    """返回 (新图, 变更报告列表)。keep_extractors=True 时只改模型与参数，不删节点。"""
    report = []
    nodes = list(graph.get("nodes") or [])
    edges = list(graph.get("edges") or [])
    byid = {n["id"]: n for n in nodes}

    for llm_id, ext_id, ans_id, title in BRANCHES:
        for nid in (llm_id, ext_id, ans_id):
            if nid not in byid:
                raise SystemExit("图里找不到节点 %s（%s）" % (nid, title))

    # ---- 1. 删「正文提取」并直连 ----
    if not keep_extractors:
        drop = {ext for _, ext, _, _ in BRANCHES}
        kept_edges, added = [], []
        for e in edges:
            if e["source"] in drop or e["target"] in drop:
                if e["source"] in drop:
                    continue                      # 正文提取 -> 回复 这一段丢掉（下面重建）
                if e["target"] in drop:
                    # LLM -> 正文提取：改指向该分支的回复节点
                    ans = next(a for l, x, a, _ in BRANCHES if x == e["target"])
                    ne = dict(e)
                    ne["target"] = ans
                    kept_edges.append(ne)
                    added.append((e["source"], e["target"], ans))
                    continue
            kept_edges.append(e)
        edges = kept_edges
        nodes = [n for n in nodes if n["id"] not in drop]
        byid = {n["id"]: n for n in nodes}
        for src, old, new in added:
            report.append("重连 %s -> %s（原经 %s）" % (src, new, old))

        for llm_id, ext_id, ans_id, title in BRANCHES:
            ans = byid[ans_id]["data"]
            ans["answer"] = "{{#%s.text#}}" % llm_id
            ans["variables"] = [{"value_selector": [llm_id, "text"], "variable": "output"}]
            report.append("改结论变量 %s：{{#%s.body#}} -> {{#%s.text#}}" % (title, ext_id, llm_id))

    # ---- 2. 显式 max_tokens ----
    for nid, mt in MAX_TOKENS.items():
        d = byid[nid]["data"]
        cp = dict((d.get("model") or {}).get("completion_params") or {})
        old = cp.get("max_tokens")
        cp["max_tokens"] = mt
        d["model"]["completion_params"] = cp
        report.append("max_tokens %s：%s -> %s" % (d.get("title"), old, mt))

    # ---- 3. 岗位知识库 top_k ----
    if JOB_KB in byid:
        cfg = byid[JOB_KB]["data"].get("multiple_retrieval_config") or {}
        old = cfg.get("top_k")
        cfg["top_k"] = JOB_TOP_K
        byid[JOB_KB]["data"]["multiple_retrieval_config"] = cfg
        report.append("岗位知识库 top_k：%s -> %s" % (old, JOB_TOP_K))

    # ---- 4. HTTP 超时 ----
    if HTTP_NODE in byid:
        d = byid[HTTP_NODE]["data"]
        old = d.get("timeout")
        d["timeout"] = {"max_connect_timeout": HTTP_TIMEOUT,
                        "max_read_timeout": HTTP_TIMEOUT,
                        "max_write_timeout": HTTP_TIMEOUT}
        report.append("实时政策源超时：%s -> %ss" % (json.dumps(old, ensure_ascii=False), HTTP_TIMEOUT))

    graph["nodes"] = nodes
    graph["edges"] = edges
    validate(graph)
    return graph, report


def validate(graph):
    """图完整性断言：悬空边、重复 id、answer 变量引用、节点连通性。"""
    nodes = {n["id"]: n for n in graph["nodes"]}
    if len(nodes) != len(graph["nodes"]):
        raise SystemExit("节点 id 重复")
    ids = set(nodes)
    for e in graph["edges"]:
        if e["source"] not in ids or e["target"] not in ids:
            raise SystemExit("悬空边：%s -> %s" % (e["source"], e["target"]))
    for nid, n in nodes.items():
        d = n.get("data") or {}
        if d.get("type") == "answer":
            sel = [v.get("value_selector") for v in (d.get("variables") or [])]
            for s in sel:
                if not s or s[0] not in ids:
                    raise SystemExit("回复节点 %s 的变量指向已删节点：%s" % (nid, s))
            if "{{#" in (d.get("answer") or ""):
                import re
                for ref in re.findall(r"\{\{#([0-9a-zA-Z_]+)\.", d.get("answer") or ""):
                    if ref not in ids and ref != "sys":
                        raise SystemExit("回复节点 %s 模板引用了已删节点 %s" % (nid, ref))


# ---------------------------------------------------------------- 真实执行
def tok():
    t = os.environ.get("CONSOLE_TOKEN", "").strip()
    if t:
        return t
    raise SystemExit("需要 CONSOLE_TOKEN")


def api(path, method="GET", body=None):
    t = tok()
    h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw[:300]


def apply(name, keep_extractors=False, app_id=None):
    if app_id:
        new_app = app_id
        print("== 1. 复用已有应用（%s），跳过复制 ==" % new_app)
    else:
        print("== 1. 复制源应用（%s）==" % SRC_APP)
        s, j = api("/console/api/apps/%s/copy" % SRC_APP, "POST",
                   {"name": name, "icon_type": None, "icon": None,
                    "icon_background": None, "mode": "advanced-chat"})
        if s not in (200, 201):          # 本 fork 的 copy 返回 201 Created
            raise SystemExit("复制失败 %s %s" % (s, j))
        new_app = j["id"]
        print("   新应用 =", new_app, "| 站点码 =", ((j.get("site") or {}).get("code")))

    print("== 2. 拉新应用草稿 ==")
    s, draft = api("/console/api/apps/%s/workflows/draft" % new_app)
    print("   hash=%s nodes=%d edges=%d" % (draft.get("hash"),
          len(draft["graph"]["nodes"]), len(draft["graph"]["edges"])))

    print("== 3. 改造图 ==")
    graph, report = patch_graph(draft["graph"], keep_extractors=keep_extractors)
    for line in report:
        print("   -", line)
    print("   改造后 nodes=%d edges=%d" % (len(graph["nodes"]), len(graph["edges"])))

    print("== 4. 保存草稿 ==")
    body = {"graph": graph, "viewport": draft.get("viewport"),
            "features": draft.get("features"),
            "environment_variables": draft.get("environment_variables"),
            "conversation_variables": draft.get("conversation_variables")}
    s, r = api("/console/api/apps/%s/workflows/draft" % new_app, "POST", body)
    print("   save ->", s)
    if s != 200:
        raise SystemExit("保存草稿失败：%s %s" % (s, r))
    s, chk = api("/console/api/apps/%s/workflows/draft" % new_app)
    got = len(chk["graph"]["nodes"])
    print("   复查 nodes=%d（期望 %d）" % (got, len(graph["nodes"])))
    if got != len(graph["nodes"]):
        raise SystemExit("保存后节点数不符")

    print("== 5. 发布 ==")
    s, pub = api("/console/api/apps/%s/workflows/publish" % new_app, "POST",
                 {"marked_name": "", "marked_comment": "v13 去掉 6 个正文提取节点 + max_tokens + 检索/超时调优"})
    wf = (pub or {}).get("id") or (pub or {}).get("workflow_id")
    print("   publish ->", s, "workflow:", wf)
    if s != 200:
        raise SystemExit("发布失败")

    print("== 6. 开站点 ==")
    s, _ = api("/console/api/apps/%s/site-enable" % new_app, "POST", {"enable_site": True})
    print("   site-enable ->", s)
    s, a = api("/console/api/apps/%s" % new_app)
    code = (a.get("site") or {}).get("code")
    print("   SITE =", code, "| app wf =", (a.get("workflow") or {}).get("id"))

    print("== 7. 等站点生效 ==")
    for i in range(12):
        time.sleep(10)
        try:
            req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": code})
            with urllib.request.urlopen(req, context=CTX, timeout=20) as r:
                if r.status == 200:
                    print("   第 %d 次探测：站点已可访问" % (i + 1))
                    break
        except Exception as e:
            print("   第 %d 次探测：%s" % (i + 1, e))

    print()
    print("NEW_APP =", new_app)
    print("SITE    =", code)
    print("URL     = https://aiagent.cqut.edu.cn:31134/chat/%s" % code)
    with open(os.path.join(HERE, "v13-result.json"), "w", encoding="utf-8") as f:
        json.dump({"app": new_app, "site": code, "workflow": wf,
                   "keep_extractors": keep_extractors, "report": report}, f,
                  ensure_ascii=False, indent=1)
    return new_app, code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local")
    ap.add_argument("--out")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--name", default="职引 · 校园就业智能体 v13")
    ap.add_argument("--app", help="复用已创建的应用（跳过复制），用于失败后续跑")
    ap.add_argument("--keep-extractors", action="store_true",
                    help="保留 6 个正文提取节点，只改 max_tokens / 检索 / 超时（think 泄漏时的退路）")
    a = ap.parse_args()
    if a.local:
        d = json.load(open(a.local, encoding="utf-8"))
        graph, report = patch_graph(d["graph"], a.keep_extractors)
        for line in report:
            print("-", line)
        print("nodes=%d edges=%d" % (len(graph["nodes"]), len(graph["edges"])))
        if a.out:
            d["graph"] = graph
            json.dump(d, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("written", a.out)
        return 0
    if a.apply:
        apply(a.name, a.keep_extractors, a.app)
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
