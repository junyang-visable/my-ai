# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-634 — Nexus WhatsApp Integration: Supplier Portal Frontend (Message Reminder Settings)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: product-editor-frontend (primary) · visable-vue · routing-lib · wlw_nginx
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-634/ # project artifacts, committed with the feature branch
- current stage: `联调中` # UI+BFF 代理全部完成并 push（app c72086a7、nginx 743a9c8）；同源 /supplier-settings-api/{list,update,bind-link,unbind}，上游映射收在 server 路由内
- single next step: 后端确认 api.staging.visable.io 对 /conversations-backend 的 403 准入要求 → 全链路验证 → PRs + evidence
- blockers (if any): 网关 403（准入要求待后端确认）；Atlassian MCP OAuth 过期（Confluence 契约页暂不可读，待重新授权）
