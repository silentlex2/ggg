# 工具脚本

三个脚本，改完文档随时跑一遍。

## 1. `check-segments.py` —— 知识库分段预检

```bash
python3 tools/check-segments.py
```

- 对每个知识库按 `##` / `###` / `####` 三种切法各算一遍，选"最大分段最小"的那种
- 生成 `知识库/分段预检报告.md`（含推荐分隔符、超限段明细、上传参数对照表）
- 判定标准：平台建议**分段最大长度 800 tokens**（`知识库/README.md` §2.1）
- token 估算偏保守（CJK 按 1 token/字），实际通常更小

**什么时候跑**：新增/修改知识库内容之后，上传之前。

## 2. `check-consistency.py` —— 方案一致性检查

```bash
python3 tools/check-consistency.py
```

检查 7 组共 30+ 项，退出码非 0 表示有失败项：

| 组 | 检查内容 |
| --- | --- |
| A | 口径一致性：平台能力 16 项 / 8 项高阶 / 13 条答辩亮点 |
| B | 陈旧表述：不得出现"12 项""四大功能""四项服务""待补充" |
| C | 知识库：KB4 的 csv 与 md 条数/编号一致，且与各文档中的数字一致；无空字段 |
| D | Markdown 结构：代码围栏成对、表格列数一致 |
| E | 交叉引用：README 文件清单与目录实际文件一致、链接有效 |
| F | 提交表字数：草稿 A ≤200 / B ≤1000 / C ≤300 |
| G | 答辩题数：`01` 中应有 17 题 |

**什么时候跑**：每次改完文档（尤其是改数字、改条数、加文件）之后。

## 3. `pack-submission.sh` —— 提交包打包

```bash
./tools/pack-submission.sh "张明" "13800000000"
```

- 检查必需材料是否齐全（缺了会明确报 ❌ 并返回非 0）
- 打包为 `提交包-<队长姓名><联系方式>.zip`（官方要求的命名格式）
- 材料放在 `提交材料/` 目录，命名规则见 `提交材料/README.md`

**什么时候跑**：材料备齐后、提交前一天。

---

## 建议的日常流程

```bash
# 改完文档
python3 tools/check-consistency.py     # 口径别漂
python3 tools/check-segments.py        # 知识库别超长

# 提交前
python3 tools/check-consistency.py && ./tools/pack-submission.sh "队长姓名" "联系方式"
```
