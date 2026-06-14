# AI Creative Toolkit 🎨

AI内容创作工具集，包含skill、工具脚本和共用素材。

## 安装

用 `skills` CLI 一键装到 agent 的 skills 目录:

```bash
# 装单个 skill(把 <skill-name> 换成下面的 skill 名)
npx skills add https://github.com/kelegele/ai-creative-skills --skill <skill-name>

# 例:装本仓的三个 skill
npx skills add https://github.com/kelegele/ai-creative-skills --skill text-to-card
npx skills add https://github.com/kelegele/ai-creative-skills --skill harvest-topics
npx skills add https://github.com/kelegele/ai-creative-skills --skill submit-to-inbox
```

## 结构

```
├ skills/           ← 可复用的创作技能
│   ├ text-to-card/    文章转图文卡片
│   ├ harvest-topics/  素材转选题候选
│   └ submit-to-inbox/ 素材提交(带降级)
├ tools/            ← 独立工具/脚本
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

## License

MIT
