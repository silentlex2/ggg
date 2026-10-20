# -*- coding: utf-8 -*-
"""把《作品提交表》docx 用 Word 导出 PDF，并抽文核对作品地址与页数。

为什么要单独一个脚本：WPS 导出的 PDF 字体是子集，离线扫不出 ASCII；
用 Word 的 ExportAsFixedFormat 才能保证提交表里的作品地址可被机器读到。

用法：
    python make_form_pdf.py            # docx -> pdf，默认同名
    python make_form_pdf.py --check    # 只核对现有 PDF，不重新导出
"""
import argparse
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAT = os.path.join(ROOT, "参赛方案", "提交材料")
DOCX = os.path.join(MAT, "作品提交表-职引.docx")
PDF = os.path.join(MAT, "作品提交表-职引.pdf")
SITE_CODE = open(os.path.join(HERE, "readysite.txt"), encoding="utf-8").read().strip()
URL = "https://aiagent.cqut.edu.cn:31134/chat/%s" % SITE_CODE


def export_pdf():
    import win32com.client  # noqa: PLC0415

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(DOCX, ReadOnly=False)
        # 17 = wdExportFormatPDF
        doc.ExportAsFixedFormat(OutputFileName=PDF, ExportFormat=17,
                                OpenAfterExport=False, OptimizeFor=0,
                                Item=0, IncludeDocProps=True, KeepIRM=True,
                                CreateBookmarks=0, DocStructureTags=True,
                                BitmapMissingFonts=True, UseISO19005_1=False)
        pages = doc.ComputeStatistics(2)  # 2 = wdStatisticPages
        doc.Close(SaveChanges=False)
    finally:
        word.Quit()
    return pages


def check_pdf():
    from pypdf import PdfReader  # noqa: PLC0415

    reader = PdfReader(PDF)
    text = "".join((page.extract_text() or "") for page in reader.pages)
    found = URL in text.replace("\n", "")
    placeholders = text.count("【待填】")
    return len(reader.pages), found, placeholders


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="只核对现有 PDF")
    args = parser.parse_args()

    if not os.path.exists(DOCX):
        sys.exit("找不到 docx：%s" % DOCX)

    pages = None
    if not args.check:
        print("导出 PDF（Word COM）…")
        pages = export_pdf()
        print("  已写出 %s（%d 字节）" % (PDF, os.path.getsize(PDF)))
    if not os.path.exists(PDF):
        sys.exit("找不到 PDF：%s" % PDF)

    pdf_pages, found, placeholders = check_pdf()
    print("")
    print("---FORM_PDF_SUMMARY---")
    print("DOCX: %s" % os.path.basename(DOCX))
    print("PDF_PAGES: %d%s" % (pdf_pages, "" if pages is None else "（Word 统计 %d）" % pages))
    print("URL_IN_PDF: %s" % ("yes" if found else "no"))
    print("EXPECT_URL: %s" % URL)
    print("PLACEHOLDER_LEFT: %d" % placeholders)
    print("---END---")
    if not found:
        sys.exit("PDF 里读不到作品地址，检查是否导出成了图片版或地址写错")
    if placeholders:
        print("提醒：还有 %d 处【待填】，填好 队伍信息.json 后重跑 gen_submission_form.py 再导出" % placeholders)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
