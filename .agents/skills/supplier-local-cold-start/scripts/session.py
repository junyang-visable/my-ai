"""获取 staging _user_session。

visable 账号走微软 SSO，故登录分两种模式：

- 默认 headless（静默续期）：从持久 profile（微软 cookie 保险柜）读出微软会话 cookie，
  注入全新 context，走 registration→Continue→Log in→微软 SSO 自动完成→抓 _user_session。
  全程无交互。仅当 _user_session 过期、而微软会话仍有效时用这条。
- --headed（首次 / 微软会话也过期时）：用持久 profile 开可见 Chrome，用户手动完成一次微软登录。
  登录后微软会话落盘到 profile（保险柜），_user_session 落盘到文件缓存。

全新 context 避免持久 profile 累积的注册表单 disabled 状态。运行依赖由 setup.sh 预装。
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

from common import (
    COOKIE_NAME,
    CREDENTIALS_CACHE,
    DATA_DIR,
    DEBUG_DIR,
    EXIT_ERROR,
    EXIT_NEED_EMAIL,
    EXIT_NEED_PASSWORD,
    PROFILE_DIR,
    STAGING_ORIGIN,
    disable_cookie_intercept,
    log,
    read_session_cache,
    save_session_cache,
)

REGISTRATION_URL = f"{STAGING_ORIGIN}/en/registration"
MS_HOST = "login.microsoftonline.com"
SCRIPTS_DIR = Path(__file__).resolve().parent

EXIT_OK = 0

EMAIL_SELECTORS = ["input[type='email']", "input[name='email']", "input#email", "input[autocomplete='email']"]
PASSWORD_SELECTORS = ["input[type='password']", "input[name='password']", "input#password", "input[autocomplete='current-password']"]
COOKIE_ACCEPT_SELECTORS = [
    "#cookiescript_accept", "button#cookiescript_accept",
    "#cookiescript_injected_wrapper button.btn-primary",
    "#cookiescript_injected_wrapper button[type='button']",
    "button:has-text('Accept')", "button:has-text('Accept all')",
    "button:has-text('Zustimmen')", "button:has-text('Alle akzeptieren')",
]


def _load_app_env() -> None:
    """加载应用 .env（凭据可放此，已被 .gitignore 忽略，不进 git）。

    仅填充 os.environ 中尚未设置的键，不覆盖已有环境变量；无第三方依赖。
    优先级：.env.local > .env；在 cwd（agent 跑脚本时的项目根）查找。
    """
    roots = [Path.cwd()]  # agent 在项目根目录跑，.env 就在这里
    seen: set = set()
    for root in roots:
        for name in (".env.local", ".env"):  # .env.local 先加载 → 优先级更高
            p = root / name
            if not p.exists() or p in seen:
                continue
            seen.add(p)
            try:
                for raw in p.read_text(encoding="utf-8").splitlines():
                    line = raw.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, _, v = line.partition("=")
                    k = k.strip()
                    v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                        v = v[1:-1]
                    if k and k not in os.environ:
                        os.environ[k] = v
            except Exception:
                pass


_load_app_env()


def require_playwright() -> None:
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("ERROR: playwright 未安装。请先运行：bash scripts/setup.sh", file=sys.stderr)
        sys.exit(EXIT_ERROR)


def read_credentials() -> dict:
    if CREDENTIALS_CACHE.exists():
        try:
            return json.loads(CREDENTIALS_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_credentials(email: Optional[str], password: Optional[str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing = read_credentials()
    if email:
        existing["email"] = email
    if password is not None:
        existing["password"] = password
    CREDENTIALS_CACHE.write_text(json.dumps(existing), encoding="utf-8")
    CREDENTIALS_CACHE.chmod(0o600)


def find_session(cookies: list) -> Optional[str]:
    for c in cookies:
        if c.get("name") == COOKIE_NAME and c.get("value"):
            return c["value"]
    return None


def has_ms_session(cookies: list) -> bool:
    return any(MS_HOST in (c.get("domain", "") or "") or "microsoftonline" in (c.get("domain", "") or "") for c in cookies)


def dismiss_cookie_banner(page) -> None:
    """CookieScript 的接受按钮是 div#cookiescript_accept。等横幅注入出现再点；无横幅则快退。"""
    wrapper = page.locator("#cookiescript_injected_wrapper")
    try:
        wrapper.first.wait_for(state="visible", timeout=2000)
    except Exception:
        return  # 该页无 cookie 横幅
    for sel in ("#cookiescript_accept",):
        loc = page.locator(sel)
        try:
            if loc.count() == 0:
                continue
            loc.first.click(timeout=3000)
            page.wait_for_timeout(500)
            return
        except Exception:
            continue
    # 兜底：其它形态的接受按钮
    for sel in COOKIE_ACCEPT_SELECTORS:
        loc = page.locator(sel)
        try:
            if loc.count() == 0:
                continue
            if loc.first.is_visible(timeout=1500):
                loc.first.click(timeout=3000)
                page.wait_for_timeout(500)
                return
        except Exception:
            continue


def type_first_visible(page, selectors: list[str], value: str) -> bool:
    """wlw 用 Vue 自定义输入组件，fill() 不触发响应式，必须用 press_sequentially 逐字符输入。"""
    for sel in selectors:
        loc = page.locator(sel)
        try:
            if loc.count() == 0:
                continue
            field = loc.first
            if field.is_visible(timeout=2000):
                try:
                    field.click()
                except Exception:
                    pass
                page.wait_for_timeout(200)
                field.press_sequentially(value, delay=30)
                return True
        except Exception:
            continue
    return False


def password_field_visible(page) -> bool:
    for sel in PASSWORD_SELECTORS:
        loc = page.locator(sel)
        try:
            if loc.count() == 0:
                continue
            if loc.first.is_visible(timeout=1500):
                return True
        except Exception:
            continue
    return False


def click_submit(page, label: Optional[str] = None) -> None:
    """点提交按钮。用 JS el.click() 直接触发，绕过 CookieScript 横幅对鼠标事件的拦截（确定性最高）。"""
    target = page.locator("button[type='submit']")
    if label:
        target = target.filter(has_text=label)
    try:
        target.first.evaluate("el => el.click()")
        return
    except Exception:
        pass
    try:
        page.locator("button[type='submit']").first.evaluate("el => el.click()")
    except Exception:
        pass


def dump_debug(page, tag: str) -> None:
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(DEBUG_DIR / f"{tag}.png"), full_page=True)
    except Exception:
        pass
    try:
        (DEBUG_DIR / f"{tag}.url").write_text(page.url, encoding="utf-8")
    except Exception:
        pass


class FlowResult:
    def __init__(self, session: Optional[str] = None, ms_wall: bool = False, need_password: bool = False, no_email: bool = False):
        self.session = session
        self.ms_wall = ms_wall
        self.need_password = need_password
        self.no_email = no_email


def run_login_flow(page, context, email: str, password: Optional[str], wait_secs: int, headed: bool = False) -> FlowResult:
    try:
        for attempt in range(3):
            try:
                page.goto(REGISTRATION_URL, wait_until="domcontentloaded", timeout=60000)
                break
            except Exception as e:
                # 重定向/profile 恢复可能触发 ERR_ABORTED，页面其实已加载，重试
                log(f"goto 第{attempt + 1}次: {str(e)[:80]}")
                if attempt == 2:
                    raise
                page.wait_for_timeout(1000)
        dismiss_cookie_banner(page)
        try:
            page.wait_for_selector("input[type='email']", state="visible", timeout=15000)
        except Exception:
            pass

        if not type_first_visible(page, EMAIL_SELECTORS, email):
            dump_debug(page, "no-email-field")
            log("未找到邮箱输入框，见 debug/no-email-field.*")
            return FlowResult(no_email=True)

        click_submit(page, "Continue")
        try:
            page.wait_for_url("**/en/login?flow=*", timeout=60000)
        except Exception:
            dump_debug(page, "after-continue")
            log("Continue 后未跳转到 login，见 debug/after-continue.*")
            return FlowResult()
        dismiss_cookie_banner(page)
        # 等 Log in 按钮就绪（替代 networkidle，后者因持续网络请求会耗满 15s）
        try:
            page.locator("button[type='submit']").filter(has_text="Log in").first.wait_for(state="visible", timeout=10000)
        except Exception:
            pass

        if password_field_visible(page):
            if not password:
                dump_debug(page, "need-password")
                return FlowResult(need_password=True)
            type_first_visible(page, PASSWORD_SELECTORS, password or "")

        click_submit(page, "Log in")

        # 等 _user_session。
        # headless：若撞微软登录墙（微软会话失效），快速判定 NEED_HEADED。
        # headed：用户要在微软页完成登录，给足时间，不中止。
        session = None
        ms_wall = False
        deadline = time.time() + wait_secs
        while time.time() < deadline:
            session = find_session(context.cookies())
            if session:
                break
            if not headed:
                url = page.url or ""
                if MS_HOST in url:
                    page.wait_for_timeout(4000)
                    if MS_HOST in (page.url or ""):
                        ms_wall = True
                        break
            page.wait_for_timeout(500)
        return FlowResult(session=session, ms_wall=ms_wall)
    except Exception as exc:
        dump_debug(page, "login-exception")
        log(f"登录异常: {exc}，见 debug/login-exception.*")
        return FlowResult()


MS_DOMAIN_HINTS = ("microsoft", "msauth", "windows.net", "live.com", "msn.com")


def is_ms_cookie(c: dict) -> bool:
    d = (c.get("domain") or "").lower()
    return any(h in d for h in MS_DOMAIN_HINTS)


def read_vault_cookies() -> list:
    """从持久 profile 读出微软会话 cookie（保险柜）。无 profile / 无 cookie 返回 []。"""
    require_playwright()
    if not PROFILE_DIR.exists():
        return []
    from playwright.sync_api import sync_playwright
    cookies = []
    with sync_playwright() as p:
        try:
            ctx = p.chromium.launch_persistent_context(str(PROFILE_DIR), headless=True, channel="chrome",
                                                       args=["--disable-blink-features=AutomationControlled"])
            cookies = ctx.cookies()
            ctx.close()
        except Exception:
            try:
                ctx = p.chromium.launch_persistent_context(str(PROFILE_DIR), headless=True,
                                                           args=["--disable-blink-features=AutomationControlled"])
                cookies = ctx.cookies()
                ctx.close()
            except Exception:
                return []
    return cookies


def is_visable_email(email: Optional[str]) -> bool:
    """visable 内部邮箱走微软 SSO（免密）；其它域名走密码登录。按邮箱域名判定。"""
    if not email or "@" not in email:
        return False
    return "visable" in email.rsplit("@", 1)[-1].lower()


def login_headed(email: str, password: Optional[str]) -> FlowResult:
    """用持久 profile 开可见 Chrome，用户完成登录（visable 的微软 SSO，或非 visable 的密码登录）。"""
    require_playwright()
    from playwright.sync_api import sync_playwright
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        try:
            ctx = p.chromium.launch_persistent_context(str(PROFILE_DIR), headless=False, channel="chrome",
                                                        args=["--disable-blink-features=AutomationControlled"])
        except Exception:
            ctx = p.chromium.launch_persistent_context(str(PROFILE_DIR), headless=False,
                                                        args=["--disable-blink-features=AutomationControlled"])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        disable_cookie_intercept(ctx)
        log("已打开可见浏览器，请在登录页完成登录（最多等 5 分钟）...")
        result = run_login_flow(page, ctx, email, password, wait_secs=300, headed=True)
        if not result.session and not result.ms_wall:
            dump_debug(page, "headed-no-session")
        ctx.close()
        return result


def login_headless(email: str, password: Optional[str]) -> FlowResult:
    """headless 登录：注入保险柜微软 cookie（若有）。visable 有微软会话则 SSO 自动续期；非 visable 走密码登录。"""
    require_playwright()
    from playwright.sync_api import sync_playwright
    vault = read_vault_cookies()
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True, channel="chrome", args=["--disable-blink-features=AutomationControlled"])
        except Exception:
            browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context()
        disable_cookie_intercept(ctx)
        ms_cookies = [c for c in vault if is_ms_cookie(c)]
        if ms_cookies:
            try:
                ctx.add_cookies(ms_cookies)
            except Exception:
                pass
        page = ctx.new_page()
        result = run_login_flow(page, ctx, email, password, wait_secs=25, headed=False)
        if not result.session:
            dump_debug(page, "headless-no-session")
        ctx.close()
        browser.close()
        return result


def resolve(email: Optional[str], password: Optional[str], headed: bool) -> str:
    cached = read_credentials()
    email = (email or os.environ.get("STAGING_EMAIL") or cached.get("email") or "").strip() or None
    password = (password if password is not None else (os.environ.get("STAGING_PASSWORD") or cached.get("password")))
    password = (password or "").strip() or None
    if email:
        save_credentials(email, None)

    if not email:
        print("NEED_EMAIL", file=sys.stderr)
        sys.exit(EXIT_NEED_EMAIL)

    is_vis = is_visable_email(email)

    if headed:
        result = login_headed(email, password)
    elif is_vis:
        # visable：有微软会话→headless 续期；无（首次/过期）→直接开浏览器，不再先 headless 试探
        if has_ms_session(read_vault_cookies()):
            result = login_headless(email, password)
            if not result.session and result.ms_wall:
                result = login_headed(email, password)
        else:
            result = login_headed(email, password)
    else:
        # 非 visable：密码登录，headless 即可
        result = login_headless(email, password)

    if result.need_password:
        print("NEED_PASSWORD: 该非 visable 邮箱需要密码登录", file=sys.stderr)
        sys.exit(EXIT_NEED_PASSWORD)
    if not result.session:
        print("ERROR: 无法获取 _user_session，见 debug/", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    save_credentials(email, password)
    save_session_cache(result.session)
    return result.session


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email")
    parser.add_argument("--password")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()

    if not args.refresh:
        cached = read_session_cache()
        if cached:
            print(cached)
            return

    session = resolve(
        email=(args.email or "").strip() or None,
        password=(args.password or "").strip() or None,
        headed=args.headed,
    )
    print(session)


if __name__ == "__main__":
    main()
