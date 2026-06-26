# AI Creative Toolkit

通用 AI 内容创作工具集,含 skill、工具脚本、共用素材。适配任意 agent 环境。

## Project Structure

```
skills/text-to-card/    # 文章转图文卡片 skill(通用版)
skills/harvest-topics/  # 素材转选题候选 skill(通用版)
skills/submit-to-inbox/ # 素材提交(带降级) skill(通用版)
tools/                  # 独立工具/脚本
assets/                 # 共用素材/模板
```

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
