# -*- coding: utf-8 -*-
"""知识库线上实检（kb_live_check.py）

为什么要有：巡检只看"答得对不对"，看不出"知识库到底有没有被检索到"——
模型完全可能凭常识把岗位匹配答得像模像样，而检索节点其实一条没命中。
自建知识库是评分项之一，所以这里直接读 stream 里 node_finished 的检索结果，
以及 message_end 顶层的 retriever_resources，两头互相印证。

用法：
    python kb_live_check.py           # 详细输出
    python kb_live_check.py --quiet   # 只打判定与契约（给 run_all.py 调）

判定：
  - 检索命中 ≥ 3 条（低于 3 说明索引/绑定出问题）
  - 最高分 ≥ 0.75（低于这个基本是"加权混合分"兜底，rerank 没生效）
  - 节点输出若给了结果，则与 retriever_resources 不矛盾（该 fork 目前 outputs 为空，视为未知）
  - 命中文档里必须出现 KB4 或 KB3（岗位库 / 专业对照库）

输出契约：
    ---KB---
    KB_HITS: 5
    KB_TOP_SCORE: 0.9903
    KB_DATASETS: KB4-岗位JD库（知识库版）.md|KB3-专业行业岗位对照库.md
    KB_CHARS: 838
    KB_OK: yes
    ---END---

退出码：0 = 通过；1 = 不通过；2 = 站点/接口异常。
"""
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
QUIET = "--quiet" in sys.argv[1:]

MIN_HITS = 3
MIN_SCORE = 0.75
MIN_CHARS = 200
WANT_KB = ("KB4", "KB3")

Q = "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位"


def log(*a):
    if not QUIET:
        print(*a)


def site():
    env = os.environ.get("SITE", "").strip()
    if env:
        return env
    with open(os.path.join(HERE, "readysite.txt"), encoding="utf-8") as f:
        return f.read().strip()


def passport(code):
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": code})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def main():
    code = site()
    if not code:
        print("readysite.txt 为空")
        return 2
    try:
        tok = passport(code)
        payload = {"response_mode": "streaming", "conversation_id": "", "query": Q,
                   "inputs": {"user_input": Q}, "parent_message_id": None}
        req = urllib.request.Request(BASE + "/api/chat-messages",
                                     data=json.dumps(payload).encode(), method="POST",
                                     headers={"Content-Type": "application/json",
                                              "X-App-Code": code,
                                              "authorization": "Bearer " + tok,
                                              "auth-token": "Bearer " + tok})
        with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
            raw = r.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as e:
        print("接口异常：%r" % (e,))
        return 2

    node_hits, answer, resources = None, [], []
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:  # noqa: BLE001
            continue
        ev = j.get("event")
        if ev == "node_finished":
            d = j.get("data", {})
            title = d.get("title") or ""
            if "知识" in title or "检索" in title:
                outs = d.get("outputs") or {}
                res = outs.get("result") or outs.get("result_str") or []
                # 实测：这个 fork 的检索节点在 node_finished 里 outputs 是空 dict，
                # 拿不到命中条目。所以只在真拿到 list 时才当信号，拿不到就留 None（未知），
                # 不能把"没给"当成"没命中"——那是把平台实现细节当成产品结论。
                if isinstance(res, list) and res:
                    node_hits = len(res)
                    log("▶ 节点 %-12s status=%s 命中=%d" % (title, d.get("status"), len(res)))
                    for it in res[:3]:
                        log("     score=%s doc=%s" % (it.get("score"), (it.get("title") or "")[:30]))
        elif ev == "message_end":
            # 注意：retriever_resources 在 message_end 的**顶层** metadata 里，
            # data 是空 dict（技术档案/README 记过这个坑，取错地方会永远 0 条）
            md = j.get("metadata") or (j.get("data") or {}).get("metadata") or {}
            resources = md.get("retriever_resources") or []
        elif ev == "message":
            answer.append(j.get("answer") or "")

    text = "".join(answer)
    scores = [float(r.get("score") or 0) for r in resources]
    top = max(scores) if scores else 0.0
    names = []
    for r in resources:
        n = r.get("dataset_name") or r.get("document_name") or ""
        if n and n not in names:
            names.append(n)

    log("")
    log("retriever_resources %d 条，最高分 %.4f" % (len(resources), top))
    log("命中文档：%s" % ("、".join(names) or "（无）"))
    log("回答 %d 字" % len(text))
    if not QUIET:
        log(text[:600])

    problems = []
    if len(resources) < MIN_HITS:
        problems.append("检索只命中 %d 条（要求 ≥%d）" % (len(resources), MIN_HITS))
    if top and top < MIN_SCORE:
        problems.append("最高分 %.4f 低于 %.2f：多半 rerank 没生效" % (top, MIN_SCORE))
    if node_hits is not None and node_hits == 0 and resources:
        problems.append("节点输出 0 条但 retriever_resources 有 %d 条：解析位置可能变了" % len(resources))
    if not any(any(k in n for k in WANT_KB) for n in names):
        problems.append("命中文档里没有 KB3/KB4（岗位库没检索到）：%s" % (names or "无"))
    if len(text) < MIN_CHARS:
        problems.append("回答仅 %d 字（要求 ≥%d）" % (len(text), MIN_CHARS))

    for p in problems:
        print("  FAIL  %s" % p)
    if not problems:
        print("  知识库实检通过：%d 条命中，最高分 %.4f" % (len(resources), top))

    print("")
    print("---KB---")
    print("KB_HITS: %d" % len(resources))
    print("KB_TOP_SCORE: %.4f" % top)
    print("KB_DATASETS: %s" % ("|".join(names) or "-"))
    print("KB_CHARS: %d" % len(text))
    print("KB_OK: %s" % ("no" if problems else "yes"))
    print("---END---")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())