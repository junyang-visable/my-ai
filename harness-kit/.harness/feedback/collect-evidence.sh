#!/usr/bin/env bash
# =============================================================================
# .harness/feedback/collect-evidence.sh — automatic failure-evidence collection
# -----------------------------------------------------------------------------
# Implements "failure info is the next round's prompt": after a test/E2E failure,
# gathers reusable evidence into one directory that the Evaluator's verdict and
# the next fix round can reference directly.
# Signal taxonomy: layout → screenshot + DOM; api → network + console;
# api-ok-but-UI-wrong → response body + render timing; execution results carry
# screenshots/assertions/step traces.
#
# Usage:
#   collect-evidence.sh <task> [failure category]
#     category: layout | api | render | generic (default generic) — decides which signals to gather
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
source "$HARNESS_DIR/config.sh"

# workspace mode: execution switches to the target repo; the task/evidence dir
# can be pointed at via HARNESS_TASKS_DIR
if [ -n "${HARNESS_REPO:-}" ]; then
  [ -d "$HARNESS_REPO" ] || { echo "HARNESS_REPO not found: $HARNESS_REPO" >&2; exit 66; }
  cd "$HARNESS_REPO"
fi
TASKS_DIR="${HARNESS_TASKS_DIR:-$HARNESS_DIR/tasks}"

TASK="${1:-_last}"
CATEGORY="${2:-generic}"
OUT="$TASKS_DIR/$TASK/evidence/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"

echo "== collecting failure evidence → $OUT (category: $CATEGORY) =="

# --- common: environment + a fresh context snapshot ------------------------------
{
  echo "time: $(date -Iseconds)"
  echo "category: $CATEGORY"
  echo "pwd: $(pwd)"
  echo "git: $(git rev-parse --short HEAD 2>/dev/null || echo n/a) / $(git branch --show-current 2>/dev/null || echo n/a)"
} > "$OUT/context.txt"

# re-run E2E once (if configured) to capture raw output
if [ -n "${HARNESS_E2E_CMD:-}" ]; then
  echo "-- re-running E2E to capture output (may be slow) --"
  bash -c "$HARNESS_E2E_CMD" > "$OUT/e2e-output.log" 2>&1 || true
fi

# --- common Cypress/Playwright artifacts (collected only when present) -----------
for d in cypress/screenshots cypress/videos test-results playwright-report; do
  if [ -d "$d" ]; then
    cp -R "$d" "$OUT/" 2>/dev/null || true
    echo "  collected: $d"
  fi
done

# --- category-specific acquisition hints (into next-prompt.md, ready for the next round) --
{
  echo "# Failure evidence summary (for the next round's prompt)"
  echo
  echo "- task: $TASK | category: $CATEGORY"
  echo "- evidence dir: $OUT"
  echo
  echo "## Suggested signals for the agent to pull (by category)"
  case "$CATEGORY" in
    layout) echo "- layout issue: screenshot + DOM structure + blank-screen check; diff expected vs actual visuals." ;;
    api)    echo "- api issue: network requests (status/latency) + console errors; check params and auth." ;;
    render) echo "- api fine but UI wrong: response body + render-timing logs; chase async races and stale state." ;;
    *)      echo "- generic: read the failing assertions in e2e-output.log first, then pick screenshots/network/logs." ;;
  esac
  echo
  echo "## Raw failure output (last 40 lines)"
  echo '```'
  [ -f "$OUT/e2e-output.log" ] && tail -n 40 "$OUT/e2e-output.log"
  echo '```'
} > "$OUT/next-prompt.md"

echo "done. use $OUT/next-prompt.md as the input for the next fix round."
