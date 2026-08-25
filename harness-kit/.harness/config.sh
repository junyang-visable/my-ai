# shellcheck shell=bash
# =============================================================================
# .harness/config.sh — 每个仓库自己的接线点（唯一需要按栈修改的文件）
# -----------------------------------------------------------------------------
# 骨架不限栈：validate.sh / hooks 全部读这里的变量。
# 留空的命令会被自动跳过并打一条 info，不会让流水线失败。
# 命令用字符串写，validate 会用 `bash -c` 执行，可自由拼管道。
# =============================================================================

# --- harness 引擎目录（.harness 自身，一般不用改）--------------------------------
# 指向本 config.sh 所在目录，即 <repo>/.harness；feedback/ 脚本都挂在它下面。
HARNESS_ROOT="${HARNESS_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
export HARNESS_ROOT

# --- 阻断级（blocking）：失败必然让 validate 退出码非 0 ----------------------------
# 顺序即执行顺序，对齐 11020601776 的「build → lint-arch → test → verify 合成一条命令」。
HARNESS_LINT_CMD="${HARNESS_LINT_CMD:-}"            # 例: "pnpm -s lint"
HARNESS_TYPECHECK_CMD="${HARNESS_TYPECHECK_CMD:-}" # 例: "pnpm -s tsc --noEmit"
HARNESS_ARCH_LINT_CMD="${HARNESS_ARCH_LINT_CMD:-bash \"$HARNESS_ROOT/feedback/lint-arch.sh\"}"
HARNESS_BUILD_CMD="${HARNESS_BUILD_CMD:-}"          # 例: "pnpm -s build" —— 前端硬门禁：不可跳过
HARNESS_TEST_CMD="${HARNESS_TEST_CMD:-}"            # 例: "pnpm -s test -- --run"

# --- 警告级（warning）：默认不阻断，--strict 时才阻断 --------------------------------
HARNESS_STYLE_CMD="${HARNESS_STYLE_CMD:-}"          # 例: "pnpm -s prettier --check ."
HARNESS_LOCK_TESTS_CMD="${HARNESS_LOCK_TESTS_CMD:-python3 \"$HARNESS_ROOT/feedback/lock-tests.py\" verify}"

# --- 提示级（informational）：只打印，永不影响退出码 --------------------------------
HARNESS_INFO_CMDS=(
  # "echo \"bundle: $(du -sh dist 2>/dev/null | cut -f1)\""
)

# --- Testing Harness / E2E ---------------------------------------------------
HARNESS_E2E_CMD="${HARNESS_E2E_CMD:-}"              # 例: "pnpm -s cypress run --spec 'cypress/e2e/smoke/**'"
# 冒烟集：断言锁与 RED 校验作用的范围。用 glob，可多条空格分隔。
HARNESS_SMOKE_GLOB="${HARNESS_SMOKE_GLOB:-cypress/e2e/smoke/**/*.cy.*}"
# 失败证据落盘目录（相对项目根）。
HARNESS_EVIDENCE_DIR="${HARNESS_EVIDENCE_DIR:-.harness/tasks/_last/evidence}"

# --- 增量检查（post-edit 钩子用）：给一个文件路径，返回该文件应跑的快检命令 --------------
# 参数 $1 = 被编辑文件的绝对路径。空输出表示无需检查。
harness_incremental_cmd() {
  local f="$1"
  case "$f" in
    *.ts|*.tsx|*.js|*.jsx)
      [ -n "$HARNESS_LINT_CMD" ] && echo "$HARNESS_LINT_CMD --max-warnings=0 -- \"$f\"" ;;
    *.py)
      command -v ruff >/dev/null 2>&1 && echo "ruff check \"$f\"" ;;
    *.go)
      echo "gofmt -l \"$f\"" ;;
    *) : ;;
  esac
}

# --- workspace 模式：最后加载仓库专属配置 ----------------------------------------
# harness CLI 通过 HARNESS_CONF 指向 workspaces/<alias>.conf.sh，放在文件末尾加载，
# 保证其中的赋值覆盖上面的默认值。install 模式下该变量为空，此段无效果。
if [ -n "${HARNESS_CONF:-}" ] && [ -f "${HARNESS_CONF:-}" ]; then
  # shellcheck source=/dev/null
  source "$HARNESS_CONF"
fi

# 子进程（lock-tests.py / collect-evidence.sh 等）需要读到这些值，显式导出
export HARNESS_SMOKE_GLOB HARNESS_EVIDENCE_DIR HARNESS_E2E_CMD
