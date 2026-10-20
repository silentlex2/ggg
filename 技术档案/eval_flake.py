# -*- coding: utf-8 -*-
"""黄金集稳定性统计（eval_flake.py）

为什么要有：单跑一次黄金集只能告诉你"这一轮过了几条"，说服力很弱——
模型的输出本身在抖，同一份配置今天 44/46、明天 43/46 是常事。
真正该知道的是：**哪几条是不稳定的**。评委面前翻车的，永远是那几条。

用法：
    python eval_flake.py                       # 全量跑 3 轮，逐条统计通过率
    python eval_flake.py --only 多轮 --runs 4   # 只盯多轮组
    python eval_flake.py --json a.json b.json   # 不重跑，直接汇总已有报告

输出：逐条通过率表 + 不稳定项清单（红项分「恒定红」和「偶发红」，性质完全不同）。
契约：
    ---FLAKE---
    RUNS: 3
    CASES: 46
    STABLE_PASS: 43
    ALWAYS_FAIL: 1
    UNSTABLE: 2
    ---END---

退出码：0 = 全部稳定（该过的都过、该红的恒红）；1 = 存在偶发项。
"""
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "scratch")


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d if isinstance(d, dict) else {}


def run_once(idx, only, workers):
    out = os.path.join(SCRATCH, "flake-%02d.json" % idx)
    os.makedirs(SCRATCH, exist_ok=True)
    cmd = [sys.executable, os.path.join(HERE, "eval_golden.py"), "--json", out,
           "--workers", str(workers)]
    if only:
        cmd += ["--only", only]
    print("\n$ %s" % " ".join(cmd))
    t0 = time.time()
    p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    tail = [l for l in (p.stdout or "").split("\n") if l.startswith(("SCORE:", "CASES:"))]
    print("  轮次 %d：%.0fs  %s" % (idx, time.time() - t0, " ".join(tail)))
    return out if os.path.exists(out) else None


def main():
    args = sys.argv[1:]
    workers = args[args.index("--workers") + 1] if "--workers" in args else "3"
    only = args[args.index("--only") + 1] if "--only" in args else ""
    runs = int(args[args.index("--runs") + 1]) if "--runs" in args else 3

    if "--json" in args:
        i = args.index("--json")
        paths = [a for a in args[i + 1:] if a.endswith(".json")]
    else:
        paths = []
        for n in range(1, runs + 1):
            got = run_once(n, only, workers)
            if got:
                paths.append(got)
    if len(paths) < 2:
        print("\n至少要两份报告才能谈稳定性（现有 %d 份）" % len(paths))
        return 2

    tally, meta = {}, {}
    for path in paths:
        d = load(path)
        for c in d.get("cases") or []:
            cid = c.get("id") or "?"
            meta[cid] = (c.get("cat") or "", (c.get("q") or "")[:28])
            rec = tally.setdefault(cid, {"run": 0, "ok": 0})
            rec["run"] += 1
            rec["ok"] += 1 if c.get("ok") else 0

    n_runs = len(paths)
    print("\n汇总 %d 份报告，共 %d 条用例" % (n_runs, len(tally)))
    print("\n%-5s %-4s %-6s %s" % ("ID", "组", "通过率", "题目"))
    unstable, always_fail = [], []
    for cid in sorted(tally, key=lambda x: (meta[x][0], x)):
        rec = tally[cid]
        rate = rec["ok"] / float(rec["run"])
        cat, q = meta[cid]
        if rec["ok"] == rec["run"]:
            flag = "稳定过"
        elif rec["ok"] == 0:
            flag = "恒定红"
            always_fail.append(cid)
        else:
            flag = "偶发"
            unstable.append(cid)
        print("%-5s %-4s %-6s %s" % (cid, cat, "%.2f" % rate, q))
        if flag != "稳定过":
            print("      ^ %s（%d/%d）" % (flag, rec["ok"], rec["run"]))

    stable_pass = sum(1 for c in tally if tally[c]["ok"] == tally[c]["run"])
    print("\n稳定通过 %d 条｜恒定红 %d 条 %s｜偶发 %d 条 %s"
          % (stable_pass, len(always_fail), always_fail or "",
             len(unstable), unstable or ""))
    print("\n判读要点：恒定红要单独定性（是产品短板还是刻意留的哨兵）；"
          "偶发项是答辩前最该盯的——它会在评委面前随机翻车。")

    print("\n---FLAKE---")
    print("RUNS: %d" % n_runs)
    print("CASES: %d" % len(tally))
    print("STABLE_PASS: %d" % stable_pass)
    print("ALWAYS_FAIL: %d" % len(always_fail))
    print("UNSTABLE: %d" % len(unstable))
    print("---END---")
    return 1 if unstable else 0


if __name__ == "__main__":
    sys.exit(main())