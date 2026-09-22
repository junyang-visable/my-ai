#!/usr/bin/env python3
"""Minimal MCP Streamable HTTP client for mcp.atlassian.com (JSON-RPC over POST + SSE)."""
import json, sys, urllib.request, urllib.error

TOKEN_FILE = "/Users/yangjun/.mcp-auth/mcp-remote-v1/01910c24c5f2edcaf999bd1eaaeaeee8_tokens.json"
URL = "https://mcp.atlassian.com/v1/mcp"
PROTO = "2025-03-26"

tok = json.load(open(TOKEN_FILE))["access_token"]
session = None
_next_id = [0]


def post(payload):
    global session
    body = json.dumps(payload).encode()
    req = urllib.request.Request(URL, data=body, method="POST", headers={
        "Authorization": f"Bearer {tok}",
        "User-Agent": "node-fetch",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": PROTO,
        **({"Mcp-Session-Id": session} if session else {}),
    })
    try:
        resp = urllib.request.urlopen(req, timeout=60)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read()[:500].decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)
    sid = resp.headers.get("Mcp-Session-Id")
    if sid:
        session = sid
    ctype = resp.headers.get("Content-Type", "")
    raw = resp.read().decode()
    if "text/event-stream" in ctype:
        for line in raw.splitlines():
            if line.startswith("data:"):
                data = line[5:].strip()
                if data and data != "[DONE]":
                    return json.loads(data)
        return None
    return json.loads(raw) if raw.strip() else None


def rpc(method, params=None, notify=False):
    if notify:
        return post({"jsonrpc": "2.0", "method": method, "params": params or {}})
    _next_id[0] += 1
    return post({"jsonrpc": "2.0", "id": _next_id[0], "method": method, "params": params or {}})


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    init = rpc("initialize", {
        "protocolVersion": PROTO,
        "capabilities": {},
        "clientInfo": {"name": "qoder-direct", "version": "1.0"},
    })
    if init and "error" in init:
        print(json.dumps(init, indent=2)[:2000]); sys.exit(1)
    rpc("notifications/initialized", {}, notify=True)

    if cmd == "list":
        res = rpc("tools/list", {})
        for t in res["result"]["tools"]:
            print(t["name"], "|", (t.get("description") or "")[:110].replace("\n", " "))
    elif cmd == "schema":
        res = rpc("tools/list", {})
        for t in res["result"]["tools"]:
            if t["name"] in sys.argv[2].split(","):
                print("===", t["name"])
                print(json.dumps(t.get("inputSchema", {}), indent=1, ensure_ascii=False)[:2500])
    elif cmd == "call":
        name, args = sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        res = rpc("tools/call", {"name": name, "arguments": args})
        print(json.dumps(res, indent=2, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
