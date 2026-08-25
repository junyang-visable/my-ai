#!/usr/bin/env bash
# =============================================================================
# install.sh — 把 harness-kit 接入一个目标仓库
# -----------------------------------------------------------------------------
# 设计：引擎(脚本)软链回 kit，便于统一升级；配置与内容(config/context/rubric/tasks)
# 拷贝进仓库，各仓库独立可改。已存在的文件默认不覆盖。
#
# 用法:
#   ./install.sh <目标仓库路径> [--copy] [--force]
#     --copy  引擎也拷贝而非软链（离线分发用）
#     --force 覆盖已存在的 config/AGENTS 等（危险，默认关）
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

[ -z "$TARGET" ] && { echo "用法: ./install.sh <目标仓库路径> [--copy] [--force]"; exit 64; }
TARGET="$(cd "$TARGET" && pwd)"   # 必须已存在
echo "== 接入 harness-kit → $TARGET （mode=$MODE）=="

link_or_copy() { # src dst
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ "$MODE" = "symlink" ]; then
    ln -sfn "$src" "$dst"
  else
    cp -f "$src" "$dst"
  fi
}

copy_keep() { # src dst  —— 已存在则保留（除非 --force）
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] && [ "$FORCE" -ne 1 ]; then
    echo "  keep  $dst（已存在，--force 可覆盖）"
  else
    cp -Rf "$src" "$dst"; echo "  put   $dst"
  fi
}

# --- 1) 引擎脚本：软链回 kit --------------------------------------------------
for f in feedback/validate.sh feedback/lint-arch.sh feedback/lock-tests.py \
         feedback/collect-evidence.sh hooks/post-edit.sh; do
  link_or_copy "$KIT_DIR/.harness/$f" "$TARGET/.harness/$f"
  echo "  wire  .harness/$f"
done
chmod +x "$KIT_DIR/.harness/feedback/"*.sh "$KIT_DIR/.harness/hooks/"*.sh 2>/dev/null || true

# --- 2) 配置与内容：拷贝，仓库独立可改 -------------------------------------------
copy_keep "$KIT_DIR/.harness/config.sh"        "$TARGET/.harness/config.sh"
copy_keep "$KIT_DIR/.harness/context"          "$TARGET/.harness/context"
copy_keep "$KIT_DIR/.harness/rubric"           "$TARGET/.harness/rubric"
copy_keep "$KIT_DIR/.harness/tasks/_template"  "$TARGET/.harness/tasks/_template"

# --- 3) 契约层与 docs ---------------------------------------------------------
copy_keep "$KIT_DIR/templates/AGENTS.md" "$TARGET/AGENTS.md"
copy_keep "$KIT_DIR/templates/docs/ARCHITECTURE.md" "$TARGET/docs/ARCHITECTURE.md"
copy_keep "$KIT_DIR/templates/docs/DEVELOPMENT.md"  "$TARGET/docs/DEVELOPMENT.md"

# --- 4) 技能与命令（agent 通用 markdown；目录按 Qoder 习惯，Claude Code 复制到 .claude/ 即可）---
skdir="${QODER_SKILLS_DIR:-$HOME/.qoderwork/skills}"
mkdir -p "$skdir" "$TARGET/.qoder/commands"
for s in "$KIT_DIR"/skills/*/; do
  [ -d "$s" ] || continue
  name="$(basename "$s")"
  ln -sfn "$KIT_DIR/skills/$name" "$skdir/$name"
done
echo "  link  技能 → $skdir/（全部）"
cp -f "$KIT_DIR/commands/"*.md "$TARGET/.qoder/commands/"
echo "  put   命令 → $TARGET/.qoder/commands/（Claude Code 复制到 .claude/commands/，文件通用）"

# --- 5) 收尾提示 --------------------------------------------------------------
cat <<EOF

接入完成。接下来 3 步：
  1) 编辑 $TARGET/.harness/config.sh —— 填 HARNESS_LINT_CMD / TEST_CMD / BUILD_CMD / E2E_CMD 等
  2) 填 $TARGET/AGENTS.md 的 <占位> 与红线；按需补 docs/
  3) 验证护栏本身： bash $TARGET/.harness/feedback/validate.sh selfcheck
     再跑一次全套： bash $TARGET/.harness/feedback/validate.sh
  冒烟集稳定后： python3 $TARGET/.harness/feedback/lock-tests.py update
EOF
