#!/bin/bash
# Scan local git repos for commits since a date, grouped by repo.
# Usage: scan_git.sh <since-date YYYY-MM-DD> [--all-authors] [root-dir...]
# Default roots: ~/Desktop/project ~/Desktop/my-ai ~/Documents (one level deep)
# Default author filter: "Jun Yang"; --all-authors lists every author.

SINCE="$1"; shift || true
AUTHOR="Jun Yang"
if [ "$1" = "--all-authors" ]; then
  AUTHOR=""
  shift
fi

ROOTS=("$@")
if [ ${#ROOTS[@]} -eq 0 ]; then
  ROOTS=("$HOME/Desktop/project" "$HOME/Desktop/my-ai" "$HOME/Documents")
fi

AUTH_FILTER=()
if [ -n "$AUTHOR" ]; then
  AUTH_FILTER=(--author="$AUTHOR")
fi

for root in "${ROOTS[@]}"; do
  [ -d "$root" ] || continue
  for d in "$root"/*/; do
    [ -d "${d}.git" ] || continue
    log=$(git -C "$d" log --all --since="$SINCE" "${AUTH_FILTER[@]}" \
      --pretty=format:"%h|%ad|%an|%s" --date=short 2>/dev/null)
    if [ -n "$log" ]; then
      printf '=== %s\n%s\n' "$d" "$log"
    fi
  done
done
