#!/usr/bin/env python3
"""screenshot.py — Playwright 截图(独立,不依赖 text-to-card)。

用法:uv run python screenshot.py <html文件> <输出png> [--width 1080]
行为:打开 file://,等字体加载,full_page 截图(高度自适应),deviceScaleFactor 2。
退出码:0 = 成功,1 = 失败。
"""
import argparse
import sys
from pathlib import Path


def screenshot(html_path: str, png_path: str, width: int = 1080) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright 未安装。运行:", file=sys.stderr)
        print("  uv add playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    url = html_path if html_path.startswith("file://") else f"file://{html_path}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": 800},
            device_scale_factor=2,
        )
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)
        Path(png_path).parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=png_path, full_page=True)
        browser.close()
    print(f"✓ {png_path}")


def main():
    parser = argparse.ArgumentParser(description="Playwright 截图")
    parser.add_argument("html", help="HTML 文件路径")
    parser.add_argument("png", help="输出 PNG 路径")
    parser.add_argument("--width", type=int, default=1080, help="viewport 宽(默认 1080)")
    args = parser.parse_args()
    screenshot(args.html, args.png, args.width)


if __name__ == "__main__":
    main()
