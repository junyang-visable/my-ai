#!/usr/bin/env bash
# =============================================================================
# .harness/feedback/validate.sh — 机械化执法的统一入口
# -----------------------------------------------------------------------------
# 合成一条命令跑完 lint → typecheck → arch → build → test，并按三级门禁给结论：
#   阻断级(blocking)  失败 => 退出码 1
#   警告级(warning)   失败 => 默认放行；--strict 时按阻断处理
#   提示级(info)      只打印，永不影响退出码
# 反馈统一格式：LEVEL | stage | file:line（如有）| reason | fix
#
# 用法:
#   validate.sh                 跑全套
#   validate.sh --strict        警告也当阻断
#   validate.sh --stage lint    只跑某一阶段
#   validate.sh selfcheck       故意制造一次违规，确认护栏真的会报错（护栏的护栏）
#
# 对齐: 11020601776（统一入口 + 验证护栏本身）、11020729209（三级门禁 + 统一格式）
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
source "$HARNESS_DIR/config.sh"

# workspace 模式：引擎在 kit，执行切到目标仓库（HARNESS_REPO 由 harness CLI 注入）
if [ -n "${HARNESS_REPO:-}" ]; then
  if [ ! -d "$HARNESS_REPO" ]; then
    echo "HARNESS_REPO 不存在: $HARNESS_REPO" >&2; exit 66
  fi
  cd "$HARNESS_REPO"
fi

STRICT=0
ONLY_STAGE=""
MODE="run"
while [ $# -gt 0 ]; do
  case "$1" in
    --strict) STRICT=1 ;;
    --stage) ONLY_STAGE="${2:-}"; shift ;;
    selfcheck) MODE="selfcheck" ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 64 ;;
  esac
  shift
done

# --- 输出助手 -----------------------------------------------------------------
c_red=$'\033[31m'; c_yel=$'\033[33m'; c_dim=$'\033[2m'; c_grn=$'\033[32m'; c_rst=$'\033[0m'
BLOCKING_FAILS=0
WARNING_FAILS=0

report() { # level stage reason fix
  local level="$1" stage="$2" reason="$3" fix="${4:-}"
  local tag color
  case "$level" in
    BLOCK) tag="BLOCKING"; color="$c_red" ;;
    WARN)  tag="WARNING";  color="$c_yel" ;;
    INFO)  tag="INFO";     color="$c_dim" ;;
    OK)    tag="OK";       color="$c_grn" ;;
  esac
  printf "%s%-9s%s | %-10s | %s\n" "$color" "$tag" "$c_rst" "$stage" "$reason"
  [ -n "$fix" ] && printf "          %s↳ fix: %s%s\n" "$c_dim" "$fix" "$c_rst"
}

run_stage() { # level stage cmd fix
  local level="$1" stage="$2" cmd="$3" fix="${4:-}"
  [ -n "$ONLY_STAGE" ] && [ "$ONLY_STAGE" != "$stage" ] && return 0
  if [ -z "$cmd" ]; then
    report INFO "$stage" "未配置命令，跳过（在 .harness/config.sh 里填 HARNESS_*_CMD）"
    return 0
  fi
  local out rc
  out="$(bash -c "$cmd" 2>&1)"; rc=$?
  if [ $rc -eq 0 ]; then
    report OK "$stage" "通过"
    return 0
  fi
  # 失败：按级别归类，末尾附最后 15 行原始输出便于当作下一轮 prompt
  local last; last="$(printf '%s\n' "$out" | tail -n 15)"
  case "$level" in
    BLOCK)
      BLOCKING_FAILS=$((BLOCKING_FAILS+1))
      report BLOCK "$stage" "命令失败（exit $rc）：$cmd" "$fix"
      ;;
    WARN)
      if [ "$STRICT" -eq 1 ]; then
        BLOCKING_FAILS=$((BLOCKING_FAILS+1))
        report BLOCK "$stage" "命令失败（--strict，exit $rc）：$cmd" "$fix"
      else
        WARNING_FAILS=$((WARNING_FAILS+1))
        report WARN "$stage" "命令失败（exit $rc）：$cmd" "$fix"
      fi
      ;;
  esac
  printf "%s---- %s 输出（末 15 行）----%s\n%s\n" "$c_dim" "$stage" "$c_rst" "$last"
}

# --- selfcheck：护栏的护栏 ------------------------------------------------------
# 11020601776：护栏建好后要故意制造一次违规，确认它真会报错——「lint 没报错说明护栏是纸糊的」。
selfcheck() {
  echo "== selfcheck：故意制造一次架构违规，确认 lint-arch 会拦 =="
  local tmp; tmp="$(mktemp -d)"
  # 造一个明显违规：源码里出现被禁的跨层 import 标记
  mkdir -p "$tmp/src/domain"
  echo "import { db } from '../../infra/db' // FORBIDDEN_CROSS_LAYER" > "$tmp/src/domain/leak.ts"
  local out rc
  out="$(HARNESS_ARCH_SCAN_ROOT="$tmp" bash "$HARNESS_DIR/feedback/lint-arch.sh" 2>&1)"; rc=$?
  rm -rf "$tmp"
  if [ $rc -ne 0 ]; then
    report OK "selfcheck" "护栏按预期拦截了违规（exit $rc）——护栏是真的"
    echo "$out" | sed 's/^/    /'
    return 0
  else
    report BLOCK "selfcheck" "护栏没有拦住已知违规——护栏是纸糊的，请检查 lint-arch.sh 规则" \
      "确认规则表能匹配 FORBIDDEN_CROSS_LAYER"
    return 1
  fi
}

if [ "$MODE" = "selfcheck" ]; then
  selfcheck; exit $?
fi

echo "== harness validate $( [ "$STRICT" -eq 1 ] && echo '(strict)')${HARNESS_REPO:+ @ $HARNESS_REPO} =="

# 阻断级（顺序执行）
run_stage BLOCK lint      "$HARNESS_LINT_CMD"      "修掉 lint 报错；风格类可先跑 $HARNESS_STYLE_CMD"
run_stage BLOCK typecheck "$HARNESS_TYPECHECK_CMD" "修类型错误，禁止用 @ts-ignore 绕过（11020656025）"
run_stage BLOCK arch      "$HARNESS_ARCH_LINT_CMD" "检查跨层依赖，规则见 .harness/feedback/lint-arch.sh"
run_stage BLOCK build     "$HARNESS_BUILD_CMD"     "build 是不可跳过的硬门禁（11020656025）"
run_stage BLOCK test      "$HARNESS_TEST_CMD"      "先看失败断言，别改测试预期去凑绿"

# 警告级
run_stage WARN  style     "$HARNESS_STYLE_CMD"       "跑格式化即可"
run_stage WARN  lock      "$HARNESS_LOCK_TESTS_CMD"  "冒烟测试被改动，见断言锁提示；确需改动加 // @lock-bypass + 说明"

# 提示级
if [ -z "$ONLY_STAGE" ] || [ "$ONLY_STAGE" = "info" ]; then
  for c in "${HARNESS_INFO_CMDS[@]:-}"; do
    [ -z "$c" ] && continue
    report INFO info "$(bash -c "$c" 2>&1 | head -n 1)"
  done
fi

echo "------------------------------------------------------------"
if [ "$BLOCKING_FAILS" -gt 0 ]; then
  report BLOCK summary "$BLOCKING_FAILS 个阻断级失败，$WARNING_FAILS 个警告"
  echo "退出码 1：未达门禁，上面的失败输出即下一轮修复的 prompt。"
  exit 1
fi
if [ "$WARNING_FAILS" -gt 0 ]; then
  report WARN summary "$WARNING_FAILS 个警告（非阻断）。加 --strict 可将其升级为阻断。"
fi
report OK summary "全部阻断级门禁通过。"
exit 0
