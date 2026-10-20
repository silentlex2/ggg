# -*- coding: utf-8 -*-
"""列出 KB4 v2 里的重名岗位，判断是同一岗位重复还是同名不同城市。"""
import collections
import csv
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "参赛方案", "知识库", "KB4-岗位JD库-v2.csv")
rows = list(csv.DictReader(io.open(path, encoding="utf-8-sig")))
groups = collections.defaultdict(list)
for row in rows:
    groups[row["job_title"]].append(row)

print("总行 %d，唯一名称 %d" % (len(rows), len(groups)))
for title, items in groups.items():
    if len(items) < 2:
        continue
    print("")
    print("重名：%s（%d 条）" % (title, len(items)))
    for row in items:
        print("   id=%-3s 城市=%-10s 行业=%-12s 学历=%-6s 薪资=%s" % (
            row["id"], row["city"], row["industry"], row["degree"], row["salary_range"]))
        print("        职责=%s" % row["duties"][:70])
