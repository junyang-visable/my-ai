# Nexus 项目 Roadmap

> 状态：持续更新 · 版本 v1.2 · 最后更新 2026-09-04 · 已收录条目：7

## 概览

Nexus 项目 9 月首发需求为 **WhatsApp Integration**：9 月 7 日（周一）进入开发，9 月 22 日（周二）release，全程 16 天。**AI Lead Enrichment** 前端开发 9 月 14 日 ~ 9 月 18 日，联调 9 月 21 日 ~ 25 日，10 月 8 日提测、10 月 15 日 UAT、10 月 20 日发布。**GTM account** 开发暂定 9 月 14 日 ~ 16 日（3 天），预期 10 月 1 日（周四）发布，联调 / 提测 / UAT 节点待排期确认后补入。**BV Process** 前端开发 9 月 21 日 ~ 23 日（3 天），测试 / 发布时间待定。存量修复项目 **fixes for existing** 自 10 月起投入人力，9 月不占用资源。**Synchronize Visable Product Changes to Alibaba** 前端暂不投入资源，排期待定。**Guide Customers to Create Products Optimized for Alibaba** 前端 3 人日，9 月 14 日（周一）启动开发，发布时间待定。其余需求排期待补充，将陆续追加至本文档。

## 时间线总览

```mermaid
%%{init: {"theme":"base","themeVariables":{"cScale0":"#dae8fc","cScale1":"#dae8fc","cScale2":"#dae8fc","cScale3":"#dae8fc","cScale4":"#dae8fc","cScale5":"#dae8fc","cScale6":"#dae8fc","cScale7":"#dae8fc","cScale8":"#dae8fc","cScale9":"#dae8fc","cScale10":"#dae8fc","cScale11":"#dae8fc","cScaleLabel0":"#1565C0","cScaleLabel1":"#1565C0","cScaleLabel2":"#1565C0","cScaleLabel3":"#1565C0","cScaleLabel4":"#1565C0","cScaleLabel5":"#1565C0","cScaleLabel6":"#1565C0","cScaleLabel7":"#1565C0","cScaleLabel8":"#1565C0","cScaleLabel9":"#1565C0","cScaleLabel10":"#1565C0","cScaleLabel11":"#1565C0","taskBkgColor":"#dae8fc","taskBorderColor":"#6c8ebf","taskTextColor":"#1565C0","taskTextDarkColor":"#1565C0","taskTextOutsideColor":"#1565C0","sectionBkgColor":"#ffffff","altSectionBkgColor":"#ffffff","sectionBkgColor0":"#ffffff","sectionBkgColor1":"#ffffff","sectionBkgColor2":"#ffffff","sectionBkgColor3":"#ffffff","sectionBkgColor4":"#ffffff","sectionBkgColor5":"#ffffff","sectionBkgColor6":"#ffffff","sectionBkgColor7":"#ffffff","sectionBkgColor8":"#ffffff","sectionBkgColor9":"#ffffff","sectionBkgColor10":"#ffffff","sectionBkgColor11":"#ffffff","altSectionBkgColor0":"#ffffff","altSectionBkgColor1":"#ffffff","altSectionBkgColor2":"#ffffff","altSectionBkgColor3":"#ffffff","altSectionBkgColor4":"#ffffff","altSectionBkgColor5":"#ffffff","altSectionBkgColor6":"#ffffff","altSectionBkgColor7":"#ffffff","altSectionBkgColor8":"#ffffff","altSectionBkgColor9":"#ffffff","altSectionBkgColor10":"#ffffff","altSectionBkgColor11":"#ffffff"}}}%%
gantt
    title Nexus 排期总览（2026-09 ~ 2026-10 · v1.2）
    dateFormat YYYY-MM-DD
    axisFormat %m-%d
    todayMarker off
    section WhatsApp Integration
    开发    :2026-09-07, 2d
    联调    :2026-09-09, 3d
    提测    :milestone, 2026-09-14, 0d
    UAT     :milestone, 2026-09-17, 0d
    Release :milestone, 2026-09-22, 0d
    section GTM account
    开发    :2026-09-14, 3d
    预期发布 :milestone, 2026-10-01, 0d
    section AI Lead Enrichment
    开发    :2026-09-14, 5d
    联调    :2026-09-21, 5d
    提测    :milestone, 2026-10-08, 0d
    UAT     :milestone, 2026-10-15, 0d
    Release :milestone, 2026-10-20, 0d
    section BV Process
    开发    :2026-09-21, 3d
    section Fixes for existing
    存量修复 :2026-10-01, 31d
    section Guide Customers
    开发    :2026-09-14, 3d
```

读图提示：WhatsApp Integration 的五个节点集中在 9 月 7 日至 22 日；AI Lead Enrichment 开发窗口 9.14 ~ 9.18（与 WhatsApp Integration 提测 / UAT 期重叠），10 月三个节点各隔一周；GTM account 开发暂定 9.14 ~ 9.16，图中仅标出预期 10-01 发布节点；BV Process 开发窗口 9.21 ~ 9.23（3 天，与 AI Lead Enrichment 联调期重叠），测试 / 发布待定；Guide Customers to Create Products Optimized for Alibaba 开发窗口 9.14 ~ 9.16（3 人日，与 GTM account 开发窗口重叠、与 AI Lead Enrichment 开发窗口重叠），测试 / 发布待定；fixes for existing 以 10-01 为示意起点，结束日期待需求范围明确后更新。

## 里程碑一览

| 日期               | 星期        | 条目                 | 节点                        |
| ------------------ | ----------- | -------------------- | --------------------------- |
| 2026-09-07 ~ 09-08 | 周一 ~ 周二 | WhatsApp Integration | 开发                        |
| 2026-09-09 ~ 09-11 | 周三 ~ 周五 | WhatsApp Integration | 联调                        |
| 2026-09-14 ~ 09-18 | 周一 ~ 周五 | AI Lead Enrichment   | 开发                        |
| 2026-09-14 ~ 09-16 | 周一 ~ 周三 | GTM account          | 开发（暂定）                |
| 2026-09-14 ~ 09-16 | 周一 ~ 周三 | Guide Customers to Create Products Optimized for Alibaba | 开发（3 人日）              |
| 2026-09-14         | 周一        | WhatsApp Integration | 提测                        |
| 2026-09-17         | 周四        | WhatsApp Integration | UAT                         |
| 2026-09-21 ~ 09-25 | 周一 ~ 周五 | AI Lead Enrichment   | 联调                        |
| 2026-09-21 ~ 09-23 | 周一 ~ 周三 | BV Process           | 开发                        |
| 2026-09-22         | 周二        | WhatsApp Integration | Release                     |
| 2026-10-01（预期） | 周四        | GTM account          | Release（排期未定，待确认） |
| 2026-10-01 起      | 周四        | Fixes for existing   | 投入开发（起始日待确认）    |
| 2026-10-08         | 周四        | AI Lead Enrichment   | 提测                        |
| 2026-10-15         | 周四        | AI Lead Enrichment   | UAT                         |
| 2026-10-20         | 周二        | AI Lead Enrichment   | Release                     |

## 排期详情

### WhatsApp Integration（首发需求）

| 阶段    | 日期          | 星期        | 说明            |
| ------- | ------------- | ----------- | --------------- |
| 开发    | 09-07 ~ 09-08 | 周一 ~ 周二 | 开发窗口共 2 天 |
| 联调    | 09-09 ~ 09-11 | 周三 ~ 周五 | —               |
| 提测    | 09-14         | 周一        | —               |
| UAT     | 09-17         | 周四        | —               |
| Release | 09-22         | 周二        | —               |

### GTM account（开发暂定，其余待定）

- **排期状态**：开发暂定，联调 / 提测 / UAT 节点均待确认
- **开发**：09-14 ~ 09-16（周一 ~ 周三，3 天，暂定）
- **预期 Release**：2026-10-01（周四）
- **备注**：开发窗口与 AI Lead Enrichment 开发窗口（9.14 ~ 9.18）及 WhatsApp Integration 提测日（9.14）重叠，若为同一批前端人力需注意排布；v0.2 中记录的 9.7 ~ 9.22 排期经确认为 WhatsApp Integration 的排期，已在该条目下更正

### AI Lead Enrichment

| 阶段    | 日期          | 星期        | 说明                      |
| ------- | ------------- | ----------- | ------------------------- |
| 开发    | 09-14 ~ 09-18 | 周一 ~ 周五 | 前端开发窗口共 5 天       |
| 联调    | 09-21 ~ 09-25 | 周一 ~ 周五 | 开发结束后紧接着进入联调  |
| 提测    | 10-08         | 周四        | 联调结束到提测间隔约 2 周 |
| UAT     | 10-15         | 周四        | —                         |
| Release | 10-20         | 周二        | —                         |

备注：开发窗口（9.14 ~ 9.18）与 WhatsApp Integration 的提测（9.14）、UAT（9.17）时间重叠，若为同一批前端人力需注意排布。

### BV Process

| 阶段    | 日期          | 星期        | 说明              |
| ------- | ------------- | ----------- | ----------------- |
| 开发    | 09-21 ~ 09-23 | 周一 ~ 周三 | 前端开发量共 3 天 |
| 提测    | 待定          | —           | —                 |
| Release | 待定          | —           | —                 |

备注：开发窗口（9.21 ~ 9.23）与 AI Lead Enrichment 联调窗口（9.21 ~ 9.25）重叠，且开发第二日（9.22）为 WhatsApp Integration 发布日，若为同一批前端人力需注意排布。

### Fixes for existing（存量修复项目）

- **投入时间**：2026 年 10 月起（10 月份之后投入），9 月不投入资源
- **范围与排期**：待补充
- **备注**：甘特图以 10-01 为示意起点，确切起始日与迭代节奏待确认

### Guide Customers to Create Products Optimized for Alibaba

| 阶段    | 日期          | 星期        | 说明                |
| ------- | ------------- | ----------- | ------------------- |
| 开发    | 09-14 ~ 09-16 | 周一 ~ 周三 | 前端开发量共 3 人日 |
| 提测    | 待定          | —           | —                   |
| Release | 待定          | —           | —                   |

备注：开发窗口（9.14 ~ 9.16）与 GTM account 开发窗口（暂定 9.14 ~ 9.16）完全重叠，并落在 AI Lead Enrichment 开发窗口（9.14 ~ 9.18）内，若为同一批前端人力需注意排布。

### Synchronize Visable Product Changes to Alibaba

- **前端投入**：暂不投入资源
- **排期**：待定（开发 / 联调 / 提测 / UAT / Release 节点均未排期）
- **备注**：确认需求范围与排期后补入本文档及排期图；如后续需要前端投入，将另行评估开发窗口

## 待补充需求

后续需求按下表口径补充（已有信息填入，未定的留空或标注"待定"）：

| 需求       | 开发 | 联调 | 提测 | UAT | Release | 备注 |
| ---------- | ---- | ---- | ---- | --- | ------- | ---- |
| （待补充） |      |      |      |     |         |      |

## 待确认事项

1. **GTM account 排期**：确认联调 / 提测 / UAT 各节点，以及预期 10.1 发布日是否可行（开发暂定 9.14 ~ 9.16）。
2. **BV Process 测试 / 发布时间**：开发窗口已定 9.21 ~ 9.23，测试与发布节点待确认。
3. **fixes for existing 起始时点**：确认确切投入日期（10 月初或更晚）及首个迭代范围。
4. **Synchronize Visable Product Changes to Alibaba 排期**：需求范围与开发 / 联调 / 提测 / UAT / Release 各节点均待确认（当前前端暂不投入资源）。
5. **Guide Customers to Create Products Optimized for Alibaba 测试 / 发布时间**：开发窗口已定 9.14 ~ 9.16（3 人日），测试与发布节点待确认。

## 更新记录

| 版本 | 日期       | 变更                                                                                                                                                                |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v1.2 | 2026-09-04 | 新增 Guide Customers to Create Products Optimized for Alibaba：前端 3 人日，开发 9.14 ~ 9.16，测试 / 发布待定；甘特图 / 里程碑 / 排期图同步更新；md 甘特图任务条配色统一为开发蓝、section 背景带统一为白色并更正图题版本；排期图修正 Sync / Guide 两行行背景绘制层级（原置于周末列之后，盖住周末底色与月分隔线）       |
| v1.1 | 2026-09-04 | 新增 Synchronize Visable Product Changes to Alibaba 条目：前端暂不投入资源，排期待定；排期图同步新增条目行，待确认事项补充 ④                                       |
| v1.0 | 2026-09-01 | BV Process 开发窗口由 10.8 ~ 10.10 提前至 9.21 ~ 9.23（周一 ~ 周三，3 天），与 AI Lead Enrichment 联调期重叠；测试 / 发布仍待定，甘特图 / 里程碑 / 排期图同步更新   |
| v0.9 | 2026-09-01 | 排期图配色改为按阶段统一：开发蓝 / 联调橙 / 提测黄 / UAT 紫 / Release 红（项目归属仍由左侧项目名色块区分）；图例拆分提测与 UAT 项；补 WhatsApp 联调条缺失的阶段文字 |
| v0.8 | 2026-09-01 | GTM account 开发窗口暂定 9.14 ~ 9.16（3 天），预期 10.1 发布不变；排期图同步新增开发条与图例对齐修正                                                                |
| v0.7 | 2026-08-31 | AI Lead Enrichment 新增联调节点 9.21 ~ 9.25（5 天）；排期图新增联调行，下游条目整体下移                                                                             |
| v0.6 | 2026-08-31 | WhatsApp Integration 联调扩展为 9.9 ~ 9.11（3 天），原 9.9 ~ 9.10 空档取消，待确认事项同步删减                                                                      |
| v0.5 | 2026-08-31 | BV Process 更正为前端需投入：开发 10.8 ~ 10.10（3 天），测试 / 发布待定；甘特图 / 里程碑 / 排期图同步更新                                                           |
| v0.4 | 2026-08-31 | 新增 AI Lead Enrichment 排期（开发 9.14 ~ 9.18、提测 10.8、UAT 10.15、发布 10.20）；新增 BV Process（前端预计不投入，待确认）                                       |
| v0.3 | 2026-08-31 | 更正条目归属：v0.2 中 GTM account 的 9.7 ~ 9.22 排期实际为 WhatsApp Integration 的排期；GTM account 排期未定，预期 10.1 发布                                        |
| v0.2 | 2026-08-27 | 提测日由 9.13（周日）调整为 9.14（周一）；移除 QA 修复窗口、发布准备等推断性排期内容                                                                                |
| v0.1 | 2026-08-26 | 初始创建：GTM account 完整排期；fixes for existing 投入时间                                                                                                         |
