"""一次性本地重定向服务：访问时 Set-Cookie 写 _user_session（localhost 跨端口共享）再 302 跳业务页。

服务 detached 后台运行，不阻塞 bootstrap。
生命周期跟随 dev server：监测 dev server 端口，dev server 停了它就自动退出。
session 从环境变量 STAGING_HELPER_SESSION 读取（bootstrap 传入），不进 argv/ps。
"""

import http.server
import os
import socketserver
import sys
import threading
import time
from urllib.parse import urlparse

from common import COOKIE_NAME, port_listening

MAX_SECS = 28800  # 8 小时安全上限（正常靠 dev server 探活退出，不至于跑到这）


class _State:
    target_url = ""
    session = ""


class _Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header(
            "Set-Cookie",
            f"{COOKIE_NAME}={_State.session}; Path=/; Max-Age=15552000; SameSite=Lax",
        )
        self.send_header("Location", _State.target_url)
        self.end_headers()

    def log_message(self, *args):
        pass


class _Server(socketserver.TCPServer):
    allow_reuse_address = True


def serve(helper_port: int, target_url: str, session: str, max_secs: int = MAX_SECS) -> None:
    _State.target_url = target_url
    _State.session = session

    # 解析 dev server 端口（target_url 形如 http://localhost:3000/...）
    dev_port = urlparse(target_url).port

    httpd = _Server(("127.0.0.1", helper_port), _Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    # 跟随 dev server 生命周期：dev 端口不在监听就退出
    start = time.time()
    while time.time() - start < max_secs:
        if dev_port and not port_listening(int(dev_port)):
            break  # dev server 停了，跟着退
        time.sleep(2)
    httpd.shutdown()
    httpd.server_close()


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--serve" and len(args) >= 3:
        # --serve <helper_port> <target_url>；session 在 env STAGING_HELPER_SESSION
        session = os.environ.get("STAGING_HELPER_SESSION", "").strip()
        if not session:
            print("ERROR: 缺少 STAGING_HELPER_SESSION 环境变量", file=sys.stderr)
            sys.exit(1)
        serve(int(args[1]), args[2], session)
    else:
        print("usage: open_browser.py --serve <port> <url>（session 走 STAGING_HELPER_SESSION env）", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
