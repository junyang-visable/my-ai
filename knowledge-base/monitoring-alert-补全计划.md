# 线上监控告警补全计划

> 基于现有上报途径（Stability SDK → Sunfire、Datadog）与已配置告警规则的逐项盘点，罗列所有需要补充的监控告警。
> Sentry 告警不在本计划范围内——客户端错误面已由 Stability SDK（Sunfire 告警）覆盖。
> 基线数据截至 2026-08-26（[告警能力清单](./V-Frontend-Monitor-告警能力清单.md)）。
> 2026-09-04 增补 user-frontend（08-26 基线审计未覆盖，现状数据源：[极端场景告警配置清单](./extreme-scenario-alert-config.md) 08-28 实测），部分接入状态待盘点。

---

## 一、Stability SDK 事件类型 vs Sunfire 告警覆盖

SDK 采集 6 类错误事件至 ODPS，但 Sunfire 仅对其中 4 类建了告警，**`api_error` 和 `script_error` 在告警层完全裸奔**。

| event_type | 说明 | ODPS 落库 | Sunfire 告警 |
|---|---|---|---|
| `white_screen` | 客户端/SSR 白屏 | ✅ | ✅ 3 项目有 |
| `ssr_error` | SSR 渲染错误 | ✅ | ✅ 3 项目有 |
| `custom_error` | 业务自定义错误 | ✅ | ✅ 3 项目有 |
| `component_error` | 组件渲染错误 | ✅ | ✅ 3 项目有 |
| **`api_error`** | **客户端 API 失败（4xx/5xx/网络/超时）** | ✅ | **❌ 无告警** |
| **`script_error`** | **JS 运行时错误 / 资源加载失败** | ✅ | **❌ 无告警** |

> `api_slow` 已明确排除在监控范围外，不纳入告警。

---

## 二、项目 × 平台告警现状矩阵

✅ = 已有告警 · ❌ = 无告警 · ⏸️ = 已静默

| 项目 | Sunfire 白屏 | Sunfire SSR | Sunfire 自定义 | Sunfire 组件 | Sunfire API错误 | Sunfire 脚本错误 | Datadog |
|---|---|---|---|---|---|---|---|
| search-frontend | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ 6条 |
| homepage-frontend | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ 5条 |
| product-editor-frontend | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ 零规则 |
| unified-search-frontend | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 6条 |
| company-overview | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ (未接入) |
| business-insights | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ✅ 1条 |
| requests-frontend | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ |
| visitors-frontend | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ |
| conversations-frontend | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ |
| user-frontend（09-04 增补） | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ❌ * | ⚠️ 3 条 ECS |

> `*` 标记的项目 SDK 接入状态待确认，需先完成 SDK 接入再建 Sunfire 告警。
> user-frontend 为 2026-09-04 增补（不在 08-26 基线审计内）：Datadog 已接入（AWS ECS 集成确认），08-27 已建 3 条容器全灭 P1 告警（317035916 / 317035974 / 317048648，非标准模板）；Sunfire SDK 落库状态待确认；标准六件套为 0。

---

## 三、需要补充的告警（完整清单）

### 3.1 Sunfire 告警（Stability SDK → ODPS → Sunfire SPM）

公共过滤基线：`env = 'production' AND level = 'error'`，按 `app_name` 和 `event_type` 区分。

#### 3.1.1 现有 3 项目补 `api_error` + `script_error`（6 条）

| # | 项目 | 告警名 | event_type | 阈值建议 | 通知 | 备注 |
|---|---|---|---|---|---|---|
| S-01 | search-frontend | 客户端 API 错误 | `api_error` | delta_5m > 50 | 钉钉 | 量大，阈值需高于白屏 |
| S-02 | search-frontend | 脚本错误 | `script_error` | wow_delta_5m > 100 | 钉钉 | 常态基线高，建议用同比而非环比 |
| S-03 | homepage-frontend | 客户端 API 错误 | `api_error` | delta_5m > 30 | 钉钉 | — |
| S-04 | homepage-frontend | 脚本错误 | `script_error` | wow_delta_5m > 50 | 钉钉 | — |
| S-05 | product-editor-frontend | 客户端 API 错误 | `api_error` | delta_5m > 20 | 钉钉 | 流量较小，阈值下调 |
| S-06 | product-editor-frontend | 脚本错误 | `script_error` | wow_delta_5m > 30 | 钉钉 | — |

> **可选增强**：为每个项目额外建一条 critical API 告警（`api_error` + `is_critical='true'`），阈值设为 delta_5m > 10，实现关键接口失败快速告警。

#### 3.1.2 unified-search-frontend 全 6 类新建（6 条）

| # | 告警名 | event_type | 阈值建议 | 通知 |
|---|---|---|---|---|
| S-07 | 白屏 | `white_screen` | delta_5m > 10 | 钉钉 |
| S-08 | SSR 渲染错误 | `ssr_error` | delta_5m > 10 | 钉钉 |
| S-09 | 自定义业务错误 | `custom_error` | delta_5m > 10 | 钉钉 |
| S-10 | 组件渲染错误 | `component_error` | delta_5m > 10 | 钉钉 |
| S-11 | 客户端 API 错误 | `api_error` | delta_5m > 30 | 钉钉 |
| S-12 | 脚本错误 | `script_error` | wow_delta_5m > 50 | 钉钉 |

#### 3.1.3 扩展项目全 6 类新建（30 条）

> **前提**：以下项目需先确认 Stability SDK 已接入且数据正常落库 ODPS。未接入 SDK 的项目需先完成接入（参照 [能力目录 §8](./monitoring-capability-catalog.md) 接入步骤），再建 Sunfire 告警。

**company-overview**（6 条）

| # | 告警名 | event_type | 阈值建议 | 通知 |
|---|---|---|---|---|
| S-13 | 白屏 | `white_screen` | delta_5m > 10 | 钉钉 |
| S-14 | SSR 渲染错误 | `ssr_error` | delta_5m > 10 | 钉钉 |
| S-15 | 自定义业务错误 | `custom_error` | delta_5m > 10 | 钉钉 |
| S-16 | 组件渲染错误 | `component_error` | delta_5m > 10 | 钉钉 |
| S-17 | 客户端 API 错误 | `api_error` | delta_5m > 20 | 钉钉 |
| S-18 | 脚本错误 | `script_error` | wow_delta_5m > 30 | 钉钉 |

**business-insights-frontend**（6 条）

| # | 告警名 | event_type | 阈值建议 | 通知 |
|---|---|---|---|---|
| S-19 | 白屏 | `white_screen` | delta_5m > 10 | 钉钉 |
| S-20 | SSR 渲染错误 | `ssr_error` | delta_5m > 10 | 钉钉 |
| S-21 | 自定义业务错误 | `custom_error` | delta_5m > 10 | 钉钉 |
| S-22 | 组件渲染错误 | `component_error` | delta_5m > 10 | 钉钉 |
| S-23 | 客户端 API 错误 | `api_error` | delta_5m > 20 | 钉钉 |
| S-24 | 脚本错误 | `script_error` | wow_delta_5m > 30 | 钉钉 |

**requests-frontend**（6 条）

| # | 告警名 | event_type | 阈值建议 | 通知 |
|---|---|---|---|---|
| S-25 | 白屏 | `white_screen` | delta_5m > 10 | 钉钉 |
| S-26 | SSR 渲染错误 | `ssr_error` | delta_5m > 10 | 钉钉 |
| S-27 | 自定义业务错误 | `custom_error` | delta_5m > 10 | 钉钉 |
| S-28 | 组件渲染错误 | `component_error` | delta_5m > 10 | 钉钉 |
| S-29 | 客户端 API 错误 | `api_error` | delta_5m > 20 | 钉钉 |
| S-30 | 脚本错误 | `script_error` | wow_delta_5m > 30 | 钉钉 |

**visitors-frontend**（6 条）

| # | 告警名 | event_type | 阈值建议 | 通知 |
|---|---|---|---|---|
| S-31 | 白屏 | `white_screen` | delta_5m > 10 | 钉钉 |
| S-32 | SSR 渲染错误 | `ssr_error` | delta_5m > 10 | 钉钉 |
| S-33 | 自定义业务错误 | `custom_error` | delta_5m > 10 | 钉钉 |
| S-34 | 组件渲染错误 | `component_error` | delta_5m > 10 | 钉钉 |
| S-35 | 客户端 API 错误 | `api_error` | delta_5m > 20 | 钉钉 |
| S-36 | 脚本错误 | `script_error` | wow_delta_5m > 30 | 钉钉 |

**conversations-frontend**（6 条）

| # | 告警名 | event_type | 阈值建议 | 通知 |
|---|---|---|---|---|
| S-37 | 白屏 | `white_screen` | delta_5m > 10 | 钉钉 |
| S-38 | SSR 渲染错误 | `ssr_error` | delta_5m > 10 | 钉钉 |
| S-39 | 自定义业务错误 | `custom_error` | delta_5m > 10 | 钉钉 |
| S-40 | 组件渲染错误 | `component_error` | delta_5m > 10 | 钉钉 |
| S-41 | 客户端 API 错误 | `api_error` | delta_5m > 20 | 钉钉 |
| S-42 | 脚本错误 | `script_error` | wow_delta_5m > 30 | 钉钉 |

**user-frontend**（6 条，09-04 增补，归属核心项目 / 9.11 前完成）

| # | 告警名 | event_type | 阈值建议 | 通知 |
|---|---|---|---|---|
| S-43 | 白屏 | `white_screen` | delta_5m > 10 | 钉钉 |
| S-44 | SSR 渲染错误 | `ssr_error` | delta_5m > 10 | 钉钉 |
| S-45 | 自定义业务错误 | `custom_error` | delta_5m > 10 | 钉钉 |
| S-46 | 组件渲染错误 | `component_error` | delta_5m > 10 | 钉钉 |
| S-47 | 客户端 API 错误 | `api_error` | delta_5m > 20 | 钉钉 |
| S-48 | 脚本错误 | `script_error` | wow_delta_5m > 30 | 钉钉 |

> user-frontend SDK 落库状态待确认，阈值需落库后按实际基线校准；通知群待确认（暂按钉钉）。

#### Sunfire 小计：48 条（其中 36 条依赖 SDK 接入确认）

---

### 3.2 Datadog 告警

#### 3.2.1 product-editor-frontend — 全套新建（6 条）

当前最大 Datadog 盲区，零规则。参照 search-frontend 模板建立：

| # | 告警名 | 类型 | 指标 / 查询 | 阈值 | 通知 |
|---|---|---|---|---|---|
| D-01 | Memory 使用率超限 | query_alert | `avg(last_5m):aws.ecs.service.memory_utilization.maximum{service:visable-dev/product-editor-frontend}` | critical > 90%, warn > 80% | 钉钉 vcn-frontend |
| D-02 | CPU 使用率超限 | query_alert | `avg(last_5m):aws.ecs.service.cpuutilization.maximum{service:visable-dev/product-editor-frontend}` | critical > 90%, warn > 80% | 钉钉 vcn-frontend |
| D-03 | p75 延迟超限 | query_alert | `percentile(last_5m):trace.web.request{env:production,service:visable-dev/product-editor-frontend,span.kind:server}` | critical > 1.2s, warn > 1s | 钉钉 vcn-frontend |
| D-04 | Server Errors 过多 | query_alert | `sum(last_5m):trace.web.request.errors{env:production,service:visable-dev/product-editor-frontend,span.kind:server}.as_count()` by http.status_code | critical > 50, warn > 30 | 钉钉 vcn-frontend |
| D-05 | SSR 渲染错误 | log_alert | `service:"visable-dev/product-editor-frontend" env:production @errorType:SSRRenderError` | 5min count > 5 (warn > 3) | 钉钉 vcn-frontend |
| D-06 | Status:error 日志过多 | log_alert | `service:"visable-dev/product-editor-frontend" env:production status:error` | 5min count > 120 (warn > 80) | 钉钉 vcn-frontend |

#### 3.2.2 unified-search-frontend — 补基础设施（2 条）

已有 6 条（3 新 + 3 旧），但缺 ECS 基础设施告警：

| # | 告警名 | 类型 | 指标 | 阈值 | 通知 |
|---|---|---|---|---|---|
| D-07 | Memory 使用率超限 | query_alert | `aws.ecs.service.memory_utilization.maximum{service:webdevs/unified-search-frontend}` | critical > 90%, warn > 80% | 钉钉 detailpages |
| D-08 | CPU 使用率超限 | query_alert | `aws.ecs.service.cpuutilization.maximum{service:webdevs/unified-search-frontend}` | critical > 90%, warn > 80% | 钉钉 detailpages |

#### 3.2.3 homepage-frontend — 补 SSR 渲染错误（1 条）

已有 5 条，缺与 search 对齐的 SSR 渲染错误 log alert：

| # | 告警名 | 类型 | 查询 | 阈值 | 通知 |
|---|---|---|---|---|---|
| D-09 | SSR 渲染错误 | log_alert | `service:"visable-dev/homepage-frontend" env:production @errorType:SSRRenderError` | 5min count > 5 (warn > 3) | 钉钉 vcn-frontend |

#### 3.2.4 company-overview — 跳过

> **不需要补 Datadog 告警。** 该项目未接入 Datadog（`enabled: false`，仅 access logs），无 APM trace / Logs 数据。待未来接入 Datadog 后再统一补建。

#### 3.2.5 business-insights-frontend — 全套（6 条）

Datadog `enabled: true`，已有 1 条 log alert（路由错误），补齐剩余 5 条 + 参照核心项目模板补 SSR 渲染错误。

| # | 告警名 | 类型 | 指标 / 查询 | 阈值 | 通知 |
|---|---|---|---|---|---|
| D-12 | Memory 使用率超限 | query_alert | `aws.ecs.service.memory_utilization.maximum{service:business-insights-frontend}` | critical > 90%, warn > 80% | Teams pegasus-alerts |
| D-13 | CPU 使用率超限 | query_alert | `aws.ecs.service.cpuutilization.maximum{service:business-insights-frontend}` | critical > 90%, warn > 80% | Teams pegasus-alerts |
| D-14 | p75 延迟超限 | query_alert | `trace.web.request(p75){env:production,service:business-insights-frontend,span.kind:server}` | critical > 1.2s, warn > 1s | Teams pegasus-alerts |
| D-15 | Server Errors 过多 | query_alert | `trace.web.request.errors(sum){env:production,service:business-insights-frontend,span.kind:server}.as_count()` by http.status_code | critical > 50, warn > 30 | Teams pegasus-alerts |
| D-16 | SSR 渲染错误 | log_alert | `service:"business-insights-frontend" env:production @errorType:SSRRenderError` | 5min count > 5 (warn > 3) | Teams pegasus-alerts |
| D-17 | Status:error 日志过多 | log_alert | `service:"business-insights-frontend" env:production status:error` | 5min count > 120 (warn > 80) | Teams pegasus-alerts |

#### 3.2.6 requests-frontend — 全套新建（6 条）

Datadog `enabled: true`，当前零规则。

| # | 告警名 | 类型 | 指标 / 查询 | 阈值 | 通知 |
|---|---|---|---|---|---|
| D-18 | Memory 使用率超限 | query_alert | `aws.ecs.service.memory_utilization.maximum{service:visable-dev/requests-frontend}` | critical > 90%, warn > 80% | 钉钉 |
| D-19 | CPU 使用率超限 | query_alert | `aws.ecs.service.cpuutilization.maximum{service:visable-dev/requests-frontend}` | critical > 90%, warn > 80% | 钉钉 |
| D-20 | p75 延迟超限 | query_alert | `trace.web.request(p75){env:production,service:visable-dev/requests-frontend,span.kind:server}` | critical > 1.2s, warn > 1s | 钉钉 |
| D-21 | Server Errors 过多 | query_alert | `trace.web.request.errors(sum){env:production,service:visable-dev/requests-frontend,span.kind:server}.as_count()` by http.status_code | critical > 50, warn > 30 | 钉钉 |
| D-22 | SSR 渲染错误 | log_alert | `service:"visable-dev/requests-frontend" env:production @errorType:SSRRenderError` | 5min count > 5 (warn > 3) | 钉钉 |
| D-23 | Status:error 日志过多 | log_alert | `service:"visable-dev/requests-frontend" env:production status:error` | 5min count > 120 (warn > 80) | 钉钉 |

#### 3.2.7 visitors-frontend — 全套新建（6 条）

Datadog `enabled: true`，当前零规则。

| # | 告警名 | 类型 | 指标 / 查询 | 阈值 | 通知 |
|---|---|---|---|---|---|
| D-24 | Memory 使用率超限 | query_alert | `aws.ecs.service.memory_utilization.maximum{service:visable-dev/visitors-frontend}` | critical > 90%, warn > 80% | 钉钉 |
| D-25 | CPU 使用率超限 | query_alert | `aws.ecs.service.cpuutilization.maximum{service:visable-dev/visitors-frontend}` | critical > 90%, warn > 80% | 钉钉 |
| D-26 | p75 延迟超限 | query_alert | `trace.web.request(p75){env:production,service:visable-dev/visitors-frontend,span.kind:server}` | critical > 1.2s, warn > 1s | 钉钉 |
| D-27 | Server Errors 过多 | query_alert | `trace.web.request.errors(sum){env:production,service:visable-dev/visitors-frontend,span.kind:server}.as_count()` by http.status_code | critical > 50, warn > 30 | 钉钉 |
| D-28 | SSR 渲染错误 | log_alert | `service:"visable-dev/visitors-frontend" env:production @errorType:SSRRenderError` | 5min count > 5 (warn > 3) | 钉钉 |
| D-29 | Status:error 日志过多 | log_alert | `service:"visable-dev/visitors-frontend" env:production status:error` | 5min count > 120 (warn > 80) | 钉钉 |

#### 3.2.8 conversations-frontend — 全套新建（6 条）

Datadog `enabled: true`，当前零规则。

| # | 告警名 | 类型 | 指标 / 查询 | 阈值 | 通知 |
|---|---|---|---|---|---|
| D-30 | Memory 使用率超限 | query_alert | `aws.ecs.service.memory_utilization.maximum{service:visable-dev/conversations-frontend}` | critical > 90%, warn > 80% | 钉钉 |
| D-31 | CPU 使用率超限 | query_alert | `aws.ecs.service.cpuutilization.maximum{service:visable-dev/conversations-frontend}` | critical > 90%, warn > 80% | 钉钉 |
| D-32 | p75 延迟超限 | query_alert | `trace.web.request(p75){env:production,service:visable-dev/conversations-frontend,span.kind:server}` | critical > 1.2s, warn > 1s | 钉钉 |
| D-33 | Server Errors 过多 | query_alert | `trace.web.request.errors(sum){env:production,service:visable-dev/conversations-frontend,span.kind:server}.as_count()` by http.status_code | critical > 50, warn > 30 | 钉钉 |
| D-34 | SSR 渲染错误 | log_alert | `service:"visable-dev/conversations-frontend" env:production @errorType:SSRRenderError` | 5min count > 5 (warn > 3) | 钉钉 |
| D-35 | Status:error 日志过多 | log_alert | `service:"visable-dev/conversations-frontend" env:production status:error` | 5min count > 120 (warn > 80) | 钉钉 |

#### 3.2.9 user-frontend — 补常规六件套（6 条，09-04 增补）

Datadog 已接入（AWS ECS 集成确认，ECS servicename `visable-dev_user-frontend_v2_web_internal`），08-27 已建 3 条容器全灭 P1 告警（317035916 / 317035974 / 317048648，不计入标准模板）。常规六件套为 0，前置确认 APM trace / Logs 数据面后补建：

| # | 告警名 | 类型 | 指标 / 查询 | 阈值 | 通知 |
|---|---|---|---|---|---|
| D-36 | Memory 使用率超限 | query_alert | `aws.ecs.service.memory_utilization.maximum{service:visable-dev/user-frontend}` | critical > 90%, warn > 80% | 待确认 |
| D-37 | CPU 使用率超限 | query_alert | `aws.ecs.service.cpuutilization.maximum{service:visable-dev/user-frontend}` | critical > 90%, warn > 80% | 待确认 |
| D-38 | p75 延迟超限 | query_alert | `trace.web.request(p75){env:production,service:visable-dev/user-frontend,span.kind:server}` | critical > 1.2s, warn > 1s | 待确认 |
| D-39 | Server Errors 过多 | query_alert | `trace.web.request.errors(sum){env:production,service:visable-dev/user-frontend,span.kind:server}.as_count()` by http.status_code | critical > 50, warn > 30 | 待确认 |
| D-40 | SSR 渲染错误 | log_alert | `service:"visable-dev/user-frontend" env:production @errorType:SSRRenderError` | 5min count > 5 (warn > 3) | 待确认 |
| D-41 | Status:error 日志过多 | log_alert | `service:"visable-dev/user-frontend" env:production status:error` | 5min count > 120 (warn > 80) | 待确认 |

> Datadog 侧 service tag 暂按 `visable-dev/user-frontend`（与同域项目一致），建单前需按实际数据面核对；通知渠道待确认后填入。

#### Datadog 小计：39 条新建（company-overview 未接入 Datadog，跳过；user-frontend 6 条以数据面确认为前提）

---

### 3.3 Datadog 旧规则清理

| # | 项目 | 规则 ID | 规则名 | 建议 | 理由 |
|---|---|---|---|---|---|
| R-01 | unified-search | [12236842](https://app.datadoghq.com/monitors/12236842) | 全部错误（旧） | 退役 | 阈值 > 0，新规则 284274411 已替代 |
| R-02 | unified-search | [62945068](https://app.datadoghq.com/monitors/62945068) | 5xx 错误（旧） | 退役 | 新规则 284284046 已替代 |
| R-03 | unified-search | [67123179](https://app.datadoghq.com/monitors/67123179) | Error 消息（旧） | 退役 | 被新规则覆盖 |
| R-04 | v-content-generator | 316500911–915 | 重复组 | 删除 | 与 316500817–823 完全重复 |

#### 清理小计：3 条退役 + 5 条去重

---

## 四、汇总

### 4.1 监控覆盖率（补全前 → 补全后）

#### 项目级覆盖率（项目是否有至少 1 条活跃告警）

| 平台 | 适用项目数 | 当前已覆盖 | 当前覆盖率 | 补全后 | 补全后覆盖率 |
|---|---|---|---|---|---|
| Sunfire | 10（全部项目，含 09-04 增补 user-frontend） | 3 | **30%** | 10 | **100%** |
| Datadog | 9（Datadog 已启用，含 user-frontend） | 5 | **56%** | 9 | **100%** |

#### 告警完整度（标准告警模板填充率）

以各平台标准告警模板为基准：Sunfire 6 类事件 × 每项目、Datadog 6 条 × 每项目。

| 平台 | 标准模板 | 应有总数 | 当前已有 | 当前完整度 | 补全后 | 补全后完整度 |
|---|---|---|---|---|---|---|
| Sunfire | 6 类 × 10 项目 | 60 | 12 | **20%** | 60 | **100%** |
| Datadog | 6 条 × 9 项目 | 54 | 14 | **26%** | 54 | **100%** |
| **合计** | — | **114** | **26** | **23%** | **114** | **100%** |

> Sunfire 当前 12 条明细：search 4/6 + homepage 4/6 + product-editor 4/6（均缺 api_error、script_error）；其余 7 个项目 0/6（含 09-04 增补的 user-frontend）。扩展项目需先确认 SDK 接入。
>
> Datadog 当前 14 条明细：search 6/6 + homepage 5/6 + unified-search 3/6（新规则，旧规则不计入标准模板）+ product-editor 0 + business-insights 0（现有 1 条为特定路由错误，不属于标准 6 类）+ requests 0 + visitors 0 + conversations 0 + user-frontend 0（08-27 已建 3 条 ECS 容器全灭 P1 告警，不属于标准 6 类，不计入）。company-overview 未接入 Datadog，不纳入统计。

#### 逐项目覆盖明细

| 项目 | Sunfire (满分 6) | Datadog (满分 6) | 总分 | 当前完整度 | 补全后 |
|---|---|---|---|---|---|
| search-frontend | 4/6 | 6/6 | 10/12 | 83% | **100%** |
| homepage-frontend | 4/6 | 5/6 | 9/12 | 75% | **100%** |
| product-editor-frontend | 4/6 | 0/6 | 4/12 | 33% | **100%** |
| unified-search-frontend | 0/6 | 3/6 | 3/12 | 25% | **100%** |
| company-overview | 0/6 | — | 0/6 | 0% | **100%** |
| business-insights | 0/6 | 0/6 | 0/12 | 0% | **100%** |
| requests-frontend | 0/6 | 0/6 | 0/12 | 0% | **100%** |
| visitors-frontend | 0/6 | 0/6 | 0/12 | 0% | **100%** |
| conversations-frontend | 0/6 | 0/6 | 0/12 | 0% | **100%** |
| user-frontend（09-04 增补） | 0/6 | 0/6 | 0/12 | 0% | **100%** |

> `—` 表示该平台不适用（未接入 Datadog）。扩展项目 Sunfire 告警依赖 SDK 接入确认。
> user-frontend：Datadog 已有 3 条 ECS 容器全灭 P1 告警（08-27 建），不属于标准 6 类模板故计 0/6，但计入项目级"已覆盖"；Sunfire SDK 落库状态待确认。

### 4.2 告警数量变化

| 平台 | 新建 | 退役/清理 |
|---|---|---|
| Sunfire | **48** | — |
| Datadog | **39** | **8** |
| **合计** | **87** | **8** |

---

## 五、执行优先级

> 阶段划分对齐 FE Epic [FE-1066](https://visable.atlassian.net/browse/FE-1066)：阶段一 = [FE-1067](https://visable.atlassian.net/browse/FE-1067)（9.11 前），阶段二 = [FE-1068](https://visable.atlassian.net/browse/FE-1068)（9.18 前）。2026-09-04 调整：requests / conversations / user-frontend 归入阶段一。

### 阶段一 · 核心项目（9.11 前 → FE-1067）

search-frontend、homepage-frontend、product-editor-frontend、unified-search-frontend、requests-frontend、conversations-frontend、user-frontend 双平台补齐：

- [ ] **D-01 ~ D-06** — product-editor Datadog 6 条全建
- [ ] **S-01 ~ S-06** — search / homepage / product-editor 补 Sunfire api_error + script_error
- [ ] **S-07 ~ S-12** — unified-search Sunfire 全 6 类新建
- [ ] **D-07 ~ D-08** — unified-search Datadog CPU/Memory
- [ ] **D-09** — homepage Datadog SSR 渲染错误
- [ ] **R-01 ~ R-03** — unified-search 旧规则退役
- [ ] **S-25 ~ S-30 + D-18 ~ D-23** — requests-frontend 双平台（前置：SDK 接入确认）
- [ ] **S-37 ~ S-42 + D-30 ~ D-35** — conversations-frontend 双平台（前置：SDK 接入确认）
- [ ] **S-43 ~ S-48 + D-36 ~ D-41** — user-frontend 双平台（前置：SDK 落库 + Datadog 数据面盘点）
- [ ] 核心项目全量验收 / 查漏补缺（9.11）

### 阶段二 · 长尾应用（9.18 前 → FE-1068）

supplier 剩余长尾应用（company-overview、business-insights-frontend、visitors-frontend）：

- [ ] **S-13 ~ S-18** — company-overview Sunfire 全 6 类（未接入 Datadog，跳过 Datadog）
- [ ] **S-19 ~ S-24 + D-12 ~ D-17** — business-insights 双平台
- [ ] **S-31 ~ S-36 + D-24 ~ D-29** — visitors-frontend 双平台
- [ ] 监控方案决策（方案待定：supplier 域维度大盘监控 + 特定场景监控 vs 逐应用告警模板）

### 后续：阈值校准

告警上线后观察 1–2 周，根据实际基线校准阈值：
- `api_error` / `script_error` 的 delta 阈值可能需要按项目流量调整
- 建议 `script_error` 优先使用 wow_delta_5m（同比），避免常态高基线误报
- 为高价值接口单独建 `is_critical` 低阈值告警

---

## 六、阈值策略参考

| event_type | 常态基线量级 | 推荐告警策略 | 理由 |
|---|---|---|---|
| `white_screen` | 极低 | delta_5m > 10–80 | 任何白屏都是严重问题 |
| `ssr_error` | 低 | delta_5m > 10 | SSR 崩溃影响全部用户 |
| `custom_error` | 低–中 | delta_5m > 5–20 | 业务语义明确 |
| `component_error` | 低 | delta_5m > 5–20 | 组件级隔离 |
| `api_error` | **高** | delta_5m > 20–50 | 量大，阈值需校准；可拆 critical 子规则 |
| `script_error` | **最高** | **wow_delta_5m** > 30–100 | 基线波动大，用同比降噪 |
