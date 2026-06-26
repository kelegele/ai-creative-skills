#!/usr/bin/env python3
"""screenshot.py — Playwright 截图(独立,不依赖 text-to-card)。

用法:python screenshot.py <html文件> <输出png> [--width 1080] [--watermark 飞栗.ai]
行为:打开 file://,等字体加载,按 body 内容高度截图(deviceScaleFactor 2),可选加品牌水印。
退出码:0 = 成功,1 = 失败。

用 async API(而非 sync_api),规避 greenlet 在 Python 3.14 +
playwright sync_api 下 Greenlet.switch() returned NULL 的问题。
水印文本由调用方传(项目级品牌),skill 不写死。
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


async def _screenshot_async(html_path: str, png_path: str, width: int, watermark: str = "") -> None:
    from playwright.async_api import async_playwright
    url = html_path if html_path.startswith("file://") else Path(html_path).resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            page = await browser.new_page(
                viewport={"width": width, "height": 800},
                device_scale_factor=2,
            )
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(300)
            if watermark:
                await page.evaluate(
                    """(txt) => {
                        document.body.style.position = 'relative';
                        const w = document.createElement('div');
                        w.id = '__wm';
                        w.textContent = txt;
                        w.style.cssText =
                            'position:absolute;right:36px;bottom:26px;font-size:22px;' +
                            'color:#9CA3AF;font-family:Noto Sans SC,Manrope,sans-serif;' +
                            'font-weight:600;letter-spacing:1.5px;pointer-events:none;z-index:9999;';
                        document.body.appendChild(w);
                    }""",
                    watermark,
                )
                await page.wait_for_timeout(100)
            height = await page.evaluate(
                "Math.max(document.body.scrollHeight,"
                "  (document.getElementById('__wm')||{getBoundingClientRect:()=>({bottom:0})})"
                "    .getBoundingClientRect().bottom)"
            )
            Path(png_path).parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=png_path, clip={"x": 0, "y": 0, "width": width, "height": height})
        finally:
            await browser.close()
    print(f"✓ {png_path}")


def screenshot(html_path: str, png_path: str, width: int = 1080, watermark: str = "") -> None:
    try:
        asyncio.run(_screenshot_async(html_path, png_path, width, watermark))
    except ImportError:
        print("ERROR: playwright 未安装。运行:", file=sys.stderr)
        print("  uv add playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Playwright 截图")
    parser.add_argument("html", help="HTML 文件路径")
    parser.add_argument("png", help="输出 PNG 路径")
    parser.add_argument("--width", type=int, default=1080, help="viewport 宽(默认 1080)")
    parser.add_argument("--watermark", default="", help="品牌水印文本(由项目传,如 飞栗.ai);不传则不加水印")
    args = parser.parse_args()
    screenshot(args.html, args.png, args.width, args.watermark)


if __name__ == "__main__":
    main()
