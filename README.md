# AI Creative Toolkit 🎨

AI内容创作工具集，包含skill、工具脚本和共用素材。

## 结构

```
├ skills/           ← 可复用的创作技能
│   ├ text-to-card/    文章转图文卡片
│   └ harvest-topics/  素材转选题候选
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

## License

MIT
