#!/usr/bin/env bash
# =============================================================================
# .harness/hooks/post-edit.sh — 编辑后增量快检钩子
# -----------------------------------------------------------------------------
# 每次 agent 写/改一个文件后触发，只对该文件跑轻量检查，并**截断输出**。
# 依据 11020603220：100 次编辑的会话累计能省 1–2 小时；但钩子输出会反向污染
# 上下文，所以必须截断（默认 40 行）。
#
# 输入（两种都兼容）:
#   1. 命令行参数:            post-edit.sh <被编辑文件路径>
#   2. Claude Code 的 stdin:  {"tool_input":{"file_path":"..."}} 通过 PostToolUse 传入
#
# 退出码:
#   0  = 无问题 / 无需检查（放行）
#   2  = 发现问题（Claude Code 约定：非 0 会把 stderr 回喂给模型）
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
source "$HARNESS_DIR/config.sh"

MAX_LINES="${HARNESS_HOOK_MAX_LINES:-40}"

# --- 解析被编辑文件路径 --------------------------------------------------------
FILE="${1:-}"
if [ -z "$FILE" ] && [ ! -t 0 ]; then
  payload="$(cat)"
  # 无 jq 也能跑：优先 jq，退化到 grep
  if command -v jq >/dev/null 2>&1; then
    FILE="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)"
  fi
  if [ -z "$FILE" ]; then
    FILE="$(printf '%s' "$payload" | grep -oE '"(file_path|path)"[[:space:]]*:[[:space:]]*"[^"]+"' | head -n1 | sed -E 's/.*"([^"]+)"$/\1/')"
  fi
fi

[ -z "$FILE" ] && exit 0            # 拿不到文件就安静放行
[ -f "$FILE" ] || exit 0

cmd="$(harness_incremental_cmd "$FILE")"
[ -z "$cmd" ] && exit 0             # 该类型无需快检

out="$(bash -c "$cmd" 2>&1)"; rc=$?
if [ $rc -eq 0 ]; then
  exit 0
fi

# 失败：截断输出后回喂
total="$(printf '%s\n' "$out" | wc -l | tr -d ' ')"
{
  echo "post-edit 快检未通过: $FILE"
  echo "命令: $cmd"
  echo "---- 输出（前 $MAX_LINES / 共 $total 行）----"
  printf '%s\n' "$out" | head -n "$MAX_LINES"
  [ "$total" -gt "$MAX_LINES" ] && echo "... 已截断，其余 $((total - MAX_LINES)) 行省略，完整结果请跑 validate.sh ..."
} >&2
exit 2
