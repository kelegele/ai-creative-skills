#!/usr/bin/env python3
"""gzh-typeset 公众号 HTML 合规校验器。

把 gzh-typeset SKILL.md「样式规范 / 踩坑记录」里的平台红线从"模型自觉"变成确定性检查。
排版生成后必跑:检查公众号会过滤或改写的标签/属性/样式,并核查正文文字是否被带 inline
样式的标签包裹(公众号粘贴后保持样式的关键)。

用法:
    uv run python validate_gzh_html.py <file.html>
    uv run python validate_gzh_html.py --stdin < file.html

退出码: 1 = 有 ERROR(会被公众号过滤或粘贴后样式丢失); 0 = 通过。
"""
import argparse
import re
import sys
from html.parser import HTMLParser


# (正则, 级别, 说明) —— ERROR 会被公众号编辑器过滤或导致样式丢失
FORBIDDEN = [
    (re.compile(r"<style[\s>]", re.I), "ERROR", "<style> 标签会被过滤,样式必须内联(仅允许 head 预览容器)"),
    (re.compile(r"<script[\s>]", re.I), "ERROR", "<script> 标签会被过滤"),
    (re.compile(r"</?div[\s>]", re.I), "ERROR", "<div> 会被公众号改写,请用 <section>"),
    (re.compile(r"<link[\s>]", re.I), "ERROR", "外部 <link>(CSS/字体)会被过滤"),
    (re.compile(r"\sclass\s*=", re.I), "ERROR", "class 属性会被剥离,请用内联 style"),
    (re.compile(r"\sid\s*=", re.I), "ERROR", "id 属性会被剥离"),
    (re.compile(r"position\s*:\s*(fixed|absolute|sticky)", re.I), "ERROR", "position fixed/absolute/sticky 不被支持"),
    (re.compile(r"float\s*:", re.I), "ERROR", "float 不被支持"),
    (re.compile(r"@media", re.I), "ERROR", "@media 媒体查询不被支持"),
    (re.compile(r"@keyframes", re.I), "ERROR", "@keyframes 动画不被支持"),
    (re.compile(r"@import", re.I), "ERROR", "@import 不被支持"),
    (re.compile(r"display\s*:\s*grid", re.I), "ERROR", "display:grid 不被支持,请用 flex/block"),
    (re.compile(r"var\s*\(\s*--", re.I), "ERROR", "CSS 变量不被支持,色值直接写死"),
    (re.compile(r"border\s*:\s*1px\s+solid\s+#?[0-9a-fA-F]{3,6}\s*;", re.I), "WARN",
     "四边 border 简写在公众号易丢,建议用 background 或单边 border-left"),
]


class InlineChecker(HTMLParser):
    """检查正文文本节点是否被带 inline style 的祖先标签包裹。"""

    INLINE_SAFE_TAGS = {"p", "h1", "h2", "h3", "span", "strong", "em", "blockquote", "section", "li", "a", "b", "u"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.bare_texts = []  # (行号, 文本片段)

    def handle_starttag(self, tag, attrs):
        has_style = any(k == "style" for k, _ in attrs)
        self.stack.append((tag, has_style))

    def handle_startendtag(self, tag, attrs):
        pass  # 自闭合(img/br)无文本内容

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        safe = any(has_style for _, has_style in self.stack if _ in self.INLINE_SAFE_TAGS)
        if not safe:
            self.bare_texts.append(text[:50])


def main():
    ap = argparse.ArgumentParser(description="公众号 HTML 合规校验")
    ap.add_argument("file", nargs="?", help="HTML 文件路径(--stdin 时忽略)")
    ap.add_argument("--stdin", action="store_true", help="从标准输入读 HTML")
    args = ap.parse_args()

    if args.stdin:
        html = sys.stdin.read()
        src = "<stdin>"
    elif args.file:
        with open(args.file, encoding="utf-8") as f:
            html = f.read()
        src = args.file
    else:
        ap.error("需要文件路径或 --stdin")

    errors, warns = [], []

    # 0) 划定 body 区间(红线只查 body;head 里的本地预览 <style> 容器豁免——公众号粘贴不受影响)
    body_match = re.search(r"<body.*?</body>", html, re.S)
    if body_match:
        scan_region = body_match.group(0)
        body_region = scan_region
    else:
        scan_region = html
        body_region = html

    # 1) 平台红线(body 内)
    for pat, level, desc in FORBIDDEN:
        for m in pat.finditer(scan_region):
            (errors if level == "ERROR" else warns).append(f"[{level}] {desc} → {scan_region[max(0, m.start()-30):m.end()+30]!r}")

    # 2) 文本节点包裹检查(body 内)
    checker = InlineChecker()
    checker.feed(body_region)
    for frag in checker.bare_texts:
        errors.append(f"[ERROR] 裸文本未被带 inline style 的标签包裹 → …{frag}…")

    # 3) 汇总
    for w in warns:
        print(w)
    for e in errors:
        print(e)
    print(f"\n{src}: {len(errors)} ERROR, {len(warns)} WARN")
    if errors:
        print("✗ 未通过:有 ERROR(会被公众号过滤或样式丢失)")
        return 1
    if warns:
        print("⚠ 通过但需人工复核 WARN")
        return 0
    print("✓ 通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
