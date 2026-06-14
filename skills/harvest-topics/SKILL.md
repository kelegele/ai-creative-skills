---
name: harvest-topics
description: Use when processing collected materials in Topics/inbox/ into topic candidates for Topics/backlog.md. Triggers include 加工inbox, 收获选题, 处理素材, 素材转选题, 清一下inbox, inbox to topics, harvest topics.
version: 0.1.0
author: Kelegele
license: MIT
metadata:
  tags: [content, topics, research, inbox, workflow]
---

# Harvest-Topics 素材转选题

把 `Topics/inbox/` 里各收集 Agent(Hermes / 其他)倒进来的素材,加工成 `Topics/backlog.md` 的选题候选。只管 **inbox → backlog** 这一段。

**inbox 是通用信箱,不绑定任何特定 agent。** 任何按 `Topics/inbox/README.md` 规范提交的素材,本 skill 都加工。素材怎么进 inbox(agent 端的事)、backlog 之后怎么创作(用 text-to-card),各管各的,互不耦合。

## 触发
"加工 inbox""收获选题""处理素材""清一下 inbox""/harvest-topics"

## ⚠️ 第0步:读目标人群规范(每次必做,不读就跑 = 跑偏)
先读**调用方项目** `AGENTS.md` 的「## 目标人群」章节——这是加工选题的**唯一判据**。
- 人群:非计算机领域、想用 AI 但不懂"能做什么""怎么用"的小白。
- 定位:专业工具 / 专业用法**降维给小白**,不是教消费级工具(豆包闲聊)。
- 选题必须**场景驱动**:从"小白真实工作 / 生活里的痛点"切入。

**画像不全(如"受众真实工作场景"还没写进 AGENTS.md)→ 停下,问用户补全再加工**,别拿不完整画像硬来——否则加工出来的选题照样不贴。

## 工作流(6 步)

### ① 扫描 inbox
读 `Topics/inbox/`,跳过 `processed/`、`README.md`。列出待加工素材(文件名 + time + type + 一句预览),告诉用户本次处理 N 条。

### ② 逐条解析(按 type)
- **link** → 用 `/browse` skill 抓内容(项目强制用 /browse,禁 mcp__claude-in-chrome),提取要点
- **text** → 直接读正文
- **image** → 多模态理解(`images/` 下的图)

提炼每条:讲什么 / 核心信息 / 可能的受众痛点。

### ③ 过目标人群筛
每条判断:能不能服务目标人群?
- **判据问法:"这条能解决受众哪个真实工作 / 生活痛点?"** 答得出 → 留;答不出 → 归档 `processed/rejected/` + 在文件里附一句原因。
- 参照第0步读的目标人群规范,**场景驱动**。

### ④ 加工成选题候选
过筛的素材,成一条选题,字段:
- **标题**:受众视角、痛点 / 好奇向,小红书 ≤20 字
- **痛点**:受众真实工作 / 生活里的具体场景(不是"这个工具很厉害")
- **专业工具 / 方法**:用什么专业工具 / 方法解决(符合"降维给小白")
- **方向**:提效 / 搞钱 / 创作 / 认知
- **能拆几张卡**:预估 8-16
- **来源**:inbox 文件名 + 原链接(可追溯)

### ⑤ 追加 backlog
加工好的选题**追加**到 `Topics/backlog.md`,格式对齐现有条目:
```
- [ ] YYYY-MM-DD — <标题>   # <方向> · 预估NN卡 · from inbox/<文件>
```
`[ ]` 未勾选(做不做由用户决定)。**只追加,不改已有条目。**

### ⑥ 归档 + 汇报
- 已加工的 inbox 文件 → 移到 `processed/`(保留原文,备追溯)
- 汇报:扫 N → 过筛 M → 出选题 M(列出标题)→ 没过筛 K(附原因)
- 提示:backlog 现有 X 个候选,挑一个开干(可用 text-to-card)

## ⚠️ 纪律

- **先读调用方 `AGENTS.md` 目标人群再动手。** 不读就加工 = 跑偏。
- **场景驱动,不是工具驱动。** 选题从受众**真实工作 / 生活痛点**切入,不是"我有个专业工具教你用"。工具是手段不是主角。曾出现工具驱动(拿 Cursor / Midjourney 等专业工具硬套)被否"不贴实际工作、没兴趣"的教训。
- **只追加 backlog,不改已有条目**——已有的都是用户决策过的。
- **画像不全就停下问用户**,别用半截画像硬加工。
- 用户说"加工 / 清 inbox"→ 直接跑完再汇报,不反问;跑完列结果让用户挑。

## 依赖
- 抓链接:`/browse` skill(项目强制)
- 文件操作:Read / Write / Edit / Bash
- 图片理解:多模态(Claude 原生)

## skill 自身结构
```
harvest-topics/
└── SKILL.md
```
轻量 skill。后续如需批量解析 / 去重 / 定时触发,再加 `scripts/`、`references/`。
