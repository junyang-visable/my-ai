# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-679-alibaba-ggs-account-creation (Jira CTOOL-679)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: visable-vue · product-editor-frontend (primary) · customer-dashboard-frontend · business-insights-frontend · visitors-frontend · ad-center-frontend · supplier-onboarding-frontend · user-frontend # business-insights/visitors/ad-center/supplier-onboarding not yet registered in harness (§4 onboarding pending)
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-679-alibaba-ggs-account-creation/ # project artifacts, committed with the feature branch
- current stage: `self-test` — **dev 脚手架清零**（2026-09-14，用户指示"把剩余的身份注入和 401 旁路也删掉"）：删 auth store 的 `NUXT_DEV_USER_PROFILE` 身份注入块（fetchUserInfo 回归纯真实 whoami）、fetch.ts `navigateToSupplierLogin` 的 401 旁路、nuxt.config 的 `devUserProfile`（runtimeConfig.public）——PE 仓库不再有任何 NUXT_DEV_* env 依赖；spec stub 同步精简（useRuntimeConfig stub 保留，因 useBaseURL 读 stage）。本地 dev 登录态 = dev proxy 转发的真实 staging 会话（与 banner api 一致）。PE 163126a2（未 push）。验证：全量 1034/1034 ✓、eslint ✓、Chrome 实测真实 whoami 登录正常 + overview 200 + banner 照常渲染。dev-only 三件套至此全部移除（mock ⑧、身份注入+401 旁路 ⑨）。本轮之前：mock 移除 c68b6815、网关直连 88740ae3/58a7ba4、staging 协议 1b1d8b5b/c1a647bf/5657473、client-only 44405e4d、弹窗内成败态 63b9ee00/5533e9ca/73e22d7、间距 3f8fa685
- single next step: user re-verifies in browser（含点击 activate 走真实 create-account——403 则需后端开测试账号权限）→ push updated branches → Task 6 release train (PRs, tag v43.45.0-beta.1, apps upgrade pins) and/or resume Task 5 (4 supplier apps — paused, needs explicit go-ahead)；待办：wlw 蓝主题变体、consent 链接 URL 法务
- Jira structure (2026-09-12): CTOOL-679 = Epic (relates to CTOOL-624, parent removed); children CTOOL-684 (components, done) / CTOOL-685 (supplier-app integration: product-editor + customer-dashboard done, 4 apps paused) / CTOOL-686 (user-frontend delete entry, done)
- blockers (if any): none — iac 侧 www 域名对 /api/membership-management 的边缘路由仍待确认（customer-dashboard/user-frontend same-origin）；另注意 user-frontend 的 CTOOL-679 分支后续需同步网关直连路径
