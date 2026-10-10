# result — distilled outcome (three fixed sections)

> Only conclusions **verified as working**; keep it lean. Raw completion
> evidence goes to `evidence/completion.md` (per
> `.harness/rubric/evidence-template.md`); lengthy process detail goes to
> history.md. Requirement / one-line goal lives in the spec
> (`docs/changes/<task>/`) — never restate it here.

## Verified conclusions

- 5/5 repos upgraded on branch `CTOOL-718/header-upgrade`, one commit each, worktrees clean: PE c5e70654 · CD a813d13 · VF 7e57945 · BI fdbc385 (amended to exclude favicon build noise) · AC 02b9fef
- Exact pins verified in committed trees (`git show HEAD:package.json`): routing 22.10.0 + vue 43.44.0 in PE/VF/BI/AC; CD pins vue 43.44.0 only — routing resolves transitively at 22.10.0 inside the vue@43.44.0 block (pnpm-lock L4112)
- `bash <kit>/harness validate` all green 5/5 (serial); tests: PE 93 files/1024 · VF 31 files/460 passed +4 skipped · AC 24 files/252; installs proven per PM (`--frozen-lockfile` / `--immutable` / npm exit 0); zero `.snap` changes in any repo
- Breaking-change audit held in practice: no `categories` usage anywhere; `currentUrl` removal = harmless DOM-attribute fallthrough (matches SO #590 precedent)

## Residual risks / uncovered scope

- Staging header regression + GA3/GA4 live tracking verification → handed to QA (app-level checks, declared out of dev scope in the plan)
- CD/BI have no real unit suite — their coverage rests on lint/typecheck/build/lock stages only
- In-flight CTOOL-636 (beta bumps) + CTOOL-679 (banner) PRs pin beta versions on all 5 repos — merge-order conflicts expected; flagged in PR bodies at push time

## Pending confirmation (out-of-scope findings, NOT acted on)

- None — no out-of-ticket findings surfaced during the upgrade

---
Evidence pointers: rubric `rubric.md` · raw artifacts `evidence/completion.md`
