---
name: submit-to-inbox
description: Use when submitting a collected material (link/text/image) to a target repo's Topics/inbox. Resilient — gh cli → GitHub API → local fallback, never loses material. Works without cloning the repo. Triggers include 提交素材, 存到inbox, 这个存一下, submit to inbox.
version: 0.1.0
author: Kelegele
license: MIT
metadata:
  tags: [content, topics, inbox, github, hermes, collection]
---

# Submit-to-Inbox 素材提交(带降级,素材绝不丢)

把一条素材(链接 / 文字 / 图片)安全提交到**目的仓库**的 `Topics/inbox/`。**不依赖本地是否 clone 了主仓**——优先 gh cli,其次 GitHub API,都不行本地兜底。

给任何能调 skill 的收集端用:Hermes / OpenClaw / Codex / Claude Code 等,在各场景(IM / CLI / 手动)收集素材时调用。

## 触发
"提交素材""存到 inbox""这个存一下""/submit-to-inbox"

## 配置(运行变量,**目的仓库不默认任何人的**)
- **目的仓库** `TARGET_REPO`(格式 `owner/repo`):**必须明确,不写死默认**——这是开源通用 skill,绝不能把别人的素材投到作者仓库。来源优先级:
  1. 环境变量 `INBOX_REPO`(如 `yourname/your-content-repo`)
  2. 本地 git remote 推断(在某个 git 仓库内运行 → 取其 GitHub origin)
  3. 都没有 → **问用户**:"目的仓库?(owner/repo)"
- **认证**(按优先级):
  1. **gh cli**——用户 `gh auth login` 过即可,skill 不碰 token。最省事。
  2. **GitHub token**——环境变量 `GH_TOKEN` / `GITHUB_TOKEN`(fine-grained PAT,Contents 读写)。

## 工作流

### ① 整理素材成 inbox 格式
按目的仓库 `Topics/inbox/README.md` 规范(远程读,或 skill 自带摘要):
- 文件名:`YYYYMMDD-HHmm-<slug>.md`
- frontmatter:`time` / `type`(link | text | image) / `source`
- 正文:分析 / 原文摘录 / 图片说明

### ② 确定目的仓库 + 认证状态
- 读 `TARGET_REPO`(环境变量 `INBOX_REPO` / 本地 git remote);都没有 → 问用户。**不默认任何固定仓库。**
- 检测认证:`gh auth status` 成功 → gh 模式;否则查 `GH_TOKEN` / `GITHUB_TOKEN` → API 模式;都没有 → 走 ④ 引导。

### ③ 提交(按优先级降级,失败就下一档)
1. **gh cli**(优先):
   `gh api -X PUT repos/<OWNER>/<REPO>/contents/Topics/inbox/<file> -f message="inbox: <slug>" -f content="<base64>"`
   gh 已认证,直接成。
2. **gh 不可用 → GitHub API**:用 token 调 Contents API PUT(同上,带 `Authorization: Bearer <token>`)。
3. **都失败(没认证 / 断网 / 限流)→ 本地兜底(⑤)**。

### ④ 认证引导(没 gh 没 token 时)
给用户两条路任选:
- **推荐 gh cli**:装 GitHub CLI → `gh auth login`(浏览器认证一次,以后自动,最省事)。
- **PAT**:GitHub Settings → Developer settings → Fine-grained PAT → 选 `<OWNER>/<REPO>` → `Contents: Read and write` → 设环境变量 `GH_TOKEN`。
配好重跑。

### ⑤ 本地兜底(连不上远程时,素材绝不丢)
- 存 Markdown 到 **skill 目录下 `inbox-fallback/`**:`<skill-dir>/inbox-fallback/YYYYMMDD-HHmm-<slug>.md`
- frontmatter 加 `status: pending-sync`、`target_repo: <repo>`
- **下次 skill 跑,先扫 `inbox-fallback/`,远程通了自动补提(③),补提成功 → 移到 `inbox-fallback/submitted/`**

### ⑥ 汇报
- 成功:"已提交 → `<repo>/Topics/inbox/<file>`"
- 兜底:"连不上远程,已本地存 `inbox-fallback/<file>`(待同步)。建议 `gh auth login` 后重跑,自动补提。"

## ⚠️ 纪律
- **素材绝不丢**:提交失败必兜底,绝不静默丢弃。
- **gh 优先**:别一上来要 token,先 `gh auth status`。
- **不假设本地有主仓**:可能只在 IM agent 里跑,本地没 clone 任何仓库。
- `inbox-fallback/` 进 `.gitignore`(开源 skill 不提交用户私有兜底数据)。

## 依赖
- gh cli(可选,优先)或 GitHub token
- 抓链接内容:`/browse` skill 或 WebFetch
- 图片:多模态(Claude 原生)

## 结构
```
submit-to-inbox/
├── SKILL.md
├── .gitignore            # 忽略 inbox-fallback/ 内容
└── inbox-fallback/       # 本地兜底(只留 .gitkeep)
    └── .gitkeep
```
