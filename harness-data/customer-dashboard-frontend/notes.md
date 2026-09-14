# customer-dashboard-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in tasks/<task>/history.md under this dir;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- Vue 3.4 + TypeScript 5.4 + Vite 5 + Pinia 2, package manager **pnpm 9.15.0**
- Vue Router 4 (real routing in `src/router/`; `src/route.js` is a vendored vue-i18n-routing copy — dead, removed by FE-1064)
- UI: @visable-dev/vue + styleguide + design-tokens; styling via tailwindcss 3 + sass
- i18n: vue-i18n 9, locales synced via `pnpm translations:sync` (i18n-cli, tag company-overview)
- Monitoring: @visable-dev/monitoring-core + biz-webvital-plugin (init in `src/utils/monitoring.ts`); Sentry via @sentry/vue
- No unit tests; cypress is scaffold-only (`cypress/e2e/example.cy.ts`)
- `pnpm lint:ci` — eslint, no fix (CI gate, added by FE-1063)
- `pnpm type-check` — vue-tsc --build --force
- `pnpm build` — run-p type-check + vite build (hard gate)

## Pitfalls & conventions
- `.npmrc` references `${GITHUB_TOKEN}` → agent shell must wrap pnpm install with `zsh -ic` (token lives in ~/.zshrc); plain pnpm runs fine with warnings
- FE-1063 added lint/typecheck gates to the PR pipeline → both must stay green
- **FE-1063 is pushed but NOT merged (as of 2026-09-03)**: origin/main has no `lint:ci` script — gate via `pnpm exec eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --ignore-path .gitignore` (same flags, no --fix) until it merges
- `pnpm install` after dep changes prompts interactively to purge node_modules → run `CI=true pnpm install --no-frozen-lockfile` in agent shell (plain CI=true hits frozen-lockfile mismatch)
- `zsh -ic` starts in the kit cwd, not the repo — harness commands must `cd` into the repo explicitly
- eslint baseline on main: 5 warnings (App.vue ×3 unused imports, Progress.vue, SuggestedTasks.vue) — 0 errors; warnings don't fail the gate
- `@visable-dev/routing` is a transitive dep of `@visable-dev/vue` (via biz-launch-app-sdk) even after the direct dep was removed (FE-1064) — knip/depcheck will keep "finding" it installed; that's not a signal to re-add
- Branch/commit convention: `FE-XXXX/<short-desc>` from latest origin/main, ticket id in every commit message (FE-1042/FE-1064 pattern)

## CTOOL-679 round (2026-09-12)
- Banner integration pattern (no Nuxt — plain Vite+vue-router SPA): `src/utils/alibabaOnboardingApi.ts` (native fetch + credentials:include against same-origin gateway path) + `src/composables/useAlibabaOnboarding.ts` (13 ALIBABA_EVENTS + GA4 via `useContextStore().googleAnalytics4` — this store carries the tracker, NOT a nuxtApp plugin) + App.vue mount between header and main. Whole app is logged-in-only, so visibility = composable's fail-closed gate alone.
- GA4 payload here is free-form (`{event:'navigate', event_label, event_position}`) — unlike product-editor's typed EventSpecificPayloadGA4; don't copy types across repos.
- Dev symlink for unpublished visable-vue components: `rm -rf node_modules/@visable-dev/vue && ln -s ../../../../project/visable-vue node_modules/@visable-dev/vue` (repo sits one level deeper: Desktop/project/customer-dashboard-frontend). No test stage configured in harness (no unit tests) — eslint fallback + type-check + build are the gates.
- (CTOOL-679 design-align) Banner constrained to content width: wrap in `px-2 lg:px-4` outer + `mx-auto xl:max-w-[1440px]` inner (mirrors main's container classes exactly — note max-w only applies at xl in this app). Verify with getBoundingClientRect, not scaled screenshots.
