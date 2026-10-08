#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「职引」的 LOGO / 会话背景渲染成 PNG（纯标准库，无需 PIL / rsvg / inkscape）。

用法：
    python3 make-png.py

产出（与 SVG 同一套配色，可直接上传平台）：
    职引-LOGO-512.png        512 x 512   应用头像（罗盘 + 向上箭头，不含文字）
    职引-背景-1200x900.png   1200 x 900  会话背景（浅色低对比）

说明：
- 抗锯齿用超采样实现（LOGO 3x3、背景 2x2）。
- 中文字形无法在无字体环境绘制，所以 PNG 版 LOGO **只含图形标记**；
  需要带「职引」二字的版本请用 `职引-LOGO.svg`（浏览器打开后另存为图片）。
"""
import math
import os
import struct
import sys
import zlib

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BRAND_1 = (0x0e, 0xa5, 0xa4)   # #0ea5a4
BRAND_2 = (0x25, 0x63, 0xeb)   # #2563eb


def write_png(path, width, height, rows):
    """rows: list[bytes]，每行 RGB，长度 = width*3"""
    raw = b''.join(b'\x00' + r for r in rows)

    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', ihdr)
           + chunk(b'IDAT', zlib.compress(raw, 9))
           + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)
    return os.path.getsize(path)


def mix(c1, c2, t):
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * t)) for i in range(3))


def over(bg, fg, alpha):
    if alpha <= 0:
        return bg
    if alpha >= 1:
        return fg
    return tuple(int(round(bg[i] * (1 - alpha) + fg[i] * alpha)) for i in range(3))


def in_rounded_rect(x, y, w, h, r):
    cx = min(max(x, r), w - r)
    cy = min(max(y, r), h - r)
    if r <= 0:
        return 0 <= x <= w and 0 <= y <= h
    dx, dy = x - cx, y - cy
    if x < r or x > w - r:
        if y < r or y > h - r:
            return dx * dx + dy * dy <= r * r
    return 0 <= x <= w and 0 <= y <= h


def in_ring(x, y, cx, cy, radius, thick):
    return abs(math.hypot(x - cx, y - cy) - radius) <= thick / 2.0


def in_circle(x, y, cx, cy, radius):
    return math.hypot(x - cx, y - cy) <= radius


def in_poly(x, y, pts):
    inside = False
    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y):
            xint = (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi
            if x < xint:
                inside = not inside
        j = i
    return inside


def _seg_dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def render_logo(size=512):
    R = size * 0.219        # 圆角半径（SVG rx=112/512）
    cx = cy = size / 2.0
    ring_r = size * 0.258   # 罗盘外环半径（132/512）
    ring_t = size * 0.031   # 环宽（16/512）

    arrow = [(size * 0.500, size * 0.289),
             (size * 0.645, size * 0.562),
             (size * 0.500, size * 0.504),
             (size * 0.355, size * 0.562)]
    hub_r = size * 0.035    # 中心圆点（18/512）

    ticks = []
    for (x1, y1, x2, y2) in [(256, 104, 256, 130), (256, 366, 256, 392),
                             (112, 248, 138, 248), (374, 248, 400, 248)]:
        ticks.append((size * x1 / 512.0, size * y1 / 512.0,
                      size * x2 / 512.0, size * y2 / 512.0))

    def sample(px, py):
        if not in_rounded_rect(px, py, size, size, R):
            return (255, 255, 255), 1.0
        t = min(1.0, max(0.0, (px / size + py / size) / 2.0))
        col = mix(BRAND_1, BRAND_2, t)

        if py < size * 0.6:                      # 顶部高光
            col = over(col, (255, 255, 255), 0.28 * (1 - py / (size * 0.6)))

        for (x1, y1, x2, y2) in ticks:
            if _seg_dist(px, py, x1, y1, x2, y2) <= size * 0.0098:
                col = over(col, (255, 255, 255), 0.55)

        if in_ring(px, py, cx, cy, ring_r, ring_t):
            col = over(col, (255, 255, 255), 0.90)

        if in_poly(px, py, arrow):
            col = over(col, (255, 255, 255), 1.0)
        if in_circle(px, py, cx, cy, hub_r):
            col = over(col, (255, 255, 255), 1.0)

        return col, 1.0

    return _render(size, size, sample, ss=3)


def render_bg(w=1200, h=900):
    blobs = [(140, 120, 220, 0.10), (1080, 780, 280, 0.10), (980, 140, 110, 0.10)]
    arrow = [(1010, 104), (1054, 220), (1010, 200), (966, 220)]

    def sample(px, py):
        t = min(1.0, max(0.0, (px / w + py / h) / 2.0))
        col = mix((0xf6, 0xfb, 0xfb), (0xee, 0xf4, 0xff), t)

        for (bx, by, br, ba) in blobs:
            d = math.hypot(px - bx, py - by)
            if d < br:
                col = over(col, BRAND_2, ba * (1 - (d / br) ** 2))

        if in_ring(px, py, 1010, 180, 96, 10):      # 右上角罗盘轮廓（淡化）
            col = over(col, BRAND_2, 0.16)
        if in_poly(px, py, arrow):
            col = over(col, BRAND_2, 0.16)

        if py >= h - 24:                            # 底部渐变线
            col = over(col, mix(BRAND_1, BRAND_2, px / float(w)), 0.35)

        return col, 1.0

    return _render(w, h, sample, ss=2)


def _render(w, h, sample, ss=2):
    rows = []
    n = ss * ss
    for y in range(h):
        row = bytearray()
        for x in range(w):
            r = g = b = 0.0
            for sy in range(ss):
                for sx in range(ss):
                    (cr, cg, cb), a = sample(x + (sx + 0.5) / ss, y + (sy + 0.5) / ss)
                    r += cr * a
                    g += cg * a
                    b += cb * a
            row += bytes((int(min(255, r / n)), int(min(255, g / n)), int(min(255, b / n))))
        rows.append(bytes(row))
        if y % 120 == 0:
            sys.stderr.write('\r  ... %d/%d' % (y, h))
    sys.stderr.write('\r')
    return rows


def main():
    print('渲染 LOGO 512x512 ...')
    rows = render_logo(512)
    p = os.path.join(OUT_DIR, '职引-LOGO-512.png')
    print('  ->', os.path.basename(p), write_png(p, 512, 512, rows), 'bytes')

    print('渲染 会话背景 1200x900 ...')
    rows = render_bg(1200, 900)
    p = os.path.join(OUT_DIR, '职引-背景-1200x900.png')
    print('  ->', os.path.basename(p), write_png(p, 1200, 900, rows), 'bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main())

