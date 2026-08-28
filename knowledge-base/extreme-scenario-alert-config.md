# 极端场景告警配置清单（Sunfire + Datadog）

> 数据查询时间：2026-08-28。校准数据：ODPS `icbu_de.visable_fe_full_monitoring_data_v1` 近 30 天（20260729–20260827）；Datadog 实测基线（2026-08-27~28）。范围：不含 Sentry。
>
> 目标：配置"触发即故障"的极端场景告警——只使用与正常业务波动正交的信号，上线前用历史数据校准，保证非故障日零触发。

## 一句话结论

基于 30 天校准数据，需要在 Sunfire 新增 12 条绝对量阈值规则（替换现有环比逻辑的盲点）、在 Datadog 为 9 个服务补齐无流量/容器全灭/5xx 饱和/延迟灾难四类极端规则（现有已发布的同类规则为 0 条），并同步补齐 5 个服务的常规告警盲区。

## 1. 为什么现有告警覆盖不了极端场景

**Sunfire 现有 12 条规则全部是 `delta_5m` 环比突增逻辑**（最近 5 分钟与过去 5 分钟的差值超阈值）。环比有两个系统性盲点：

- 持续高位平台期：差值趋零，不再触发（事故进行时反而静默）
- 缓慢爬升：差值始终小于阈值，永不触发

**Datadog 现有规则是质量线而非故障线**：p75 1~1.2s、错误数 50~400 条/5m 等。这些阈值正常业务波动也可能触及，触发不等于故障。极端规则需要换用与流量无关的信号：无流量、容器计数、比率饱和、绝对量。

验证发现的事实（2026-08-28 实测）：

| 事实 | 数据 | 含义 |
|---|---|---|
| v-content-generator 无流量告警 316500818 是 **draft 状态未发布** | `draftStatus: "draft"` | 全组实际已发布的无流量告警为 0 条 |
| 两条 unified-search legacy email 告警当前正处 **Alert** 状态 | 12236842 / 67123179 | 收件人已非值班人，告警在响无人处理 |
| search p75 延迟告警 233667687 当前处于 **Alert** | 查询实际值为 1.2s 阈值边缘 | 现有质量线阈值贴近业务常态，正在产生噪声 |
| 08-27 同事已给 user-frontend 建 3 条 P1 告警 | 317035916 / 317035974 / 317048648 | ECS running<1 模式团队已开始用，值得标准化推广 |

## 2. Sunfire 极端规则（12 条新增）

### 2.1 校准数据（30 天，5 分钟窗口，生产 error 级）

| 项目 | 事件类型 | 非零窗口数 | 均值 | p99 | p99.9 | 30天最大 | 建议绝对量阈值 |
|---|---|---|---|---|---|---|---|
| search | white_screen | 4660 | 3.8 | 40 | 101 | **123** | **80** |
| search | ssr_error | 3 | 1.3 | 2 | 2 | 2 | **10** |
| search | custom_error | 780 | 1.2 | 3 | 4 | 4 | **20** |
| homepage | white_screen | 1998 | 1.5 | 6 | 16 | 17 | **30** |
| homepage | ssr_error | 56 | 1.4 | 8 | 8 | 8 | **15** |
| homepage | custom_error | 173 | 1.0 | 2 | 2 | 2 | **15** |
| homepage | component_error | 84 | 2.9 | 41 | 41 | 41 | **60** |
| product-editor | white_screen | 365 | 1.4 | 5 | 8 | 8 | **15** |
| product-editor | ssr_error | 51 | 1.1 | 6 | 6 | 6 | **10** |
| product-editor | custom_error | 104 | 2.7 | 22 | 35 | 35 | **50** |
| product-editor | component_error | 3 | 1.0 | 1 | 1 | 1 | **5** |

（search component_error 无行 = 30 天内该维度无生产 error 数据，说明 Sunfire 监控项 9911 存在但该事件在生产长期为零。若要配规则，参考 homepage 阈值取 60。）

尖峰日期核对（确认阈值不在事故日基线内被"吃掉"）：

- search white_screen 最大 5 个窗口全部落在 **2026-08-07 08:00–08:30**（123/117/114/108/101），为一次真实事故；08-25 的 Sentry 回归事故主要走日志通道（Datadog 侧 search 日志当天 39,642 条，为正常日 ~1,100 条的 35 倍）
- homepage component_error 三个独立尖峰：08-22 22:15（41）、08-13 01:20（32）、08-03 03:35（30）——阈值 60 高于全部历史尖峰，事故日不会误报
- product-editor custom_error 尖峰在 08-10 10:00–10:05（35/22）——阈值 50 高于历史最大

### 2.2 配置规格

每条规则 = 绝对量阈值 + 连续触发确认 + 分级通知：

| 配置项 | 值 | 理由 |
|---|---|---|
| 阈值 | 上表"建议绝对量阈值"列 | 全部高于 30 天历史最大值（≥1.5× p99.9 或 ≥1.4× max），非故障日零触发 |
| 触发确认 | 连续 2 个 1m 检查周期超限 | 消除单窗口毛刺；等效持续 ≥1 分钟 |
| 通知 | **短信/电话**（sunfire sms 通道） | 极端规则走独立通道，与存量钉钉环比规则区分 |
| 通知文案 | 含当前值、阈值、30 天 p99 对比值 | 值班人能立刻判断量级 |

依据 `skills/coverage-diagnosis/config/alert_capabilities.yaml`：Sunfire 监控项挂在 tenant 6，三个项目各有 white_screen / ssr_error / custom_error / component_error 四个监控项 id 可复用（search 9886/9906/9907/9912，homepage 9902/9905/9909/9910，product-editor 9903/9904/9908/9911——见 yaml）。**新增绝对量规则时新建监控项，不改动存量环比规则**，两套并行。

## 3. Datadog 极端规则（E1–E4 × 9 服务）

### 3.1 流量基线实测（决定 E1 阈值分档）

| 服务 | 日志量/天 | 深夜(UTC 01-02时)/小时 | 流量形态 |
|---|---|---|---|
| unified-search-frontend | 6,905,106 | 255,805 | 高流量，日夜持续 |
| homepage-frontend | 1,254,825 | 30,302 | 高流量 |
| search-frontend | 1,108（正常日） | 42 | **低流量**（流量已迁移至 unified-search） |
| requests-frontend | 5,325 | 70 | 中低流量 |
| business-insights-frontend | 263 | ~0（深夜无数据） | **B2B 低流量** |
| conversations-frontend | 210 | 2 | **B2B 低流量** |
| visitors-frontend | 29 | ~0 | **B2B 低流量** |
| product-editor-frontend | 95 | 8 | **B2B 低流量** |
| v-content-generator | 0（7 天查无日志） | 0 | 日志未接入，只有 trace 指标 |

5xx 基线：homepage 全天 **0 条** 5xx 日志（任何持续 5xx 都是真异常）；unified-search 55 条/天。

### 3.2 四类极端规则模板

**E1 无流量**（log 或 trace hits，按流量档取阈值）：

| 档位 | 适用服务 | 查询（示例 service 替换） | 阈值 |
|---|---|---|---|
| 高流量档 | unified-search, homepage | `logs("service:webdevs/unified-search-frontend env:production").rollup("count").last("5m")` | < 100 |
| 低流量档 | search, requests | 同上 | < 5 |
| B2B 档（只能用 trace，无日志） | product-editor, visitors, conversations, business-insights, v-content-generator | `sum(last_5m):sum:trace.servlet.request.hits{service:...,env:production}.as_count()` | < 1 |
| 复刻参照 | — | v-content-generator 316500818 的查询（未发布，可参考） | — |

高流量档配 `notifyNoData: false` + `onMissingData: default`；B2B 档建议 `notify_no_data` 10 分钟。注意 search-frontend 日志量含正常日 1.1k，深夜 42/小时——5 分钟窗口 <5 已贴近但低于深夜基线，可上线后观察一周再收。

**E2 5xx 饱和**（比率而非绝对数）：

```
sum(last_5m): (sum:trace.web.request.errors{env:production,service:X,http.status_code:5xx}.as_count() /
 sum:trace.web.request.hits{env:production,service:X}.as_count()) * 100 > 30
```

触发条件：5xx 比例 > 30% 持续 5m。homepage 基线为 0，unified-search 现有 5xx 绝对数告警（284284046，阈值 12/5m）保留作 warn 档。

**E3 延迟灾难**：`percentile(last_10m):p95:trace.web.request{env:production,service:X,span.kind:server} > 5s` 持续 2 个周期。现有 p75 1~1.2s 规则是质量线保留不动。

**E4 容器全灭**（标准化 08-27 user-frontend 已建模式）：

```
avg(last_5m):avg:aws.ecs.service.running{env:production, servicename:<ecs-service-name>} < 1
```

参照 317035916（user-frontend，P1，08-27 由 zhenyu.liu 创建），`onMissingData: show_and_notify_no_data`。**前置动作：需要先在 Datadog AWS 集成里确认每个服务的 `servicename` tag 实际值**（user-frontend 的是 `visable-dev_user-frontend_v2_web_internal` 格式）。

### 3.3 落地范围与优先级

| 批次 | 内容 | 条数 |
|---|---|---|
| 第一批（本周） | E1 + E4 × search / homepage / unified-search / v-content-generator | 8 条 |
| 第二批 | E2 + E3 × 同上 4 服务 | 8 条 |
| 第三批 | E1–E4 × 其余 5 服务（product-editor / visitors / conversations / business-insights / requests）+ v-content-generator 补 CPU/Mem | ~21 条 |

第一批上线后观察 1 周再推广，重点确认低流量档阈值不夜间误报。

## 4. 常规盲区补齐（非极端规则，按优先级）

| # | 项目 | 现状 | 待补 |
|---|---|---|---|
| 1 | product-editor-frontend | Datadog **0 条**（最大盲区） | CPU / Memory / p75 / Server Errors / error logs 五件套 |
| 2 | business-insights-frontend | 仅 1 条路由错误 | 5xx、p95、CPU/Mem |
| 3 | unified-search-frontend | 有 5xx/p75/error logs | CPU、Memory |
| 4 | homepage-frontend | 有 5 项 | SSR 渲染错误 log 告警（照抄 search 266909627，filter 换 service） |
| 5 | visitors / requests / conversations | 0 条 | error logs + 5xx + p75 各一 |

## 5. 治理项（顺手修，含已确认的告警债）

| # | 动作 | 对象 | 理由 |
|---|---|---|---|
| G1 | **停用** | unified-search legacy email 告警 12236842 / 62945068 / 67123179 | 收件人（benjamin.vetter / pegasus）已非值班人，两条正处 Alert 无人处理；与新规则重复 |
| G2 | **发布** | v-content-generator 316500818（无流量，draft） | 唯一无流量规则卡在草稿 |
| G3 | **复核** | search p75 233667687（当前 Alert 中） | 阈值 1.2s 贴近业务常态产生噪声，考虑阈值上移或改 warn |
| G4 | **发布** | v-content-generator 其余 8 条 monitor 若同为 draft 需逐条确认 | 08-25 批量创建，状态未验证 |
| G5 | 建议新增 | "Stability ETL 数据断流"元监控 | 监控管道自身故障也要可见（曾有 pyodps 静默吞错教训） |

## 6. 落地顺序与验证

1. **第 1 周**：G1/G2/G3 治理项 + E1/E4 第一批 8 条。上线后逐日核对告警事件与实际故障记录，目标非故障日零触发
2. **第 2 周**：Sunfire 12 条绝对量规则（阈值已校准，可直接配置）
3. **第 3-4 周**：E2/E3 及第三批铺开 + 常规盲区补齐
4. **持续**：每季度重跑校准 SQL（本文档 §2.1 的查询，替换日期区间），阈值随业务增长重新校准

验证口径：每条极端规则上线时，用 30 天历史数据回放一遍确认触发次数 = 历史真实事故次数（预期：search white_screen @80 触发 1 次 = 08-07 事故；homepage component_error @60 触发 0 次；其余均为 0）。

## 附：数据来源与口径

- Sunfire 校准：ODPS 表 `icbu_de.visable_fe_full_monitoring_data_v1`，`env='production' AND level='error'`，分区 ds 20260729–20260827，按 `create_time` 分钟位做 5 分钟分桶（分区 hh 为 GMT+1、create_time 为 GMT+8，小时错位不影响分钟分桶内聚）
- Datadog 基线：Logs Aggregate API（2026-08-27 全天 + 08-28 UTC 01-02 时深夜档），Monitor API（org 231549，2026-08-28 拉取）
- 存量告警清单：`skills/coverage-diagnosis/config/alert_capabilities.yaml`（2026-08-26 快照）+ 2026-08-28 Monitor API 实测核对
- search-frontend 08-25 事故日志量 39,642 vs 正常日 ~1,100：Datadog 日志通道实测，用于说明日志量告警需区分事故日
