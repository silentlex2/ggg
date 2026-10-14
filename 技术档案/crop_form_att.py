# -*- coding: utf-8 -*-
"""裁剪截图：去掉左侧会话栏与右侧空白，只留聊天内容区，统一宽度 784。"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

D = "F:/zcode/suiyi/ggg/参赛方案/提交材料/"
OUT = "F:/zcode/suiyi/ggg/过程截图/2026-10-15-v7e/提交表配图/"
os.makedirs(OUT, exist_ok=True)

# (源文件, y0, y1)
JOBS = [
    ("作品截图-01.png", 8, 1588),
    ("作品截图-02.png", 8, 1645),
    ("作品截图-03.png", 8, 1490),
    ("作品截图-05.png", 8, 1588),
    ("作品截图-07.png", 60, 1280),
]
NAMES = ["配图-01-首页.png","配图-02-简历诊断.png","配图-03-岗位匹配.png","配图-04-面试复盘.png","配图-05-政策咨询.png"]
X0, X1 = 466, 1254
for i, (fn, y0, y1) in enumerate(JOBS, 1):
    im = Image.open(D+fn).convert("RGB")
    c = im.crop((X0, y0, X1, y1))
    out = os.path.join(OUT, NAMES[i-1])
    c.save(out)
    print(f"{NAMES[i-1]} <- {fn}  {c.size}  ratio h/w={c.size[1]/c.size[0]:.3f}")
