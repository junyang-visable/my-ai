#!/usr/bin/env python3
"""Post PR-link comments to CTOOL-679 child tasks + epic summary comment."""
import json, importlib.util

spec = importlib.util.spec_from_file_location("amc", "/Users/yangjun/Desktop/my-ai/.scratch/atlassian-mcp-call.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# initialize session
init = m.rpc("initialize", {
    "protocolVersion": "2025-03-26",
    "capabilities": {},
    "clientInfo": {"name": "qoder-direct", "version": "1.0"},
})
assert "error" not in (init or {}), init
m.rpc("notifications/initialized", {}, notify=True)

CLOUD = "visable.atlassian.net"
GH = "https://github.com/visable-dev"


def comment(key, body):
    res = m.rpc("tools/call", {
        "name": "addCommentToJiraIssue",
        "arguments": {
            "cloudId": CLOUD,
            "issueIdOrKey": key,
            "commentBody": body,
            "contentFormat": "markdown",
        },
    })
    ok = res and "result" in res
    print(key, "OK" if ok else "FAIL", "" if ok else json.dumps(res)[:400])
    return ok


c684 = """Pull request delivering the shared component:

- [{repo}/visable-vue/pull/738 visable-vue #738] — *CTOOL-679: self-contained Alibaba onboarding banner (GA4+GA3 tracking)*
  - Single public component `VisAlibabaOnboardingBanner` (activation modal as internal subcomponent), self-contained data layer (injectable fetcher / gateway base) and self-contained funnel tracking (`ga4Tracker` / `ga3Tracker` props), status-driven visibility incl. the BV-pending (`under_review`) variant, wlw blue theme variant, 21 locales.
  - Published to GitHub Packages as `@visable-dev/vue@43.44.0-beta.6` (tag `v43.44.0-beta.6`); beta.3–beta.5 tags had failed CI on stylelint (`color-hex-length`), fixed by `cf597b3c`.
""".format(repo=GH)

c685 = """Pull requests delivering the banner integration, one per supplier app (branches `CTOOL-679/*`, component pinned to `@visable-dev/vue@43.44.0-beta.6`):

- [{repo}/product-editor-frontend/pull/104 product-editor-frontend #104] — GA4 (`$trackingGA4`) + GA3 (`$tracking`) injection, external-mode fetcher adapter; still pins vue 43.40.0, pin-bump commit to follow before merge
- [{repo}/customer-dashboard-frontend/pull/40 customer-dashboard-frontend #40] — GA4 + GA3 via `useTracking` adapter (app has a bare GA client)
- [{repo}/supplier-onboarding-frontend/pull/591 supplier-onboarding-frontend #591] — GA4 + GA3 dual injection
- [{repo}/business-insights-frontend/pull/324 business-insights-frontend #324] — GA3 only (app tracks UA-only)
- [{repo}/visitors-frontend/pull/248 visitors-frontend #248] — GA3 only (GA4 disabled in this app); added `Tracking.show()` for non-interaction events
- [{repo}/ad-center-frontend/pull/80 ad-center-frontend #80] — GA4 adapter only (GA3 disabled in this app)
""".format(repo=GH)

c686 = """Pull request delivering the delete account entry:

- [{repo}/user-frontend/pull/233 user-frontend #233] — *CTOOL-679: Alibaba account delete entry with two-step feedback flow (My Account)*
  - Delete entry moved into the AccountDeletion card per design; two-step modal flow (reason feedback → confirmation); unlinking status via IAM user-backend, feedback reported via `POST /api/feedbacks` (survey `delete_alibaba_account`); 21 locales.
  - Note: the confirm step cannot be E2E-verified on staging until the IAM v3.0 endpoint is deployed (soft-fail, non-blocking).
""".format(repo=GH)

c683 = """Note on frontend delivery: the banner's BV-pending (`under_review`) variant — the frontend piece of the BV status display — is implemented within [{repo}/visable-vue/pull/738 visable-vue #738] and integrated via product-editor-frontend #104 / customer-dashboard-frontend #40. `GET /bv/status` currently returns 403 on staging (backend/gateway enablement pending); the banner degrades gracefully (fail-closed) in the meantime.
""".format(repo=GH)

c679 = """## Summary — Frontend delivery (8 PRs across 8 repositories)

All frontend work under this epic is code-complete and open for review. Mapping to child tasks:

### Shared component (CTOOL-684)
- [{repo}/visable-vue/pull/738 visable-vue #738] — self-contained `VisAlibabaOnboardingBanner`: internal data layer, GA4+GA3 dual-channel funnel tracking, 21 locales, wlw theme, BV-pending variant (also serves CTOOL-683's frontend piece)

### Banner integration (CTOOL-685)
- [{repo}/product-editor-frontend/pull/104 product-editor-frontend #104]
- [{repo}/customer-dashboard-frontend/pull/40 customer-dashboard-frontend #40]
- [{repo}/supplier-onboarding-frontend/pull/591 supplier-onboarding-frontend #591]
- [{repo}/business-insights-frontend/pull/324 business-insights-frontend #324]
- [{repo}/visitors-frontend/pull/248 visitors-frontend #248]
- [{repo}/ad-center-frontend/pull/80 ad-center-frontend #80]

Each app injects only the trackers it actually has (see per-task comment on CTOOL-685); funnel logic lives inside the component, dimension enrichment stays in the app wrappers.

### Delete account entry (CTOOL-686)
- [{repo}/user-frontend/pull/233 user-frontend #233] — two-step delete flow in My Account (CTOOL-686)

### Release status
- Component published as `@visable-dev/vue@43.44.0-beta.6` (tag `v43.44.0-beta.6`). The 5 supplier apps above are pinned to it; **product-editor-frontend still pins 43.40.0 — a pin-bump commit will follow on #104 before merge**.
- Tags `v43.44.0-beta.3`–`beta.5` had failed CI on stylelint (`color-hex-length`); fixed by `cf597b3c`.

### Known blockers / follow-ups
- `GET /bv/status` returns 403 on staging — backend/gateway enablement pending; banner degrades fail-closed.
- `/api/membership-management` edge routing confirmation (iac) for customer-dashboard / user-frontend.
- IAM v3.0 endpoint deployment needed to E2E-verify the delete confirm step (#233).
- GA3 funnel events: final verification via GA DebugView on staging.
- Machine-translated locales (19 languages) pending native-speaker review, consent copy especially.
""".format(repo=GH)

for key, body in [("CTOOL-684", c684), ("CTOOL-685", c685), ("CTOOL-686", c686), ("CTOOL-683", c683), ("CTOOL-679", c679)]:
    comment(key, body)
