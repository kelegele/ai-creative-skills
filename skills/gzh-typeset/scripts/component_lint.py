#!/usr/bin/env python3
"""gzh-typeset 组件一致性 lint。

检查 wechat.html 里"同类组件"的 inline style 是否一致(公众号排版里,同一组件的字号/颜色/
行高/边距必须统一,不一致 = 视觉杂乱)。不做语法校验(那是 validate_gzh_html.py 的活)。

用法:
    uv run python component_lint.py <file.html>

退出码: 1 = 有不一致(WARN 级别,需人工确认); 0 = 通过。
"""
import argparse
import re
import sys
from collections import defaultdict


# 按标签 + 关键 style 特征归组,组内比对该特征的取值是否统一
# (标签, style 中的属性正则) → 组件名
RULES = [
    (r"<p\s", r"font-size", "正文/段落字号"),
    (r"<p\s", r"line-height", "正文/段落行高"),
    (r"<p\s", r"color", "正文/段落颜色"),
    (r"<h2\s", r"font-size", "H2 章节字号"),
    (r"<h2\s", r"color", "H2 章节颜色"),
    (r"<span[^>]*style", r"background", "内联强调/胶囊背景"),
    (r"<section\s", r"background", "容器块背景"),
    (r"<section\s", r"border-left", "容器块左边条"),
    (r"<blockquote\s", r"border-left", "引用块左边条"),
]


def extract_style_attr(tag_html: str) -> str:
    """从标签 HTML 里提取 style 属性值。"""
    m = re.search(r'style="([^"]*)"', tag_html, re.S)
    return m.group(1) if m else ""


def prop_value(style_attr: str, prop: str) -> str:
    """从 style 属性值里取某属性的值(如 font-size 后的 16px)。"""
    m = re.search(rf"{prop}\s*:\s*([^;]+)", style_attr)
    return m.group(1).strip() if m else "<无>"


def main():
    ap = argparse.ArgumentParser(description="组件一致性 lint")
    ap.add_argument("file", help="HTML 文件路径")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as f:
        html = f.read()

    issues = []

    for tag_pat, prop, comp_name in RULES:
        matches = list(re.finditer(tag_pat, html))
        if len(matches) < 2:
            continue  # 同类组件不足 2 个,无从对比
        values = defaultdict(list)
        for m in matches:
            # 取该标签的完整开标签(到 > 或 />)
            end = m.end()
            close = html.find(">", end)
            if close == -1:
                continue
            tag_html = html[m.start():close + 1]
            style_attr = extract_style_attr(tag_html)
            if not style_attr:
                continue
            v = prop_value(style_attr, prop)
            values[v].append(m.start())
        if len(values) > 1:
            most = max(values, key=lambda k: len(values[k]))
            others = [k for k in values if k != most]
            for o in others:
                issues.append(f"[WARN] {comp_name}不一致:多数为 {most!r},发现 {o!r}(位置 {values[o][:3]})")

    if issues:
        for i in issues:
            print(i)
        print(f"\n{args.file}: {len(issues)} 处不一致,需人工确认")
        return 1
    print(f"{args.file}: 组件样式一致 ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
