#!/usr/bin/env python3
"""Generate uniform HTML cards from template functions + content data.

This is the RECOMMENDED way to generate cards (v0.6+).
AI designs the templates (fonts, colors, spacing, decorations),
Python fills in content and generates all cards with 100% style consistency.

Usage:
  1. AI designs template functions (make_cover, make_single, make_merged, make_ending)
  2. Define content data in the `cards` list below
  3. Run: python3 gen_cards.py
  4. All HTML files generated in OUTPUT_DIR
  5. Then run screenshot.py to convert to PNG

Customize:
  - Template functions: adjust fonts, sizes, colors, decorations
  - Content data: fill in titles, body text, tips for each card
  - OUTPUT_DIR: change output location
"""

import os

OUTPUT_DIR = "/tmp/cards_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONTS_IMPORT = """
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&family=Noto+Serif+SC:wght@700;900&display=swap" rel="stylesheet">
""".strip()

# ============================================================
# TEMPLATE FUNCTIONS — AI designs these, do NOT modify per-card
# ============================================================

def make_cover(num, total, title, subtitle):
    """Cover card: magazine-style with ghost number watermark."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=1080">
{FONTS_IMPORT}
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1440px; overflow:hidden; background:#FFFFFF; font-family:'Inter',sans-serif; position:relative; }}
.ghost {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-55%); font-family:'Playfair Display',serif; font-size:720px; font-weight:900; color:#FF5701; opacity:0.06; pointer-events:none; }}
.top-bar {{ position:absolute; top:0; left:0; right:0; height:8px; background:#FF5701; }}
.content {{ position:absolute; top:0; left:0; right:0; bottom:0; display:flex; flex-direction:column; justify-content:center; padding:80px 88px; }}
.badge {{ display:inline-block; background:#FF5701; color:#FFF; font-family:'JetBrains Mono',monospace; font-size:24px; font-weight:600; padding:8px 20px; letter-spacing:2px; margin-bottom:40px; }}
.main-title {{ font-family:'Noto Serif SC',serif; font-size:76px; font-weight:900; color:#111827; line-height:1.3; margin-bottom:32px; }}
.main-title .accent {{ color:#FF5701; }}
.sub {{ font-family:'Inter',sans-serif; font-size:32px; color:#6B7280; margin-bottom:60px; }}
.sub .hl {{ color:#FF5701; font-family:'JetBrains Mono',monospace; font-weight:600; }}
.bottom-bar {{ position:absolute; bottom:0; left:0; right:0; height:64px; background:#F6F6F1; display:flex; align-items:center; justify-content:space-between; padding:0 88px; }}
.page-num {{ font-family:'JetBrains Mono',monospace; font-size:22px; color:#9CA3AF; }}
.brand {{ font-family:'JetBrains Mono',monospace; font-size:18px; color:#9CA3AF; letter-spacing:3px; }}
.corner {{ position:absolute; width:40px; height:40px; border-color:#E5E7EB; border-style:solid; }}
.tl {{ top:40px; left:40px; border-width:3px 0 0 3px; }}
.br {{ bottom:80px; right:40px; border-width:0 3px 3px 0; }}
</style></head><body>
<div class="ghost">22</div>
<div class="top-bar"></div>
<div class="corner tl"></div>
<div class="corner br"></div>
<div class="content">
  <div class="badge">深度拆解</div>
  <div class="main-title">{title}</div>
  <div class="sub">{subtitle}</div>
</div>
<div class="bottom-bar">
  <div class="page-num">{num:02d} / {total}</div>
  <div class="brand">AGENTIC</div>
</div>
</body></html>"""


def make_single(num, total, title, body, tip):
    """Single-point content card: one topic per card."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=1080">
{FONTS_IMPORT}
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1440px; overflow:hidden; background:#FFFFFF; font-family:'Inter',sans-serif; position:relative; }}
.top-bar {{ position:absolute; top:0; left:0; right:0; height:8px; background:#FF5701; }}
.card-num {{ position:absolute; top:60px; left:88px; font-family:'Playfair Display',serif; font-size:140px; font-weight:900; color:#FF5701; line-height:1; }}
.page-ind {{ position:absolute; top:80px; right:88px; font-family:'JetBrains Mono',monospace; font-size:24px; color:#9CA3AF; }}
.main {{ position:absolute; top:260px; left:88px; right:88px; bottom:80px; display:flex; flex-direction:column; }}
.accent-line {{ width:64px; height:6px; background:#FF5701; margin-bottom:40px; }}
.title {{ font-family:'Noto Serif SC',serif; font-size:72px; font-weight:900; color:#111827; line-height:1.25; margin-bottom:36px; }}
.body {{ font-family:'Inter',sans-serif; font-size:36px; color:#374151; line-height:1.75; margin-bottom:40px; }}
.tip {{ background:#FFF7ED; border-left:5px solid #FF5701; padding:24px 28px; font-family:'Inter',sans-serif; font-size:30px; color:#9A3412; line-height:1.6; border-radius:0 8px 8px 0; }}
.bottom-bar {{ position:absolute; bottom:0; left:0; right:0; height:8px; background:linear-gradient(to right, #FF5701 0%, #FF5701 33%, #F6F6F1 33%, #F6F6F1 66%, #FF5701 66%, #FF5701 100%); }}
</style></head><body>
<div class="top-bar"></div>
<div class="card-num">{num:02d}</div>
<div class="page-ind">{num:02d} / {total}</div>
<div class="main">
  <div class="accent-line"></div>
  <div class="title">{title}</div>
  <div class="body">{body}</div>
  <div class="tip">💡 {tip}</div>
</div>
<div class="bottom-bar"></div>
</body></html>"""


def make_merged(num, total, title_a, body_a, tip_a, title_b, body_b, tip_b):
    """Merged two-point card: two topics in upper/lower split."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=1080">
{FONTS_IMPORT}
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1440px; overflow:hidden; background:#FFFFFF; font-family:'Inter',sans-serif; position:relative; }}
.top-bar {{ position:absolute; top:0; left:0; right:0; height:8px; background:#FF5701; }}
.card-num {{ position:absolute; top:50px; left:88px; font-family:'Playfair Display',serif; font-size:120px; font-weight:900; color:#FF5701; line-height:1; }}
.page-ind {{ position:absolute; top:66px; right:88px; font-family:'JetBrains Mono',monospace; font-size:22px; color:#9CA3AF; }}
.sections {{ position:absolute; top:200px; left:88px; right:88px; bottom:60px; display:flex; flex-direction:column; }}
.section {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
.divider {{ width:100%; height:3px; background:#F6F6F1; margin:8px 0; position:relative; }}
.divider::after {{ content:''; position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:12px; height:12px; background:#FF5701; border-radius:50%; }}
.accent-line {{ width:48px; height:4px; background:#FF5701; margin-bottom:20px; }}
.title {{ font-family:'Noto Serif SC',serif; font-size:52px; font-weight:900; color:#111827; line-height:1.25; margin-bottom:16px; }}
.body {{ font-family:'Inter',sans-serif; font-size:28px; color:#374151; line-height:1.7; margin-bottom:14px; }}
.tip {{ background:#FFF7ED; border-left:4px solid #FF5701; padding:14px 18px; font-family:'Inter',sans-serif; font-size:24px; color:#9A3412; line-height:1.5; border-radius:0 6px 6px 0; }}
.bottom-bar {{ position:absolute; bottom:0; left:0; right:0; height:8px; background:linear-gradient(to right, #FF5701 0%, #FF5701 33%, #F6F6F1 33%, #F6F6F1 66%, #FF5701 66%, #FF5701 100%); }}
</style></head><body>
<div class="top-bar"></div>
<div class="card-num">{num:02d}</div>
<div class="page-ind">{num:02d} / {total}</div>
<div class="sections">
  <div class="section">
    <div class="accent-line"></div>
    <div class="title">{title_a}</div>
    <div class="body">{body_a}</div>
    <div class="tip">💡 {tip_a}</div>
  </div>
  <div class="divider"></div>
  <div class="section">
    <div class="accent-line"></div>
    <div class="title">{title_b}</div>
    <div class="body">{body_b}</div>
    <div class="tip">💡 {tip_b}</div>
  </div>
</div>
<div class="bottom-bar"></div>
</body></html>"""


def make_ending(num, total, quote, attribution, source):
    """Ending card: centered quote with attribution."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=1080">
{FONTS_IMPORT}
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1440px; overflow:hidden; background:#FFFFFF; font-family:'Inter',sans-serif; position:relative; }}
.top-bar {{ position:absolute; top:0; left:0; right:0; height:8px; background:#FF5701; }}
.quote-mark {{ position:absolute; font-family:'Playfair Display',serif; font-size:400px; font-weight:900; color:#FF5701; opacity:0.08; line-height:1; }}
.qm-open {{ top:120px; left:60px; }}
.qm-close {{ bottom:200px; right:60px; }}
.center {{ position:absolute; top:0; left:0; right:0; bottom:0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:0 120px; }}
.quote-text {{ font-family:'Noto Serif SC',serif; font-size:60px; font-weight:900; color:#111827; line-height:1.5; text-align:center; margin-bottom:48px; }}
.divider {{ width:120px; height:4px; background:#FF5701; margin-bottom:36px; }}
.attr {{ font-family:'JetBrains Mono',monospace; font-size:26px; color:#6B7280; margin-bottom:20px; }}
.source {{ font-family:'Inter',sans-serif; font-size:24px; color:#9CA3AF; text-align:center; line-height:1.8; }}
.source .hl {{ color:#FF5701; font-family:'JetBrains Mono',monospace; font-weight:600; }}
.bottom-bar {{ position:absolute; bottom:0; left:0; right:0; height:64px; background:#F6F6F1; display:flex; align-items:center; justify-content:center; }}
.page-num {{ font-family:'JetBrains Mono',monospace; font-size:22px; color:#9CA3AF; }}
.corner {{ position:absolute; width:40px; height:40px; border-color:#E5E7EB; border-style:solid; }}
.tl {{ top:40px; left:40px; border-width:3px 0 0 3px; }}
.br {{ bottom:80px; right:40px; border-width:0 3px 3px 0; }}
</style></head><body>
<div class="top-bar"></div>
<div class="corner tl"></div>
<div class="corner br"></div>
<div class="quote-mark qm-open">"</div>
<div class="quote-mark qm-close">"</div>
<div class="center">
  <div class="quote-text">{quote}</div>
  <div class="divider"></div>
  <div class="attr">{attribution}</div>
  <div class="source">{source}</div>
</div>
<div class="bottom-bar">
  <div class="page-num">{num:02d} / {total}</div>
</div>
</body></html>"""


# ============================================================
# CONTENT DATA — Fill in your card content here
# ============================================================

TOTAL = 18  # Total card count (cover + content + ending)

cards = [
    # Card 01 — Cover
    ("cover", {
        "num": 1, "total": TOTAL,
        "title": '掌握 <span class="accent">Matt Van Horn</span> 的22条驾驭Agent的技巧，不再被笨AI气到跳脚',
        "subtitle": '原文 <span class="hl">913K</span> 阅读 · 我帮你拆成了 <span class="hl">18</span> 张卡片'
    }),
    # Card 02 — Single point
    ("single", {
        "num": 2, "total": TOTAL,
        "title": "永远先写计划",
        "body": "有想法就先写计划，不要直接开干。不管是一个新产品点子、一个bug、还是一个终端报错——先让Agent出计划，再让它执行。传统开发80%时间在写代码，20%在规划。反过来就对了。",
        "tip": "任何想法冒出来，第一反应不是写代码，而是让Agent先出计划"
    }),
    # Card 03 — Single point
    ("single", {
        "num": 3, "total": TOTAL,
        "title": "计划是给Agent看的",
        "body": "写计划但不要读计划。计划的作用是约束Agent不偷懒——有计划它就会认真调研、写验收标准、逐条完成。你只需要扫一眼标题，有问题直接问「为什么这么做」。",
        "tip": "写计划时用「请列出步骤，每步给出预期输出」的格式"
    }),
    # Card 04 — Merged: 模糊想法 + 先计划如何计划
    ("merged", {
        "num": 4, "total": TOTAL,
        "title_a": "模糊想法先头脑风暴", "body_a": "需求说不清楚？别急着规划，先跟Agent聊。把模糊想法聊清楚，等方向明确了再出计划。",
        "tip_a": "不知道自己要什么的时候，先跟Agent聊十分钟理清思路",
        "title_b": "先计划如何计划", "body_b": "复杂任务别直接出结果。先让Agent做一个「怎么做这件事的计划」，再按计划执行。先规划再干活，质量高一个量级。",
        "tip_b": "面对模糊需求时，先让Agent拆解需求再开始干活"
    }),
    # Card 05 — Single
    ("single", {
        "num": 5, "total": TOTAL,
        "title": "语音输入解放双手",
        "body": "对着Agent说话比打字快三倍。Mac用Monologue或Wispr Flow，手机用系统自带听写就够了——听者是LLM，理解力很强，你含糊其辞它也能猜对。买个话筒，边走边说。",
        "tip": "通勤路上用语音描述需求，到工位时Agent已经写好初版代码"
    }),
    # Card 06 — Single
    ("single", {
        "num": 6, "total": TOTAL,
        "title": "并行4-6个会话",
        "body": "一个窗口写计划，一个窗口构建功能，一个窗口跑调研，一个窗口修bug。Agent在A窗口研究代码的时候，你切到B窗口审查已完成的工作。轮转起来，从不空等。",
        "tip": "同时开3个会话：一个调研、一个写前端、一个写后端"
    }),
    # Card 07 — Merged: 新Tab + 手机远程
    ("merged", {
        "num": 7, "total": TOTAL,
        "title_a": "新Tab直进Agent", "body_a": "新开终端标签页应该直接进入Agent对话，而不是先cd再手动启动。启动成本降到一次按键，自然开更多会话。",
        "tip_a": "配置终端让新标签页直接进入Agent",
        "title_b": "手机远程操控Agent", "body_b": "桌面开Agent会话，出门后用手机远程接管。更进一步：给Agent一个邮箱地址，发邮件就自动触发新会话开始干活。",
        "tip_b": "在外面用手机直接操控家里的Agent继续干活"
    }),
    # Card 08 — Merged: 信任Agent + 双引擎
    ("merged", {
        "num": 8, "total": TOTAL,
        "title_a": "信任Agent，跳过权限确认", "body_a": "同时跑6个会话，不可能挨个确认权限。开启bypass模式，配合声音提醒知道哪个完成了。有Git兜底，大不了回滚。",
        "tip_a": "让Agent直接改代码，改完 git diff 审查一遍就行",
        "title_b": "双引擎并行", "body_b": "一个引擎负责规划和品味，另一个负责构建和执行。两个并排跑，大型并行构建推给第二引擎，第一个专注规划。",
        "tip_b": "用两个AI引擎各司其职，一个负责想一个负责做"
    }),
    # Card 09 — Merged: 调研先行 + 原始素材
    ("merged", {
        "num": 9, "total": TOTAL,
        "title_a": "last30days调研先行", "body_a": "做决策前先搜近30天社区讨论——Reddit、X、YouTube、HN全部并行搜索。几分钟了解真实用户怎么说，比看过时文档靠谱。",
        "tip_a": "选技术栈前，让Agent搜索最近30天社区讨论再拍板",
        "title_b": "原始素材胜过摘要", "body_b": "不要自己概括再给Agent。丢完整会议录音、原始报错日志、全部聊天记录。信息越完整，输出越准确。",
        "tip_b": "给Agent贴完整报错日志，别只说「它报错了」"
    }),
    # Card 10 — Single
    ("single", {
        "num": 10, "total": TOTAL,
        "title": "做品味担当",
        "body": "同时跑6个Agent，你的工作不是干活，而是做信号。Agent提供执行量，你提供品味、方向和纠偏。看看Agent的产出，说「方案二更接近但用方案一的语言」，它们就动了。稀缺的是你的判断力。",
        "tip": "你来定设计风格，让Agent去写CSS"
    }),
    # Card 11 — Merged: 视频Agent + 读取大脑
    ("merged", {
        "num": 11, "total": TOTAL,
        "title_a": "视频也能Agent做", "body_a": "用HTML写视频脚本，Agent直接渲染成MP4。不需要剪辑软件，不需要时间线。做视频的成本降到了一次对话。",
        "tip_a": "让Agent把产品介绍写成HTML动画脚本，自动渲染成短视频",
        "title_b": "让Agent读取你的大脑", "body_b": "把笔记工具接入Agent——十年的笔记、会议记录、想法，Agent都能读到。每次新会话都站在历史知识的肩膀上，越用越聪明。",
        "tip_b": "把你的笔记工具接入Agent，新会话也能继承历史知识"
    }),
    # Card 12 — Merged: Mosh + 飞机
    ("merged", {
        "num": 12, "total": TOTAL,
        "title_a": "Mosh替代SSH", "body_a": "远程连服务器用Mosh代替SSH。网络波动、切换WiFi、甚至漫游，连接都不断。普通SSH每次按键都在等网络往返，Mosh让远程跟本地一样流畅。",
        "tip_a": "远程服务器用Mosh代替SSH，网络波动也不卡",
        "title_b": "飞机上也能干活", "body_b": "用tmux在远程服务器挂Agent会话。飞机上WiFi断了20分钟？重连后attach回tmux，Agent还在原地干活。",
        "tip_b": "长途飞行用tmux挂远程会话，落地重连继续干"
    }),
    # Card 13 — Merged: 双系统 + Cookie同步
    ("merged", {
        "num": 13, "total": TOTAL,
        "title_a": "双系统生态", "body_a": "同时跑两个Agent系统——一个擅长自学习越用越好，另一个擅长技能广度。两个系统切换用，互补短板。",
        "tip_a": "同时用两个Agent系统，一个主深度一个主广度",
        "title_b": "Agent Cookie同步登录态", "body_b": "让Agent以你的身份操作需要登录的网站。同步浏览器cookies，Agent就能帮你下单、查订单、管理后台。",
        "tip_b": "让Agent帮你操作需要登录的网站，不用手动输密码"
    }),
    # Card 14 — Merged: 分享计划 + 重复变Skill
    ("merged", {
        "num": 14, "total": TOTAL,
        "title_a": "把计划分享给同事", "body_a": "plan.md对不熟悉终端的同事是天书。用工具把计划渲染成文档，同事在线审阅、评论，评论还能流回Agent循环里。",
        "tip_a": "把Agent生成的方案发给同事看，他们能直接在线评论",
        "title_b": "重复两次变Skill", "body_b": "同样的事做了两次？固化成Skill。第三次直接调用。技巧是找一个已有的Skill让Agent参照格式复制一个。",
        "tip_b": "第三次写同类PR时，把流程存成Skill一键调用"
    }),
    # Card 15 — Single
    ("single", {
        "num": 15, "total": TOTAL,
        "title": "开源贡献赚人脉",
        "body": "给你每天用的开源工具提PR——不是改typo，而是真正的功能。然后去Discord混，认识维护者，交朋友。PR是敲门砖，人脉才是真正收益。",
        "tip": "找一个你每天用的开源工具，给它提一个真正的功能PR"
    }),
    # Card 16 — Merged: 硬件 + CLIs跑生活
    ("merged", {
        "num": 16, "total": TOTAL,
        "title_a": "硬件不断电", "body_a": "6个Agent会话全天跑，笔记本扛不住。配置禁止休眠，随身带充电宝，车里也放一个。Agent最怕的不是bug，是你断了电。",
        "tip_a": "配置禁止休眠+随身带充电宝，Agent 24小时不中断",
        "title_b": "CLIs跑真实生活", "body_b": "Agent不止写代码。Tesla预热、买菜、赛事提醒、机票比价——用CLIs把真实服务包一层，Agent就能帮你跑腿。",
        "tip_b": "旅行前让Agent帮你对比机票酒店、排行程表"
    }),
    # Card 17 — Single
    ("single", {
        "num": 17, "total": TOTAL,
        "title": "注意平衡别上瘾",
        "body": "Agent是史上最好玩的游戏。朋友里有人沉迷到忘了身边人，上线了却没有用户。问题不是空发布，而是消失在构建中、失去身边的人。学会休息，学会关心人。",
        "tip": "每周留一天不用Agent，纯手动写代码保持手感"
    }),
    # Card 18 — Ending
    ("ending", {
        "num": 18, "total": TOTAL,
        "quote": "做那个提供品味的人，让Agent做那双执行的手",
        "attribution": "@mvanhorn · June 2026",
        "source": '基于 Matt Van Horn 原文改编<br>原文 <span class="hl">913K+</span> 阅读'
    }),
]

# ============================================================
# GENERATOR — Do NOT modify
# ============================================================

generators = {
    "cover": lambda d: make_cover(d["num"], d["total"], d["title"], d["subtitle"]),
    "single": lambda d: make_single(d["num"], d["total"], d["title"], d["body"], d["tip"]),
    "merged": lambda d: make_merged(d["num"], d["total"], d["title_a"], d["body_a"], d["tip_a"], d["title_b"], d["body_b"], d["tip_b"]),
    "ending": lambda d: make_ending(d["num"], d["total"], d["quote"], d["attribution"], d["source"]),
}

for i, (kind, data) in enumerate(cards, 1):
    html = generators[kind](data)
    path = os.path.join(OUTPUT_DIR, f"20260606-Agent技巧-card-{i:02d}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ {os.path.basename(path)} ({kind})")

print(f"\nDone: {len(cards)} cards generated in {OUTPUT_DIR}")
