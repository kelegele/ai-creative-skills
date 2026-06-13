# DESIGN.md 规范(自定义设计模板指南)

设计模板是一份 **DESIGN.md**,描述一个设计系统(配色/字体/组件/布局/反模式)。第④步生成卡片时,AI 读它作设计上下文,按其规范写内联 HTML/CSS。

本规范用于引导你**自定义模板**。内置模板(`templates/agentic.md`)和 open-design 仓库的系统都符合此结构。

## 来源
- open-design 仓库:`nexu-io/open-design` 的 `plugins/_official/design-systems/<name>/DESIGN.md`(~150 个现成系统)
- 规范定义:[getdesign.md](https://getdesign.md)、open-design 的 plugin schema

## 推荐 章节 结构

一份完整的 DESIGN.md 建议包含以下章节(参照 open-design 的 DESIGN.md 实例,如 xiaohongshu):

1. **标题 + 分类 + 一句话定位** — 如"Xiaohongshu / Media & Consumer / 生活 UGC 社交,单一品牌红,大圆角,内容优先"
2. **Visual Theme & Atmosphere** — 整体气质、关键特征列表(品牌色、字体、圆角、阴影、留白原则)
3. **Color Palette & Roles** — 每个颜色的色值(token)+ 用途角色(主色/背景/文字/语义),含 dark mode(若有)
4. **Typography Rules** — 字体族(中文/拉丁/数字)、字号/字重/行高表、原则(如"三种字重以内""tracking 0""软黑非纯黑")
5. **Component Stylings** — 按钮(主/次/outline)、卡片、输入、tab、标签、badge、头像、弹层等,给色值+圆角+padding
6. **Layout Principles** — 间距系统(如 8pt grid)、响应式断点、栅格、留白
7. **Depth & Elevation** — 阴影层级(几级,各用于什么)
8. **Do's and Don'ts** — ✅ 该做 / ❌ 不该做(具体,如"不要把品牌色渐变""不要用 Inter 做中文展示字")
9. **Agent Prompt Guide**(关键) — 给 AI 的速查:Quick Color Reference、Quick Type Reference、Component One-Liners(可直接 copy 的 CSS 片段)、Iteration Guide

## 写作要点

- **色值用具体 hex/token**,不写"主色调红色"——写 `Brand Red: #FF2442`
- **Component One-Liners** 给可直接粘贴的 CSS(如 `background: #FF2442; color: #FFF; border-radius: 9999px;`),AI 生成时最依赖这部分
- **Do's/Don'ts 要具体到反模式**,如"不要用紫色/深蓝/黑金做主色——科技/金融/奢华词汇是错的调性"
- **Agent Prompt Guide 是给 AI 读的**,越精确(色值/字号/圆角数值)生成越准
- 它是 **AI 上下文,不是浏览器加载的 CSS**——AI 读后写内联 `<style>`

## 最小可用模板

如果只想快速自定义,至少写:标题定位 + Color(token+角色)+ Typography(字体+字号表)+ Component One-Liners(CSS 片段)+ 3-5 条 Don'ts。其余按需补。

## 示例参考

- `templates/agentic.md`(内置,简洁版)
- open-design 仓库的 `xiaohongshu/DESIGN.md`、`apple/DESIGN.md` 等(详尽版,9 节完整)
