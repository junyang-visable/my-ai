#!/usr/bin/env bash
# 用一个已装 playwright 的 Python 跑脚本。
# - 优先复用 PATH 里已有的 playwright，没有才建专属 venv
# - node 由 bootstrap.py 内部检测（读 $NVM_DIR + nvm default 别名 + .nvmrc），不依赖 shell PATH
# - IDE agent 非交互 shell 不加载 ~/.zshrc，从 .zshrc 补读关键环境变量
# 用法: bash scripts/run.sh bootstrap.py --supplier-id=xxx
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${HOME}/.config/supplier-local-cold-start/venv/bin/python3"

# 1) 从 ~/.zshrc 补关键环境变量（agent 非交互 shell 不加载 rc）
_rc_file=""
case "$SHELL" in
  *zsh)  _rc_file="$HOME/.zshrc" ;;
  *bash) _rc_file="$HOME/.bashrc" ;;
esac
if [[ -n "$_rc_file" && -f "$_rc_file" ]]; then
  for _var in GITHUB_TOKEN STAGING_EMAIL STAGING_PASSWORD NODE_AUTH_TOKEN; do
    if [[ -z "${!_var}" ]]; then
      _line=$(grep -E "^(export )?${_var}=" "$_rc_file" 2>/dev/null | tail -1)
      [[ -n "$_line" ]] && eval "$_line"
    fi
  done
fi
if [[ -z "$NODE_AUTH_TOKEN" && -n "$GITHUB_TOKEN" ]]; then
  export NODE_AUTH_TOKEN="$GITHUB_TOKEN"
fi
unset _rc_file _var _line

has_pw() { "$1" -c "import playwright" 2>/dev/null; }

for py in python3 python; do
  if command -v "$py" >/dev/null 2>&1 && has_pw "$py"; then
    exec "$py" "${SCRIPT_DIR}/$@"
  fi
done

if [[ -f "$VENV_PYTHON" ]] && has_pw "$VENV_PYTHON"; then
  exec "$VENV_PYTHON" "${SCRIPT_DIR}/$@"
fi

echo "[supplier-local-cold-start] 未检测到 playwright，正在安装..." >&2
bash "${SCRIPT_DIR}/setup.sh" || exit 1

for py in python3 python "$VENV_PYTHON"; do
  [[ -z "$py" || ! -e "$py" ]] && continue
  if has_pw "$py"; then exec "$py" "${SCRIPT_DIR}/$@"; fi
done
echo "[supplier-local-cold-start] 安装后仍找不到 playwright" >&2
exit 1
