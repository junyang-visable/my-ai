# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
# Note: npm needs tokens from ~/.zshrc (devDeps include github: refs) → wrap with `zsh -ic`.
# zsh -ic starts at kit cwd — commands must cd into the repo first.
# Stack: plain JS routing-constants lib, npm, jest, vite build.
HARNESS_LINT_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/routing-lib && npm run lint'"       # eslint .
HARNESS_TYPECHECK_CMD=""                                                                        # plain JS, no typecheck
HARNESS_BUILD_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/routing-lib && npm run build'"     # vite build (hard gate)
HARNESS_TEST_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/routing-lib && npm run test:ci'"    # jest

# Advisory
HARNESS_STYLE_CMD=""

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""
HARNESS_SMOKE_GLOB=""
