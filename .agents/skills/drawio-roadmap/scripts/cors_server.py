#!/usr/bin/env python3
"""drawio 验证用 CORS server：8123 端口，多线程，serve 启动时的工作目录

从工作区根启动（verify.html 用绝对路径 /tmp-verify.drawio 取文件）：
    python3 .agents/skills/drawio-roadmap/scripts/cors_server.py
"""
import http.server
import socketserver


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


if __name__ == '__main__':
    ThreadingServer(('127.0.0.1', 8123), Handler).serve_forever()
