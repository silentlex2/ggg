# 职引 · 自建前端（H5）

一个**单文件静态页** `职引-H5.html`，直连星辰平台的公开 API，用来解决平台自带页面解决不了的三件事：

| 平台自带页面 | 这个 H5 |
| --- | --- |
| 首屏是 4 个表单字段，评委第一眼是懵的 | 任务卡片 + 预设问题 + 对话流 |
| **LLM 节点拿不到会话历史**（实测），多轮必丢上下文 | 前端保存每轮发言，压成 `〔历史〕…` 塞进 `inputs.ctx`，平台侧提示词按"这就是上文"来用 |
| 表格/报告排版差、移动端体验一般 | 卡片式报告、横向表格、进度条、移动端自适应 |
| 答案不给引用来源，看不出「有依据」还是「编的」 | 每轮把 `metadata.retriever_resources` 渲染成溯源标签（如 📚 岗位库 ×5） |
| 报告看完就没了，学生要给老师看只能截图 | 「导出」一键存成 Markdown（含每轮引用来源） |

## 用法

1. 本地直接双击打开（`file://` 也能用，因为平台 API 的 CORS 是 `*`）。
2. 想给学生扫码：把 `职引-H5.html` 丢到任意静态托管（GitHub Pages / 校内静态目录），
   再把 `参赛方案/素材/职引-二维码-公开站点.png` 指向该地址即可（`技术档案/make_qr.py` 目前只认平台站点码，
   换成 H5 地址需要改一行 URL）。

## 关键实现

- 对端应用：v19 `214d5f6b-c1ca-4bc8-9ee7-02be1f1ecbf4`（站点 `YnmaDNCRpd1otyrC`）
- `POST https://aiagent.cqut.edu.cn:31134/v1/chat-messages`
  - `Authorization: Bearer app-…`（**应用级 API key，内嵌在页面里；公开页专用，可随时在控制台吊销**）
  - `response_mode: "blocking"` —— 本 fork 的 `streaming` 只回一个事件，拿不到完整答案；
    打字机效果在前端本地做
  - `inputs: { user_input, ctx }`，`ctx` 对应工作流 start 节点的可选变量
- 会话状态（`conversation_id`、消息、面试进度）存在 `localStorage`，键名 `zhiyin.v1`
- 面试进度条从答案里正则抓 `面试进度：N/5`
- **溯源标签**：blocking 响应的 `metadata.retriever_resources` 带 `dataset_name` 与 `score`，
  前端按数据集聚合、取最高分，渲染成 `📚 岗位库 ×5`（悬停看命中段数与最高匹配分）。
  标签随消息一起存进 `localStorage`，刷新后照样显示；导出 Markdown 时写成 `> 参考：岗位库 ×5`。
  数据集名到中文名的映射在页面里的 `KBLABEL`（KB1 简历规范库 / KB2 面试题库 / KB3 专业岗位对照 /
  KB4 岗位库 / KB5 政策库 / KB6 常见问答），新增库要同步这张表。
- **导出**：把会话按「## 我 / ## 职引」拼成 Markdown，用 Blob 下载成 `职引-会话-YYYY-MM-DD.md`。

## 对应的平台侧改动（v19，最终口径）

1. start 节点新增可选变量 `ctx`（`paragraph`，2000 字上限）
2. **只给**「闲聊引导」与「岗位匹配」两个节点的提示词追加「历史上下文」纪律块，
   并插入 `{{#1791542455112.ctx#}}`
3. **模拟面试官一个字没动**——v16/v17 给它加同一段块后，多轮面试进度全崩
   （进度倒退 `[1,2,1,0]`、模型自称"这场面试还没开始"，黄金集掉到 0.850）
4. 其余不变（25 节点）

> 这条链路的证据见 [技术档案/history.md](../技术档案/history.md) 与交接说明第 2 节：
> 平台确实不向任何 LLM 节点注入历史；`ctx` 透传是用暗号测试验证过的（问"我学号尾号多少"，回答 7391）。

## 实拍证据（2026-10-20，浏览器实跑 v19）

| 图 | 内容 |
| --- | --- |
| [01-溯源标签.png](../过程截图/2026-10-20-v19-H5/01-溯源标签.png) | 桌面宽度：政策回答底部 `📚 政策库 ×3` `📚 常见问答 ×2`，头部有「导出」 |
| [02-移动端-岗位库溯源.png](../过程截图/2026-10-20-v19-H5/02-移动端-岗位库溯源.png) | 390×844 视口（DPR 2）：岗位回答底部 `📚 岗位库 ×5`，窄屏头部单行不折行 |

出图方式：`owb open "file:///<路径>/职引-H5.html"` → `owb eval "send('…')"` 真跑一轮 →
`owb cdp --args '{"method":"Emulation.setDeviceMetricsOverride","params":{"width":390,"height":844,"deviceScaleFactor":2,"mobile":true}}'` → `owb shot --out <路径>`。
注意 `owb cdp` 不认扁平参数，`method`/`params` 必须嵌套；后台标签页直接截图会 `Page.captureScreenshot` 超时，
先 `owb cdp --method Page.bringToFront` 再拍。
