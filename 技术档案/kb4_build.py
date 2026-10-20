# -*- coding: utf-8 -*-
"""KB4 岗位库构建器：CSV -> 知识库版 Markdown，可复现、可校验。

用法：
    python kb4_build.py            # 只校验：能否逐字节复现现有 KB4-岗位JD库（知识库版）.md
    python kb4_build.py --emit     # 由指定 CSV 生成 Markdown（--src / --out 覆盖路径）

分段约定：按 `##` 二级标题分段，每段一个完整岗位，端口对平台知识库的分段预检。
"""
import argparse
import csv
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(HERE, "..", "参赛方案", "知识库")
DEFAULT_CSV = os.path.join(KB_DIR, "KB4-岗位JD库.csv")
DEFAULT_MD = os.path.join(KB_DIR, "KB4-岗位JD库（知识库版）.md")

HEADER = """# KB4 · 岗位 JD 库（知识库版）

> 用途：「职引」岗位匹配模块的知识库检索版本。
> 与 `KB4-岗位JD库.csv` 同源。**本文件是岗位匹配实际上线的数据源**；
> CSV 原计划用于数据库节点（NL2SQL），因该节点实测连接超时未采用。
> 共 **{count}** 个岗位。建议分段：按 `##` 二级标题分段，每段即一个完整岗位。

## 使用说明

- 每个岗位块包含：企业类型、行业、城市、招聘类型、学历与专业要求、必备/加分技能、岗位职责、薪资参考。
- 智能体检索后应输出：岗位名称 + 匹配度 + 匹配理由 + 差距提示。
- 数据为示例数据，实际岗位以学校就业网发布为准。

---
"""

BLOCK = """## {job_title}（岗位编号 {id}）

| 字段 | 内容 |
| --- | --- |
| 企业类型 | {company_type} |
| 所属行业 | {industry} |
| 工作城市 | {city} |
| 招聘类型 | {job_type} |
| 学历要求 | {degree} |
| 专业要求 | {major_req} |
| **必备技能** | {must_skills} |
| 加分技能 | {plus_skills} |
| 薪资参考 | {salary_range} |

**岗位职责**：{duties}

---
"""


APPENDIX = """## 附录 A · 专业名称对照（检索时按同一专业处理）

同一专业在校内不同材料里写法不一，检索与匹配时按同一专业处理：

| 规范专业名 | 常见别名 / 写法 |
| --- | --- |
| 机械设计制造及其自动化 | 机械、机械类、机械工程、机械设计制造、机械电子工程 |
| 计算机科学与技术 | 计算机、计算机类、软件工程（相近专业） |
| 电气工程及其自动化 | 电气、电气工程、电气类 |
| 统计学 | 应用统计、统计 |
| 化学工程与工艺 | 化工、化工工艺、应用化学（相近专业） |
| 材料科学与工程 | 材料类、材料化学、高分子、材料成型 |
| 车辆工程 | 汽车工程、汽车服务工程 |
| 英语 | 商务英语、翻译、英语语言文学 |
| 金融学 | 经济金融、金融工程、投资学 |
| 会计学 | 会计、财务管理（相近专业） |

## 附录 B · 城市字段约定

工作城市写作「重庆 + 区县 / 园区」，只写「重庆」表示主城未限定区县。
检索时把「重庆」当作上级地域：学生问某个区县时，只写「重庆」的岗位也要一并召回，不要漏掉。

## 附录 C · 数据版本与覆盖范围

| 项 | 内容 |
| --- | --- |
| 数据版本 | 2026-10 扩充版，共 {count} 个岗位 |
| 覆盖城市 | 重庆主城及各区县为主，另有成都、绵阳、宜宾、贵阳少量岗位 |
| 覆盖专业 | 化工、材料、机械、车辆、电气、计算机、人工智能、数学统计、经管、会计、金融、药学、环境、外语、体育、法学、知识产权、心理、教育 |
| 数据性质 | 示例数据，按重庆市高校就业常见岗位整理；真实岗位以学校就业网发布为准 |
"""


def join_cn(text):
    """把 CSV 里的分号分隔串渲染成中文顿号串。"""
    parts = [p.strip() for p in (text or "").replace("；", ";").split(";")]
    return "、".join(p for p in parts if p)


def load_rows(path):
    return list(csv.DictReader(io.open(path, encoding="utf-8-sig")))


def render(rows, appendix=False):
    out = [HEADER.format(count=len(rows))]
    for row in rows:
        out.append(BLOCK.format(
            job_title=row["job_title"].strip(),
            id=row["id"].strip(),
            company_type=row["company_type"].strip(),
            industry=row["industry"].strip(),
            city=row["city"].strip(),
            job_type=row["job_type"].strip(),
            degree=row["degree"].strip(),
            major_req=join_cn(row["major_req"]),
            must_skills=join_cn(row["must_skills"]),
            plus_skills=join_cn(row["plus_skills"]),
            salary_range=row["salary_range"].strip(),
            duties=row["duties"].strip(),
        ))
    if appendix:
        out.append("")
        out.append(APPENDIX.format(count=len(rows)))
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default=DEFAULT_CSV)
    parser.add_argument("--out", default=DEFAULT_MD)
    parser.add_argument("--emit", action="store_true", help="写出 Markdown")
    parser.add_argument("--appendix", action="store_true", help="追加附录（专业对照 / 城市约定 / 数据版本）")
    args = parser.parse_args()

    rows = load_rows(args.src)
    text = render(rows, appendix=args.appendix)
    print("CSV %s -> %d 个岗位 / Markdown %d 字符" % (os.path.basename(args.src), len(rows), len(text)))

    if args.emit:
        with io.open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print("已写出 %s" % args.out)
        return 0

    existing = io.open(args.out, encoding="utf-8").read()
    if existing == text:
        print("校验：生成结果与现有 %s 逐字节一致 ✅" % os.path.basename(args.out))
        return 0
    print("校验：与现有 %s 不一致 ❌" % os.path.basename(args.out))
    diff_at = next((i for i, (a, b) in enumerate(zip(existing, text)) if a != b), min(len(existing), len(text)))
    print("  首个差异位置 %d，现有 %d 字符 / 生成 %d 字符" % (diff_at, len(existing), len(text)))
    print("  现有 …%r" % existing[max(0, diff_at - 40):diff_at + 40])
    print("  生成 …%r" % text[max(0, diff_at - 40):diff_at + 40])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
