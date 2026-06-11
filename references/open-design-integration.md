# Open Design 集成指南

## 仓库

https://github.com/nexu-io/open-design/tree/main/plugins/_official/design-systems

每个设计系统 = 一个目录，含 `DESIGN.md`（完整规范）+ `open-design.json`（元数据）。

## 已采纳：Agentic

- 目录：`agentic/`
- 主色 `#FF5701`，背景 `#FFFFFF`，文字 `#111827`
- 字体：Playfair Display + Inter + JetBrains Mono
- 规范文件：`references/agentic-design.md`（AI 生成 HTML 时注入此文件作为上下文）

## 如何添加新设计系统

1. 从仓库读目标目录的 `DESIGN.md`（通过 `mcp_zread_read_file`）
2. 提取核心规范：色板、字体族、字号层级、圆角、阴影策略
3. 创建 `references/<name>-design.md`，精简写入色板+字体+排版规范
4. 更新 SKILL.md 第4步，将新设计系统规范文件加入 AI 生成时的上下文
5. 商业字体设 fallback 链（如 Playfair→Noto Serif SC→Georgia）
6. 用 AI 生成测试 HTML + `scripts/screenshot.py` 验证
7. 发预览给用户确认

## 热门候选系统（适合小红书卡片）

| 系统 | 调性 | 适合场景 |
|---|---|---|
| xiaohongshu | 品牌红，圆角，内容优先 | 平台原生感 |
| theverge | 暗底，薄荷+紫外线，粗体 | 科技抓眼 |
| vercel | 黑白极简，Geist，shadow-as-border | 开发者美学 |
| wired | 纸白杂志，衬线标题，零圆角 | 权威编辑感 |
| warm-editorial | 赤陶色，暖纸白，衬线 | 长文舒适 |
| stripe | 紫色渐变，轻量优雅 | 高级感 |

## 设计系统 DESIGN.md 核心结构

每个 DESIGN.md 包含9节：
1. Visual Theme & Atmosphere
2. Color Palette & Roles
3. Typography Rules
4. Component Stylings
5. Layout Principles
6. Depth & Elevation
7. Do's and Don'ts
8. Responsive Behavior
9. Agent Prompt Guide（可直接用于生成 prompt）
