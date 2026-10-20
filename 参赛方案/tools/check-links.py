# -*- coding: utf-8 -*-
"""提交材料死链检查：扫 Markdown 里的相对链接，确认目标文件真的存在。

形式审查最常见的翻车不是内容不行，而是材料里引用的文件根本不存在（改名、挪目录、从没产出过）。
这个脚本只看 Markdown 链接语法 [文字](路径)，不猜反引号里的示意路径，避免误报。

用法：
    python 参赛方案/tools/check-links.py            # 扫 参赛方案/ 与 交接说明.md
    python 参赛方案/tools/check-links.py --all      # 连 技术档案/ 与 前端/ 一起扫
"""
import argparse
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
INLINE_CODE = re.compile(r"`[^`]*`")   # 反引号里的是示例/路径片段，不是真链接
SKIP_PREFIX = ("http://", "https://", "mailto:", "#", "tel:")


def walk_targets(scan_all):
    targets = [os.path.join(ROOT, "交接说明.md")]
    dirs = [os.path.join(ROOT, "参赛方案")]
    if scan_all:
        dirs += [os.path.join(ROOT, "技术档案"), os.path.join(ROOT, "前端")]
    for base in dirs:
        for cur, _, files in os.walk(base):
            for name in files:
                if name.endswith(".md"):
                    targets.append(os.path.join(cur, name))
    return sorted(set(targets))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="连技术档案与前端一起扫")
    args = parser.parse_args()

    broken, checked = [], 0
    for path in walk_targets(args.all):
        try:
            text = io.open(path, encoding="utf-8").read()
        except Exception:  # noqa: BLE001
            continue
        in_fence = False
        for line_no, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for raw in LINK.findall(INLINE_CODE.sub("", line)):
                target = raw.split("#")[0].strip()
                if not target or target.lower().startswith(SKIP_PREFIX):
                    continue
                checked += 1
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
                if not os.path.exists(resolved):
                    broken.append((os.path.relpath(path, ROOT).replace("\\", "/"), line_no, target))

    print("扫描 Markdown %d 个，检查相对链接 %d 条" % (len(walk_targets(args.all)), checked))
    if not broken:
        print("死链：0 ✅")
        return 0
    print("死链：%d ❌" % len(broken))
    for src, line_no, target in broken:
        print("  %s:%d -> %s" % (src, line_no, target))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
