# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-679-alibaba-ggs-account-creation (Jira CTOOL-679)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: visable-vue · product-editor-frontend (primary) · customer-dashboard-frontend · business-insights-frontend · visitors-frontend · ad-center-frontend · supplier-onboarding-frontend · user-frontend # business-insights/visitors/ad-center/supplier-onboarding not yet registered in harness (§4 onboarding pending)
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-679-alibaba-ggs-account-creation/ # project artifacts, committed with the feature branch
- current stage: `self-test` — **modal spacing fixed to the GTM STEP 1 frame** (2026-09-14, user report): root causes were phantom token `--v-size-75` (never existed → VisModal fell back to 480px), zero padding on VisModal's `article` (default slot has none), and a uniform 16px flex gap vs the design's 32px sections / 8px lead. Fix: 600px via `--vis-modal-width` on a fallthrough `.alibaba-modal` class, padding-block 20/32 + `var(--_padding-inline)`, section gap 32 / lead 8 / actions 16, `.narrow` 450px centered column, title display-600, green text links. Measured in Chrome (600w, gaps 32/8/16, #7faf0d) + Step1/Step2 screenshots. Also fixed stylelint max-nesting-depth ×3 (pre-existing) — `yarn lint:style` clean. Commit: visable-vue 3f8fa685 (NOT pushed). Apps need no change (dev symlink picks it up)
- single next step: user re-verifies the modal in browser → push updated branches → Task 6 release train (PRs, tag v43.45.0-beta.1, apps upgrade pins) and/or resume Task 5 (4 supplier apps — paused, needs explicit go-ahead)
- Jira structure (2026-09-12): CTOOL-679 = Epic (relates to CTOOL-624, parent removed); children CTOOL-684 (components, done) / CTOOL-685 (supplier-app integration: product-editor + customer-dashboard done, 4 apps paused) / CTOOL-686 (user-frontend delete entry, done)
- blockers (if any): none — API contract now LANDED (MMB); remaining open item is the edge route for MMB on www hosts (customer-dashboard/user-frontend same-origin paths) to confirm in iac
