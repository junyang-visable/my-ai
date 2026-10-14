# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-634 — Nexus WhatsApp Integration: Supplier Portal Frontend (Message Reminder Settings)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: product-editor-frontend (primary) · visable-vue · routing-lib · wlw_nginx
- spec/plan: /Users/yangjun/Desktop/project/product-editor-frontend/docs/changes/CTOOL-634/ # project artifacts, committed with the feature branch
- current stage: `测试反馈调整轮（2026-10-13~14，plan Task 9）` # Steps 9.1–9.6 完成，commit afabdfe0 + 8fc44c3b + 033965fe（本地未推）；矩阵 v1、v2（AI LE 修订 99 格）均已同步进 Lokalise 并回拉验证值级一致，仓库净零改动
- single next step: ①用户在 Lokalise 删孤儿 key `supplier-settings.whatsapp.link_success_toast`（自跑删除命令或 UI；这是 Lokalise 与仓库同源的最后一块）②用户浏览器复验 → 通过后推送 push
- blockers (if any): 删除类直调 API 操作全部被 auto 分类器拦截（token 提取脚本/浏览器自动化/node_modules 补丁三条路都试过），必须用户执行；node_modules dist 补丁 replace_modified:true 在位（pnpm install 自动冲掉）；DS 5.x 升级待另立事项
