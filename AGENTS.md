# AI Creative Toolkit

通用 AI 内容创作工具集,含 skill、工具脚本、共用素材。适配任意 agent 环境。

## Project Structure

```
skills/text-to-card/    # 文章转图文卡片 skill(通用版)
skills/harvest-topics/  # 素材转选题候选 skill(通用版)
tools/                  # 独立工具/脚本
assets/                 # 共用素材/模板
```

## Skills

### text-to-card

需要做图文卡片时,严格遵循 `skills/text-to-card/SKILL.md` 中的完整工作流。

**触发词:** "图文卡片"、"文章转卡片"、"做卡片"、"小红书卡片"

**核心流程(第0步 + 7步):**
0. 运行参数(OUTPUT_DIR / HTML_PATTERN / PNG_SUBDIR,问用户存运行变量)+ 设计模板(动态获取/复用/自定义)
→ ① 接收文章 → ② 大纲(封面+内容+结尾) → ③ 分页+尺寸+平台 → ④ 生成HTML(基准卡先行) → ⑤ 预览 → ⑥ 修改/确认 → ⑦ 定版+截图

**关键规则(必读):**
- 先读 SKILL.md 再动手,里面有大量实战教训
- **开工前第0步必做**:问用户确定输出目录/命名/设计模板,无固定默认
- delegate_task 批量生成 HTML 时必须附基准卡源码,否则风格不一致
- 内容卡文字精简大字换行,不要长段落
- 封面/结尾页用 absolute 定位铺满,不复用内容卡 flex
- card-number 必须衬线体(Playfair Display),不用等宽体
- 章节标签(WHY/WHAT/TOOLS/HOW)边缘标注,不占独立页
- 用户说"确认/归档/覆盖"→ 直接执行,不反问
- 用户说"?"或纠正 → 先理解意图再回应,不跳执行

**设计模板:** `skills/text-to-card/templates/`(DESIGN.md 格式,默认 `agentic.md`;可从 `nexu-io/open-design` 动态获取或自定义,详见 SKILL.md 第0b 步)

**截图工具:** `skills/text-to-card/scripts/screenshot.py`(Playwright + Chromium)

**IM 对话型 agent 环境**(Hermes/OpenClaw/QwenPaw)的预览/发图/取图/路径见 `skills/text-to-card/references/im-agent-env.md`

### harvest-topics

把调用方项目 `Topics/inbox/` 里各收集 Agent(Hermes 等)倒进来的素材,加工成 `Topics/backlog.md` 选题候选。inbox 是通用信箱,不绑特定 agent。

**触发词:** "加工inbox"、"收获选题"、"处理素材"、"素材转选题"

**核心流程(第0步 + 6步):** 读目标人群规范 → ① 扫inbox → ② 解析(link/text/image) → ③ 过目标人群筛 → ④ 加工选题(标题/痛点/工具/方向/卡数) → ⑤ 追加backlog → ⑥ 归档+汇报

**关键规则:**
- **场景驱动,不是工具驱动**——从受众真实工作痛点切入,不是"拿专业工具教人"
- 先读调用方 `AGENTS.md` 目标人群再加工;画像不全就停下问用户
- 只追加 backlog,不改已有条目
- 提交规范见调用方 `Topics/inbox/README.md`(各 agent 往那倒素材)
