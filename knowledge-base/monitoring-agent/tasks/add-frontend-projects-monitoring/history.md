# history — 只追加日志

> 每次动作追加一行，永不回改。格式：时间 ｜ 动作 ｜ 结果/证据。

- 2026-08-28 ｜ 澄清：用户圈定 5 项目（customer-dashboard / business-insights / requests / conversations / visitors），策略=DD+AWS 全开、Sentry 只开已确认的 visitors、tracking_patrol 全关 ｜ 依据 docs/frontend-monitoring-capabilities.json 的 DD services_census + Sentry discovered_projects
- 2026-08-28 ｜ 编码：分支 feat/add-frontend-monitoring-projects（自 origin/master）上改 monitoring_config.yaml 新增 5 个 project 条目 ｜ diff 仅单文件
- 2026-08-28 ｜ 自测：config 解析验证（9 项目、信号开关符合预期）+ 181 tests passed（.venv pytest 9.1.1）+ harness validate --strict 全绿 ｜ 冒烟 run 见下行
- 2026-08-28 ｜ 冒烟：visitors-frontend 端到端 run 20260828T075955Z，sentry/datadog/aws/stability 四信号 available 且拉到真实数据（Sentry 4 errors、AWS CPU 10.8%） ｜ 证据已归档 evidence/smoke-visitors-20260828T075955Z
- 2026-08-28 ｜ 提交：35f2063 feat(orchestrator): add 5 frontend projects to monitoring config（分支 feat/add-frontend-monitoring-projects，未推送） ｜ 待用户验证后推送
- 2026-08-28 ｜ 冒烟2：conversations-frontend run 20260828T080408Z 验证 DD-only 路径：Sentry/tracking_patrol 正确跳过；DD 拉到 230 error logs（Proxy error 115，服务名解析正确）；AWS unavailable=无 ECS datapoint（该服务无 AWS 资源或 tag 缺失，非配置错误，unavailable 不阻断） ｜ 证据 evidence/smoke-conversations-20260828T080408Z
