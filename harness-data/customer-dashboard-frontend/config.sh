# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
# Note: pnpm needs the private registry token from ~/.zshrc → wrap with `zsh -ic`.
# `pnpm lint:ci` only exists after FE-1063 (lint gates PR) merges; until then call eslint directly (same flags, no --fix).
# zsh -ic starts at kit cwd — commands must cd into the repo first.
HARNESS_LINT_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/customer-dashboard-frontend && pnpm exec eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --ignore-path .gitignore'"
HARNESS_TYPECHECK_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/customer-dashboard-frontend && pnpm type-check'" # vue-tsc --build --force
HARNESS_BUILD_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/customer-dashboard-frontend && pnpm build'"          # run-p type-check + vite build
HARNESS_TEST_CMD=""                               # no unit test files in repo

# Advisory
HARNESS_STYLE_CMD=""                              # prettier format script only writes; skip

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""                                # cypress scaffold only (example.cy.ts)
HARNESS_SMOKE_GLOB=""
