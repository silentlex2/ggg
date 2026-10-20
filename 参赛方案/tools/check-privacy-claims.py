# -*- coding: utf-8 -*-
"""隐私口径一致性检查：材料里不许出现"不落库 / 不留存原文"这类不实表述。

为什么要有这条：
  上传的简历文件是**平台按会话保存的**。早期材料里写"不落库、不留存原文"，
  这句话经不起追问——评委只要问一句"上传的文件存不存"，就露馅。
  2026-10-20 已把全部材料统一成"不进长期记忆、不进埋点、不做二次使用；
  上传文件由平台按会话保存"。

检查规则：
  - 扫 参赛方案/ + 交接说明.md + 前端/ 下的 Markdown（历史归档 历史-*.md 除外）
  - 命中禁用措辞即失败
  - 若同一行还带有"不要写 / 不说 / 不准确 / 校准 / 会被追问"等说明词，
    说明它是在**讨论这个措辞本身**，放行

用法：
    python 参赛方案/tools/check-privacy-claims.py
退出码：0 = 口径一致；1 = 有需要改的表述
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

BANNED = [
    "不留存简历原文",
    "不留存原文",
    "不留存副本",
    "简历原文不落库",
    "不落库、不入记忆",
    "不落库不进日志",
]
# 命中禁用词但同时出现这些词，视为"在讨论措辞本身"，放行
GUARDS = ["不要写", "别写", "不说", "不准确", "口径校准", "会被追问", "经不起追问",
          "不许出现", "故意写", "这类表述", "报 FAIL"]

SCAN_DIRS = [os.path.join(ROOT, "参赛方案"), os.path.join(ROOT, "前端")]
SCAN_FILES = [os.path.join(ROOT, "交接说明.md")]
SKIP_NAME = re.compile(r"^历史-")


def iter_markdown():
    for path in SCAN_FILES:
        if os.path.exists(path):
            yield path
    for base in SCAN_DIRS:
        for cur, _, files in os.walk(base):
            for name in files:
                if not name.endswith(".md") or SKIP_NAME.match(name):
                    continue
                yield os.path.join(cur, name)


def main():
    hits, scanned = [], 0
    for path in iter_markdown():
        scanned += 1
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:  # noqa: BLE001
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for phrase in BANNED:
                if phrase not in line:
                    continue
                if any(guard in line for guard in GUARDS):
                    continue
                hits.append((os.path.relpath(path, ROOT).replace("\\", "/"), line_no, phrase, line.strip()[:90]))
    print("扫描 Markdown %d 个，禁用措辞 %d 条" % (scanned, len(BANNED)))
    if not hits:
        print("隐私口径：一致 ✅")
        print("---PRIVACY_SUMMARY---")
        print("RESULT: PASS")
        print("HITS: 0")
        print("---END---")
        return 0
    print("命中 %d 处 ❌" % len(hits))
    for path, line_no, phrase, line in hits:
        print("  %s:%d  「%s」  %s" % (path, line_no, phrase, line))
    print("---PRIVACY_SUMMARY---")
    print("RESULT: FAIL")
    print("HITS: %d" % len(hits))
    print("---END---")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
