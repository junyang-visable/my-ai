# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
# Note: pnpm needs the private registry token from ~/.zshrc → wrap with `zsh -ic`.
# zsh -ic starts at kit cwd — commands must cd into the repo first.
# Stack: Nuxt 3 (nuxi), pnpm, vitest. Scripts verified from package.json @ v1.0.1.
HARNESS_LINT_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/product-editor-frontend && pnpm lint'"           # eslint && prettier --check .
HARNESS_TYPECHECK_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/product-editor-frontend && pnpm typecheck'" # nuxi typecheck
HARNESS_BUILD_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/product-editor-frontend && pnpm build'"         # nuxi build (hard gate)
HARNESS_TEST_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/product-editor-frontend && pnpm test:ci'"        # vitest run --silent

# Advisory
HARNESS_STYLE_CMD=""                              # `format` script writes files; skip

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""
HARNESS_SMOKE_GLOB=""
