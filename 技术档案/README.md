# 职引 · 校园就业智能体 — 平台工具集

> ⚠️ **本文件多处说法已过时，不要照做。**（2026-10-11 标注）
> 已确认错的用 ~~删除线~~ + **批注** 就地标出；**没标注的部分也不保证仍然成立**。
> 这是多轮会话留下的工程笔记，写作时间跨度大，结论被推翻后原文没有回改。
> 总入口与可信度说明见仓库根目录 `交接说明.md`。

操作星辰智能体平台（`https://aiagent.cqut.edu.cn:31134`，Dify 内核）工作流的脚本与提示词。
~~参赛材料在 `ggg/参赛方案/`（另一个 git 仓库），这里只放工程工具。~~
→ **已归档**：整个项目现在都在 `ggg/` 一个仓库里，本目录即 `ggg/技术档案/`。

## 🚪 进平台的标准姿势（2026-10-14 记，**别省这一步**）

**不要直接打开 `https://aiagent.cqut.edu.cn:31134/...`。**
直接开会落到 `/signin` 要账号密码 + 验证码，而且那种标签页里 `localStorage.console_token` 是空的，
所有平台接口一律返回 `401 {"code":"4000","message":"鉴权异常"}`。

正确路径是**两步**：

1. 打开大赛门户 **`http://aiac.cqut.edu.cn:3090/ai`**（「智小理智能体平台」介绍页）
2. 点页面上的 **「体验"智小理智能体平台"」** 按钮 →
   跳 `uis.cqut.edu.cn` 的 CAS 单点登录
   （`?service=https://aiagent.cqut.edu.cn:31134/cas-proxy/api/casRedirect`）自动回落

走完这两步，那个 `aiagent.cqut.edu.cn:31134` 标签页里的 `localStorage.console_token`（535 字符）才是活的。
平台接口全部依赖它：`Authorization: Bearer <t>` + `OperToken: <t>`。

> 公开站点 `/chat/<站点码>` 是只读对话地址，**不受此限，可以直接开**。
> 这条约束只针对**控制台 / 工作流接口**。

所有脚本都通过浏览器标签页里的 `console_token` 调平台接口，不存密码、不落令牌。
标签页：`owb eval --tab ~~2030596171~~ <现取> --await-promise --expression "..."`（表达式要先 base64 再包一层
`eval(new TextDecoder('utf-8').decode(Uint8Array.from(atob('...'),c=>c.charCodeAt(0))))`，
否则中文和引号会被 shell 吃掉）。

**先 `cd experiments/zhiyin/` 再跑**——脚本之间用相对文件名互相引用，换目录就跑不到。

## 日常操作用这三个

| 文件 | 作用 |
| --- | --- |
| `spinfresh.js` | 开一个绑定了当前草稿的新应用。**（2026-10-14 夜再反转：站点固定跑「建站/复制时刻」那一次发布的版本，之后发布新版本不生效——实测关站重开也不重新绑定。所以想上线新配置，仍然只能重新 copy 出一个新站点。）** 复制→存草稿→发布→返回站点码和工作流 ID |
| `poll.py` | 轮询新站点的 live workflow_id，确认它绑的确实是刚发布那个。用法 `python poll.py <站点码> <工作流ID> <重试次数>` |
| `finaltest_ready.py` | 全量回归。场景1 面试全流程+换话题+续答、场景2 无面试时别说面试话、场景3 岗位匹配与闲聊。改顶部 `SITE` 指向要测的站点 |

## 提示词（面试官 + 分类器）

| 文件 | 说明 |
| --- | --- |
| `ivprompt3.txt` | 当前版面试官提示词，2166 字。~~**未实测**（写完就撞上余额耗尽）。~~ → **已实测通过**（2026-10-11 公开站点全量回归）。核心是三条铁律：进度只前进不倒退、除明确说重开外永不为 0 也不重出第 1 题、拿不准就选比自我介绍更靠后的题型 |
| `clsprompt2.txt` | 当前版分类器指令，1288 字。~~**未实测**。~~ → **已实测通过**。关键是短承接语（嗯/好的/继续）归面试陪练、不算寒暄 |
| `ivprompt2_verified.txt` | 上一版面试官提示词，已实测通过：干净流程 0→1→2→3→4→5 全通并出复盘报告 |
| `clsprompt_verified.txt` | 上一版分类器指令，已实测通过 |

写提示词用 `python applyprompts.py <面试官.txt> <分类器.txt>` 生成 `apply_iv.js` / `apply_cls.js`，
再 `bash runapply.sh` 执行。回归不过就换成 `_verified` 那两个再跑一遍。

## 备份与状态

| 文件 | 说明 |
| --- | --- |
| `graph_backup_20261010.json` | 拆死链前的完整图，29 节点。要还原就把里面的 `graph` 存回草稿 |
| `srcdraft.json` | 某次保存的工作应用草稿全量（app `f2e4f2a5`，29 节点，早于 v19），用来离线翻结构 |
| `snapshots/v19-draft.json` | **★ v19 现役草稿全量快照**（app `214d5f6b`，25 节点，123 KB，含全部提示词）。这是灾难恢复的唯一真基准；控制台没有版本历史，改坏了只能靠它 |
| `workflow_diff.py` | 草稿漂移检测：线上草稿 vs 快照逐节点比提示词哈希。`--dump-only` 建档、`--ref` 换基准、`--restore --yes` 写回草稿、`--list` 列快照 |
| `readysite.txt` | 当前公开站点码。~~`81sZtuESIgx4USJK`~~ → ~~`ncfAarVCvUUWO56e`~~ → ~~`tZ9PTLM9GtKcn3Ci`~~ → ~~`vBP7v5MWoBA6yCPt`~~ → ~~`3PNowdyi2c13Khnl`（v2/v3，已关站）~~ → ~~`jb3VQ96s2Vmv5aP4`（v4，岗位库 rerank，留作回退）~~ → ~~`3dx3j3cacsfYdLe8`（v5，留作回退）~~ → ~~`g2XDtP2IvbgTKh8k`（v6，评分总分挪到分项之后，留作回退）~~ → ~~`j5qWmoi0m0UYWDpj`（v7，v6b 技能证据纪律 / 时效说明 / 专业兜底 / 来源冲突裁决）~~ → ~~`wcQKFhBvvTDarYlC`（v7d，v7a/b/c 重练分支 + 收尾硬规则 + 政策拒答给路径）~~ → ~~`bZ98CHD4YaVpajtY`（v7e：面试进度 max(M+1,C) + 重练只走一轮）~~ → ~~`rWxRKhq13wV1PS3X`（v8：要求—证据矩阵 / 隐私遮罩 / 证据四值 / 政策引用溯源）~~ → ~~`Y7oLU89eNCqPvcJV`（v8b：结尾修正 + 评分档位锚点）~~ → ~~`Se6izgWbb0jK9DBZ`（v9：覆盖度统计 + 岗位原文逐字摘录 + 追问预演 + 政策分档）~~ → ~~`l8HJAJ78lH0XfGzn`（v10：面试收尾优先级 + 判定只看标记 + 不打发用户 + 硬门槛判据）~~ → ~~`vs58iotZUg5QX4OG`（v11：会话起始守卫 + 题型标记硬性 + 简历方法分流 + 闲聊收尾四项）~~ → ~~`HeYM5jZOBsKPURdj`（2026-10-15 v12：简历优先规则 + 方法类提问归闲聊 + 分类器纠偏）~~ → ~~v13–v18~~ → **`YnmaDNCRpd1otyrC`（2026-10-20 v19：上下文通道 + 简历上传 + 进度兜底，现役）**。完整版本链与回退站点见 `参赛方案/运行状态与待办.md` |

## 一键门禁与体检

| 文件 | 作用 |
| --- | --- |
| `run_all.py` | 一键门禁：五分支巡检 + 黄金集 + 死链 / 隐私 / 一致性 / H5 四道离线检查 + 草稿漂移，输出 `---SCORE_SUMMARY---` 契约 |
| `h5_lint.py` | 自建前端静态体检：`node --check` 语法、页面里的站点码是否等于 readysite.txt、有无 CDN 外链、`.attach[hidden]` 那条已知回归、无障碍底线、体积预算。`--file` 可查任意副本 |
| `workflow_diff.py` | 线上草稿 vs 仓库快照逐节点比哈希；`--dump-only` 建档、`--restore --yes` 写回 |
| `eval_flake.py` | 黄金集稳定性统计：同一配置跑 N 轮，逐条给通过率，分开「恒定红」与「偶发红」——评委面前翻车的永远是偶发那几条 |
| `gen_submission_form.py` / `make_form_pdf.py` | 生成提交表 docx 与 PDF，正文三段字数超限直接非零退出 |
| `make_materials.py` | 提交材料一键再生：docx → PDF → 二维码 → 终检，四步串起来并当场交叉核对（PDF 里的地址必须等于 readysite.txt、二维码解出来必须含当前站点码）。`--pack 姓名 联系方式` 直接打出官网上传要的 zip，材料缺项默认拒绝打包 |

## scratch/

~~828 个~~ → 实际 **947 个**一次性探查脚本，按产生顺序堆着，没有整理价值。
确认不需要可以直接整个删掉，不影响上面任何工具。

里面值得一提的只有几个：`kblist.js` / `probe2.js` / `oldapp.js` 是查知识库列表、
应用列表作用域、旧版应用状态的；`shots/` 是 16 张自测截图。

## 这个项目踩过的平台坑（都在 `ggg/参赛方案/运行状态与待办.md` 里有详细证据）

- 会话变量写入是空操作：赋值节点返回成功，读回仍是默认值
- 大模型记忆配置齐全但历史从未注入
- `sys.dialogue_count` 在提示词里取不到（inputs 里看得见）
- ~~站点与工作流永久绑定，发布不会让线上地址切换，重置令牌也不行~~ → ~~已推翻~~ →
  **最终结论（2026-10-14 夜，三轮实测）：站点固定执行「建站或复制时刻」那一次发布的版本。**
  之后在同一个 app 上重新 publish，`app.workflow.id` 会更新，但站点仍跑旧版本；
  关站再开也不重新绑定；等 10 分钟也不是缓存问题。**想上线新配置只能重新复制应用、换站点码。**
  （这条来回翻了两次，所以关键结论一定要写成"在什么条件下成立"，别只写结论。）
- **钉死的不只是工作流图，还有 `features`**（2026-10-14 实测）：开场白、预置问题、文件上传白名单
  都存在草稿的 `features` 字段里（**不在草稿顶层，也不在 `app.site`**，`app.site.opening_statement` 是空串）。
  改 `features.opening_statement` → save → publish 全部 200，但站点 `GET /api/parameters`（需带 access_token）
  返回的仍是旧开场白。**所以想改开场白/预置问题同样只能重新复制应用换站点码。**
  副作用：站点的开场白不能用接口热更新，别在这个方向浪费时间。
- 知识库重排（rerank）：4 个检索节点默认全是 `reranking_enable: false`，
  平台其实**提供** `bge-reranker-v2-m3`；开启后「岗位知识库」的召回排序有改善（v4 站点已启用）
- **线上到底开的哪套检索，可以从回复里反推**（2026-10-14 实测确认）：
  **取数路径**：`retriever_resources` 在 `message_end` 事件的**顶层** `metadata` 里 ——
  正确写法 `j["metadata"]["retriever_resources"]`；`message_end` 的 `data` 是**空 dict**
  （顶层 keys = `conversation_id / created_at / event / files / has_graph_rag / id / message_id / metadata / task_id`），
  `workflow_finished.data` 里也没有这个字段。写成 `j["data"]["metadata"]` 会永远取到 0 条 ——
  看起来像「rerank 失效」，其实是取错了地方，别被它骗第二次。
  判定法：`max(score) > 0.75` → reranker 分（不归一化，常见 1.0）；`0.3–0.6` → 加权混合分。
  实测对照（同一条化工求职提问）：
  - 正式站 `jb3VQ96s2Vmv5aP4`（v4）与 `j5qWmoi0m0UYWDpj`（v7）岗位匹配 → **8 条**，
    `1.0 / 0.9903 / 0.9762 / 0.9343 / 0.9266 / 0.92 / 0.8752 / 0.8423`，
    命中 **KB3-专业行业岗位对照库 + KB4-岗位JD库** ⇒ 走的是 rerank。
  - 旧站 `3PNowdyi2c13Khnl` 同题 → 5 条、全部 KB4、`0.51 / 0.505 / 0.505 / 0.504 / 0.5` ⇒ 走的是加权。
  - v7 三个分支同时实测：模拟面试 2 条 `0.2525 / 0.1882`（KB2）、政策咨询 5 条 `0.2561–0.1951`（KB5）、
    岗位匹配 8 条 reranker 分 —— **同一个工作流里两种检索形态并存**，证明 rerank 只作用在岗位库那一个节点上。
- **5 题制的固有语义（2026-10-15 实测确认）**：面试进度行「N/5」表示**即将出的题号**，
  所以答完第 5 题时最后一条消息仍是「第 5 题 / 5/5」，复盘出现在**用户下一条消息之后**。
  `probe_v7d.py` 最初只发 5 条作答就断言「收尾复盘 FAIL」，属**测试断言错误**，已改成全轮扫描。
- **v8–v10 的补丁入口**：`技术档案/scratch/patch.py <edits.json> [app_id] [备注]`（pull → needle 必须**恰好命中 1 次** → push → publish）。
  ⚠️ `技术档案/draft.py push <body.json>` 是**整份覆盖**草稿，会冲掉平台上已有的提示词补丁；
  结构改动必须放最后一次，顺序是「先 pull → patch.py 打补丁 → 最后才 push 结构」。
  中文 needle/repl 必须先写成 UTF-8 的 JSON 文件，别在 Python 源码里写中文字面量。
- 克隆站点模板：`技术档案/clone_v8.py` / `clone_v8b.py` / `clone_v9.py` / `clone_v10.py`
  （改 SRC/OLD/标记清单 → 复制应用 → 恢复图标 → publish → 旧正式站改名加「（回退 · vN）」）。
