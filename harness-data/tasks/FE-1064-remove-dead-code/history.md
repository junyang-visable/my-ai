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
- 2026-09-04 15:40 | knip 6.34 re-scan of post-cleanup branch | found 5 dead items (12 cookie constants, UserV2, API_URL_V2, App.vue imports, main.ts comment) — all grep-verified zero refs
- 2026-09-04 15:50 | harness-change: scope addition | user folded all 5 into FE-1064; Jira description updated (+ re-scan section); spec demoted→draft, plan Task 5 appended; user re-confirmed
- 2026-09-04 15:55 | commit 9ed1ad0: removed the 5 items | +1/-22; eslint 6→2 warnings (API_URL_V2 + App.vue warnings gone); validate --strict ALL GREEN again
- 2026-09-04 15:57 | commit 894df67: docs (change log + Task 5) | branch: 4 code commits + 2 docs commits; ready to push & update PR #37
