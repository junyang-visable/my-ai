#!/usr/bin/env bash
# =============================================================================
# .harness/feedback/lint-arch.sh — architecture dependency-violation check (blocking)
# -----------------------------------------------------------------------------
# Stack-agnostic implementation: grep rules matching "cross-layer dependencies
# that must not exist". One rule per line, format:
#   <protected path glob>\t<forbidden regex>\t<human-readable reason>
# A hit => print file:line + reason + fix suggestion, exit 1.
#
# In a real project, replace this with a native tool (dependency-cruiser /
# import-linter / go list …). validate.sh only cares about the exit code and
# the "file:line | reason | fix" format, never the implementation.
# =============================================================================
set -uo pipefail
shopt -s globstar nullglob 2>/dev/null || true

SCAN_ROOT="${HARNESS_ARCH_SCAN_ROOT:-.}"

# ---- rule table: add/remove as needed. One generic example by default ----------
# Three columns separated by real TABs.
RULES=$(cat <<'RULES'
src/domain/**	(from|import|require).*(infra|infrastructure)/	the domain layer must not depend on the infrastructure layer directly (invert via interfaces/ports)
src/**	FORBIDDEN_CROSS_LAYER	explicit cross-layer ban marker hit
RULES
)

fail=0
c_red=$'\033[31m'; c_dim=$'\033[2m'; c_rst=$'\033[0m'

while IFS=$'\t' read -r glob pattern reason; do
  [ -z "${glob:-}" ] && continue
  # expand the glob into a file list
  while IFS= read -r file; do
    [ -f "$file" ] || continue
    matches="$(grep -nE "$pattern" "$file" 2>/dev/null || true)"
    [ -z "$matches" ] && continue
    while IFS= read -r m; do
      line="${m%%:*}"
      printf "%sBLOCKING%s | arch | %s:%s | %s\n" "$c_red" "$c_rst" "$file" "$line" "$reason"
      printf "         %s↳ fix: remove the dependency or go through an abstract interface; for a deliberate exception explain in review and adjust the rules%s\n" "$c_dim" "$c_rst"
      fail=1
    done <<< "$matches"
  done < <(cd "$SCAN_ROOT" 2>/dev/null && compgen -G "$glob" 2>/dev/null | sed "s#^#$SCAN_ROOT/#" || true)
done <<< "$RULES"

if [ "$fail" -ne 0 ]; then
  exit 1
fi
echo "arch: no cross-layer violations"
exit 0
