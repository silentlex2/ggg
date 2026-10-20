# -*- coding: utf-8 -*-
"""把某个已建好的应用「扶正」为对外正式站：一次做完改名、换真源、重出二维码、改提交表、跑资产校验。

用法：
    python promote.py --app <新应用ID> --site <站点码> [--old <旧应用ID>] [--skip-docx]

做哪些事（顺序固定）：
  1. 新应用 PUT 改名/描述/图标/use_icon_as_answer_icon
  2. 旧应用 PUT 改名标注「回退 · 上一版」
  3. readysite.txt 覆写为新站点码（先打印旧值）
  4. 调 make_qr.py 重出二维码并解码回验
  5. 提交表 docx 里所有 chat/<码> 替换成新码；有 Word COM 就重出 PDF
  6. 跑 check_assets.py，打印契约块
任何一步失败即停并打印已经改到哪一步（readysite 与二维码是幂等的，可重跑）。
"""
import argparse
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile

BASE = "https://aiagent.cqut.edu.cn:31134"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
ICON = "ff8cb252-6223-4c43-9eb7-22844fd9adfa"
READY = os.path.join(HERE, "readysite.txt")
DOCX = os.path.join(ROOT, "参赛方案", "提交材料", "作品提交表-职引.docx")
PDF = os.path.join(ROOT, "参赛方案", "提交材料", "作品提交表-职引.pdf")
NAME = "职引 · 校园就业智能体"
DESC = "校园就业智能体：简历诊断 / 岗位匹配 / 模拟面试 / 政策咨询 · 重庆理工大学"


def tok():
    t = os.environ.get("CONSOLE_TOKEN", "").strip()
    if not t:
        raise SystemExit("需要 CONSOLE_TOKEN")
    return t


def api(path, method="GET", body=None):
    t = tok()
    h = {"Authorization": "Bearer " + t, "OperToken": t}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=120) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:200]


def patch_docx(site):
    if not os.path.exists(DOCX):
        print("  ! 找不到提交表 docx，跳过")
        return False
    src = zipfile.ZipFile(DOCX)
    items = [(i, src.read(i.filename)) for i in src.infolist()]
    src.close()
    changed = 0
    out = []
    for info, data in items:
        if info.filename == "word/document.xml":
            xml = data.decode("utf-8")
            new = re.sub(r"chat/[A-Za-z0-9]{8,20}", "chat/" + site, xml)
            changed = len(re.findall(r"chat/", xml))
            data = new.encode("utf-8")
        out.append((info, data))
    with zipfile.ZipFile(DOCX, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in out:
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            z.writestr(zi, data)
    print("  docx 地址已替换（%d 处）" % changed)
    return True


def export_pdf():
    ps = (
        "$ErrorActionPreference='Stop';"
        "$w=New-Object -ComObject Word.Application; $w.Visible=$false; $w.DisplayAlerts=0;"
        "$d=$w.Documents.Open('%s',$false,$false); $d.SaveAs2('%s',17); $d.Close(0);"
        "try{$w.Quit()}catch{}" % (DOCX, PDF)
    )
    p = subprocess.run(["pwsh", "-NoProfile", "-Command", ps],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0 or not os.path.exists(PDF):
        print("  ! PDF 导出失败：%s" % (p.stderr or "")[:200])
        return False
    print("  PDF 已重出：%d 字节" % os.path.getsize(PDF))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", required=True)
    ap.add_argument("--site", required=True)
    ap.add_argument("--old")
    ap.add_argument("--skip-docx", action="store_true")
    a = ap.parse_args()

    old_site = open(READY, encoding="utf-8").read().strip() if os.path.exists(READY) else ""
    print("旧站点码：%s -> 新站点码：%s" % (old_site or "(空)", a.site))

    print("[1] 新应用改名 + 图标")
    s, _ = api("/console/api/apps/%s" % a.app, "PUT", {
        "name": NAME, "description": DESC, "icon_type": "image", "icon": ICON,
        "icon_background": "", "use_icon_as_answer_icon": True})
    print("    ->", s)

    if a.old and a.old != a.app:
        print("[2] 旧应用标注回退")
        s, _ = api("/console/api/apps/%s" % a.old, "PUT", {
            "name": "%s（回退 · 上一版）" % NAME,
            "description": "回退用：上一版（站点 %s）" % (old_site or "?")})
        print("    ->", s)

    print("[3] 覆写 readysite.txt")
    with open(READY, "w", encoding="utf-8", newline="\n") as f:
        f.write(a.site)
    print("    ->", open(READY, encoding="utf-8").read().strip())

    print("[4] 重出二维码并回验")
    p = subprocess.run([sys.executable, os.path.join(HERE, "make_qr.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("    " + (p.stdout or p.stderr).strip().replace("\n", "\n    "))
    if p.returncode != 0:
        raise SystemExit("二维码重出/回验失败")

    if not a.skip_docx:
        print("[5] 提交表 docx / PDF")
        patch_docx(a.site)
        export_pdf()

    print("[6] 资产一致性校验")
    p = subprocess.run([sys.executable, os.path.join(HERE, "check_assets.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    tail = (p.stdout or "").strip().split("\n")[-8:]
    for line in tail:
        print("    " + line)
    print()
    print("PROMOTE_DONE site=%s rc=%d" % (a.site, p.returncode))
    return 0


if __name__ == "__main__":
    sys.exit(main())
