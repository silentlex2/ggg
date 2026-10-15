# -*- coding: utf-8 -*-
"""职引 黄金集评估（golden-set eval）。

设计对标：
  - career-ops evals/README.md：指标是"与参考标签的一致度"，不是绝对正确性；
    archetype 是门（可复现），score 只作容差带信号；用例刻意偏向边界。
  - gov_rag docs/EVAL_DATASET_README.md：30 条 = 27 可回答 + 3 无答案/拒答；
    题型分散，不能只考某一类，否则天然偏向某一种检索方式。

用法：
    python eval_golden.py [站点码] [--json 输出路径] [--only 意图,边界]

输出末尾固定契约（可被其它脚本 grep）：
    ---SCORE_SUMMARY---
    SCORE: 0.850
    ---END---

退出码：0 = SCORE >= 0.80；1 = 低于阈值（用作回归门）。
"""
import json, re, ssl, sys, time, urllib.request, urllib.error

BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

ARGS = list(sys.argv[1:])
SITE = ARGS[0] if ARGS and not ARGS[0].startswith("--") else "HeYM5jZOBsKPURdj"
JSON_OUT = ARGS[ARGS.index("--json") + 1] if "--json" in ARGS else None
ONLY = set(ARGS[ARGS.index("--only") + 1].split(",")) if "--only" in ARGS else None

# 路由签名正则：反推模型实际走了哪条分支（不依赖模型自述）
ROUTE_SIGN = {
    "简历诊断": r"简历诊断报告|分项得分|综合算式|要求—证据矩阵|结构化诊断",
    "岗位匹配": r"岗位匹配建议|匹配理由",
    "模拟面试": r"第 1 题|面试进度|模拟面试复盘",
    "政策咨询": r"政策解答|办理流程",
    "闲聊": r"接待助手|接下来你可以",
}


def route_of(ans):
    best, pos = None, 10 ** 9
    for r, pat in ROUTE_SIGN.items():
        m = re.search(pat, ans)
        if m and m.start() < pos:
            best, pos = r, m.start()
    return best or "未识别"


# 黄金集：20 条 = 16 可回答 + 4 拒答/边界，刻意偏向边界。
GOLDEN = [
    # A 组 明确意图（5）
    dict(id="A1", cat="意图", q="帮我看看我的简历有什么问题", route="简历诊断",
         must=["简历", "上传"], must_not=[]),
    dict(id="A2", cat="意图", q="我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位",
         route="岗位匹配", must=["岗位", "重庆"], must_not=[]),
    dict(id="A3", cat="意图", q="我想模拟面试，目标岗位是化工工艺工程师", route="模拟面试",
         must=["第 1 题", "进度"], must_not=[]),
    dict(id="A4", cat="意图", q="重庆应届生有哪些就业补贴可以领", route="政策咨询",
         must=["补贴"], must_not=[]),
    dict(id="A5", cat="意图", q="你好", route="闲聊",
         must=["简历", "岗位", "面试", "政策"], must_not=[]),
    # B 组 边界 / 易混（8）
    dict(id="B1", cat="边界", q="简历里的项目经历怎么写才好看", route=None,
         must=["简历"], must_not=[]),
    dict(id="B2", cat="边界", q="面试被问到期望薪资应该怎么答", route=None,
         must=["面试"], must_not=[]),
    dict(id="B3", cat="边界", q="三方协议怎么签", route="政策咨询",
         must=["三方"], must_not=[]),
    dict(id="B4", cat="边界", q="帮我投递简历吧", route=None,
         must=["简历"], must_not=["已经帮你投递", "已投递成功"]),
    dict(id="B5", cat="边界", q="今天天气怎么样", route="闲聊",
         must=["简历"], must_not=[]),
    dict(id="B6", cat="边界", q="我是学会计的，能帮我匹配审计岗位吗", route="岗位匹配",
         must=["会计"], must_not=[]),
    dict(id="B7", cat="边界", q="重庆的就业见习补贴是多少", route="政策咨询",
         must=["见习"], must_not=[]),
    dict(id="B8", cat="边界", q="来一场面试", route="模拟面试",
         must=["第 1 题", "进度"], must_not=[]),
    # C 组 拒答 / 能力边界（4）
    dict(id="C1", cat="拒答", q="试用期最长多久", route="政策咨询",
         must=["12333", "就业指导中心"], must_not=[]),
    dict(id="C2", cat="拒答", q="美国 OPT 签证怎么申请", route=None,
         must=[], must_not=["你可以去问政策咨询"]),
    dict(id="C3", cat="拒答", q="帮我直接写一份简历", route=None,
         must=[], must_not=["这是为你写好的简历", "以下是一份完整的简历正文"]),
    dict(id="C4", cat="拒答", q="你能保证我拿到 offer 吗", route=None,
         must=[], must_not=["保证你拿到 offer", "一定能拿到 offer"]),
    # D 组 异常输入（3）
    dict(id="D1", cat="异常", q="\u3000\u3000", route=None,
         must=["简历", "岗位"], must_not=[]),
    dict(id="D2", cat="异常", q="？？？", route=None,
         must=["简历", "岗位"], must_not=[]),
    dict(id="D3", cat="异常", q="简历" * 200, route=None, must=[], must_not=[]),
]

if ONLY:
    GOLDEN = [g for g in GOLDEN if g["cat"] in ONLY]


def passport():
    r = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(r, context=CTX, timeout=30) as resp:
        return json.loads(resp.read().decode())["access_token"]


def ask(q, tok, cid=""):
    body = json.dumps({"response_mode": "streaming", "conversation_id": cid, "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    r = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=400) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return "[HTTP %d] %s" % (e.code, e.read().decode("utf-8", "replace")[:200])
    ans = ""
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        if j.get("event") == "message":
            ans += j.get("answer", "")
    return ans


def main():
    print("=" * 78)
    print("职引 黄金集评估   站点 %s   用例 %d 条" % (SITE, len(GOLDEN)))
    print("=" * 78)
    tok = passport()
    rows = []
    t0 = time.time()
    for g in GOLDEN:
        a = ask(g["q"], tok)
        got = route_of(a)
        route_ok = (g["route"] is None) or (got == g["route"])
        miss = [k for k in g["must"] if k not in a]
        bad = [k for k in g["must_not"] if k in a]
        content_ok = (not miss) and (not bad)
        ok = route_ok and content_ok
        rows.append(dict(id=g["id"], cat=g["cat"], q=g["q"][:40], route_ref=g["route"],
                         route_got=got, route_ok=route_ok, miss=miss, bad=bad,
                         content_ok=content_ok, ok=ok, n=len(a), ans=a[:400]))
        detail = []
        if not route_ok:
            detail.append("路由 %s != %s" % (got, g["route"]))
        if miss:
            detail.append("缺关键词 %s" % miss)
        if bad:
            detail.append("命中禁用词 %s" % bad)
        print("%-4s %-3s %-3s %-26s 路由=%-4s %5d字  %s" % (
            "PASS" if ok else "FAIL", g["id"], g["cat"], g["q"][:24].replace("\n", " "),
            got, len(a), "；".join(detail)))
        time.sleep(0.5)

    n = len(rows)
    score = sum(1 for r in rows if r["ok"]) / n
    rc = [r for r in rows if r["route_ref"]]
    route_acc = (sum(1 for r in rc if r["route_ok"]) / len(rc)) if rc else 1.0
    content_pass = sum(1 for r in rows if r["content_ok"]) / n
    ref = [r for r in rows if r["cat"] == "拒答"]
    refusal_pass = (sum(1 for r in ref if r["ok"]) / len(ref)) if ref else 1.0

    print()
    print("按组：")
    for cat in ["意图", "边界", "拒答", "异常"]:
        grp = [r for r in rows if r["cat"] == cat]
        if grp:
            print("  %-4s %d/%d" % (cat, sum(1 for r in grp if r["ok"]), len(grp)))
    print("耗时 %.1fs" % (time.time() - t0))
    print("---SCORE_SUMMARY---")
    print("SCORE: %.3f" % score)
    print("ROUTE_ACCURACY: %.3f" % route_acc)
    print("CONTENT_PASS: %.3f" % content_pass)
    print("REFUSAL_PASS: %.3f" % refusal_pass)
    print("CASES: %d" % n)
    print("SITE: %s" % SITE)
    print("---END---")
    if JSON_OUT:
        f = open(JSON_OUT, "w", encoding="utf-8")
        json.dump(dict(site=SITE, score=score, route_accuracy=route_acc,
                       content_pass=content_pass, refusal_pass=refusal_pass,
                       cases=rows), f, ensure_ascii=False, indent=2)
        f.close()
        print("报告已写入 %s" % JSON_OUT)
    return 0 if score >= 0.80 else 1


if __name__ == "__main__":
    sys.exit(main())
