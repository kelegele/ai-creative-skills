#!/usr/bin/env python3
"""check_fonts.py — 校验卡片 HTML 的字体使用 vs Google Fonts 加载一致性。

抓两类低级错误(都是 font-family 声明和 <link> 加载不同步导致):
1. CSS 用了某字体,但 <link> 没加载 → fallback 到系统字体(风格不对)
2. CSS 用了某字重,但 <link> 没加载该字重 → 浏览器合成 fake bold/light(笔画失真)

典型坑:card-number font-weight:600,但 link 只 Playfair:wght@400;700;900 → 600 合成。

用法:uv run python check_fonts.py <卡片目录>
退出码:0 = 通过,1 = 有问题(定版前必须 0)。
"""
import re, sys, pathlib

GENERIC = {'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy',
           'system-ui', 'inherit', 'initial', 'ui-serif', 'ui-sans-serif', 'ui-monospace'}


def parse_loaded(html):
    """从 Google Fonts <link> 解析 {字体名: {字重集合}}"""
    m = re.search(r'href="(https://fonts\.googleapis\.com/css2\?[^"]+)"', html)
    if not m:
        return {}
    qs = m.group(1).split('?', 1)[1]
    loaded = {}
    for part in qs.split('&'):
        if not part.startswith('family='):
            continue
        spec = part[7:]
        name, _, rest = spec.partition(':')
        name = name.replace('+', ' ')
        weights = set()
        if rest.startswith('wght@'):
            weights = set(rest[5:].split(';'))
        loaded[name] = weights
    return loaded


def parse_usage(html):
    """从 <style> 解析 [(主字体, 字重)] —— 每条 CSS 规则取 font-family 第一个非 generic 字体"""
    m = re.search(r'<style[^>]*>(.*?)</style>', html, re.S)
    if not m:
        return []
    css = m.group(1)
    usage = []
    for block in re.finditer(r'\{([^}]*)\}', css):
        body = block.group(1)
        fm = re.search(r'font-family:\s*([^;]+)', body)
        if not fm:
            continue
        families = [f.strip().strip("'\"") for f in fm.group(1).split(',')]
        primary = next((f for f in families if f and f not in GENERIC), None)
        if not primary:
            continue
        fw = re.search(r'font-weight:\s*(\d+)', body)
        weight = fw.group(1) if fw else '400'
        usage.append((primary, weight))
    return usage


def check(d):
    issues = []
    for f in sorted(d.glob("card-*.html")):
        html = f.read_text(encoding="utf-8")
        loaded = parse_loaded(html)
        seen = set()
        for fam, w in parse_usage(html):
            key = (fam, w)
            if key in seen:
                continue
            seen.add(key)
            if fam not in loaded:
                issues.append(f"  {f.name}: 用 '{fam}' 但 link 未加载")
            elif loaded[fam] and w not in loaded[fam]:
                issues.append(f"  {f.name}: '{fam}' weight {w} 未加载(只加载 {','.join(sorted(loaded[fam]))})")
    return issues


if __name__ == "__main__":
    d = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".")
    if not d.is_dir():
        print(f"[FAIL] 目录不存在: {d}")
        sys.exit(2)
    n_cards = len(list(d.glob("card-*.html")))
    issues = check(d)
    if issues:
        print(f"[FAIL] {len(issues)} 个字体问题:")
        for i in issues:
            print(i)
        sys.exit(1)
    else:
        print(f"[OK] {n_cards} 张卡,字体/字重与 link 加载一致")
        sys.exit(0)
