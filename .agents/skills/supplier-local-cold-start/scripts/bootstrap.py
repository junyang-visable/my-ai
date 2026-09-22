"""Staging 本地调试一键启动（Python）。"""

import argparse
import collections
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

from common import (
    COOKIE_NAME,
    DEV_LOG_PREFIX,
    DEV_PIDS_PREFIX,
    EXIT_NEED_EMAIL,
    EXIT_NEED_PASSWORD,
    STAGING_ORIGIN,
    TMP_DIR,
    clear_session_cache,
    log,
    pid_alive,
    port_listening,
    read_session_cache,
)

PORT_DEFAULT = 3000
PORT_MAX = 3020
SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPTS_DIR.parent
PROJECTS_JSON = SKILL_ROOT / "projects.json"

LOCKFILE_NAMES = ("pnpm-lock.yaml", "yarn.lock", "package-lock.json")
INSTALL_STAMP = ".supplier-local-cold-start"
INSTALL_HEARTBEAT_SECS = 30


def fail(msg: str, code: int = 1) -> None:
    print(f"[staging-local-dev] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


# ---------- node/yarn 解析（自包含，不依赖调用方 shell 的 PATH） ----------


def _ver_key(d: Path) -> tuple:
    """把 v24.19.0 解析成 (24,19,0) 用于数字排序（字母序会让 v18>v24）。"""
    import re
    m = re.match(r"v?(\d+)(?:\.(\d+))?(?:\.(\d+))?", d.name)
    if not m:
        return (0, 0, 0)
    return tuple(int(g) if g else 0 for g in m.groups())


def _nvm_versions_dir() -> Path:
    """尊重 $NVM_DIR（默认 ~/.nvm），不写死。"""
    return Path(os.environ.get("NVM_DIR", Path.home() / ".nvm")) / "versions" / "node"


def _nvm_default_version() -> str:
    """读 nvm 的 default 别名文件（nvm alias default <ver> 后落盘）。"""
    nvm_dir = Path(os.environ.get("NVM_DIR", Path.home() / ".nvm"))
    alias = nvm_dir / "alias" / "default"
    if alias.exists():
        v = alias.read_text(encoding="utf-8").strip()
        if v:
            return v
    return ""


def _nvmrc_version() -> str:
    """读项目 .nvmrc 指定的版本（可能是 24 / 24.19.0 / lts/*）。"""
    rc = Path.cwd() / ".nvmrc"
    if rc.exists():
        v = rc.read_text(encoding="utf-8").strip()
        if v:
            return v
    return ""


def _match_nvm_version(versions: "list[Path]", want: str) -> "Optional[Path]":
    """从已装版本里找匹配 want 的（支持前缀匹配，如 .nvmrc 写 24 匹配 v24.19.0）。"""
    if not want:
        return None
    want = want.lstrip("v")
    # 精确匹配
    for d in versions:
        if d.name.lstrip("v") == want:
            return d
    # 前缀匹配（.nvmrc=24 → v24.x.x）
    for d in sorted(versions, key=_ver_key, reverse=True):
        if d.name.lstrip("v").startswith(want):
            return d
    return None


def _node_bin_candidates() -> list[str]:
    """常见 node/yarn 安装位置，按优先级。nvm 读 $NVM_DIR + default 别名 + .nvmrc。"""
    out: list[str] = []
    nvm_root = _nvm_versions_dir()
    if nvm_root.exists():
        versions = [d for d in nvm_root.iterdir() if d.is_dir()]
        # 优先级：.nvmrc 指定 > default 别名 > 其它（按版本号降序，不用字母序）
        picked: list[Path] = []
        for want in (_nvmrc_version(), _nvm_default_version()):
            m = _match_nvm_version(versions, want)
            if m and m not in picked:
                picked.append(m)
        for v in sorted(versions, key=_ver_key, reverse=True):
            if v not in picked:
                picked.append(v)
        out += [str(d / "bin") for d in picked]
    if (Path.home() / ".volta" / "bin").exists():
        out.append(str(Path.home() / ".volta" / "bin"))
    fnm = Path.home() / ".fnm" / "node-versions"
    if fnm.exists():
        out += sorted(str(d / "installation" / "bin") for d in fnm.iterdir() if d.is_dir())
    fnm_default = Path.home() / ".fnm" / "aliases" / "default" / "bin"
    if fnm_default.exists():
        out.append(str(fnm_default))
    asdf = Path.home() / ".asdf" / "shims"
    if asdf.exists():
        out.append(str(asdf))
    nver = Path.home() / ".n" / "versions" / "node"
    if nver.exists():
        out += sorted(str(d / "bin") for d in nver.iterdir() if d.is_dir())
    out += ["/opt/homebrew/bin", "/usr/local/bin"]
    return out


def node_bin_dir() -> str:
    """解析 node/yarn 所在 bin 目录，自包含、不依赖调用方 shell 的 PATH。"""
    for tool in ("yarn", "node"):
        p = shutil.which(tool)
        if p:
            return os.path.dirname(p)
    for d in _node_bin_candidates():
        if (Path(d) / "yarn").exists():
            return d
    for d in _node_bin_candidates():
        if (Path(d) / "node").exists():
            return d
    return ""


def node_env() -> dict:
    """供子进程（yarn dev / yarn install）使用的环境，确保 PATH 含 node/yarn bin。"""
    env = os.environ.copy()
    bdir = node_bin_dir()
    if bdir and bdir not in env.get("PATH", ""):
        env["PATH"] = bdir + os.pathsep + env.get("PATH", "")
    return env


def prepare_node_cmd(command: str) -> list[str]:
    """把 'yarn dev' 这样的命令解析成可执行 argv：yarn/pnpm 在就用原样，缺失但有 corepack 则用 corepack 兜底，否则报清楚错。"""
    parts = command.split()
    if not parts:
        fail("空的 dev/install 命令")
    bdir = node_bin_dir()
    if shutil.which(parts[0]) or (bdir and (Path(bdir) / parts[0]).exists()):
        return parts
    if bdir and (Path(bdir) / "corepack").exists() and parts[0] in ("yarn", "pnpm"):
        return ["corepack", parts[0]] + parts[1:]
    fail(
        f"未找到 {parts[0]}/node。请安装 Node.js 和 {parts[0]}（nvm/fnm/volta/homebrew 均可），"
        "或确保其在 PATH 中。"
    )


# ---------- 端口与进程管理 ----------


def find_free_port() -> int:
    """从 PORT_DEFAULT 起找第一个空闲端口。"""
    for p in range(PORT_DEFAULT, PORT_MAX + 1):
        if not port_listening(p):
            return p
    fail(f"{PORT_DEFAULT}-{PORT_MAX} 均被占用，无空闲端口")


def _pids_file_for(project: str) -> Path:
    return TMP_DIR / f"{DEV_PIDS_PREFIX}{project}.json"


def _dev_log_file_for(project: str) -> Path:
    return TMP_DIR / f"{DEV_LOG_PREFIX}{project}.log"


def _read_pid_rec(project: str) -> dict:
    f = _pids_file_for(project)
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_pid_rec(project: str, rec: dict) -> None:
    _pids_file_for(project).write_text(json.dumps(rec), encoding="utf-8")


def _terminate_pgid(pgid: int) -> None:
    """SIGTERM 优雅退出，3s 后仍存活才 SIGKILL（避免硬杀留下文件锁等残留）。"""
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except Exception as e:
        log(f"终止旧进程组 {pgid} 失败: {e}")
        return
    deadline = time.time() + 3
    while time.time() < deadline:
        try:
            os.killpg(pgid, 0)
        except ProcessLookupError:
            return
        time.sleep(0.1)
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def kill_stale_dev(project: str) -> None:
    """按记录的 PGID 精确终止该项目上次起的 dev server 进程组（不碰其他项目）。"""
    pids_file = _pids_file_for(project)
    if not pids_file.exists():
        return
    try:
        rec = json.loads(pids_file.read_text(encoding="utf-8"))
    except Exception:
        pids_file.unlink(missing_ok=True)
        return
    for pgid in rec.get("pgids", []):
        log(f"终止 {project} 上次 dev server 进程组 {pgid}")
        _terminate_pgid(int(pgid))
    pids_file.unlink(missing_ok=True)


# ---------- session 校验 ----------


def staging_session_valid(session: Optional[str], timeout: float = 8):
    """直接打 staging /me 预检 session（不依赖 dev server）。
    返回 True=有效, False=无效, None=无法判定（网络问题，别据此重登）。"""
    if not session:
        return False
    try:
        req = urllib.request.Request(
            f"{STAGING_ORIGIN}/api/user-hub/me",
            headers={"Cookie": f"{COOKIE_NAME}={session}"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return False
            data = json.loads(resp.read().decode("utf-8"))
            return bool(data.get("userUuid") or data.get("uuid") or data.get("email") or data.get("id"))
    except urllib.error.HTTPError:
        return False  # 401/403 → 无效
    except Exception:
        return None  # 网络问题 → 无法判定，保持原 session 走正常流程


def check_session(port: int, session: Optional[str]) -> str:
    """三态：'ok' | 'invalid' | 'not_ready'。区分 server 未就绪 vs session 失效。"""
    if not session:
        return "invalid"
    try:
        req = urllib.request.Request(
            f"http://localhost:{port}/api/user-hub/me",
            headers={"Cookie": f"{COOKIE_NAME}={session}"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status != 200:
                return "invalid"
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("userUuid") or data.get("uuid") or data.get("email") or data.get("id"):
                return "ok"
            return "invalid"
    except urllib.error.HTTPError as e:
        if 400 <= e.code < 500:
            return "invalid"  # 401/403：session 问题，立即重登
        return "not_ready"  # 5xx：server 瞬时错误，继续等
    except Exception:
        return "not_ready"  # 连接拒绝/超时：server 没起


def wait_session(port: int, session: Optional[str], timeout: float = 90) -> str:
    """轮询 session：not_ready 继续，invalid 立即返回重登，ok 完成。"""
    start = time.time()
    while time.time() - start < timeout:
        st = check_session(port, session)
        if st in ("ok", "invalid"):
            return st
        time.sleep(0.5)
    return "timeout"


def _is_our_project(port: int, route: str, timeout: float = 5) -> bool:
    """端口上的 server 是不是本项目：本项目路由不应 404。防别的项目占同端口被误复用。"""
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://localhost:{port}{route}"), timeout=timeout)
        return True  # 2xx/3xx
    except urllib.error.HTTPError as e:
        return e.code != 404  # 404=路由不存在=不是本项目；401/500 等=本项目
    except Exception:
        return False  # 连接失败/超时：不确定，保守不复用


def try_reuse_dev_server(project: str, route: str) -> Optional[int]:
    """判断上次 dev server 是否可复用，返回端口或 None。
    端口在服务 + 路由验证是本项目（防跨项目端口碰撞）。"""
    pids_file = _pids_file_for(project)
    if not pids_file.exists():
        return None
    try:
        rec = json.loads(pids_file.read_text(encoding="utf-8"))
    except Exception:
        return None
    port = rec.get("port")
    if not port or not port_listening(int(port)):
        return None
    if not _is_our_project(int(port), route):
        return None  # 端口上是别的项目，不复用
    return int(port)


def relogin(port: int, args) -> str:
    """清缓存重新登录并校验。session 失效时调用。"""
    clear_session_cache()
    email = (args.email or "").strip() or None
    password = (args.password or "").strip() or None
    session, need = try_get_session(refresh=True, email=email, password=password, headed=args.headed)
    if need == "NEED_EMAIL":
        fail("NEED_EMAIL", EXIT_NEED_EMAIL)
    if need == "NEED_PASSWORD":
        fail("NEED_PASSWORD", EXIT_NEED_PASSWORD)
    if not session or not validate_session(port, session):
        fail("登录态无效，请检查邮箱或密码后重试")
    return session


def detect_project(cwd: Path) -> tuple[str, dict, Path]:
    """用 cwd 名匹配 projects.json。skill 由项目内 agent 调用，cwd 即项目根；不是就报错。"""
    projects = json.loads(PROJECTS_JSON.read_text(encoding="utf-8"))
    name = cwd.name
    if name in projects and (cwd / "package.json").exists():
        return name, projects[name], cwd
    known = ", ".join(projects.keys())
    fail(f"当前目录 {cwd.name} 不是已知项目根（需含 package.json 且目录名匹配 projects.json）。已知项目：{known}。请在项目根目录运行。")


def try_get_session(
    refresh: bool = False,
    email: Optional[str] = None,
    password: Optional[str] = None,
    headed: bool = False,
) -> Tuple[Optional[str], Optional[str]]:
    """返回 (session, need) — need 为 NEED_EMAIL / NEED_PASSWORD。"""
    cmd = [sys.executable, str(SCRIPTS_DIR / "session.py")]
    if refresh:
        cmd.append("--refresh")
    if headed:
        cmd.append("--headed")
    if email:
        cmd.extend(["--email", email])
    if password:
        cmd.extend(["--password", password])

    result = subprocess.run(cmd, text=True, capture_output=True)

    if result.returncode == 0:
        session = result.stdout.strip()
        return (session or None), None

    stderr = result.stderr.strip()
    if result.returncode == EXIT_NEED_EMAIL:
        return None, "NEED_EMAIL"
    if result.returncode == EXIT_NEED_PASSWORD:
        return None, "NEED_PASSWORD"
    if stderr:
        log(stderr)
    return None, None


def validate_session(port: int, session: str) -> bool:
    req = urllib.request.Request(
        f"http://localhost:{port}/api/user-hub/me",
        headers={"Cookie": f"{COOKIE_NAME}={session}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                return False
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            return bool(data.get("userUuid") or data.get("uuid") or data.get("email") or data.get("id"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return False


# ---------- dev server ----------


def _dump_dev_log_tail(project: str, lines: int = 30) -> None:
    log_file = _dev_log_file_for(project)
    if not log_file.exists():
        return
    try:
        tail = log_file.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:]
    except Exception:
        return
    if tail:
        log(f"--- dev server 日志尾部（完整日志: {log_file}）---")
        for line in tail:
            log(f"  {line}")


def wait_for_server(port: int, project: str, timeout: int = 120) -> None:
    """等 dev server 监听端口。用 port_listening（lsof+socket 双探，IP 族无关）。超时自动附日志尾部。"""
    start = time.time()
    last_log = 0
    while time.time() - start < timeout:
        if port_listening(port):
            return
        elapsed = int(time.time() - start)
        if elapsed >= last_log + 5:
            log(f"  仍在等 dev server 启动... {elapsed}s")
            last_log = elapsed
        time.sleep(1)
    _dump_dev_log_tail(project)
    fail(f"等待 localhost:{port} 超时")


def start_dev_server(
    dev_command: str,
    cwd: Path,
    port: int,
    project: str,
    port_flag: Optional[str] = None,
    route: Optional[str] = None,
    supplier_id: Optional[str] = None,
) -> int:
    log_file = _dev_log_file_for(project)
    env = node_env()
    env["PORT"] = str(port)
    env["NITRO_PORT"] = str(port)
    env["HOST"] = os.environ.get("DEV_HOST", "127.0.0.1")  # 默认仅本机访问；需局域网调试时 export DEV_HOST=0.0.0.0
    env["CI"] = "true"  # pnpm/npm 在非 TTY（输出重定向）下会误判 CI 中止 install，显式声明避免
    cmd = prepare_node_cmd(dev_command)
    if port_flag:
        cmd.extend([port_flag, str(port)])
    with log_file.open("w") as logf:
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdout=logf,
            stderr=logf,
            start_new_session=True,
        )
    log(f"dev server 日志: {log_file}")
    rec = _read_pid_rec(project)
    rec.update({"pgids": [proc.pid], "port": port})
    if route:
        rec["route"] = route
    if supplier_id:
        rec["supplierId"] = supplier_id
    _write_pid_rec(project, rec)
    return proc.pid


# ---------- 依赖安装（lockfile 指纹防陈旧） ----------


def _lockfile_path(cwd: Path) -> Optional[Path]:
    for name in LOCKFILE_NAMES:
        p = cwd / name
        if p.exists():
            return p
    return None


def _install_stamp(cwd: Path) -> Path:
    return cwd / "node_modules" / INSTALL_STAMP


def _install_fingerprint(cwd: Path) -> str:
    """lockfile 内容指纹：lockfile 变了（拉新代码/切分支）就该重装。"""
    lf = _lockfile_path(cwd)
    if lf is None:
        return "no-lockfile"
    return hashlib.sha1(lf.read_bytes()).hexdigest()


def mark_installed(cwd: Path) -> None:
    try:
        _install_stamp(cwd).write_text(_install_fingerprint(cwd), encoding="utf-8")
    except Exception:
        pass  # node_modules 只读等场景不影响主流程


def install_needed(cwd: Path) -> Tuple[bool, str]:
    """返回 (是否需要装, 原因)。node_modules 存在但无 stamp（升级前的老安装）时补写 stamp
    视为已同步——避免升级当天把所有项目全量重装一遍。"""
    if not (cwd / "node_modules").exists():
        return True, "node_modules 不存在"
    stamp = _install_stamp(cwd)
    if not stamp.exists():
        mark_installed(cwd)
        return False, ""
    try:
        if stamp.read_text(encoding="utf-8").strip() != _install_fingerprint(cwd):
            return True, "lockfile 已变更（拉新代码/切分支），重装依赖"
    except Exception:
        mark_installed(cwd)
    return False, ""


def run_install(command: str, cwd: Path) -> Tuple[int, list]:
    """流式跑 install：每 30s 打一行心跳（agent 干等有进度感），保留尾部输出供失败诊断。"""
    proc = subprocess.Popen(
        prepare_node_cmd(command),
        cwd=cwd,
        env=node_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    tail: "collections.deque[str]" = collections.deque(maxlen=30)
    start = time.time()
    last_hb = 0.0
    for line in proc.stdout:  # type: ignore[union-attr]
        tail.append(line.rstrip())
        elapsed = time.time() - start
        if elapsed - last_hb >= INSTALL_HEARTBEAT_SECS:
            log(f"  install 进行中... {int(elapsed)}s")
            last_hb = elapsed
    rc = proc.wait()
    return rc, list(tail)


# ---------- cookie 注入 helper ----------


def _ephemeral_port() -> int:
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def reusable_helper(project: str, session: Optional[str]) -> Optional[int]:
    """若已有一个活着的、session 匹配的 cookie 注入 helper，返回其端口；否则 None。"""
    if not session:
        return None
    rec = _read_pid_rec(project)
    hp, hpid, hs = rec.get("helper_port"), rec.get("helper_pid"), rec.get("helper_session")
    if not (hp and hpid and hs) or hs != session:
        return None
    if not pid_alive(int(hpid)):
        return None
    return int(hp) if port_listening(int(hp)) else None


def spawn_helper(target_url: str, session: str) -> tuple:
    """起新的 cookie 注入 helper（detached，生命周期跟 dev server），返回 (pid, port)。
    session 走环境变量传给子进程，不进 argv（ps 可见明文 cookie）。"""
    hport = _ephemeral_port()
    env = dict(os.environ)
    env["STAGING_HELPER_SESSION"] = session
    proc = subprocess.Popen(
        [sys.executable, str(SCRIPTS_DIR / "open_browser.py"), "--serve", str(hport), target_url],
        start_new_session=True,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc.pid, hport


def record_helper(project: str, hpid: int, hport: int, session: str) -> None:
    rec = _read_pid_rec(project)
    rec["helper_pid"] = hpid
    rec["helper_port"] = hport
    rec["helper_session"] = session
    _write_pid_rec(project, rec)


def resolve_session(email: Optional[str], password: Optional[str], headed: bool = False) -> str:
    session, need = try_get_session(email=email, password=password, headed=headed)
    if need == "NEED_EMAIL":
        fail("NEED_EMAIL", EXIT_NEED_EMAIL)
    if need == "NEED_PASSWORD":
        fail("NEED_PASSWORD", EXIT_NEED_PASSWORD)
    if not session:
        fail("无法获取 _user_session")
    return session


# ---------- --status ----------


def print_status() -> None:
    """列出本 skill 起过的 dev server（含已死记录，便于判断复用/清理）。任意目录可跑，只读。"""
    servers = []
    for f in sorted(TMP_DIR.glob(f"{DEV_PIDS_PREFIX}*.json")):
        project = f.name[len(DEV_PIDS_PREFIX):-len(".json")]
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            port = rec.get("port")
            entry = {
                "project": project,
                "port": port,
                "listening": bool(port and port_listening(int(port))),
                "log": str(_dev_log_file_for(project)),
            }
            route = rec.get("route")
            if route and port:
                entry["url"] = f"http://localhost:{port}{route}"
            hp, hpid = rec.get("helper_port"), rec.get("helper_pid")
            if hp and hpid and pid_alive(int(hpid)) and port_listening(int(hp)):
                entry["cookieHelper"] = f"http://localhost:{hp}/"
            servers.append(entry)
        except Exception:
            continue
    print(json.dumps({"ok": True, "servers": servers}, ensure_ascii=False, indent=2))


# ---------- 主流程 ----------


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--supplier-id")
    parser.add_argument("--email")
    parser.add_argument("--password")
    parser.add_argument("--project")
    parser.add_argument("--no-open", action="store_true")
    parser.add_argument("--headed", action="store_true", help="首次/微软会话过期时，开可见浏览器交互登录")
    parser.add_argument("--reinstall", action="store_true", help="强制重装依赖（node_modules 存在但可疑时）")
    parser.add_argument("--status", action="store_true", help="列出运行中的 dev server（任意目录可跑，只读）")
    args = parser.parse_args()

    if args.status:
        print_status()
        return
    if not args.supplier_id:
        parser.error("--supplier-id 必填（查运行状态用 --status）")

    cwd = Path.cwd()
    if args.project:
        projects = json.loads(PROJECTS_JSON.read_text(encoding="utf-8"))
        config = projects.get(args.project)
        if not config:
            fail(f"未知项目: {args.project}")
        name = args.project
        if not (cwd / "package.json").exists():
            fail(f"--project={args.project} 已识别，但当前目录 {cwd} 不是项目根（无 package.json）。请在项目根目录运行。")
    else:
        name, config, cwd = detect_project(cwd)

    need_auth = config.get("auth", True)
    port_flag = config.get("portFlag")

    # 内联读缓存 session（命中就不起 session.py 子进程）
    session = read_session_cache() if need_auth else None

    # 先验 cookie（对 staging 直接，不依赖 dev server / 端口复用判断）—— cookie 优先于端口复用
    if need_auth and session:
        pre = staging_session_valid(session)
        if pre is False:
            log("预检：session 已失效，重新登录")
            clear_session_cache()
            session = None
        # pre is None（网络问题）→ 保持 session，走正常流程

    # 优先复用上次还活着的 dev server（省掉 kill/start/wait 构建开销）
    route = config["route"].replace("{supplierId}", args.supplier_id.strip())
    reuse_port = try_reuse_dev_server(name, route)
    if reuse_port:
        log(f"复用运行中的 dev server :{reuse_port}（无需重启）")
        port = reuse_port
        if need_auth:
            st = check_session(port, session)
            if st != "ok":
                log(f"session 失效（{st}），重新登录（dev server 保留）...")
                session = relogin(port, args)
            log("鉴权成功")
    else:
        kill_stale_dev(name)
        port = find_free_port()
        log(f"使用端口 :{port}")

        if args.reinstall:
            need_install, install_reason = True, "--reinstall 强制重装"
        else:
            need_install, install_reason = install_needed(cwd)
        if need_install:
            log(f"安装项目依赖: {config['install']}（{install_reason}）")
            rc, tail_lines = run_install(config["install"], cwd)
            if rc != 0:
                log("install 失败，最后输出：")
                for line in tail_lines:
                    log(f"  {line}")
                if any("401" in l or "Unauthorized" in l for l in tail_lines):
                    fail("npm registry 认证失败（401）。请检查 .npmrc 中 GitHub Packages 的 authToken 配置。")
                fail(f"{config['install']} 退出码 {rc}")
            mark_installed(cwd)

        log(f"启动 dev server ({config['dev']}) on :{port}")
        start_dev_server(
            config["dev"], cwd, port, project=name, port_flag=port_flag,
            route=route, supplier_id=args.supplier_id.strip(),
        )  # 后台 build
        # 登录与 dev server 构建并行（登录不依赖 dev server）
        if need_auth and not session:
            log("正在登录获取 session（与 dev server 构建并行，约 10-40s）...")
            email = (args.email or "").strip() or None
            password = (args.password or "").strip() or None
            session = resolve_session(email, password, headed=args.headed)
        log(f"等待 localhost:{port} 就绪...")
        wait_for_server(port, name)  # TCP 端口监听

        if need_auth:
            # 三态轮询：not_ready 继续，invalid 立即重登，ok 完成（不盲目等满超时）
            st = wait_session(port, session, timeout=90)
            if st == "ok":
                log("鉴权成功")
            else:
                log(f"session 失效或 server 未就绪（{st}），重新登录...")
                session = relogin(port, args)

    target_url = f"http://localhost:{port}{route}"

    log(f"业务页: {target_url}")

    if not args.no_open:
        import webbrowser
        if need_auth:
            hp = reusable_helper(name, session)
            if hp:
                log(f"复用 cookie 注入入口 :{hp}（默认浏览器已有 cookie，直接访问 {target_url}）")
                webbrowser.open(target_url)
            else:
                hpid, hport = spawn_helper(target_url, session)
                record_helper(name, hpid, hport, session)
                helper_url = f"http://localhost:{hport}/"
                webbrowser.open(helper_url)
                log(f"cookie 注入入口（可选，其它浏览器用）：{helper_url}")
        else:
            webbrowser.open(target_url)

    result = {
        "ok": True,
        "project": name,
        "port": port,
        "supplierId": args.supplier_id.strip(),
        "url": target_url,
        "log": str(_dev_log_file_for(name)),
    }
    if need_auth:
        result["me"] = f"http://localhost:{port}/api/user-hub/me"
    print(json.dumps(result))


if __name__ == "__main__":
    main()
