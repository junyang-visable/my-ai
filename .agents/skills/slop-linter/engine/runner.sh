#!/usr/bin/env bash
# slop-linter engine — deterministic mechanical layer (spec §5.1)
# NOTE: bash-3.2 compatible (this machine's /bin/bash is 3.2.57): no mapfile, no declare -A.
# Usage: runner.sh --repo <path> [--base <ref>] [--files <p1,p2>] [--out <file>]
# Exit: 0 = clean or nothing-to-lint · 1 = error-tier findings · 2 = usage/setup failure
set -euo pipefail

ENGINE_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
OXLINT_BIN="$ENGINE_DIR/node_modules/.bin/oxlint"
CONFIG="$ENGINE_DIR/oxlintrc.json"
die() { echo "runner: $*" >&2; exit 2; }

REPO="" BASE="" OUT="" FILES=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)  REPO="$2"; shift 2 ;;
    --base)  BASE="$2"; shift 2 ;;
    --files) FILES="$2"; shift 2 ;;
    --out)   OUT="$2"; shift 2 ;;
    *) die "unknown argument: $1" ;;
  esac
done
if [[ -z "$REPO" ]]; then die "--repo is required"; fi
if [[ ! -d "$REPO" ]]; then die "repo not found: $REPO"; fi
if [[ ! -f "$CONFIG" ]]; then die "config missing: $CONFIG"; fi
if [[ ! -x "$OXLINT_BIN" ]]; then die "oxlint not installed — run once: cd $ENGINE_DIR && npm install"; fi
REPO="$(cd "$REPO" && pwd)"

if [[ -z "$BASE" ]]; then
  DEFAULT="$(git -C "$REPO" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || true)"
  DEFAULT="${DEFAULT#origin/}"
  if [[ -z "$DEFAULT" ]]; then
    for c in main master; do
      if git -C "$REPO" show-ref --verify --quiet "refs/remotes/origin/$c"; then DEFAULT="$c"; break; fi
    done
  fi
  if [[ -z "$DEFAULT" ]]; then die "cannot resolve default branch — pass --base explicitly"; fi
  BASE="origin/$DEFAULT"
fi

DIRTY=false
if [[ -n "$(git -C "$REPO" status --porcelain)" ]]; then DIRTY=true; fi

# changed file set (bash 3.2: while-read into indexed array, no mapfile)
FILE_ARR=()
if [[ -n "$FILES" ]]; then
  while IFS= read -r f; do
    if [[ -n "$f" ]]; then FILE_ARR+=("$f"); fi
  done < <(printf '%s\n' "$FILES" | tr ',' '\n')
else
  while IFS= read -r f; do
    if [[ -n "$f" ]]; then FILE_ARR+=("$f"); fi
  done < <(git -C "$REPO" diff --name-only "$BASE"...HEAD | grep -E '\.(ts|tsx|js|mjs|cjs|jsx|vue)$')
fi

# changed line ranges, parallel indexed arrays (bash 3.2: no assoc arrays)
RANGE_FILES=()
RANGE_VALS=()
if [[ -z "$FILES" && ${#FILE_ARR[@]} -gt 0 ]]; then
  cur_file="" cur_ranges=""
  while IFS= read -r line; do
    if [[ "$line" == "+++ b/"* ]]; then
      if [[ -n "$cur_file" ]]; then RANGE_FILES+=("$cur_file"); RANGE_VALS+=("$cur_ranges"); fi
      cur_file="${line#+++ b/}"; cur_ranges=""
    elif [[ "$line" == "@@"* ]]; then
      plus="${line#*+}"; plus="${plus%% *}"
      start="${plus%%,*}"
      if [[ "$plus" == *,* ]]; then count="${plus#*,}"; else count=1; fi
      if [[ "$count" -eq 0 ]]; then continue; fi
      cur_ranges+="${start}-$((start + count - 1));"
    fi
  done < <(git -C "$REPO" diff --unified=0 "$BASE"...HEAD)
  if [[ -n "$cur_file" ]]; then RANGE_FILES+=("$cur_file"); RANGE_VALS+=("$cur_ranges"); fi
fi

emit() {
  if [[ -n "$OUT" ]]; then printf '%s\n' "$1" > "$OUT"; else printf '%s\n' "$1"; fi
}

# nothing to lint: MUST skip oxlint (zero paths would lint the whole cwd)
if [[ ${#FILE_ARR[@]} -eq 0 ]]; then
  emit "$(jq -nc --arg repo "$REPO" --arg base "$BASE" --arg head "$(git -C "$REPO" rev-parse --short HEAD)" \
    --argjson dirty "$DIRTY" \
    '{repo:$repo, base:$base, head:$head, dirty:$dirty, nothingToLint:true, files:[], diagnostics:[], oxlintExitCode:0}')"
  exit 0
fi

FILES_JSON="[]"
for f in "${FILE_ARR[@]}"; do
  r=""
  if [[ ${#RANGE_FILES[@]} -gt 0 ]]; then
    for i in "${!RANGE_FILES[@]}"; do
      if [[ "${RANGE_FILES[$i]}" == "$f" ]]; then r="${RANGE_VALS[$i]}"; break; fi
    done
  fi
  FILES_JSON="$(printf '%s' "$FILES_JSON" | jq -c --arg p "$f" --arg r "$r" \
    '. + [{path: $p, changedLines: (if $r == "" then [] else ($r | rtrimstr(";") | split(";") | map(split("-") | map(tonumber))) end)}]')"
done

set +e
OXLINT_OUT="$(cd "$REPO" && "$OXLINT_BIN" --config "$CONFIG" --disable-nested-config -f json "${FILE_ARR[@]}")"
OXLINT_RC=$?
set -e
# oxlint -f json 顶层是包装对象 {diagnostics:[...], ...}（spec §13 实测）——提取 diagnostics 数组
DIAG="$(printf '%s' "$OXLINT_OUT" | jq -c '.diagnostics' 2>/dev/null)"
if [[ -z "$DIAG" ]]; then die "oxlint output is not valid JSON or missing diagnostics — report explicitly, never silently skip (spec §11)"; fi
ERRORS="$(printf '%s' "$DIAG" | jq '[.[] | select(.severity == "error")] | length')"

emit "$(jq -nc --arg repo "$REPO" --arg base "$BASE" --arg head "$(git -C "$REPO" rev-parse --short HEAD)" \
  --argjson dirty "$DIRTY" --argjson files "$FILES_JSON" --argjson diag "$DIAG" --argjson rc "$OXLINT_RC" \
  '{repo:$repo, base:$base, head:$head, dirty:$dirty, nothingToLint:false, files:$files, diagnostics:$diag, oxlintExitCode:$rc}')"

if [[ "$ERRORS" -gt 0 ]]; then exit 1; else exit 0; fi
