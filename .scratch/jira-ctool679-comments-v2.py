#!/usr/bin/env python3
"""Update the 5 CTOOL comments in place with proper [text](url) markdown links."""
import json, importlib.util

spec = importlib.util.spec_from_file_location("amc", "/Users/yangjun/Desktop/my-ai/.scratch/atlassian-mcp-call.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
init = m.rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "qoder-direct", "version": "1.0"}})
m.rpc("notifications/initialized", {}, notify=True)

CLOUD = "visable.atlassian.net"
GH = "https://github.com/visable-dev"

L = {
    "vue": f"{GH}/visable-vue/pull/738",
    "pe": f"{GH}/product-editor-frontend/pull/104",
    "cd": f"{GH}/customer-dashboard-frontend/pull/40",
    "so": f"{GH}/supplier-onboarding-frontend/pull/591",
    "bi": f"{GH}/business-insights-frontend/pull/324",
    "vf": f"{GH}/visitors-frontend/pull/248",
    "ac": f"{GH}/ad-center-frontend/pull/80",
    "uf": f"{GH}/user-frontend/pull/233",
}

bodies = {
    "CTOOL-684": f"""Pull request delivering the shared component:

- [visable-vue #738]({L['vue']}) — *CTOOL-679: self-contained Alibaba onboarding banner (GA4+GA3 tracking)*
  - Single public component `VisAlibabaOnboardingBanner` (activation modal as internal subcomponent), self-contained data layer (injectable fetcher / gateway base) and self-contained funnel tracking (`ga4Tracker` / `ga3Tracker` props), status-driven visibility incl. the BV-pending (`under_review`) variant, wlw blue theme variant, 21 locales.
  - Published to GitHub Packages as `@visable-dev/vue@43.44.0-beta.6` (tag `v43.44.0-beta.6`); beta.3–beta.5 tags had failed CI on stylelint (`color-hex-length`), fixed by `cf597b3c`.
""",
    "CTOOL-685": f"""Pull requests delivering the banner integration, one per supplier app (branches `CTOOL-679/*`, component pinned to `@visable-dev/vue@43.44.0-beta.6`):

- [product-editor-frontend #104]({L['pe']}) — GA4 (`$trackingGA4`) + GA3 (`$tracking`) injection, external-mode fetcher adapter; still pins vue 43.40.0, pin-bump commit to follow before merge
- [customer-dashboard-frontend #40]({L['cd']}) — GA4 + GA3 via `useTracking` adapter (app has a bare GA client)
- [supplier-onboarding-frontend #591]({L['so']}) — GA4 + GA3 dual injection
- [business-insights-frontend #324]({L['bi']}) — GA3 only (app tracks UA-only)
- [visitors-frontend #248]({L['vf']}) — GA3 only (GA4 disabled in this app); added `Tracking.show()` for non-interaction events
- [ad-center-frontend #80]({L['ac']}) — GA4 adapter only (GA3 disabled in this app)
""",
    "CTOOL-686": f"""Pull request delivering the delete account entry:

- [user-frontend #233]({L['uf']}) — *CTOOL-679: Alibaba account delete entry with two-step feedback flow (My Account)*
  - Delete entry moved into the AccountDeletion card per design; two-step modal flow (reason feedback → confirmation); unlinking status via IAM user-backend, feedback reported via `POST /api/feedbacks` (survey `delete_alibaba_account`); 21 locales.
  - Note: the confirm step cannot be E2E-verified on staging until the IAM v3.0 endpoint is deployed (soft-fail, non-blocking).
""",
    "CTOOL-683": f"""Note on frontend delivery: the banner's BV-pending (`under_review`) variant — the frontend piece of the BV status display — is implemented within [visable-vue #738]({L['vue']}) and integrated via product-editor-frontend #104 / customer-dashboard-frontend #40. `GET /bv/status` currently returns 403 on staging (backend/gateway enablement pending); the banner degrades gracefully (fail-closed) in the meantime.
""",
    "CTOOL-679": f"""## Summary — Frontend delivery (8 PRs across 8 repositories)

All frontend work under this epic is code-complete and open for review. Mapping to child tasks:

### Shared component (CTOOL-684)
- [visable-vue #738]({L['vue']}) — self-contained `VisAlibabaOnboardingBanner`: internal data layer, GA4+GA3 dual-channel funnel tracking, 21 locales, wlw theme, BV-pending variant (also serves CTOOL-683's frontend piece)

### Banner integration (CTOOL-685)
- [product-editor-frontend #104]({L['pe']})
- [customer-dashboard-frontend #40]({L['cd']})
- [supplier-onboarding-frontend #591]({L['so']})
- [business-insights-frontend #324]({L['bi']})
- [visitors-frontend #248]({L['vf']})
- [ad-center-frontend #80]({L['ac']})

Each app injects only the trackers it actually has (see per-task comment on CTOOL-685); funnel logic lives inside the component, dimension enrichment stays in the app wrappers.

### Delete account entry (CTOOL-686)
- [user-frontend #233]({L['uf']}) — two-step delete flow in My Account (CTOOL-686)

### Release status
- Component published as `@visable-dev/vue@43.44.0-beta.6` (tag `v43.44.0-beta.6`). The 5 supplier apps above are pinned to it; **product-editor-frontend still pins 43.40.0 — a pin-bump commit will follow on #104 before merge**.
- Tags `v43.44.0-beta.3`–`beta.5` had failed CI on stylelint (`color-hex-length`); fixed by `cf597b3c`.

### Known blockers / follow-ups
- `GET /bv/status` returns 403 on staging — backend/gateway enablement pending; banner degrades fail-closed.
- `/api/membership-management` edge routing confirmation (iac) for customer-dashboard / user-frontend.
- IAM v3.0 endpoint deployment needed to E2E-verify the delete confirm step (#233).
- GA3 funnel events: final verification via GA DebugView on staging.
- Machine-translated locales (19 languages) pending native-speaker review, consent copy especially.
""",
}


def last_comment_id(key):
    res = m.rpc("tools/call", {"name": "getJiraIssue", "arguments": {
        "cloudId": CLOUD, "issueIdOrKey": key, "fields": ["comment"]}})
    inner = json.loads(res["result"]["content"][0]["text"])
    cs = inner["fields"]["comment"]["comments"]
    return cs[-1]["id"] if cs else None


for key, body in bodies.items():
    cid = last_comment_id(key)
    if not cid:
        print(key, "SKIP (no comment found)")
        continue
    res = m.rpc("tools/call", {"name": "addCommentToJiraIssue", "arguments": {
        "cloudId": CLOUD, "issueIdOrKey": key, "commentId": cid,
        "commentBody": body, "contentFormat": "markdown"}})
    ok = res and "result" in res
    print(key, "updated" if ok else "FAIL", cid, "" if ok else json.dumps(res)[:300])
