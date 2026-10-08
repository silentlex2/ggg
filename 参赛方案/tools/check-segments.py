#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识库分段预检：找出每个知识库最合适的分段标识符，并生成报告。

用法：
    python3 tools/check-segments.py

产出：
    知识库/分段预检报告.md

背景：平台建议「分段最大长度 800 tokens」（见 知识库/README.md §2.1）。
本脚本对 ## / ### / #### 三种切法各算一遍，选“最大分段最小”的那种，
并列出仍超限的段落与拆分建议。
"""
import io
import math
import os
import re
import sys

KB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '知识库')
LIMIT = 800
MARKERS = ['##', '###', '####']
FILES = [
    'KB1-简历写作规范库.md',
    'KB2-面试题库.md',
    'KB3-专业行业岗位对照库.md',
    'KB4-岗位JD库（知识库版）.md',
    'KB5-就业政策与流程库.md',
]


def est_tokens(text):
    """保守估算 token 数：CJK 按 1 token/字，其余按 4 字符/token。"""
    cjk = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', text))
    rest = re.sub(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', '', text)
    rest = re.sub(r'\s', '', rest)
    return cjk + int(math.ceil(len(rest) / 4.0))


def split_by(text, marker):
    parts = re.split(r'\n(?=%s )' % re.escape(marker), text)
    segs = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        title = part.split('\n', 1)[0].replace('#', '').strip()[:44]
        segs.append((title, est_tokens(part), len(part)))
    return segs


def main():
    report = []
    report.append('# 知识库分段预检报告')
    report.append('')
    report.append('> 由 `tools/check-segments.py` 自动生成，**不要手工编辑**。')
    report.append('> 用途：上传前确认每个「分段」不超过平台建议的 **800 tokens**（`README.md` §2.1）。')
    report.append('> token 估算偏保守（CJK 按 1 token/字），实际通常更小。')
    report.append('')
    report.append('## 一、结论：每个库该用哪个分隔符')
    report.append('')
    report.append('| 文件 | **建议分隔符** | 分段数 | 最大分段(tokens) | 超限段数 | 说明 |')
    report.append('| --- | --- | --- | --- | --- | --- |')

    details = []
    for fn in FILES:
        path = os.path.join(KB_DIR, fn)
        if not os.path.exists(path):
            report.append('| `%s` | — | — | — | — | ⚠️ 文件不存在 |' % fn)
            continue
        text = io.open(path, encoding='utf-8').read()
        per_marker = {m: split_by(text, m) for m in MARKERS}
        # 选“最大分段最小”的切法；并列时优先更粗的分隔符（分段更完整）
        best = min(MARKERS, key=lambda m: (max([s[1] for s in per_marker[m]] or [0]),
                                           MARKERS.index(m)))
        segs = per_marker[best]
        over = [s for s in segs if s[1] > LIMIT]
        mx = max([s[1] for s in segs] or [0])
        if not over:
            note = '✅ 可直接上传'
        elif mx <= LIMIT * 1.15:
            note = '⚠️ 略超（≤15%%），可直接上传；若平台报错再拆'
        else:
            note = '❌ 需拆段，见第三节'
        report.append('| `%s` | `%s` | %d | %d | %d | %s |'
                      % (fn, best, len(segs), mx, len(over), note))
        details.append((fn, best, per_marker, segs, over))

    report.append('')
    report.append('> 💡 平台支持**每个知识库单独设分隔符**，第一节「建议分隔符」这一列直接照填。')
    report.append('')

    report.append('## 二、三种切法对比（说明为什么这么选）')
    report.append('')
    report.append('| 文件 | 按 `##` 切 | 按 `###` 切 | 按 `####` 切 |')
    report.append('| --- | --- | --- | --- |')
    for fn, best, per_marker, segs, over in details:
        cells = []
        for m in MARKERS:
            sg = per_marker[m]
            cells.append('%d 段 / 最大 %d' % (len(sg), max([s[1] for s in sg] or [0])))
        report.append('| `%s` | %s | %s | %s |' % (fn, cells[0], cells[1], cells[2]))
    report.append('')

    report.append('## 三、超限分段明细与拆分建议')
    report.append('')
    any_over = False
    for fn, best, per_marker, segs, over in details:
        if not over:
            continue
        any_over = True
        report.append('### `%s`（按 `%s` 切后仍超限）' % (fn, best))
        report.append('')
        report.append('| 分段标题 | tokens | 字符数 | 建议 |')
        report.append('| --- | --- | --- | --- |')
        for title, tokens, chars in sorted(over, key=lambda x: -x[1]):
            report.append('| %s | %d | %d | 在该段内插一个 `#####` 子标题拆成两段 |'
                          % (title, tokens, chars))
        report.append('')
    if not any_over:
        report.append('（无——按推荐分隔符切分后，全部段落都在 800 tokens 以内）')
        report.append('')

    report.append('## 四、上传参数对照（照填）')
    report.append('')
    report.append('| 参数 | 值 |')
    report.append('| --- | --- |')
    report.append('| 分段方式 | 自定义 |')
    report.append('| 分段标识符 | **见第一节表格**（各库可能不同） |')
    report.append('| 分段最大长度 | 800 tokens |')
    report.append('| 分段重叠长度 | 120 tokens |')
    report.append('| 文本预处理 | 开启 |')
    report.append('| 解析方式 | 快速解析 |')
    report.append('| 检索方式 | 混合检索（语义 0.6 / 全文 0.4） |')
    report.append('| 最大召回片段数 | 5 |')
    report.append('| 结果重排 | 开启 |')
    report.append('| 相似度匹配值 | 0.45（岗位库 0.40） |')
    report.append('| 引用与归属 | 开启 |')
    report.append('')
    report.append('> **KB6（问答对）**：数据类型选「问答对」，单条即一段、不要合并（`README.md` §2.2）；')
    report.append('> 上传文件用 `KB6-高频问答对.csv`（已拆成 `question` / `answer` 两列）。')
    report.append('')

    out = os.path.join(KB_DIR, '分段预检报告.md')
    io.open(out, 'w', encoding='utf-8').write('\n'.join(report))

    for fn, best, per_marker, segs, over in details:
        print('%-30s pick=%-4s segs=%2d max=%4d over=%d'
              % (fn, best, len(segs), max([s[1] for s in segs] or [0]), len(over)))
    print('report ->', os.path.relpath(out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
