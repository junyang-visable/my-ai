# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-679-alibaba-ggs-account-creation (Jira CTOOL-679)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: visable-vue · product-editor-frontend (primary) · customer-dashboard-frontend · business-insights-frontend · visitors-frontend · ad-center-frontend · supplier-onboarding-frontend · user-frontend # business-insights/visitors/ad-center/supplier-onboarding not yet registered in harness (§4 onboarding pending)
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-679-alibaba-ggs-account-creation/ # project artifacts, committed with the feature branch
- current stage: `self-test` — **STEP 2 company card restored** (2026-09-14, user report): selected card bg #f2f7e7 + green-100 stroke + 24px radio-dot (was 16px checkmark), unselected border #b5bdb9, address line (14px, darkgreen-100), 48px white avatar w/ neutral-20 border, bold name (display-400), **ep+wlw 双品牌标并排**（右侧，静态两个都展示——公司同时挂在两平台；SVG 从 Figma 511:30253/30254 导出）。卡片全宽 536（.narrow 移除）、卡间距 24、picker 改为 ≥1 公司即渲染（单公司预选中，设计 511:30225 如此）。**address 字段 MMB 契约（2026-09-14）没有**——前端类型加 `address?`（标 UNCONFIRMED）+ 透传 + dev mock 填了样例地址，需 MMB 补字段。**wlw 蓝色主题变体**（560:2369：#0060df accent/#e5effb 选中底）未实现——按钮/链接还是 DS 绿，单独做才连贯，列为待办。Verified in Chrome（选中底 rgb(242,247,231)、地址渲染、4 个品牌 img）。Commits: visable-vue 841b6bb8, product-editor 12e4d736, customer-dashboard 62f5e16（均未 push）。前一轮：间距修复 3f8fa685（600px/32 节奏/450 列/article padding 幽灵 token 教训）
- single next step: user re-verifies STEP 2 card in browser → push updated branches → Task 6 release train (PRs, tag v43.45.0-beta.1, apps upgrade pins) and/or resume Task 5 (4 supplier apps — paused, needs explicit go-ahead)；待办：MMB 补 address 字段确认、wlw 蓝主题变体、consent 链接 URL 法务
- Jira structure (2026-09-12): CTOOL-679 = Epic (relates to CTOOL-624, parent removed); children CTOOL-684 (components, done) / CTOOL-685 (supplier-app integration: product-editor + customer-dashboard done, 4 apps paused) / CTOOL-686 (user-frontend delete entry, done)
- blockers (if any): none — API contract now LANDED (MMB); remaining open item is the edge route for MMB on www hosts (customer-dashboard/user-frontend same-origin paths) to confirm in iac
