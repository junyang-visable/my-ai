# FY27 H1 OKR 修订稿 v2（对齐部门 OKR）— Jun Yang (Eric)

> 基准：[FY27 H1 OKR - Yang, Eric](https://visable.atlassian.net/wiki/spaces/~71202075c2285d8115445a8b9dc5244bebf36f)（v1，2026-06-11）
> 部门目标：[OKRs FY2027 - FE Department](https://home.atlassian.com/o/132de72c-a57c-4f54-8d6f-b60a3f8fcf4f/s/6661348b-dad9-44d9-b90d-e6ab64f9f894/goal/VISAB3-118/about)（VISAB3-118，Ran Wang，66.2%；三个 O owner 均为 Bin Xu，2026-09-21 实测）
> v1 → v2 变化：每条 KR 增加**部门 OKR 对齐**行；每个 O 增加对部门目标的贡献摘要；「接下来的规划」按部门缺口认领重排。修订原则与划线留痕同 v1（见 `FY27H1-OKR-修订稿.md`）
> 标记：~~删除线~~ = 取消/移出；`[修订]` = 原文改写；`[新增]` = 本期新增 KR；**交付人 / 主体交付 / 收尾 / 参与者** = 与部门 KR 的关系
> 本文仅为本地审阅稿，未经确认不更新 Confluence 页面

---

## 修订定位（一句话）

个人工作恰好压在部门 OKR 最需要的两个方向上：**部门短板 O2（AI-native 工程基座，31.7%）的 KR1/KR2 由我实际交付；部门收尾期 O3 的 Stability（80%）与 GA4 防线（50% Pending）由我承担主体/收尾**。

---

## O1：【业务增长】构建 AI 驱动的商品管理与内容优化体系，通过 A/B 实验验证策略，提升商家效率与商品质量，支撑商品规模翻倍与质量提升的业务目标

> **对部门目标的贡献**：O1 主体属业务线交付（Product Editor 改版与 AI 采纳率），不直接映射部门技术 O；其数据底座（GA4 迁移）同时是部门 O3-KR2 Defensive Tracking GA4 防线的收尾部分；9 月起扩展承接 supplier 域 Nexus 业务需求（见 KR7）。

### KR1 【修订】数据基建

> KR1：【数据基建】完成商家后台核心页面域的 GA4 埋点迁移与数据层验收，用户行为采集升级到 GA4 口径（Q1 主体完成，2 项收尾中）

* KA1: 约 10 个页面域完成 GA4 迁移与事件补齐（Product Editor、Company Overview / Editor / Creation、User Frontend、Signin-Signup、Top Ranking Products、Product Posting 等）
* KA2: 6 大页面域数据层验收 backlog 全量产出并逐项核验通过；注册登录核心埋点接入 Cypress 自动化校验
* KA3（收尾）: visitors / business-insights 迁移合并发布（Code Review 中，预计 H2 初完成）
* ~~原目标：全链路数据闭环、Badcase 结构化归集、问题治理机制、治理率 > XX%~~ —— 未启动，随 6 月后业务重心调整移出
* ~~数据看板覆盖率 100%~~ —— 无统计口径，移除（H2 先与数据团队定义"覆盖率"分母口径）

**部门对齐**：O3-KR2 Defensive Tracking（VISAB3-150，83.3%）——GA3 防线与 SSOT 同步已由团队达成 100%；**卡在 50% Pending 的正是 GA4 这半块，我是收尾交付人**（迁移 + FE-865 Cypress 校验 + ga4-tracking-validation Skill）。

### KR2 【保留，KA 结果固化】新商转化

> KR2：【新商转化】升级商品管理后台全流程体验，通过 A/B 实验验证（KA 层全部交付；KR 主体指标延后回收）

* KA1 - 商品列表重构（已交付）：前端重构完成；3.13 需求发布，4.2 功能推全；Quick Editor 6.2 推全上线；AB 结果 save action(UV) **+15%**、save counts **+18%**（去年同期 -6.6%）
* KA2 - AI 推荐采纳率（已交付，未达 60% 目标）：AI Keywords **22.61% → 53.60%**（+31.0pp）、AI Category **19.24% → 41.01%**（+21.8pp）；未达标归因：算法侧依赖后端/AI 团队迭代，前端交互与埋点已交付，H2 继续协同
* ~~新商家分阶段引导体系、60 天发品率 41%→70%、操作时长、引导点击率~~ —— 未启动，移至 H2 规划（需产品侧共同承接）

**部门对齐**：不映射（业务线成果，支撑公司业务目标而非部门技术 OKR）。

### KR3 【取消，划线留痕】

~~KR3：【AI 证书识别】…~~ —— 取消原因：业务优先级调整，需求随 CTOOL-368（Certificate Management Migration）标记 Won't Do（2026-05）。

**部门对齐**：无。

### KR4 【维持原划线】

~~KR4：【AI Agent 商品质量优化】…~~（原文已划线，维持不变）

**部门对齐**：无。

### KR5 【修订】HITL 实践落地

> KR5：【HITL 实践】在商品编辑与团队工程场景落地 Human-in-the-Loop 协同模式，关键节点引入用户主动确认机制（Q2 已交付）

* KA1: Quick Editor 人机协同编辑体验上线（AI 建议 + 商家确认，随 6.2 推全）
* KA2: cr-frontend Skill 的 HITL 修复确认机制（FE-788），高风险修复必须经开发者确认
* ~~独立的多策略 A/B 实验基础能力建设~~ —— 未按独立框架立项；实验能力由现有平台承接，本期完成实验桶治理（释放 wlwTestGroup7）

**部门对齐**：O3-KR3 A/B Testing SDK Enhancement（VISAB3-147，85%）—— 参与者（AB 实验清理评估 + 实验桶治理，边缘贡献，汇报不占篇幅）。

### KR6 【修订·收尾态】Accio Work

> KR6:【Accio Work】完成 Accio Work Visable 核心架构建设，交付三个技能的插件形态落地（架构已交付；上线指标未回收）

* 已交付：Visable Assistant（Accio）插件架构、supplier-backend-mcp-service MCP 工具、三技能脚手架、跨用户上下文串用缺陷修复（CTOOL-589）
* ~~技能完成率 ≥70%、写操作成功率 ≥90%~~ —— 指标未回收；后续重心转向 team plugin / marketplace 体系，并入 O2 呈现

**部门对齐**：并入 O2-KR1（AI 基础设施的早期探索部分）。

### KR7 【新增】Supplier 域 Nexus 项目群

> KR7 【新增】：【Supplier 域 Nexus 项目群】以域级集成交付模式承接 Nexus supplier 前端需求，建立可复用的跨仓交付范式（2026-09 启动；H1 里程碑：WhatsApp staging + GTM Phase 1 合入）

* KA1 - 跨仓集成范式：WhatsApp 设置页（CTOOL-634）横跨 5 仓一次打通——routing-lib 路由常量、visable-vue 导航入口、product-editor 设置页、wlw_nginx 边缘路由与 settings BFF 契约、iac 环境域名；routing 22.10.0-beta.1 六仓统一节奏。**5 仓集成需求 4 天到 Ready for QA（09-07 建票 → 09-11，Jira 时戳可查）**；范式直接复用于后续 BV（CTOOL-683）、AI Lead Enrichment（FE-1075）
* KA2 - GTM Phase 1 账号创建（CTOOL-679 Epic）：六应用依赖统一升级（beta.7→beta.8，4/6 验证完成）+ supplier-id 注入 + 403 错误页门控（替代白屏）；提前定位 bv/status 403 为前端 X-Supplier-Id 缺失，消解跨团队阻塞（CTOOL-684/685/686 已完成，8 PR 推进中）
* KA3 - 防御性交付：WA-2530 埋点与需求同步就位（0 事后补埋）；实验桶冲突提前治理
* KA4 - 交付过程工程化：全程走个人 harness 工具链（spec→plan→code→test 门禁 + 全局任务池），CTOOL-679 累计 33+ 轮迭代留痕（my-ai git log 可查），跨仓决策可回溯
* 状态说明：本 KR 于 2026-09 启动，H1 尾以里程碑呈现（WhatsApp staging + GTM 合入），主体交付在 H2（Fill Score / BV / AI Lead Enrichment）

**部门对齐**：业务不映射部门 KR；KA4 仅作为 H2 认领 O2-KR2 Dev Agent（「≥70% 新需求」，现 20%）的流程迁移基础——**当期不作为贡献申报**（尚未使用 dev-agent，如实呈现）。

**EN**: KR7 (new): Nexus supplier-frontend requirements delivered via a domain-level integration pattern — WhatsApp settings page spanning 5 repos in one pass (routing constant, nav entry, settings page, edge routes + BFF contract, IaC env), reaching Ready-for-QA in 4 days; GTM Phase 1 across 6 apps with unified beta pinning, supplier-id injection and 403 gating; tracking (WA-2530) shipped with the feature, zero retrofit. Delivery process itself engineered on the personal harness toolchain (33+ recorded iteration rounds). Started Sep 2026; H1 milestone = WhatsApp staging + GTM merge; main delivery lands in H2.

---

## O2：【效率效能】深化 AI Coding 应用，规范 Supplier 侧技术资产，沉淀可复用的 AI 开发工作流，显著提升个人及团队研发效率

> **对部门目标的贡献**：**本条是部门 O2（AI-native 工程基座，31.7%，部门当前最大短板）的主要推进项**。部门 O2 的量化目标是 H1 需求吞吐 +100% / H2 +300%；其 KR1（AI 基础设施，60%）的 RepoWiki、FE AI Plugin、Skills 计数、人日评估 agent 四个子项我均有直接交付。

### KR1 【修订】资产规范 & AI 渗透

> KR1：【资产规范 & AI 渗透】完成 supplier 侧全部 6 个前端应用的技术资产规范化，达标率 100%（Q2 达成）

* KA1: repoWiki 知识库 6/6 初始化并全量发布（schema v2），另完成 product-editor schema v2 重建——**共 7 仓**
* KA2: Cursor Rules 升级为团队级 Team AI Rules 单一源（.mdc），Cursor / CLAUDE.md 双端同步，marketplace 统一分发
* ~~个人 AI Lines 占比提升至 80%~~ —— 无回收口径，移除（H2 替代：Qoder / Cursor 面板 AI 归因占比，月度记录）

**部门对齐**：**O2-KR1 Frontend AI Infrastructure（VISAB3-153，60%）—— 交付人**。其子目标「RepoWiki 标准定稿+全应用初始化（Q1）」现 90%，我承担供应商域全部 7 仓，无欠账。

### KR2 【超额达成】工具沉淀

> KR2：【工具沉淀】沉淀并落地可复用的 Cursor Skills/Agent 并在团队内推广（Q1 达成；实际交付超出 ≥1 目标）

* KA1: cr-frontend Code Review Skill 搭建完成并推广到全域（Cursor + Qoder 双端 marketplace 安装）
* KA2: 能力持续迭代 4 项：HITL 修复确认、SSR 安全规则（FE-1042）、SEO 评估合并、AB 实验清理评估
* KA3: visable-plugin-marketplace 统一分发仓库建立（含 manage_github 配置与《使用指南》推广）

**部门对齐**：**O2-KR1 · 「FE AI Plugin v1 团队采用（H1）」—— 交付人**；同时计入「≥15 个生产级 AI Skills 覆盖 Intake→Spec→Dev→Deploy→QA」份额（harness 六件套 + jira-lifecycle 全家桶 + cr-frontend + fe-stability-analysis + GA4 校验等）。

### KR3 【超额达成】流程创新

> KR3：【流程创新】输出并落地可复用的 AI 工作流并形成最佳实践（Q2 达成；实际交付 ≥2 个，超出 ≥1 目标）

* KA1: AI 驱动 Code Review 工作流（cr-frontend，团队可用）
* KA2: AI 辅助 PRD 解析工作流（Monitoring Agent 需求链路：PRD → AC → feature_list → commit/PR）
* KA3: 稳定性报告自动化工作流（fe-stability-analysis：每周 1-2 小时人工分析 → 分钟级自动报告）

**部门对齐**：O2-KR1 · Skills/工作流计数 —— 贡献者（多项计入 15-Skills 目标）。

### KR4 【新增】AI 能力管理平台

> KR4 【新增】：【AI 平台建设】交付 AI Management Platform Phase 1，为内部 Skill / MCP 资产提供统一的发现、安装、发布入口（8 月达成）

* 背景：6-8 月最大单项工程产出，原 OKR 未覆盖，补录为正式 KR
* KA1: v-ai-platform 从 0 到 1（React + Vite、企业 SSO、开放市场：发现/详情/收藏/发布/安装/个人中心），12 子任务全部 Done（FE-831）
* KA2: 部署与基础设施（staging + 生产流水线、IaC、独立域名 ai.visable.com，PIT-3398）
* KA3: 过程资产：中英双语 PRD、SSO 技术方案、Nuxt 4 迁移、repoWiki 同步

**部门对齐**：O2-KR1（AI 基础设施的承载平台）—— 交付人；同时是部门「人工 vs AI 人日评估 agent + 效率基准」（50% 子目标）的对口能力底座（legacy-pd-estimator Skill + Codex 古法人日评估 Question Log）。

---

## O3：【稳定性】保障前端全域应用稳定性，完善监控告警与应急响应体系，确保持续零 P0/P1 故障

> **对部门目标的贡献**：部门 O3-KR4 Frontend Stability（VISAB3-151，80%）的**主体交付人**——其 9/30 目标「全核心应用 Stability SDK 集成 + Datadog/Sentry/ODPS/埋点巡检四路数据连通」即我的 O3-KR1/KR2/KR3 交付物；同时作为 **O2-KR2 Monitoring Agent MVP 的交付人**反向支撑部门 O2。

### KR1 【修订·范围扩大】监控全覆盖

> KR1：【监控全覆盖】实现前端全域应用监控 100% 覆盖（原口径：Buyer 侧；2026-08 承接 VEU→VCN 交接后范围扩大至 supplier 域），支持白屏、API 错误、自定义错误与 Web Vitals 实时告警（Q1 Buyer 侧达成；9 月全域收官）

* KA1: Buyer 侧 —— Stability SDK 按 8 站点组合全量推全（ep/de·fr·tr·it·es + wlw/ch·at·de，FE-849~852）；多国站点（pt/dk/pl/nl/uk）监控接入（FE-789）
* KA2: Supplier 侧 —— 6 应用全部补齐 Sentry + 稳定性 SDK + Web Vitals（FE-1028；治理前 5/6 缺稳定性 SDK，治理后全部达 product-editor 基线）
* KA3: 告警体系 —— Sunfire 数据结构适配（FE-764）+ Datadog 统一模板（homepage 5-monitor 标准）批量导入与订阅，两阶段收官（FE-1066/1067/1068 Done）

**部门对齐**：**O3-KR4 Frontend Stability（VISAB3-151，80%）—— 主体交付人**。其描述中「Sentry & Sunfire 100% SDK 覆盖 + Datadog/Sentry/ODPS/埋点巡检数据连通」四路对应我 KA1~KA3 + fe-stability-analysis 的 ODPS 链路。

### KR2 【修订·探索→交付】AI 智能运维

> KR2：【AI 智能运维】交付 Monitoring Agent 线上监控能力，实现多信号源自动采集、自动总结与巡检报告（Phase 1 已交付；v2 覆盖度诊断进行中）

* KA1: Monitoring Agent Phase 1（FE-907，M1-M4 全 Done）：五信号源自动采集（含 AWS 第 5 源）、定时巡检、结构化监控报告
* KA2: fe-stability-analysis Skill（FE-872）：稳定性周报端到端自动化，数据获取从小时级降到分钟级
* KA3（进行中）: v2 监控覆盖度诊断（FE-984）：需求链路解析、失败模式推导、信号匹配器、置信评估模型
* 配套：QA Evaluation Platform 前端（FE-930，6 子任务 Done）

**部门对齐**：**O2-KR2 Harness Agent Orchestration（VISAB3-186，35%）· Monitoring Agent MVP（9/30：e2e 回归、埋点校验、异常检测、auto Jira，≥5 次端到端发布）—— 交付人**。该子目标现 40%，我的 9 月收尾（≥5 次真实发布跑通 + auto Jira 回流）直接把它拉到达成；四份生命周期文档（FE-923/924/925/926）就是其交付物。

### KR3 【修订】误报治理专项

> KR3：【专项治理】主导稳定性 SDK 误报治理专项，消除噪音信号对告警有效性的干扰（Q2 交付；错误总量下降指标延后回收）

* KA1: 页面导航中断 fetch 误报修复（FE-1037）
* KA2: 第三方资源与 API 噪音内置忽略列表；slow check 默认关闭
* KA3: 线上异常调查方法论沉淀（CloudFront 错误激增调查：定位爬虫噪音，非 CDN 故障，产出报告）
* ~~原目标：错误总量下降 XX%~~ —— 口径未定；H2 以 ODPS 稳定性数据环比口径回收（HubSpot 噪音过滤 FE-1019 已立项）

**部门对齐**：O3-KR4 ·「initiate remediation of existing issues」—— 贡献者（误报治理是存量问题治理的前置，保证告警信噪比）。

### KR4 【新增】Supplier 域交接与技术治理

> KR4 【新增】：【组织与治理】完成 supplier 前端域 VEU→VCN 知识转移与技术治理盘点，产出项目整合方案与技术重构立项（8-9 月交付）

* KA1: 知识转移 —— KT Question List、14 项 In-Flight 项目清单、监控告警交接、VEU Handover 页面，交接无断点
* KA2: 治理盘点 —— 改造必要性盘点、BFF vs 同源分析、路由与本地调试工具文档（routes / init.sh）、P0-P2 改造清单
* KA3: 方案产出 —— 6 应用整合为 2-3 个的整合方案（分 4 步）；技术重构 Epic 立项（FE-1062）

**部门对齐**：组织职责（8 月新增），不直接映射部门 KR，但 O3-KR4 的 supplier 域覆盖扩张正是这次交接的结果——没有这次治理盘点，部门 Stability KR 的「all frontend applications」收不了口。

---

## 接下来的规划 / Next Plan（v2：按部门缺口认领排序）

| # | 事项 | 对应部门缺口/目标 | 说明 |
|---|---|---|---|
| 1 | **Monitoring Agent MVP 收尾**：≥5 次真实发布端到端跑通 + auto Jira 回流闭环 | O2-KR2 · Monitoring Agent（40%，9/30 到期） | 我是其交付人，9 月内直接拉到达成 |
| 2 | **Dev Agent 试点与采用**：以 1-2 个 Nexus 需求试点 dev-agent 流程，跑通后逐步全量并留度量 | O2-KR2 · Dev Agent「≥70% 新需求」（20%，部门最拖后腿） | 当前交付走个人 harness 工具链、尚未用 dev-agent——需真实切换试点后才可计入采用率；个人 harness 流程是迁移基础 |
| 3 | **GA4 防线补全**：visitors / business-insights 迁移合并发布 + 防线覆盖业务 KPI | O3-KR2 · GA4（50% Pending） | 收尾交付人 |
| 4 | **Stability 存量治理启动**：buyer 核心场景（HP/CSERP/PSERP/CPP/PDP/RFQ）问题 remediation | O3-KR4（80%） | 主体交付人的最后一段 |
| 5 | **harness orchestrator dashboard**：全局任务池 + Jira 状态流转追踪 | O2-KR1 · dashboard 子目标（40/100，8/15 已过期） | harness-kit 任务池是现成雏形 |
| 6 | **Loop Engineering 立项**：harness 全链路（spec→plan→code→test→commit）自闭环 MVP | O2-KR3（0% 未启动） | H2 个人立项方向，抢占部门空白 |
| 7 | **Nexus 项目群交付**（即 KR7 主体，H2 范围）：Fill Score（CTOOL-678）→ BV（CTOOL-683，10-01 发版）→ AI Lead Enrichment（FE-1075）；H1 尾收 WhatsApp staging + GTM Phase 1 合入 | ——（H2 业务范围） | 按 roadmap 推进 |
| 8 | **Supplier 技术重构**（FE-1062）+ 长线：unified-search / visitors Nuxt 4（FE-740/745）、cr-frontend HITL 2.0（FE-1043/1076/1077） | —— | 依赖整合方案拍板 |

## 一页速览（含部门对齐）

| 位置 | 处理 | 部门对齐 | 一句话 |
|---|---|---|---|
| O1-KR1 | 改写 | O3-KR2 GA4 防线 · **收尾** | GA4 迁移 + 数据层验收；Badcase/治理划线；无口径数字删除 |
| O1-KR2 | 保留 | —— | KA 结果固化；主体指标移 H2 |
| O1-KR3 | 划线取消 | —— | 随 CTOOL-368 Won't Do，留痕 |
| O1-KR4 | 维持划线 | —— | 原样 |
| O1-KR5 | 改写 | O3-KR3 · 参与者 | HITL 落地；独立 AB 框架划线 |
| O1-KR6 | 改写收尾态 | 并入 O2-KR1 | 架构交付写实；上线指标划线 |
| O1-KR7 | **新增** | ——（业务）；KA4 为 H2 Dev Agent 迁移基础 | Nexus 跨仓范式：5 仓 4 天到 QA、埋点随发就位、GTM 六仓统一 |
| O2-KR1 | 改写 | O2-KR1 RepoWiki · **交付人** | 资产规范 100% 写死；AI Lines 删除给替代口径 |
| O2-KR2 | 超额标注 | O2-KR1 FE AI Plugin · **交付人** | 1 skill → 双端分发 + 4 项迭代 + marketplace |
| O2-KR3 | 超额标注 | O2-KR1 Skills 计数 · 贡献者 | ≥1 工作流 → 实际 3 个 |
| O2-KR4 | **新增** | O2-KR1 · **交付人** | AI 管理平台 Phase 1（6-8 月最大单项） |
| O3-KR1 | 范围扩大 | **O3-KR4 Stability · 主体交付人** | Buyer → 全域；双平台；9 月收官 |
| O3-KR2 | 探索→交付 | **O2-KR2 Monitoring Agent · 交付人** | Phase 1 Done + v2 进行中 + QA 平台 |
| O3-KR3 | 改写 | O3-KR4 remediation · 贡献者 | 总量 XX% → 误报治理专项 |
| O3-KR4 | **新增** | 组织职责（O3-KR4 覆盖扩张的前提） | Supplier 交接 + 治理盘点 + 整合方案 |
| Nexus | 不入 H1 | —— | 移「接下来的规划」，作 H2 OKR 雏形 |
