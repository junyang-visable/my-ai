#!/usr/bin/env bash
# 预装：playwright 包。浏览器用系统 Chrome（channel=chrome），不依赖下载 chromium（公司代理 cdn.playwright.dev 拦截）。
# 注意：channel=chrome 需启动 /Applications/Google Chrome，沙箱会拦——agent 必须用完整文件权限运行（见 SKILL.md）。
set -uo pipefail

# venv/marker 放 ~/.config：/tmp 会被 macOS 定期清理，丢 venv 会意外触发重装
DATA_DIR="${HOME}/.config/supplier-local-cold-start"
VENV_DIR="${DATA_DIR}/venv"
VENV_PYTHON="${VENV_DIR}/bin/python3"
MARKER="${DATA_DIR}/.installed"

mkdir -p "$DATA_DIR" 2>/dev/null

# 选有 playwright 的 python（系统优先）
PW_PY=""
for py in python3 python "$VENV_PYTHON"; do
  [[ -z "$py" ]] && continue
  if command -v "$py" >/dev/null 2>&1 && "$py" -c "import playwright" 2>/dev/null; then
    PW_PY="$py"; break
  fi
done

# 都没有 → 建 venv
if [[ -z "$PW_PY" ]]; then
  PY_BIN=""
  for py in python3 python; do
    # 脚本用了内建泛型标注（tuple[...]/list[...]），需 3.9+
  if command -v "$py" >/dev/null 2>&1 && "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)' 2>/dev/null; then
      PY_BIN="$py"; break
    fi
  done
  [[ -z "$PY_BIN" ]] && { echo "setup: 未找到 >= 3.8 的 python" >&2; exit 1; }
  [[ ! -d "$VENV_DIR" ]] && "$PY_BIN" -m venv "$VENV_DIR" || { echo "setup: venv 失败" >&2; exit 1; }
  "${VENV_DIR}/bin/pip" install -q playwright || { echo "setup: pip install 失败" >&2; exit 1; }
  PW_PY="$VENV_PYTHON"
fi

# 检查系统 Chrome 可用（channel=chrome 是登录/渲染的依赖）
if "$PW_PY" - <<'PY' 2>/dev/null
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context("/tmp/.pw-setup-probe", headless=True, channel="chrome")
    ctx.close()
PY
then
  : # 系统 Chrome OK
else
  echo "setup: 警告 — 系统 Chrome 启动失败（可能沙箱拦截）。需用完整文件权限运行；chromium 下载因公司代理不可用。" >&2
fi
rm -rf /tmp/.pw-setup-probe 2>/dev/null

touch "$MARKER"
echo "INSTALLED ($PW_PY)"
