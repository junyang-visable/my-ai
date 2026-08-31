# history — append-only log

> Append one line per action; never rewrite old lines.
> Format: time | action | result/evidence.

- 2026-08-31 | Task1: branch FE-1045/stability-sdk-upgrade off origin/main | clean tree, branch confirmed
- 2026-08-31 | Task1: bump 3 declarations in package.json | grep shows ^2.4.0/^2.2.0/^2.0.3 exactly
- 2026-08-31 | Task1: yarn install | resolved+linked 2.4.0/2.2.0/2.0.3; needed user's fresh GITHUB_TOKEN (old classic PAT >60d blocked by Visable enterprise policy, 403 on all npm.pkg.github.com endpoints)
- 2026-08-31 | Task1: verify A/B/C | core:2.4.0 server:2.2.0 vue:2.0.3; 1 monitoring-core copy; git status only package.json+yarn.lock
- 2026-08-31 | Task2 attempt 1: harness validate | 4 BLOCKING failures — all environmental (yarn needs GITHUB_TOKEN in env for ANY command via .yarnrc.yml expansion), not code; retrying via zsh -ic with user rc token
- 2026-08-31 | Task2: harness validate via zsh -ic | all stages OK (lint/typecheck/build/test), exit 0
- 2026-08-31 | Task2: diff discipline post-validate | git status still only package.json+yarn.lock
- 2026-08-31 | Task3: yarn dev --port 3101 + curl | HTTP 200 on /en/search?q=industrial+pumps, no SSR exception in log
- 2026-08-31 | Task3: browser smoke (Chrome DevTools MCP) | page rendered (title wlw.localhost); injected FE-1045 smoke error; 4 POST /web/metrics observed — SDK uses navigator.sendBeacon (shows as "ping", not xhr/fetch; re-listed full network log to find them)
- 2026-08-31 | Task3: /web/metrics 404 triage | expected — app dev server has no /web/metrics route (no refs in src/server/ or nuxt.config.ts; production infra handles it); request firing is the acceptance evidence
- 2026-08-31 | Task3: stop dev server, lsof -ti:3101 | no output, exit 1 — port free
- 2026-08-31 | Task4: commit package.json+yarn.lock | 753882b2, 2 files changed 20+/20-, message contains FE-1045 (note: repo pre-commit hook exists but not executable, git ignored it — pre-existing state)
- 2026-08-31 | Task4: push branch (user validated + requested PR) | tracking set, no unpushed marker; gh needed zsh -ic GH_TOKEN (agent shell unauthenticated)
- 2026-08-31 | Task4: create PR via gh (template filled, English per user rule) | https://github.com/visable-dev/search-frontend/pull/483
- 2026-08-31 | Task4: wrap-up | current.md → accept; evidence/ (validate.txt re-run + versions + commit + smoke); notes.md lessons (sendBeacon ping-type, local 404); plan.md all ticks incl. DoD
