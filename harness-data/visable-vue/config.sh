# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
# Note: yarn needs the private registry token from ~/.zshrc → wrap with `zsh -ic`.
# zsh -ic starts at kit cwd — commands must cd into the repo first.
# Stack: Vue 3 component library, yarn 1, vitest, Storybook. No TS typecheck script (plain JS + vue SFC).
HARNESS_LINT_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/visable-vue && yarn lint'"    # eslint && stylelint && prettier --check
HARNESS_TYPECHECK_CMD=""                                                                  # no typecheck script in package.json
HARNESS_BUILD_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/visable-vue && yarn build'"  # node build.js (hard gate)
HARNESS_TEST_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/visable-vue && yarn test:ci'" # vitest run

# Advisory
HARNESS_STYLE_CMD=""                              # `format` script writes files; skip

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""
HARNESS_SMOKE_GLOB=""
