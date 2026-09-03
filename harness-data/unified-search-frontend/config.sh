# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
HARNESS_LINT_CMD="yarn lint"            # lint:js + lint:css with --fix (repo convention)
HARNESS_TYPECHECK_CMD="yarn typecheck"  # vue-tsc (single tsconfig)
HARNESS_BUILD_CMD="yarn build"          # hard gate for frontends
HARNESS_TEST_CMD="yarn test"            # vitest run

# Advisory
HARNESS_STYLE_CMD=""

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""             # no cypress smoke set configured
HARNESS_SMOKE_GLOB=""
