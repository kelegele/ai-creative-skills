# Agentic Engineering 知识摘要

来源：@jeremyphoward "Every Agentic Engineering Hack I Know (June 2026)"
原文：https://x.com/i/status/2061877533885473181
阅读量：913K

## 核心原则

1. **Plan First** — 永远先出 plan.md，不直接动手。计划迫使 Agent 研究、承诺方案、写验收标准
2. **Make the plan, trust the plan, don't read the plan** — 计划是给 Agent 的，人类只扫标题
3. **Plan for the plan** — 深度非代码任务，先计划如何计划，再执行
4. **Voice-to-LLM** — 语音输入 + LLM 理解力 = 快。AI 能补全模糊语音
5. **并行多会话** — 4-6 tab 同时跑，一个计划一个执行一个修 bug
6. **YOLO 模式** — 跳过权限确认，信任 Agent + Git 兜底
7. **Research → Plan → Build** — 做决定前先调研（last30days/搜索），不靠过时数据
8. **Raw context > 摘要** — 给 Agent 原始材料，不要人工先总结
9. **重复 2 次 → Skill** — 工作流固化，复利加速
10. **Be the taste** — 人类提供品味/方向/判断，Agent 提供执行力
11. **视频也能 Agent 做** — HyperFrame 把视频当 HTML 写
12. **真实生活 Agent 化** — CLI 跑腿：Tesla、Instacart、航班比价
13. **注意平衡** — Agent 上瘾是真的，别消失在构建中

## 工具栈

- Claude Code + Compound Engineering plugin（/ce-plan, /ce-work, /ce-brainstorm）
- Codex（并行引擎，reasoning xhigh + fast mode）
- last30days（调研：Reddit/X/YouTube/HN/GitHub 并行搜索，26K⭐）
- Playwright / agent-browser（浏览器自动化）
- HyperFrame（视频=HTML→MP4）
- Granola + Printing Press CLI（会议转录→结构化数据）
- Proof（plan.md 分享给非终端用户审阅）
- AgentMail（给 Agent 一个邮箱地址）
- Monologue / Wispr Flow（语音输入）
- cmux / Ghostty（终端多路复用）

## 对 Hermes Agent 的适配

已固化为 `dev-workflow` skill（Plan→Work→React），核心原则：
- 先出方案等用户确认再执行
- 调研先行
- 原始素材直接给 Agent
- 重复工作流固化成 Skill
- 人类做品味担当
