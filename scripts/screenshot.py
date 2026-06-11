#!/usr/bin/env python3
"""
screenshot.py — Playwright 截图工具
接收 HTML 文件路径列表，输出 PNG 截图
"""
import argparse
import sys
from pathlib import Path


def screenshot(html_files: list, output_dir: str, width: int = 1080, height: int = 1440):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run:", file=sys.stderr)
        print("  pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    png_files = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html_path in html_files:
            html_path = str(html_path)
            if not html_path.startswith("file://"):
                html_path = f"file://{html_path}"
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(html_path)
            page.wait_for_load_state("networkidle")
            png_name = Path(html_path).stem + ".png"
            png_path = output_dir / png_name
            page.screenshot(path=str(png_path), full_page=False)
            png_files.append(str(png_path))
            print(f"  ✓ {png_name}")
        browser.close()

    print(f"\nDone: {len(png_files)} PNG → {output_dir}")
    return png_files


def main():
    parser = argparse.ArgumentParser(description="Screenshot HTML files via Playwright")
    parser.add_argument("--files", nargs="+", required=True, help="HTML file paths")
    parser.add_argument("--output", required=True, help="Output directory for PNGs")
    parser.add_argument("--width", type=int, default=1080, help="Viewport width (default: 1080)")
    parser.add_argument("--height", type=int, default=1440, help="Viewport height (default: 1440)")
    args = parser.parse_args()
    screenshot(args.files, args.output, args.width, args.height)


if __name__ == "__main__":
    main()
