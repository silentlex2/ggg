# -*- coding: utf-8 -*-
"""看单条用例的完整答案与长度，判断是"偶发缺块"还是"内容确实不同"。"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
target = sys.argv[1]
path = sys.argv[2] if len(sys.argv) > 2 else "regression-v19-46.json"
data = json.load(open(os.path.join(HERE, path), encoding="utf-8"))
for case in data["cases"]:
    if case["id"] != target:
        continue
    ans = case.get("ans") or ""
    print("id=%s  字数=%d  秒=%s" % (case["id"], len(ans), case.get("seconds")))
    print("含「面试进度」：%s" % ("面试进度" in ans))
    print("含「第 1 题」：%s" % ("第 1 题" in ans))
    print("---- 全文 ----")
    print(ans)
