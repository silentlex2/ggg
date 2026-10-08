# 2026年"天翼AI"杯重庆高校人工智能大赛（重庆理工大学赛区）官网 — 抓取报告

> 抓取时间：2026-10-08 · 目标：`http://aiac.cqut.edu.cn:3090/` · 方式：公开只读 GET（未使用任何账号，未调用任何写接口）

---

## 一、站点基本信息

| 项 | 值 |
| --- | --- |
| 站点地址 | `http://aiac.cqut.edu.cn:3090/` |
| 服务器 IP | `113.249.119.51` |
| Web 服务器 | nginx |
| 协议 | **仅 HTTP**（同端口 3090 不支持 HTTPS，TLS 握手报 `wrong version number`） |
| 站点标题 | 2026年"天翼AI"杯重庆高校人工智能大赛 |
| 站点描述 | 2026年"天翼AI"杯重庆高校人工智能大赛 |
| 前端框架 | **Nuxt 3**（SSR 关闭，纯客户端渲染 SPA），前端版本 **1.9.0** |
| 后端框架 | **likeadmin**（`shop_name` 字段值为 `likeadmin`），后端版本 **1.9.4** |
| 管理后台 | `http://aiac.cqut.edu.cn/admin` |
| 站点 logo | `uploads/images/20260720/20260720140502e0e0f2879.png` |
| 站点图标 | `uploads/images/20260720/20260720141701c5a075401.ico` |
| 登录页配图 | `uploads/images/20260923/20260923182946ca4a77299.webp` |
| 登录方式 | `login_way: [1]`（账号密码），支持第三方登录 `third_auth:1`、微信 `wechat_auth:1`、QQ 关闭 |
| robots.txt | `User-agent: *` + `Disallow:`（空）→ 允许全站抓取 |

## 二、站点定位与背景

这是**重庆理工大学**联合**中国电信股份有限公司重庆分公司**举办的校级人工智能竞赛平台，
赛事全称：**2026 年"天翼AI"杯重庆高校人工智能大赛（重庆理工大学赛区）**。

- **大赛主题**：智创校园 · 赋能未来
- **承办背景**：落实国家创新驱动发展战略、教育部"人工智能赋能教育行动"及数字重庆建设部署
- **开发平台**：所有参赛作品必须基于学校**"智小理"智能体平台**开发
- **冠名赞助**：中国电信重庆分公司

## 三、前端页面结构

从 `entry.js` 提取的路由表（共 19 个页面/动态路由）：

| 路径 | 页面标题 | 说明 |
| --- | --- | --- |
| `/` | 首页 | 大赛门户首页 |
| `/intro` | 大赛简介 - 天翼AI杯 | 赛事介绍 |
| `/ai` | 智小理智能体平台 - 天翼AI杯 | 开发平台入口 |
| `/guide/:id` | 参赛指南 - 天翼AI杯 | 指南详情 |
| `/materials`、`/materials/:id` | 大赛资料 - 天翼AI杯 | 资料下载列表/详情 |
| `/notice/:id` | 详情 - 天翼AI杯 | 公告详情 |
| `/showcase`、`/showcase/:id` | 成果展示 - 天翼AI杯 | 作品展示（含"全部/获奖作品/部门风采"分类） |
| `/recruit`、`/recruit/:id` | 招募队伍 - 天翼AI杯 | 指定命题招募/组队 |
| `/apply` | 大赛报名 - 天翼AI杯 | 报名表单 |
| `/submit` | 作品提交 - 天翼AI杯 | 作品提交 |
| `/topic` | 课题管理 - 天翼AI杯 | 命题发布方管理 |
| `/search` | 搜索 - 天翼AI杯 | 站内搜索 |
| `/contact` | 联系我们 - 天翼AI杯 | 联系方式 |
| `/login`、`/register`、`/forgot` | 登录 / 注册 / 忘记密码 | 账号体系 |
| `/user/center`、`/user/info`、`/account/security` | 个人中心 | 用户中心、收藏、话题 |

## 四、内容抓取结果总览

| 模块 | 接口 | 条数 | 备注 |
| --- | --- | --- | --- |
| 轮播图 | `/api/comp.banner/lists` | 1 | banner1 |
| 大赛新闻 | `/api/comp.news/lists` | 1 | 赛事启动新闻 |
| 通知公告 | `/api/comp.notice/lists` | 3 | 含大赛正式通知全文 |
| 参赛指南 | `/api/comp.guide/lists` | 5 | 参赛要求 / 报名 / 奖项 / 作品要求 / 提交要求 |
| 大赛资料 | `/api/comp.material/lists` | 10 | 手册、模板、PDF 下载 |
| 成果展示 | `/api/comp.showcase/lists` | **0** | `全部 / award / dept` 三类均为空 |
| 招募队伍 | `/api/comp.recruit/lists` | **0** | 招募通道当前未开放 |
| 学院选项 | `/api/comp.college/options` | 55 | 全校 55 个学院 / 单位 |
| 作品类别 | `/api/comp.workCate/options` | 4 | 四大赛道 |
| 命题时间设置 | `/api/comp.recruit/topicSetting` | 1 | 发布期 2026-09-16 ~ 09-28，当前 `is_open: 0` |

## 五、大赛核心信息（据公告与指南整理）

### 1. 组织单位

- **指导单位**：重庆理工大学、中国电信股份有限公司重庆分公司
- **主办单位**：重庆理工大学信息中心、中国电信股份有限公司巴南分公司
- **承办单位**：计算机科学与工程学院
- **协办单位**：宣传部、校团委、教务处、研究生院、学生处、两江国际学院
- **技术支持**：计算机科学与工程学院、两江人工智能学院、重庆电信大数据和 AI 中心、中国电信巴南分公司
- **赛事咨询**：钟老师，电话 `62563266`

### 2. 参赛对象与组队规则

- 对象：重庆理工大学在读学生（本科生、研究生、留学生）
- 队伍：1—4 人，指定 1 名队长，队长负责报名与材料提交；可单人参赛，可自愿选填指导教师
- 限制：每人仅限报 1 支队伍，不得跨队重复报名
- 锁定：报名截止后队员名单与项目名称不可修改；每队限交 1 件作品
- 费用：**不收取参赛费**，比赛算力由中国电信免费提供

### 3. 四大赛道

| 赛道 | 主要场景 | 评审侧重 |
| --- | --- | --- |
| 管理服务智能体 | 校园办事、智能迎新/毕业、设施预约等 | 解决服务痛点，7×24 小时响应，具备推广条件 |
| 教学赋能智能体 | AI 课程助教、作业批改等 | 服务教学活动，结合课堂实际，提升教学效率与质量 |
| 科研赋能智能体 | 科研文献分析、数据分析、实验设计优化等 | 提高科研效率，突破科研瓶颈 |
| 其它创意智能体 | 多模态交互、个性化陪伴等 | 突出创新性、体验性、前瞻性，鼓励跨界融合 |

### 4. 选题方式

- **自主命题**：队伍结合赛道与学校实际自主确定开发内容，须审核通过
- **指定命题**：校内单位提出真实需求 → 主办单位审核后公开发布 → 学生选定后由命题单位双向沟通**择优确定 1 支队伍**
- 二者**择一申报，不得兼报**；指定命题未获选者可转报自主命题

### 5. 关键时间节点

| 时间 | 事项 |
| --- | --- |
| 2026-07-17 | 大赛正式通知发布 |
| 2026-09-11 ~ 09-18 | 各单位指定命题发布人注册并提交命题需求 |
| 2026-09-20 18:00 | 命题征集截止 |
| 2026-09-16 ~ 09-28 | 命题发布窗口（系统 `topicSetting`） |
| 2026-09-23 ~ 09-28 | 指定命题报名 |
| 2026-09-24 ~ 10-20 | 自主命题报名（10-20 含当日有效） |
| 2026-09-28 | 指定命题截止，命题单位确定队伍 |
| 2026-09-30 前 | 命题发布人登录官网确定 1 支开发队伍 |
| 2026-11-10 18:00 | **作品提交截止**（逾期无效） |
| 总决赛 | 5 分钟路演 + 3 分钟答辩 |

### 6. 奖项设置

| 奖项 | 名额 | 奖励 |
| --- | --- | --- |
| 特等奖 | 1 名 | 6000 元 + 奖杯 + 荣誉证书 |
| 一等奖 | 2 名 | 3000 元 + 奖杯 + 荣誉证书 |
| 二等奖 | 4 名 | 2000 元 + 奖杯 + 荣誉证书 |
| 三等奖 | 8 名 | 1000 元 + 奖杯 + 荣誉证书 |
| 优秀奖 | 10 名 | 奖品 + 荣誉证书 |
| 优秀指导老师 | 若干 | 荣誉证书 |

> 奖金均为**税前**标准，个税自理。另含学校学分奖励及电信公司实习机会。

### 7. 作品与提交要求

- 作品须为**智能体**，且必须基于学校"智小理"平台开发
- 需 3 分钟以内演示视频，清晰展示功能模块、操作流程、应用效果与核心优势
- 须原创，严禁抄袭；存在知识产权纠纷或违背法律法规、公序良俗者不得参赛
- **版权归学校所有**，学校有权修改、使用、宣传，不另付稿酬；材料概不退还
- 初赛材料：① 作品提交表（PDF）② 团队活动记录图片/视频（图片 ≥3 张，视频 ≥30 秒）③ 演示视频（≤3 分钟）
- 打包命名格式：**队长姓名 + 联系方式**，通过官网指定端口提交


## 六、通知公告（3 篇，全文见 `content/`）

| # | 标题 | 发布 | 全文 |
| --- | --- | --- | --- |
| 1 | 关于举办 2026 年"天翼 AI"杯重庆高校人工智能大赛（重庆理工大学赛区）的通知 | 2026-07-17 | [链接](./content/) |
| 6 | 关于征集 2026 年"天翼AI"杯重庆高校人工智能大赛征集指定命题的通知 | 2026-09-14 | [链接](./content/) |
| 7 | 关于"指定命题"截止和确定队伍的通知 | 2026-09-28 | [链接](./content/) |

公告 1 是本次大赛的**纲领性文件**，共十二节：大赛主题、参赛对象与组队要求、赛道设置、选题方式、
报名安排、作品要求、评审方式、赛程安排、奖项设置、参赛权益、组织单位、其他事项。
公告 6 面向校内单位征集"指定命题"，明确了命题方向、命题要求、发布流程与时间安排。

## 七、参赛指南（5 篇，全文见 `content/`）

| # | 标题 | 图标 | 核心内容 |
| --- | --- | --- | --- |
| 1 | 参赛要求 | `icon-saishi` | 参赛对象（重理工在读学生）+ 四大赛道分类及要求 |
| 2 | 大赛报名 | `icon-navicon-bmjl` | 报名规则 6 条：报名方式、组队人数、人员限制、选题类型、选题规则、注意事项 |
| 3 | 奖项设置 | `icon-quanyi` | 特等奖 1 名 6000 元 / 一等 2 名 3000 元 / 二等 4 名 2000 元 / 三等 8 名 1000 元 / 优秀奖 10 名 |
| 4 | 作品要求 | `icon-zuzhushouce` | 技术要求、功能要求、原创要求、演示要求、版权要求 |
| 5 | 提交要求 | `icon-saishi` | 初赛/决赛提交材料、命名格式、提交方式与材料要求 |

## 八、大赛资料（10 项，含可下载附件）

| # | 标题 | 类型 | 时间 | 附件（已下载） |
| --- | --- | --- | --- | --- |
| 10 | 智小理平台使用手册 | manual | 2026-09-29 | `assets/files/.../20260929110533cf8534979.docx`（25 MB） |
| 9 | 2026 年"天翼 AI"杯…作品提交表 | manual | 2026-09-24 | `assets/files/.../20260924102044c59e90534.docx`（118 KB） |
| 8 | 智能体开发大赛选题参考方向 | manual | 2026-09-20 | `assets/files/.../20260920150451a96b89185.docx`（42 KB） |
| 7 | 重庆理工大学-学生登录报名操作手册 | manual | 2026-09-17 | `assets/files/.../202609171437018e8f85934.pdf`（881 KB） |
| 6 | 重庆理工大学-教师发布课题与指定队伍操作手册 | manual | 2026-09-17 | `assets/files/.../2026091714363635d5c3702.pdf`（544 KB） |
| 5 | 大赛官网注册指南-教师版 | manual | 2026-09-15 | `assets/files/.../20260915150828b6a468605.pdf`（798 KB） |
| 4 | 大赛官网注册指南-学生版 | manual | 2026-09-15 | `assets/files/.../20260915150702df6d91567.pdf`（808 KB） |
| 3 | 星辰超级智能体介绍 | video | 2026-09-14 | `assets/videos/.../20260914113407a4fde7696.mp4`（20.7 MB） |
| 2 | 星辰超级智能体 TeleAgent·桌面版--操作手册 | manual | 2026-07-20 | 外链 `teleai.com.cn/doc/...`（未下载） |
| 1 | 星辰超级智能体 TeleAgent·桌面版--下载链接 | manual | 2026-07-20 | 外链 `teleai.com.cn/product/teleagent`（未下载） |

> 说明：第 1、2 项是**中国电信"星辰/TeleAgent"产品**的外部链接，不是本站资源，因此只记录未下载。


## 九、接口分析

### 1. 调用约定

前端所有请求都走统一封装：`$request.get({ url: "...", params: {...} })`，最终地址为
`{apiUrl}{apiPrefix}{url}` = `http://aiac.cqut.edu.cn:3090/api{url}`（见 `entry.js` 中的
`window.__NUXT__.config.public`）。

### 2. 统一响应格式

```json
{ "code": 1, "show": 0, "msg": "", "data": { ... } }
```

- `code: 1` 表示成功，`code: 0` 表示失败
- 列表型数据的 `data` 结构为：`{ lists: [...], count, page_no, page_size, extend }`

### 3. 分页与筛选参数

| 参数 | 说明 |
| --- | --- |
| `page_no` / `page_size` | 分页（默认 `page_size=25`，最大实测可用 200） |
| `id` | 详情查询 |
| `showcase_cate` | 成果展示分类：`award`（获奖作品）/ `dept`（部门风采） |
| `keyword` | 站内搜索（`/comp.search/index`） |

### 4. 公开接口（本次已调用，全部返回 200）

| 接口 | 说明 |
| --- | --- |
| `GET /api/pc/config` | 站点配置（logo、标题、登录方式、后台地址、版本） |
| `GET /api` | PC 端页面配置（当前仍是 likeadmin 演示数据） |
| `GET /api/index/policy` | 协议/隐私政策（当前为空） |
| `GET /api/comp.banner/lists` | 轮播图 |
| `GET /api/comp.news/lists` `…/detail` | 大赛新闻 |
| `GET /api/comp.notice/lists` `…/detail` | 通知公告 |
| `GET /api/comp.guide/lists` `…/detail` | 参赛指南 |
| `GET /api/comp.material/lists` `…/detail` | 大赛资料（含附件、视频） |
| `GET /api/comp.recruit/lists` `…/detail` | 招募队伍 |
| `GET /api/comp.showcase/lists` `…/detail` | 成果展示 |
| `GET /api/comp.workCate/options` | 作品类别（4 个赛道） |
| `GET /api/comp.college/options` | 学院/单位选项（55 个） |
| `GET /api/comp.recruit/topicSetting` | 命题发布窗口与开关 |
| `GET /api/comp.page/detail` | 单页内容 |
| `GET /api/comp.search/index` | 站内搜索 |

### 5. 需登录 / 写操作接口（**本次未调用**）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/login/account`、`/api/login/register`、`/api/login/logout` | POST | 账号登录/注册/登出 |
| `/api/login/getScanCode`、`/api/login/scanLogin` | GET/POST | 扫码登录 |
| `/api/sms/sendCode` | POST | 短信验证码 |
| `/api/user/info`、`/api/user/setInfo`、`/api/user/bindMobile` | GET/POST | 用户资料 |
| `/api/user/changePassword`、`/api/user/resetPassword`、`/api/user/resetPasswordByIdentity` | POST | 密码相关 |
| `/api/user/collection`、`/api/user/topic` | GET/POST | 收藏、话题 |
| `/api/comp.apply/*` | GET/POST | 报名（设置、详情、元数据、我的报名、提交、教师审核、命题队伍） |
| `/api/comp.work/submit`、`/api/comp.work/myLists`、`/api/comp.work/myScores` | GET/POST | 作品提交与成绩 |
| `/api/comp.recruit/publish`、`/api/comp.recruit/myLists` | GET/POST | 命题发布与我的发布 |
| `/api/upload/file`、`/api/upload/image`、`/api/upload/video` | POST | 文件上传 |
| `/api/article/collect`、`/api/article/cancelCollect` | POST | 文章收藏 |

> 以上接口仅从打包代码中静态提取，**未发送任何请求**。涉及账号、短信、提交类操作一律未触碰。

## 十、静态资源清单（已下载 19 个文件，共约 50 MB）

| 大小 | 文件 | 说明 |
| --- | --- | --- |
| 25.0 MB | `assets/files/uploads/file/20260929/…docx` | 智小理平台使用手册 |
| 20.7 MB | `assets/videos/uploads/video/20260914/…mp4` | 星辰超级智能体介绍视频 |
| 0.9 MB | `assets/files/uploads/file/20260917/…8e8f85934.pdf` | 学生登录报名操作手册 |
| 0.8 MB | `assets/files/uploads/file/20260915/…df6d91567.pdf` | 官网注册指南-学生版 |
| 0.8 MB | `assets/files/uploads/file/20260915/…b6a468605.pdf` | 官网注册指南-教师版 |
| 0.5 MB | `assets/files/uploads/file/20260917/…35d5c3702.pdf` | 教师发布课题操作手册 |
| 0.5 MB | `assets/images/uploads/images/20260923/…a4a77299.webp` | 登录页配图 / 首页 banner |
| 0.3 MB | `assets/images/resource/image/adminapi/default/article01.png` | likeadmin 演示图 |
| 0.2 MB | `assets/images/uploads/images/20260717/…412443357.png` | 公告正文配图 |
| 0.1 MB | `assets/files/uploads/file/20260924/…c59e90534.docx` | 作品提交表模板 |
| 其余 | 站点 logo、favicon、新闻配图、选题参考方向 docx 等 | 见 `assets/_manifest.json` |


## 十一、观察与发现

抓取过程中注意到的一些细节，可作为分析/改进的切入点：

1. **PC 端首页配置仍是框架自带演示数据**
   `GET /api` 返回的页面配置里，页面名还是"商城首页"，轮播图指向
   `/resource/image/adminapi/default/banner001.png`，链接标题是"来自瓷器的爱""金山电池公布'沪广深市民绿色生活方式'调查结果"
   等 likeadmin 官方 demo 内容，并未替换成大赛相关配置。实际首页由前端自定义组件渲染，未使用这套页面配置。

2. **两个内容模块为空**
   `/api/comp.showcase/lists`（成果展示）与 `/api/comp.recruit/lists`（招募队伍）在
   `全部 / award / dept` 三种分类下均返回 0 条。结合 `topicSetting` 显示
   `is_open: 0`（提示"当前不在发布期限内"），说明招募/展示通道尚未开放或已关闭。

3. **前后端版本号不一致**
   前端构建版本 `1.9.0`（`__NUXT__.config.public.version`），后端接口返回 `version: "1.9.4"`。

4. **全站明文 HTTP**
   站点仅监听 3090 端口的 HTTP，同端口不支持 HTTPS。学生报名需提交姓名、学号、手机号等信息，
   明文传输存在隐私风险；同时页面里还有扫码登录、短信验证码等敏感入口。

5. **管理后台地址直接暴露**
   `/api/pc/config` 的响应中明文包含 `admin_url: "http://aiac.cqut.edu.cn/admin"`，
   任何人都能直接拿到后台入口。

6. **内容里的两处笔误**
   - 公告 7 落款为"**2029 年** 9 月 28 日"（应为 2026 年）
   - 公告 6 与指南 2 中官网链接写成 `https://http://aiac.cqut.edu.cn:3090/`（协议头重复，且与站点实际 HTTP 不符）

7. **接口无鉴权即可读取全部公开内容**
   本次抓取未使用任何账号，仅凭公开 GET 接口就取到了公告、指南、资料附件、视频等全部内容；
   robots.txt 亦为全站允许。

8. **代码层面**：前端为 Nuxt 3 打包产物（49 个 chunk），未做源码映射（无 `.map`），
   接口路径与业务逻辑均以明文常量形式存在于 bundle 中。

## 十二、目录结构与复现方法

```
site-dump/
├── report.md              本报告
├── crawl.log              抓取日志（接口调用记录）
├── chunks/                前端 49 个 JS chunk（含 entry）
├── api/                   接口原始响应 JSON
│   ├── pc-config.json     站点配置
│   ├── list-*.json        各模块列表
│   ├── detail/*.json      各条目详情（按 模块-id 命名）
│   ├── _lists.json        列表汇总
│   └── _details.json      详情汇总
├── content/               可读 Markdown（公告/指南/新闻全文 + 资料清单 + 学院清单）
└── assets/                下载的图片 / 文档 / 视频
    ├── images/  files/  videos/
    └── _manifest.json     资源清单（含外链记录）
```

### 复现命令

```bash
# 1. 站点配置与列表
curl -s "http://aiac.cqut.edu.cn:3090/api/pc/config"
curl -s "http://aiac.cqut.edu.cn:3090/api/comp.notice/lists?page_no=1&page_size=50"

# 2. 详情（id 来自列表）
curl -s "http://aiac.cqut.edu.cn:3090/api/comp.notice/detail?id=1"
curl -s "http://aiac.cqut.edu.cn:3090/api/comp.material/detail?id=10"

# 3. 前端资源
curl -s "http://aiac.cqut.edu.cn:3090/_nuxt/entry.2d897bb2.js" -o entry.js
curl -s "http://aiac.cqut.edu.cn:3090/_nuxt/comp.003d71ee.js" -o comp.js   # 全部接口定义在这
```

### 合规说明

本次抓取**仅访问公开可读接口**（HTTP GET），全程限速 0.35~0.4 秒/请求，未并发轰炸；
**未**使用任何账号登录，**未**调用登录、短信验证码、报名提交、作品提交、文件上传等任何写接口；
robots.txt 明确允许全站抓取。数据仅用于作业分析。

