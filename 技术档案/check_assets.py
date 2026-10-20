# -*- coding: utf-8 -*-
"""职引 · 资产一致性校验（check_assets.py）

一条命令把「同一事实的 5 份副本」对齐：二维码 / Markdown / 提交表 DOCX /
提交表 PDF / 素材目录里的二维码文件数量。任何一处还指着旧站点码，都算不一致。

用法：
    python check_assets.py             # 任意目录执行均可
    python check_assets.py --quiet     # 只打印结论与契约块，不打印逐处明细

判定口径（为什么只对「标签」报错）：
    历史站点码本身允许存在——交接说明的版本链、回退站清单本来就要留旧码。
    真正危险的是「旧码被贴在『当前 / 正式 / 公开站点』这类标签后面」，
    因为那一份才会被人抄进材料、扫给评委。所以：
        站点码 == readysite                          -> [当前]  通过
        站点码 != readysite，无当前标签 / 在归档文件 -> [历史]  只登记不报错
        站点码 != readysite，同行有当前标签          -> [错标]  计一次 MISMATCH
    归档文件 = 文件名含「历史」（如 参赛方案/历史-运行状态与待办.md）。

Windows 注意：PNG 一律 np.fromfile + cv2.imdecode。
    cv2.imread 走的是 ANSI 路径转换，中文路径上会静默返回 None（不报错、直接判空），
    所以本文件绝不使用 cv2.imread。

退出码：0 = 无 FAIL；1 = 有 FAIL（存在实质不一致）。
输出末尾固定契约块，可被 release.py / CI grep：
    ---ASSET_SUMMARY---
    RESULT: PASS|FAIL
    SITE: <readysite>
    MISMATCHES: <n>        # n = 具体不一致条目数（逐处计，不是文件数）
    ---END---
"""
import glob
import html
import os
import re
import sys
import zipfile
import zlib

sys.stdout.reconfigure(encoding="utf-8")   # 中文输出与 run_all.py 一致，统一 UTF-8

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BASE = "https://aiagent.cqut.edu.cn:31134"
HOST_FRAG = "aiagent.cqut.edu.cn:31134"
HOST_BYTES = HOST_FRAG.encode()

READY_PATH = os.path.join(HERE, "readysite.txt")
DOCX = os.path.join(ROOT, "参赛方案", "提交材料", "作品提交表-职引.docx")
PDF = os.path.join(ROOT, "参赛方案", "提交材料", "作品提交表-职引.pdf")
ASSET_DIR = os.path.join(ROOT, "参赛方案", "素材")
QR_NAME = "职引-二维码-公开站点.png"

# 站点码在不同地方出现过 12 位与 16 位两种描述，这里统一按 10~32 位抓取再整串比对。
CHAT_RE = re.compile(r"/chat/([A-Za-z0-9]{10,32})")
CHAT_BYTES = re.compile(rb"/chat/([A-Za-z0-9]{10,32})")
IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

# 「这一行在讲当前地址」的标签
CURRENT_LABELS = ("当前", "正式", "最新", "公开站点", "公开地址", "公开访问地址",
                  "对外地址", "作品地址", "材料正式地址", "二维码指向", "提交表必填",
                  "浏览器打开")
# 「这一行在讲历史」的标签（优先级高于当前标签：归档行的「正式站」不算错标）
ARCHIVE_LABELS = ("历史", "回退", "已关停", "追溯", "不要当", "旧站", "旧版",
                  "废弃", "作废", "版本链", "已被取代")


# ---------------------------------------------------------------- 基础设施
def read_site(path=None):
    """读站点码唯一真源 readysite.txt；缺失/为空返回空串（由调用方判 FAIL）。"""
    path = path or READY_PATH
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


class Tally(object):
    """收集每项结论，顺便数 FAIL / WARN / 不一致条目。"""

    def __init__(self, quiet=False):
        self.quiet = quiet
        self.mismatches = 0
        self.fails = 0
        self.warns = 0
        self.fix_hints = []      # 结尾「待修」清单

    def ok(self, msg):
        print("  PASS  %s" % msg)

    def warn(self, msg, hint=None):
        self.warns += 1
        print("  WARN  %s" % msg)
        if hint:
            self.fix_hints.append(hint)

    def fail(self, msg, n=1, hint=None):
        self.fails += 1
        self.mismatches += max(1, n)
        print("  FAIL  %s" % msg)
        if hint:
            self.fix_hints.append(hint)

    def note(self, msg):
        if not self.quiet:
            print("        %s" % msg)


def section(no, total, title):
    print()
    print("-" * 72)
    print("[%d/%d] %s" % (no, total, title))


def classify(relpath, line, code, ready):
    """把一处站点码出现归成 当前 / 历史 / 错标。"""
    if code == ready:
        return "当前"
    if "历史" in os.path.basename(relpath):
        return "历史"
    low = line
    if any(k in low for k in ARCHIVE_LABELS):
        return "历史"
    if any(k in low for k in CURRENT_LABELS):
        return "错标"
    return "历史"


# ---------------------------------------------------------------- 1. 二维码
def decode_qr(path):
    """解一张二维码 -> (文本, 图像尺寸元组)。读不到或解不出返回 ("", None)。

    Windows 中文路径必须 np.fromfile + cv2.imdecode，imread 会静默失败。
    """
    try:
        import numpy as np
        import cv2
    except ImportError:
        return "", None
    try:
        buf = np.fromfile(path, dtype=np.uint8)
    except (OSError, ValueError):
        return "", None
    if buf.size == 0:
        return "", None
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if img is None:
        return "", None
    shape = img.shape
    det = cv2.QRCodeDetector()
    try:
        data, _, _ = det.detectAndDecode(img)
    except cv2.error:
        data = ""
    if not data:
        # 小图 / 深色码在灰度下更好解，放大一倍再试一次（INTER_NEAREST 不糊边）
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
            data, _, _ = det.detectAndDecode(gray)
        except cv2.error:
            data = ""
    return (data or "").strip(), shape


def check_qr(ready, t):
    """检查 1：二维码解码结果必须等于 readysite。"""
    section(1, 5, "二维码 · 参赛方案/素材/%s" % QR_NAME)
    path = os.path.join(ASSET_DIR, QR_NAME)
    if not os.path.exists(path):
        t.fail("二维码文件不存在：%s" % path, hint="重出二维码：python 技术档案/release.py ... 或 python 技术档案/scratch/make_qr.py")
        return
    data, shape = decode_qr(path)
    if not data:
        t.fail("%s 存在但解不出二维码（形状 %s）" % (QR_NAME, shape),
               hint="二维码图片损坏或被覆盖；用 scratch/make_qr.py 重出")
        return
    t.ok("解码成功 %s×%s -> %s" % (shape[1], shape[0], data))
    m = CHAT_RE.search(data)
    if not m:
        t.fail("二维码内容不是 /chat/<站点码> 形式的地址：%s" % data,
               hint="二维码指向的不是公开站点聊天页")
        return
    code = m.group(1)
    if code == ready:
        t.ok("站点码一致：%s == readysite" % code)
    else:
        t.fail("站点码不一致：二维码=%s  readysite=%s" % (code, ready),
               hint="二维码指向旧站点，扫码后是旧版页面；重出二维码")


# ---------------------------------------------------------------- 2. Markdown
def scan_markdown(ready, t=None):
    """扫 交接说明.md + 参赛方案/**/*.md 里所有 /chat/<站点码>，返回逐处明细。"""
    files = [os.path.join(ROOT, "交接说明.md")]
    files += sorted(glob.glob(os.path.join(ROOT, "参赛方案", "**", "*.md"), recursive=True))
    files = [f for f in files if os.path.isfile(f)]
    rows = []
    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            for m in CHAT_RE.finditer(line):
                code = m.group(1)
                rows.append({"file": rel, "line": i, "code": code,
                             "verdict": classify(rel, line, code, ready),
                             "context": line.strip()})
    return rows, len(files)


def check_markdown(ready, t):
    """检查 2：Markdown 里的站点码；只有「错标」才 FAIL。"""
    section(2, 5, "Markdown 站点码（交接说明.md + 参赛方案/**/*.md）")
    rows, nfiles = scan_markdown(ready)
    if not rows:
        t.fail("一个 /chat/ 地址都没扫到（%d 个文件）" % nfiles,
               hint="文档里的公开地址被删了？")
        return
    counts = {}
    for r in rows:
        counts[r["code"]] = counts.get(r["code"], 0) + 1
    t.note("扫了 %d 个文件，命中 %d 处，涉及 %d 个站点码：" % (nfiles, len(rows), len(counts)))
    for code, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        mark = "← readysite" if code == ready else "[历史]"
        t.note("  %-20s %2d 处  %s" % (code, n, mark))
    t.note("")
    t.note("逐处明细：")
    bad = []
    for r in rows:
        tag = {"当前": "[当前]", "历史": "[历史]", "错标": "[错标]"}[r["verdict"]]
        t.note("%s %s:%d  %s" % (tag, r["file"], r["line"], r["context"][:120]))
        if r["verdict"] == "错标":
            bad.append(r)
    if not any(r["code"] == ready for r in rows):
        t.fail("全文没有一处出现当前站点码 %s" % ready,
               hint="文档里的公开地址整体过期")
        return
    if bad:
        t.fail("%d 处把旧站点码标成「当前/正式/公开站点」" % len(bad), n=len(bad),
               hint="改下列行：" + "；".join("%s:%d(%s)" % (r["file"], r["line"], r["code"]) for r in bad))
        for r in bad:
            t.note("  ↑ %s:%d 标了当前/正式，但站点码 %s != %s" % (r["file"], r["line"], r["code"], ready))
    else:
        t.ok("没有把旧站点码标成当前/正式的行（历史码 %d 处，允许保留）"
             % sum(1 for r in rows if r["verdict"] == "历史"))


# ---------------------------------------------------------------- 3. DOCX
def docx_text(path):
    """取 docx 正文：解 zip 读 word/document.xml，段落断行后去标签。"""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    xml = xml.replace("</w:p>", "\n").replace("<w:br/>", "\n").replace("<w:tab/>", " ")
    text = re.sub(r"<[^>]+>", "", xml)
    return html.unescape(text)


def check_docx(ready, t):
    """检查 3：提交表 docx 的作品地址必须等于 readysite。"""
    section(3, 5, "提交表 DOCX · 参赛方案/提交材料/%s" % os.path.basename(DOCX))
    if not os.path.exists(DOCX):
        t.warn("docx 不存在（提交材料被 .gitignore 排除时正常），跳过")
        return
    try:
        text = docx_text(DOCX)
    except (zipfile.BadZipFile, KeyError, OSError) as e:
        t.fail("docx 解析失败：%s" % e)
        return
    lines = text.splitlines()
    hits = []
    for i, line in enumerate(lines, 1):
        hits += [(i, m.group(1), line.strip()) for m in CHAT_RE.finditer(line)]
    hosts = text.count(HOST_FRAG)
    t.note("正文 %d 字 / %d 段；命中 /chat/ %d 处，平台域名 %d 处"
           % (len(text), len(lines), len(hits), hosts))
    if not hits:
        if hosts:
            t.fail("docx 有平台域名（%d 处）但抓不到完整 /chat/<站点码>（可能被拆成多个 run）"
                   % hosts, hint="手工核对 docx 的「作品地址」一格")
        else:
            t.warn("docx 里没有作品地址（提交表还没填？），无法比对",
                   hint="提交表「作品地址」必须填 %s/chat/%s" % (BASE, ready))
        return
    bad = 0
    for ln, code, ctx in hits:
        if code == ready:
            t.ok("第 %d 段作品地址 = %s（readysite）" % (ln, code))
        else:
            bad += 1
            t.fail("第 %d 段作品地址 = %s != readysite %s" % (ln, code, ready), n=1,
                   hint="改 docx 的「作品地址」段落 -> %s/chat/%s，再由 docx 重出 PDF" % (BASE, ready))
            t.note("  原文：%s" % ctx[:160])
    if not bad and hits:
        t.ok("docx 作品地址与 readysite 一致")


# ---------------------------------------------------------------- 4. PDF
def pdf_blocks(path):
    """读 PDF：返回 (原始字节, 解压后的流列表)。"""
    with open(path, "rb") as f:
        raw = f.read()
    blobs = []
    for m in re.finditer(rb"stream\r?\n", raw):
        start = m.end()
        end = raw.find(b"endstream", start)
        if end < 0:
            continue
        try:
            blobs.append(zlib.decompress(raw[start:end]))
        except zlib.error:
            continue
    return raw, blobs


def check_pdf(ready, t):
    """检查 4：PDF 二进制扫 ASCII，找 chat/<站点码>。"""
    section(4, 5, "提交表 PDF · 参赛方案/提交材料/%s" % os.path.basename(PDF))
    if not os.path.exists(PDF):
        t.warn("pdf 不存在，跳过")
        return
    try:
        raw, blobs = pdf_blocks(PDF)
    except OSError as e:
        t.fail("pdf 读不了：%s" % e)
        return
    codes, hosts = set(), 0
    for blob in [raw] + blobs:
        codes |= {m.group(1).decode() for m in CHAT_BYTES.finditer(blob)}
        hosts += blob.count(HOST_BYTES)
    t.note("文件 %d 字节 / 解压出 %d 个内容流；ASCII 命中 /chat/ %d 个、平台域名 %d 处"
           % (len(raw), len(blobs), len(codes), hosts))
    if not codes:
        why = ("PDF 正文由字体子集（Type0 / CIDFontType2）编码且不带 ToUnicode，"
               "字符不落 ASCII，离线扫不出来")
        t.warn("扫不到 /chat/ 地址：%s" % why,
               hint="PDF 无法离线校验；docx 改完后用 WPS 重新导出 PDF，再跑一次本脚本")
        if hosts:
            t.note("（但平台域名是可读的，说明只是文字被编码，不是没地址）")
        return
    bad = [c for c in codes if c != ready]
    if bad:
        t.fail("PDF 里的站点码 %s != readysite %s" % (sorted(codes), ready), n=len(bad),
               hint="由改好的 docx 重新导出 PDF")
    elif ready in codes:
        t.ok("PDF 站点码 = %s（readysite）" % ready)


# ---------------------------------------------------------------- 5. 多张二维码
def qr_scan(directory):
    """列目录下所有能解出二维码的图片 -> [(路径, 内容)]。"""
    found = []
    for dirpath, _, files in os.walk(directory):
        for fn in files:
            if not fn.lower().endswith(IMG_EXT):
                continue            # .bak / 无扩展名不扫
            path = os.path.join(dirpath, fn)
            data, _ = decode_qr(path)
            if data:
                found.append((path, data))
    return found


def check_qr_files(ready, t):
    """检查 5：素材目录里不能有多个二维码文件（之前就是多个 QR 打架）。"""
    section(5, 5, "素材目录二维码数量 · 参赛方案/素材/")
    named = []
    for dirpath, _, files in os.walk(ASSET_DIR):
        for fn in files:
            if "二维码" in fn:
                named.append(os.path.join(dirpath, fn))
    decoded = qr_scan(ASSET_DIR)
    if not named:
        t.fail("素材目录里没有名字含「二维码」的文件",
               hint="二维码丢了；重出 职引-二维码-公开站点.png")
        return
    t.note("名字含「二维码」的文件 %d 个：%s" % (len(named), "、".join(os.path.basename(p) for p in named)))
    t.note("能解出二维码的图片 %d 张" % len(decoded))
    stale = []
    for path, data in decoded:
        m = CHAT_RE.search(data)
        code = m.group(1) if m else ""
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        t.note("  %s -> %s" % (rel, data))
        if code and code != ready:
            stale.append((rel, code))
    if len(decoded) > 1:
        t.fail("素材目录里有 %d 个可用二维码，收件人扫哪张全凭运气" % len(decoded),
               n=len(decoded) - 1,
               hint="只留 职引-二维码-公开站点.png，其余移出 素材/（-NEW / -旧 / .bak 都算）")
    elif len(decoded) == 1:
        t.ok("只有 1 张二维码，无歧义")
    if stale:
        t.warn("%d 张二维码指向旧站点码：%s" % (len(stale), "、".join("%s(%s)" % x for x in stale)),
               hint="旧二维码是上次事故的来源（-NEW.png 指向废弃站），删掉或改名加 -旧")
    if not decoded:
        t.fail("素材目录没有任何图片能解出二维码")


# ---------------------------------------------------------------- 主流程
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    quiet = "--quiet" in argv
    ready = read_site()
    t = Tally(quiet=quiet)

    print("=" * 72)
    print("职引 · 资产一致性校验")
    print("=" * 72)
    print("真源  技术档案/readysite.txt -> %s" % (ready or "（空！）"))
    print("对照  %s/chat/%s" % (BASE, ready or "?"))

    if not ready:
        t.fail("readysite.txt 缺失或为空，全部检查无法比对",
               hint="先写入当前站点码（release.py 会自动写）")

    check_qr(ready, t)
    check_markdown(ready, t)
    check_docx(ready, t)
    check_pdf(ready, t)
    check_qr_files(ready, t)

    print()
    print("-" * 72)
    print("结论")
    if not t.fix_hints:
        print("  · 5 份副本一致，可以交付")
    else:
        for i, hint in enumerate(t.fix_hints, 1):
            print("  %d. %s" % (i, hint))

    result = "FAIL" if t.fails else "PASS"
    print()
    print("---ASSET_SUMMARY---")
    print("RESULT: %s" % result)
    print("SITE: %s" % (ready or "(missing)"))
    print("MISMATCHES: %d" % t.mismatches)
    print("---END---")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
