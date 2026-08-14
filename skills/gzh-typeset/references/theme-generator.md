# 主题注册机制(gzh-typeset)

> 目的:让 gzh-typeset 不只服务飞栗品牌——把「一套品牌模板」扩展为「可注册的主题库」,每个主题是一组设计变量 + 组件模板,排版时按文章/品牌选主题。
> 原则:主题只存**变量与模板**,不写死内容;注册新主题不改 SKILL.md(增补式,不侵入)。

## 主题是什么

一个主题 = `references/themes/<name>/theme.md`,包含:

1. **设计变量**(frontmatter):
   - `primary` 主色(hex)
   - `accent_bg` 辅色浅底(hex)
   - `body_color` / `body_size` / `body_lineheight` 正文
   - `heading_color` / `heading_size` 标题
   - `radius` 圆角
2. **组件模板**(markdown 代码块,每组件一个):
   - 刊头条 / H1 / H2(含章节标签)/ 正文段 / 三档强调 / 功能列表卡 / 引用块 / 署名块 / 图片 / 分割线
   - 模板里色值用占位符 `{{primary}}` 等,排版时替换成实际值(不写死,方便换色)
3. **题材契合说明**:这主题适合什么文章(供自动推荐参考)

## 注册一个新主题

1. 在 `references/themes/` 下建 `<name>/theme.md`(按上面的结构,模板从现有主题复制改变量——改色值/字号,不重排结构)
2. 在 `references/theme-index.md` 追加一行:主题名 / 一句话风格 / 适合题材 / theme.md 路径
3. 用 `scripts/render_theme.py`(若实现)把主题模板渲染成完整 inline HTML 片段,浏览器目检
4. 排一篇短文实测:基准段先行 → 确认 → 批量

## 换主题排版

- 第 1 步选主题:读 `references/theme-index.md`,按文章题材推荐(有契合 → 单问确认;无 → 列主题让用户选)
- 用户指定主题 → 直接用,不问
- 全部主题都不满意 → 走「注册新主题」流程

## 与飞栗默认的关系

- 默认主题 = 飞栗品牌(`references/themes/feili/theme.md`,即当前 SKILL.md 里的品牌配置搬进去)
- 不删 SKILL.md 里的品牌配置,theme.md 是它的结构化版本;两者保持同步(改一个另一个也改)

## 不做(YAGNI)

- 不做 6 套预设主题(按需注册,注册即用)
- 不做主题生成器 CLI(注册 = 手写 theme.md,简单直接;真要生成器再补)
- 不做从参考图生成主题(视觉→变量映射主观,留给 agent 判断)
