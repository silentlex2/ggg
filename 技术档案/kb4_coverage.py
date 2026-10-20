# -*- coding: utf-8 -*-
"""KB4 岗位库覆盖度分析：行业/城市/学历/专业维度，定位覆盖缺口。"""
import collections
import csv
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "参赛方案", "知识库", "KB4-岗位JD库.csv")


def main():
    rows = list(csv.DictReader(io.open(CSV_PATH, encoding="utf-8-sig")))
    print("岗位总数 %d" % len(rows))
    for field in ("industry", "city", "job_type", "degree", "company_type"):
        counter = collections.Counter(r[field] for r in rows)
        print("")
        print("[%s] %d 类" % (field, len(counter)))
        for key, val in counter.most_common():
            print("   %-18s %d" % (key, val))

    majors = collections.Counter()
    for row in rows:
        for part in row["major_req"].replace("；", ";").split(";"):
            part = part.strip()
            if part:
                majors[part] += 1
    print("")
    print("[专业覆盖] %d 个" % len(majors))
    for key, val in majors.most_common():
        print("   %-26s %d" % (key, val))


if __name__ == "__main__":
    main()
