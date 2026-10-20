# -*- coding: utf-8 -*-
"""打印提交表模板的表格结构：每行每个单元格的文字，用来定位【待填】在哪一格。"""
import os
import sys

import docx

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"F:\zcode\suiyi\ggg"
TPL = os.path.join(ROOT, "site-dump", "assets", "files", "uploads", "file", "20260924",
                   "20260924102044c59e90534.docx")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def cell_text(tc):
    return "".join(node.text or "" for node in tc.iter(W + "t")).strip()


doc = docx.Document(TPL)
table = doc.tables[0]
print("表格 %d 行" % len(table.rows))
for ri, row in enumerate(table.rows):
    cells = row._tr.findall(W + "tc")
    parts = []
    for ci, tc in enumerate(cells):
        text = cell_text(tc)
        long_text = text if len(text) <= 24 else text[:24] + "…"
        parts.append("[%d]%s" % (ci, long_text or "(空)"))
    print("行 %-2d 格数=%d  %s" % (ri, len(cells), " | ".join(parts)))
