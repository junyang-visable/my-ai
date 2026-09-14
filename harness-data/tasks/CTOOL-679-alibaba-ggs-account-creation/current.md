# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-679-alibaba-ggs-account-creation (Jira CTOOL-679)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: visable-vue · product-editor-frontend (primary) · customer-dashboard-frontend · business-insights-frontend · visitors-frontend · ad-center-frontend · supplier-onboarding-frontend · user-frontend # business-insights/visitors/ad-center/supplier-onboarding not yet registered in harness (§4 onboarding pending)
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-679-alibaba-ggs-account-creation/ # project artifacts, committed with the feature branch
- current stage: `self-test` — **BFF 层移除：MMB 网关直连**（2026-09-14）：研究确认 gtm 端点与 MEMBERSHIP_BASE_PATH 共用同一网关（`/api/membership-management`），无需 app 层 server 代理 → 删除 server/middleware/alibaba-onboarding-api.ts + server/routes/alibaba-onboarding-api/**（devProxy 本就代理 /api → www.wlw-staging.de）；PE 改 `$customFetch` 直连（createAccount `isInternalRequest=false` 保留自选 X-Supplier-Id），dev mock 迁入 api 工厂内部（?status=/?fail=1 驱动不变），CD 同步改直连路径。**关键修复**：`devUserProfile` 原在私有 runtimeConfig（server-only），client 侧 gate（api 工厂、fetch.ts 401 旁路）永远读不到 → 移入 `runtimeConfig.public` 并显式接线 `process.env.NUXT_DEV_USER_PROFILE`（env 名不变，用户 .env 无需改）；连带修出 devMockApi SSR 崩溃（工厂在 layout setup 执行时无 window）→ query 改懒读取。Chrome 实测全流程 ✓：mock 成功态（Got it 后 banner 消失）、失败态+Try again、?status=no_gtm_merchant 隐藏 banner、网络面板零 gtm 请求；真实路径回退此前已证（overview 200 / create-account 403=staging 权限）。PE 全量 1034/1034 ✓。commits：PE 88740ae3、CD 58a7ba4（均未 push）。本轮之前：staging 协议 1b1d8b5b/c1a647bf/5657473（company_address+platforms 数据驱动角标）、client-only 44405e4d、弹窗内成败态 63b9ee00/5533e9ca/73e22d7、间距 3f8fa685
- single next step: user re-verifies in browser → push updated branches → Task 6 release train (PRs, tag v43.45.0-beta.1, apps upgrade pins) and/or resume Task 5 (4 supplier apps — paused, needs explicit go-ahead)；待办：真实 MMB staging 数据可端到端验证后删除 dev-only 脚手架（NUXT_DEV_USER_PROFILE 注入、401 旁路、内联 mock）、wlw 蓝主题变体、consent 链接 URL 法务
- Jira structure (2026-09-12): CTOOL-679 = Epic (relates to CTOOL-624, parent removed); children CTOOL-684 (components, done) / CTOOL-685 (supplier-app integration: product-editor + customer-dashboard done, 4 apps paused) / CTOOL-686 (user-frontend delete entry, done)
- blockers (if any): none — iac 侧 www 域名对 /api/membership-management 的边缘路由仍待确认（customer-dashboard/user-frontend same-origin）；另注意 user-frontend 的 CTOOL-679 分支后续需同步网关直连路径
