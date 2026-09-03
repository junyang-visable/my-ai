# unified-search-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in tasks/<task>/history.md under this dir;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- Nuxt 3 / Vue 3 SSR app (`nuxi`), yarn berry `nodeLinker: node-modules`, config in `nuxt.config.ts` + `routes.js` (not src/pages).
- Commands (all via `bin/env` wrapper):
  - `yarn lint` (`lint:js` + `lint:css`, both `--fix` — auto-fix on lint is repo convention)
  - `yarn typecheck` (`nuxi prepare && vue-tsc --noEmit --skipLibCheck --project tsconfig.json` — single tsconfig, no cypress tsconfig)
  - `yarn build` (`bin/env nuxi build`)
  - `yarn test` (`nuxi prepare && vitest run --reporter=basic`)
- `@visable-dev/*` packages resolve from **npm.pkg.github.com** — `.yarnrc.yml` requires
  `GITHUB_TOKEN` in env for **any** yarn command; agent shells lack it — wrap with
  `zsh -ic '<cmd>'` (loads user rc). Classic PATs >60 days are 403-blocked by the
  Visable enterprise policy (see search-frontend notes for the full incident).
- No cypress smoke set; default branch: `master` (local checkout may sit on feature branches, e.g. access-monitoring).

## Pitfalls & conventions
- Stability SDK (`@visable-dev/monitoring-{core,server,vue}`) touchpoints:
  - `src/plugins/8.monitoring.client.ts` / `src/plugins/8.monitoring.server.ts` — plugin number prefix is **8** here (7 in search/homepage)
  - `src/server/plugins/ssr-monitor.ts` — `setupNitroRenderHooks(nitroApp)`
  - Adapters identical to search-frontend's (appName/env only) — see FE-1045 spec.
- node_modules was missing the monitoring-* packages entirely before FE-1045's install
  (stale install state) — fresh `yarn install` after bump pulls them in.
- Routes come from `routes.js`; home is `/` (home_root).

## Stability SDK observability (verified pattern from search/homepage, FE-1045)
- **Inner reports are env-gated**: monitoring-core ≥2.3.2 only POSTs /web/metrics when env ∈ {staging, production};
  dev defaults to stage='development' → SDK sends nothing locally. To exercise: `STAGE=staging zsh -ic 'yarn dev --port <p>'`.
- **/web/metrics has two writers**: SDK (`"type":"stability_monitor"`, env-gated) vs tracking-layer GA mirrors
  (`"type":"stability"`, any env) — assert on payload type, not URL alone.
- SDK introspection: `$monitorSDK` via `document.querySelector('#__nuxt').__vue_app__.config.globalProperties`;
  `sdk.reporter.env='staging'` opens the gate without a server restart.
- **Reporter flushes on a ~60s interval** (verified 2026-08-31, FE-1045): an injected error's beacon landed
  ~56s after injection — a few seconds' wait shows nothing. Re-poll the DevTools network list instead.
  sendBeacon requests also never appear in `performance.getEntriesByType('resource')` — counting them via
  the Performance API always returns 0; use the network panel only.
- `reporter.enableInnerReport` lives at `sdk.config.reporter.enableInnerReport` (nested), not `sdk.config.enableInnerReport`.
- Organic `resource_load_failed` beacons (hotjar ORB-block, cookiebot 404) usually fire on page load —
  useful as passive smoke evidence before injecting anything.
