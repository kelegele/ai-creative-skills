---
name: gzh-illustration
description: 公众号长文配图。读 article.md 占位 → HTML 设计 → Playwright 截图 → 回填(草稿/定版两态)。当用户给公众号长文配图、做封面、生成正文插图时使用。触发词:公众号配图、文章配图、封面图、配图生成。
version: 0.1.0
author: Kelegele
license: MIT
metadata:
  tags: [content, wechat, gongzhonghao, illustration, image, html, screenshot]
---

# gzh-illustration 公众号配图

公众号长文配图 skill。读 `article.md` 占位(或当场接描述)→ 按 agentic 设计系统自由设计 HTML → Playwright 截图 PNG → 回填到文章。不调 text-to-card,自带截图脚本。

## 工作流

**第 0 步 运行参数 + 读设计系统**

问用户:
- **目标文章路径**(如 `Content/20260626-xxx/article.md`)
- **设计预设**(默认 agentic,详见 `references/design-system.md`)
- **输入方式**(读占位 / 当场给)

读 `references/design-system.md` 取当前预设 token。

**第 1 步 解析配图清单**

- **读占位**:扫 `article.md` 的 `🖼️` 占位块,解析成清单(序号/尺寸/来源/描述)。格式见 `references/placeholder-format.md`。
- **当场给**:用户口述每张图,整理成等价清单。
- 无占位 → 停下问用户。

**第 2 步 基准图先行(风格确认)**

先只做 **封面 + 第一张正文配图**:
- 按描述 + agentic 设计系统,自由设计 HTML+内联 CSS,水印融入内容(见「品牌水印」节)
- HTML 存 `images/html/gzh-imaget-{N}.html`,截图存 `images/gzh-imaget-{N}.png`
- 截图命令:`uv run python scripts/screenshot.py <html> <png> --width <尺寸宽>`
- 尺寸规范见 `references/size-spec.md`

截图给用户审。确认 → 进第 3 步;不确认 → 改基准图重审(不进批量)。

**第 3 步 批量出其余配图**

- 按基准图风格,逐张设计 HTML + 截图,逐张给用户审
- 自供图占位跳过生成(用户已提供)

**第 4 步 回填(草稿态)**

```bash
uv run python scripts/replace_placeholders.py <article.md> --mode draft
```
生成/自供图均在占位块下方插入 `![描述](path)`,**保留占位描述块**。草稿态便于改图对账。

**第 5 步 定版**

用户确认所有图后:

```bash
uv run python scripts/replace_placeholders.py <article.md> --mode final
```
删除所有 `🖼️` 占位块,只留图片。运行前自动备份 `article.md.bak`。

## 占位格式

```
> 🖼️ 【配图N · 尺寸 · 来源】描述
```

详见 `references/placeholder-format.md`。来源可缺省,默认 `生成`。

## 草稿/定版分态

- **草稿态**:占位描述 + 图片并存,可反复改图重截图、重跑 draft 更新
- **定版态**:清掉占位描述,只留图片,可发文
- 两态由 `replace_placeholders.py --mode` 切换

## 品牌水印

每张配图都要加品牌水印,规范:

- **融入内容,不怼角标** —— 水印作为内容的一部分(标题副标 / 图注署名 / 卡片署名位等),不要固定右下角角标(会和主内容重叠、视觉割裂)。
- **位置由大模型判断** —— 每张图根据自身布局选合适的融入位(标题、图注、输出块、foot 等),不一刀切;基准图阶段就把水印位置定下来。
- **文本由项目传,skill 不写死** —— 品牌名(如「飞栗.ai」)是项目级决定,skill 保持通用;调用方知道品牌,设计 HTML 时写进对应位置。
- **样式** —— 弱色(`#9CA3AF` Subtitle)、不抢主视觉、作为署名/页脚的自然一部分。
- `screenshot.py --watermark <文本>` 是**角标注入**(右下角),仅用于快速/批量场景;**项目配图优先在 HTML 里融入水印,截图时不传 `--watermark`**。

设计 HTML 时把品牌水印作为内容元素写进合适位置(如标题副标末尾「· 飞栗.ai」、图注署名「— 飞栗.ai」、底部 foot 署名)。

## 依赖

skill 目录有独立 uv 环境(`pyproject.toml` 声明 playwright)。首次用:
```bash
cd skills/gzh-illustration
uv sync
uv run playwright install chromium
```

## 不做(YAGNI)

- 不调 text-to-card(自带截图脚本)
- 不自动衔接 gzh-longform(用户手动跑)
- 不做多预设实现(初版只 agentic,预留)
- 不做固定模板(自由设计)
- 不做推送(用户人工)

## 经验教训

- **基准图先行,不批量** —— 封面+1 张正文图定风格,确认后批量,避免全量返工(同 text-to-card 教训)。
- **截图前等字体** —— `document.fonts.ready` + 300ms,避免字体未加载截图导致风格错位。
- **草稿保留描述** —— 改图时能对账"这张图画的是什么",定版才清掉。
- **自供图路径校验** —— 自供图路径缺失要报警不回填,别静默生成错误图片。
- **水印融入内容,不角标** —— 品牌水印作为内容一部分(标题/图注/署名位),位置因图而异、由大模型判断;别固定右下角(`--watermark` 角标会和主内容重叠)。文本项目传(如 飞栗.ai),skill 不写死。
