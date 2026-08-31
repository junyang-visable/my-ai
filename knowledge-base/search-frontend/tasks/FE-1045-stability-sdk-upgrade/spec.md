# spec — the implementer's technical design

> Standard mode: required. Minimal mode: keep only the clarification Q&A
> conclusions (no confirmed gate). For multi-app requirements this file *is*
> the design doc covering every involved app. You (the implementer) never see
> the acceptance Rubric (role isolation) — this file is **your** understanding
> of the requirement and your approach; the acceptance side judges
> independently, and the two get compared afterwards — mismatches are
> clarification signals.

- Task name / ID: FE-1045-stability-sdk-upgrade (Jira FE-1045, umbrella FE-1028)
- status: confirmed # draft / confirmed — confirmed must come from explicit user agreement; changes are demoted back by harness-change

## Involved apps

- App list: search-frontend (single app; SDK source monorepo frontend-monitoring is read-only reference, not modified)
- Per-app changes / boundaries: bump three dependency declarations + lockfile only; zero source-file changes in search-frontend
- Cross-app contracts (required for multi-app: interfaces / ordering / dependencies): n/a (single app)

## Requirement boundary

- Do:
  - Upgrade `@visable-dev/monitoring-core` `^2.2.0` → `^2.4.0` (installed 2.2.0 → 2.4.0)
  - Upgrade `@visable-dev/monitoring-server` `^2.1.0` → `^2.2.0` (installed 2.1.0 → 2.2.0)
  - Upgrade `@visable-dev/monitoring-vue` `^2.0.0` → `^2.0.3` (installed 2.0.0 → 2.0.3)
  - Refresh yarn.lock so all three resolve to the target versions (nested core copies under server/vue dedupe onto root core 2.4.0)
  - Run full local validation (lint / typecheck / build / vitest) and a local dev-server smoke
- Don't (explicitly excluded):
  - No `enableSlowCheck` config added anywhere — slow-API (`api_slow`) reporting intentionally stops (SDK 2.4.0 opt-in default; downstream error-regression detection already excludes `event_type = 'api_slow'`)
  - No new unit tests for the monitoring plugins (user decision: pure version upgrade)
  - No changes to `src/plugins/7.monitoring.*.ts`, `src/server/plugins/ssr-monitor.ts`, ErrorPage files, or any other source file — current adapters (appName/env/reporter only) stay as-is
  - No SDK-side changes (frontend-monitoring repo is reference only)
  - Staging/platform-side data-flow verification is out of scope (post-deploy, tracked under FE-1028 rollout)

## Approach

- Idea: minimal-diff dependency bump with behavior change consciously accepted rather than config-compensated; verification via typecheck (catches SDK API/signature drift) + build + existing suite + local init smoke
- Affected files / modules: `package.json` (3 dependency lines), `yarn.lock` (resolution entries). Nothing else.
- Risks & trade-offs:
  - `api_slow` data flow for search-frontend disappears from the stability data table — accepted (downstream metrics exclude it; ad-hoc slow-request analysis loses data)
  - 2.4.0/2.2.0/2.0.3 not yet confirmed published to npm.pkg.github.com (registry query needs GITHUB_TOKEN) — if `yarn install` cannot resolve, stop and re-confirm target with user
  - `yarn install` requires GITHUB_TOKEN in env (agent shell lacks it) — user must supply at code stage
  - Runtime behavior changes ride along silently: FE-1037 abort fix (fewer false `api_error` status:0), built-in noise filters (HubSpot/Bing UET/AWS WAF ignored) — no action needed, but release notes should mention them
  - peerDependencies of server 2.2.0 / vue 2.0.3 pin core exactly → all three must land together in one PR (they do)

## Plan

> Task breakdown lives elsewhere — see `plan.md` in this dir (harness-plan derives it from this spec).
> Once confirmed, the spec is frozen: execution drift goes into the plan; requirement changes go through harness-change, never direct edits here.

## Acceptance boundary (implementer's view)

- Observable behavior:
  - `yarn install` resolves the three packages at 2.4.0 / 2.2.0 / 2.0.3 (yarn.lock pinned; single deduped monitoring-core copy)
  - `bash <kit>/harness validate` exits green: lint, typecheck (app + cypress tsconfigs), build, full vitest suite
  - Local dev-server smoke: app boots, monitoring client SDK initializes (`$monitorSDK` provided), a `/web/metrics` report request fires on page load/error; SSR server adapter initializes without errors in server logs
  - `git status` shows only `package.json` + `yarn.lock` changed (branch `FE-1045/<short-desc>` off latest origin/main)
- Declared not covered (honest scope): staging deployment, platform-side data ingestion, production regression watch

## Change log

- 2026-08-31: spec drafted from Jira FE-1045 + clarification round (4 decisions: slow-check off accepted / no new tests / local observable acceptance boundary / caret declarations)
