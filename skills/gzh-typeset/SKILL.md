---
name: gzh-typeset
description: 公众号长文排版。读 article.md 输出可复制粘贴公众号的 wechat.html(全 inline 样式,套品牌排版:刊头条/章节标签/胶囊/功能卡/署名块/三档关键词强调)。当用户给公众号长文排版、生成 wechat.html、问公众号怎么排版或复制粘贴排版工具时使用。触发词:公众号排版、长文排版、wechat.html、排版、typeset。
version: 0.1.0
author: Kelegele
license: MIT
metadata:
  tags: [content, wechat, gongzhonghao, typeset, publish, html, inline-style]
---

# gzh-typeset 公众号长文排版

把 gzh-longform 写好的 `article.md` 排成可一键复制粘贴到公众号后台的 `wechat.html`。全 inline 样式(粘贴即生效),套飞栗品牌排版,正文标点全角化。

## 为什么是 inline 样式

公众号后台是富文本编辑器,复制粘贴时只保留 **inline style**(`<p style="...">`)。`<style>` 块和 class 会被丢掉。所以本 skill 产出**全部 inline 样式**的 HTML:浏览器打开 → Ctrl+A 全选 → 复制 → 粘贴公众号,样式 100% 生效。

## 工作流

### 第 0 步 运行参数 + 读规范

问用户:
- **目标文章路径**(如 `Content/20260626-xxx/article.md`)
- **品牌配置**(默认见下,用户可改)

读目的仓库 `AGENTS.md`/`CLAUDE.md` 的「公众号长文创作」节,确认:文字小标题(不用 ①②③)、正文无 #tag、长文节奏(段落连贯,不是卡片短句)。

### 第 1 步 标点全角化

```bash
uv run python scripts/punct_normalize.py <article.md>
```

把正文标点转中文全角(，：（）？),**保护** frontmatter YAML 键(`title:`)、markdown 图片/链接语法(`![]()` `[]()`)、URL(`https://`)。article.md 已全角则跳过。

### 第 2 步 基准段先行(风格确认)

先只生成**刊头条 + H1 + 开头一段 + 一个 H2 章节(含章节标签)**,让用户在浏览器看。**用户确认风格后才批量生成全文。** 不一口气全生成(同 text-to-card/gzh-illustration 教训)。

### 第 3 步 生成完整 wechat.html

从 article.md **逐段复制正文文字**(不手敲,防错字),套「样式规范」的 inline 模板。图片用相对路径 `images/xxx.png`。输出 `Content/<组>/wechat.html`。

### 第 4 步 自检

- [ ] 正文标点全角(，：（）？)
- [ ] inline style 完整;CSS / markdown 语法 / URL 的半角标点没被破坏
- [ ] 关键词强调三档克制(见下),标差异点不标重复标签
- [ ] 没改原文文字(只排版)
- [ ] 图片位置对

### 第 5 步 预览 + 实测提醒

- 浏览器 `file://` 打开预览
- **务必提醒用户**:复制粘贴到公众号草稿**实测一次**,尤其反色块(白字橙底)、胶囊的 `background` 兼容性;图片需手动上传(公众号不吃本地路径)

## 品牌配置(项目级,换品牌改这里)

- **主色**:`#FF5700`
- **辅色(浅橙底)**:`#FFF7F2`
- **刊头条文案**:
  - 📖 分享我所知道的AI技巧笔记
  - 🧐 多实践 · 挖技巧 · 让复杂变简单
- **署名块**:
  - 品牌:飞栗.ai
  - 定位语:多实践 · 挖技巧 · 让复杂变简单
  - 关注引导:关注我,从放弃学习到驾驭AI 👇

## 样式规范(inline 模板,复制复用,不手敲)

> inline 不认 CSS 变量,下面模板里色值直接写死。

**品牌刊头条**(标题上方):
```html
<p style="text-align:center;margin:0 0 22px;">
  <span style="display:inline-block;padding:11px 20px;background:#FFF7F2;border-radius:10px;line-height:1.7;">
    <span style="display:block;font-size:13px;color:#3f3f3f;">📖 分享我所知道的AI技巧笔记</span>
    <span style="display:block;font-size:12px;color:#FF5700;letter-spacing:0.5px;margin-top:2px;">🧐 多实践 · 挖技巧 · 让复杂变简单</span>
  </span>
</p>
```

**H1 标题**:
```html
<h1 style="text-align:center;font-size:22px;font-weight:bold;color:#1a1a1a;margin:8px 0 24px;line-height:1.4;letter-spacing:0.5px;">标题</h1>
```

**H2 章节(性质标签 + 左色条标题)**:
```html
<p style="margin:36px 0 8px;"><span style="display:inline-block;padding:2px 10px;background:#FF5700;color:#fff;font-size:12px;border-radius:10px;letter-spacing:1px;">问题</span></p>
<h2 style="font-size:18px;font-weight:bold;color:#1a1a1a;margin:0 0 16px;padding-left:11px;border-left:4px solid #FF5700;line-height:1.5;">小标题</h2>
```

章节标签词(飞栗方法论结构,按章节性质选):`问题` `方案` `延伸` `上手` `判断` `对比` `避坑` `总结`。

**正文段落**:
```html
<p style="margin:0 0 18px;font-size:16px;line-height:1.8;color:#3f3f3f;letter-spacing:0.3px;">正文</p>
```

**三档关键词强调**(克制,全文 10-15 处,每段 1-2 处):

| 档 | 用途 | 模板 |
|----|------|------|
| 加粗主色(轻) | 大部分关键词 / 痛点数字 | `<strong style="color:#FF5700;font-weight:bold;">词</strong>` |
| 反色(重) | 最核心 2-3 个差异点 | `<span style="background:#FF5700;color:#fff;padding:1px 6px;border-radius:3px;font-weight:bold;">词</span>` |
| 胶囊(品牌概念) | 产品名/核心概念首次出现 | `<span style="background:#FFF7F2;color:#FF5700;padding:2px 8px;border-radius:10px;font-weight:bold;font-size:15px;">Agent Mail</span>` |

高亮**差异点**,不标重复标签词(如别每条都高亮"别用")。不用黄色荧光(和橙色品牌色不搭,坚持品牌橙系)。

**功能列表卡片**(成组的并列条目):
```html
<div style="margin:18px 0 24px;padding:16px 18px;background:#FAFAFA;border-left:3px solid #FF5700;border-radius:0 6px 6px 0;">
  <p style="margin:0 0 10px;font-size:16px;line-height:1.75;color:#3f3f3f;">📥 条目一</p>
  <p style="margin:0 0 10px;font-size:16px;line-height:1.75;color:#3f3f3f;">🗂 条目二</p>
  <p style="margin:0;font-size:16px;line-height:1.75;color:#3f3f3f;">✂️ 条目三</p>
</div>
```

**核心观点引用块**(文末金句):
```html
<blockquote style="margin:28px 0 0;padding:14px 16px;border-left:4px solid #FF5700;background:#FFF7F2;font-size:15px;line-height:1.75;color:#5a5a5a;">
  <strong style="color:#FF5700;font-weight:bold;">核心观点</strong>:一句话总结。
</blockquote>
```

**结尾署名块**(白底橙边):
```html
<div style="margin:28px 0 0;padding:22px 16px;border:1px solid #FF5700;border-radius:8px;text-align:center;">
  <p style="margin:0 0 8px;font-size:17px;font-weight:bold;color:#FF5700;letter-spacing:0.5px;">飞栗.ai</p>
  <p style="margin:0 0 4px;font-size:14px;color:#5a5a5a;line-height:1.7;">多实践 · 挖技巧 · 让复杂变简单</p>
  <p style="margin:0;font-size:14px;color:#FF5700;line-height:1.7;">关注我,从放弃学习到驾驭AI 👇</p>
</div>
```

**图片**:
```html
<img src="images/xxx.png" alt="说明" style="max-width:100%;width:100%;display:block;margin:24px 0;border-radius:6px;" />
```

**本地预览容器**(head 里,不影响粘贴):
```html
<style>body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;max-width:680px;margin:40px auto;padding:0 24px;background:#fff;}</style>
```

## 标点全角化脚本

```bash
uv run python scripts/punct_normalize.py <article.md 或 wechat.html>
```

自动识别 md / html:半角 `, : ? ! ; ( )` → 全角,保护 markdown 语法 / URL / frontmatter / HTML 属性和 `<style>` 块。详见 `scripts/punct_normalize.py`。

## 不做(YAGNI)

- 不改原文文字(只排版;文字改动归 gzh-longform)
- 不自动判断所有强调点(agent 按三档策略判断,不机械遍历每个词)
- 不处理图片上传公众号(手动)
- 不做代码块语法高亮(本期长文无代码块,预留)
- 不调用 md-to-wechat / 不推送(用户人工)

## 经验教训(踩坑记录)

- **从 article.md 复制正文,不手敲** —— 手敲 HTML 易混入错字(实战出现过"退订"敲成"退荐")。正文文字一律从 md 复制,只套样式。
- **标点全角只改正文,不碰 CSS / md 语法 / URL** —— `style="color:#FF5700;"` 的冒号、`![]()` 的括号、`https://` 的冒号改了就废。脚本用遮罩法保护(见 punct_normalize.py)。
- **强调三档克制,标差异点** —— 全强调 = 没强调;加粗主色为主,反色只给 2-3 个最核心差异点,胶囊只给产品名/核心概念首次。不标重复标签词。
- **反色 / 胶囊上线前必测** —— inline 的 `background` 在公众号偶尔有兼容细节,本地好看 ≠ 公众号好看,粘草稿实测。
- **图片不跟随粘贴** —— 公众号不吃本地图片路径,文字粘贴后图片位手动上传插入。
- **基准段先行** —— 刊头条 + H1 + 一个章节定风格,确认后批量,避免全量返工(同 gzh-illustration / text-to-card 教训)。
