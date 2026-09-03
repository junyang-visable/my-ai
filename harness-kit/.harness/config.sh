# shellcheck shell=bash
# =============================================================================
# .harness/config.sh — per-repo wiring point (the only file to adapt per stack)
# -----------------------------------------------------------------------------
# The skeleton is stack-agnostic: validate.sh / hooks read only these variables.
# Empty commands are skipped automatically with an info line; the pipeline
# never fails because of them. Commands are strings executed via `bash -c`,
# so pipes are free to use.
# =============================================================================

# --- harness engine dir (.harness itself; rarely changed) ------------------------
# Points at the dir containing this config.sh, i.e. <repo>/.harness;
# the feedback/ scripts hang off it.
HARNESS_ROOT="${HARNESS_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
export HARNESS_ROOT

# --- blocking stages: any failure makes validate exit non-zero --------------------
# Order below is execution order: one composed command, lint → arch → build → test.
HARNESS_LINT_CMD="${HARNESS_LINT_CMD:-}"            # e.g. "pnpm -s lint"
HARNESS_TYPECHECK_CMD="${HARNESS_TYPECHECK_CMD:-}" # e.g. "pnpm -s tsc --noEmit"
HARNESS_ARCH_LINT_CMD="${HARNESS_ARCH_LINT_CMD:-bash \"$HARNESS_ROOT/feedback/lint-arch.sh\"}"
HARNESS_BUILD_CMD="${HARNESS_BUILD_CMD:-}"          # e.g. "pnpm -s build" — hard gate for frontends: cannot be skipped
HARNESS_TEST_CMD="${HARNESS_TEST_CMD:-}"            # e.g. "pnpm -s test -- --run"

# --- warning stages: non-blocking by default; blocking under --strict -------------
HARNESS_STYLE_CMD="${HARNESS_STYLE_CMD:-}"          # e.g. "pnpm -s prettier --check ."
HARNESS_LOCK_TESTS_CMD="${HARNESS_LOCK_TESTS_CMD:-python3 \"$HARNESS_ROOT/feedback/lock-tests.py\" verify}"

# --- informational stages: print only, never affect the exit code -----------------
HARNESS_INFO_CMDS=(
  # "echo \"bundle: $(du -sh dist 2>/dev/null | cut -f1)\""
)

# --- Testing Harness / E2E -------------------------------------------------------
HARNESS_E2E_CMD="${HARNESS_E2E_CMD:-}"              # e.g. "pnpm -s cypress run --spec 'cypress/e2e/smoke/**'"
# smoke set: the scope protected by the assertion lock and RED checks. Globs; space-separate multiple.
HARNESS_SMOKE_GLOB="${HARNESS_SMOKE_GLOB:-cypress/e2e/smoke/**/*.cy.*}"
# where failure evidence lands (relative to the repo root).
HARNESS_EVIDENCE_DIR="${HARNESS_EVIDENCE_DIR:-.harness/tasks/_last/evidence}"

# --- incremental checks (post-edit hook): given a file path, emit its quick-check command ----
# $1 = absolute path of the edited file. Empty output means "nothing to check".
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

# --- workspace mode: load the project's harness-data config last ----------------
# The harness CLI points HARNESS_CONF at the project's <hd>/<alias>/config.sh;
# loading it at the end of this file lets its assignments override the
# defaults above. In install mode that variable is empty and this block is a
# no-op.
if [ -n "${HARNESS_CONF:-}" ] && [ -f "${HARNESS_CONF:-}" ]; then
  # shellcheck source=/dev/null
  source "$HARNESS_CONF"
fi

# child processes (lock-tests.py / collect-evidence.sh …) need these values
export HARNESS_SMOKE_GLOB HARNESS_EVIDENCE_DIR HARNESS_E2E_CMD
