#!/usr/bin/env bash
# =============================================================================
# .harness/hooks/post-edit.sh — incremental post-edit quick-check hook
# -----------------------------------------------------------------------------
# Fires after each file the agent writes/edits; runs lightweight checks on that
# file only, and **truncates the output**. Across a 100-edit session this saves
# an hour or two; but hook output pollutes context in the other direction, so
# truncation (default 40 lines) is mandatory.
#
# Input (both forms supported):
#   1. CLI arg:                post-edit.sh <path of the edited file>
#   2. Claude Code stdin:      {"tool_input":{"file_path":"..."}} via PostToolUse
#
# Exit codes:
#   0  = clean / nothing to check (pass)
#   2  = issue found (Claude Code convention: non-zero feeds stderr back to the model)
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
source "$HARNESS_DIR/config.sh"

MAX_LINES="${HARNESS_HOOK_MAX_LINES:-40}"

# --- parse the edited file path -------------------------------------------------
FILE="${1:-}"
if [ -z "$FILE" ] && [ ! -t 0 ]; then
  payload="$(cat)"
  # runs without jq too: prefer jq, fall back to grep
  if command -v jq >/dev/null 2>&1; then
    FILE="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)"
  fi
  if [ -z "$FILE" ]; then
    FILE="$(printf '%s' "$payload" | grep -oE '"(file_path|path)"[[:space:]]*:[[:space:]]*"[^"]+"' | head -n1 | sed -E 's/.*"([^"]+)"$/\1/')"
  fi
fi

[ -z "$FILE" ] && exit 0            # no file resolved — pass silently
[ -f "$FILE" ] || exit 0

cmd="$(harness_incremental_cmd "$FILE")"
[ -z "$cmd" ] && exit 0             # nothing to quick-check for this file type

out="$(bash -c "$cmd" 2>&1)"; rc=$?
if [ $rc -eq 0 ]; then
  exit 0
fi

# failure: truncate the output, then feed back
total="$(printf '%s\n' "$out" | wc -l | tr -d ' ')"
{
  echo "post-edit quick-check failed: $FILE"
  echo "command: $cmd"
  echo "---- output (first $MAX_LINES of $total lines) ----"
  printf '%s\n' "$out" | head -n "$MAX_LINES"
  [ "$total" -gt "$MAX_LINES" ] && echo "... truncated; $((total - MAX_LINES)) more lines omitted — run validate.sh for the full result ..."
} >&2
exit 2
