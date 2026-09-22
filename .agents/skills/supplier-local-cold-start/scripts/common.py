"""共享常量与工具：scripts/ 下所有脚本单源引用，防止路径漂移。

目录布局：
- 持久状态（session 缓存、凭据、微软 SSO profile、debug 截图）→ ~/.config/staging-local-dev/
  （/tmp 会被 macOS 定期清理，SSO 保险柜丢了会逼用户重新人工登录）
- dev server 进程记录与日志 → /tmp（运行时状态，重启自清）
- skill 的 venv 与安装 marker → ~/.config/supplier-local-cold-start/（由 setup.sh/run.sh 管理）
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

COOKIE_NAME = "_user_session"
STAGING_ORIGIN = "https://www.wlw-staging.de"

DATA_DIR = Path.home() / ".config" / "staging-local-dev"
SESSION_CACHE = DATA_DIR / "session"
CREDENTIALS_CACHE = DATA_DIR / "credentials.json"
PROFILE_DIR = DATA_DIR / "playwright-profile"
DEBUG_DIR = DATA_DIR / "debug"

LEGACY_DATA_DIR = Path("/tmp/staging-local-dev")  # 旧布局，首次运行自动迁移

TMP_DIR = Path("/tmp")
DEV_PIDS_PREFIX = "dev-pids-"
DEV_LOG_PREFIX = "staging-local-dev-"

EXIT_ERROR = 1
EXIT_NEED_EMAIL = 2
EXIT_NEED_PASSWORD = 3


def log(msg: str) -> None:
    print(f"[staging-local-dev] {msg}", file=sys.stderr)


def ensure_data_dir() -> Path:
    """确保持久数据目录存在；旧 /tmp 布局一次性搬迁（保住 SSO profile 与 session）。"""
    if LEGACY_DATA_DIR.exists() and not DATA_DIR.exists():
        try:
            DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(LEGACY_DATA_DIR), str(DATA_DIR))
        except Exception:
            pass  # 迁移失败不致命：最多重新登录一次
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def read_session_cache() -> Optional[str]:
    override = os.environ.get("STAGING_USER_SESSION", "").strip()
    if override:
        return override
    ensure_data_dir()
    if SESSION_CACHE.exists():
        v = SESSION_CACHE.read_text(encoding="utf-8").strip()
        if v:
            return v
    return None


def save_session_cache(value: str) -> None:
    ensure_data_dir()
    SESSION_CACHE.write_text(value, encoding="utf-8")
    SESSION_CACHE.chmod(0o600)


def clear_session_cache() -> None:
    SESSION_CACHE.unlink(missing_ok=True)


def port_listening(port: int) -> bool:
    """端口是否在监听。lsof 优先；不可用时回退 socket 连通（v4+v6，兼容 Nuxt 仅绑 ::1）。"""
    try:
        out = subprocess.check_output(
            ["lsof", "-ti", f":{port}", "-sTCP:LISTEN"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        if out:
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    import socket
    for fam, addr in ((socket.AF_INET, ("127.0.0.1", port)), (socket.AF_INET6, ("::1", port))):
        sock = socket.socket(fam, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            sock.connect(addr)
            sock.close()
            return True
        except OSError:
            try:
                sock.close()
            except OSError:
                pass
    return False


def pid_alive(pid) -> bool:
    try:
        os.kill(int(pid), 0)
        return True
    except (ProcessLookupError, ValueError, TypeError):
        return False
    except PermissionError:
        return True  # 进程存在但属别的用户


COOKIE_INTERCEPT_JS = (
    "const s=document.createElement('style');"
    "s.textContent='#cookiescript_injected_wrapper{display:none !important;pointer-events:none !important}';"
    "document.documentElement.appendChild(s);"
)


def disable_cookie_intercept(target) -> None:
    """注入 CSS 让 CookieScript 横幅不拦截鼠标事件（每次导航自动生效）。target: context 或 page。"""
    target.add_init_script(COOKIE_INTERCEPT_JS)
