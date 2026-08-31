# plan — verifiable task breakdown

> Derived from spec.md: spec = what & boundaries (frozen once confirmed),
> plan = how (adjustable during execution; adjustments need no re-confirmation).
> Every step must carry a verification command and a concrete expected output —
> **output not matching expectation = not done**. Checkboxes are the progress;
> a fresh session can resume from them (a personal edition of superpowers
> writing-plans).

- Task name: FE-1045-stability-sdk-upgrade
- Based on spec: spec.md (status: confirmed, 2026-08-31)

Repo: `/Users/yangjun/Desktop/project/search-frontend` · kit: `/Users/yangjun/Desktop/my-ai/harness-kit`

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

## Definition of done

- [x] all Tasks/Steps checked, every verification matched its expectation
- [x] `bash <kit>/harness validate` all green (add --strict for cross-file changes)
- [x] diff limited to `package.json` + `yarn.lock`; branch `FE-1045/stability-sdk-upgrade` pushed after user validation
