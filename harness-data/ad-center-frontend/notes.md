# ad-center-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in the harness-data root's tasks/<task>/history.md;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- (lint / typecheck / build / test commands that actually work here, plus known quirks)

## Pitfalls & conventions
- (selector conventions, env vars, deployment, landmines to avoid…)
- Nuxt 3 (nuxi) + npm (package-lock.json; CI runs `npm clean-install`); no packageManager field.
- Private registry: repo `.npmrc` points `@visable-dev` scope to npm.pkg.github.com; auth token via GITHUB_TOKEN (~/.zshrc → wrap installs with `zsh -ic`).
- Header comes from `VisBackOfficeLayout` (@visable-dev/vue) in layouts/default.vue — no direct VisPageHeader usage.
- Snapshot tests exist (2 .snap files on main); scoped-style hash changes may require snapshot refresh.
- Default branch: main. In-flight beta-bump PRs exist (CTOOL-636 #79, CTOOL-679 #80) — coordinate before merging dep upgrades.

## CTOOL-718 round (2026-10-09)
- Dependency-bump verified clean: exact-pin routing `^22.4.0 → 22.10.0` + vue `^43.0.1 → 43.44.0` (biggest lineage jump in the CTOOL-718 batch) → `zsh -ic 'npm install'` exit 0 → validate all green (vitest 24 files / 252 tests). Zero `.snap` changes — the 2 .snap files don't capture scoped-style hashes.
