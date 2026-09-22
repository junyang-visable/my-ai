"""让 agent 检视运行中的业务页。

默认用 Playwright headless 渲染（支持 --click 交互）。--fast 模式用 curl 直取 SSR HTML（毫秒级，不支持交互）。
用缓存的 _user_session cookie。不碰 dev server、不重启。

用法：
  python3 view_page.py <url>                       # Playwright 渲染，输出可见文本
  python3 view_page.py <url> --fast                # curl 快速读 SSR 文本
  python3 view_page.py <url> --click "button.x"    # 点击后再读
  python3 view_page.py <url> --screenshot /tmp/p.png
  python3 view_page.py <url> --html
"""

import argparse
import re
import subprocess
import sys
import time

from common import COOKIE_NAME, disable_cookie_intercept, read_session_cache


def strip_html_tags(html: str) -> str:
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html).strip()


def fast_fetch(url: str, session: str) -> str:
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "10",
         "-H", f"Cookie: {COOKIE_NAME}={session}", url],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return ""
    html = result.stdout
    if not html or '<div id="__nuxt"></div>' in html or '<div id="app"></div>' in html:
        return ""
    return strip_html_tags(html)


def playwright_render(url: str, session: str, args) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright 未安装。先跑 setup.sh", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(headless=True, channel="chrome")
        except Exception:
            browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context()
        expires = int(time.time()) + 15552000
        # localhost 与 127.0.0.1 都发一份，URL 用哪种写法都能带 cookie
        ctx.add_cookies([
            {"name": COOKIE_NAME, "value": session, "domain": "localhost", "path": "/", "expires": expires},
            {"name": COOKIE_NAME, "value": session, "domain": "127.0.0.1", "path": "/", "expires": expires},
        ])
        page = ctx.new_page()
        disable_cookie_intercept(page)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=args.timeout * 1000)
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            if args.click:
                try:
                    page.click(args.click, timeout=5000)
                    time.sleep(1)
                    try:
                        page.wait_for_load_state("networkidle", timeout=10000)
                    except Exception:
                        pass
                except Exception as e:
                    print(f"[view_page] 点击失败: {e}", file=sys.stderr)
            if args.screenshot:
                page.screenshot(path=args.screenshot, full_page=True)
                print(f"[view_page] 截图: {args.screenshot}", file=sys.stderr)
            if args.html:
                print(page.content())
            else:
                print(page.inner_text("body"))
        except Exception as e:
            print(f"ERROR: 渲染失败: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            ctx.close()
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="要检视的页面 URL")
    parser.add_argument("--screenshot", metavar="PATH", help="存整页截图")
    parser.add_argument("--html", action="store_true", help="输出渲染后 HTML")
    parser.add_argument("--fast", action="store_true", help="curl 快速模式（SSR，不支持交互）")
    parser.add_argument("--click", metavar="SELECTOR", help="点击指定元素后再读内容")
    parser.add_argument("--timeout", type=int, default=60, help="页面加载超时秒数")
    args = parser.parse_args()

    session = read_session_cache()
    if not session:
        print("ERROR: 无 _user_session 缓存。先跑 bootstrap.py 完成登录。", file=sys.stderr)
        sys.exit(1)

    if args.fast and not args.screenshot and not args.html and not args.click:
        text = fast_fetch(args.url, session)
        if text:
            print(text)
            return
        print("[view_page] fast 模式无内容（可能是 SPA），降级到 Playwright", file=sys.stderr)

    playwright_render(args.url, session, args)


if __name__ == "__main__":
    main()
