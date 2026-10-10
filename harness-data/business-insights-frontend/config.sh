# harness-kit project config — the ONLY file to adapt per stack.
# Commands run via `bash -c`; empty commands are skipped with an info line.
# Note: yarn 4 (vendored yarnPath .yarn/releases/yarn-4.10.3.cjs) reads GITHUB_TOKEN from env for
# npm.pkg.github.com auth (npmRegistries in .yarnrc.yml) → wrap with `zsh -ic` to load ~/.zshrc.
# CI: `yarn install --immutable` + `yarn lint` + `yarn test`. Verified from package.json scripts.
# zsh -ic starts at kit cwd — commands must cd into the repo first.
HARNESS_LINT_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/business-insights-frontend && yarn lint'"           # npm-run-all lint:{format,ts,types} = prettier + eslint + nuxi typecheck
HARNESS_TYPECHECK_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/business-insights-frontend && yarn lint:types'" # nuxi typecheck --noEmit
HARNESS_BUILD_CMD="zsh -ic 'cd /Users/yangjun/Desktop/project/business-insights-frontend && yarn build'"         # nuxi build (hard gate)
HARNESS_TEST_CMD=""                               # test = echo test (no real unit tests in repo)

# Advisory
HARNESS_STYLE_CMD=""                              # prettier check already part of lint (lint:format)

# E2E / smoke set (assertion-lock scope, globs relative to repo root)
HARNESS_E2E_CMD=""
HARNESS_SMOKE_GLOB=""
