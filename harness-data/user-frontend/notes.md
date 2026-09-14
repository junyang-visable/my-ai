# user-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in tasks/<task>/history.md under this dir;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- Nuxt 3 (`nuxi`), yarn 1, vitest, vue-tsc; app code under `src/` (views in `src/views/`, components in `src/components/`, locales in `src/locales` synced via i18n-cli tag `user-frontend`).
- All commands go through `bin/env` wrapper (env vars optional). lint = `yarn lint:js && yarn lint:css`; typecheck runs TWO vue-tsc passes (app tsconfig + root); build = `node build-service-workers && bin/env nuxi build`.
- yarn needs the private registry token from ~/.zshrc → wrap agent shells with `zsh -ic`, `cd` into the repo first.

## Pitfalls & conventions
- GA4 tracking: `src/plugins/tracking.client.ts` provides `$trackingGA4`; components call `useNuxtApp().$trackingGA4.click({...})` (see BackButton.vue / Security.vue patterns).
- My Account settings page = `src/views/SettingsPage.vue` composing `src/components/settings/*` cards (UserName, RoleAndTitle, Notifications, CompanyProfiles, PreferredLanguage, AccountInformation, Security, AccountDeletion); Security card owns the "Delete this account" row — the Alibaba delete entry lands next to it.
- Default branch: `main`.

## CTOOL-679 round (2026-09-12)
- **Baseline traps (environment, not code)**: a fresh checkout may miss `@visable-dev/monitoring-{core,server,vue}` in node_modules (sentry/monitoring TS errors, 2 sentry test failures, rollup "failed to resolve @visable-dev/monitoring-vue" build failure). `yarn install` fixes ALL of them — judge changes only after a full install.
- harness config commands MUST be `zsh -ic 'yarn <cmd>'` — plain `yarn` dies with "Environment variable not found (GITHUB_TOKEN)" because .yarnrc.yml reads it (token lives in ~/.zshrc).
- Security.vue Alibaba delete entry pattern: status fetch in onMounted with fail-closed catch; tap fires BOTH `$googleAnalytics.trackEvent` (UA legacy) and `$trackingGA4.click({event:'navigate', event_label, event_position:'security'})`, then greyed label state — deletion itself is CS-owned, frontend only logs.
- Favicon churn after build: `git restore -- src/public/` before staging.
