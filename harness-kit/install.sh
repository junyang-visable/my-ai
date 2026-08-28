#!/usr/bin/env bash
# =============================================================================
# install.sh — wire harness-kit into a target repo
# -----------------------------------------------------------------------------
# Design: engine (scripts) symlinks back to the kit for unified upgrades;
# config & content (config/context/rubric/tasks) are copied into the repo so
# each repo can evolve independently. Existing files are kept by default.
#
# Usage:
#   ./install.sh <target-repo-path> [--copy] [--force]
#     --copy  copy the engine too instead of symlinking (for offline distribution)
#     --force overwrite existing config/AGENTS etc. (dangerous; off by default)
# =============================================================================
set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET=""
MODE="symlink"
FORCE=0

while [ $# -gt 0 ]; do
  case "$1" in
    --copy) MODE="copy" ;;
    --force) FORCE=1 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    -*) echo "unknown flag: $1" >&2; exit 64 ;;
    *) TARGET="$1" ;;
  esac
  shift
done

[ -z "$TARGET" ] && { echo "usage: ./install.sh <target-repo-path> [--copy] [--force]"; exit 64; }
TARGET="$(cd "$TARGET" && pwd)"   # must already exist
echo "== wiring harness-kit → $TARGET (mode=$MODE) =="

link_or_copy() { # src dst
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ "$MODE" = "symlink" ]; then
    ln -sfn "$src" "$dst"
  else
    cp -f "$src" "$dst"
  fi
}

copy_keep() { # src dst — keep existing unless --force
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] && [ "$FORCE" -ne 1 ]; then
    echo "  keep  $dst (exists; --force overwrites)"
  else
    cp -Rf "$src" "$dst"; echo "  put   $dst"
  fi
}

# --- 1) engine scripts: symlink back to the kit --------------------------------
for f in feedback/validate.sh feedback/lint-arch.sh feedback/lock-tests.py \
         feedback/collect-evidence.sh hooks/post-edit.sh; do
  link_or_copy "$KIT_DIR/.harness/$f" "$TARGET/.harness/$f"
  echo "  wire  .harness/$f"
done
chmod +x "$KIT_DIR/.harness/feedback/"*.sh "$KIT_DIR/.harness/hooks/"*.sh 2>/dev/null || true

# --- 2) config & content: copied, per-repo editable -----------------------------
copy_keep "$KIT_DIR/.harness/config.sh"        "$TARGET/.harness/config.sh"
copy_keep "$KIT_DIR/.harness/context"          "$TARGET/.harness/context"
copy_keep "$KIT_DIR/.harness/rubric"           "$TARGET/.harness/rubric"
copy_keep "$KIT_DIR/.harness/tasks/_template"  "$TARGET/.harness/tasks/_template"

# --- 3) contract layer & docs ---------------------------------------------------
copy_keep "$KIT_DIR/templates/AGENTS.md" "$TARGET/AGENTS.md"
copy_keep "$KIT_DIR/templates/docs/ARCHITECTURE.md" "$TARGET/docs/ARCHITECTURE.md"
copy_keep "$KIT_DIR/templates/docs/DEVELOPMENT.md"  "$TARGET/docs/DEVELOPMENT.md"

# --- 4) skills & commands (agent-universal markdown; Qoder-style dirs, Claude Code copies to .claude/) ---
skdir="${QODER_SKILLS_DIR:-$HOME/.qoderwork/skills}"
mkdir -p "$skdir" "$TARGET/.qoder/commands"
for s in "$KIT_DIR"/skills/*/; do
  [ -d "$s" ] || continue
  name="$(basename "$s")"
  ln -sfn "$KIT_DIR/skills/$name" "$skdir/$name"
done
echo "  link  skills → $skdir/ (all)"
cp -f "$KIT_DIR/commands/"*.md "$TARGET/.qoder/commands/"
echo "  put   commands → $TARGET/.qoder/commands/ (Claude Code: copy to .claude/commands/; files are universal)"

# --- 5) wrap-up hints -----------------------------------------------------------
cat <<EOF

Wiring complete. Next 3 steps:
  1) edit $TARGET/.harness/config.sh — fill HARNESS_LINT_CMD / TEST_CMD / BUILD_CMD / E2E_CMD etc.
  2) fill $TARGET/AGENTS.md placeholders and red lines; extend docs/ as needed
  3) prove the guardrails: bash $TARGET/.harness/feedback/validate.sh selfcheck
     then the full run:  bash $TARGET/.harness/feedback/validate.sh
  once the smoke set is stable: python3 $TARGET/.harness/feedback/lock-tests.py update
EOF
