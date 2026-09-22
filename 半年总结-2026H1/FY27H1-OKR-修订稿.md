# FY27 H1 OKR 修订稿（审阅版）— Jun Yang (Eric)

> 基准：[FY27 H1 OKR - Yang, Eric](https://visable.atlassian.net/wiki/spaces/~71202075c2285d8115445a8b9dc5244bebf36f/pages/199065617)（v1，2026-06-11）· 修订原则：达标的写实写死；未启动的划线并注明移出原因；无口径的数字删除并给替代方案；范围演进显性标注；不做静默删除
> 标记说明：~~删除线~~ = 取消/移出；`[修订]` = 原文改写；`[新增]` = 本期新增 KR；「原口径 → 新口径」= 范围演进
> 本文仅为本地审阅稿，未经确认不更新 Confluence 页面

---

## O1：【业务增长】构建 AI 驱动的商品管理与内容优化体系，通过 A/B 实验验证策略，提升商家效率与商品质量，支撑商品规模翻倍与质量提升的业务目标

（O 描述不变）

### KR1 【修订】数据基建

> KR1：【数据基建】完成商家后台核心页面域的 GA4 埋点迁移与数据层验收，用户行为采集升级到 GA4 口径（Q1 主体完成，2 项收尾中）

* KA1: 约 10 个页面域完成 GA4 迁移与事件补齐（Product Editor、Company Overview / Editor / Creation、User Frontend、Signin-Signup、Top Ranking Products、Product Posting 等）
* KA2: 6 大页面域数据层验收 backlog 全量产出并逐项核验通过；注册登录核心埋点接入 Cypress 自动化校验
* KA3（收尾）: visitors / business-insights 迁移合并发布（Code Review 中，预计 H2 初完成）
* ~~原目标：全链路数据闭环、Badcase 结构化归集、问题治理机制、治理率 > XX%~~ —— 未启动，随 6 月后业务重心调整移出
* ~~数据看板覆盖率 100%~~ —— 无统计口径，移除（如需保留，H2 先与数据团队定义"覆盖率"的分母口径）

**EN**: KR1 (Data Infrastructure): Complete GA4 tracking migration and data-layer acceptance for core merchant-backend page domains (~10 domains), upgrading behavior collection to the GA4 standard. Main body delivered in Q1; visitors / business-insights in final code review. ~~Original scope: full closed-loop data system, structured Badcase aggregation, issue governance rate~~ — not started, moved out with the business priority shift after June.

### KR2 【保留，KA 结果固化】新商转化

> KR2：【新商转化】升级商品管理后台全流程体验，通过 A/B 实验验证（KA 层全部交付；KR 主体指标延后回收）

* KA1 - 商品列表重构（已交付）：
    * 完成前端重构，配合后端优化；3.13 需求发布，4.2 功能推全；Quick Editor 6.2 推全上线
    * AB 结果：save action(UV) **+15%**，save counts **+18%**（去年同期 -6.6%）；推全后长期结果待数据回收
* KA2 - AI 推荐采纳率（已交付，未达 60% 目标）：
    * AI Keywords 采纳率：**22.61% → 53.60%**（+31.0pp）
    * AI Category 采纳率：**19.24% → 41.01%**（+21.8pp）
    * 未达标归因：推荐算法侧依赖后端/AI 团队迭代，前端交互与埋点侧已交付；H2 继续协同推进
* ~~新商家分阶段引导体系、60 天发品率 41%→70%、操作时长、引导点击率~~ —— 未启动，移至 H2 规划（需产品侧共同承接）

**EN**: KR2 (New Merchant Conversion): Upgrade the product management backend experience, validated via A/B testing. KA1 Product List refactor + Quick Editor delivered (save UV +15%, save counts +18% vs -6.6% last year); KA2 AI adoption improved (Keywords 22.61%→53.60%, Category 19.24%→41.01%, below the 60% target — frontend interaction and tracking delivered; algorithm iteration continues with the AI team). ~~Phased onboarding guidance system and 60-day publishing-rate metrics~~ — moved to H2 with product counterpart.

### KR3 【取消，划线留痕】

~~KR3：【AI 证书识别】建设 Certificate 智能管理功能，探索 AI 自动识别与信息提取，实现证书上传流程完成率 >XX%，AI 自动填充准确率 >XX%（Q2）~~

* 取消原因：业务优先级调整，需求随 CTOOL-368（Certificate Management Migration）标记 Won't Do（2026-05）。与 KR4 同款处理，保留取消记录。

### KR4 【维持原划线】

~~KR4：【AI Agent 商品质量优化】…~~（原文已划线，维持不变）

### KR5 【修订】AI Agent & AB 平台 → HITL 实践落地

> KR5：【HITL 实践】在商品编辑与团队工程场景落地 Human-in-the-Loop 协同模式，关键节点引入用户主动确认机制（Q2 已交付）

* KA1: Quick Editor 人机协同编辑体验上线（AI 建议 + 商家确认，随 6.2 推全）
* KA2: cr-frontend Skill 的 HITL 修复确认机制（FE-788），高风险修复必须经开发者确认
* ~~原目标：独立的多策略 A/B 实验基础能力建设（实验框架功能完成度 100%）~~ —— 未按独立框架立项；实验能力由现有平台承接，本期仅完成实验桶治理（释放 wlwTestGroup7）

**EN**: KR5 (HITL Practice): Land Human-in-the-Loop collaboration in product editing and team engineering — Quick Editor AI-suggestion + merchant confirmation shipped with the June rollout; cr-frontend HITL fix confirmation implemented. ~~Standalone multi-strategy A/B experiment framework~~ — not pursued as a standalone project; experiments carried by the existing platform, with experiment-bucket governance done this period.

### KR6 【修订·收尾态】Accio Work

> KR6:【Accio Work】完成 Accio Work Visable 核心架构建设，交付三个技能（Performance Insights、Company Profile Optimization、Product Optimization）的插件形态落地（架构已交付；上线指标未回收）

* 已交付：Visable Assistant（Accio）插件架构（v-agent-hub-bamboo）、supplier-backend-mcp-service MCP 工具、三技能脚手架、跨用户上下文串用缺陷修复（CTOOL-589）
* ~~技能完成率 ≥70%、写操作成功率 ≥90%~~ —— 指标未回收；后续重心已转向 team plugin / marketplace 体系，该方向并入 O2 呈现

### KR7 【新增】Supplier 域 Nexus 项目群

> KR7 【新增】：【Supplier 域 Nexus 项目群】以域级集成交付模式承接 Nexus supplier 前端需求，建立可复用的跨仓交付范式（2026-09 启动；H1 里程碑：WhatsApp staging + GTM Phase 1 合入）

* KA1 - 跨仓集成范式：WhatsApp 设置页（CTOOL-634）横跨 5 仓一次打通——routing-lib 路由常量、visable-vue 导航入口、product-editor 设置页、wlw_nginx 边缘路由与 settings BFF 契约、iac 环境域名；routing 22.10.0-beta.1 六仓统一节奏。**5 仓集成需求 4 天到 Ready for QA（09-07 建票 → 09-11，Jira 时戳可查）**；范式直接复用于后续 BV（CTOOL-683）、AI Lead Enrichment（FE-1075）
* KA2 - GTM Phase 1 账号创建（CTOOL-679 Epic）：六应用依赖统一升级（beta.7→beta.8，4/6 验证完成）+ supplier-id 注入 + 403 错误页门控（替代白屏）；提前定位 bv/status 403 为前端 X-Supplier-Id 缺失，消解跨团队阻塞（CTOOL-684/685/686 已完成，8 PR 推进中）
* KA3 - 防御性交付：WA-2530 埋点与需求同步就位（0 事后补埋）；实验桶冲突提前治理
* KA4 - 交付过程工程化：全程走个人 harness 工具链（spec→plan→code→test 门禁 + 全局任务池），CTOOL-679 累计 33+ 轮迭代留痕（my-ai git log 可查），跨仓决策可回溯
* 状态说明：本 KR 于 2026-09 启动，H1 尾以里程碑呈现（WhatsApp staging + GTM 合入），主体交付在 H2（Fill Score / BV / AI Lead Enrichment）

**EN**: KR7 (new): Nexus supplier-frontend requirements delivered via a domain-level integration pattern — WhatsApp settings page spanning 5 repos in one pass (routing constant, nav entry, settings page, edge routes + BFF contract, IaC env), reaching Ready-for-QA in 4 days; GTM Phase 1 across 6 apps with unified beta pinning, supplier-id injection and 403 gating; tracking (WA-2530) shipped with the feature, zero retrofit. Delivery process itself engineered on the personal harness toolchain (33+ recorded iteration rounds). Started Sep 2026; H1 milestone = WhatsApp staging + GTM merge; main delivery lands in H2.

---

## O2：【效率效能】深化 AI Coding 应用，规范 Supplier 侧技术资产，沉淀可复用的 AI 开发工作流，显著提升个人及团队研发效率

（O 描述不变）

### KR1 【修订】资产规范 & AI 渗透

> KR1：【资产规范 & AI 渗透】完成 supplier 侧全部 6 个前端应用的技术资产规范化，达标率 100%（Q2 达成）

* KA1: repoWiki 知识库 6/6 初始化并全量发布（product-editor / supplier-onboarding / business-insights / visitors / ad-center / customer-dashboard，schema v2）
* KA2: Cursor Rules 升级为团队级 Team AI Rules 单一源（.mdc），Cursor / CLAUDE.md 双端同步，经 plugin marketplace 统一分发
* ~~个人 AI Lines 占比提升至 80%~~ —— 无回收口径，移除（H2 替代方案：用 Qoder / Cursor 面板的 AI 归因占比，建立月度记录）

**EN**: KR1 (Asset Standardization): 100% technical-asset standardization across all 6 supplier-side frontend applications — repoWiki knowledge bases initialized on schema v2 for all six; Cursor Rules upgraded to team-level Team AI Rules single source of truth distributed via the plugin marketplace. ~~Personal AI Lines ratio 80%~~ — no measurement channel; replaced in H2 by monthly AI-attribution panel records.

### KR2 【超额达成】工具沉淀

> KR2：【工具沉淀】沉淀并落地可复用的 Cursor Skills/Agent 并在团队内推广（Q1 达成；实际交付超出 ≥1 目标）

* KA1: cr-frontend Code Review Skill 搭建完成并推广到全域（Cursor + Qoder 双端 marketplace 安装）
* KA2: 能力持续迭代 4 项：HITL 修复确认、SSR 安全规则（FE-1042）、SEO 评估合并、AB 实验清理评估
* KA3: visable-plugin-marketplace 统一分发仓库建立（含 manage_github 配置与《使用指南》推广）

**EN**: KR2 (Tool Precipitation) — exceeded: cr-frontend skill built and promoted team-wide with dual-end distribution (Cursor + Qoder); four capability iterations (HITL, SSR safety, SEO assessment, AB cleanup assessment); a unified plugin marketplace repository established for distribution.

### KR3 【超额达成】流程创新

> KR3：【流程创新】输出并落地可复用的 AI 工作流并形成最佳实践（Q2 达成；实际交付 ≥2 个，超出 ≥1 目标）

* KA1: AI 驱动 Code Review 工作流（cr-frontend，团队可用）
* KA2: AI 辅助 PRD 解析工作流（Monitoring Agent 需求链路：PRD → AC → feature_list → commit/PR）
* KA3: 稳定性报告自动化工作流（fe-stability-analysis：每周 1-2 小时人工分析 → 分钟级自动报告）

**EN**: KR3 (Process Innovation) — exceeded: two-plus reusable AI workflows delivered — AI-driven code review (cr-frontend), AI-assisted PRD parsing (Monitoring Agent requirement chain), and automated stability reporting (fe-stability-analysis).

### KR4 【新增】AI 能力管理平台

> KR4 【新增】：【AI 平台建设】交付 AI Management Platform Phase 1，为内部 Skill / MCP 资产提供统一的发现、安装、发布入口（8 月达成）

* 背景：6-8 月的最大单项工程产出，原 OKR 未覆盖，补录为正式 KR
* KA1: v-ai-platform 仓库从 0 到 1（React + Vite、企业 SSO 登录、开放市场：发现/详情/收藏/发布/安装/个人中心），12 个子任务全部 Done（FE-831）
* KA2: 部署与基础设施（staging + 生产流水线、IaC、独立域名 ai.visable.com 上线，PIT-3398）
* KA3: 过程资产：中英双语 PRD、SSO 技术方案、Nuxt 4 迁移、repoWiki 同步

**EN**: KR4 (new): AI Management Platform Phase 1 delivered from scratch (v-ai-platform) — enterprise SSO login, open market (discover / install / publish / favorites / personal center), all 12 sub-tasks done (FE-831); deployed with IaC and live on ai.visable.com. Added retroactively as the largest single engineering effort of Jun–Aug, previously uncovered by the OKR.

---

## O3：【稳定性】保障前端全域应用稳定性，完善监控告警与应急响应体系，确保持续零 P0/P1 故障

（O 描述不变；「前端全域」在 8 月交接后成为真实职责范围）

### KR1 【修订·范围扩大】监控全覆盖

> KR1：【监控全覆盖】实现前端全域应用监控 100% 覆盖（原口径：Buyer 侧；2026-08 承接 VEU→VCN 交接后范围扩大至 supplier 域），支持白屏、API 错误、自定义错误与 Web Vitals 实时告警（Q1 Buyer 侧达成；9 月全域收官）

* KA1: Buyer 侧 —— Stability SDK 按 8 站点组合全量推全（ep/de·fr·tr·it·es + wlw/ch·at·de，FE-849~852）；多国站点（pt/dk/pl/nl/uk）监控接入（FE-789）
* KA2: Supplier 侧 —— 6 应用全部补齐 Sentry + 稳定性 SDK + Web Vitals（FE-1028；治理前 5/6 缺稳定性 SDK、1 个未接 Sentry；治理后全部达 product-editor 基线）
* KA3: 告警体系 —— Sunfire 数据结构适配（FE-764）+ Datadog 监控统一模板（homepage 5-monitor 标准）批量导入与订阅，两阶段收官（FE-1066/1067/1068 Done）

**EN**: KR1 (Full Monitoring Coverage) — scope expanded: 100% monitoring coverage across all frontend applications (originally Buyer-side only; expanded to the supplier domain after the VEU→VCN handover in Aug). Stability SDK fully rolled out across 8 site combos (FE-849~852); all 6 supplier apps completed Sentry + Stability SDK + Web Vitals (FE-1028); Sunfire data-structure adaptation plus unified Datadog monitor templates imported and subscribed, closed out in September (FE-1066).

### KR2 【修订·探索→交付】AI 智能运维

> KR2：【AI 智能运维】交付 Monitoring Agent 线上监控能力，实现多信号源自动采集、自动总结与巡检报告（Phase 1 已交付，Q2 目标达成；v2 覆盖度诊断进行中）

* KA1: Monitoring Agent Phase 1（FE-907，M1-M4 全 Done）：五信号源自动采集（Datadog / Sentry / 稳定性 SDK / Defensive SEO / 埋点巡检 + 新增 AWS 第 5 源）、定时巡检、结构化监控报告
* KA2: fe-stability-analysis Skill（FE-872）：稳定性周报端到端自动化，覆盖核心应用，故障定位数据获取从小时级降到分钟级
* KA3（进行中）: v2 监控覆盖度诊断（FE-984）：需求链路解析、失败模式推导、现有信号匹配器、置信评估模型
* 配套：QA Evaluation Platform 前端（FE-930，6 子任务 Done）作为 AI 质量评估的配套载体

**EN**: KR2 (AI Ops) — delivered beyond "exploration": Monitoring Agent Phase 1 shipped (FE-907) — five signal sources auto-collected (plus AWS as the 5th source), scheduled patrol, structured monitoring reports; fe-stability-analysis skill automated the weekly stability report end-to-end (FE-872); v2 coverage diagnosis in progress (FE-984); QA Evaluation Platform frontend delivered as a companion (FE-930).

### KR3 【修订】专项治理 → 误报治理

> KR3：【专项治理】主导稳定性 SDK 误报治理专项，消除噪音信号对告警有效性的干扰（Q2 交付；错误总量下降指标延后回收）

* KA1: 页面导航中断 fetch 的误报修复（FE-1037）
* KA2: 第三方资源与 API 噪音内置忽略列表；slow check 默认关闭
* KA3: 线上异常调查方法论沉淀（CloudFront 错误激增调查：定位爬虫噪音，非 CDN 故障，产出报告）
* ~~原目标：推动接入 SDK 应用前端错误总量下降 XX%~~ —— 口径未定；H2 以 ODPS 稳定性数据环比口径回收（HubSpot 噪音过滤 FE-1019 已立项）

**EN**: KR3 (Special Governance) — rescoped to false-positive governance: fetch-aborted-by-navigation fix (FE-1037), built-in ignore lists for third-party noise, slow check disabled by default, online anomaly investigation methodology (CloudFront incident). ~~Original: reduce total error volume by XX%~~ — measurement caliber pending; to be recovered in H2 via ODPS stability data.

### KR4 【新增】Supplier 域交接与技术治理

> KR4 【新增】：【组织与治理】完成 supplier 前端域 VEU→VCN 知识转移与技术治理盘点，产出项目整合方案与技术重构立项（8-9 月交付）

* 背景：8 月组织调整后新增的职责范围，原 OKR 未覆盖，补录为正式 KR
* KA1: 知识转移 —— KT Question List、14 项 In-Flight 项目清单、监控告警交接、VEU Handover 页面，交接无断点
* KA2: 治理盘点 —— 改造必要性盘点（稳定性/repoWiki/性能矩阵）、BFF vs 同源调用分析、路由与本地调试工具文档（routes / init.sh）、P0-P2 改造清单
* KA3: 方案产出 —— 6 应用整合为 2-3 个的整合方案（分 4 步实施）；技术重构 Epic 立项（FE-1062）

**EN**: KR4 (new): Completed the VEU→VCN knowledge transfer for the supplier frontend domain (KT question list, 14-item in-flight inventory, monitoring handover) and produced the technical-governance deliverables — refactoring necessity matrix, BFF vs same-origin analysis, P0-P2 improvement list, and a consolidation proposal (6 apps → 2-3), with the technical refactoring epic established (FE-1062). Added retroactively to cover the organizational handover absorbed in August.

---

## 修订总览（一页速览）

| 位置 | 处理 | 一句话 |
|---|---|---|
| O1-KR1 | 改写 | GA4 迁移 + 数据层验收为实际形态；Badcase/治理划线移出；无口径数字删除 |
| O1-KR2 | 保留 | KA 结果固化（save +15%/+18%；采纳率 +31/+21.8pp 未达 60% 如实标注）；主体指标移 H2 |
| O1-KR3 | 划线取消 | 随 CTOOL-368 Won't Do，留痕 |
| O1-KR4 | 维持划线 | 原样 |
| O1-KR5 | 改写 | HITL 实践落地；独立 AB 框架划线，实验桶治理如实呈现 |
| O1-KR6 | 改写收尾态 | 架构交付写实；上线指标划线；方向并入 O2 |
| O1-KR7 | **新增** | Nexus supplier 域跨仓交付范式：WhatsApp 5 仓 4 天到 QA、GTM 六仓统一、埋点随发就位 |
| O2-KR1 | 改写 | 资产规范 100% 写死；AI Lines 80% 删除并给 H2 口径替代 |
| O2-KR2 | 超额标注 | 1 个 skill → 双端分发 + 4 项能力迭代 + marketplace |
| O2-KR3 | 超额标注 | ≥1 个工作流 → 实际 3 个 |
| O2-KR4 | **新增** | AI Management Platform Phase 1（6-8 月最大单项产出） |
| O3-KR1 | 范围扩大 | Buyer 侧 → 全域（8 月交接），Sunfire → 双平台，9 月收官 |
| O3-KR2 | 探索→交付 | Monitoring Agent Phase 1 + fe-stability 自动化 + QA 平台 |
| O3-KR3 | 改写 | 错误总量 XX% → 误报治理专项；总量口径 H2 回收 |
| O3-KR4 | **新增** | Supplier 域交接与技术治理（8 月新增职责） |
| Nexus 项目群（H2 主体） | 已入 O1-KR7（H1 里程碑：WhatsApp staging + GTM 合入）；FillScore/BV/AI Lead Enrichment → 「接下来的规划」/ H2 OKR 雏形 |
