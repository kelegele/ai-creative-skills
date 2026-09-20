#!/usr/bin/env python3
"""gzh-typeset 组件一致性 lint。

检查 wechat.html 里"同类组件"的 inline style 是否一致(公众号排版里,同一组件的字号/颜色/
行高/边距必须统一,不一致 = 视觉杂乱)。不做语法校验(那是 validate_gzh_html.py 的活)。

用法:
    uv run python component_lint.py <file.html> [--primary #FF5700] [--accent #FFF7F2]

主题色用 --primary / --accent 传入(默认 feili 主题;换主题排版时传对应 theme.md 的
primary / accent_bg,否则反色/胶囊规则静默失效)。

退出码: 1 = 有不一致(WARN 级别,需人工确认); 0 = 通过。
"""
import argparse
import re
import sys
from collections import defaultdict


# 按标签 + 关键 style 特征归组,组内比对该特征的取值是否统一
# (标签, style 中的属性正则) → 组件名;主题色规则由 build_rules 动态生成
BASE_RULES = [
    (r"<p\s", r"font-size", "正文/段落字号"),
    (r"<p\s", r"line-height", "正文/段落行高"),
    (r"<p\s", r"color", "正文/段落颜色"),
    (r"<h2\s", r"font-size", "H2 章节字号"),
    (r"<h2\s", r"color", "H2 章节颜色"),
    (r"<section\s", r"background", "容器块背景"),
    (r"<section\s", r"border-left", "容器块左边条"),
    (r"<blockquote\s", r"border-left", "引用块左边条"),
]


def build_rules(primary: str, accent: str) -> list:
    """反色/胶囊规则依赖主题色,按所选主题动态生成。"""
    return BASE_RULES[:5] + [
        (rf"<span[^>]*style=\"[^\"]*background:\s*{re.escape(primary)}", r"background", "反色强调(白字主题底)"),
        (rf"<span[^>]*style=\"[^\"]*background:\s*{re.escape(accent)}", r"background", "胶囊(浅色主题底)"),
    ] + BASE_RULES[5:]


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
    ap.add_argument("--primary", default="#FF5700", help="主题主色(反色强调规则用,默认 feili)")
    ap.add_argument("--accent", default="#FFF7F2", help="主题辅色(胶囊规则用,默认 feili)")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as f:
        html = f.read()

    # 剥掉 head 里的 <style> 块(本地预览容器,不是正文组件,避免误报)
    html = re.sub(r"<style.*?</style>", "", html, flags=re.S)

    issues = []

    for tag_pat, prop, comp_name in build_rules(args.primary, args.accent):
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
            if v == "<无>":
                continue  # 特殊用途标签(章节标签行/图片行等)无该属性,不参与对比
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
