# AI Creative Toolkit

通用 AI 内容创作工具集,含 skill、工具脚本、共用素材。适配任意 agent 环境。

> 本文件是单一真相源。`CLAUDE.md` 是指向它的软链接——Claude Code 约定读 `CLAUDE.md`,其他 agent(Hermes/OpenClaw/Codex/Copilot…)读 `AGENTS.md`,内容一致,改这里即可。

## Project Structure

```
skills/text-to-card/      # 文章转图文卡片 skill(通用版)
skills/harvest-topics/    # 素材转选题候选 skill(通用版)
skills/submit-to-inbox/   # 素材提交(带降级) skill(通用版)
skills/gzh-longform/      # 公众号长文(两阶段) skill
skills/gzh-illustration/  # 公众号配图(HTML→截图) skill
skills/gzh-typeset/       # 公众号排版(article.md→wechat.html) skill
skills/remotion-video/    # Remotion 视频创作 skill
skills/video-asset-library/ # 视频素材库管理 skill
tools/                    # 独立工具/脚本
tools/asset-library-web/  # 视频素材库静态橱窗(gallery.html)
assets/                   # 共用素材/模板
```

## 内容生产管线(架构)

各 skill 是独立的 `skills/<name>/SKILL.md` 工作流,通过**目的仓库**里的中间产物解耦,不互相调用:

```
收集端 ──提交──▶ Topics/inbox/ ──加工──▶ Topics/backlog.md ──取选题──▶ gzh-longform ──▶ article.md ──▶ {gzh-typeset, gzh-illustration} ──▶ 发布
                                                                                            ▲
                                          text-to-card(文章转卡片,独立支线)
```

- `submit-to-inbox`(收集端):各收集 agent 把素材(链接/文字/图)提交到**目的仓库** `Topics/inbox/`。三级降级(gh cli → GitHub API → 本地 `inbox-fallback/`),素材绝不丢。
- `harvest-topics`(加工端):扫 inbox → 解析 → 过目标人群筛 → 加工成 `Topics/backlog.md` 选题候选。**只追加,不改已有**。
- `gzh-longform`(写作端):**从 backlog 取选题**(不从 inbox 取原始素材),两阶段(研究→写作,中间硬闸门)出 `article.md`。
- `gzh-typeset`(排版端):把 `article.md` 排成全 inline 样式的 `wechat.html`,可一键复制粘贴公众号后台。
- `gzh-illustration`(配图端):给长文配图(读占位 → HTML → Playwright 截图 → 回填,草稿/定版两态)。
- `text-to-card`(独立支线):文章转图文卡片(小红书/公众号),大纲→HTML→截图。

**解耦原则:** 收集↔写作靠 `Topics/inbox/` 和 `Topics/backlog.md`(目的仓库的中间产物)通信,不直接耦合。各 skill 自带脚本,互不调用(gzh-longform / gzh-typeset / gzh-illustration 都不调 text-to-card)。

**目的仓库 vs 本仓库:** skill 装在各 agent 的项目里;`Topics/inbox/`、`Content/<组>/article.md` 等产出在**目的仓库**(用户的内容仓),不在这个 skill 仓。skill 不假设本地有目的仓库——本地有就本地读写,没有就走 `gh`/API 远程。

## Commands

Python 一律走 `uv`(全局规则)。本仓无 build / lint——是 skill 仓,不是应用。

### 测试(纯 stdlib unittest,逐个跑)

```bash
uv run python skills/gzh-longform/scripts/test_wordcount.py
uv run python skills/gzh-illustration/scripts/test_replace_placeholders.py
```

### 关键脚本(各 skill 工作流内调用)

| 脚本 | 作用 |
|------|------|
| `skills/gzh-longform/scripts/wordcount.py <article.md>` | 数字数 + 查结构;定版前必跑,**0 报警才定版** |
| `skills/gzh-typeset/scripts/punct_normalize.py <file.md\|.html>` | 标点全角化(遮罩保护 frontmatter / URL / markdown 语法 / CSS,只改正文) |
| `skills/gzh-illustration/scripts/replace_placeholders.py` | 占位 → 图片回填(草稿/定版两态) |
| `skills/{text-to-card,gzh-illustration}/scripts/screenshot.py` | Playwright + Chromium 截图;`gzh-illustration` 有自己的 `pyproject.toml` / `uv.lock`(playwright 依赖,`uv sync` 装) |

## Skills

### text-to-card

需要做图文卡片时,严格遵循 `skills/text-to-card/SKILL.md` 中的完整工作流。

**触发词:** "图文卡片"、"文章转卡片"、"做卡片"、"小红书卡片"

**核心流程(第0步 + 7步):**
0. 运行参数(OUTPUT_DIR / HTML_PATTERN / PNG_SUBDIR,问用户存运行变量)+ 设计模板(动态获取/复用/自定义)
→ ① 接收文章 → ② 大纲(封面+内容+结尾) → ③ 分页+尺寸+平台 → ④ 生成HTML(基准卡先行) → ⑤ 预览 → ⑥ 修改/确认 → ⑦ 定版+截图

**关键规则(必读):**
- 先读 SKILL.md 再动手,里面有大量实战教训
- **开工前第0步必做**:问用户确定输出目录/命名/设计模板,无固定默认
- delegate_task 批量生成 HTML 时必须附基准卡源码,否则风格不一致
- 内容卡文字精简大字换行,不要长段落
- 封面/结尾页用 absolute 定位铺满,不复用内容卡 flex
- card-number 必须衬线体(Playfair Display),不用等宽体
- 章节标签(WHY/WHAT/TOOLS/HOW)边缘标注,不占独立页
- 用户说"确认/归档/覆盖"→ 直接执行,不反问
- 用户说"?"或纠正 → 先理解意图再回应,不跳执行

**设计模板:** `skills/text-to-card/templates/`(DESIGN.md 格式,默认 `agentic.md`;可从 `nexu-io/open-design` 动态获取或自定义,详见 SKILL.md 第0b 步)

**截图工具:** `skills/text-to-card/scripts/screenshot.py`(Playwright + Chromium)

**IM 对话型 agent 环境**(Hermes/OpenClaw/QwenPaw)的预览/发图/取图/路径见 `skills/text-to-card/references/im-agent-env.md`

### harvest-topics

把目的仓库 `Topics/inbox/` 里各收集 Agent 倒进来的素材,加工成 `Topics/backlog.md` 选题候选。**不依赖本地是否 clone 主仓**(本地有 Topics→本地读写;没有→gh/api 远程),开源通用。

**触发词:** "加工inbox"、"收获选题"、"处理素材"、"素材转选题"

**核心流程(第0步 + 6步):** 读目标人群规范 → ① 扫inbox → ② 解析(link/text/image) → ③ 过目标人群筛 → ④ 加工选题(标题/痛点/工具/方向/卡数) → ⑤ 追加backlog → ⑥ 归档+汇报

**关键规则:**
- **场景驱动,不是工具驱动**——从受众真实工作痛点切入,不是"拿专业工具教人"
- 先读目的仓库 `AGENTS.md` 目标人群再加工;画像不全就停下问用户
- 只追加 backlog,不改已有条目
- 访问:本地有 Topics→本地;没有→gh cli 优先,GitHub API 次之

### submit-to-inbox

把一条素材(链接/文字/图片)安全提交到目的仓库 `Topics/inbox/`。**带降级,素材绝不丢**:gh cli → GitHub API → 本地兜底(skill 目录 `inbox-fallback/`)。不依赖本地 clone 主仓。

**触发词:** "提交素材"、"存到inbox"、"这个存一下"

**核心流程(6步):** ① 整理成inbox格式 → ② 确定仓库+认证(gh优先) → ③ 提交(gh→API降级) → ④ 没认证则引导(gh auth login / PAT) → ⑤ 连不上则本地兜底 → ⑥ 汇报

**关键规则:**
- **素材绝不丢**:提交失败必兜底到 `inbox-fallback/`,远程通了自动补提
- gh cli 优先(用户 `gh auth login` 过即可),别一上来要 token
- 不假设本地有主仓;`inbox-fallback/` 进 .gitignore

**配合:** 收集端(Hermes/OpenClaw/Codex/CC)用本 skill 提交素材 → harvest-topics 加工。两者通过目的仓库 `Topics/inbox/` 解耦。

### gzh-longform

写公众号长文时,遵循 `skills/gzh-longform/SKILL.md` 的两阶段工作流(研究 + 写作,中间硬闸门)。

**触发词:** "公众号长文"、"公众号文章"、"写长文"、"深度图文"

**核心流程(第0步 + 6步):**
0. 运行参数(OUTPUT_DIR/字数/是否查证)+ 读目的仓库人设(整篇读 AGENTS.md/CLAUDE.md)
→ ① 接收选题(backlog 取 或 当场给)→ ② 事实查证(可选联网)→ ③ 定核心观点+结构+字数预算 → **用户确认研究简报(硬闸门)** → ④ 生成正文 → ⑤ 自检 → ⑥ 定版

**关键规则:**
- 通用版,不写死人设;人设读目的仓库 AGENTS.md/CLAUDE.md,缺关键字段停下问用户
- 选题从 backlog(加工过的),不从 inbox(原始素材)
- 字数预算第 3 步分到每段,先控字数再写(不写长再砍)
- 核心观点是"明确主张",不强求反常识
- 事实查证用 agent 可用联网能力,无则标注跳过;二手不许当原话
- 定版前必跑 `scripts/wordcount.py`,0 报警才定版
- 不调用 md-to-wechat / text-to-card / 任何第三方 skill
- 字数脚本不做禁用词,归 agent 自检

### gzh-illustration

给公众号长文配图时,遵循 `skills/gzh-illustration/SKILL.md` 的工作流。

**触发词:** "公众号配图"、"文章配图"、"封面图"、"配图生成"

**核心流程(第0步 + 5步):**
0. 运行参数(文章路径/设计预设/输入方式)+ 读设计系统
→ ① 解析配图清单(读占位 或 当场给)→ ② 基准图先行(封面+第一张正文图,确认风格)→ ③ 批量出其余(逐张审)→ ④ 回填草稿态(保留描述)→ ⑤ 定版(清描述只留图)

**关键规则:**
- 独立 skill,不调 text-to-card;自带 `scripts/screenshot.py`(Playwright)
- 占位格式:`> 🖼️ 【配图N · 尺寸 · 来源】描述`,来源=生成/自供(可缺省默认生成)
- 草稿/定版分态:草稿保留占位描述+图片并存,定版清描述只留图
- 基准图先行:封面+1 张正文图定风格,确认后批量
- 截图前 `document.fonts.ready` + 300ms 等字体
- 尺寸:封面 900×383,正文宽 1080 高度自由
- 自供图路径缺失报警不回填

### gzh-typeset

给公众号长文排版时(把 `article.md` 排成可粘贴公众号的 `wechat.html`),遵循 `skills/gzh-typeset/SKILL.md`。

**触发词:** "公众号排版"、"长文排版"、"wechat.html"、"排版"、"typeset"

**核心流程(第0步 + 5步):**
0. 运行参数(文章路径/品牌配置)+ 读目的仓库排版规范
→ ① 标点全角化(`punct_normalize.py`)→ ② 基准段先行(刊头条+H1+一个章节,确认风格)→ ③ 生成完整 wechat.html → ④ 自检 → ⑤ 预览+提醒粘草稿实测

**关键规则:**
- **全 inline 样式**:公众号粘贴只保留 inline style,`<style>` 块和 class 会被丢掉;所以产出全部 inline 样式
- 容器块用 `<section>` 不用 `<div>`(公众号对 div 的 inline style 支持差,粘贴常整个丢);要边框感用 `background` 代替 `border` 四边简写(单边 `border-left` 通常保留)
- 正文从 article.md **复制不手敲**(手敲易混入错字);只排版,不改原文文字
- 标点全角只改正文,**保护** frontmatter 键 / markdown 语法 / URL / CSS(脚本遮罩法)
- 三档强调克制(加粗主色为主 / 反色给 2-3 个核心差异点 / 胶囊给产品名首次),标差异点不标重复词
- 基准段先行(同 text-to-card / gzh-illustration 教训),不一口气全量生成
- 反色块 / 胶囊上线前**务必粘草稿实测**(`background` 在公众号偶尔有兼容细节)
- 图片不跟随粘贴(公众号不吃本地路径,手动上传)

### remotion-video

用 Remotion(React 写视频)创作可程序化渲染的视频,遵循 `skills/remotion-video/SKILL.md` 工作流。

**触发词:** "Remotion"、"做视频"、"视频创作"、"视频代码"、"分镜"

**核心流程(第0步 + 7步):**
0. 运行参数(PROJECT_DIR/OUTPUT_DIR/视频规格/素材来源)
→ ① 需求确认 → ② 前置检查(14 项清单,不得跳过)→ ③ 分镜拆解(逐场景审)→ ④ 资产清单 → ⑤ 代码生成(Video.tsx/scenes/components/constants)→ ⑥ 自检 → ⑦ 交付

**关键规则:**
- **Node 生态**:用 npx/npm,不用 uv;预览 `npx remotion studio`,渲染 `npx remotion render`
- 所有时间描述转换为帧数;动画优先 `spring()`/`interpolate()`
- 基准场景先行:第 1 个场景渲染小样确认风格后再批量(同 text-to-card 基准卡原则)
- 先低清小样(720p)确认节奏,再出正片
- 素材先从 video-asset-library 库里取,别从零造;项目结束回收可复用素材入库
- 前置检查清单与快速决策卡见 `references/checklist.md`

### video-asset-library

视频制作素材库的建库/入库/盘点/维护,遵循 `skills/video-asset-library/SKILL.md` 工作流。

**触发词:** "素材库"、"视频素材"、"素材入库"、"素材管理"

**核心流程(第0步 + 7步):**
0. LIBRARY_ROOT(素材库根目录,问用户)
→ ① 需求分析 → ② 库结构设计 → ③ 现有资产盘点 → ④ 缺失资产识别 → ⑤ 入库(重命名+metadata.yaml+缩略图)→ ⑥ 索引与橱窗重建 → ⑦ 使用指南输出

**关键规则:**
- **素材本体 + 元信息 + 生成物不进 git**(库目录、`*.metadata.yaml`、`gallery.html` 已 gitignore);git 里只有规范和查看器代码
- skill 是唯一写入方;web 橱窗只读
- 单一数据源 = 文件系统目录 + 每件素材旁的 metadata.yaml;索引/橱窗可随时重建
- 分类体系/元数据 schema/命名规范见 `references/library-spec.md`,不自造分类
- 查看器:`tools/asset-library-web/`,`uv run build_gallery.py <LIBRARY_ROOT>` 生成 gallery.html(数据内联,file:// 直接打开,不起 server)
