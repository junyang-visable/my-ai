# V-Frontend-Monitor 监控能力清单

> 按 项目 × 错误类型 罗列现有监控与告警触发条件。
> 包含两个平台：Sunfire（Alibaba 内部）和 Sentry（SaaS）。

---

## 一、Sunfire 监控告警

> 数据来源：Sunfire 租户 6（ICBU），文件夹 `V-Frontend-Monitor`

### 能力总览

覆盖 **3 个前端项目**，每个项目监控 **4 类错误**，共 12 项监控 + 12 条告警规则，均为 critical 级别、全部生效。

| 项目代号 | 对应前端项目      |
| -------- | ----------------- |
| Arise    | Homepage Frontend |
| Bamboo   | Product Editor    |
| Dolphin  | Search Frontend   |

### 统一触发逻辑

**告警条件**：某类错误的**总量，最近 5 分钟与过去 5 分钟的差值超过阈值** → 触发 critical 告警。

- 即**环比突增检测**：只有当错误量相比上一个 5 分钟明显突增时才告警；错误量一直平稳（无论高低）不会触发。
- 检测频率：每分钟一次。
- 通知渠道：以钉钉为主（Dolphin 的 SSR 错误为短信）。

### Arise（Homepage Frontend）

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| 白屏 | SPM count (`6_spm_9886`) | 总量（最近 5 分钟与过去 5 分钟差值）> 10 | `app_name = 'homepage-frontend' AND event_type = 'white_screen' AND env = 'production' AND level = 'error'` | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9886?crossTenant=true) |
| SSR 渲染错误 | SPM count (`6_spm_9906`) | 总量（最近 5 分钟与过去 5 分钟差值）> 10 | `app_name = 'homepage-frontend' AND event_type = 'ssr_error' AND env = 'production' AND level = 'error'` | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9906?crossTenant=true) |
| 自定义业务错误 | SPM count (`6_spm_9907`) | 总量（最近 5 分钟与过去 5 分钟差值）> 5 | `app_name = 'homepage-frontend' AND event_type = 'custom_error' AND env = 'production' AND level = 'error'` | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9907?crossTenant=true) |
| 组件渲染错误 | SPM count (`6_spm_9912`) | 总量（最近 5 分钟与过去 5 分钟差值）> 20 | `app_name = 'homepage-frontend' AND event_type = 'component_error' AND env = 'production' AND level = 'error'` | 钉钉（10 分钟内不重复提醒） | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9912?crossTenant=true) |

### Bamboo（Product Editor）

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| 白屏 | SPM count (`6_spm_9902`) | 总量（最近 5 分钟与过去 5 分钟差值）> 10 | `app_name = 'product-editor-frontend' AND event_type = 'white_screen' AND env = 'production' AND level = 'error'` | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9902?crossTenant=true) |
| SSR 渲染错误 | SPM count (`6_spm_9905`) | 总量（最近 5 分钟与过去 5 分钟差值）> 10 | `app_name = 'product-editor-frontend' AND event_type = 'ssr_error' AND env = 'production' AND level = 'error'` | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9905?crossTenant=true) |
| 自定义业务错误（商品更新接口）※ | SPM count (`6_spm_9909`) | 总量（最近 5 分钟与**一周前同期**差值）> 50 | `app_name = 'product-editor-frontend' AND event_type = 'custom_error' AND env = 'production' AND level = 'error'`（eventName 过滤为 update_failed） | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9909?crossTenant=true) |
| 组件渲染错误 | SPM count (`6_spm_9910`) | 总量（最近 5 分钟与过去 5 分钟差值）> 5 | `app_name = 'product-editor-frontend' AND event_type = 'component_error' AND env = 'production' AND level = 'error'` | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9910?crossTenant=true) |

### Dolphin（Search Frontend）

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| 白屏 | SPM count (`6_spm_9903`) | 总量（最近 5 分钟与过去 5 分钟差值）> 80 | `app_name = 'search-frontend' AND event_type = 'white_screen' AND env = 'production' AND level = 'error'` | 钉钉（15 分钟内不重复提醒） | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9903?crossTenant=true) |
| SSR 渲染错误 | SPM count (`6_spm_9904`) | 总量（最近 5 分钟与过去 5 分钟差值）> 10 | `app_name = 'search-frontend' AND event_type = 'ssr_error' AND env = 'production' AND level = 'error'` | **短信** | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9904?crossTenant=true) |
| 自定义业务错误 | SPM count (`6_spm_9908`) | 总量（最近 5 分钟与过去 5 分钟差值）> 20 | `app_name = 'search-frontend' AND event_type = 'custom_error' AND env = 'production' AND level = 'error'` | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9908?crossTenant=true) |
| 组件渲染错误 | SPM count (`6_spm_9911`) | 总量（最近 5 分钟与过去 5 分钟差值）> 5 | `app_name = 'search-frontend' AND event_type = 'component_error' AND env = 'production' AND level = 'error'` | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9911?crossTenant=true) |

### 说明

- **数据链路**：Stability SDK 采集 → POST /web/metrics → `icbu_de.s_tt_v_web_metrics_tt4`（原始采集表）→ ETL → `icbu_de.visable_fe_full_monitoring_data_v1`（ODPS 宽表）→ Sunfire SPM 监控。
- **公共过滤基线**：所有监控项均基于 `env = 'production' AND level = 'error'`，分项目按 `app_name` 字段区分，分类型按 `event_type` 字段区分。
- **分区**：ODPS 表按 `ds`/`hh`（天/小时）分区，分区时区为 GMT+1（原始数据 GMT+8 经 `eu_udf:bi_changetimezone` 转换）。
- ※ **唯一例外**：Bamboo 的「自定义业务错误（商品更新接口）」对比基线是**一周前同期**（同比突增检测），触发逻辑为"最近 5 分钟比一周前同期多出 50 以上才告警"，与其余 11 条的环比口径不同；额外过滤 `eventName = 'update_failed'`。
- 全部监控项为 SPM 类型（租户 6）、处于生效状态；告警规则统一归属应用 `v-search-rec-data-process`。
- 通知渠道以钉钉为主，Dolphin 的 SSR 渲染错误为短信。
- 抑制窗口仅 2 条设置：Dolphin 白屏（15 分钟）、Arise 组件渲染错误（10 分钟），其余使用默认。
- 「查看链接」指向各监控项的 Sunfire 数据页（x.alibaba-inc.com，需内网登录后访问）。

---

## 二、Sentry 监控告警

> 数据来源：Sentry SaaS（us.sentry.io），组织 `visable-gmbh`
> 告警类型为 Issue Alert（基于 issue 优先级触发），非 Metric Alert。

### 能力总览

组织下共 **12 个前端项目**，其中 **6 个项目** 配置了告警规则（共 6 条）；其余 6 个项目暂无告警。

| Sentry 项目                    | Project ID        | 告警规则数 | 状态                |
| ------------------------------ | ----------------- | ---------- | ------------------- |
| search-frontend                | 4508256647184384  | 1          | ✅ 活跃              |
| homepage-frontend              | 4508879109226497  | 1          | ⏸️ 已静默（Snooze）  |
| company-overview               | 4507819492114432  | 1          | ✅ 活跃              |
| ad-center-frontend             | 4508244957593600  | 1          | ✅ 活跃              |
| sales-tool-frontend            | 4509360083501056  | 1          | ✅ 活跃              |
| supplier-onboarding-frontend   | 4506059434950656  | 1          | ✅ 活跃              |
| product-editor-frontend        | 4510321462214656  | 0          | —                   |
| unified-search-frontend        | 1781756           | 0          | —                   |
| business-insights-frontend     | 4511947853398021  | 0          | —                   |
| requests-frontend              | 4511806531829760  | 0          | —                   |
| user-frontend                  | 4511970064728064  | 0          | —                   |
| visitors-frontend              | 4507377901568000  | 0          | —                   |

### 统一触发逻辑

**告警条件**：Sentry 将某个 issue 标记为 **High Priority**（新 issue 或已有 issue 升级为高优先级）→ 触发通知。

- 通知渠道：邮件（发送给 Issue Owners，无 Owner 时回退到 Active Members）。
- 频率控制：同一规则 30 分钟内不重复通知。

### search-frontend

| 监控项                  | 触发条件                                           | 过滤项                                                        | 通知                                       | 查看链接                                                                                                        |
| ----------------------- | -------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 高优先级 Issue 告警     | 新 issue 标记高优 **或** 已有 issue 升级为高优     | 排除 `source=client` 及 `source` 含 `server` 的事件           | 邮件（Issue Owners → Active Members），30 min 不重复 | [查看规则](https://visable-gmbh.sentry.io/alerts/rules/search-frontend/15558042/details/) |

- 状态：✅ 活跃 · 最近触发：2026-08-25 17:23 UTC · 创建时间：2024-11-07

### homepage-frontend

| 监控项                  | 触发条件                                           | 过滤项     | 通知                                       | 查看链接                                                                                                        |
| ----------------------- | -------------------------------------------------- | ---------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 高优先级 Issue 告警     | 新 issue 标记高优 **或** 已有 issue 升级为高优     | 无         | 邮件（Issue Owners → Active Members），30 min 不重复 | [查看规则](https://visable-gmbh.sentry.io/alerts/rules/homepage-frontend/15815255/details/) |

- 状态：⏸️ 已静默（Snooze for everyone） · 从未触发 · 创建时间：2025-02-25

### company-overview

| 监控项                  | 触发条件                                           | 过滤项     | 通知                                       | 查看链接                                                                                                        |
| ----------------------- | -------------------------------------------------- | ---------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 高优先级 Issue 告警     | 新 issue 标记高优 **或** 已有 issue 升级为高优     | 无         | 邮件（Issue Owners → Active Members），30 min 不重复 | [查看规则](https://visable-gmbh.sentry.io/alerts/rules/company-overview/15401031/details/) |

- 状态：✅ 活跃 · 最近触发：2026-08-22 04:25 UTC · 创建时间：2024-08-22

### ad-center-frontend

| 监控项                  | 触发条件                                           | 过滤项     | 通知                                       | 查看链接                                                                                                        |
| ----------------------- | -------------------------------------------------- | ---------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 高优先级 Issue 告警     | 新 issue 标记高优 **或** 已有 issue 升级为高优     | 无         | 邮件（Issue Owners → Active Members），30 min 不重复 | [查看规则](https://visable-gmbh.sentry.io/alerts/rules/ad-center-frontend/15550916/details/) |

- 状态：✅ 活跃 · 最近触发：2026-08-24 11:44 UTC · 创建时间：2024-11-05

### sales-tool-frontend

| 监控项                  | 触发条件                                           | 过滤项     | 通知                                       | 查看链接                                                                                                        |
| ----------------------- | -------------------------------------------------- | ---------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 高优先级 Issue 告警     | 新 issue 标记高优 **或** 已有 issue 升级为高优     | 无         | 邮件（Issue Owners → Active Members），30 min 不重复 | [查看规则](https://visable-gmbh.sentry.io/alerts/rules/sales-tool-frontend/16009398/details/) |

- 状态：✅ 活跃 · 最近触发：2026-08-25 07:51 UTC · 创建时间：2025-05-21

### supplier-onboarding-frontend

| 监控项                            | 触发条件                                                                                        | 过滤项                      | 通知                                             | 查看链接                                                                                                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| 新 Issue / 回归 / 频率告警        | 新 issue 创建 **或** 5 分钟内出现 >1 次 **或** issue 从 resolved 回归 unresolved（满足任一）     | issue 至少发生 3 次          | MS Teams（team.sphinx → Alerts 频道），10 min 不重复 | [查看规则](https://visable-gmbh.sentry.io/alerts/rules/supplier-onboarding-frontend/15142955/details/) |

- 状态：✅ 活跃 · 环境：production · 最近触发：2026-08-26 08:34 UTC · 创建时间：2024-04-25 · Owner：team:sphinx

### 其余项目（无告警规则）

以下项目未配置任何告警规则，Sentry 仍在采集错误数据但不会主动通知：

- product-editor-frontend
- unified-search-frontend
- business-insights-frontend
- requests-frontend
- user-frontend
- visitors-frontend

### 说明

- Sentry 的告警基于 **Issue Priority**（Sentry 内置 AI 优先级分类），与 Sunfire 的"数量突增"逻辑不同。
- `search-frontend` 的过滤条件（filterMatch = none）意味着：只对 `source` 标签既不是 `client` 也不包含 `server` 的事件生效——排除了大部分来源已知的错误，仅保留未标记来源的高优事件。
- `homepage-frontend` 的规则虽然存在但已被 **Snooze**，当前不会发出任何通知。
- Metric Alert Rules 接口返回 410（已废弃），当前组织未使用 Sentry 的指标告警能力。
- 数据查询时间：2026-08-26。

---

## 三、Datadog 监控告警

> 数据来源：Datadog SaaS（app.datadoghq.com），组织 ID 231549
> 告警类型包括 Query Alert（指标阈值）、Log Alert（日志计数阈值）、Trace Analytics Alert 和 Synthetics Alert。

### 能力总览

覆盖 **6 个前端服务** + **1 个前端 BFF 服务** + **Synthetics 页面拨测**，共 **55+ 条**活跃监控规则。

| 分类 | 服务 | 告警规则数 | 团队标签 |
| ---- | ---- | ---------- | -------- |
| 前端 SSR | visable-dev/search-frontend | 6 | team:vcn-frontend |
| 前端 SSR | visable-dev/homepage-frontend | 5 | team:vcn-frontend |
| 前端 SSR | webdevs/unified-search-frontend | 6 | team:vcn-frontend / team:pegasus |
| 前端 SSR | visable-dev/product-editor-frontend | 0 | — |
| 前端 SPA | supplier/onboarding-frontend | 2 | team:pegasus |
| 前端 SPA | business-insights-frontend | 1 | team:pegasus |
| BFF | visable-dev/v-content-generator (CPP/PDP) | 9 | team:arise |
| 拨测 | Synthetics（team:arise SEO 页面） | ~13 (live) | team:arise |
| 拨测 | Synthetics（team:dolphin SERP/产品） | ~20 (live) | team:dolphin |

---

### search-frontend

> 服务：`visable-dev/search-frontend` · 团队：vcn-frontend / dolphin

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| Memory 使用率超限 | `aws.ecs.service.memory_utilization.maximum` | avg(last_5m) > 90%（warn > 80%） | `{service:visable-dev/search-frontend}` | 钉钉 vcn-frontend | [查看](https://app.datadoghq.com/monitors/171637218) |
| CPU 使用率超限 | `aws.ecs.service.cpuutilization.maximum` | avg(last_5m) > 90%（warn > 80%） | `{service:visable-dev/search-frontend}` | 钉钉 vcn-frontend | [查看](https://app.datadoghq.com/monitors/171637260) |
| p75 延迟超限 | `trace.web.request` (p75) | percentile(last_5m) > 1.2s（warn > 1s），恢复 0.6s / 0.4s | `{env:production, service:visable-dev/search-frontend, span.kind:server}` | 钉钉 vcn-frontend | [查看](https://app.datadoghq.com/monitors/233667687) |
| Server Errors 过多 | `trace.web.request.errors` (sum, as_count) | sum(last_5m) by {http.status_code} > 200（warn > 120） | `{env:production, service:visable-dev/search-frontend, span.kind:server}` | 钉钉 vcn-frontend | [查看](https://app.datadoghq.com/monitors/233672283) |
| SSR 渲染错误 | Logs rollup count | last 5m count > 5（warn > 3），恢复 4 / 2 | `service:"visable-dev/search-frontend" env:production @errorType:SSRRenderError` | 钉钉 vcn-frontend | [查看](https://app.datadoghq.com/monitors/266909627) |
| Status:error 日志过多 | Logs rollup count | last 30m count > 400（warn > 300），恢复 80 / 40 | `service:"visable-dev/search-frontend" env:production status:error` | 钉钉 vcn-frontend | [查看](https://app.datadoghq.com/monitors/270496383) |

- 当前状态：p75 延迟 **Alert**（持续超 1.2s），其余 OK。

### homepage-frontend

> 服务：`visable-dev/homepage-frontend` · 团队：vcn-frontend / arise

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| Memory 使用率超限 | `aws.ecs.service.memory_utilization.maximum` | avg(last_5m) > 90%（warn > 80%） | `{service:visable-dev/homepage-frontend}` | 钉钉 vcn-frontend + arise-frontend | [查看](https://app.datadoghq.com/monitors/233667959) |
| CPU 使用率超限 | `aws.ecs.service.cpuutilization.maximum` | avg(last_5m) > 90%（warn > 80%） | `{service:visable-dev/homepage-frontend}` | 钉钉 vcn-frontend + arise-frontend | [查看](https://app.datadoghq.com/monitors/233668208) |
| p75 延迟超限 | `trace.web.request` (p75) | percentile(last_5m) > 1s（warn > 700ms），恢复 600ms / 400ms | `{env:production, service:visable-dev/homepage-frontend, span.kind:server}` | 钉钉 vcn-frontend + arise-frontend | [查看](https://app.datadoghq.com/monitors/233668367) |
| Server Errors 过多 | `trace.web.request.errors` (sum, as_count) | sum(last_5m) by {http.status_code} > 50（warn > 30） | `{env:production, service:visable-dev/homepage-frontend, span.kind:server}` | 钉钉 vcn-frontend + arise-frontend | [查看](https://app.datadoghq.com/monitors/233671589) |
| Status:error 日志过多 | Logs rollup count | last 5m count > 120（warn > 80），恢复 80 / 40 | `service:"visable-dev/homepage-frontend" env:production status:error` | 钉钉 vcn-frontend | [查看](https://app.datadoghq.com/monitors/270555958) |

- 当前状态：全部 OK。

### unified-search-frontend

> 服务：`webdevs/unified-search-frontend` · 团队：vcn-frontend / arise / pegasus

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| Status:error 日志过多 | Logs rollup count | last 5m count > 300（warn > 200） | `service:"webdevs/unified-search-frontend" status:error env:production` | 钉钉 detailpages | [查看](https://app.datadoghq.com/monitors/284274411) |
| p75 延迟超限 | `trace.web.request` (p75) | percentile(last_5m) > 1.2s（warn > 1s） | `{span.kind:server, service:webdevs/unified-search-frontend, env:production}` | 钉钉 detailpages | [查看](https://app.datadoghq.com/monitors/284280863) |
| 5xx 错误过多（新） | Logs rollup count | last 5m count > 12（warn > 8） | `service:"webdevs/unified-search-frontend" stage:production @status:(>=500 <=599) -@url:(*products/null OR *produkte/null)` | 钉钉 detailpages | [查看](https://app.datadoghq.com/monitors/284284046) |
| 全部错误（旧） | Logs rollup count | last 5m count > 0 | `service:"webdevs/unified-search-frontend" stage:production status:error` | 邮件 benjamin.vetter | [查看](https://app.datadoghq.com/monitors/12236842) |
| 5xx 错误（旧） | Logs rollup count | last 5m count > 5（warn > 1） | `service:"webdevs/unified-search-frontend" stage:production @status:(>=500 <=599)` | 邮件 pegasus 团队 | [查看](https://app.datadoghq.com/monitors/62945068) |
| Error 消息（旧） | Logs rollup count | last 5m count > 5（warn > 3） | `service:"webdevs/unified-search-frontend" stage:production ERROR -api.authenticate -"Proxy error"` | 邮件 pegasus 团队 | [查看](https://app.datadoghq.com/monitors/67123179) |

- 当前状态：「全部错误（旧）」**Alert**，「Error 消息（旧）」**Warn**，其余 OK。
- 注：前 3 条为 2026 年新建（team:vcn-frontend），后 3 条为早期遗留规则（team:pegasus）。

### supplier-onboarding-frontend

> 服务：`supplier/onboarding-frontend` · 团队：pegasus

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| Supplier Facts 错误激增 | Trace Analytics (span count) | last 10m count > 5（warn > 2） | `service:supplier/onboarding-frontend env:production status:error @http.host:supplier-facts.internal.wlw-1.production.visable.cloud` | Teams pegasus-alerts | [查看](https://app.datadoghq.com/monitors/301373193) |
| HTTP 错误响应过多 | Trace Analytics (span count) | last 15m count > 20（warn > 10） | `service:supplier/onboarding-frontend env:production @http.status_code:[400 TO 599]` | Teams pegasus-alerts | [查看](https://app.datadoghq.com/monitors/301415375) |

- 当前状态：全部 OK。

### business-insights-frontend

> 服务：`business-insights-frontend` · 团队：pegasus

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| 页面路由错误（Missing supplierId） | Logs rollup count | last 5m count > 50（warn > 40） | `service:business-insights-frontend stage:production message:"[@visable-dev/routing] RoutingError: Missing parameters: supplierId"` | Teams pegasus-alerts | [查看](https://app.datadoghq.com/monitors/301378560) |

- 当前状态：OK。

### product-editor-frontend

> 服务：`visable-dev/product-editor-frontend` · 团队：—

当前未配置任何 Datadog 监控告警规则。

---

### v-content-generator（CPP/PDP，前端 BFF）

> 服务：`visable-dev/v-content-generator` · 团队：arise
> 为 Company Profile Page (CPP) 和 Product Detail Page (PDP) 提供渲染数据。

| 监控项 | 监控指标 | 触发条件 | 过滤项 | 通知 | 查看链接 |
| ------ | -------- | -------- | ------ | ---- | -------- |
| API P95 延迟 | `trace.spring.handler` (p95) | percentile(last_5m) > 1.2s（warn > 650ms），恢复 1s / 500ms | `{service:visable-dev/v-content-generator, env:production, span.kind:server}` by {cluster} | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/287464684) |
| CPU 负载高 | `ecs.fargate.cpu.percent` | max(last_5m) > 40%（warn > 35%），恢复 35% / 30% | `{service:visable-dev/v-content-generator}` by {cluster} | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/287464805) |
| Error 日志 | Logs rollup count | last 5m count > 20 | `stage:production status:error -visitors -DomainUtil -Filter -servlet service:visable-dev/v-content-generator` | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/287464979) |
| Memory 负载高 | `ecs.fargate.mem.usage` | max(last_5m) > 1 GB（warn > 600 MB），恢复 900 MB / 520 MB | `{service:visable-dev/v-content-generator}` by {cluster} | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/287465083) |
| 单资源 P95 > 2s | `trace.servlet.request` (p95) | percentile(last_5m) > 2s（warn > 1.5s） | `{service:visable-dev/v-content-generator, env:production, span.kind:server}` by {resource_name} | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/316500817) |
| 服务无流量（可用性） | `trace.servlet.request.hits` (sum, as_count) | sum(last_5m) < 10 | `{service:visable-dev/v-content-generator, env:production}` | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/316500818) |
| HTTP 错误率 > 5% | `trace.servlet.request.errors` / `trace.servlet.request.hits` | sum(last_5m) ratio > 5%（warn > 3%） | `{env:production, service:visable-dev/v-content-generator}` | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/316500819) |
| 下游依赖失败 | Logs rollup count | last 10m count > 10（warn > 5） | `service:visable-dev/v-content-generator env:production status:error ("RemoteServiceException" OR "timeout" OR "connection refused" OR "Connect timed out")` | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/316500820) |
| 404 Not Found 过多 | Logs rollup count | last 15m count > 50（warn > 30） | `service:visable-dev/v-content-generator env:production ("Product not found" OR "Company can not be found")` | Webhook CPPPDPWebhook | [查看](https://app.datadoghq.com/monitors/316500823) |

- 当前状态：全部 OK。

---

### Synthetics 拨测（team:arise · SEO 页面）

> 类型：Browser Test / API Multi-step · 从 AWS eu-central-1 发起

| 拨测名称 | 类型 | 状态 | 查看链接 |
| -------- | ---- | ---- | -------- |
| WLW-Showroom(de)-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/151979088) |
| EP-showroom(couk)-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/152841007) |
| WLW-CPV(de)-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/152850156) |
| External Link | api-multi | live | [查看](https://app.datadoghq.com/monitors/152851689) |
| EP-CPV(fr)-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/157939317) |
| EP-homepage(co.uk)-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/159025374) |
| EP-CSERP(de)-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/160212839) |
| EP-Best Product-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/161558756) |
| sitemap | api-multi | live | [查看](https://app.datadoghq.com/monitors/160773471) |
| robots.txt | api-multi | live | [查看](https://app.datadoghq.com/monitors/161818511) |
| WLW-homepage(de)-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/168958574) |
| WLW-SEA-Prod | browser | live | [查看](https://app.datadoghq.com/monitors/238288805) |
| Sales Keywords Refresh | browser | live | [查看](https://app.datadoghq.com/monitors/169507594) |

- 通知：由各 Synthetics 规则配置独立通知（多为邮件 + 钉钉）。
- 当前状态：全部 OK。

### Synthetics 拨测（team:dolphin · SERP/产品功能）

> 类型：API Test / Browser Test · 从 AWS eu-central-1 发起
> 主要监控搜索结果页（SERP）的广告位、排名功能、产品推荐接口。

| 拨测名称 | 类型 | 状态 | 查看链接 |
| -------- | ---- | ---- | -------- |
| (wlw) P-SERP TopRanking detect | api | live | [查看](https://app.datadoghq.com/monitors/152937719) |
| SponsoredBrand Detect | api | live | [查看](https://app.datadoghq.com/monitors/164530105) |
| (wlw) P-SERP TopRanking duplicate display | api | live | [查看](https://app.datadoghq.com/monitors/167002655) |
| AI CSERP supplier tag | api | live | [查看](https://app.datadoghq.com/monitors/167422139) |
| (wlw) C-SERP TopRanking detect | api | live | [查看](https://app.datadoghq.com/monitors/168167621) |
| (wlw) P-SERP group Shuffle logic | api | live | [查看](https://app.datadoghq.com/monitors/168175478) |
| [Product] Req-Admin recommend | api | live | [查看](https://app.datadoghq.com/monitors/171318450) |
| RecommendByQuery (HP hub landing) | api | live | [查看](https://app.datadoghq.com/monitors/175233673) |
| TopRanking Preview function | api | live | [查看](https://app.datadoghq.com/monitors/175236401) |
| SponsoredBrands Preview function | api | live | [查看](https://app.datadoghq.com/monitors/175237069) |
| PSERP WLW AI selling point | api | live | [查看](https://app.datadoghq.com/monitors/176120881) |
| [Product] Req-Hub search | api | live | [查看](https://app.datadoghq.com/monitors/189606565) |
| [Product] Rfq-hub recommend for supplier | api | live | [查看](https://app.datadoghq.com/monitors/189615667) |
| (ep) support ukraine api | api | live | [查看](https://app.datadoghq.com/monitors/226818076) |
| Price-range-filter-on-PSERP | api | live | [查看](https://app.datadoghq.com/monitors/229511692) |
| CSERP-WLW-Web-display | browser | live | [查看](https://app.datadoghq.com/monitors/231366268) |
| PSERP-EP-Web-display | browser | live | [查看](https://app.datadoghq.com/monitors/231366735) |
| [Product] Rfq-hub rfq category predication | api | live | [查看](https://app.datadoghq.com/monitors/234180160) |
| [Product] Rfq recommend suppliers | api | paused | [查看](https://app.datadoghq.com/monitors/234182660) |
| C-SERP translation detect | api | live | [查看](https://app.datadoghq.com/monitors/285162526) |

- 通知：钉钉 dolphin-alert + 邮件个人。
- 当前状态：P-SERP group Shuffle logic **Alert**，[Product] Req-Admin recommend **Alert**，其余 OK。

---

### 说明

- 所有告警均基于 **production 环境**数据。
- 通知渠道分布：
  - **钉钉机器人**：`dingtalk-vcn-frontend`、`dingtalk-arise-frontend`、`dingtalk-detailpages`、`dingtalk-dolphin-alert`
  - **MS Teams**：`teams-pegasus-alerts`
  - **Webhook**：`CPPPDPWebhook`（CPP/PDP 专用）
  - **邮件**：遗留规则（pegasus 成员、arise 成员）
- unified-search-frontend 存在新旧两套规则并行：旧规则（2020–2023 年，team:pegasus）阈值极低；新规则（2026 年，team:vcn-frontend）阈值更合理。
- 指标告警（query alert）使用 Datadog Metrics API + APM Traces；日志告警（log alert）使用 Logs Aggregate API；Trace Analytics Alert 基于 APM Span 数据。
- 评估延迟（evaluation delay）：Memory / CPU 类配置了 900s 延迟（等待 AWS CloudWatch 数据上报）。
- CPP/PDP 存在一组重复 monitors（ID 316500911–316500915 与 316500817–316500823 完全相同），可能需要清理。
- **product-editor-frontend 未配置任何 Datadog 告警**，为当前最大监控盲区。
- 数据查询时间：2026-08-26。
