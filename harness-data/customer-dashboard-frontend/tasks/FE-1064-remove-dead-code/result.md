# result — valid conclusions & residual risks

> Distill only conclusions **verified as working**; keep it lean.
> Lengthy process detail goes into history.md.

## Requirement

- Task: FE-1064-remove-dead-code (Jira: FE-1064) — remove ~1,700 lines of verified dead code + 4 unused deps, zero behavior change
- Branch: `FE-1064/remove-dead-code` from `origin/main` @ eea827f; commits 4f2605d → e01f252 → aa19214 → 064164e (docs)
- Diff vs main: 14 files, +6/−1,975, all matching the ticket checklist

## Verified conclusions

- `bash harness-kit/harness validate --strict` → lint/typecheck/arch/build/lock ALL OK (production vite build included)
- eslint: 0 errors / 6 warnings (5 pre-existing on main + 1 newly-exposed `API_URL_V2` unused, kept per scope boundary)
- Every ticket claim re-verified against the tree before deletion (zero live references); diff contains only checklist items + direct entailments (dead imports, lockfile −138 lines)

## Uncovered scope

- No dev-server/manual smoke (user decision: gates only; user verifies routes + locales before push)
- No unit/E2E tests exist in this repo — not applicable

## Residual risks / uncovered

- `@visable-dev/routing` remains as a transitive dep of `@visable-dev/vue` — expected; only the unused direct dep was removed
- FE-1063 (CI gates) unmerged: this branch gates via equivalent direct eslint/vue-tsc commands; `pnpm lint:ci` becomes canonical after FE-1063 merges (no conflict expected — different package.json sections)

## Pending-confirmation list (out of ticket scope, NOT acted on)

1. `src/utils/request.ts:8` — `API_URL_V2` const now fully unused (only consumer `getUserInfo` was deleted); ticket said "drop export" only. Suggest deleting in a follow-up.
2. `src/main.ts:14` — `// const env = getEnv()` commented line (ex-datadog wiring); safe to delete alongside.
3. `src/App.vue:10` — pre-existing unused imports `getLocale` / `getCountryCode` / `updateIsInternalUser` (already warn on main).
