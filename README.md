# AI Creative Toolkit 🎨

AI内容创作工具集，包含skill、工具脚本和共用素材。

## 安装

用 `skills` CLI 装到指定 agent——加 `-a <agent名>` 指定目标 agent(用法详见 [vercel-labs/skills](https://github.com/vercel-labs/skills)):

```bash
# 装单个 skill 到指定 agent
npx skills add https://github.com/kelegele/ai-creative-skills --skill <skill-name> -a <agent-name>

# 例:装 submit-to-inbox 到 Hermes
npx skills add https://github.com/kelegele/ai-creative-skills --skill submit-to-inbox -a hermes-agent

# 例:装 text-to-card 到 Hermes
npx skills add https://github.com/kelegele/ai-creative-skills --skill text-to-card -a hermes-agent
```

> `<agent-name>` 按目标 agent 填(hermes-agent / openclaw / codex / claude-code 等),完整列表见 [vercel-labs/skills](https://github.com/vercel-labs/skills)。

## 结构

```
├ skills/           ← 可复用的创作技能
│   ├ text-to-card/    文章转图文卡片
│   ├ harvest-topics/  素材转选题候选
│   ├ submit-to-inbox/ 素材提交(带降级)
│   ├ gzh-longform/   公众号长文(两阶段)
│   ├ gzh-illustration/ 公众号配图(HTML→截图)
│   ├ gzh-typeset/    公众号排版(wechat.html)
│   ├ remotion-video/  Remotion 视频创作
│   └ video-asset-library/ 视频素材库管理
├ tools/            ← 独立工具/脚本
│   └ asset-library-web/ 视频素材库静态橱窗(gallery.html)
└ assets/           ← 共用素材/模板
```

## Skills

### text-to-card
文章/博客转图文卡片流水线：大纲 → AI生成HTML → Playwright截图PNG。
支持小红书、微信公众号等平台。

→ 详见 [`skills/text-to-card/SKILL.md`](skills/text-to-card/SKILL.md)

### harvest-topics
把 `Topics/inbox/` 收集的素材加工成 `Topics/backlog.md` 选题候选。场景驱动,过目标人群筛,只追加不改。

→ 详见 [`skills/harvest-topics/SKILL.md`](skills/harvest-topics/SKILL.md)

### submit-to-inbox
把素材(链接/文字/图片)安全提交到 `Topics/inbox/`,带降级(gh cli→API→本地兜底),素材绝不丢。不依赖本地 clone 主仓。配合 harvest-topics:收集端提交 → 加工端加工。

→ 详见 [`skills/submit-to-inbox/SKILL.md`](skills/submit-to-inbox/SKILL.md)

### gzh-longform
公众号长文创作:两阶段(研究+写作),读目的仓库人设,内置爆款认知+可选联网查证,输出 markdown。

→ 详见 [`skills/gzh-longform/SKILL.md`](skills/gzh-longform/SKILL.md)

### gzh-illustration
公众号长文配图:读占位 → HTML 设计 → Playwright 截图 → 回填(草稿/定版两态)。封面 900×383 + 正文宽 1080。

→ 详见 [`skills/gzh-illustration/SKILL.md`](skills/gzh-illustration/SKILL.md)

### gzh-typeset
公众号长文排版:读 article.md 输出全 inline 样式的 wechat.html,可直接复制粘贴进公众号后台。

→ 详见 [`skills/gzh-typeset/SKILL.md`](skills/gzh-typeset/SKILL.md)

### remotion-video
Remotion 视频创作:前置检查清单(14 项)→ 分镜拆解 → 资产清单 → 代码生成 → 自检交付。Node 生态(npx),基准场景先行。

→ 详见 [`skills/remotion-video/SKILL.md`](skills/remotion-video/SKILL.md)

### video-asset-library
视频素材库管理:建库/入库/盘点/维护全流程,skill 驱动写操作,素材和元信息不进 git。查看走静态橱窗 `tools/asset-library-web/`。

→ 详见 [`skills/video-asset-library/SKILL.md`](skills/video-asset-library/SKILL.md)

## License

MIT
