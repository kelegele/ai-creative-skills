#!/usr/bin/env python3
"""wechat.html 本地预览包装。

公众号 HTML 全 inline 样式,直接浏览器打开会贴满整屏(无页面容器)。本脚本在 HTML 的 head
里注入一段"本地预览容器"样式(仅本地浏览器看,不影响复制粘贴公众号——公众号只认 inline)。
等价于 gzh-typeset 样式规范里的「本地预览容器」,做成命令方便复用。

用法:
    uv run python wrap_preview.py <wechat.html> [--width 680] [--out preview.html]

不改正文 HTML,只在 head 注入 <style> 预览样式。默认就地覆盖,或 --out 输出副本。
"""
import argparse
import re
import sys


PREVIEW_CSS = (
    "body{{font-family:-apple-system,\"PingFang SC\",\"Microsoft YaHei\",sans-serif;"
    "max-width:{width}px;margin:40px auto;padding:0 24px;background:#fff;}}"
    "img{{max-width:100%;height:auto;}}"
)


def main():
    ap = argparse.ArgumentParser(description="本地预览容器包装")
    ap.add_argument("file", help="wechat.html 路径")
    ap.add_argument("--width", type=int, default=680, help="预览容器宽度(px)")
    ap.add_argument("--out", help="输出路径(缺省就地覆盖)")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as f:
        html = f.read()

    # 幂等:已有预览容器则不重复注入
    if "wrap_preview" in html:
        print("已存在预览容器,跳过")
        return 0

    css = PREVIEW_CSS.format(width=args.width)
    if "<head>" in html:
        html = html.replace("<head>", f"<head>\n<!-- wrap_preview 本地预览容器,不影响粘贴 -->\n<style>{css}</style>", 1)
    else:
        html = f"<html><head><style>{css}</style></head>\n{html}\n</html>"

    out = args.out or args.file
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK 预览容器已注入 → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
