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
skills/oral-script/       # 口播稿创作与调稿 skill(通用版)
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

## 仓库维护约定

- 各 skill 的详细工作流与实战教训以 `skills/<name>/SKILL.md` 为准(内含大量踩坑记录,**动工前必读**),本文件只留索引
- 增删 skill 必须同步本文件与 README 的结构树和 Skills 章节(含触发词)
- skill 必须自包含:不引用其他 skill 的文件(经 `npx skills add` 是独立安装的)
- 改规范/修脚本坑时,同步全仓所有副本(引用该规范的 references/示例/模板、姊妹脚本)——副本间不会自动同步
- `examples/` 只放自产内容,不收第三方内容的全文翻译/摘编(MIT 再分发有版权风险)

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
| `skills/gzh-illustration/scripts/replace_placeholders.py` | 占位 → 图片回填(草稿/定版两态,自供图缺失报警不回填) |
| `skills/{text-to-card,gzh-illustration}/scripts/screenshot.py` | Playwright + Chromium 截图;`gzh-illustration` 有自己的 `pyproject.toml` / `uv.lock`(playwright 依赖,`uv sync` 装) |

## Skills 索引

| Skill | 用途 | 触发词 |
|-------|------|--------|
| text-to-card | 文章转图文卡片(小红书/公众号),大纲→HTML→截图 | 图文卡片、文章转卡片、做卡片、小红书卡片 |
| harvest-topics | inbox 素材加工成 backlog 选题候选(场景驱动,只追加) | 加工inbox、收获选题、处理素材、素材转选题 |
| submit-to-inbox | 素材提交到 Topics/inbox(gh→API→本地三级降级,素材绝不丢) | 提交素材、存到inbox、这个存一下 |
| gzh-longform | 公众号长文(两阶段:研究→写作,中间硬闸门) | 公众号长文、公众号文章、写长文、深度图文 |
| gzh-typeset | article.md → 全 inline 样式的 wechat.html(粘贴公众号) | 公众号排版、长文排版、wechat.html、排版、typeset |
| gzh-illustration | 长文配图(占位→HTML→Playwright 截图→回填,草稿/定版两态) | 公众号配图、文章配图、封面图、配图生成 |
| oral-script | 口播稿(播客/视频)创作与逐轮调稿,带节奏标注 | 口播稿、播客稿、逐字稿、生成口播、口播文案、调口播 |
| video-asset-library | 视频素材库建库/入库/盘点/维护(素材本体不进 git) | 素材库、视频素材、素材入库、素材管理 |
