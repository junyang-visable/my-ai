#!/usr/bin/env bash
# =============================================================================
# .harness/feedback/collect-evidence.sh — 失败证据自动收集
# -----------------------------------------------------------------------------
# 把「失败信息即下一轮 prompt」落地：一次跑测/E2E 失败后，把可复用的证据聚到
# 一个目录，供 Evaluator 判定与下一轮修复直接引用。
# 依据 11020723621（失败摘要 + 分类信号：布局→截图+DOM、接口→网络+Console、
# 接口对但 UI 错→响应体+渲染时机），11020604944（执行结果须带截图/断言/步骤追踪）。
#
# 用法:
#   collect-evidence.sh <任务名> [失败类别]
#     失败类别: layout | api | render | generic（默认 generic），决定收哪几路信息
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
source "$HARNESS_DIR/config.sh"

# workspace 模式：执行切到目标仓库；任务/证据目录可由 HARNESS_TASKS_DIR 指定
if [ -n "${HARNESS_REPO:-}" ]; then
  [ -d "$HARNESS_REPO" ] || { echo "HARNESS_REPO 不存在: $HARNESS_REPO" >&2; exit 66; }
  cd "$HARNESS_REPO"
fi
TASKS_DIR="${HARNESS_TASKS_DIR:-$HARNESS_DIR/tasks}"

TASK="${1:-_last}"
CATEGORY="${2:-generic}"
OUT="$TASKS_DIR/$TASK/evidence/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"

echo "== 收集失败证据 → $OUT （类别: $CATEGORY）=="

# --- 通用：环境与最近一次 validate 摘要 ------------------------------------------
{
  echo "time: $(date -Iseconds)"
  echo "category: $CATEGORY"
  echo "pwd: $(pwd)"
  echo "git: $(git rev-parse --short HEAD 2>/dev/null || echo n/a) / $(git branch --show-current 2>/dev/null || echo n/a)"
} > "$OUT/context.txt"

# 重跑一次 E2E（如配置）抓原始输出
if [ -n "${HARNESS_E2E_CMD:-}" ]; then
  echo "-- 重跑 E2E 抓输出（可能较慢）--"
  bash -c "$HARNESS_E2E_CMD" > "$OUT/e2e-output.log" 2>&1 || true
fi

# --- Cypress/Playwright 常见产物（存在才收）--------------------------------------
for d in cypress/screenshots cypress/videos test-results playwright-report; do
  if [ -d "$d" ]; then
    cp -R "$d" "$OUT/" 2>/dev/null || true
    echo "  收集: $d"
  fi
done

# --- 按类别补充采集提示（写进 next-prompt.md，供下一轮直接用）------------------------
{
  echo "# 失败证据摘要（下一轮 prompt 用）"
  echo
  echo "- 任务: $TASK ｜ 类别: $CATEGORY"
  echo "- 证据目录: $OUT"
  echo
  echo "## 建议 Agent 自主拉取的信息（11020723621 分类）"
  case "$CATEGORY" in
    layout) echo "- 布局问题：看截图 + DOM 结构 + 是否白屏；对比期望与实际视觉差异。" ;;
    api)    echo "- 接口异常：看网络请求（状态码/耗时）+ Console 报错；确认请求参数与鉴权。" ;;
    render) echo "- 接口对但 UI 错：看响应体 + 渲染时机日志；排查异步竞态与状态未更新。" ;;
    *)      echo "- 通用：先读 e2e-output.log 的失败断言，再决定拉截图/网络/日志哪一路。" ;;
  esac
  echo
  echo "## 原始失败输出（末 40 行）"
  echo '```'
  [ -f "$OUT/e2e-output.log" ] && tail -n 40 "$OUT/e2e-output.log"
  echo '```'
} > "$OUT/next-prompt.md"

echo "完成。把 $OUT/next-prompt.md 作为下一轮修复的输入。"
