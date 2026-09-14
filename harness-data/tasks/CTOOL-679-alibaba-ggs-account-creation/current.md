# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-679-alibaba-ggs-account-creation (Jira CTOOL-679)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: visable-vue · product-editor-frontend (primary) · customer-dashboard-frontend · business-insights-frontend · visitors-frontend · ad-center-frontend · supplier-onboarding-frontend · user-frontend # business-insights/visitors/ad-center/supplier-onboarding not yet registered in harness (§4 onboarding pending)
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-679-alibaba-ggs-account-creation/ # project artifacts, committed with the feature branch
- current stage: `self-test` — **MMB staging 协议落地：company_address + platforms**（2026-09-14，后端 Lee 的 Staging 联调记录）：companies 新增 `company_address`（之前"待 MMB 补地址"已解决）和 `platforms`（['ep'] 或 ['wlw','ep']）→ 公司卡品牌标改为**按公司数据驱动**（单/双平台角标），替代此前静态双标；类型/映射/dev mock/spec fixture 三仓库同步（visable-vue c1a647bf + 新增平台角标测试 21/21、product-editor 1b1d8b5b、customer-dashboard 5657473，均未 push）；Chrome 实测 Example GmbH(['ep'])单标、Another Ltd(['wlw','ep'])双标 ✓。协议其余部分（路径 /gtm/*、X-Supplier-Id、静态 i18n 失败文案、account-deletion 404 无需对接）与现有实现一致无需改。注意：**user-frontend 当前 checkout 在他人 DRG 分支**（CTOOL-679 删除入口在 `CTOOL-679/alibaba-delete-entry` 分支），协议变更不涉及它（只读 banner_status）；X-Forwarded-Auth-User-Profile 由网关注入，BFF 转发逻辑不变。本轮之前：client-only 可见性 44405e4d、按钮 loading+弹窗内成败态 63b9ee00/5533e9ca/73e22d7、间距 3f8fa685、公司卡 841b6bb8
- single next step: user re-verifies in browser → push updated branches → Task 6 release train (PRs, tag v43.45.0-beta.1, apps upgrade pins) and/or resume Task 5 (4 supplier apps — paused, needs explicit go-ahead)；待办：wlw 蓝主题变体、consent 链接 URL 法务（address 已随 staging 协议解决）
- Jira structure (2026-09-12): CTOOL-679 = Epic (relates to CTOOL-624, parent removed); children CTOOL-684 (components, done) / CTOOL-685 (supplier-app integration: product-editor + customer-dashboard done, 4 apps paused) / CTOOL-686 (user-frontend delete entry, done)
- blockers (if any): none — API contract now LANDED (MMB); remaining open item is the edge route for MMB on www hosts (customer-dashboard/user-frontend same-origin paths) to confirm in iac
