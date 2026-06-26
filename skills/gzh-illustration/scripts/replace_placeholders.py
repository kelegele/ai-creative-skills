#!/usr/bin/env python3
"""replace_placeholders.py — 占位回填(草稿/定版两态)。纯标准库。

用法:
  uv run python replace_placeholders.py <article.md> --mode draft
  uv run python replace_placeholders.py <article.md> --mode final

草稿态:占位块下方插入图片,保留占位描述。
定版态:删除所有 🖼️ 占位块,只留图片。运行前备份 article.md.bak。
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

# 占位块正则:> 🖼️ 【序号 · 尺寸 · 来源】描述
PLACEHOLDER_RE = re.compile(
    r"^> 🖼️ 【([^·]+?)·\s*([^·】]+?)(?:·\s*([^】]+?))?】(.*)$",
    re.M,
)


def parse_placeholders(text: str) -> list:
    """解析所有占位块,返回 list[dict(seq,size,source,desc,line)]。"""
    phs = []
    for m in PLACEHOLDER_RE.finditer(text):
        phs.append({
            "seq": m.group(1).strip(),
            "size": m.group(2).strip(),
            "source": (m.group(3) or "").strip() or "生成",
            "desc": m.group(4).strip(),
            "line": m.group(0),
        })
    return phs


def _image_path_for(ph: dict) -> str:
    """生成图用 images/gzh-imaget-{seq}.png;自供图用 desc 里的路径。"""
    if ph["source"] == "自供":
        return ph["desc"]
    return f"images/gzh-imaget-{ph['seq']}.png"


def _image_md(ph: dict) -> str:
    """生成 ![desc](path) 行。自供图 desc 即路径,作 alt。"""
    path = _image_path_for(ph)
    alt = ph["desc"] if ph["source"] == "自供" else ph["seq"]
    return f"![{alt}]({path})"


def replace_draft(text: str, phs: list) -> str:
    """草稿态:每个占位块下方插入图片行,保留占位块。"""
    for ph in phs:
        img_line = _image_md(ph)
        if img_line in text:
            continue
        text = text.replace(ph["line"], ph["line"] + "\n\n" + img_line, 1)
    return text


def replace_final(text: str) -> str:
    """定版态:删除所有 🖼️ 占位块(整行),保留图片行。"""
    return PLACEHOLDER_RE.sub("", text)


def _clean_blank_lines(text: str) -> str:
    """清理删除后多余空行(3+ 连续空行压成 2)。"""
    return re.sub(r"\n{3,}", "\n\n", text)


def main():
    parser = argparse.ArgumentParser(description="占位回填(草稿/定版)")
    parser.add_argument("article", help="article.md 路径")
    parser.add_argument("--mode", choices=["draft", "final"], required=True)
    args = parser.parse_args()

    path = Path(args.article)
    text = path.read_text(encoding="utf-8")
    phs = parse_placeholders(text)

    gen = sum(1 for p in phs if p["source"] != "自供")
    sup = len(phs) - gen
    print(f"将处理 {len(phs)} 处占位({gen} 生成 / {sup} 自供),mode={args.mode}")
    sys.stdout.write("回车继续: ")
    sys.stdout.flush()
    input()

    if args.mode == "draft":
        result = replace_draft(text, phs)
    else:
        backup = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, backup)
        print(f"已备份 → {backup}")
        result = replace_final(text)
        result = _clean_blank_lines(result)

    path.write_text(result, encoding="utf-8")
    print(f"✓ 已写回 {path}")


if __name__ == "__main__":
    main()
