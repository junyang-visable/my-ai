# result — distilled outcome (three fixed sections)

> Only conclusions **verified as working**; keep it lean. Raw completion
> evidence goes to `evidence/completion.md` (per
> `.harness/rubric/evidence-template.md`); lengthy process detail goes to
> history.md. Requirement / one-line goal lives in the spec
> (`docs/changes/<task>/`) — never restate it here.

## Verified conclusions

- `getRequestPlatform` derivation helper shipped with a 7-case TDD branch matrix (RED `7 failed | 3 passed`, exit 1 → GREEN `10 passed`, exit 0) — commit `e2b674a`
- `request_platform` wired into BOTH live `show_messages_messageDetail` firing points (MessageCenterUpgrade + legacy ConversationDetails), conditional-spread so the key is omitted when no signal; GA4 pipeline and the shared `deriveConversationCustomDimentions` helper untouched (no-leak grep: exactly 3 intended files) — commit `63e0e70`
- **Value-domain fix (user correction, change-executed)**: output is the lowercase `REQUEST_ORIGINS` vocabulary `'alibaba' | 'wlw' | 'ep'` (NOT raw uppercase codes); bugfix-style RED `expected 'WLW' to be 'wlw'` → GREEN 10/10 — commit `2648da3`; spec re-confirmed after harness-change round
- **UTM stripping (second scope, harness-change round)**: `omitUtmParams` helper (TDD 4/4) wired into BOTH `setNewRoute` entry points (page-level `index.vue` + list-level `ConversationList.vue` filter navigation) — in-page rewrites no longer carry `utm_medium`/`utm_source`/`utm_campaign`; landing URL and history untouched — commit `0e18acf`; spec re-confirmed after change round
- Full gate run green (post-fix, both scopes): lint OK, typecheck OK (exit 0; 19 printed diagnostics pre-exist on main, error set identical with/without branch changes), arch OK, build OK, test OK, lock OK
- Environment repair (pre-existing rot): lockfile-vs-node_modules drift fixed via full `yarn install --frozen-lockfile` + removal of an orphaned nested `routing@22.7.2` copy not backed by yarn.lock

## Residual risks / uncovered scope

- No live browser payload check yet (no E2E suite in repo; auth needs docker stack + real login) — QA live-check recipe: read `window.dataLayer` (GA3 path; `__mcTrackingEvents` probe does NOT capture this event), disable sends via `window.googleAnalytics3TrackingDisabled = true`
- 'alibaba' is a deliberate superset of the ticket's literal `originAli` wording (user decision, spec Q&A) — Jira AC note pending

## Pending confirmation (out-of-scope findings, NOT acted on)

- Branch push + PR: awaiting explicit user instruction
- Jira CTOOL-719 AC note in English (alibaba = originAli OR metadata ALI superset): user-owned follow-up
- 19 pre-existing typecheck diagnostics on origin/main (11 files) + the stale-node_modules failure mode seen twice this session: repo health items for the team, not this ticket
