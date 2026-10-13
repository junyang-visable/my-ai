# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
HARNESS_LINT_CMD="yarn lint"            # eslint . (repo AGENTS.md verification set)
HARNESS_TYPECHECK_CMD="yarn typecheck"  # nuxi typecheck -> vue-tsc
HARNESS_BUILD_CMD="yarn build"          # bin/env nuxi build — env vars all optional
HARNESS_TEST_CMD="yarn test:nowatch"    # vitest run (plain `yarn test` is watch mode — avoid)

# Advisory
HARNESS_STYLE_CMD=""                    # prettier via lint-staged on commit

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""                      # no cypress/playwright in this repo
HARNESS_SMOKE_GLOB=""
