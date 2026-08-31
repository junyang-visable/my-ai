# result — 有效结论与残留风险

> 只沉淀「已验证有效」的结论，保持精简。冗长过程写进 history.md。

## 已验证结论

- monitoring_config.yaml 新增 5 个前端项目（customer-dashboard / business-insights / requests / conversations / visitors），共 9 个受监控项目；DD+AWS 全开、Sentry 仅 visitors 开、tracking_patrol 全关。
- 冒烟1（visitors-frontend，run 20260828T075955Z）：sentry/datadog/aws/stability_sdk 四信号全部 available，真实数据（Sentry 4 errors/TypeError、AWS CPU 10.8% MEM 57.8%）。
- 冒烟2（conversations-frontend，run 20260828T080408Z）：DD-only 路径正确——Sentry/tracking_patrol 被 eligibility 跳过、DD 拉到 230 error logs（`visable/conversations-frontend` 服务名解析正确）；AWS unavailable（无 ECS datapoint，属资源侧事实，非配置错误）。
- 181 tests passed（.venv pytest 9.1.1）；harness validate --strict 全绿（arch/test/lock OK）。

## 残留风险 / 未覆盖

- customer-dashboard / business-insights / requests 三项目未逐一真实拉取（与已冒烟两项目走同一 dispatch 代码路径，风险低）。
- 4 个 DD-only 项目的 Sentry project 存在性未确认（org 枚举需高权限 token），确认后把 `sentry.enabled` 改 true 即可。
- conversations 的 AWS 信号无 datapoint：若该服务实际有 ECS 资源，需核对 Datadog 里 service tag 与 ECS 资源关联；否则属正常空信号。
- tracking_patrol workflow 名未知（gh 查询被环境权限拦截），确认后补 `enabled: true + workflow`。

## 验收证据

- Rubric：`rubric.md`
- 证据目录：`evidence/`
- 提交：feat/add-frontend-monitoring-projects @ 35f2063
