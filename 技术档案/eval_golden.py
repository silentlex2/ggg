# -*- coding: utf-8 -*-
"""职引 黄金集评估（golden-set eval）。

设计对标：
  - career-ops evals/README.md：指标是"与参考标签的一致度"，不是绝对正确性；
    archetype 是门（可复现），score 只作容差带信号；用例刻意偏向边界。
  - gov_rag docs/EVAL_DATASET_README.md：30 条 = 27 可回答 + 3 无答案/拒答；
    题型分散，不能只考某一类，否则天然偏向某一种检索方式。

用例数据在 eval_cases.py（40 条：意图 8 / 边界 12 / 拒答 6 / 异常 6 / 多轮 8）。
本文件只负责：发消息、判路由、判关键词、判截断、并发、打分、打契约块。

用法：
    python eval_golden.py [站点码] [--json 输出路径] [--only 意图,边界] [--workers 6]

并发：每条用例一条独立对话（多轮用例在同一个 conversation_id 里连续发）。
默认 --workers 3；--workers 1 即串行兜底。结果先收集、最后按用例原顺序统一打印，
避免并发下 stdout 交错。**实测 6 线程会把平台打进排队**（单条 120~280s、0 字超时、
分数掉到 0.825），3 线程才稳定。

截断断言：答案 >300 字且结尾不是句号/问号/感叹号/右引号/右括号/换行/列表项末尾
→ truncated=True，该条判 FAIL，detail 写"疑似截断（末尾 %r）"。
用于捕获已知缺陷「长答案偶发截断」。

输出末尾固定契约（可被其它脚本 grep）：
    ---SCORE_SUMMARY---
    SCORE: 0.850
    ROUTE_ACCURACY: 1.000
    CONTENT_PASS: 0.900
    REFUSAL_PASS: 1.000
    CASES: 40
    SITE: xxxx
    ---END---

退出码：0 = SCORE >= 0.80；1 = 低于阈值（用作回归门）。
"""
import json, os, re, ssl, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from eval_cases import GOLDEN as ALL_CASES          # 用例数据层（40 条）

BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

ARGS = list(sys.argv[1:])


def _opt(name, default=None):
    """取 "--flag 值" 形式的值；缺值返回 default。"""
    if name in ARGS:
        i = ARGS.index(name)
        if i + 1 < len(ARGS):
            return ARGS[i + 1]
    return default


def _default_site():
    """站点码唯一真源：环境变量 SITE > 同目录 readysite.txt（换站只改那一个文件）。"""
    env = os.environ.get("SITE", "").strip()
    if env:
        return env
    with open(os.path.join(HERE, "readysite.txt"), "r", encoding="utf-8") as f:
        return f.read().strip()


SITE = ARGS[0] if ARGS and not ARGS[0].startswith("--") else _default_site()
JSON_OUT = _opt("--json")
ONLY = set(_opt("--only").split(",")) if "--only" in ARGS else None
# 默认 3：实测 6 线程会把平台打进排队状态，单条涨到 120~280s 并出现 0 字超时（40 条 0.825）；
# 3 线程同一套用例 217s 跑完、结果稳定（0.975）。并发不是越高越好，别调高。
try:
    WORKERS = max(1, int(_opt("--workers", "3")))
except ValueError:
    WORKERS = 3

# 路由签名正则：反推模型实际走了哪条分支（不依赖模型自述）
ROUTE_SIGN = {
    "简历诊断": r"简历诊断报告|分项得分|综合算式|要求—证据矩阵|结构化诊断",
    "岗位匹配": r"岗位匹配建议|匹配理由",
    "模拟面试": r"第 1 题|面试进度|模拟面试复盘",
    "政策咨询": r"政策解答|办理流程",
    "闲聊": r"接待助手|接下来你可以",
}

# 结尾视为"完整"的字符白名单（截断判定的正面证据）
END_OK = set("。．.？?！!…～\"”’》〉」』】]）)")
# 末行是完整列表项，也算正常收尾（避免把 bullet 列表型答案误判为截断）
LAST_ITEM = re.compile(r"^\s*(?:[-*•·]|\d+[.、)]|[①-⑳])\s+.{6,}$")


def route_of(ans):
    best, pos = None, 10 ** 9
    for r, pat in ROUTE_SIGN.items():
        m = re.search(pat, ans)
        if m and m.start() < pos:
            best, pos = r, m.start()
    return best or "未识别"


def progress_of(ans):
    """面试进度行的题号（1..5）；没有进度行返回 0（= 无信号）。"""
    m = re.search(r"面试进度[：:]\s*(\d+)\s*/\s*\d+", ans)
    return int(m.group(1)) if m else 0


def trunc_detail(ans):
    """答案是否疑似被截断；返回 detail 字符串或 None。"""
    if len(ans) <= 300:
        return None
    if ans.endswith(("\n", "\r")):
        return None
    t = ans.rstrip()
    if not t:
        return None
    if t[-1] in END_OK:
        return None
    if LAST_ITEM.match(t.splitlines()[-1] if t.splitlines() else ""):
        return None
    return "疑似截断（末尾 %r）" % t[-1]


def passport():
    r = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(r, context=CTX, timeout=30) as resp:
        return json.loads(resp.read().decode())["access_token"]


def ask(q, tok, cid=""):
    """发一条消息，返回 (答案, conversation_id)。多轮用例把上一轮 cid 传回来。"""
    body = json.dumps({"response_mode": "streaming", "conversation_id": cid, "query": q,
                       "inputs": {"user_input": q}, "parent_message_id": None}).encode()
    r = urllib.request.Request(BASE + "/api/chat-messages", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-App-Code": SITE,
                 "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=400) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return "[HTTP %d] %s" % (e.code, e.read().decode("utf-8", "replace")[:200]), cid
    except Exception as e:                                   # 网络抖动 / 超时
        return "[ERR] %s" % e, cid
    ans, cid2 = "", cid
    for blk in raw.replace("\r\n", "\n").split("\n\n"):
        if not blk.startswith("data:"):
            continue
        try:
            j = json.loads(blk[5:].strip())
        except Exception:
            continue
        d = j.get("data") or {}
        if d.get("conversation_id"):
            cid2 = d["conversation_id"]
        if j.get("event") == "message":
            ans += j.get("answer", "")
    return ans, cid2


# ---------------------------------------------------------------- 单条用例
def run_case(g, tok):
    turns = g["turns"]
    multi = len(turns) > 1
    tag = (lambda i: "T%d:" % (i + 1)) if multi else (lambda i: "")
    t0 = time.time()
    answers, progs, cid = [], [], ""
    for q in turns:
        a, cid = ask(q, tok, cid)
        answers.append(a)
        progs.append(progress_of(a))
    elapsed = time.time() - t0

    graded = list(range(len(turns))) if g["assert_all"] else [len(turns) - 1]
    last = answers[-1]
    got = route_of(last)
    route_ok = (g["route"] is None) or (got == g["route"])

    miss, bad, truncs = [], [], []
    for i in graded:
        a = answers[i]
        miss += [tag(i) + k for k in g["must"] if k not in a]
        bad += [tag(i) + k for k in g["must_not"] if k in a]
        d = trunc_detail(a)
        if d:
            truncs.append(tag(i) + d)
    content_ok = (not miss) and (not bad)

    inv_bad = []
    seen = [p for p in progs if p > 0]          # 0 = 本轮没进度行，不作信号
    if "progress_nonregress" in g["invariants"] and len(seen) >= 2:
        if seen != sorted(seen):
            inv_bad.append("进度倒退 %s" % progs)
    if "progress_increase" in g["invariants"] and progs[0] > 0 and progs[-1] > 0:
        if progs[-1] <= progs[0]:
            inv_bad.append("进度未递增 %s" % progs)

    ok = route_ok and content_ok and (not truncs) and (not inv_bad)
    detail = []
    if not route_ok:
        detail.append("路由 %s != %s" % (got, g["route"]))
    if miss:
        detail.append("缺关键词 %s" % miss)
    if bad:
        detail.append("命中禁用词 %s" % bad)
    detail += truncs + inv_bad
    if not ok:                                        # FAIL 时带答案开头，便于人工复核
        detail.append("答案开头 %r" % last[:60].replace("\n", " "))
    return dict(id=g["id"], cat=g["cat"], q=turns[-1] if g.get("q") == "" else g["q"],
                turns=len(turns), route_ref=g["route"], route_got=got, route_ok=route_ok,
                miss=miss, bad=bad, truncated=bool(truncs), trunc_detail=truncs,
                invariants=inv_bad, progress=progs, content_ok=content_ok, ok=ok,
                n=len(last), chars=[len(a) for a in answers], seconds=round(elapsed, 1),
                detail="；".join(detail), ans=last[:400])


def main():
    t0 = time.time()
    cases = [c for c in ALL_CASES if (not ONLY) or (c["cat"] in ONLY)]
    print("=" * 78)
    print("职引 黄金集评估   站点 %s   用例 %d 条   并发 %d 线程" % (SITE, len(cases), WORKERS))
    print("=" * 78)
    tok = passport()

    rows = [None] * len(cases)
    if WORKERS <= 1:                                  # 串行兜底
        for i, g in enumerate(cases):
            rows[i] = run_case(g, tok)
            print("  ... %s 完成（%.1fs）" % (g["id"], rows[i]["seconds"]))
    else:
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futs = [ex.submit(run_case, g, tok) for g in cases]
            for i, fu in enumerate(futs):
                rows[i] = fu.result()

    # 并发下 stdout 不乱序：全部跑完再按原顺序统一打印
    nshow = 0
    for g, r in zip(cases, rows):
        nshow += 1
        qshow = g["turns"][-1][:24].replace("\n", " ")
        print("%-4s %-3s %-3s %-26s 路由=%-4s %5d字 %5.1fs %s%s" % (
            "PASS" if r["ok"] else "FAIL", g["id"], g["cat"], qshow,
            r["route_got"], r["n"], r["seconds"],
            "[%d轮] " % r["turns"] if r["turns"] > 1 else "", r["detail"]))

    n = len(rows)
    score = sum(1 for r in rows if r["ok"]) / n if n else 0.0
    rc = [r for r in rows if r["route_ref"]]
    route_acc = (sum(1 for r in rc if r["route_ok"]) / len(rc)) if rc else 1.0
    content_pass = (sum(1 for r in rows if r["content_ok"]) / n) if n else 0.0
    ref = [r for r in rows if r["cat"] == "拒答"]
    refusal_pass = (sum(1 for r in ref if r["ok"]) / len(ref)) if ref else 1.0

    print()
    print("按组：")
    for cat in ["意图", "边界", "拒答", "异常", "多轮"]:
        grp = [r for r in rows if r["cat"] == cat]
        if grp:
            print("  %-4s %d/%d" % (cat, sum(1 for r in grp if r["ok"]), len(grp)))
    print("耗时 %.1fs（并发 %d 线程）" % (time.time() - t0, WORKERS))
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
                       workers=WORKERS, cases=rows), f, ensure_ascii=False, indent=2)
        f.close()
        print("报告已写入 %s" % JSON_OUT)
    return 0 if score >= 0.80 else 1


if __name__ == "__main__":
    sys.exit(main())
