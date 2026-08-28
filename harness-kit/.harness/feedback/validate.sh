#!/usr/bin/env bash
# =============================================================================
# .harness/feedback/validate.sh — the single entry point of mechanical enforcement
# -----------------------------------------------------------------------------
# Composes lint → typecheck → arch → build → test into one command and reports
# by gate level:
#   blocking  — failure => exit code 1
#   warning   — failure passes by default; treated as blocking under --strict
#   info      — print only, never affects the exit code
# Unified feedback format: LEVEL | stage | file:line (if any) | reason | fix
#
# Usage:
#   validate.sh                 full pipeline
#   validate.sh --strict        warnings become blocking
#   validate.sh --stage lint    single stage only
#   validate.sh selfcheck       deliberately plant a violation to prove the guardrail fires
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
source "$HARNESS_DIR/config.sh"

# workspace mode: engine lives in the kit, execution switches to the target repo
# (HARNESS_REPO injected by the harness CLI)
if [ -n "${HARNESS_REPO:-}" ]; then
  if [ ! -d "$HARNESS_REPO" ]; then
    echo "HARNESS_REPO not found: $HARNESS_REPO" >&2; exit 66
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
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 64 ;;
  esac
  shift
done

# --- output helpers -------------------------------------------------------------
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
    report INFO "$stage" "no command configured, skipping (fill HARNESS_*_CMD in the repo's harness config)"
    return 0
  fi
  local out rc
  out="$(bash -c "$cmd" 2>&1)"; rc=$?
  if [ $rc -eq 0 ]; then
    report OK "$stage" "passed"
    return 0
  fi
  # failure: classify by level; append the last 15 lines of raw output as next-round prompt
  local last; last="$(printf '%s\n' "$out" | tail -n 15)"
  case "$level" in
    BLOCK)
      BLOCKING_FAILS=$((BLOCKING_FAILS+1))
      report BLOCK "$stage" "command failed (exit $rc): $cmd" "$fix"
      ;;
    WARN)
      if [ "$STRICT" -eq 1 ]; then
        BLOCKING_FAILS=$((BLOCKING_FAILS+1))
        report BLOCK "$stage" "command failed (--strict, exit $rc): $cmd" "$fix"
      else
        WARNING_FAILS=$((WARNING_FAILS+1))
        report WARN "$stage" "command failed (exit $rc): $cmd" "$fix"
      fi
      ;;
  esac
  printf "%s---- %s output (last 15 lines) ----%s\n%s\n" "$c_dim" "$stage" "$c_rst" "$last"
}

# --- selfcheck: the guardrail of the guardrail ----------------------------------
# Once a guardrail exists, deliberately plant a violation and confirm it fires —
# "a linter that never complains proves the guardrail is paper".
selfcheck() {
  echo "== selfcheck: planting a known architecture violation, expecting lint-arch to block =="
  local tmp; tmp="$(mktemp -d)"
  # fabricate an obvious violation: a forbidden cross-layer import in source
  mkdir -p "$tmp/src/domain"
  echo "import { db } from '../../infra/db' // FORBIDDEN_CROSS_LAYER" > "$tmp/src/domain/leak.ts"
  local out rc
  out="$(HARNESS_ARCH_SCAN_ROOT="$tmp" bash "$HARNESS_DIR/feedback/lint-arch.sh" 2>&1)"; rc=$?
  rm -rf "$tmp"
  if [ $rc -ne 0 ]; then
    report OK "selfcheck" "guardrail blocked the violation as expected (exit $rc) — the guardrail is real"
    echo "$out" | sed 's/^/    /'
    return 0
  else
    report BLOCK "selfcheck" "guardrail failed to block a known violation — it's paper; check lint-arch.sh rules" \
      "confirm the rule table matches FORBIDDEN_CROSS_LAYER"
    return 1
  fi
}

if [ "$MODE" = "selfcheck" ]; then
  selfcheck; exit $?
fi

echo "== harness validate $( [ "$STRICT" -eq 1 ] && echo '(strict)')${HARNESS_REPO:+ @ $HARNESS_REPO} =="

# blocking stages (in order)
run_stage BLOCK lint      "$HARNESS_LINT_CMD"      "fix lint errors; style-only issues can go through $HARNESS_STYLE_CMD first"
run_stage BLOCK typecheck "$HARNESS_TYPECHECK_CMD" "fix type errors; @ts-ignore is not a workaround"
run_stage BLOCK arch      "$HARNESS_ARCH_LINT_CMD" "cross-layer dependency check; rules in .harness/feedback/lint-arch.sh"
run_stage BLOCK build     "$HARNESS_BUILD_CMD"     "build is a hard gate that cannot be skipped"
run_stage BLOCK test      "$HARNESS_TEST_CMD"      "read the failing assertions first; never bend expectations to green"

# warning stages
run_stage WARN  style     "$HARNESS_STYLE_CMD"       "run the formatter"
run_stage WARN  lock      "$HARNESS_LOCK_TESTS_CMD"  "smoke tests were modified (see the assertion-lock output); for a deliberate change add // @lock-bypass + a reason"

# informational stages
if [ -z "$ONLY_STAGE" ] || [ "$ONLY_STAGE" = "info" ]; then
  for c in "${HARNESS_INFO_CMDS[@]:-}"; do
    [ -z "$c" ] && continue
    report INFO info "$(bash -c "$c" 2>&1 | head -n 1)"
  done
fi

echo "------------------------------------------------------------"
if [ "$BLOCKING_FAILS" -gt 0 ]; then
  report BLOCK summary "$BLOCKING_FAILS blocking failure(s), $WARNING_FAILS warning(s)"
  echo "exit 1: gates not met; the failure output above is the next round's prompt."
  exit 1
fi
if [ "$WARNING_FAILS" -gt 0 ]; then
  report WARN summary "$WARNING_FAILS warning(s) (non-blocking). Add --strict to promote them to blocking."
fi
report OK summary "all blocking gates passed."
exit 0
