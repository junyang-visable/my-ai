# homepage-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in tasks/<task>/history.md under this dir;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- Nuxt 3 / Vue 3 SSR app (`nuxi`), yarn berry with `nodeLinker: node-modules`, config in `nuxt.config.js` + custom `routes.js` (not src/pages).
- Commands (all go through `bin/env`; env vars optional — runs without secrets):
  - `yarn lint` (`lint:js` + `lint:css`, both `--fix` — auto-fix on lint is repo convention)
  - `yarn typecheck` (vue-tsc ×2: app tsconfig + cypress tsconfig; `nuxi prepare` first)
  - `yarn build` (`bin/env nuxi build`)
  - `yarn test` (`nuxi prepare && vitest run --coverage`)
- `@visable-dev/*` packages resolve from **npm.pkg.github.com** — `.yarnrc.yml` requires
  `GITHUB_TOKEN` in env for **any** yarn command; agent shells lack it — wrap with
  `zsh -ic '<cmd>'` (loads user rc). Classic PATs >60 days are 403-blocked by the
  Visable enterprise policy (see search-frontend notes for the full incident).
- E2E: `cypress:run` exists; no `cypress/e2e/smoke/` set (only `showroom.cy.ts`).
- Default branch: `main`.

## Pitfalls & conventions
- Stability SDK (`@visable-dev/monitoring-{core,server,vue}`) touchpoints:
  - `src/plugins/7.monitoring.client.ts` — `createNuxtClientAdapter` + `setCustomReportContext({pageId})` per route
  - `src/plugins/7.monitoring.server.ts` — `createNuxtServerAdapter` + `setCustomReportContext` on `page:start`
  - `src/server/plugins/ssr-monitor.ts` — `setupNitroRenderHooks(nitroApp)`
  - `src/views/ErrorPage.vue`, `src/components/showroom/{Results,SeoFooterModule}.vue` — `$monitorSDK` usages
  - Adapters identical to search-frontend's (appName/env only) — see FE-1045 spec.
- Routes come from `routes.js` (getLocalizedRoutes + explicit path table); home is `/` → `src/views/HomePage.vue`.
- Repo publishes/deploys via PR to main; conventional commit prefixes (`feat:`, `chore(deps):` …).

## Stability SDK observability (verified FE-1045, 2026-08-31)
- **Inner reports are env-gated**: monitoring-core ≥2.3.2 `Reporter.sendToHttpEndpoint` returns early unless
  env ∈ {staging, production}. Dev runs `runtimeConfig.public.stage = 'development'` → **zero** /web/metrics
  from the SDK, by design. To exercise the report path locally: `STAGE=staging zsh -ic 'yarn dev --port <p>'`
  (bin/env maps STAGE → NUXT_PUBLIC_STAGE). Gate added in release-2.3.2 (frontend-monitoring commit 6644b09).
- **/web/metrics has two writers** — don't judge by URL alone:
  - stability SDK → `{"type":"stability_monitor",...}` (env-gated; navigator.sendBeacon, shows as "ping")
  - @visable-dev/tracking GA-event mirrors → `{"type":"stability","data":{"gaEventAction":...}}` (any env,
    fires in pairs per event) — these fooled part-1's search-frontend smoke reading.
- SDK runtime introspection: `$monitorSDK` via `document.querySelector('#__nuxt').__vue_app__.config.globalProperties`
  — `sdk.config.env`, `sdk.reporter.env` (console-patching `sdk.reporter.env='staging'` opens the gate without
  restarting the server).
