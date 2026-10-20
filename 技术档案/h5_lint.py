# -*- coding: utf-8 -*-
"""把 H5 里的 <script> 抽出来单独存盘，交给 node --check 做语法校验。"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
html = io.open(os.path.join(HERE, "..", "前端", "职引-H5.html"), encoding="utf-8").read()
m = re.search(r"<script>(.*?)</script>", html, re.S)
if not m:
    print("没找到 <script> 块")
    raise SystemExit(1)
js = m.group(1)
out = os.path.join(HERE, "scratch", "h5-script.js")
os.makedirs(os.path.dirname(out), exist_ok=True)
io.open(out, "w", encoding="utf-8", newline="\n").write(js)
print("已抽出 %d 行脚本 -> %s" % (js.count("\n") + 1, out))
print("HTML 总行数 %d，字节 %d" % (html.count("\n") + 1, len(html.encode("utf-8"))))
