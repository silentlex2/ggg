# -*- coding: utf-8 -*-
"""把一次黄金集回归结果压成按组统计，供文档填实测数字。"""
import collections
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "regression-v19.json")
data = json.load(open(path, encoding="utf-8"))
cases = data["cases"] if isinstance(data, dict) else data

print("文件 %s" % os.path.basename(path))
if isinstance(data, dict):
    for key in ("score", "route_accuracy", "content_pass", "refusal_pass", "site", "workers"):
        if key in data:
            print("   %-16s %s" % (key, data[key]))
print("")
print("用例字段：%s" % ", ".join(sorted(cases[0].keys())))
print("")

group = collections.defaultdict(lambda: [0, 0])
fails = []
for case in cases:
    tag = case.get("cat") or case.get("kind") or case.get("group_name") or "?"
    ok = bool(case.get("ok", case.get("pass")))
    group[tag][0] += 1
    group[tag][1] += 1 if ok else 0
    if not ok:
        fails.append(case)

print("按组：")
for tag in sorted(group):
    total, passed = group[tag]
    print("   %-10s %d/%d" % (tag, passed, total))
print("   合计 %d/%d" % (sum(v[1] for v in group.values()), len(cases)))
print("")
print("失败用例 %d 条" % len(fails))
for case in fails:
    print(json.dumps({k: v for k, v in case.items() if k not in ("answer", "raw")},
                     ensure_ascii=False)[:900])
