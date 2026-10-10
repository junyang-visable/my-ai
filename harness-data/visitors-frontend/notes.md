# visitors-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in the harness-data root's tasks/<task>/history.md;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- (lint / typecheck / build / test commands that actually work here, plus known quirks)

## Pitfalls & conventions
- (selector conventions, env vars, deployment, landmines to avoid…)
- Nuxt 3 (nuxi) + npm (package-lock.json; CI runs `npm clean-install`). package.json has a vestigial `packageManager: pnpm@9.15.0` — ignore it, CI and lockfile are npm.
- Private registry: repo `.npmrc` points `@visable-dev` scope to npm.pkg.github.com; auth token via GITHUB_TOKEN (~/.zshrc → wrap installs with `zsh -ic`).
- Header comes from `VisBackOfficeLayout` (@visable-dev/vue) in layouts/default.vue — no direct VisPageHeader usage.
- Snapshot tests exist (13 .snap files on main); dependency upgrades that change scoped-style hashes require snapshot refresh (vitest -u after review).
- Default branch: main. In-flight beta-bump PRs exist (CTOOL-636 #247, CTOOL-679 #248) — coordinate before merging dep upgrades.

## CTOOL-718 round (2026-10-09)
- Dependency-bump verified clean: exact-pin routing `^22.7.3 → 22.10.0` + vue `43.41.1 → 43.44.0` → `zsh -ic 'npm install'` exit 0 → validate all green (vitest 31 files / 460 passed + 4 skipped). **Zero `.snap` changes despite 13 .snap files** — VF snapshots do NOT capture scoped-style hashes, so header-package bumps need no refresh here (unlike SO #590).
- Qoder background terminals can share/lose output buffers (one parallel test run's output vanished) — rerun evidence-critical commands in the foreground.
