# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-679-alibaba-ggs-account-creation (Jira CTOOL-679)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: visable-vue · product-editor-frontend (primary) · customer-dashboard-frontend · business-insights-frontend · visitors-frontend · ad-center-frontend · supplier-onboarding-frontend · user-frontend # business-insights/visitors/ad-center/supplier-onboarding not yet registered in harness (§4 onboarding pending)
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-679-alibaba-ggs-account-creation/ # project artifacts, committed with the feature branch
- current stage: `self-test` — **dev mock 移除：直读真实 MMB 返回**（2026-09-14，用户指示"去除mock，直接引用接口的返回数据"）：PE api 工厂删 devMockApi + dev 身份 gate，`$customFetch` 直连网关端点成为唯一路径（`?status=`/`?fail=1` 驱动能力随之取消，UI 成败态模拟退回 spec fixture）；PE c68b6815（未 push）。Chrome 实测真实 staging 数据全链路 ✓：overview 200（`show_banner:true`；EuroPack Germany ['ep'] is_bound:false + Farsoon Technology ['wlw','ep'] is_bound:true）、选择器按 is_bound 过滤只显示 EuroPack（真实地址+单 ep 角标）；**activate 未代点**（真实 POST 留给用户自验；此前 403=staging 权限限制）。PE 全量 1034/1034 ✓。本轮之前：网关直连 88740ae3/58a7ba4（删 Nitro BFF、devUserProfile 移 runtimeConfig.public、dev mock 曾内联）、staging 协议 1b1d8b5b/c1a647bf/5657473、client-only 44405e4d、弹窗内成败态 63b9ee00/5533e9ca/73e22d7、间距 3f8fa685
- single next step: user re-verifies in browser（含点击 activate 走真实 create-account——403 则需后端开测试账号权限）→ push updated branches → Task 6 release train (PRs, tag v43.45.0-beta.1, apps upgrade pins) and/or resume Task 5 (4 supplier apps — paused, needs explicit go-ahead)；待办：wlw 蓝主题变体、consent 链接 URL 法务、真实 E2E 完成后删剩余 dev 脚手架（现仅剩 NUXT_DEV_USER_PROFILE 身份注入 + 401 旁路）
- Jira structure (2026-09-12): CTOOL-679 = Epic (relates to CTOOL-624, parent removed); children CTOOL-684 (components, done) / CTOOL-685 (supplier-app integration: product-editor + customer-dashboard done, 4 apps paused) / CTOOL-686 (user-frontend delete entry, done)
- blockers (if any): none — iac 侧 www 域名对 /api/membership-management 的边缘路由仍待确认（customer-dashboard/user-frontend same-origin）；另注意 user-frontend 的 CTOOL-679 分支后续需同步网关直连路径
