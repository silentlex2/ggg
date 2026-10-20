# -*- coding: utf-8 -*-
"""凭据泄露检查（check-secrets.py）

为什么要有：这个仓库里有两种"看着像密钥"的东西，性质完全不同——
  · 站点码 / 应用密钥：本来就是公开的（站点码就是 URL，H5 静态页必须内嵌 app key 才能调 /v1），
    泄露不算事故，控制台随时可吊销；
  · 控制台 token（535 字符 JWT）与模型供应商 Key：**拿到就能操作整个租户**，绝不能进仓库。

人肉检查靠不住，所以这里按 git 跟踪清单扫一遍：
  1. 本地 .token 里的控制台 token 不得出现在任何被跟踪文件里（按精确值比对）
  2. 任何形如 JWT 的串（eyJ...）都当控制台 token 处理
  3. sk- 开头的模型供应商 Key
  4. app- 开头的应用密钥：只允许出现在 H5（公开静态页，设计如此），其它位置报 WARN

用法：
    python 参赛方案/tools/check-secrets.py           # 扫 git 跟踪的文件
    python 参赛方案/tools/check-secrets.py --all     # 连未跟踪的工作区文件一起扫

契约：
    ---SECRETS---
    SCANNED: 132
    TOKEN_VALUE_HITS: 0
    JWT_HITS: 0
    SK_HITS: 0
    APP_KEY_WARN: 2
    SECRETS_OK: yes
    ---END---

退出码：0 = 干净；1 = 发现控制台 token / JWT / sk- 泄露。
"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TOKEN_FILE = os.path.join(REPO, "技术档案", ".token")

TEXT_EXT = {".py", ".js", ".md", ".html", ".htm", ".json", ".txt", ".yml", ".yaml",
            ".sh", ".ps1", ".csv", ".sql", ".toml", ".ini", ".cfg"}
SKIP_DIRS = {"node_modules", ".git", "__pycache__", "scratch"}

APP_KEY_ALLOWED_IN = {os.path.join("前端", "职引-H5.html")}

JWT_RE = re.compile(r"eyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{8,}")
SK_RE = re.compile(r"\bsk-[A-Za-z0-9]{16,}")
APP_RE = re.compile(r"\bapp-[A-Za-z0-9]{16,}")


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True)
        names = [n for n in out.stdout.decode("utf-8", "replace").split("\0") if n]
        if names:
            return [os.path.join(REPO, n) for n in names]
    except OSError:
        pass
    return []


def walk_files():
    found = []
    for dirpath, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            found.append(os.path.join(dirpath, fn))
    return found


def rel(path):
    return os.path.relpath(path, REPO).replace(os.sep, "/")


def read_token():
    try:
        with open(TOKEN_FILE, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def main():
    scan_all = "--all" in sys.argv[1:]
    files = walk_files() if scan_all else (tracked_files() or walk_files())
    token = read_token()

    token_hits, jwt_hits, sk_hits, app_warns = [], [], [], []
    scanned = 0
    for path in files:
        ext = os.path.splitext(path)[1].lower()
        if ext not in TEXT_EXT:
            continue
        try:
            if os.path.getsize(path) > 2 * 1024 * 1024:
                continue
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        scanned += 1
        name = rel(path)
        if token and token in text:
            token_hits.append(name)
        for m in JWT_RE.finditer(text):
            if not (token and m.group(0) in token):
                jwt_hits.append("%s: %s…" % (name, m.group(0)[:12]))
        for m in SK_RE.finditer(text):
            sk_hits.append("%s: %s…" % (name, m.group(0)[:8]))
        if name.replace("/", os.sep) not in APP_KEY_ALLOWED_IN:
            for m in APP_RE.finditer(text):
                app_warns.append("%s: %s…" % (name, m.group(0)[:10]))

    for hit in token_hits:
        print("  FAIL  控制台 token 明文出现在：%s" % hit)
    for hit in jwt_hits:
        print("  FAIL  疑似 JWT/控制台 token：%s" % hit)
    for hit in sk_hits:
        print("  FAIL  疑似模型供应商 Key：%s" % hit)
    for hit in app_warns:
        print("  WARN  应用密钥出现在非 H5 位置（公开密钥，确认一下就好）：%s" % hit)

    bad = bool(token_hits or jwt_hits or sk_hits)
    if not bad:
        print("  凭据检查通过：扫描 %d 个文本文件，没有控制台 token / JWT / sk- 泄露" % scanned)

    print("")
    print("---SECRETS---")
    print("SCANNED: %d" % scanned)
    print("TOKEN_VALUE_HITS: %d" % len(token_hits))
    print("JWT_HITS: %d" % len(jwt_hits))
    print("SK_HITS: %d" % len(sk_hits))
    print("APP_KEY_WARN: %d" % len(app_warns))
    print("SECRETS_OK: %s" % ("no" if bad else "yes"))
    print("---END---")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())