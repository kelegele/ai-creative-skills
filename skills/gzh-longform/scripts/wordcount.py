#!/usr/bin/env python3
"""wordcount.py — 字数统计 + 结构标记检查(纯标准库)。

只统计正文(去 frontmatter / 参考来源 / 候选标题);检查结构标记(核心观点/参考来源/候选标题)。
不做禁用词检测(归 agent 自检)。

用法:uv run python wordcount.py <article.md> [--min 1500 --max 2000]
退出码:0 = 通过,1 = 字数越界或缺结构标记。
"""
import argparse
import re
import sys
from pathlib import Path


def _strip_frontmatter(text: str) -> str:
    """去掉 YAML frontmatter(--- ... ---)。"""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :]
    return text


def _strip_sections(text: str, headers: list) -> str:
    """从 `### 参考来源` / `### 候选标题` 等标题处起,删到文末或下一个同级标题。"""
    for h in headers:
        text = re.sub(rf"{re.escape(h)}.*?(?=\n### |\Z)", "", text, flags=re.S)
    return text


def _strip_markdown(text: str) -> str:
    """去 markdown 符号(# * ` - > | ①② 等),只留可读字。"""
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # 代码块
    text = re.sub(r"`[^`]*`", "", text)  # 行内代码
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # 图片
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)  # 链接
    text = re.sub(r"[#*`>\-|]", "", text)
    text = re.sub(r"^\s*\d+\.", "", text, flags=re.M)  # 有序列号
    return text


def count_words(text: str) -> int:
    """统计正文中文字符数(去 frontmatter/参考来源/候选标题/markdown 符号)。"""
    text = _strip_frontmatter(text)
    text = _strip_sections(text, ["### 参考来源", "### 候选标题"])
    text = _strip_markdown(text)
    chars = re.findall(r"[一-鿿぀-ヿA-Za-z0-9]", text)
    return len(chars)


def check_structure(text: str) -> list:
    """检查结构标记,返回缺失项列表(空 list = 通过)。"""
    missing = []
    if "核心观点" not in text:
        missing.append("缺'核心观点'标记")
    if "### 参考来源" not in text:
        missing.append("缺'参考来源'段")
    if "### 候选标题" not in text:
        missing.append("缺'候选标题'段")
    return missing


def main():
    parser = argparse.ArgumentParser(description="字数统计 + 结构标记检查")
    parser.add_argument("article", help="article.md 路径")
    parser.add_argument("--min", type=int, default=1500, help="最小字数(默认 1500)")
    parser.add_argument("--max", type=int, default=2000, help="最大字数(默认 2000)")
    args = parser.parse_args()

    text = Path(args.article).read_text(encoding="utf-8")
    n = count_words(text)
    missing = check_structure(text)

    print(f"字数:{n}")
    in_range = args.min <= n <= args.max
    print(f"区间:[{args.min}, {args.max}] {'✓' if in_range else '✗'}")
    if missing:
        for m in missing:
            print(f"  ✗ {m}")
    else:
        print("  结构标记:✓")
    sys.exit(0 if (in_range and not missing) else 1)


if __name__ == "__main__":
    main()
