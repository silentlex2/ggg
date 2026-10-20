# -*- coding: utf-8 -*-
"""提交材料一键再生（make_materials.py）

为什么要有：提交材料由四个脚本分别产出（提交表 docx、PDF、二维码、终检），
顺序和参数散在文档里，换站或改稿时少跑一步就是"地址还是旧的"这种致命错误。
这里把它们串成一条命令，并做交叉核对——生成完当场验证，不留到提交前一晚才发现。

用法：
    python make_materials.py                 # 只做再生与核对，不打包
    python make_materials.py --pack 张三 13800000000   # 顺带打成官网要的 zip
    python make_materials.py --pack ... --force        # 材料缺项也照样打（默认拒绝）

打包命名按官方要求：`队长姓名 + 联系方式`，产 `参赛方案/提交包-<姓名><联系方式>.zip`，
该文件已被 .gitignore 排除（含个人信息，不进仓库）。

输出契约：
    ---MATERIALS---
    SITE: YnmaDNCRpd1otyrC
    DOCX: ok
    PDF_PAGES: 7
    URL_IN_PDF: yes
    PLACEHOLDER_LEFT: 3
    QR: ok
    MISSING: 3
    ZIP: -
    ---END---

退出码：0 = 全部再生并核对通过；1 = 有硬失败（docx/PDF/二维码/地址不符）；
        2 = 打包条件不满足（材料缺项且没给 --force）。
"""
import os
import re
import subprocess
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SUBMIT = os.path.join(ROOT, "参赛方案", "提交材料")
FORM_DOCX = os.path.join(SUBMIT, "作品提交表-职引.docx")
FORM_PDF = os.path.join(SUBMIT, "作品提交表-职引.pdf")


def read_site():
    with open(os.path.join(HERE, "readysite.txt"), encoding="utf-8") as f:
        return f.read().strip()


def run(script, extra=None):
    """跑同目录脚本，返回 (退出码, 输出文本)。"""
    cmd = [sys.executable, os.path.join(HERE, script)] + (extra or [])
    print("\n$ %s" % " ".join(cmd))
    p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    print(out.rstrip())
    return p.returncode, out


def field(out, name):
    m = re.search(r"^%s:\s*(.+)$" % re.escape(name), out, re.M)
    return m.group(1).strip() if m else ""


def pack(name, contact, force, missing):
    """按官网要求打包：队长姓名 + 联系方式。"""
    if missing and not force:
        print("\n拒绝打包：提交材料还缺 %d 项（缺项用 --force 可以硬打，但上传会被判形式审查不通过）" % missing)
        return 2
    pkg = "%s%s" % (name.strip(), contact.strip())
    if not pkg:
        print("\n拒绝打包：姓名或联系方式为空")
        return 2
    dest = os.path.join(ROOT, "参赛方案", "提交包-%s.zip" % pkg)
    print("\n打给官网上传的压缩包：%s" % os.path.basename(dest))
    n = 0
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, _dirs, files in os.walk(SUBMIT):
            for fn in sorted(files):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, SUBMIT).replace(os.sep, "/")
                z.write(full, os.path.join(pkg, rel))
                n += 1
                print("  + %-42s %7.1f KB" % (rel, os.path.getsize(full) / 1024.0))
    print("共 %d 个文件，压缩包 %.2f MB" % (n, os.path.getsize(dest) / 1048576.0))
    return dest


def main():
    args = sys.argv[1:]
    force = "--force" in args
    name = contact = ""
    if "--pack" in args:
        i = args.index("--pack")
        name = args[i + 1] if len(args) > i + 1 else ""
        contact = args[i + 2] if len(args) > i + 2 else ""

    site = read_site()
    print("站点码真源：%s" % site)
    hard_fail = False

    # 1) 提交表 docx（正文三段字数超限会非零退出）
    rc, out = run("gen_submission_form.py")
    docx_ok = rc == 0 and os.path.exists(FORM_DOCX)
    if not docx_ok:
        hard_fail = True

    # 2) PDF 导出（Word COM）
    rc, out_pdf = run("make_form_pdf.py")
    pages = field(out_pdf, "PDF_PAGES")
    url_ok = field(out_pdf, "URL_IN_PDF")
    left = field(out_pdf, "PLACEHOLDER_LEFT")
    if rc != 0:
        hard_fail = True
    if url_ok and url_ok != "yes":
        print("！PDF 里的作品地址与 readysite.txt 不一致")
        hard_fail = True

    # 3) 二维码
    rc, out_qr = run("make_qr.py")
    qr_url = field(out_qr, "URL")
    qr_ok = rc == 0 and (site in qr_url if qr_url else True)
    if not qr_ok:
        hard_fail = True

    # 4) 终检
    rc, out_sub = run(os.path.join(ROOT, "参赛方案", "tools", "check-submission.py"))
    m = re.search(r"MISSING:\s*(\d+)", out_sub)
    missing = int(m.group(1)) if m else 0

    zip_name = "-"
    if "--pack" in args:
        got = pack(name, contact, force, missing)
        if isinstance(got, str):
            zip_name = os.path.basename(got)
        else:
            return got

    print("\n---MATERIALS---")
    print("SITE: %s" % site)
    print("DOCX: %s" % ("ok" if docx_ok else "fail"))
    print("PDF_PAGES: %s" % (pages or "?"))
    print("URL_IN_PDF: %s" % (url_ok or "?"))
    print("PLACEHOLDER_LEFT: %s" % (left or "?"))
    print("QR: %s" % ("ok" if qr_ok else "fail"))
    print("MISSING: %d" % missing)
    print("ZIP: %s" % zip_name)
    print("---END---")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())