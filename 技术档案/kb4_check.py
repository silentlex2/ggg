# -*- coding: utf-8 -*-
"""KB4 知识库版结构校验 + 学院覆盖度检查。

校验项：
 1. `##` 分段数 = 岗位数 + 使用说明 + 附录
 2. 每个岗位块 9 个字段齐全、无空值
 3. 每个教学单位至少命中 1 个岗位
 4. 岗位编号连续且唯一
"""
import collections
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(HERE, "..", "参赛方案", "知识库")
MD = os.path.join(KB_DIR, "KB4-岗位JD库（知识库版）-v2-扩充80.md")

FIELDS = ["企业类型", "所属行业", "工作城市", "招聘类型", "学历要求",
          "专业要求", "**必备技能**", "加分技能", "薪资参考"]

# 教学单位 -> 该院专业在 KB4 里可能出现的写法（含别名）
COLLEGES = {
    "两江人工智能学院": ["人工智能", "数据科学", "智能"],
    "车辆工程学院": ["车辆工程", "汽车"],
    "机械工程学院": ["机械"],
    "药学与生物工程学院": ["药学", "制药工程", "药物制剂", "生物工程"],
    "物理与新能源学院": ["物理与新能源", "光电信息", "材料类", "新能源"],
    "数学科学学院": ["数学", "统计"],
    "管理学院": ["管理类", "市场营销", "物流管理", "人力资源", "工业工程", "电子商务"],
    "计算机科学与工程学院": ["计算机", "软件工程", "网络工程", "数据科学"],
    "电气与电子工程学院": ["电气", "电子信息", "自动化"],
    "重庆知识产权学院": ["知识产权", "法学"],
    "语言与传播学院": ["英语", "翻译", "新闻传播", "汉语言文学", "商务英语"],
    "体育部": ["体育", "运动训练", "运动人体科学"],
    "化学化工学院": ["化学工程与工艺", "应用化学", "化学"],
    "材料科学与工程学院": ["材料科学与工程", "材料成型", "高分子", "材料化学", "材料类"],
    "会计学院": ["会计", "财务管理", "审计"],
    "经济金融学院": ["金融", "经济学", "投资学", "保险", "国际经济与贸易"],
    "应用技术学院": ["机械", "电子", "计算机", "自动化"],
    "两江国际学院": ["计算机", "电子信息", "软件工程"],
}


def main():
    text = io.open(MD, encoding="utf-8").read()
    heads = re.findall(r"^## (.+)$", text, re.M)
    blocks = re.split(r"^## ", text, flags=re.M)[1:]
    jobs, others = [], []
    for block in blocks:
        title = block.split("\n", 1)[0].strip()
        if "岗位编号" in title:
            jobs.append((title, block))
        else:
            others.append(title)

    print("分段总数 %d（岗位块 %d + 非岗位段 %d）" % (len(blocks), len(jobs), len(others)))
    print("非岗位段：%s" % "、".join(others))
    print("")

    problems = []
    for title, block in jobs:
        for field in FIELDS:
            pattern = r"^\| %s \| (.+?) \|$" % re.escape(field)
            match = re.search(pattern, block, re.M)
            if not match:
                problems.append("%s 缺字段 %s" % (title, field))
            elif not match.group(1).strip() or match.group(1).strip() in ("—", "-", "无"):
                problems.append("%s 字段 %s 为空" % (title, field))
        if "**岗位职责**：" not in block:
            problems.append("%s 缺岗位职责" % title)

    ids = [int(re.search(r"岗位编号 (\d+)", t).group(1)) for t, _ in jobs]
    print("岗位编号 %d..%d，连续=%s，唯一=%s" % (
        min(ids), max(ids), len(ids) == max(ids) - min(ids) + 1, len(set(ids)) == len(ids)))
    print("字段完整性：%s" % ("全部齐全 ✅" if not problems else "问题 %d 处 ❌" % len(problems)))
    for item in problems[:15]:
        print("   - %s" % item)
    print("")

    body = "\n".join(block for _, block in jobs)
    print("学院覆盖度：")
    holes = []
    for college, aliases in COLLEGES.items():
        hits = sum(1 for _, block in jobs
                   if any(alias in block for alias in aliases))
        flag = "✅" if hits else "❌"
        print("   %-14s %-3s 命中 %d 个岗位" % (college, flag, hits))
        if not hits:
            holes.append(college)
    print("")
    print("未覆盖学院：%s" % ("无 ✅" if not holes else "、".join(holes)))
    return 0 if (not problems and not holes and len(set(ids)) == len(ids)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
