# -*- coding: utf-8 -*-
"""自建前端静态体检（h5_lint.py）

为什么要有：`前端/职引-H5.html` 是单文件、直连平台接口的页面，没有构建步骤、
没有依赖管理，改坏了浏览器不报错、只是某块功能静默失效。这里把能静态查的全查掉。

查这些东西：
  1. 脚本语法：抽出 <script> 交给 `node --check`
  2. 站点码：文件里写死的 /chat/<站点码> 必须等于 readysite.txt 真源
     ——站点一换、页面里还指着旧站，打开就是 404，而且改的人往往只改 readysite.txt
  3. 外链自足：不许引 CDN / 外部字体 / 外部脚本，否则离线或校园网受限时整页白屏
  4. 接口域名：所有 https:// 只能指向平台域名（防止残留测试地址）
  5. 已知回归：.attach 用了 display:flex 就必须有 .attach[hidden]{display:none} 兜底
     ——hidden 属性会被 display 规则盖掉，我们为这个 bug 单独修过一次
  6. 无障碍底线：<html lang>、viewport、button 有文字或 aria-label
  7. 体积预算：超过 60 KB 报 WARN（单文件还能接受，再大就该拆了）

用法：
    python h5_lint.py            # 体检，退出码 0 = 通过 / 1 = 有 FAIL
    python h5_lint.py --extract  # 顺带把脚本抽到 scratch/h5-script.js（改代码时用）
    python h5_lint.py --file 别的.html   # 体检别的副本（自测/线上抓回来的页面都行）

输出契约：
    ---H5_LINT---
    LINES: 619
    BYTES: 31265
    PLATFORM: YnmaDNCRpd1otyrC
    FAIL: 0
    WARN: 0
    ---END---
"""
import io
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "..", "前端", "职引-H5.html")
SITE_FILE = os.path.join(HERE, "readysite.txt")
PLATFORM_HOST = "aiagent.cqut.edu.cn:31134"
SIZE_WARN = 60 * 1024

fails, warns = [], []


def fail(msg):
    print("  FAIL  %s" % msg)
    fails.append(msg)


def warn(msg):
    print("  WARN  %s" % msg)
    warns.append(msg)


def ok(msg):
    print("  PASS  %s" % msg)


def read_site():
    try:
        with io.open(SITE_FILE, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def check_script(html, extract=False):
    print("\n[1] 脚本语法")
    blocks = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not blocks:
        fail("没有内联 <script> 块")
        return
    js = "\n".join(blocks)
    ok("内联脚本 %d 块，共 %d 行" % (len(blocks), js.count("\n") + 1))
    if extract:
        out = os.path.join(HERE, "scratch", "h5-script.js")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        io.open(out, "w", encoding="utf-8", newline="\n").write(js)
        print("  已抽出 -> %s" % os.path.relpath(out, HERE))
    node = shutil.which("node")
    if not node:
        warn("本机没有 node，跳过 node --check（语法错误查不出来）")
        return
    tmp = os.path.join(HERE, "scratch", ".h5-syntax-check.js")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(js)
    p = subprocess.run([node, "--check", tmp], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    try:
        os.remove(tmp)
    except OSError:
        pass
    if p.returncode == 0:
        ok("node --check 通过")
    else:
        fail("node --check 失败：%s" % (p.stderr or p.stdout).strip()[:300])


def check_site(html):
    print("\n[2] 站点码")
    site = read_site()
    if not site:
        fail("readysite.txt 为空，无法校验页面指向")
        return ""
    hits = re.findall(r"/chat/([A-Za-z0-9]+)", html)
    if not hits:
        warn("页面里没有 /chat/<站点码> 形式的平台入口链接")
        return site
    uniq = sorted(set(hits))
    if uniq == [site]:
        ok("页面里的平台入口指向当前站点：%s" % site)
    else:
        fail("页面里的站点码 %s 与 readysite.txt（%s）不一致" % (uniq, site))
    return site


def check_offline(html):
    print("\n[3] 外链自足")
    bad = []
    for m in re.finditer(r'<(script|link|img|iframe|audio|video|source)\b[^>]*\b(?:src|href)\s*=\s*["\'](https?://[^"\']+)', html, re.I):
        url = m.group(2)
        if PLATFORM_HOST not in url:
            bad.append(m.group(1) + " -> " + url)
    if re.search(r"@import\s+url\(\s*['\"]?https?://", html, re.I):
        bad.append("@import 外部样式")
    if re.search(r"fonts\.googleapis|fonts\.gstatic|cdn\.jsdelivr|unpkg\.com|cdnjs", html, re.I):
        bad.append("引用公共 CDN / 外部字体")
    if bad:
        fail("存在外部资源依赖（离线会白屏）：%s" % "；".join(bad[:5]))
    else:
        ok("无外部脚本 / 样式 / 字体依赖，单文件自足")


def check_hosts(html):
    print("\n[4] 接口域名")
    hosts = sorted(set(re.findall(r"https://([A-Za-z0-9.:_-]+)", html)))
    odd = [h for h in hosts if h.rstrip("/") != PLATFORM_HOST]
    if odd:
        fail("出现平台以外的域名：%s" % odd)
    else:
        ok("所有 https 地址都指向 %s（共 %d 处）" % (PLATFORM_HOST, len(hosts)))


def check_attach(html):
    print("\n[5] 已知回归：.attach 的 hidden 兜底")
    if not re.search(r"\.attach\s*\{[^}]*display\s*:\s*flex", html, re.S):
        ok(".attach 没有用 display 覆盖 hidden，无需兜底")
        return
    if re.search(r"\.attach\[hidden\][^{]*\{[^}]*display\s*:\s*none", html, re.S):
        ok(".attach 有 [hidden]{display:none} 兜底")
    else:
        fail(".attach 用 display:flex 会盖掉 hidden 属性，但缺少 .attach[hidden]{display:none}")


def check_a11y(html):
    print("\n[6] 无障碍底线")
    if re.search(r'<html[^>]*\blang\s*=', html, re.I):
        ok("<html> 有 lang 属性")
    else:
        fail("<html> 缺 lang 属性（读屏与搜索引擎都按它判断语言）")
    if re.search(r'<meta[^>]+name\s*=\s*["\']viewport', html, re.I):
        ok("有 viewport meta")
    else:
        fail("缺 viewport meta（手机上会按 980px 缩放）")
    # 图标按钮必须带 aria-label：取 <button ...> 开标签里只有图标没有文字的
    bare = []
    for m in re.finditer(r"<button\b([^>]*)>(.*?)</button>", html, re.S):
        attrs, inner = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if inner:
            continue
        if re.search(r"aria-label\s*=", attrs):
            continue
        bare.append(m.group(0)[:60])
    if bare:
        fail("有 %d 个无文字且无 aria-label 的按钮：%s" % (len(bare), bare[:3]))
    else:
        ok("按钮都有可读文本或 aria-label")


def main():
    args = sys.argv[1:]
    extract = "--extract" in args
    target = HTML
    if "--file" in args:
        target = args[args.index("--file") + 1]
        if not os.path.isabs(target):
            target = os.path.join(os.getcwd(), target)
    if not os.path.exists(target):
        print("找不到前端文件：%s" % target)
        return 1
    html = io.open(target, encoding="utf-8").read()
    raw = html.encode("utf-8")
    try:
        shown = os.path.relpath(target, HERE)
    except ValueError:          # 跨盘符时 relpath 会抛，退回绝对路径
        shown = target
    print("体检对象：%s" % shown)
    print("行数 %d，字节 %d" % (html.count("\n") + 1, len(raw)))

    check_script(html, extract)
    site = check_site(html)
    check_offline(html)
    check_hosts(html)
    check_attach(html)
    check_a11y(html)

    print("\n[7] 体积预算")
    if len(raw) > SIZE_WARN:
        warn("文件 %.1f KB 超过 %.0f KB 预算，考虑拆分" % (len(raw) / 1024.0, SIZE_WARN / 1024.0))
    else:
        ok("文件 %.1f KB，在 %.0f KB 预算内" % (len(raw) / 1024.0, SIZE_WARN / 1024.0))

    print("\n---H5_LINT---")
    print("LINES: %d" % (html.count("\n") + 1))
    print("BYTES: %d" % len(raw))
    print("PLATFORM: %s" % site)
    print("FAIL: %d" % len(fails))
    print("WARN: %d" % len(warns))
    print("---END---")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
