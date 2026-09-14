# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-679-alibaba-ggs-account-creation (Jira CTOOL-679)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: visable-vue · product-editor-frontend (primary) · customer-dashboard-frontend · business-insights-frontend · visitors-frontend · ad-center-frontend · supplier-onboarding-frontend · user-frontend # business-insights/visitors/ad-center/supplier-onboarding not yet registered in harness (§4 onboarding pending)
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-679-alibaba-ggs-account-creation/ # project artifacts, committed with the feature branch
- current stage: `self-test` — **按钮 loading + 弹窗内成功/失败态落地**（2026-09-14，用户需求）：①activate/retry 不再切独立 spinner 页——留在当前视图，主按钮用 DS `btn--spinner`（VisButton `pending` prop），Cancel 请求中隐藏；banner 新增 `pending` prop（awaiting || status in_progress）。②接口返回不关窗——成功态（绿告警条 #f2f7e7/#c4dd8b(primary-50)/#5b8200+勾图标，r8）停留展示，用户点 Got it **或关 X** 后 app 才 `acknowledgeCreation()` 退场 banner；失败态（红告警条 #fce8ed/#f7b9c8/#a00f32+感叹号图标）Try again 重试。③跨会话 in_progress 落在确认页 pending（watch 里 step=confirmation）。modal 删除 progress state/独立 spinner/progress 文案（en/de）。Chrome 全流程实测：按钮 loading ✓ → 成功告警条 ✓ → Got it 后 banner 消失 ✓；失败流 ✓ → X 关闭 banner 保留 ✓。Commits: visable-vue 63b9ee00, product-editor 5533e9ca, customer-dashboard 73e22d7（均未 push）。前两轮：间距修复 3f8fa685、STEP2 公司卡 841b6bb8（address 待 MMB 补字段、wlw 蓝主题待办）
- single next step: user re-verifies STEP 2 card in browser → push updated branches → Task 6 release train (PRs, tag v43.45.0-beta.1, apps upgrade pins) and/or resume Task 5 (4 supplier apps — paused, needs explicit go-ahead)；待办：MMB 补 address 字段确认、wlw 蓝主题变体、consent 链接 URL 法务
- Jira structure (2026-09-12): CTOOL-679 = Epic (relates to CTOOL-624, parent removed); children CTOOL-684 (components, done) / CTOOL-685 (supplier-app integration: product-editor + customer-dashboard done, 4 apps paused) / CTOOL-686 (user-frontend delete entry, done)
- blockers (if any): none — API contract now LANDED (MMB); remaining open item is the edge route for MMB on www hosts (customer-dashboard/user-frontend same-origin paths) to confirm in iac
