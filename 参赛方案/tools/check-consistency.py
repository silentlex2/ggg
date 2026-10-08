#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「职引」参赛方案一致性检查。

用法：
    python3 tools/check-consistency.py

检查项（改完文档后跑一遍，避免口径漂移）：
  A. 口径一致性：平台能力 16 项 / 高阶 8 项 / 答辩亮点 13 条 / 三大功能 + 1 加分项
  B. 陈旧表述：不得出现 "12 项"、"四大功能"、"四项服务"、"待补充" 等旧口径
  C. 知识库：KB4 的 csv 与 md 条数/编号一致，且与各文档中的数字一致
  D. Markdown 结构：代码围栏成对、表格列数一致
  E. 交叉引用：README 文件清单与目录实际文件一致
  F. 提交表字数：草稿 A ≤200、B ≤1000、C ≤300
  G. 答辩题数：01 中应有 17 题

退出码：0 全部通过；1 有失败项。
"""
import csv
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

fails = []
warns = []


def ok(msg):
    print('  \033[32mPASS\033[0m %s' % msg)


def fail(msg):
    print('  \033[31mFAIL\033[0m %s' % msg)
    fails.append(msg)


def warn(msg):
    print('  \033[33mWARN\033[0m %s' % msg)
    warns.append(msg)


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding='utf-8').read()


def md_files():
    return sorted(glob.glob(os.path.join(ROOT, '**', '*.md'), recursive=True))


def check_terms():
    print('\n[A] 口径一致性')
    expect = {
        '00-方案总览.md': ['16 项', '8 项为高阶'],
        '05-工作流搭建手册（下）.md': ['16 项', '8 项为高阶能力', '13 条答辩亮点'],
        '01-路演与答辩.md': ['16 项'],
        '07-进阶能力实现.md': ['16 项'],
        '06-作品打磨清单.md': ['16 项（8 项高阶）', '13 条'],
    }
    for fn, needles in expect.items():
        s = read(fn)
        miss = [n for n in needles if n not in s]
        if miss:
            fail('%s 缺少口径表述：%s' % (fn, miss))
        else:
            ok('%s 口径完整' % fn)


STALE = ['12 个平台能力', '12 项平台能力', '四大功能', '四项服务', '待补充']


def check_stale():
    print('\n[B] 陈旧表述')
    hit = []
    for p in md_files():
        rel0 = os.path.relpath(p, ROOT).replace(os.sep, '/')
        # 这些文件本身就在描述/列举旧口径，跳过
        if 'site-dump' in rel0 or rel0.startswith('tools/') \
                or rel0.startswith('09-官方要求核对表'):
            continue
        s = io.open(p, encoding='utf-8').read()
        for kw in STALE:
            if kw in s:
                hit.append('%s → %s' % (os.path.relpath(p, ROOT), kw))
    if hit:
        fail('发现陈旧表述：%s' % '；'.join(hit))
    else:
        ok('无陈旧表述')


def check_markdown():
    print('\n[D] Markdown 结构')
    bad_fence, bad_table = [], []
    for p in md_files():
        rel = os.path.relpath(p, ROOT)
        s = io.open(p, encoding='utf-8').read()
        depth = 0
        for line in s.split('\n'):
            if line.strip().startswith('```'):
                depth = 1 - depth
        if depth:
            bad_fence.append(rel)
        for m in re.finditer(r'(?:^\|.*\n)+', s, re.M):
            lines = m.group(0).strip().split('\n')
            if len(lines) >= 2:
                n = lines[0].count('|')
                if any(l.count('|') != n for l in lines[1:]):
                    bad_table.append(rel)
                    break
    if bad_fence:
        fail('代码围栏不成对：%s' % bad_fence)
    else:
        ok('所有 md 代码围栏成对')
    if bad_table:
        fail('表格列数不一致：%s' % bad_table)
    else:
        ok('所有 md 表格列数一致')


def check_refs():
    print('\n[E] 交叉引用与文件清单')
    readme = read('README.md')
    listed = set(re.findall(r'\]\(\./([^)]+)\)', readme))
    actual = set()
    for entry in os.listdir(ROOT):
        p = os.path.join(ROOT, entry)
        if os.path.isdir(p):
            actual.add(entry + '/')
        elif entry.endswith('.md') and entry != 'README.md':
            actual.add(entry)
    missing = sorted(a for a in actual if a not in listed)
    broken = sorted(l for l in listed if not os.path.exists(os.path.join(ROOT, l)))
    if missing:
        fail('README 目录未列出：%s' % missing)
    else:
        ok('README 目录已列出全部文件/目录')
    if broken:
        fail('README 中存在失效链接：%s' % broken)
    else:
        ok('README 链接均有效')


def check_wordcount():
    print('\n[F] 提交表字数上限')
    s = read('02-提交材料清单.md')
    pats = [
        ('A', r'### 草稿 A · 作品简介（200 字内）\n\n(.*?)\n\n### 草稿 B', 200),
        ('B', r'### 草稿 B · 设计思路与技术实现（1000 字内）— \*\*正式稿\*\*\n\n>.*?\n\n(.*?)\n\n### 草稿 C', 1000),
        ('C', r'### 草稿 C · 作品使用说明（300 字内）\n\n(.*?)\n\n---', 300),
    ]
    for name, pat, lim in pats:
        m = re.search(pat, s, re.S)
        if not m:
            fail('未找到草稿 %s' % name)
            continue
        n = len(re.sub(r'\s', '', m.group(1)))
        if n <= lim:
            ok('草稿 %s：%d / %d 字' % (name, n, lim))
        else:
            fail('草稿 %s 超限：%d / %d 字' % (name, n, lim))


def check_qa():
    print('\n[G] 答辩题数')
    s = read('01-路演与答辩.md')
    n_script = len(re.findall(r'^### Q\d+ ·', s, re.M))
    if n_script == 17:
        ok('逐字答案稿 17 题')
    else:
        fail('逐字答案稿为 %d 题，应为 17' % n_script)
    if '17 个答辩预测题' in read('README.md'):
        ok('README 中的题数表述已更新')
    else:
        warn('README 未写"17 个答辩预测题"')


def check_kb():
    print('\n[C] 知识库一致性')
    csv_path = os.path.join(ROOT, '知识库', 'KB4-岗位JD库.csv')
    md_path = os.path.join(ROOT, '知识库', 'KB4-岗位JD库（知识库版）.md')
    rows = list(csv.DictReader(io.open(csv_path, encoding='utf-8')))
    md = io.open(md_path, encoding='utf-8').read()

    ids_csv = [int(r['id']) for r in rows]
    ids_md = [int(x) for x in re.findall(r'岗位编号 (\d+)', md)]

    if len(rows) != len(ids_md):
        fail('KB4 条数不一致：csv %d 条 / md %d 条' % (len(rows), len(ids_md)))
    else:
        ok('KB4 csv 与 md 均为 %d 条' % len(rows))
    if ids_csv != ids_md:
        fail('KB4 编号不一致（顺序或取值不同）')
    else:
        ok('KB4 编号一一对应')

    empties = [(r['id'], k) for r in rows for k, v in r.items() if not str(v).strip()]
    if empties:
        fail('KB4 存在空字段：%s' % empties[:5])
    else:
        ok('KB4 无空字段')

    n = len(rows)
    checks = [
        ('知识库/KB4-岗位JD库（知识库版）.md', r'共 \*\*(\d+)\*\* 个岗位'),
        ('知识库/README.md', r'岗位库共 \*\*(\d+)\*\* 条'),
        ('00-方案总览.md', r'(\d+) 条岗位'),
        ('02-提交材料清单.md', r'（(\d+) 条岗位'),
        ('07-进阶能力实现.md', r'岗位库 \*\*(\d+) 条\*\*'),
        ('09-官方要求核对表.md', r'岗位库 (\d+) 条'),
        ('08-测试与验收.md', r'岗位库共 \*\*(\d+) 条\*\*'),
        ('原型/README.md', r'`KB4` 的 (\d+) 条'),
    ]
    for rel, pat in checks:
        try:
            s = read(rel)
        except IOError:
            warn('%s 不存在，跳过' % rel)
            continue
        found = [int(x) for x in re.findall(pat, s)]
        if not found:
            warn('%s 未找到条数表述（模式 %s）' % (rel, pat))
        elif n not in found:
            fail('%s 中的条数 %s 与实际 %d 不一致' % (rel, found, n))
        else:
            ok('%s 条数 = %d' % (rel, n))

    qa = os.path.join(ROOT, '知识库', 'KB6-高频问答对.csv')
    if os.path.exists(qa):
        with io.open(qa, encoding='utf-8') as f:
            n_qa = sum(1 for _ in csv.reader(f)) - 1
        ok('KB6 问答对 CSV 共 %d 组' % n_qa)
    else:
        warn('KB6 问答对 CSV 不存在')


def main():
    print('「职引」参赛方案一致性检查\n根目录：%s' % ROOT)
    check_terms()
    check_stale()
    check_kb()
    check_markdown()
    check_refs()
    check_wordcount()
    check_qa()

    print('\n' + '=' * 56)
    if fails:
        print('❌ 失败 %d 项，警告 %d 项' % (len(fails), len(warns)))
        for f in fails:
            print('   - ' + f)
        return 1
    print('✅ 全部通过（警告 %d 项）' % len(warns))
    for w in warns:
        print('   - ' + w)
    return 0


if __name__ == '__main__':
    sys.exit(main())

