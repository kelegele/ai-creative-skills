#!/usr/bin/env python3
"""
screenshot.py — Playwright 截图工具(批量)
接收 HTML 文件路径列表,输出 PNG 截图。卡片 HTML 是固定 viewport(overflow:hidden),
用 full_page=False 按视口尺寸出图。

用 async API(而非 sync_api),规避 Python 3.14 + playwright sync_api 下
Greenlet.switch() returned NULL 的问题(同 gzh-illustration/scripts/screenshot.py 的教训)。
路径一律 resolve 成绝对 file:// URI(相对路径拼 file:// 会把首段当 host)。
"""
import argparse
import asyncio
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


async def _screenshot_all(html_files, output_dir: Path, width: int, height: int) -> list:
    from playwright.async_api import async_playwright

    output_dir.mkdir(parents=True, exist_ok=True)
    png_files = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            for html_path in html_files:
                url = html_path if html_path.startswith("file://") else Path(html_path).resolve().as_uri()
                page = await browser.new_page(viewport={"width": width, "height": height})
                await page.goto(url)
                await page.wait_for_load_state("networkidle")
                await page.evaluate("document.fonts.ready")
                await page.wait_for_timeout(300)
                png_name = Path(html_path).stem + ".png"
                png_path = output_dir / png_name
                await page.screenshot(path=str(png_path), full_page=False)
                png_files.append(str(png_path))
                print(f"  ✓ {png_name}")
                await page.close()
        finally:
            await browser.close()
    return png_files


def main():
    parser = argparse.ArgumentParser(description="Screenshot HTML files via Playwright")
    parser.add_argument("--files", nargs="+", required=True, help="HTML file paths")
    parser.add_argument("--output", required=True, help="Output directory for PNGs")
    parser.add_argument("--width", type=int, default=1080, help="Viewport width (default: 1080)")
    parser.add_argument("--height", type=int, default=1440, help="Viewport height (default: 1440)")
    args = parser.parse_args()
    try:
        png_files = asyncio.run(_screenshot_all(args.files, Path(args.output), args.width, args.height))
    except ImportError:
        print("ERROR: playwright not installed. Run:", file=sys.stderr)
        print("  uv add playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)
    print(f"\nDone: {len(png_files)} PNG → {args.output}")


if __name__ == "__main__":
    main()
