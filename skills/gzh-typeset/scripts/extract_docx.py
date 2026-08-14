#!/usr/bin/env python3
"""docx 文本提取(docx → 纯文本段落列表)。

docx 本质是 zip,正文在 word/document.xml。本脚本用纯 stdlib(zipfile + re)提取段落,
供 format-normalize 流程把 Word 文档转成 Markdown 草稿。不依赖 python-docx。

用法:
    uv run python extract_docx.py <file.docx> [--out out.md]

输出:每个段落一行(含标题层级推断,见 --headings)。无 --out 时打印到 stdout。
"""
import argparse
import re
import sys
import zipfile
from xml.sax.saxutils import unescape


NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract_paragraphs(docx_path: str) -> list:
    """返回 [(text, style_or_None)],style 是该段落 w:pStyle 的 val(如 Heading1)。"""
    with zipfile.ZipFile(docx_path) as z:
        names = [n for n in z.namelist() if n.endswith("document.xml")]
        if not names:
            raise ValueError("docx 里没有 word/document.xml,可能不是有效 Word 文档")
        xml = z.read(names[0]).decode("utf-8", errors="replace")

    paras = []
    # 按 <w:p ...>...</w:p> 切段落
    for pm in re.finditer(r"<w:p\b[^>]*>.*?</w:p>", xml, re.S):
        p_xml = pm.group(0)
        # 段落样式(标题)
        style = None
        sm = re.search(rf"<w:pStyle w:val=\"([^\"]+)\"", p_xml)
        if sm:
            style = sm.group(1)
        # 文本:取所有 <w:t> 内容
        texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p_xml, re.S)
        text = unescape("".join(texts)).strip()
        paras.append((text, style))
    return paras


def style_to_md_prefix(style: str) -> str:
    """把 Word 标题样式映射到 Markdown 前缀(仅推断,正文段落无前缀)。"""
    if not style:
        return ""
    s = style.lower()
    if "heading1" in s or "title" in s:
        return "# "
    if "heading2" in s:
        return "## "
    if "heading3" in s:
        return "### "
    return ""


def main():
    ap = argparse.ArgumentParser(description="docx 文本提取")
    ap.add_argument("file", help=".docx 文件")
    ap.add_argument("--out", help="输出 .md 路径(缺省打印 stdout)")
    ap.add_argument("--headings", action="store_true", help="按 Word 标题样式加 Markdown # 前缀")
    args = ap.parse_args()

    try:
        paras = extract_paragraphs(args.file)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    lines = []
    for text, style in paras:
        if not text:
            continue
        prefix = style_to_md_prefix(style) if args.headings else ""
        lines.append(prefix + text)

    out = "\n\n".join(lines) if args.headings else "\n".join(lines)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
        print(f"OK 写 {len(lines)} 段 → {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
