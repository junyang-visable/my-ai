# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
HARNESS_LINT_CMD="yarn lint"           # eslint --fix + stylelint --fix (repo convention: auto-fix on lint)
HARNESS_TYPECHECK_CMD="yarn typecheck" # vue-tsc for app + cypress tsconfigs (runs nuxi prepare first)
HARNESS_BUILD_CMD="yarn build"         # bin/env nuxi build — env vars all optional, runs without secrets
HARNESS_TEST_CMD="yarn test"           # nuxi prepare && vitest run

# Advisory
HARNESS_STYLE_CMD=""                   # stylelint already inside `yarn lint`

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""                     # cypress:run / playwright:test:local exist; scope per task
HARNESS_SMOKE_GLOB=""
