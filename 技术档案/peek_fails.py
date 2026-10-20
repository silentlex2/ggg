# -*- coding: utf-8 -*-
"""列出一次回归里的失败用例，带失败原因与答案开头。"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else "regression-v19-46.json"
data = json.load(open(os.path.join(HERE, path), encoding="utf-8"))
fails = [c for c in data["cases"] if not c["ok"]]
print("失败 %d / %d" % (len(fails), len(data["cases"])))
for case in fails:
    print("")
    print("=== %s [%s] %s" % (case["id"], case["cat"], case["q"][:60]))
    print("  路由 期望=%s 实际=%s ok=%s" % (case.get("route_ref"), case.get("route_got"), case.get("route_ok")))
    print("  缺关键词 %s / 出现禁词 %s / 截断 %s" % (case.get("miss"), case.get("bad"), case.get("truncated")))
    print("  详情 %s" % (case.get("detail") or "")[:200])
    print("  答案 %s" % (case.get("ans") or "")[:260].replace("\n", " "))
