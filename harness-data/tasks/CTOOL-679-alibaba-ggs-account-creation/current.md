# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-679-alibaba-ggs-account-creation (Jira CTOOL-679)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: visable-vue · product-editor-frontend (primary) · customer-dashboard-frontend · business-insights-frontend · visitors-frontend · ad-center-frontend · supplier-onboarding-frontend · user-frontend # business-insights/visitors/ad-center/supplier-onboarding not yet registered in harness (§4 onboarding pending)
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-679-alibaba-ggs-account-creation/ # project artifacts, committed with the feature branch
- current stage: `self-test` — **banner 可见性改 client-only**（2026-09-14，用户报 SSR 闪现）：dismiss 标记在 localStorage 服务端读不到 → SSR 渲染 banner 后水合消失闪烁。product-editor useAsyncData 加 `{server: false}`（overview 只在客户端取，SSR HTML 不含 banner），代价是 eligible 用户 banner 改为水合后出现（用户拍板接受）。Chrome 实测：dismissed 刷新 banner 全程不出现 ✓；eligible 刷新正常显示 ✓；curl SSR HTML 0 命中 ✓。**customer-dashboard 是 SPA（index.html+vite）无 SSR，天然无此问题，未改**；user-frontend 无 banner 不涉及。Commit: product-editor 44405e4d（未 push）。本轮之前：按钮 loading+弹窗内成败态 63b9ee00/5533e9ca/73e22d7；间距 3f8fa685；公司卡 841b6bb8（address 待 MMB 补、wlw 蓝主题待办）
- single next step: user re-verifies STEP 2 card in browser → push updated branches → Task 6 release train (PRs, tag v43.45.0-beta.1, apps upgrade pins) and/or resume Task 5 (4 supplier apps — paused, needs explicit go-ahead)；待办：MMB 补 address 字段确认、wlw 蓝主题变体、consent 链接 URL 法务
- Jira structure (2026-09-12): CTOOL-679 = Epic (relates to CTOOL-624, parent removed); children CTOOL-684 (components, done) / CTOOL-685 (supplier-app integration: product-editor + customer-dashboard done, 4 apps paused) / CTOOL-686 (user-frontend delete entry, done)
- blockers (if any): none — API contract now LANDED (MMB); remaining open item is the edge route for MMB on www hosts (customer-dashboard/user-frontend same-origin paths) to confirm in iac
