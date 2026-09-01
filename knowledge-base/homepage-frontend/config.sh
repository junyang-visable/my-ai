# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
HARNESS_LINT_CMD="yarn lint"           # lint:js + lint:css (eslint --fix --cache + stylelint --fix; repo convention: auto-fix on lint)
HARNESS_TYPECHECK_CMD="yarn typecheck" # nuxi prepare && vue-tsc ×2 (app + cypress tsconfigs)
HARNESS_BUILD_CMD="yarn build"         # bin/env nuxi build — env vars optional, runs without secrets
HARNESS_TEST_CMD="yarn test"           # nuxi prepare && vitest run --coverage

# Advisory
HARNESS_STYLE_CMD=""                   # stylelint already inside `yarn lint:css`

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""                     # cypress:run exists; scope per task
HARNESS_SMOKE_GLOB=""                  # no cypress/e2e/smoke/ set in this repo (only showroom.cy.ts)
