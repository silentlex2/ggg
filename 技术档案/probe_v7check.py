# -*- coding: utf-8 -*-
"""v7 站点专项核对：① 岗位库 rerank 是否仍生效（retriever_resources 形态）
② 实时政策源（HTTP 节点）是否仍在链路里 ③ 时效性政策问题是否引用实时数据

用法：python probe_v7check.py <站点码>
"""
import json, os, re, ssl, sys, time, urllib.request

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SITE = sys.argv[1] if len(sys.argv) > 1 else "j5qWmoi0m0UYWDpj"


def token():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def chat(tok, q, cid=""):
    body = json.dumps({"response_mode": "streaming", "conversation_id": cid, "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    req = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    ans, cid2, chain, rr, failed = "", cid, [], [], []
    t0 = time.time()
    with urllib.request.urlopen(req, context=CTX, timeout=400) as r:
        raw = r.read().decode("utf-8", "replace")
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"): continue
        try: j = json.loads(blk[5:].strip())
        except Exception: continue
        e = j.get("event"); d = j.get("data") or {}
        if e == "message": ans += j.get("answer", "")
        elif e == "message_end":
            cid2 = j.get("conversation_id") or cid
            rr = (j.get("metadata") or {}).get("retriever_resources") or []
        elif e == "node_finished":
            chain.append(d.get("title"))
            if d.get("status") == "failed": failed.append(d.get("title"))
    return ans, cid2, chain, rr, failed, time.time() - t0


tok = token()
print("站点:", SITE, "| token OK")

# ① 岗位库 rerank
ans, _, chain, rr, fail, cost = chat(tok, "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位")
sc = [round((x.get("score") or 0), 4) for x in rr]
docs = sorted({(x.get("document_name") or "")[:22] for x in rr})
print("\n" + "=" * 74)
print("① 岗位匹配检索形态  %.1fs  条数=%d" % (cost, len(rr)))
print("=" * 74)
print("  scores:", sc)
print("  docs  :", docs)
if sc:
    mx = max(sc)
    print("  形态判定:", "reranker 分（max %.3f > 0.75）" % mx if mx > 0.75 else "加权混合分（max %.3f 落在 0.3–0.6）" % mx)
print("  节点链:", " → ".join(chain))
print("  失败节点:", fail or "无")

# ②③ 实时政策源
ans2, _, chain2, _, fail2, cost2 = chat(tok, "最近有什么新的就业政策动态吗")
print("\n" + "=" * 74)
print("②③ 实时政策源  %.1fs" % cost2)
print("=" * 74)
print("  节点链:", " → ".join(chain2))
print("  链路含实时政策源:", "✅" if "实时政策源" in chain2 else "❌")
print("  回答前 700 字:\n" + ans2[:700])
dates = re.findall(r"20\d\d-\d\d-\d\d", ans2)
print("\n  出现的发布日期:", dates or "无")
print("  引用来源含 ncss:", "✅" if "ncss" in ans2 else "❌")
print("  失败节点:", fail2 or "无")
print("\n（完）")
