# spec — the implementer's technical design

> Standard mode: required. Minimal mode: keep only the clarification Q&A
> conclusions (no confirmed gate). For multi-app requirements this file *is*
> the design doc covering every involved app. You (the implementer) never see
> the acceptance Rubric (role isolation) — this file is **your** understanding
> of the requirement and your approach; the acceptance side judges
> independently, and the two get compared afterwards — mismatches are
> clarification signals.

- Task name / ID: FE-1045-stability-sdk-upgrade (Jira FE-1045, umbrella FE-1028)
- status: confirmed # re-confirmed 2026-08-31 after 3-repo scope extension (was demoted to draft by harness-change, user re-confirmed same day)

## Involved apps

- App list: search-frontend (part 1, done — PR visable-dev/search-frontend#483), homepage-frontend (part 2), unified-search-frontend (part 3). SDK source monorepo frontend-monitoring is read-only reference, not modified.
- Per-app changes / boundaries: identical pure version bump per app — three dependency declarations + lockfile only, zero source-file changes in each repo.
  - search-frontend: DONE (commit 753882b2, branch FE-1045/stability-sdk-upgrade, PR #483 open; keep as-is, no follow-up commits)
  - homepage-frontend: bump off latest origin/main; touchpoints `src/plugins/7.monitoring.{client,server}.ts`, `src/server/plugins/ssr-monitor.ts` stay untouched
  - unified-search-frontend: bump off latest origin/master (local checkout currently on `access-monitoring`, clean tree — branch base is master per convention); touchpoints `src/plugins/8.monitoring.{client,server}.ts`, `src/server/plugins/ssr-monitor.ts` stay untouched
- Cross-app contracts (required for multi-app: interfaces / ordering / dependencies): three independent repos → three independent PRs, all referencing FE-1045. No code-level coupling, no merge/deploy ordering constraint (each repo releases on its own cadence; SDK peerDependencies pin within each repo's lockfile, not across repos). All three lockfiles must resolve the same targets: core ^2.4.0 / server ^2.2.0 / vue ^2.0.3.

## Requirement boundary

- Do:
  - Upgrade `@visable-dev/monitoring-core` `^2.2.0` → `^2.4.0` in all three repos
  - Upgrade `@visable-dev/monitoring-server` `^2.1.0` → `^2.2.0` in all three repos
  - Upgrade `@visable-dev/monitoring-vue` `^2.0.0` → `^2.0.3` in all three repos
  - Refresh each repo's yarn.lock so all three resolve to the target versions (nested core copies dedupe onto root core 2.4.0)
  - Register homepage-frontend and unified-search-frontend as harness workspaces (config.sh + notes.md each) before code stage
  - Run per-repo full local validation (lint / typecheck / build / vitest) and a local dev-server smoke
  - search-frontend part 1 is already delivered — not re-done
- Don't (explicitly excluded, per repo):
  - No `enableSlowCheck` config added anywhere — slow-API (`api_slow`) reporting intentionally stops (SDK 2.4.0 opt-in default; downstream error-regression detection already excludes `event_type = 'api_slow'`)
  - No new unit tests for the monitoring plugins (user decision: pure version upgrade)
  - No changes to monitoring plugins, ssr-monitor.ts, ErrorPage files, or any other source file — current adapters (appName/env only, identical across all three repos, verified) stay as-is; Jira's "Align SDK initialization and configuration where needed" is satisfied by the bump alone
  - No SDK-side changes (frontend-monitoring repo is reference only)
  - Staging/platform-side data-flow verification is out of scope (post-deploy, tracked under FE-1028 rollout)

## Approach

- Idea: minimal-diff dependency bump replicated across three structurally identical Nuxt apps; verification via typecheck (catches SDK API/signature drift) + build + existing suite + local init smoke, per repo
- Affected files / modules: per repo `package.json` (3 dependency lines) + `yarn.lock` (resolution entries). Nothing else. Plus kit-side: 2 new workspace registrations.
- Risks & trade-offs:
  - `api_slow` data flow disappears from the stability data table for all three apps — accepted (same reasoning as part 1)
  - `yarn install` in both new repos requires GITHUB_TOKEN in env — user's ≤60-day classic PAT works (proven in part 1); wrap agent commands with `zsh -ic`
  - Runtime behavior changes ride along silently (FE-1037 abort fix, built-in noise filters) — no action needed, release notes should mention them
  - peerDependencies of server 2.2.0 / vue 2.0.3 pin core exactly → all three packages land together in each repo's PR (they do)
  - unified-search-frontend is currently checked out on `access-monitoring` (clean) — switching to a new branch off origin/master is safe; the old branch stays untouched

## Plan

> Task breakdown lives elsewhere — see `plan.md` in this dir (harness-plan derives it from this spec).
> Once confirmed, the spec is frozen: execution drift goes into the plan; requirement changes go through harness-change, never direct edits here.

## Acceptance boundary (implementer's view)

- Observable behavior (per repo, homepage-frontend and unified-search-frontend):
  - `yarn install` resolves the three packages at 2.4.0 / 2.2.0 / 2.0.3 (yarn.lock pinned; single deduped monitoring-core copy)
  - `bash <kit>/harness validate` (in that repo's workspace) exits green: lint, typecheck, build, full test suite
  - Local dev-server smoke: app boots, monitoring client SDK initializes (`$monitorSDK` provided), a `/web/metrics` report request fires on page load/error (sendBeacon — "ping" type, not xhr/fetch); SSR server adapter initializes without errors
  - `git status` shows only `package.json` + `yarn.lock` changed (branch `FE-1045/stability-sdk-upgrade` off latest origin/main resp. origin/master)
- search-frontend part 1 already satisfies the same observable boundary (evidence filed: result.md + evidence/)
- Declared not covered (honest scope): staging deployments, platform-side data ingestion, production regression watch — for all three repos

## Change log

- 2026-08-31: spec drafted from Jira FE-1045 + clarification round (4 decisions: slow-check off accepted / no new tests / local observable acceptance boundary / caret declarations)
- 2026-08-31: harness-change — Jira FE-1045 scope extended to homepage-frontend + unified-search-frontend (title/scope updated in Jira). Deltas: +2 apps with identical pure-bump boundary; 4 locked decisions carried over verbatim (user: 沿用); task becomes multi-app single-task (user: option A); search-frontend PR #483 keep as-is (user). status confirmed → draft pending re-confirmation.
