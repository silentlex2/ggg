# -*- coding: utf-8 -*-
"""职引 · 一键回归门（run_all.py）

一条命令跑完：五分支巡检 → 黄金集评估 →（可选）全流程回归。

站点码只有一个真源：`技术档案/readysite.txt`。本脚本、`eval_golden.py`、
`finaltest_ready.py` 都从这里读，换站只改这一个文件。
环境变量 `SITE` 可临时覆盖（CI / 临时试站用）。

用法：
    python run_all.py                 # 五分支 + 黄金集
    python run_all.py --no-golden     # 只跑五分支巡检（约 1.5 分钟）
    python run_all.py --only 边界,拒答 # 巡检照跑，黄金集只跑指定组
    python run_all.py --full          # 追加 finaltest_ready 全流程（约 6 分钟，仅提示不拦截）
    python run_all.py --no-offline    # 跳过材料侧两道离线检查（死链 / 隐私口径）；--no-links 是它的旧名

输出末尾固定契约（可被其它脚本 / CI grep）：
    ---SCORE_SUMMARY---
    PATROL: 5/5
    LINKS: ok
    PRIVACY: ok
    CONSISTENCY: ok
    SUBMISSION: missing(2)
    GOLDEN_EXIT: 0
    SCORE: 1.000
    ---END---

CONSISTENCY 参与门禁（口径漂移必须挡住）；SUBMISSION 只报不拦——三样材料里
有视频和照片只能人来录，缺项是常态，不该把整道门打成红。

退出码：0 = 全绿；1 = 有分支未按预期路由 / 答案过短 / 黄金集低于 0.80；2 = 站点不可达。
"""
import json
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://aiagent.cqut.edu.cn:31134"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

REPORT = os.path.join(HERE, "regression-latest.json")

ARGS = list(sys.argv[1:])
ONLY = set(ARGS[ARGS.index("--only") + 1].split(",")) if "--only" in ARGS else None
NO_GOLDEN = "--no-golden" in ARGS
FULL = "--full" in ARGS
# 材料侧两道离线检查：死链、隐私口径。都不碰站点，放进这道门最划算——改完文档随手就跑到了
NO_OFFLINE = ("--no-offline" in ARGS) or ("--no-links" in ARGS)
TOOLS_DIR = os.path.join(os.path.dirname(HERE), "参赛方案", "tools")
LINKS_SCRIPT = os.path.join(TOOLS_DIR, "check-links.py")
PRIVACY_SCRIPT = os.path.join(TOOLS_DIR, "check-privacy-claims.py")
CONSISTENCY_SCRIPT = os.path.join(TOOLS_DIR, "check-consistency.py")
SUBMISSION_SCRIPT = os.path.join(TOOLS_DIR, "check-submission.py")


def site_code():
    """站点码唯一真源：环境变量 SITE > readysite.txt。"""
    env = os.environ.get("SITE", "").strip()
    if env:
        return env
    path = os.path.join(HERE, "readysite.txt")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read().strip()
    if not code:
        raise SystemExit("readysite.txt 为空：先写入当前站点码")
    return code


SITE = site_code()

# 分支判定原语：节点 ID（最硬）＋ 回答签名（兜底，覆盖没有独立节点的简历分支）
NODE_IV = "1791600000050"
NODE_CH = "1791600000001"
NODE_POL = "1791600000060"
NODE_JOB = "1791600000030"
# 简历分支没有单一判定节点：文档提取 / 简历大模型 / 提示上传简历 三者任一出现即算
NODE_RESUME = {"1791544765658", "1791550106443", "1791552000001"}
SIG_RESUME = r"简历诊断报告|分项得分|综合算式|要求—证据矩阵|覆盖度"


# ---------------------------------------------------------------- 巡检用例
# (场景名, 提问, 期望分支集合)
BRANCH_CASES = [
    ("闲聊", "你好", {"闲聊"}),
    ("简历诊断", "帮我看看我的简历有什么问题", {"简历"}),
    ("岗位匹配", "我是化学工程与工艺专业大四，会 Aspen Plus，想找重庆的化工类校招岗位", {"岗位"}),
    ("模拟面试", "来一场模拟面试，我目标岗位是化工工艺工程师", {"面试"}),
    ("政策咨询", "重庆应届生有哪些就业补贴可以领", {"政策"}),
]

MIN_LEN = 20   # 低于这个字数的回答视为空转


def passport():
    req = urllib.request.Request(BASE + "/api/passport", headers={"X-App-Code": SITE})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read().decode())["access_token"]


def ask(q, tok, retries=3):
    """发一条消息，返回 (答案, 节点ID列表, 耗时秒, conversation_id)。"""
    t0 = time.time()
    last = ("", [], 0.0, "")
    for attempt in range(retries):
        body = json.dumps({"response_mode": "streaming", "conversation_id": "",
                           "query": q, "inputs": {"user_input": q},
                           "parent_message_id": None}).encode()
        req = urllib.request.Request(
            BASE + "/api/chat-messages", data=body, method="POST",
            headers={"Content-Type": "application/json", "X-App-Code": SITE,
                     "authorization": "Bearer " + tok, "auth-token": "Bearer " + tok})
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=300) as resp:
                raw = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:200]
            last = ("[HTTP %d] %s" % (e.code, detail), [], time.time() - t0, "")
            time.sleep(2)
            continue
        except Exception as e:                                # 网络抖动 / 超时
            last = ("[ERR] %s" % e, [], time.time() - t0, "")
            time.sleep(3)
            continue
        ans, nodes, cid = "", [], ""
        for blk in raw.replace("\r\n", "\n").split("\n\n"):
            if not blk.startswith("data:"):
                continue
            try:
                j = json.loads(blk[5:].strip())
            except Exception:
                continue
            d = j.get("data") or {}
            if d.get("conversation_id"):
                cid = d["conversation_id"]
            if j.get("event") == "message":
                ans += j.get("answer", "")
            if j.get("event") == "node_finished":
                nodes.append(d.get("node_id", "?"))
        last = (ans, nodes, time.time() - t0, cid)
        if len(ans) >= 10 or attempt == retries - 1:
            return last
        time.sleep(4)
    return last


def branch_of(ans, nodes):
    """先看节点，再看签名，都判不出才算未识别。"""
    if NODE_IV in nodes:
        return "面试"
    if NODE_POL in nodes:
        return "政策"
    if NODE_JOB in nodes:
        return "岗位"
    if NODE_CH in nodes:
        return "闲聊"
    if NODE_RESUME & set(nodes) or re.search(SIG_RESUME, ans):
        return "简历"
    if re.search(r"面试进度|第 1 题", ans):
        return "面试"
    if re.search(r"岗位匹配建议|匹配理由", ans):
        return "岗位"
    if re.search(r"政策解答|办理流程", ans):
        return "政策"
    return "未识别"


def patrol():
    print("=" * 78)
    print("职引 五分支巡检   站点 %s" % SITE)
    print("=" * 78)
    tok = passport()
    rows, npass = [], 0
    for name, q, expect in BRANCH_CASES:
        ans, nodes, sec, cid = ask(q, tok)
        got = branch_of(ans, nodes)
        ok = got in expect and len(ans) >= MIN_LEN
        npass += 1 if ok else 0
        why = [] if ok else ["分支 %s ∉ %s" % (got, sorted(expect)) if got not in expect else "",
                             "答案仅 %d 字" % len(ans) if len(ans) < MIN_LEN else ""]
        rows.append(dict(name=name, q=q, expect=sorted(expect), got=got,
                         ok=ok, chars=len(ans), seconds=round(sec, 1),
                         nodes=nodes[:12], ans=ans[:300]))
        print("%-4s %-8s -> %-5s %3d字 %5.1fs   %s" % (
            "PASS" if ok else "FAIL", name, got, len(ans), sec,
            "；".join(x for x in why if x)))
        time.sleep(1)
    total = len(rows)
    print("巡检 %d/%d 通过" % (npass, total))
    return rows, npass, total


def run_script(abs_path, extra=None):
    """跑任意路径的脚本（用于 参赛方案/tools 下的离线检查）。"""
    cmd = [sys.executable, abs_path] + (extra or [])
    print("\n$ %s" % " ".join(cmd))
    p = subprocess.run(cmd, cwd=HERE)
    return p.returncode


def run_script_capture(abs_path, extra=None):
    """同上，但把子进程输出收上来解析（给只报不拦的检查用）。"""
    cmd = [sys.executable, abs_path] + (extra or [])
    print("\n$ %s" % " ".join(cmd))
    p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print(p.stdout or "", end="")
    if p.stderr:
        print(p.stderr, end="", file=sys.stderr)
    return p.returncode, (p.stdout or "")


def run_child(script, extra=None):
    """以子进程跑兄弟脚本，继承站点码真源。"""
    cmd = [sys.executable, os.path.join(HERE, script)] + (extra or [])
    print("\n$ %s" % " ".join(cmd))
    env = dict(os.environ, SITE=SITE)
    p = subprocess.run(cmd, cwd=HERE, env=env)
    return p.returncode


def main():
    t0 = time.time()
    patrol_rows = []
    npass = ntotal = 0
    golden_rc = None
    full_rc = None

    try:
        patrol_rows, npass, ntotal = patrol()
    except SystemExit:
        raise
    except Exception as e:
        print("巡检阶段异常：%s" % e)
        print("---SCORE_SUMMARY---")
        print("PATROL: 0/0")
        print("SCORE: 0.000")
        print("SITE: %s" % SITE)
        print("---END---")
        return 2

    links_rc = None
    privacy_rc = None
    consistency_rc = None
    submission_rc = None
    submission_missing = None
    if not NO_OFFLINE:
        if os.path.exists(LINKS_SCRIPT):
            links_rc = run_script(LINKS_SCRIPT)
        if os.path.exists(PRIVACY_SCRIPT):
            privacy_rc = run_script(PRIVACY_SCRIPT)
        if os.path.exists(CONSISTENCY_SCRIPT):
            consistency_rc = run_script(CONSISTENCY_SCRIPT)
        if os.path.exists(SUBMISSION_SCRIPT):
            # 只报不拦：材料要靠人录视频拍照，缺项不该阻断门禁
            submission_rc, submission_out = run_script_capture(SUBMISSION_SCRIPT)
            m = re.search(r"MISSING:\s*(\d+)", submission_out)
            submission_missing = int(m.group(1)) if m else None

    if not NO_GOLDEN:
        extra = ["--json", REPORT]
        if ONLY:
            extra = ["--only", ",".join(sorted(ONLY))] + extra
        golden_rc = run_child("eval_golden.py", extra)

    if FULL:
        full_rc = run_child("finaltest_ready.py")

    ok = ((npass == ntotal and ntotal > 0) and (golden_rc in (None, 0))
          and (links_rc in (None, 0)) and (privacy_rc in (None, 0))
          and (consistency_rc in (None, 0)))
    print("\n" + "=" * 78)
    print("总耗时 %.1fs   站点 %s" % (time.time() - t0, SITE))
    if full_rc is not None:
        print("全流程回归（仅提示，不参与门禁）：退出码 %s，人工看上方输出" % full_rc)
    print("---SCORE_SUMMARY---")
    print("PATROL: %d/%d" % (npass, ntotal))
    print("LINKS: %s" % ("skipped" if links_rc is None else ("ok" if links_rc == 0 else "fail(%d)" % links_rc)))
    print("PRIVACY: %s" % ("skipped" if privacy_rc is None else ("ok" if privacy_rc == 0 else "fail(%d)" % privacy_rc)))
    print("CONSISTENCY: %s" % ("skipped" if consistency_rc is None else ("ok" if consistency_rc == 0 else "fail(%d)" % consistency_rc)))
    if submission_rc is None:
        print("SUBMISSION: skipped")
    elif submission_rc == 0:
        print("SUBMISSION: ready")
    else:
        print("SUBMISSION: missing(%s)" % ("?" if submission_missing is None else submission_missing))
    print("GOLDEN_EXIT: %s" % ("skipped" if golden_rc is None else golden_rc))
    print("SCORE: %s" % ("1.000" if ok else "0.000"))
    print("SITE: %s" % SITE)
    print("---END---")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
