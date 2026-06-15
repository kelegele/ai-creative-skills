---
name: harvest-topics
description: Use when processing collected materials in Topics/inbox/ into topic candidates for Topics/backlog.md. Works with or without a local repo clone (local → gh cli → GitHub API). Triggers include 加工inbox, 收获选题, 处理素材, 素材转选题, 清一下inbox, harvest topics.
version: 0.2.0
author: Kelegele
license: MIT
metadata:
  tags: [content, topics, research, inbox, workflow]
---

# Harvest-Topics 素材转选题

把**目的仓库** `Topics/inbox/` 里各收集 Agent 倒进来的素材,加工成 `Topics/backlog.md` 选题候选。只管 **inbox → backlog** 这一段。

**不依赖本地是否 clone 了主仓**(开源通用):本地有 `Topics/` → 直接读写;没有 → 通过 gh cli / GitHub API 读写远程。给任何能调 skill 的 agent 用。

## 触发
"加工 inbox""收获选题""处理素材""清一下 inbox""/harvest-topics"

## 配置(运行变量)
- **目的仓库** `TARGET_REPO`(格式 `owner/repo`):**必须明确,不写死默认**——开源通用 skill,不绑作者仓库。来源:环境变量 `INBOX_REPO` / 本地 git remote 推断(本地有 `Topics/` 的仓库)/ 都没有则问用户。
- **访问模式**(自动检测):
  - 本地(当前目录或环境变量 `INBOX_ROOT` 指向的)有 `Topics/inbox/` → **本地模式**(直接读写)。
  - 没有 → **远程模式**:优先 gh cli(`gh auth status` OK),否则 GitHub API(`GH_TOKEN` / `GITHUB_TOKEN`)。
  - 远程也没认证 → 停下,引导用户 `gh auth login` 或配 token(同 submit-to-inbox ④)。

## ⚠️ 第0步:读目标人群规范(每次必做,不读就跑 = 跑偏)
读**目的仓库** `AGENTS.md` 的「## 目标人群」章节——加工选题的**唯一判据**。本地有就读本地,否则远程读(gh / api)。
- 画像不全(如"受众真实工作场景"没写)→ 停下问用户,别拿半截画像硬来。
- 选题必须**场景驱动**:从受众真实工作 / 生活痛点切入,不是"我有个专业工具教你用"。

## 工作流(6 步)

### ① 扫描 inbox
- 本地:读 `Topics/inbox/`(跳过 `processed/`、`README.md`)。
- 远程:`gh api repos/<OWNER>/<REPO>/contents/Topics/inbox` 列文件,逐个读。
列出待加工素材(N 条),告诉用户。

### ② 逐条解析(按 type)
- **link** → `/browse` skill 抓内容(项目强制)
- **text** → 直接读正文
- **image** → 多模态理解(`images/` 下的图)

提炼每条:讲什么 / 核心信息 / 受众痛点。

### ③ 过目标人群筛
每条判断:"这条能解决受众哪个真实工作 / 生活痛点?" 答得出 → 留;答不出 → 归档 `processed/rejected/` + 附原因。参照第0步规范,**场景驱动**。

### ④ 加工成选题候选
过筛的素材,成一条选题,字段:
- **标题**:受众视角、痛点 / 好奇向,小红书 ≤20 字
- **痛点**:受众真实工作 / 生活场景(不是"工具很厉害")
- **专业工具 / 方法**:用什么专业工具 / 方法解决
- **方向**:提效 / 搞钱 / 创作 / 认知
- **能拆几张卡**:预估 8-16
- **来源**:inbox 文件名 + 原链接

### ⑤ 追加 backlog
- 本地:追加到 `Topics/backlog.md`。
- 远程:读 backlog.md(取 SHA)→ `gh api -X PUT` 更新。
格式:`- [ ] YYYY-MM-DD — <标题>   # <方向> · 预估NN卡 · from inbox/<文件>`。`[ ]` 未勾。**只追加,不改已有条目。**

### ⑥ 归档 + 汇报
- 已加工素材移 `processed/`(本地 mv;远程 = 新路径 PUT + 旧路径 DELETE)。
- 汇报:扫 N → 过筛 M → 出选题 M(标题)→ 没过筛 K(原因)。
- 提示:backlog 现有 X 候选,挑一个开干(可用 text-to-card)。

## ⚠️ 纪律
- **先读 `AGENTS.md` 目标人群再动手。** 不读就加工 = 跑偏。
- **场景驱动,不是工具驱动。** 选题从受众真实工作 / 生活痛点切入,不是"拿专业工具教人"。工具是手段不是主角。曾出现工具驱动(Cursor / Midjourney 硬套)被否"不贴实际工作"的教训。
- **只追加 backlog,不改已有条目。**
- **画像不全就停下问用户**,别硬加工。
- 用户说"加工 / 清 inbox"→ 直接跑完汇报,不反问。

## 远程操作备忘(gh 优先)
- 列目录:`gh api repos/<OWNER>/<REPO>/contents/Topics/inbox`
- 读文件:`gh api repos/<OWNER>/<REPO>/contents/<path>`(返回含 base64 content)
- 写 / 改文件:`gh api -X PUT repos/<OWNER>/<REPO>/contents/<path> -f message="..." -f content="<base64>" -f sha="<现有文件 sha,改时必带>"`
- 移动文件:无直接 API,= 新路径 PUT + 旧路径 DELETE
- gh 不可用 → `curl` GitHub API + `Authorization: Bearer $GH_TOKEN`

## 依赖
- gh cli(优先)/ GitHub token(次)
- 抓链接:`/browse` skill(项目强制)
- 图片理解:多模态(Claude 原生)

## skill 自身结构
```
harvest-topics/
└── SKILL.md
```
轻量 skill。后续如需批量 / 去重 / 定时,再加 `scripts/`、`references/`。
