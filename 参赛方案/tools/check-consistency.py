#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「职引」参赛方案一致性检查。

用法：
    python3 tools/check-consistency.py

检查项（改完文档后跑一遍，避免口径漂移）：
  A. 口径一致性：平台能力 14 项 / 9 类平台节点 / 答辩亮点 14 条 / 三大功能 + 1 加分项
  B. 陈旧表述：不得出现 "16 项"、"8 项高阶"、"NL2SQL" 等已废弃口径（行内含豁免词者除外）
  I. 黄金集条数：eval_cases.py 实际条数 / 分组条数 与 08 文档、README 对齐
  H. 站点码一致：readysite.txt / finaltest_ready.py / make_qr.py 三处必须一致，且不得残留旧站点码
  C. 知识库：KB4 的 csv 与 md 条数/编号一致，且与各文档中的数字一致
  D. Markdown 结构：代码围栏成对、表格列数一致
  E. 交叉引用：README 文件清单与目录实际文件一致
  F. 提交表字数：草稿 A ≤200、B ≤1000、C ≤300
  G. 答辩题数：01 中「### Qn ·」条数须等于 README 的「N 个答辩预测题」，且不少于 17

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
        '00-方案总览.md': ['平台能力 = 14 项', '9 类平台节点'],
        '05-工作流搭建手册（下）.md': ['平台能力 14 项', '9 类平台节点', '14 条答辩亮点'],
        '01-路演与答辩.md': ['9 类平台节点、14 项能力'],
        '02-提交材料清单.md': ['14 项能力', '9 类平台节点'],
        '07-进阶能力实现.md': ['14 项'],
        '06-作品打磨清单.md': ['14 项 / 9 类平台节点', '14 条'],
    }
    for fn, needles in expect.items():
        s = read(fn)
        miss = [n for n in needles if n not in s]
        if miss:
            fail('%s 缺少口径表述：%s' % (fn, miss))
        else:
            ok('%s 口径完整' % fn)


STALE = ['12 个平台能力', '12 项平台能力', '四大功能', '待补充',
         '16 项平台能力', '16 项能力', '8 项为高阶', '8 项高阶',
         '13 项能力', '13 项平台能力', '13 条答辩亮点', '9 类平台节点、13 项']

# 行内出现这些词的行属于"回头看/已降级/实测结论"的说明，允许保留旧口径
EXEMPT = ['早期', '旧口径', '已废弃', '降级', '未采用', '未落地', '没有进入最终版本',
          '实测', '不再', '不要再提', '已被', '原计划', '原方案', '不要讲', '删除',
          '已下线', '旧地址', '旧站点', '返回 404']


def check_stale():
    print('\n[B] 陈旧表述')
    hit = []
    for p in md_files():
        rel0 = os.path.relpath(p, ROOT).replace(os.sep, '/')
        # 这些文件本身就在描述/列举旧口径，跳过
        if 'site-dump' in rel0 or rel0.startswith('tools/') \
                or rel0.startswith('09-官方要求核对表'):
            continue
        for i, line in enumerate(io.open(p, encoding='utf-8').read().split('\n'), 1):
            if any(e in line for e in EXEMPT):
                continue
            for kw in STALE:
                if kw in line:
                    hit.append('%s:%d → %s' % (os.path.relpath(p, ROOT), i, kw))
    if hit:
        fail('发现陈旧表述：%s' % '；'.join(hit[:10]))
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
    archived = set()
    for entry in os.listdir(ROOT):
        p = os.path.join(ROOT, entry)
        if os.path.isdir(p):
            actual.add(entry + '/')
        elif entry.endswith('.md') and entry != 'README.md':
            # 「历史-*.md」是归档区（旧台账/旧结论），条目会持续增加，
            # 不逐个进 README 清单；但 README 必须显式交代归档前缀，否则等于藏起来
            if entry.startswith('历史-'):
                archived.add(entry)
            else:
                actual.add(entry)
    if archived and not re.search(r'历史-', readme):
        fail('存在 %d 个「历史-*.md」归档文件，但 README 未交代归档前缀（%s）'
             % (len(archived), sorted(archived)[:3]))
    elif archived:
        ok('归档文件 %d 个，README 已交代「历史-」前缀' % len(archived))
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
        ('B', r'### 草稿 B · 设计思路与技术实现（1000 字内）— \*\*正式稿\*\*\n\n(.*?)\n\n### 草稿 C', 1000),
        ('C', r'### 草稿 C · 作品使用说明（300 字内）\n\n(.*?)\n\n---', 300),
    ]
    for name, pat, lim in pats:
        m = re.search(pat, s, re.S)
        if not m:
            fail('未找到草稿 %s' % name)
            continue
        body = '\n'.join(l for l in m.group(1).split('\n') if not l.strip().startswith('>'))
        n = len(re.sub(r'\s', '', body))
        if n <= lim:
            ok('草稿 %s：%d / %d 字' % (name, n, lim))
        else:
            fail('草稿 %s 超限：%d / %d 字' % (name, n, lim))


# 站点码只有一个真源
SITES = {
    '../技术档案/readysite.txt': None,
}
# 其它脚本一律不许硬编码，必须读真源；这里校验"它们确实指向真源"
SITE_CONSUMERS = ['../技术档案/finaltest_ready.py',
                  '../技术档案/eval_golden.py',
                  '../技术档案/run_all.py',
                  '../技术档案/make_qr.py']
QR_PNG = '素材/职引-二维码-公开站点.png'   # make_qr.py 的默认输出
# 站点生命周期台账：本来就该记录旧站点码，跳过
SITE_LOG = ['运行状态与待办.md', '交接说明.md']
DEAD_SITES = ['ncfAarVCvUUWO56e', 'vBP7v5MWoBA6yCPt', 'tZ9PTLM9GtKcn3Ci', '43898f25']


def check_qr(cur_site):
    """材料里印的那张二维码必须指向当前站点。

    站点一换、码没重出，评委扫出来就是 404，而且现场没人会发现。
    """
    png = os.path.join(ROOT, QR_PNG)
    if not os.path.exists(png):
        warn('二维码 PNG 不存在，跳过扫码校验（%s）' % QR_PNG)
        return
    try:
        import cv2
        import numpy as np
    except ImportError:
        warn('本机没有 cv2/numpy，无法解码二维码校验（%s）' % QR_PNG)
        return
    img = cv2.imdecode(np.fromfile(png, dtype=np.uint8), cv2.IMREAD_COLOR)
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    if not data:
        fail('二维码 PNG 解不出内容（%s），可能已损坏' % QR_PNG)
    elif not cur_site:
        warn('读不到站点码真源，无法比对二维码内容（%s）' % data)
    elif cur_site in data:
        ok('二维码指向当前站点：%s' % data)
    else:
        fail('二维码指向的地址与当前站点不匹配：%s（应为含 %s）' % (data, cur_site))


def check_site():
    print('\n[H] 站点码一致性')
    import re as _re
    found = {}
    for rel, pat in SITES.items():
        try:
            s = read(rel)
        except IOError:
            warn('%s 不存在，跳过' % rel)
            continue
        m = _re.search(pat, s) if pat else None
        v = m.group(1) if m else s.strip().splitlines()[0].strip()
        found[rel] = v
    vals = set(found.values())
    cur_site = found.get('../技术档案/readysite.txt', '')
    if len(vals) == 1:
        ok('站点码真源：%s' % cur_site)
    else:
        fail('站点码不一致：%s' % found)

    # 消费者脚本必须读真源，不许再硬编码（v7e 时代 finaltest_ready.py 写死过站点码）
    for rel in SITE_CONSUMERS:
        try:
            s = read(rel)
        except IOError:
            warn('%s 不存在，跳过真源校验' % rel)
            continue
        if 'readysite.txt' in s:
            ok('%s 读 readysite.txt 真源' % os.path.basename(rel))
        else:
            fail('%s 未引用 readysite.txt，可能又硬编码了站点码' % rel)

    check_qr(cur_site)

    for p in md_files():
        rel0 = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if rel0.startswith('tools/') or rel0 in SITE_LOG:
            continue
        # 「历史-*.md」是归档台账，本来就该留着旧站点码
        if os.path.basename(rel0).startswith('历史-'):
            continue
        for i, line in enumerate(io.open(p, encoding='utf-8').read().split('\n'), 1):
            if any(e in line for e in EXEMPT):
                continue
            for d in DEAD_SITES:
                if d in line:
                    fail('%s:%d 残留已下线站点码 %s' % (rel0, i, d))


def check_qa():
    print('\n[G] 答辩题数')
    s = read('01-路演与答辩.md')
    n_script = len(re.findall(r'^### Q\d+ ·', s, re.M))
    readme = read('README.md')
    m = re.search(r'(\d+) 个答辩预测题', readme)
    if not m:
        warn('README 未写"N 个答辩预测题"，无法交叉校验题数')
        return
    n_readme = int(m.group(1))
    if n_script == n_readme:
        ok('逐字答案稿 %d 题，与 README 表述一致' % n_script)
    else:
        fail('逐字答案稿为 %d 题，README 写 %d 题（改题了要同步 README）'
             % (n_script, n_readme))
    if n_script < 17:
        fail('答辩预测题只剩 %d 题，低于 17 题基线' % n_script)


def check_cases():
    """黄金集条数：以 eval_cases.py 为唯一真源，和文档里写的数字对齐。

    这是最容易悄悄漂的一处——加了几条用例，文档里的"46 条"没人改，
    等到答辩被问"你们测了多少条"就露馅。
    """
    print('\n[I] 黄金集条数与文档')
    src = os.path.join(os.path.dirname(ROOT), '技术档案', 'eval_cases.py')
    if not os.path.exists(src):
        warn('找不到 eval_cases.py，跳过用例数校验')
        return
    body = io.open(src, encoding='utf-8').read()
    cats = re.findall(r'cat="([^"]+)"', body)
    total = len(cats)
    if not total:
        warn('eval_cases.py 里没解析到用例（cat="..." 一个也没有）')
        return
    counts = {}
    for c in cats:
        counts[c] = counts.get(c, 0) + 1
    ok('黄金集共 %d 条：%s' % (total, '，'.join('%s %d' % kv for kv in sorted(counts.items()))))

    doc = read('08-测试与验收.md')
    m = re.search(r'黄金集回归（自动化，(\d+) 条）', doc)
    if not m:
        warn('08 文档没写"黄金集回归（自动化，N 条）"，无法交叉校验')
    elif int(m.group(1)) != total:
        fail('08 文档写 %s 条，eval_cases.py 实际 %d 条' % (m.group(1), total))
    else:
        ok('08 文档条数与代码一致（%d）' % total)

    # 分组表：| A 意图分类 | 8 | ... 逐组核对
    table = re.findall(r'^\|\s*[A-F][^|]*\|\s*(\d+)\s*\|', doc, re.M)
    if not table:
        warn('08 文档分组表没解析到条数')
        return
    doc_counts = [int(x) for x in table]
    if sorted(doc_counts) == sorted(counts.values()):
        ok('分组条数与代码一致：%s' % doc_counts)
    else:
        fail('分组条数不一致：文档 %s / 代码 %s'
             % (sorted(doc_counts), sorted(counts.values())))
    readme = read('README.md')
    if re.search(r'黄金集 (\d+) 条', readme):
        n = int(re.search(r'黄金集 (\d+) 条', readme).group(1))
        if n != total:
            fail('参赛方案/README 写黄金集 %d 条，实际 %d 条' % (n, total))
        else:
            ok('README 条数与代码一致（%d）' % total)


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
        ('02-提交材料清单.md', r'(\d+) 条岗位'),
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
    check_cases()
    check_markdown()
    check_refs()
    check_wordcount()
    check_qa()
    check_site()

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

