import io
reps = [
    ('参赛方案/00-方案总览.md',
     '## 五、四大功能模块',
     '## 五、功能模块（三大功能 + 1 个加分项）'),
    ('参赛方案/02-提交材料清单.md',
     '   - 以工作流应用为核心，四大功能分支',
     '   - 以工作流应用为核心，三大功能分支 + 成长档案（加分项）'),
]
for p, old, new in reps:
    s = io.open(p, encoding='utf-8').read()
    assert s.count(old) == 1, (p, s.count(old))
    s = s.replace(old, new)
    io.open(p, 'w', encoding='utf-8').write(s)
print('ok')
