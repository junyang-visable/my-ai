# result — valid conclusions & residual risks

> Distill only conclusions **verified as working**; keep it lean.
> Lengthy process detail goes into history.md.

## Verified conclusions

- Installed versions resolve exactly to target: `core:2.4.0 server:2.2.0 vue:2.0.3`, single deduped `monitoring-core` copy in node_modules (evidence/installed-versions.txt)
- `harness validate` all blocking gates green (lint / typecheck / arch / build / test / lock) — rerun 2026-08-31, raw output in evidence/validate.txt
- Diff discipline held end-to-end: only `package.json` + `yarn.lock` changed; commit `753882b2`, PR #483 (https://github.com/visable-dev/search-frontend/pull/483)
- Local dev smoke: page renders (HTTP 200, no SSR exception); SDK report pipeline verified — genuine `stability_monitor` payload captured on POST /web/metrics after setting reporter env to staging (monitoring-core ≥2.3.2 gates inner reports to staging/production; dev default 'development' suppresses them). The 4 POSTs first observed in the initial smoke turned out to be tracking-layer GA-event mirrors (`"type":"stability"`), not SDK reports — correction and both payload shapes in evidence/smoke.txt

### Parts 2–3 (homepage-frontend, unified-search-frontend) — verified 2026-08-31

- Both repos: installed versions resolve exactly to `core:2.4.0 server:2.2.0 vue:2.0.3`, single deduped `monitoring-core` copy; diff discipline held (only `package.json` + `yarn.lock`)
- homepage-frontend: validate all gates green (evidence/homepage-validate.txt); STAGE=staging smoke verified 2 genuine `stability_monitor` payloads (evidence/homepage-smoke.txt); commit `6b10fdf` on `FE-1045/stability-sdk-upgrade` (off origin/main)
- unified-search-frontend: validate all gates green (evidence/unified-search-validate.txt); STAGE=staging smoke verified 3 genuine `stability_monitor` payloads incl. injected `js_runtime_error` with stack (evidence/unified-search-smoke.txt); commit `1c65599e` on `FE-1045/stability-sdk-upgrade` (off origin/master a2fc4d24)
- Reporter flush latency observed on unified-search: beacons buffer on a ~60s interval — smoke procedures must re-poll, not short-wait (notes in each repo's notes.md)

## Residual risks / uncovered

- Parts 2–3 share part 1's residuals below (same SDK version, same local-observable boundary, same no-tests decision); delivered as PR #230 (homepage-frontend) and PR #1588 (unified-search-frontend), each with an English cr-frontend review comment (no Must Fix)

- Platform-side data flow (reports arriving in the monitoring backend post-deploy) — out of scope per spec; local-observable boundary only
- `api_slow` stops reporting under core 2.4.0 defaults (`enableSlowCheck: false`) — accepted per spec; not re-verified at runtime
- Other 2.4.0 ride-alongs (FE-1037 fix, built-in ignore lists) taken on CHANGELOG trust; smoke only proved the report pipeline fires
- No unit tests added for `7.monitoring.*` plugins — user decision (pure version upgrade)
- Pre-existing repo state: `.git/hooks/pre-commit` not executable → git ignores it; not addressed

## Acceptance evidence

- Rubric: `rubric.md` (acceptance side, role isolation — not authored here)
- Evidence dir: `evidence/` (installed-versions.txt, commit.txt, validate.txt, smoke.txt)
