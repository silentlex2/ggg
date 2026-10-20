# -*- coding: utf-8 -*-
"""看跨专业用例的实际回答：确认"没瞎编化工"的同时，答案本身是有用的。"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "regression-major.json"), encoding="utf-8"))
for case in data["cases"]:
    if case["id"] not in ("F5", "F6", "F1"):
        continue
    print("=== %s %s" % (case["id"], case["q"]))
    print(case["ans"][:520].replace("\n", " "))
    print("")
