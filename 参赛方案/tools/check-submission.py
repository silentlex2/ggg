# -*- coding: utf-8 -*-
"""提交包终检：按官网《提交要求》逐项核对文件是否齐全、时长是否达标。

官方只要求三样（指南 5 §提交材料）：
  (1) 作品提交表 PDF
  (2) 团队活动记录 图片 ≥3 张 或 视频 ≥30 秒
  (3) 作品演示视频 ≤3 分钟
其余（作品截图等）是提交表内的配图，不作为独立材料。

用法：
    python 参赛方案/tools/check-submission.py
退出码：0 = 齐全；1 = 有缺项
"""
import glob
import json
import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SUBMIT = os.path.join(ROOT, "参赛方案", "提交材料")

PHOTO_PATTERNS = ["团队活动-*.jpg", "团队活动-*.jpeg", "团队活动-*.png",
                  "团队活动*.jpg", "团队活动*.jpeg", "团队活动*.png"]
VIDEO = "团队活动记录.mp4"
DEMO = "作品演示视频.mp4"
FORM_PDF = "作品提交表-职引.pdf"


def probe_duration(path):
    """优先 ffprobe，其次尝试用系统自带能力；都拿不到就返回 None。"""
    exe = shutil.which("ffprobe")
    if exe:
        try:
            out = subprocess.run([exe, "-v", "error", "-show_entries", "format=duration",
                                  "-of", "json", path],
                                 capture_output=True, text=True, timeout=60)
            data = json.loads(out.stdout or "{}")
            return float(data.get("format", {}).get("duration") or 0) or None
        except Exception:  # noqa: BLE001
            return None
    return None


def fmt_size(path):
    n = os.path.getsize(path)
    return "%.1f MB" % (n / 1048576.0) if n >= 1048576 else "%d KB" % max(1, n // 1024)


def main():
    lines, missing = [], []

    def add(ok, text):
        lines.append(("  PASS  " if ok else "  MISS  ") + text)
        if not ok:
            missing.append(text)

    # (1) 作品提交表 PDF
    pdf = os.path.join(SUBMIT, FORM_PDF)
    add(os.path.exists(pdf), "%s（作品提交表，PDF）%s" % (FORM_PDF,
        ("  " + fmt_size(pdf)) if os.path.exists(pdf) else "  —— 未生成"))

    # (2a) 团队活动图片 ≥3
    photos = []
    for pattern in PHOTO_PATTERNS:
        photos.extend(glob.glob(os.path.join(SUBMIT, pattern)))
    photos = sorted(set(p for p in photos if "团队活动记录" not in os.path.basename(p)))
    add(len(photos) >= 3, "团队活动图片 ≥3 张：现有 %d 张%s" % (
        len(photos), "" if len(photos) >= 3 else "  —— 还差 %d 张" % (3 - len(photos))))

    # (2b) 团队活动视频 ≥30 秒
    video = os.path.join(SUBMIT, VIDEO)
    if not os.path.exists(video):
        add(False, "%s（团队活动记录视频，≥30 秒）—— 未录制" % VIDEO)
    else:
        dur = probe_duration(video)
        if dur is None:
            lines.append("  WARN  %s 存在（%s），但本机没有 ffprobe，无法校验时长（需 ≥30 秒）"
                         % (VIDEO, fmt_size(video)))
        else:
            add(dur >= 30, "%s 时长 %.1f 秒（需 ≥30 秒）" % (VIDEO, dur))

    # (3) 作品演示视频 ≤3 分钟
    demo = os.path.join(SUBMIT, DEMO)
    if not os.path.exists(demo):
        add(False, "%s（作品演示视频，≤3 分钟）—— 未录制" % DEMO)
    else:
        dur = probe_duration(demo)
        if dur is None:
            lines.append("  WARN  %s 存在（%s），但本机没有 ffprobe，无法校验时长（需 ≤180 秒）"
                         % (DEMO, fmt_size(demo)))
        else:
            add(dur <= 180, "%s 时长 %.1f 秒（需 ≤180 秒，超了要剪）" % (DEMO, dur))

    print("提交包目录：%s" % SUBMIT)
    print("")
    for line in lines:
        print(line)
    print("")
    print("---SUBMISSION_SUMMARY---")
    if missing:
        print("READY: no")
        print("MISSING: %d" % len(missing))
        for item in missing:
            print("  - " + item)
    else:
        print("READY: yes")
        print("MISSING: 0")
    print("---END---")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
