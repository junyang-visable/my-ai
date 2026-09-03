# plan — verifiable task breakdown

> Derived from spec.md: spec = what & boundaries (frozen once confirmed),
> plan = how (adjustable during execution; adjustments need no re-confirmation).
> Every step must carry a verification command and a concrete expected output —
> **output not matching expectation = not done**. Checkboxes are the progress;
> a fresh session can resume from them (a personal edition of superpowers
> writing-plans).

- Task name: FE-1045-stability-sdk-upgrade
- Based on spec: spec.md (status: confirmed, 2026-08-31; 3-repo version — re-confirmed after harness-change scope extension)

Repo: `/Users/yangjun/Desktop/project/search-frontend` · kit: `/Users/yangjun/Desktop/my-ai/harness-kit`

> **Scope change 2026-08-31 (harness-change)**: FE-1045 extended to homepage-frontend +
> unified-search-frontend. Tasks 1–4 below (search-frontend) are DONE and unaffected —
> check history stays as-is. Tasks 5+ for the two new repos are to be derived by
> harness-plan from the updated spec (pattern: same as Task 1–4 per repo, branch base
> origin/main resp. origin/master; plus workspace registration as a Step 0 per repo).

## Task 1: branch + dependency declarations + install

- [x] Step 0: precondition — user adds the repo folder to the Qoder workspace (write access) and stands by to supply `GITHUB_TOKEN` for Step 3
  - Verify: (evidenced by Step 2/3 succeeding — no probe writes)
  - Expect: user confirms both ready

- [x] Step 1: create branch off latest origin/main
  - Command:
    ```
    git -C /Users/yangjun/Desktop/project/search-frontend fetch origin
    git -C /Users/yangjun/Desktop/project/search-frontend symbolic-ref refs/remotes/origin/HEAD
    git -C /Users/yangjun/Desktop/project/search-frontend checkout --no-track -b FE-1045/stability-sdk-upgrade origin/main
    ```
  - Verify: `git -C /Users/yangjun/Desktop/project/search-frontend branch --show-current`
  - Expect: `FE-1045/stability-sdk-upgrade` (working tree clean before edits)

- [x] Step 2: bump the three dependency declarations in `package.json` (caret style)
  - `@visable-dev/monitoring-core`: `^2.2.0` → `^2.4.0`
  - `@visable-dev/monitoring-server`: `^2.1.0` → `^2.2.0`
  - `@visable-dev/monitoring-vue`: `^2.0.0` → `^2.0.3`
  - Verify: `grep -n "monitoring-" /Users/yangjun/Desktop/project/search-frontend/package.json`
  - Expect: exactly 3 matching lines containing `^2.4.0`, `^2.2.0`, `^2.0.3`

- [x] Step 3: install with user-provided GITHUB_TOKEN (token supplied by user at this moment; never written to any file/log)
  - Command: `cd /Users/yangjun/Desktop/project/search-frontend && GITHUB_TOKEN=<user-supplied> yarn install`
  - Verify A: `node -p "['core','server','vue'].map(p=>p+':'+require('/Users/yangjun/Desktop/project/search-frontend/node_modules/@visable-dev/monitoring-'+p+'/package.json').version).join(' ')"`
  - Expect A: `core:2.4.0 server:2.2.0 vue:2.0.3`
  - Verify B (dedupe — single core copy in tree): `find /Users/yangjun/Desktop/project/search-frontend/node_modules -path '*@visable-dev/monitoring-core/package.json' -not -path '*/.yarn/*' | wc -l`
  - Expect B: `1`
  - Verify C (diff discipline): `git -C /Users/yangjun/Desktop/project/search-frontend status --porcelain`
  - Expect C: only ` M package.json` and ` M yarn.lock`
  - Failure mode: resolution error for any target version → not published → **stop, escalate to user to re-confirm target** (spec risk item)

## Task 2: full validation gate

- [x] Step 1: run the single validation entry
  - Command: `bash /Users/yangjun/Desktop/my-ai/harness-kit/harness validate`
  - Expect: exit 0; every stage line reports OK (lint / typecheck / build / test)

- [x] Step 2: diff discipline after lint --fix side effects
  - Verify: `git -C /Users/yangjun/Desktop/project/search-frontend status --porcelain`
  - Expect: still only ` M package.json` and ` M yarn.lock` (any other auto-fixed file = pre-existing style debt — investigate and report, don't silently commit)

## Task 3: local dev smoke (SDK init + report request)

- [x] Step 1: boot dev server (port/command proven by playwright.config.ts webServer)
  - Command: `cd /Users/yangjun/Desktop/project/search-frontend && yarn dev --port 3101` (background, wait for ready)
  - Verify: `curl -s -o /dev/null -w '%{http_code}' 'http://localhost:3101/en/search?q=industrial+pumps'`
  - Expect: `200` (page renders; dev-server log shows no uncaught SSR exception)

- [x] Step 2: browser smoke — SDK initialized and report fires
  - Action: via browser automation open `http://localhost:3101/en/search?q=industrial+pumps`, then evaluate an uncaught error (`setTimeout(() => { throw new Error('FE-1045 smoke') }, 0)`) to trigger ScriptErrorMonitor
  - Verify: list network requests of the page session
  - Expect: ≥ 1 `POST` request whose URL contains `/web/metrics` (client reporting pipeline alive)

- [x] Step 3: stop the dev server (no orphan process)
  - Verify: `lsof -ti:3101`
  - Expect: no output (command exits 1 — port free)

## Task 4: commit + handoff

- [x] Step 1: commit the two files
  - Command: `git -C /Users/yangjun/Desktop/project/search-frontend add package.json yarn.lock && git -C /Users/yangjun/Desktop/project/search-frontend commit -m "chore(deps): upgrade stability SDK to core 2.4.0 / server 2.2.0 / vue 2.0.3 (FE-1045)"`
  - Verify: `git -C /Users/yangjun/Desktop/project/search-frontend show --stat --oneline HEAD | head -5`
  - Expect: message contains `FE-1045`; stat shows exactly `package.json` + `yarn.lock`

- [x] Step 2: push — only after the user has validated the change themselves (standing rule)
  - Command: `git -C /Users/yangjun/Desktop/project/search-frontend push -u origin FE-1045/stability-sdk-upgrade`
  - Verify: `git -C /Users/yangjun/Desktop/project/search-frontend status -sb`
  - Expect: tracking branch `origin/FE-1045/stability-sdk-upgrade`, no unpushed marker

- [x] Step 3: wrap-up — update `current.md` (stage → accept) and `history.md` (one line per Task), file evidence per `<kit>/.harness/rubric/evidence-template.md`, write repo lessons into `<kb>/search-frontend/notes.md`, remind user: acceptance happens in a separate harness-testing session

## Task 5: homepage-frontend — register workspace + branch + bump + install

> Cross-app order: Tasks 5–6 (homepage-frontend) before Tasks 7–8 (unified-search-frontend); no dependency between the two repos — sequential only to keep one coding loop.

- [x] Step 0: precondition — homepage-frontend folder is in the Qoder workspace (write access); user's ≤60-day GITHUB_TOKEN in `~/.zshrc` (proven working in Task 1)
  - Verify: (evidenced by Step 4 succeeding — no probe writes)
  - Expect: later steps succeed

- [x] Step 1: register workspace + fill config
  - Command:
    ```
    bash /Users/yangjun/Desktop/my-ai/harness-kit/harness add homepage-frontend /Users/yangjun/Desktop/project/homepage-frontend
    # then fill knowledge-base/homepage-frontend/config.sh:
    # HARNESS_LINT_CMD="yarn lint" / HARNESS_TYPECHECK_CMD="yarn typecheck" /
    # HARNESS_BUILD_CMD="yarn build" / HARNESS_TEST_CMD="yarn test"; E2E/SMOKE empty
    bash /Users/yangjun/Desktop/my-ai/harness-kit/harness use homepage-frontend
    ```
  - Verify: `bash /Users/yangjun/Desktop/my-ai/harness-kit/harness current && grep -c "HARNESS_.*_CMD=\"yarn" /Users/yangjun/Desktop/my-ai/knowledge-base/homepage-frontend/config.sh`
  - Expect: current prints homepage-frontend repo path; grep count `4`

- [x] Step 2: create branch off latest origin/main
  - Command:
    ```
    git -C /Users/yangjun/Desktop/project/homepage-frontend fetch origin
    git -C /Users/yangjun/Desktop/project/homepage-frontend checkout --no-track -b FE-1045/stability-sdk-upgrade origin/main
    ```
  - Verify: `git -C /Users/yangjun/Desktop/project/homepage-frontend branch --show-current && git -C /Users/yangjun/Desktop/project/homepage-frontend status --porcelain`
  - Expect: `FE-1045/stability-sdk-upgrade`; empty status (clean tree before edits)

- [x] Step 3: bump the three dependency declarations in `package.json` (caret style)
  - `@visable-dev/monitoring-core`: `^2.2.0` → `^2.4.0`
  - `@visable-dev/monitoring-server`: `^2.1.0` → `^2.2.0`
  - `@visable-dev/monitoring-vue`: `^2.0.0` → `^2.0.3`
  - Verify: `grep -n "monitoring-" /Users/yangjun/Desktop/project/homepage-frontend/package.json`
  - Expect: exactly 3 matching lines containing `^2.4.0`, `^2.2.0`, `^2.0.3`

- [x] Step 4: install (token from user rc — never written to any file/log)
  - Command: `cd /Users/yangjun/Desktop/project/homepage-frontend && zsh -ic 'yarn install'`
  - Verify A: `node -p "['core','server','vue'].map(p=>p+':'+require('/Users/yangjun/Desktop/project/homepage-frontend/node_modules/@visable-dev/monitoring-'+p+'/package.json').version).join(' ')"`
  - Expect A: `core:2.4.0 server:2.2.0 vue:2.0.3`
  - Verify B (dedupe): `find /Users/yangjun/Desktop/project/homepage-frontend/node_modules -path '*@visable-dev/monitoring-core/package.json' -not -path '*/.yarn/*' | wc -l`
  - Expect B: `1`
  - Verify C (diff discipline): `git -C /Users/yangjun/Desktop/project/homepage-frontend status --porcelain`
  - Expect C: only ` M package.json` and ` M yarn.lock`
  - Failure mode: resolution error → stop, escalate to user (spec risk item)

## Task 6: homepage-frontend — validate + smoke + commit + PR

- [x] Step 1: run the unified validation entry (active repo = homepage-frontend)
  - Command: `zsh -ic 'bash /Users/yangjun/Desktop/my-ai/harness-kit/harness validate'`
  - Expect: exit 0; summary line `all blocking gates passed` (lint / typecheck / arch / build / test / lock)

- [x] Step 2: diff discipline after lint --fix side effects
  - Verify: `git -C /Users/yangjun/Desktop/project/homepage-frontend status --porcelain`
  - Expect: still only ` M package.json` and ` M yarn.lock`

- [x] Step 3: local dev smoke (SDK init + report request)
  - Command: `cd /Users/yangjun/Desktop/project/homepage-frontend && zsh -ic 'yarn dev --port 3102'` (background, wait for ready)
  - Verify: `curl -s -o /dev/null -w '%{http_code}' 'http://localhost:3102/'`
  - Expect: `200` (HomePage at `/`; no uncaught SSR exception in dev log)
  - Then: browser-open the page, inject `setTimeout(() => { throw new Error('FE-1045 smoke') }, 0)`, list network requests
  - Expect: ≥ 1 `POST` to a URL containing `/web/metrics` (sendBeacon — appears as "ping" type, NOT xhr/fetch; local 404 response is expected)
  - Then: stop the dev server; `lsof -ti:3102` → no output (exit 1)
  - **Adjustment (executed)**: dev smoke ran with `STAGE=staging zsh -ic 'yarn dev --port 3102'` and expectation
    tightened to a genuine SDK payload. Reason: monitoring-core ≥2.3.2 only sends inner reports when env ∈
    {staging, production}; dev default 'development' correctly sends none (first observed when 0 POSTs fired
    with the SDK verifiably initialized). Also must assert payload `"type":"stability_monitor"` — the tracking
    layer separately posts `"type":"stability"` GA-event mirrors to /web/metrics that fire in any env (this
    invalidated part 1's initial smoke reading; evidence/smoke.txt carries the correction).
    Result: 2 POST /web/metrics [404] with verified `stability_monitor` bodies (1 organic resource_load_failed,
    1 from injected error) + SDK init dump; ports 3101/3102 both freed after. Evidence: evidence/homepage-smoke.txt

- [x] Step 4: commit the two files
  - Command: `git -C /Users/yangjun/Desktop/project/homepage-frontend add package.json yarn.lock && git -C /Users/yangjun/Desktop/project/homepage-frontend commit -m "chore(deps): upgrade stability SDK to core 2.4.0 / server 2.2.0 / vue 2.0.3 (FE-1045)"`
  - Verify: `git -C /Users/yangjun/Desktop/project/homepage-frontend show --stat --oneline HEAD | head -5`
  - Expect: message contains `FE-1045`; stat shows exactly `package.json` + `yarn.lock`

- [x] Step 5: push (only after user validates the change themselves — standing rule) + create PR
  - Command: `git -C /Users/yangjun/Desktop/project/homepage-frontend push -u origin FE-1045/stability-sdk-upgrade` then `gh pr create` (English, per repo's PR template, references FE-1045)
  - Verify: PR creation output URL; `git -C /Users/yangjun/Desktop/project/homepage-frontend status -sb`
  - Expect: tracking branch set, no unpushed marker
  - Done 2026-08-31 (user explicitly requested PR submission): PR #230 https://github.com/visable-dev/homepage-frontend/pull/230 (template filled, Non-functional); cr-frontend review comment posted in English (no Must Fix): issuecomment-5477655202

## Task 7: unified-search-frontend — register workspace + branch + bump + install

- [x] Step 0: precondition — unified-search-frontend folder is in the Qoder workspace (write access); GITHUB_TOKEN as in Task 5
  - Verify: (evidenced by Step 4 succeeding)
  - Expect: later steps succeed

- [x] Step 1: register workspace + fill config (same commands as homepage-frontend)
  - Command:
    ```
    bash /Users/yangjun/Desktop/my-ai/harness-kit/harness add unified-search-frontend /Users/yangjun/Desktop/project/unified-search-frontend
    # fill knowledge-base/unified-search-frontend/config.sh identically (yarn lint/typecheck/build/test; E2E/SMOKE empty)
    bash /Users/yangjun/Desktop/my-ai/harness-kit/harness use unified-search-frontend
    ```
  - Verify: `bash /Users/yangjun/Desktop/my-ai/harness-kit/harness current && grep -c "HARNESS_.*_CMD=\"yarn" /Users/yangjun/Desktop/my-ai/knowledge-base/unified-search-frontend/config.sh`
  - Expect: current prints unified-search-frontend repo path; grep count `4`
  - Re-verified 2026-08-31: current prints unified-search-frontend + repo path; grep count `4`

- [x] Step 2: create branch off latest origin/master (local checkout is on `access-monitoring`, clean — switching leaves that branch untouched)
  - Command:
    ```
    git -C /Users/yangjun/Desktop/project/unified-search-frontend fetch origin
    git -C /Users/yangjun/Desktop/project/unified-search-frontend checkout --no-track -b FE-1045/stability-sdk-upgrade origin/master
    ```
  - Verify: `git -C /Users/yangjun/Desktop/project/unified-search-frontend branch --show-current && git -C /Users/yangjun/Desktop/project/unified-search-frontend status --porcelain`
  - Expect: `FE-1045/stability-sdk-upgrade`; empty status
  - Done 2026-08-31: branch off origin/master a2fc4d24; tree clean (log of Task 8 commit confirms parent a2fc4d24)

- [x] Step 3: bump the three dependency declarations in `package.json` (caret style, same targets)
  - Verify: `grep -n "monitoring-" /Users/yangjun/Desktop/project/unified-search-frontend/package.json`
  - Expect: exactly 3 matching lines containing `^2.4.0`, `^2.2.0`, `^2.0.3`
  - Re-verified 2026-08-31: lines 34–36 match exactly

- [x] Step 4: install
  - Command: `cd /Users/yangjun/Desktop/project/unified-search-frontend && zsh -ic 'yarn install'`
  - Verify A/B/C: same as Task 5 Step 4 (paths → unified-search-frontend)
  - Expect A: `core:2.4.0 server:2.2.0 vue:2.0.3`; B: `1`; C: only ` M package.json` + ` M yarn.lock`
  - Re-verified 2026-08-31: A `core:2.4.0 server:2.2.0 vue:2.0.3`; B `1`; C held until commit

## Task 8: unified-search-frontend — validate + smoke + commit + PR

- [x] Step 1: run the unified validation entry (active repo = unified-search-frontend)
  - Command: `zsh -ic 'bash /Users/yangjun/Desktop/my-ai/harness-kit/harness use unified-search-frontend && bash /Users/yangjun/Desktop/my-ai/harness-kit/harness validate'`
  - Expect: exit 0; summary line `all blocking gates passed`
  - Done 2026-08-31: exit 0, `all blocking gates passed` (lint/typecheck/arch/build/test/lock). Evidence: evidence/unified-search-validate.txt

- [x] Step 2: diff discipline
  - Verify: `git -C /Users/yangjun/Desktop/project/unified-search-frontend status --porcelain`
  - Expect: still only ` M package.json` and ` M yarn.lock`
  - Done 2026-08-31: exactly ` M package.json` + ` M yarn.lock` (6/34 changed lines)

- [x] Step 3: local dev smoke
  - Command: `cd /Users/yangjun/Desktop/project/unified-search-frontend && zsh -ic 'yarn dev --port 3103'` (background)
  - Verify: `curl -s -o /dev/null -w '%{http_code}' 'http://localhost:3103/'`
  - Expect: `200` (home_root at `/`); browser smoke + `/web/metrics` evidence as Task 6 Step 3; then stop server, `lsof -ti:3103` → no output
  - **Adjustment (executed)**: ran with `STAGE=staging zsh -ic 'yarn dev --port 3103'` for the same env-gate
    reason as Task 6 Step 3. curl `/` → 200; SDK config dump `env: "staging"`, `appName:
    "unified-search-frontend"`, `reporter.enableInnerReport: true`; 3 genuine POST /web/metrics [404] with
    `"type":"stability_monitor"` bodies (2 organic resource_load_failed — hotjar ORB, cookiebot 404 — plus 1
    injected js_runtime_error with full stack). New observation: the reporter flushes on a ~60s interval — the
    injected error's beacon landed ~56s after injection, so a 4s wait shows nothing; smoke must re-poll the
    network list (sendBeacon also never appears in performance.getEntriesByType('resource')). Server stopped;
    `lsof -ti:3103` empty. Evidence: evidence/unified-search-smoke.txt

- [x] Step 4: commit the two files
  - Command: `git -C /Users/yangjun/Desktop/project/unified-search-frontend add package.json yarn.lock && git -C /Users/yangjun/Desktop/project/unified-search-frontend commit -m "chore(deps): upgrade stability SDK to core 2.4.0 / server 2.2.0 / vue 2.0.3 (FE-1045)"`
  - Verify: `git -C /Users/yangjun/Desktop/project/unified-search-frontend show --stat --oneline HEAD | head -5`
  - Expect: message contains `FE-1045`; stat shows exactly `package.json` + `yarn.lock`
  - Done 2026-08-31: commit `1c65599e` on `FE-1045/stability-sdk-upgrade` (parent a2fc4d24), 2 files, 20+/20-; tree clean after

- [x] Step 5: push (only after user validates — standing rule) + create PR (English, repo template, references FE-1045)
  - Verify: PR URL; `git -C /Users/yangjun/Desktop/project/unified-search-frontend status -sb`
  - Expect: tracking branch set, no unpushed marker
  - Done 2026-08-31 (user explicitly requested PR submission; repo has no PR template → same body structure without checklist): PR #1588 https://github.com/visable-dev/unified-search-frontend/pull/1588; cr-frontend review comment posted in English (no Must Fix): issuecomment-5477663157

- [x] Step 6: wrap-up — update `current.md` (stage → accept), `history.md` append, evidence into this task's evidence/ dir with per-repo prefixes, lessons into each new repo's notes.md, remind user: acceptance of all three PRs in a separate harness-testing session
  - Done 2026-08-31 (push/PR reminder included in the coding-loop handoff message; acceptance-session reminder repeated there)

## Definition of done

- [x] part 1 (search-frontend, Tasks 1–4): all Tasks/Steps checked, every verification matched its expectation
- [x] part 1: `bash <kit>/harness validate` all green (evidence/validate.txt)
- [x] part 1: diff limited to `package.json` + `yarn.lock`; branch pushed after user validation (PR #483)
- [x] parts 2–3 (Tasks 5–8): all Tasks/Steps checked, every verification matched its expectation
- [x] parts 2–3: `harness validate` green in homepage-frontend and unified-search-frontend workspaces (evidence/homepage-validate.txt, evidence/unified-search-validate.txt)
- [x] parts 2–3: per-repo diff limited to `package.json` + `yarn.lock` (held: commits 6b10fdf / 1c65599e); both branches pushed after user validation; both PRs reference FE-1045 — PR #230 (homepage-frontend) + PR #1588 (unified-search-frontend), each with an English cr-frontend review comment posted
