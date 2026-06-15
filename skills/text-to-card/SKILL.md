---
name: text-to-card
description: Use when turning articles/blog posts into social image card sets (封面+内容卡+结尾) for 小红书/微信/微博. Triggers include 图文卡片, 文章转卡片, 做卡片, 小红书卡片, card generation, article to cards.
version: 0.9.1
author: Kelegele
license: MIT
metadata:
  tags: [content, social-media, xiaohongshu, wechat, html, screenshot, design-system]
---

# Text-to-Card 文章转图文卡片

将文章/博客转为图文卡片。AI 按**设计模板**直接生成完整 HTML(内联样式),Playwright 截图 PNG。适配任意 agent 环境。

## 第0步:运行参数 + 设计模板(开工前必做)

### 0a 运行参数(问用户,存运行变量,无固定默认)
开始前问用户,回答存为本次运行变量,全程引用:
- **OUTPUT_DIR** — "这次输出到哪个目录?"(必问,如 `Content/20260613-xxx/`)
- **HTML_PATTERN** — "HTML 文件名格式?(建议 `card-{NN}.html`)"
- **PNG_SUBDIR** — "PNG 放哪个子目录?(建议 `preview/`)"

占位符:`{NN}` 两位序号、`{YYYYMMDD}`、`{slug}`。"建议"仅作提示,以用户回答为准。PNG 跟随 HTML 同名 stem,`screenshot.py --output` 指向 `OUTPUT_DIR/PNG_SUBDIR`。

### 0b 设计模板(动态获取/复用/自定义)
模板 = 一份 **DESIGN.md** 格式设计系统(配色/字体/组件/布局/反模式/agent 指南),第④步生成时作设计上下文。

1. 读 `templates/.current`(记录上次用的模板名)
2. 问用户:**用 `<当前>` / 换一个 / 自定义?**
3. **换一个** → 从 GitHub `nexu-io/open-design` 的 `plugins/_official/design-systems/` 列出(~150 系统:agentic/apple/claude/stripe/xiaohongshu…)。读候选 `open-design.json` 的 title + 中文 description 帮选 → 用户选 → 读该系统 `DESIGN.md` → 存 `templates/<name>.md` → 更新 `.current`
4. **自定义** → 按 `references/design-md-spec.md` 规范引导写,存调用方项目 `.text-to-card/templates/<name>.md`
5. 选定 → 存运行变量 **DESIGN_TEMPLATE**

查找优先级:项目 `.text-to-card/templates/` → skill `templates/`。fallback:网络不可达 → 用 `templates/` 现有(至少 `agentic` 内置默认)。

## 架构

```
用户文章 → AI 生成大纲 → 用户确认
    → AI 逐张生成完整 HTML(注入 DESIGN_TEMPLATE)
    → Playwright 截图 PNG → 用户预览 → 修改 → 确认 → 输出到 OUTPUT_DIR
```

## 工作流(第0步 + 7步,每步用户确认)

`0 参数+模板 → ① 接收文章 → ② 大纲 → ③ 分页+尺寸+平台 → ④ 生成HTML(基准卡先行) → ⑤ 预览 → ⑥ 修改/确认 → ⑦ 定版+截图`

### 第1步 接收文章
用户提供文章文本(纯文本/Markdown)或 URL(agent 抓取)。

### 第2步 生成大纲(封面+内容+结尾)
- AI 提取结构:标题/小标题/论点/金句
- **封面页**:标题 + 引子
- **内容页**:标题 + 精简要点(3-5句,每句独立一行) + 💡实战场景句
- **结尾页**:收尾金句 + 来源标注
- 编号大纲展示,用户调整后确认

**⚠️ 内容卡文字精简,不要长段落。** 每张 3-5 句,每句独立一行,正文 42-48px,行高 1.6-1.8。详细内容留给配文,卡片只"说清楚"。让用户审阅精选,不要塞满。

**⚠️ 保留原文粒度,不擅自合并。** 有 N 条就拆 N 张,合并/精简由用户决定。(曾被驳回:25 条被合并成 13 条。)

**⚠️ 引子=标题**,短、直击痛点、大白话。❌"配色选了又改…"(长) ✅"小白也能用AI出设计稿"。区分推荐 vs 原创。作者信息必须核实不编造。标题用中文。

**⚠️ 选题/目标受众/工具范围对齐。** 用户指定就遵循,不自行发挥。目标受众没说就先问。工具范围先问再列(别漏用户常用工具,别硬塞专业工具)。

**⚠️ 大纲不自作主张。** 用户给选题标题就按标题理解,不加限定/人群/技术栈。太杂(>15)让用户自己挑。

#### 内容页结构(每张3层)
1. **标题**:精炼要点(如"永远先写计划")
2. **要点**:3-5句精简,每句独立一行(非长段)
3. **💡实战场景句**:具体可操作的日常动作(20-40字,"让Agent做X",非抽象建议)。HTML 用 💡 前缀 + 浅色背景框。

### 第3步 分页 + 尺寸 + 平台
完整卡片 = 封面 + N 张正文 + 结尾页。每张正文 = 大纲一条,50-150字。用户可合并/拆分。

**平台张数上限(提前确认):** 小红书 18 / 朋友圈 9 / 公众号 不限 / 微博 18。超上限 → **合并非删减**(短/相近两条合一,各保留标题+正文+💡)。

**尺寸预置:** xiaohongshu-v(1080×1440 小红书竖)/ xiaohongshu-s(1080×1080 方)/ wechat-cover(900×383 公众号封面)/ wechat-moments(1080×1080 朋友圈)。

### 第4步 生成 HTML(基准卡先行)
核心:AI 直接写完整 HTML(内联样式),不依赖外部 CSS。加载 DESIGN_TEMPLATE 作设计上下文。

**⚠️ 先生成基准卡(card-01封面 + card-02 第一张内容),用户确认 HTML 风格后再批量。**

每张:加载 DESIGN_TEMPLATE → 按其色板/字体/排版生成 → 独立 .html,viewport 对应尺寸 → 命名按 HTML_PATTERN。
HTML 要求:完整 `<!DOCTYPE html>`、Google Fonts(含 Noto Serif SC 中文)、样式内联 `<style>`、viewport 固定 `overflow:hidden`、中文优先排版。

**⚠️ 字体字重一致性(防低级错误):** 每个 `font-family` 用到的字体 + 每个 `font-weight` 字重,**都必须在 Google Fonts `<link>` 里加载**。漏加载 → fallback 系统字体 / 浏览器合成 fake bold(笔画失真,数字尤其明显,曾出现 card-number 09 看着像不同字体)。写完所有卡跑 `check_fonts.py` 校验(第7步)。

### 第5步 预览(用户确认 HTML 后再截图)
**⚠️ 不要在用户确认 HTML 前生成截图!**
通用方式:`screenshot.py` 截图基准卡 2-3 张抽样 → 发用户确认风格。(IM 对话型 agent 环境的文件服务器预览见 `references/im-agent-env.md`)
❌ 一口气全生成+截图才给看 ✅ 生成→抽样截图→用户确认→再批量

**⚠️ 截图字体必须等加载(card-number 衬线体易 fallback):** `screenshot.py` 已在截图前 `page.evaluate("document.fonts.ready")` + 300ms 缓冲,确保 Google Fonts 加载完再截。若 card-number 等衬线字体仍不一致(某些卡 fallback 到系统 serif)→ 网络不稳,**终极方案本地化字体**(`@font-face` 引本地文件,不依赖远程 CDN)。注意:`check_fonts.py` 只查 `<link>` 声明、查不到实际加载 —— **它通过 ≠ 截图字体对**。教训:card-number 字体不一致 → 先查截图字体加载时机,**别改 CSS**(CSS 一致却渲染不同 = 截图问题)。

### 第6步 修改/确认
用户审阅可要求修改 = 重写该张 HTML → 重截图 → 再预览。用户说"OK/确认"才进下一步。

### 第7步 定版+截图
用户确认后,最终 HTML + PNG 存到 OUTPUT_DIR。HTML 按 HTML_PATTERN,PNG 放 PNG_SUBDIR(跟随 stem)。**定版立即保存,不等不拖。** 版本管理用新目录避免覆盖。

**⚠️ 定版前必跑字体校验:** `uv run python scripts/check_fonts.py <OUTPUT_DIR>`,**0 报警才定版**。它自动抓两类低级错误(人眼 review 必漏):① font-family 用了某字体但 `<link>` 没加载;② font-weight 用了某字重但该字重没加载。有报警 → 修 `<link>` 的 `wght@` 补字重,或改 CSS `font-weight` 用已加载的 → 重截图 → 再校验到 0。

## 卡片设计系统(布局规则)
配色/字体由 DESIGN_TEMPLATE 决定。布局规则通用:

- **封面页**:充分利用画布,像杂志封面饱满。装饰 3-4 个(大号半透明背景字+角标+底部色条+几何)。⚠️ **封面不能复用内容卡 `.card` flex 布局**(内容卡有 card-number 占位,封面没有 → flex 子元素被推中间)。用独立 CSS 类,`position:absolute` 铺满。内容从上展开:badge→title→accent-line→subtitle。
- **内容卡(单点)**:大号 card-number(**衬线体!**)、标题、accent-line、正文(精简大字)、💡框。⚠️ **card-number 必须衬线体(Playfair Display/Georgia/serif),不用等宽体(JetBrains Mono)**——font-family 是 monospace 一定错。序号大小全卡一致(grep `font-size` 对比 `.card-number`,不用 vision 判字号)。
- **合并卡(两条合一)**:上下两栏各~50%,色条/细线分隔,各标题+正文+💡,字号比单点略小(标题 64-72 vs 88-96,正文 28-32 vs 36-40)。prompt 标 `MERGED — TWO POINTS` + upper/lower split。
- **结尾页**:居中金句+attribution+来源,半透明引号装饰。
- **章节标签(WHY/WHAT/TOOLS/HOW)**:英文大写,边缘标注(编号下/右上角)14px。❌ 不放标题文本里 ❌ 不单独成页。分组由用户决定,不计入总张数。
- **配色**:严格遵循 DESIGN_TEMPLATE。❌ 把 Text 色当背景 ❌ 设计系统无的深色底。先读 DESIGN.md,不确定用 Surface 色。
- **中文字体必须引入**(Google Fonts 加 Noto Serif SC 700/900),否则 fallback 系统字体风格不统一。
- **DESIGN.md 是 AI 上下文,不是 CSS**。AI 按它写内联 `<style>`,不需外部 CSS。

## ⚠️ 协作纪律(通用化提炼)

### delegate_task 批量生成必须附基准卡源码
问题:delegate_task 让子 agent 各写 HTML,理解差异 → 字体/间距/装饰不一致。
✅ 先确认基准卡(card-02)风格 → 后续每批 prompt **附基准卡完整 HTML 源码** + `CRITICAL: strictly match the reference template, copy CSS verbatim, only change text`。AI 仍负责设计决策,基准卡是一致性锚点。
❌ 只描述规范不附源码 → 子 agent 自由发挥 ❌ Python 模板填变量 → 死板(用户拒绝,已删除)

### 用户说"确认/归档/覆盖/删/移" → 直接执行,不反问
用户的"确认"是确认他自己的指令,不是问你。**先执行再汇报。**
❌ "确认执行吗?" ✅ 立刻 mv/cp → "已归档到X"
但:用户只指出问题没要求重做时,**先问"要重做吗?"再动手**(别多此一举重新生成)。

### 找文件/多版本不过度分析
快速列候选,不启动 vision/HTML 解析多轮对比。用户说"这版不是最新"→ 直接问哪个是定版,别翻遍目录。

### 定版立即保存
用户说"OK/定版"→ 立刻存最终版到 OUTPUT_DIR。不等不拖(教训:确认版未持久化,下次会话丢失)。

## 小红书配文写作
卡片做完后通常需要发布文案。

**风格由用户人设决定**(不同人设口径不同)。写前先确认/读用户人设文档。
- **反 AI 腔**(通用):禁"在当今 AI 时代""让我们一起""助力""赋能""你值得拥有"等套话;靠**具体信息和判断**,不要正确废话。
- **去 AI 味 ≠ 加低俗口语**(教训):别为"去 AI 味"堆网感词(破防/那个味儿/一眼假/那一坨)或砍序号工整——专业人设的序号是结构感,不是 AI 味。真正的去 AI 味靠信息密度。
- **本项目(飞栗)人设**:冷静的陈述者——客观平和、有对话感、用客观事实制造焦虑、给利他操作路径;保留序号工整。详见调用方项目 `AGENTS.md`「文案口吻(飞栗人设)」。

**结构:** 标题(痛点/好奇,小红书≤20字)→ 引入 → 编号要点(01/02/03)→ 展开 → 操作指引 → 话题标签 5-8 个。配文存 `Content/<组>/copy.md`,**顶部放纯文本可直接复制版**(无 markdown 格式),说明/口径放底部 `═══` 分隔。配文交给用户定稿。

## 依赖 & 截图
- Playwright + Chromium、Python 3.11+
- `python scripts/screenshot.py --files card-01.html card-02.html ... --output <OUTPUT_DIR/PNG_SUBDIR>`
- `uv run python scripts/check_fonts.py <OUTPUT_DIR>` — **定版前字体字重一致性校验**(防 link 漏加载字体/字重,Windows 加 `PYTHONUTF8=1`)

## 文件命名
- HTML:`HTML_PATTERN`(用户确定,默认建议 `card-{NN}.html`),**ASCII**(中文文件名致 http.server 404)
- PNG:跟随 HTML stem,放 `PNG_SUBDIR`
- 中文只在目录名/zip 名

## skill 自身结构
```
text-to-card/
├── SKILL.md
├── templates/              # 设计模板(DESIGN.md)+ .current 指针
│   ├── agentic.md          # 内置默认
│   └── .current
├── references/
│   ├── design-md-spec.md   # DESIGN.md 规范(自定义引导)
│   └── im-agent-env.md     # IM 对话型 agent 环境适配
├── examples/               # 示例(非主流程)
│   ├── reference-card-single.html  # 基准卡示例(delegate_task 锚点)
│   └── matt-van-horn-25-tips.md    # 首次实战的25条完整内容
└── scripts/
    ├── screenshot.py       # Playwright 截图
    └── check_fonts.py      # 字体字重一致性校验(定版前必跑)
```

> 📎 **IM 对话型 agent 环境**(Hermes/OpenClaw/QwenPaw 等)的文件服务器预览、IM 发图、image_cache 取图、成品路径等见 `references/im-agent-env.md`
