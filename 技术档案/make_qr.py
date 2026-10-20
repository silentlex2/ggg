# -*- coding: utf-8 -*-
"""二维码生成器：默认按 readysite.txt 出平台站点码，也可以给任意地址出码。

站点码只有 readysite.txt 一个真源；默认模式不再自己拼地址。
旧二维码历史不再留 .bak —— 参赛方案/素材/职引-二维码-公开站点.png 已被 git 跟踪，
需要旧版本时用 git 取。

用法：
    python make_qr.py                                   # 平台站点（写进 参赛方案/素材/）
    python make_qr.py --url https://example.com/x.html   # 任意地址（默认写到 前端/）
    python make_qr.py --url ... --out 某路径.png          # 指定输出
    python make_qr.py --print-url                        # 只打印当前平台地址，不出码

注意：`参赛方案/素材/` 里只允许有一张二维码（check_assets.py 会校验“只有 1 张，无歧义”），
所以 --url 模式默认写到 `前端/` 目录，避免把素材目录弄脏。
"""
import argparse
import io
import os
import sys

import cv2
import numpy as np
import qrcode

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE_FILE = os.path.join(HERE, "readysite.txt")
SITE = open(SITE_FILE, encoding="utf-8").read().strip()
PLATFORM_URL = "https://aiagent.cqut.edu.cn:31134/chat/%s" % SITE
DEFAULT_OUT = os.path.join(ROOT, "参赛方案", "素材", "职引-二维码-公开站点.png")
FRONTEND_DIR = os.path.join(ROOT, "前端")


def make(url, target):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1d4ed8", back_color="white")
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    img.save(target)
    print("已生成 %s  (%d 字节)" % (target, os.path.getsize(target)))
    print("URL: %s" % url)

    # 解码回验（Windows 中文路径必须走 fromfile/imdecode，imread 会失败）
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(
        cv2.imdecode(np.fromfile(target, dtype=np.uint8), cv2.IMREAD_COLOR))
    print("解码回验: %s" % (data or "(识别失败)"))
    if data != url:
        sys.exit("二维码内容与目标地址不一致，停止")
    print("OK")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="要编码的地址；不给就用 readysite.txt 的平台站点地址")
    parser.add_argument("--out", help="输出 png 路径")
    parser.add_argument("--print-url", action="store_true", help="只打印当前平台地址")
    args = parser.parse_args()

    if not SITE:
        sys.exit("readysite.txt 为空")

    if args.print_url:
        print(PLATFORM_URL)
        return 0

    if args.url:
        target = args.out or os.path.join(FRONTEND_DIR, "职引-二维码-前端.png")
        return make(args.url, target)

    if args.out and args.out != DEFAULT_OUT:
        sys.exit("给了 --out 却没给 --url：改用 --url 指定地址，或去掉 --out 走平台站点默认输出")
    return make(PLATFORM_URL, DEFAULT_OUT)


if __name__ == "__main__":
    raise SystemExit(main())
