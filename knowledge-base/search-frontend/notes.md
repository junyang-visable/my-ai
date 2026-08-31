# search-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in tasks/<task>/history.md under this dir;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- Nuxt 3 / Vue 3 SSR app (`nuxi`), yarn berry 3.6.1 with `nodeLinker: node-modules`.
- Commands (all go through `bin/env` which rewrites optional env vars — every var is
  guarded by `[[ "$X" != "" ]]`, so lint/typecheck/build/test run locally without secrets):
  - `yarn lint` (eslint+stylelint, both `--fix` — auto-fix on lint is repo convention)
  - `yarn typecheck` (vue-tsc ×2: app tsconfig + cypress tsconfig; `nuxi prepare` first)
  - `yarn build` (`bin/env nuxi build`)
  - `yarn test` (`nuxi prepare && vitest run`)
- `@visable-dev/*` packages resolve from **npm.pkg.github.com** — `.yarnrc.yml` requires
  `GITHUB_TOKEN` in env for **any** yarn command (install, build, test — the
  `${GITHUB_TOKEN}` expansion is evaluated on every yarn invocation), not just installs.
  Agent shells don't have it: wrap commands with `zsh -ic '<cmd>'` to load the user's rc,
  otherwise they die with "Environment variable not found (GITHUB_TOKEN)".
  Token landmine (2026-08-31): classic PATs older than 60 days are forbidden by the
  Visable GmbH enterprise on npm.pkg.github.com (403 on packument AND tarball endpoints;
  error body names the offending token id). Rotating to a ≤60-day classic PAT with
  `read:packages` fixed it. `~/.npmrc` also stores an auth token for this registry —
  keep it in sync when rotating.
- E2E: `playwright:test:local` (local-replay scenario) and `cypress:run` exist.

## Pitfalls & conventions
- Stability SDK (`@visable-dev/monitoring-{core,server,vue}`) touchpoints:
  - `src/plugins/7.monitoring.client.ts` — `createNuxtClientAdapter` + `setCustomReportContext({pageId})` per route
  - `src/plugins/7.monitoring.server.ts` — `createNuxtServerAdapter` + `setCustomReportContext` on `page:start`
  - `src/server/plugins/ssr-monitor.ts` — `setupNitroRenderHooks(nitroApp)`
  - `src/views/ErrorPage.vue` + `src/OldSearch/views/ErrorPage.vue` — `$monitorSDK.reportWhiteScreen(...)`
- SDK transport is `navigator.sendBeacon` (core Reporter.ts) → in browser devtools
  network panel these report requests show as resource type **"ping"**, not
  xhr/fetch — filtering by xhr/fetch makes them invisible. Report path:
  `POST /web/metrics`. Local dev returns **404** for it — the app's own server
  has no such route (no refs in `src/server/` or nuxt.config.ts); production
  infra receives it. Request *firing* is the smoke-pass evidence.
- No unit tests exist for the `7.monitoring.*` plugins ( neighbours like
  `tests/plugins/webvital.client.spec.ts` are the pattern to copy).
- `src/OldSearch/` duplicates parts of `src/` (types, views) — changes usually need both trees.
- SDK source monorepo: `~/Desktop/project/frontend-monitoring` (pnpm; packages/core|server|vue).
  On main as of 2026-08-31: core 2.4.0 / server 2.2.0 / vue 2.0.3. Publishes via GitHub
  workflow (npm_publish), git tags are stale — don't rely on tags for latest version.
- Repo publishes/deploys via PR to main; commit style: conventional-ish prefixes
  (`fix(ci):`, `feat:`, plain `PGS-905: ...` also seen).
