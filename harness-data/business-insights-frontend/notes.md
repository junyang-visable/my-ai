# business-insights-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in the harness-data root's tasks/<task>/history.md;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- (lint / typecheck / build / test commands that actually work here, plus known quirks)

## Pitfalls & conventions
- (selector conventions, env vars, deployment, landmines to avoid…)
- Nuxt 3 (nuxi) + yarn 4 (vendored yarnPath .yarn/releases/yarn-4.10.3.cjs, nodeLinker: node-modules, yarn.lock).
- Private registry: .yarnrc.yml maps @visable-dev to npm.pkg.github.com with `npmAuthToken: "${GITHUB_TOKEN}"` → installs must run via `zsh -ic` to load the token.
- Header: direct VisPageHeader import in layouts/default.vue + module declarations in types/visable.d.ts (prop-level types not declared).
- No unit tests (`test: echo test`); quality gates = yarn lint (prettier+eslint+nuxi typecheck) + yarn build.
- Default branch: **master** (not main). In-flight beta-bump PRs exist (CTOOL-636 #323, CTOOL-679 #324) — coordinate before merging dep upgrades.

## CTOOL-718 round (2026-10-09)
- Dependency-bump verified clean: exact-pin routing 22.10.0 + vue 43.44.0 → `zsh -ic 'yarn install'` (Done in 16s) → `yarn install --immutable` exit 0 → validate all green (lint/build; test stage is `echo test`). yarn.lock uses a merged key: `@visable-dev/routing@npm:22.10.0, @visable-dev/vue@npm:43.44.0`.
- **Favicon build noise**: `nuxi build` regenerates 9 tracked `public/**/favicons/*` files (SVG attr reorder + PNG re-encode, content-equivalent) — a `git add -A` commit caught them and needed `git checkout origin/master -- public/` + `git commit --amend` (run via a bash script file in Qoder sandbox). ALWAYS commit with explicit paths after any build.
