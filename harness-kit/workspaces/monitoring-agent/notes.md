# monitoring-agent 仓库经验笔记

> 该仓库的栈、命令实测、坑与约定。任务级过程写 tasks/<需求名>/history.md，
> 跨仓库通用的经验提练到 kit 的 playbooks/<主题>.md。

## 栈与命令实测
- 纯 Python 仓库（无 lint/typecheck/build 配置）。测试用仓库自带 `.venv`（pytest 9.1.1）：`.venv/bin/python -m pytest tests/ -v`，181 tests 约 10s。系统 python3.14 无 pytest，勿用裸 `python3 -m pytest`。
- 端到端冒烟：`.venv/bin/python skills/monitoring-orchestrator/signal_collector.py --projects <name> --intent last_24h`——venv 环境下 DD/Sentry/AWS 凭据实际可用（2026-08-28 实测三信号 available，产物落 artifacts/monitoring/<run_id>/）。单项目全流程约 2-4 分钟（含 Stability 管线 A-C6 SQL），超出 Bash 2 分钟上限需放后台。

## 坑与约定
- Bash 工具 cwd 每次命令后重置回会话主目录：操作本仓库必须带 `dir_path`，否则 git 会误跑在 my-ai 上（实测踩坑）。
- 默认分支 `master`（不是 main）。
- monitoring_config.yaml 是入库实配置：新增项目条目参考 `docs/frontend-monitoring-capabilities.json` 的 `platforms.datadog.services_census`（7 日日志量普查）与 `platforms.sentry.services_census.discovered_projects`（已确认存在的 Sentry project）。
- 约定：`appName = Sentry project slug = ODPS app_name`；DD service 命名不统一（`visable-dev/`、`webdevs/`、`visable/`、无前缀均有），必须按 census 实际值写 `datadog.service` 覆盖，不能猜。
- 信号开关语义：`enabled: false` 在 eligibility 阶段被干净跳过，运行无副作用；仓库约定"确认平台资源后再启用"。
- gh 查 visable-dev org 仓库会被本环境权限分类器拦截（判为与当前仓库无关）；shell profile 搜凭据也被安全策略拦——枚举外部资源优先用仓库 docs 普查数据或 Datadog MCP。
- Datadog MCP 的 aggregate-logs 返回 `[object Object]`（序列化损坏）不可用；search-logs 正常。
- 契约测试 `test_monitoring_orchestrator_contract.py` 只锁 stability_sdk 段，不锁 projects 列表——增删项目不会破坏契约。
