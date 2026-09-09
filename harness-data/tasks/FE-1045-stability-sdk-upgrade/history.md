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
- 2026-08-31 | harness-change: Jira FE-1045 scope extended to 3 repos (title/scope updated in Jira 09:27) | surveyed both new repos: same current versions (^2.2.0/^2.1.0/^2.0.0), same token registry, adapters identical to search-frontend's; defaults main resp. master
- 2026-08-31 | harness-change grill (4 decisions) | 沿用 four locked decisions ×2 repos; branch base = latest origin/master (unified-search, standing rule); single multi-app task option A; PR #483 keep as-is
- 2026-08-31 | harness-change: spec.md synced to 3-app version, status confirmed→draft | plan.md annotated (Tasks 1-4 done & unaffected, Tasks 5+ to be derived by harness-plan); current.md stage accept→clarify
- 2026-08-31 | harness-change: user re-confirmed 3-app spec (确认) | status draft→confirmed; routing to harness-plan for Tasks 5+
- 2026-08-31 | harness-plan: Tasks 5-8 derived (per-repo: register/branch/bump/install + validate/smoke/commit/PR; homepage off main, unified-search off master; smoke ports 3102/3103; DoD split part1 vs parts2-3) | plan.md updated, ≤8 tasks
- 2026-08-31 | Task5: harness add homepage-frontend + config/notes filled | active workspace confirmed, 4 yarn commands in config.sh
- 2026-08-31 | Task5: branch FE-1045/stability-sdk-upgrade off fresh origin/main (914ecfa→067341c fetched) | clean tree
- 2026-08-31 | Task5: bump 3 declarations + zsh -ic yarn install | grep ^2.4.0/^2.2.0/^2.0.3 exactly; core:2.4.0 server:2.2.0 vue:2.0.3; 1 core copy; git status only package.json+yarn.lock
- 2026-08-31 | Task6 Step1-2: harness validate (homepage-frontend active) | all blocking gates passed; diff discipline held (only package.json+yarn.lock)
- 2026-08-31 | Task6 Step3 attempt 1: smoke with default dev (stage=development) | SDK initialized ($monitorSDK env=development, appName=homepage-frontend) but 0 POST /web/metrics — investigation opened
- 2026-08-31 | Task6 Step3 diagnosis: monitoring-core ≥2.3.2 Reporter env gate (dist `r !== "staging" && r !== "production"` → return); gate added in release-2.3.2 (frontend-monitoring 6644b09) | dev stage='development' suppresses inner reports by design
- 2026-08-31 | Task6 Step3 diagnosis (cross-check vs part 1): re-ran search-frontend dev + payload inspection | part-1's 4 POSTs were tracking-layer `"type":"stability"` GA-event mirrors (no env gate), NOT SDK reports — evidence/smoke.txt + result.md corrected; genuine SDK report on search-frontend captured via sdk.reporter.env='staging' console patch (stability_monitor payload, reqid 2260)
- 2026-08-31 | Task6 Step3 attempt 2: STAGE=staging dev smoke | 2 POST /web/metrics [404] with verified stability_monitor bodies (1 organic resource_load_failed hotjar-ORB + 1 injected); runtime stage/skEnv=staging confirmed; ports 3101/3102 freed; evidence/homepage-smoke.txt filed
- 2026-08-31 | Task6 Step4: commit homepage bump | 6b10fdf, exactly package.json+yarn.lock (20+/20-)
- 2026-08-31 | Task7: harness add unified-search-frontend + config/notes filled | active workspace confirmed, 4 yarn commands in config.sh
- 2026-08-31 | Task7: branch FE-1045/stability-sdk-upgrade off fresh origin/master (30bef616..a2fc4d24 fetched) | clean tree (access-monitoring left untouched)
- 2026-08-31 | Task7: bump 3 declarations + zsh -ic yarn install | grep ^2.4.0/^2.2.0/^2.0.3 exactly; core:2.4.0 server:2.2.0 vue:2.0.3; 1 core copy; git status only package.json+yarn.lock
- 2026-08-31 | Task8 Step1-2: harness validate (unified-search-frontend active) via zsh -ic | all blocking gates passed (lint/typecheck/arch/build/test/lock); diff discipline held (package.json+yarn.lock only); evidence/unified-search-validate.txt
- 2026-08-31 | Task8 Step3: STAGE=staging dev smoke port 3103 | curl / → 200; SDK config dump env=staging appName=unified-search-frontend reporter.enableInnerReport=true; 3 POST /web/metrics [404] all "type":"stability_monitor" (2 organic resource_load_failed + 1 injected js_runtime_error w/ stack); server stopped, lsof 3103 empty; evidence/unified-search-smoke.txt
- 2026-08-31 | Task8 Step3 observation: reporter flush latency | injected error's beacon landed ~56s after injection (reporter buffers on ~60s interval); sendBeacon absent from performance.getEntriesByType — must re-poll DevTools network list, 4s wait insufficient
- 2026-08-31 | Task8 Step4: commit unified-search bump | 1c65599e on FE-1045/stability-sdk-upgrade (parent a2fc4d24), exactly package.json+yarn.lock (20+/20-), tree clean
- 2026-08-31 | Task8 wrap-up (push/PR pending user validation) | plan.md Task7/8 ticks + DoD; current.md → accept; unified-search notes.md flush-latency lesson; both repos' push+PR paused per standing rule
- 2026-08-31 | Task6 Step5 + Task8 Step5: user requested PR submission → push both branches + gh pr create | homepage PR #230 (template filled, Non-functional); unified-search PR #1588 (no template → same body structure); both English, reference FE-1045
- 2026-08-31 | cr-frontend review on both PRs (user request; comments in English per standing rule) | both: Change Type = third-party SDK upgrade elevated to Major, Risk 🔴 High; regression checklist 1.1-7; no Must Fix; Suggestion [tracking-impact] ×2 (api_slow default-off in core 2.4.0 + contract guard skipped for pure dep bump); Good Practice (diff discipline + genuine stability_monitor smoke evidence); posted: issuecomment-5477655202 (PR #230), issuecomment-5477663157 (PR #1588)
- 2026-08-31 | current.md → done (all three PRs delivered with CR comments) | DoD all boxes ticked; remaining: human merge, harness-testing acceptance session, my-ai KB commit
