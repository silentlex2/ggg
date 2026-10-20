# -*- coding: utf-8 -*-
"""按 readysite.txt 重出公开站点二维码，并当场解码回验。

站点码只有 readysite.txt 一个真源；这个脚本不再自己拼地址。
旧二维码历史不再留 .bak —— 参赛方案/素材/职引-二维码-公开站点.png 已被 git 跟踪，
需要旧版本时用 git 取。

用法：
    python make_qr.py
"""
import io
import os
import sys

import cv2
import numpy as np
import qrcode

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()
URL = "https://aiagent.cqut.edu.cn:31134/chat/%s" % SITE
TARGET = os.path.join(ROOT, "参赛方案", "素材", "职引-二维码-公开站点.png")


def main():
    if not SITE:
        sys.exit("readysite.txt 为空")
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1d4ed8", back_color="white")
    img.save(TARGET)
    print("已生成 %s  (%d 字节)" % (TARGET, os.path.getsize(TARGET)))
    print("URL: %s" % URL)

    # 解码回验（Windows 中文路径必须走 fromfile/imdecode，imread 会失败）
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(
        cv2.imdecode(np.fromfile(TARGET, dtype=np.uint8), cv2.IMREAD_COLOR))
    print("解码回验: %s" % (data or "(识别失败)"))
    if data != URL:
        sys.exit("二维码内容与 readysite.txt 不一致，停止")
    print("OK")


if __name__ == "__main__":
    main()
