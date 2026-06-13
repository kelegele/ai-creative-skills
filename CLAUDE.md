# AI Creative Toolkit

## Project Structure

```
skills/text-to-card/    # 文章转图文卡片 skill
tools/                  # 独立工具/脚本
assets/                 # 共用素材/模板
```

## Skills

### text-to-card

当需要做图文卡片时，严格遵循 `skills/text-to-card/SKILL.md` 中的完整工作流。

**触发词：** "图文卡片"、"文章转卡片"、"做卡片"、"小红书卡片"

**核心流程：**
1. 接收文章 → 2. 生成大纲（封面+内容+结尾） → 3. 分页+选尺寸 → 4. AI生成HTML → 5. 预览确认 → 6. 修改/确认 → 7. 截图PNG输出

**关键规则（必读）：**
- 先读 SKILL.md 再动手，里面有大量实战教训
- delegate_task 批量生成HTML时必须附带基准卡源码，否则风格不一致
- 内容卡文字精简大字换行，不要长段落
- 封面/结尾页用 absolute 定位铺满画布，不复用内容卡 flex 布局
- card-number 必须用衬线体（Playfair Display），不用等宽体
- 章节标签（WHY/WHAT/TOOLS/HOW）边缘标注，不占独立页
- 输出到 `output/YYYYMMDD-主题/`，绝对不要放 /tmp
- 用户说"确认/归档/覆盖"→ 直接执行，不要反问
- 用户说"？"或纠正 → 先理解意图再回应，不要跳到执行

**设计系统：** 参考 `skills/text-to-card/references/agentic-design.md`

**截图工具：** `skills/text-to-card/scripts/screenshot.py`（依赖 Playwright + Chromium）

**输出目录：** `output/YYYYMMDD-主题/`
- HTML源文件：`card_01.html` ~ `card_XX.html`
- PNG截图：`preview/01.png` ~ `XX.png`
- 废弃项目：`output/archive/`
