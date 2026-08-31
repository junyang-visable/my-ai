# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
HARNESS_LINT_CMD=""            # e.g. "pnpm -s lint"
HARNESS_TYPECHECK_CMD=""       # e.g. "pnpm -s tsc --noEmit"
HARNESS_BUILD_CMD=""           # e.g. "pnpm -s build" (hard gate for frontends)
HARNESS_TEST_CMD=""            # e.g. "pnpm -s test -- --run"

# Advisory
HARNESS_STYLE_CMD=""

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""             # e.g. "pnpm -s cypress run --spec 'cypress/e2e/smoke/**'"
HARNESS_SMOKE_GLOB="cypress/e2e/smoke/**/*.cy.*"
