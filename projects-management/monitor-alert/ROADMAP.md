# 监控告警补齐排期（Monitor-Alert Roadmap）

> 状态：持续更新 · 版本 v1.1 · 最后更新 2026-09-02 · 周期 2026-09-02 ~ 2026-09-18 · 已收录条目：12（10 个任务条 + 2 个里程碑）
>
> 范围数据源：[监控告警补全计划](../../knowledge-base/monitoring-alert-补全计划.md)（Sunfire 新建 42 条 + Datadog 新建 33 条 + 清理 8 条）。本文档为排期 source of truth，[ROADMAP.drawio](./ROADMAP.drawio) 为可视化衍生，两处同步修改。

## 概览

从 9.2（周三）到 9.11（下周五）完成核心 6 项目 —— search-frontend、homepage-frontend、requests-frontend、conversations-frontend、unified-search-frontend、product-editor-frontend —— 的 **Sunfire + Datadog 双平台监控补齐**；随后 9.14 ~ 9.18 完成其余长尾应用（company-overview、business-insights、visitors-frontend）的监控覆盖，**9.18（周五）全部收口**。

阶段划分：

- **阶段一 · 核心项目监控补齐（09-02 ~ 09-11，8 个工作日）**：6 个项目逐个补齐，每项约 2 天（首个项目顺带固化告警模板与阈值基线），9.11 当天做全量验收与查漏补缺。工作量按补全计划条目映射：轻则 search-frontend 仅补 2 条 Sunfire，重则 product-editor / requests / conversations 双平台全套 8~12 条。
- **阶段二 · 长尾应用监控覆盖（09-14 ~ 09-18，5 个工作日）**：company-overview（仅 Sunfire，Datadog 未接入跳过）、business-insights、visitors-frontend 各约 2 天；9.18 为缓冲收口日（含 v-content-generator 重复规则清理）。

## 时间线总览

```mermaid
gantt
    title 监控告警补齐排期（2026-09 · v1.1）
    dateFormat YYYY-MM-DD
    axisFormat %m-%d
    todayMarker off
    section 阶段一 · 核心项目
    search-frontend          :2026-09-02, 2d
    homepage-frontend        :2026-09-03, 2d
    product-editor-frontend  :2026-09-04, 4d
    unified-search-frontend  :2026-09-07, 2d
    requests-frontend        :2026-09-08, 2d
    conversations-frontend   :2026-09-09, 2d
    核心验收 / 查漏           :2026-09-10, 2d
    里程碑 核心补齐完成       :milestone, 2026-09-11, 0d
    section 阶段二 · 长尾应用
    company-overview         :2026-09-14, 2d
    business-insights        :2026-09-15, 2d
    visitors-frontend        :2026-09-16, 2d
    里程碑 长尾覆盖完成       :milestone, 2026-09-18, 0d
```

读图提示：相邻任务条重叠 1 天表示当天交接（如 search 9.3 收尾时 homepage 同日切入）；product-editor 条跨 9.5 ~ 9.6 周末，实际工作日为 9.4（周五）+ 9.7（周一）2 天；9.11 验收完成后阶段二从 9.14（周一）启动。drawio 图示时间轴为 **08-26 ~ 09-25**：按默认缓冲规则在排期前后各多展示一周空白（轴起 = min(今天, 最早任务)−7 天，轴止 = 最晚任务+7 天），供后续追加任务（如阈值校准）使用。

## 里程碑一览

| 日期       | 星期 | 里程碑                 | 说明                                   |
| ---------- | ---- | ---------------------- | -------------------------------------- |
| 2026-09-11 | 周五 | 核心项目监控补齐完成   | 6 个核心项目 Sunfire + Datadog 全部到位 |
| 2026-09-18 | 周五 | 长尾应用监控覆盖完成   | 其余长尾应用全部覆盖，整体收口          |

## 排期详情

### 阶段一 · 核心项目监控补齐（09-02 ~ 09-11）

| 日期             | 星期          | 条目                   | 工作内容（对应补全计划条目）                                                              |
| ---------------- | ------------- | ---------------------- | ----------------------------------------------------------------------------------------- |
| 09-02 ~ 09-03    | 周三 ~ 周四   | search-frontend       | Sunfire 补 api_error / script_error 告警（S-01 ~ S-02）；首个项目顺带固化告警模板与阈值基线；Datadog 已 6/6 仅核验 |
| 09-03 ~ 09-04    | 周四 ~ 周五   | homepage-frontend     | Sunfire S-03 ~ S-04；Datadog 补 SSR 渲染错误（D-09）                                        |
| 09-04 ~ 09-07    | 周五 ~ 周一   | product-editor-frontend | Datadog 全套新建（D-01 ~ D-06）；Sunfire S-05 ~ S-06。跨周末，实际 2 个工作日              |
| 09-07 ~ 09-08    | 周一 ~ 周二   | unified-search-frontend | Sunfire 全 6 类新建（S-07 ~ S-12）；Datadog 补 CPU / Memory（D-07 ~ D-08）；旧规则退役（R-01 ~ R-03） |
| 09-08 ~ 09-09    | 周二 ~ 周三   | requests-frontend     | 前置：Stability SDK 接入状态确认；Sunfire S-25 ~ S-30；Datadog 全套（D-18 ~ D-23）         |
| 09-09 ~ 09-10    | 周三 ~ 周四   | conversations-frontend | 前置：Stability SDK 接入状态确认；Sunfire S-37 ~ S-42；Datadog 全套（D-30 ~ D-35）         |
| 09-10 ~ 09-11    | 周四 ~ 周五   | 核心验收 / 查漏        | 6 项目双平台全量核验、阈值抽查、查漏补缺；**9.11 里程碑：核心项目监控补齐完成**              |

### 阶段二 · 长尾应用监控覆盖（09-14 ~ 09-18）

| 日期          | 星期        | 条目                | 工作内容（对应补全计划条目）                                                                |
| ------------- | ----------- | ------------------- | ------------------------------------------------------------------------------------------- |
| 09-14 ~ 09-15  | 周一 ~ 周二 | company-overview    | 前置：SDK 接入状态确认，未接入先接入；Sunfire S-13 ~ S-18。Datadog 未接入，跳过（D-10 ~ D-11 已划掉） |
| 09-15 ~ 09-16  | 周二 ~ 周三 | business-insights   | Sunfire S-19 ~ S-24；Datadog D-12 ~ D-17（通知走 Teams pegasus-alerts）                     |
| 09-16 ~ 09-17  | 周三 ~ 周四 | visitors-frontend   | Sunfire S-31 ~ S-36；Datadog D-24 ~ D-29                                                    |
| 09-18          | 周五        | 缓冲 / 收口          | v-content-generator 重复规则清理（R-04）、整体收尾核验；**里程碑：长尾应用监控覆盖完成**      |

## 待确认事项

1. **扩展项目 SDK 接入状态待盘点**：requests / conversations / company-overview / business-insights / visitors 五个应用的 Stability SDK 接入情况未确认——未接入的需先完成接入（参照补全计划 §3.1.3 前提），会放大阶段一末两项与整个阶段二的工作量。
2. **阈值校准不在本排期内**：告警上线后观察 1~2 周再按实际基线校准（api_error / script_error 按项目流量调整），预计 9 月底进行。
3. **9.18 deadline 风险**：若 SDK 接入工作量超预期，长尾应用覆盖存在延期风险，届时优先保证 Sunfire 告警落地、Datadog 顺延。

## 更新记录

| 版本 | 日期       | 变更                                                                                     |
| ---- | ---------- | ---------------------------------------------------------------------------------------- |
| v1.0 | 2026-09-02 | 初版：核心 6 项目 9.11 前双平台补齐 + 长尾 3 应用 9.18 前覆盖，共 12 条目、2 个里程碑。 |
| v1.1 | 2026-09-02 | drawio 时间轴扩展为 08-26 ~ 09-25（排期前后各留一周缓冲，规则沉淀入 drawio-roadmap 技能）；排期条目与日期不变。 |
