# history — append-only log

> Append one line per action; never rewrite old lines.
> Format: time | action | result/evidence.

- 2026-09-03 19:06 | task created (harness task new FE-1064-remove-dead-code) | process dir + docs/changes/ skeleton
- 2026-09-03 19:10 | repo onboarding | harness add + config.sh (pnpm stack) + doctor/selfcheck green
- 2026-09-03 19:20 | spec drafted & confirmed | docs/changes/FE-1064-remove-dead-code/spec.md status: confirmed; scope strictly ticket-only, automation gates only, 3 commits
- 2026-09-03 19:25 | plan written | 4 Tasks, every step with verify command
- 2026-09-03 19:30 | branch FE-1064/remove-dead-code from origin/main @ eea827f | discovered FE-1063 (CI gates) pushed but unmerged → lint:ci script absent on main, switched gate to direct eslint invocation (equivalent, no --fix)
- 2026-09-03 19:35 | commit 4f2605d: deleted route.js/IconWlw/IconEp/tracking.ts | −1,516 lines; lint+typecheck green
- 2026-09-03 19:40 | commit e01f252: removed 4 deps + stub + datadog comment block | lockfile −138 (routing stays as transitive dep of @visable-dev/vue); pnpm install needed CI=true --no-frozen-lockfile (interactive purge prompt); lint+typecheck green
- 2026-09-03 19:45 | commit aa19214: pruned dead exports across 6 files | −298 lines; new eslint warning: API_URL_V2 now unused (getUserInfo was its only consumer) → kept, pending list
- 2026-09-03 19:50 | harness validate --strict | ALL GREEN (lint/typecheck/arch/build/lock)
- 2026-09-03 19:52 | commit 064164e: docs (spec+plan) | branch complete: 4 commits, tree clean
- 2026-09-03 19:55 | wrap-up | result.md evidence filed; pending list: API_URL_V2 const, main.ts:14 comment, App.vue unused imports
