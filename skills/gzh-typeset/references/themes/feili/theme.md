# 主题:feili(飞栗品牌,默认)

> 默认主题。对应 SKILL.md「品牌配置 / 样式规范」。改这里与改 SKILL.md 品牌配置需同步。

## 设计变量

- primary: #FF5700
- accent_bg: #FFF7F2
- body_color: #3f3f3f
- body_size: 16px
- body_lineheight: 1.8
- heading_color: #1a1a1a
- heading_size: 22px(H1)/18px(H2)
- radius: 10px
- 强调三档:加粗主色 / 反色(白字橙底)/ 胶囊(浅橙底橙字)

## 组件模板(占位符 {{primary}} 等,排版时替换)

**刊头条**(标题上方):
```html
<p style="text-align:center;margin:0 0 22px;">
  <span style="display:inline-block;padding:11px 20px;background:{{accent_bg}};border-radius:10px;line-height:1.7;">
    <span style="display:block;font-size:13px;color:#3f3f3f;">📖 分享我所知道的AI技巧笔记</span>
    <span style="display:block;font-size:12px;color:{{primary}};letter-spacing:0.5px;margin-top:2px;">🧐 多实践 · 挖场景 · 让复杂变简单</span>
  </span>
</p>
```

**H1 标题**:
```html
<h1 style="text-align:center;font-size:22px;font-weight:bold;color:{{heading_color}};margin:8px 0 24px;line-height:1.4;letter-spacing:0.5px;">标题</h1>
```

**H2 章节(性质标签 + 左色条标题)**:
```html
<p style="margin:36px 0 8px;"><span style="display:inline-block;padding:2px 10px;background:{{primary}};color:#fff;font-size:12px;border-radius:10px;letter-spacing:1px;">问题</span></p>
<h2 style="font-size:18px;font-weight:bold;color:{{heading_color}};margin:0 0 16px;padding-left:11px;border-left:4px solid {{primary}};line-height:1.5;">小标题</h2>
```

**正文段落**:
```html
<p style="margin:0 0 18px;font-size:16px;line-height:1.8;color:{{body_color}};letter-spacing:0.3px;">正文</p>
```

**三档强调**:
- 加粗主色:`<strong style="color:{{primary}};font-weight:bold;">词</strong>`
- 反色(最核心 2-3 个):`<span style="background:{{primary}};color:#fff;padding:1px 6px;border-radius:3px;font-weight:bold;">词</span>`
- 胶囊(品牌概念首次):`<span style="background:{{accent_bg}};color:{{primary}};padding:2px 8px;border-radius:10px;font-weight:bold;font-size:15px;">词</span>`

**功能列表卡片**:
```html
<section style="margin:18px 0 24px;padding:16px 18px;background:#FAFAFA;border-left:3px solid {{primary}};border-radius:0 6px 6px 0;">
  <p style="margin:0 0 10px;font-size:16px;line-height:1.75;color:{{body_color}};">📥 条目一</p>
</section>
```

**核心观点引用块**:
```html
<blockquote style="margin:28px 0 0;padding:14px 16px;border-left:4px solid {{primary}};background:{{accent_bg}};font-size:15px;line-height:1.75;color:#5a5a5a;">
  <strong style="color:{{primary}};font-weight:bold;">核心观点</strong>:一句话总结。
</blockquote>
```

**结尾署名块**:
```html
<section style="margin:28px 0 0;padding:22px 16px;background:{{accent_bg}};border-radius:8px;text-align:center;">
  <p style="margin:0 0 8px;font-size:17px;font-weight:bold;color:{{primary}};letter-spacing:0.5px;">飞栗.ai</p>
  <p style="margin:0 0 4px;font-size:14px;color:#5a5a5a;line-height:1.7;">多实践 · 挖场景 · 让复杂变简单</p>
  <p style="margin:0;font-size:14px;color:{{primary}};line-height:1.7;">关注我,从放弃学习到驾驭AI 👇</p>
</section>
```

**图片**:
```html
<img src="images/xxx.png" alt="说明" style="max-width:100%;width:100%;display:block;margin:24px 0;border-radius:6px;" />
```

## 题材契合

- AI 技巧 / 工具方法 / 认知分享(飞栗主线内容)
- 默认主题,无特殊题材限制
