# FY27 H1 OKR 结果收录

> 用途：收录 FY27H1 全部 O/KR 的量化结果，供 OKR review 时直接引用写结果。
> 对比口径约定：改造前基线 = 2026-01~02 加权；推全后 = 2026-05~08 加权。AI 改造：2026-03-13 发布、2026-04-02 推全；Quick Editor：2026-04-27 开 A/B、2026-06-02 推全。数据截至 2026-09-28。
> 未完成的 KR 保留"待收录"占位，结果出来后按同样格式填入。

---

## O1【业务增长】构建 AI 驱动的商品管理与内容优化体系，通过 A/B 实验验证策略，提升商家效率与商品质量，支撑商品规模翻倍与质量提升的业务目标

### KR1【数据基建】完成商家后台 4 个应用共计 9 个模块的 GA4 埋点迁移与数据层验收

**结果：1 期商家后台 4 个应用的 9 个模块全部完成迁移；2 期已发布 1 个模块，另有 2 个模块完成开发与验证、待发布；仅剩 2 个业务模块待迁移**

| 阶段 | 范围 | 状态 |
|---|---|---|
| 1 期 | 商家后台 4 个应用的 9 个模块 | 迁移完成 |
| 2 期 | 1 个模块 | 已发布 |
| 2 期 | 2 个模块 | 完成开发与验证，待发布 |
| 剩余 | 2 个业务模块 | 待迁移 |

### KR2【新商转化】升级商品管理后台全流程体验，通过 A/B 实验验证，提高 AI 的商家采纳率 >60%，提升平台每日人均保存商品数

**结果：① AI 商家采纳率达标（UV 级 64.8% ~ 70.3%，> 60%）；② A/B 期间实验组每日人均保存商品数较对照组 +34.7%（含新鲜感效应，逐周衰减至 +9%）；推全后平台日均人均保存商品数较推全前 +12.5%（剔除 9 月约 +16%），与实验稳态水平一致**

**① 提高 AI 商家采纳率（>60%）—— AI Keywords/Category（eventlabel='new'，新建商品流程）**

| 指标 | 改造前（01~02 月） | 推全后（05~08 月） | 变化 | 对应目标 |
|---|---|---|---|---|
| AI Keywords 采纳率（UV 级） | 57.6% | 70.3% | +12.7pp | >60% 达标 |
| AI Category 采纳率（UV 级） | 42.0% | 64.8% | +22.8pp | >60% 达标 |
| AI Keywords 采纳率（事件级） | 21.3% | 52.0% | ≈2.4 倍 | — |
| AI Category 采纳率（事件级） | 19.6% | 48.7% | ≈2.5 倍 | — |

**② 提升平台每日人均保存商品数 —— Quick Editor A/B 实验（4.27 开 A/B、6.2 推全）**

| 指标 | 对照组 control | 实验组 treatment | 提升 |
|---|---|---|---|
| **每日人均保存商品数** | 5.41 | **7.28** | **+34.7%** |
| 人均保存商品数（A/B 期间累计） | 8.09 | 11.42 | **+41.1%** |
| 每日人均保存动作 | 5.40 | 6.62 | +22.5% |
| 人均保存动作（A/B 期间累计） | 8.08 | 10.50 | +29.9% |
| 单次保存覆盖商品数 | 1.00 | 1.09 | +8.7% |

按周趋势（新鲜感衰减证据，人均保存商品数）：

| 周次 | 对照组 | 实验组 | 提升 |
|---|---|---|---|
| W1（04-27~05-03） | 6.09 | 10.26 | +68.7% |
| W2（05-04~05-10） | 5.67 | 9.87 | +74.1% |
| W3（05-11~05-17） | 8.13 | 11.27 | +38.6% |
| W4（05-18~05-24） | 6.87 | 8.82 | +28.4% |
| W5（05-25~06-01） | 7.27 | 7.95 | +9.4% |

推全前后平台整体走势（稳态读数）：

| 窗口 | 天数 | 日均 UV | 日均保存商品/人 |
|---|---|---|---|
| 推全前（03-01~04-26） | 57 | 167 | 6.34 |
| A/B 期间（04-27~06-01） | 36 | 163 | 7.70 |
| 推全后（06-02~09-28） | 119 | 178 | 7.13（较推全前 +12.5%） |

注（review 答辩用）：

- ① 采纳率主口径为"新建商品流程"（eventlabel='new'）：该场景建议量占约 1/3、采纳量占约 73%，是 AI 建议价值主力；整体口径（含编辑已有商品）事件级 Keywords +87%、Category +83%
- ① 事件级 = 采纳事件数 ÷ 建议事件数（每次建议被采纳概率）；UV 级 = 采纳过去重用户 ÷ 收到建议去重用户（人群渗透）。4.2 推全时建议触发逻辑有变更，达标判定以 UV 级为准
- ② A/B 两组样本均衡（control 1,497 / treatment 1,550 UV）；口径为 8 个 save 事件（列表保存×2、编辑器弹窗×3、发布页 CTA×3，与查询 1338/1340 一致），Quick Editor 无独立 save 埋点，无漏计
- ② 全量 +12.5% 低于 A/B +34.7% 的主因是新鲜感效应：实验组提升逐周衰减（W1 +68.7% → W5 +9.4%），A/B 末周稳态差距（+9%）与推全后平台提升（+12.5%，剔除 9 月约 +16%）基本一致，数据自洽
- ② 次要因素：实验仅覆盖约一半保存用户（分桶周均约 600~780 人 vs 未分桶约 660~735 人），且分桶用户人均保存（6~11）高于未分桶（约 4.5），平台口径被轻量用户摊薄；9 月走低（日均 6.39 vs 8 月 7.52）拖累推全后窗口约 2pp
- ② 答辩口径：若被问"为何全量只有 +12%"，答"实验全周期均值含新鲜感高峰，稳态差距 W5 已收敛至 +9%，与全量 +12.5%（剔除 9 月约 +16%）一致"；衰减不排除曝光机制差异，需曝光日志才能完全排除
- ①② 叠加提示：05~08 月人均保存动作较 01~02 +27.7% 为 AI 改造与 Quick Editor 的叠加效应，review 时勿对两个需求重复归因
- 3 月为灰度混合月、4 月为推全过渡月、9 月为不完整月，均未纳入对比
- 数据源：Redash 仪表盘「AI 建议采纳率监控（新建商品流程）」（id 403），查询 5682 / 5683；A/B 与保存行为口径参考查询 1338 / 1340 / 1302

### KR3【Accio Work】完成 Accio Work Visable 核心架构建设，交付三个技能（Performance Insights、Company Profile Optimization、Product Optimization）的插件形态落地

**结果：Accio Work Visable 双仓库架构（Plugin 配置包 + MCP Server）设计完成并落地首版——产出 visable-assistant 插件包（34 文件 / 4,476 行：Agent 层 + 三个技能 + 插件记忆机制 + 连接器与引导资源），协助 Connector/OAuth 认证链路落地（connectors.json 授权配置、MCP 工具注册重构、accio_id 身份参数全链路贯通）；三个技能均以插件形态交付，Performance Insights 留存并被团队生产化至 v2.2.2（65 行骨架 → 1,087 行），Company Profile Optimization 与 Product Optimization 在团队重构中移除，插件末态收敛为单技能形态（v0.1.3）；跨用户上下文串用缺陷 CTOOL-589 已修复。PRD 定义的上线指标未回收，插件发布 CI 闭环未建**

**一、KR 结果**

**① 双仓库架构设计**

| 交付物 | 体量 | 性质 |
|---|---|---|
| Visable 侧技术方案（概览 + 实现 + 轻量备选三版） | 1,206 行 | 本人原创 |
| 实施计划（Task 级拆解） | 1,518 行 | 本人原创 |
| 插件包设计文档 + 实施计划 | 991 行 | 本人原创 |
| Visable Connector PRD + 三技能规格 | 724 行 | 归属待确认（见注） |
| Accio 平台接入规范与答疑纪要 | 2,001 行 | 采集整理（Accio 团队文档 1,866 行 + 本人接入答疑纪要 135 行） |

- 本人原创方案与计划合计 **3,715 行**（已入库 my-ai，commit d0c8624 / 420cfa8）
- 方案核心内容：三种接入形态（Agent+Skill / CLI / Connector-MCP）对比与选型论证、双仓库职责边界与唯一耦合点（connectors.json 的 MCP Server URL）、9 个 MCP 工具契约、OAuth / MCP Gateway 认证链路、三阶段交付计划、10 项依赖 Accio 的未知项按 P0/P1/P2 分级
- 架构落成的两个仓库：`v-agent-hub-bamboo`（Plugin 配置包）+ `supplier-backend-mcp-service`（MCP Server），与设计一致

**② visable-assistant 插件包（首版交付态）**

| 模块 | 体量 | 说明 |
|---|---|---|
| Agent 层 | 6 文件 / 252 行 | agent.json、agents.md（技能消歧规则 101 行）、identity（商业红线）、soul、bootstrap、user |
| visable-product-opt（Product Optimization） | 2,021 行 / 10 文件 | SKILL.md 542 行 + 6 份 reference + 中英 README |
| visable-supplier-diagnostics（Company Profile Optimization） | 88 行 | Store Profile Diagnostics，接 `get_company_by_id` |
| visable-business-insight（Performance Insights） | 65 行 | 数据洞察骨架 |
| plugin-memory-manager（插件记忆机制） | 1,544 行 / 9 文件 | 6 个 Python 脚本（bootstrap_load / memory_manager / post_skill / skill_lifecycle / outcome_manager / linker）+ jit/outcome 配置 |
| supplier-self-evolving | 273 行 | 自演进技能 |
| 接入与资源 | — | connectors.json（MCP + OAuth）、dependencies.json、plugin.json、recommend.json、logo |

插件包首版合计 **34 文件 / 4,476 行**；本人 main 提交 18 个、涉及 33 个文件，PR #1（30 文件 +3,804 行）/ #2 / #3 / #20 / #33。

**③ 三技能末态**

| KR 技能名 | 仓库内技能名 | 交付态 | H1 末态 |
|---|---|---|---|
| Performance Insights | visable-business-insight | 65 行骨架 | **留存，v2.2.2 / 1,087 行**（团队生产化，≈4.7 倍） |
| Company Profile Optimization | visable-supplier-diagnostics | 88 行 | 团队 PR #13「skill driven company selection」重构中移除 |
| Product Optimization | visable-product-opt | 2,021 行 / 10 文件 | 团队 PR #16「no agent mode」重构中移除 |

插件末态：main v0.1.3，12 文件 / 1,306 行，单技能形态（Agent 层改为 prompt.md 44 行）；仓库最后 push 2026-06-29，此后无演进。

**④ 协助 Connector/OAuth 认证链路落地**

- 插件侧：connectors.json 的 MCP Server 注册与 OAuth 配置（含授权不可用时的禁用处理与数据服务地址切换）
- 服务侧（`supplier-backend-mcp-service`）：PR #2 工具注册重构 + README（14 文件 +172/−26）；PR #4 为多个工具贯通 `accio_id` 身份参数 + docstring 规范化（6 文件 +116/−5）；工具命名跨仓对齐（`getCompanyById` → `get_company_by_id`，与技能侧 SKILL.md 引用一致）
- 现 main 上 `accio_id` 贯通 6 处（client → service → 4 个 tool）
- 归属边界：OAuth v2（PR #5）与 Accio token 校验（confidential client introspection）由后端同学完成，本人承担插件侧配置与身份参数贯通

**⑤ 质量收口**

CTOOL-589「[Accio] reuses information from previous chat for a different user」Development Defect，状态 Closed / Fixed；修复方式为 prompt.md 加入 Memory Policy（non-negotiable）4 条硬约束，并将 memory search 纳入 Anti-Redundancy 禁用清单（PR #20）。另有插件清单与品牌资源收口（PR #33）。

**二、个人亮点贡献**

**① 定下 Visable 侧的接入路线，而不是等平台给方案**

Accio Work 提供 Agent+Skill / CLI / Connector(MCP) 三种接入形态，平台侧不会替业务选。选定 MCP 并给出三条论证：业务核心是后端真实数据（店铺健康度、转化漏斗，LLM 无法自行生成）、token 由 MCP Gateway 统一持有不落用户本机、接口变更只改服务不需重发插件。同时把双仓库的耦合面收敛到 connectors.json 里的一条 URL——后端接口演进不再牵动插件发版，这个边界后续被团队沿用。

**② 插件包从 0 到 1 一次成型，成为团队后续全部迭代的载体**

PR #1 单次 30 文件 +3,804 行，Agent 层（含技能消歧规则与商业红线）、三个业务技能、连接器与引导资源同时就位；另建插件记忆机制（6 个 Python 脚本 / 1,544 行），是当时插件内唯一的跨会话状态层实现。团队后续 4 位同学的迭代（含把 Performance Insights 生产化到 v2.2.2）都跑在这个骨架上；main 上该插件目录的提交数本人 18 个，与两位主要贡献者持平。

**③ 把身份链路打通，让"谁在问"贯穿到工具层**

`accio_id` 身份参数从 client → service → tool 全链路贯通，并把 MCP 工具命名与技能侧引用跨仓对齐。这是多公司供应商场景下"不串号"的前提，也让后来 CTOOL-589 能被定位到会话/记忆层而非数据层。

**④ 风险前置：设计阶段就把未知项摊开，并留一条备选路线**

技术方案里把 10 项依赖 Accio 的未知项按 P0/P1/P2 分级列出（Plugin 注册方式、MCP Gateway 地址、OAuth redirect_uri、CI 版本登记 endpoint、对象存储方案等），逐项标明阻塞哪个阶段；同时保留一份不依赖自建 MCP Server 的轻量备选方案（Browser Session 认证）。联调期因此没有出现"等平台回答"的空转。

**⑤ 跨用户数据串用缺陷用策略硬约束收口，而不是加提示词**

CTOOL-589 属数据安全性质。修复没有走"提醒模型注意"的软路径，而是在 prompt 层立 Memory Policy（non-negotiable）：禁止使用跨会话记忆，回答只能基于当前会话、用户显式输入与本次 MCP 结果；并把 memory search 写进 Anti-Redundancy 禁用清单，堵住"工具失败时回退去查记忆"的旁路。

注（review 答辩用）：

- **"交付三个技能的插件形态落地"在首版插件包内一度成立**（三技能 + 记忆机制同在一个插件包），但 H1 末态仅 Performance Insights 留存；两次移除均由团队重构决定（PR #13 skill-driven company selection、PR #16 no agent mode，后者单次 −4,658 行），非本人交付回退。若被问"三个技能呢"，按此口径答
- Performance Insights 的生产化由团队完成（PGS-802 技能路由 / PGS-815 未读消息数不一致 / PGS-840 免费会员商品明细口径 / PGS-850 模板泄漏与 deepLinks 映射）；本人贡献为骨架与插件接入形态，不写成该生产版本的作者
- **上线指标零回收**：PRD §12 的 9 项 launch 指标（Auth ≥85%、多公司选择成功率 ≥95%、Insight delivery ≥85%、Skill completion ≥70%、Skill failure ≤5%、Confirmed write success ≥90%、Unsafe write incidents = 0、Benchmark 透明度 100%、PM UAT 100%）与 4 项 30 天健康指标均无数据；与 `修订稿-v2` KR6 已划线的"技能完成率 ≥70%、写操作成功率 ≥90%"口径一致，勿一处划线一处申报
- **发布闭环未建**：设计中的 Phase 3（Git Tag → GitHub Actions → plugin.zip → phoenix-gateway 版本登记）未落地，仓库无 tag、无 release.yml
- **「核心架构」的归属边界**：团队 agent hub 底座 `v-agent-hub-base`（11 commits）由同事独立完成，本人未参与；本人产出为 Visable 侧接入架构（形态选型、双仓库边界、插件内部结构、认证链路设计与配置）。若被问"Accio Work 核心架构是不是你建的"，答"Accio 平台侧架构由 Accio 团队定义，我完成的是 Visable 侧接入架构与插件实现"
- ① 表中 2,001 行为 Accio 团队文档的采集与整理（Plugin System 工程侧设计方案 1,642 行 + 六步配置规范 224 行）加本人接入答疑纪要 135 行，不计入原创设计产出；原创口径只取 3,715 行
- 证据面：架构文档在 `my-ai/docs/superpowers/`（已入库）与本地 `my-ai/v-accio/`（被 .gitignore 排除，未入库）；**无 Confluence 交付页**，外部可验证证据仅 GitHub 提交 + Jira 工单
- 待确认：`v-accio/requirement/` 的 PRD 与技能规格署名 PM Owner = Dominik Dern、Eng Lead = Qin Zhang，本地无提交痕迹可证作者。若为收到后归档，① 表中 724 行应从本人交付剔除
- 数字口径：4,476 行 = commit `1ada4de`（PR #3 合并态）下 `plugins/visable-assistant` 全目录行数，含 SVG 资源；1,087 行 / v2.2.2 为 origin/main 末态读数
- 数据源：`v-agent-hub-bamboo`（PR #1/#2/#3/#20/#33，峰值态 commit 1ada4de，末态 origin/main，远端 pushed_at 2026-10-07 实测）、`supplier-backend-mcp-service`（PR #2/#4，commit a4e76f1）、Jira CTOOL-589 与 PGS-802/815/840/850（Jira 数据采集日 2026-09-12）、`my-ai/docs/superpowers/specs|plans/2026-04-21-*` 与 `2026-05-06-*`

### KR4【Nexus & GTM】承接 supplier 域 Nexus 系列前端需求，探索跨应用开发方式

**结果：承接 Nexus / GTM 系列前端需求 5 项（其中 2 项主开发），横跨 11 个仓库交付 18 个 PR；探索并跑通 harness 跨应用开发方式——以个人工具仓驱动公司多仓开发，目标仓零安装，单个需求单任务最大统管 8 个仓库，已沉淀 10 个仓库工作区**

**一、KR 结果**

**① 需求承接**

| 需求 | Jira | 我的角色 |
|---|---|---|
| Nexus WhatsApp Integration — Supplier Portal Settings | CTOOL-634 + 635/636/637 | 建票拆票 + 主开发 |
| GTM Phase 1 — Alibaba GGS 账号创建 | CTOOL-679 + 684/685/686 | 建票拆票 + 主开发 |
| Alibaba Business Verification 状态展示 | CTOOL-683 / FE-1076 | 建票 + 范围定义 + 前端件交付 |
| GTM Phase 1.5 — Product Fill Score 权重更新 | CTOOL-678 | 建票 + 权重口径拍板 |
| Nexus AI Lead Enrichment | FE-1075 | 建票 + 仓库归属与范围定义 |

**② 交付状态（截至 2026-10-07）**

- 已进入团队 staging 集成分支：product-editor（WhatsApp settings hub + Alibaba banner + 21 语言）、user-frontend（账号删除入口）、business-insights（组件库 beta 版）
- 18 个 PR 待合并主干，发版火车由同事接力推进；外部依赖阻塞项 6 条（后端端点、边缘路由、IAM 部署、GA3 终验、多语言审校、测试身份从属）

**二、个人亮点贡献**

**① 把工作单元从"仓库"换成"需求"，让单需求跨多仓开发第一次可被一个人驱动**

AI 编码工具的天然边界是单个仓库，跨仓需求只能在每个仓重新解释上下文，且拿不到依赖拓扑（谁先发版、谁必须同窗口上线）。我把任务做成全局池：一个任务条目同时持有多个仓的 spec / plan / 进度 / 证据。CTOOL-634 单任务统管 5 个仓（routing-lib → visable-vue → wlw_nginx + iac + 应用）、CTOOL-679 单任务统管 8 个仓（组件库 + 6 个应用 + user-frontend），依赖顺序与合并窗口在一个上下文里推完。

**② 零侵入设计，使跨仓开发不需要任何仓库 owner 批准**

引擎、任务状态、经验全部留在个人工具仓，公司仓库不落任何工具文件（只有 `docs/changes/<task>/` 的 spec/plan 属正常项目产物）。这是能同时改动 11 个仓的前提——包括我并不拥有的 nginx 边缘配置仓、iac 基础设施仓和 4 个长尾 supplier 应用，无需提"接入框架"的改造 PR，推广成本为零。

**③ 把踩过的坑从聊天记录变成结构化资产，仓知识跨任务复用**

每个注册仓一份 config.sh（lint / typecheck / test 命令）+ notes.md（技术栈与坑）+ e2e-context.md，一次积累、后续任务直接复用，已沉淀 10 个仓库工作区。实际价值：这批 6 个应用有 4 种包管理器（pnpm / yarn4 / npm×2，其中一个 `packageManager` 字段声明与实际 lockfile 不符）、一个仓主干是 master 而非 main、装包缺 token 会静默装成旧版本——这些过去每开一次新会话都要重踩一遍。

**④ 实现者与验收者分离，流程轻重由人显式决定**

工具里写死"只做实现者、绝不做验收者"，验收走独立的测试技能与 validate / verify 命令；standard / minimal 两档流程只能由人显式切换，不主动降级、不替人判断任务大小。AI 驱动但判断权在人，这是这套方式敢用在业务需求上的前提。

注（review 答辩用）：

- 目标句是"承接 + 探索"，两项均有实证；上线口径以团队发版火车为准。若被问进度，答"前端件已进 staging 集成分支并由同事接力推进，主干合并受 GTM 整体上线节奏与 6 条外部依赖制约，非前端交付缺口"
- 亮点 ① 是本 KR 的核心，②③④ 是它的推论；跨应用开发方式此前团队没有成型做法，本期第一次完整跑通并回流为 playbook，后续 Nexus 需求（AI Lead Enrichment）由同事在我搭的 supplier settings hub 上直接叠加，验证了产出的页面可作为跨需求载体
- CTOOL-678 / FE-1075 代码作者是同事，我的贡献是建票、范围定义与口径拍板，不写成开发交付
- 与 O2 的边界：本 KR 只写"用 harness 跨仓方式承接业务需求"（实践验证），harness 工具本身的建设与资产沉淀归 O2-KR3 / KR4，playbook 不在此展开，避免重复归因
- 数字口径：10 个注册工作区 ≠ 单任务 8 仓；CTOOL-679 的 8 个仓中 4 个为注册工作区，另 4 个长尾应用为任务内驱动、未建知识库。目前该方式仅本人使用，无同事试用记录，不写"团队级"
- Jira 状态引自 2026-09-12 采集快照，近三周未复核；Git / PR / 分支状态为 2026-10-07 远端实测

---

## O2【前端 Harness 工程】建设前端研发 Harness，聚焦 Monitoring Agent 与 AI 研发基建两个方向，沉淀可复用的工具与工作流，显著提升团队研发效率

### KR1【Monitoring Agent】交付 Monitoring Agent 线上监控能力，实现多信号源自动采集、自动总结与巡检报告

**结果：Phase 1 交付并投入真实使用（FE-907 + M1~M4 全 Done）；5 类信号源自动采集、11 个前端应用在案、08-12~09-24 累计 21 次真实运行；产出结构化报告与可检索能力目录；技能以 monitoring-orchestrator v4.0.0 随团队插件四端分发**

**一、KR 结果**

| 项 | 内容 |
|---|---|
| 信号源 5 类 | Datadog Logs、Sentry、稳定性 SDK（ODPS）、埋点巡检、AWS ECS（FE-985）|
| 覆盖应用 11 个 | search、product-editor、homepage、unified-search、customer-dashboard、business-insights、requests、conversations、visitors、supplier-onboarding、user-frontend |
| 报告形态 | HTML + Markdown 结构化报告、按错误类型展示、可检索能力目录（FE-986/987/988）|
| 真实使用 | 21 次 run（08-12~09-24），每 run 按项目落 evidence 与报告 |
| 触发路径 | 全量定时巡检；发布后按发布时间推窗（release-guard v2.0.0）|
| 配套自动化 | 稳定性周报自动化（FE-872，8 子任务）：每周 1~2 小时人工分析压成自动编排，定位取数从小时级到分钟级 |

**二、个人亮点贡献**

- Phase 1 四个里程碑独立设计并交付，建单、方案、验收均由我产出，是唯一交付人
- 第 5 信号源 AWS ECS 由我提出并改走 Datadog AWS 集成取数，不引入 AWS 凭据与 CloudWatch 直连，一套 key 覆盖五源
- 主导拆分采集引擎与发布生命周期，evidence 与窗口边界走标准接口，KR2 覆盖度诊断直接复用
- 定下「只做真实调用」纪律：缺凭据、超时、空响应如实报 partial 或 unavailable，不生成合成指标

注（review 答辩用）：

- FE-923~926 的 Jira 标题是 M1~M4 里程碑任务，修订稿旧说法「四份生命周期文档」不准确，勿沿用
- 21 次 run 含验证性运行（08-12 有 3 次在 8 分钟内连续触发），对外建议写「累计 21 次真实运行（含验证）」；定时调度是否已固化为无人值守任务待确认后再写死
- MVP 子目标（≥5 次真实发布端到端 + auto Jira 回流）9/30 未达成，已明确不入 OKR；是否留一行「H2 收尾缺口」待拍板
- 与 O3 边界：告警体系与 SDK / ODPS 链路建设归 O3-KR1，本 KR 只写 Agent 侧采集、总结与报告能力

### KR2【监控覆盖度诊断】建立需求级监控覆盖度诊断机制，支持需求上线的覆盖评估

**结果：诊断机制建成为四技能闭环并在真实需求 CTOOL-637 跑通——推导 11 个业务失败模式，判定 6 个可被现有监控检测（4 高 + 2 中置信）、5 个为静默失败盲区**

**一、KR 结果**

| 环节 | 技能与版本 |
|---|---|
| 诊断 | coverage-diagnosis v1.2.0 |
| 补全建议 | gap-recommendation v1.1.0（同 run 链式触发）|
| 筛选登记 | coverage-filter v1.0.0 |
| 上线核对 | requirement-guard v3.0.0 |
| 发布守卫 | release-guard v2.0.0 |

实证 CTOOL-637（WhatsApp 设置页，product-editor PR #103 @ cde6f95d，run 20260923T082143Z）：输入结构化 intake bundle（24 需求 / 8 开放问题 / 65 证据），产出 11 个失败模式与 6 份产物（coverage_report.md/.json、failure_modes.json、match_result.json、recommendations.md/.json），统一落 `.v-harness/<需求号>/monitoring-agent/diagnosis/`；上线核对路径有 ARISE-1360 三次 patrol run 为证；需求链路解析（PRD 到 AC、feature list 再到 commit 与 PR）FE-989 Done。

**二、个人亮点贡献**

- 独立设计方法论：需求证据推导失败模式，用失败模式匹配现有监控能力，按四档口径（高 / 中 / 低 / 不可覆盖）出结论，把「监控够不够」从主观判断变成可复核产物
- 定下判定纪律：凭据或内网不可达时 api_name / page_id 标 unverified 并强制降置信，5 个静默失败盲区如实标为不可覆盖，不折算成已覆盖
- 打通需求侧与监控侧产物协议：intake bundle、诊断产物、筛选条件三段用统一目录规范串起来（FE-1060/1061，随插件 0.5.0 落地）
- 推动两条技能改进写进规则并升到 v1.2.0：混合失败模式必须拆开单独判定；page_id 接线要核实 definePageMeta 与 virtualPageTitle 链，GA 常量不算证据

注（review 答辩用）：

- **Jira 状态落后于实物**：FE-990（失败模式推导）、991（信号匹配器）、992（置信模型）在 09-12 快照里是 In Progress，但技能已 v1.2.0 且产物含 failure_modes / match_result，实际已落地；收录前建议先回收 Jira 状态
- **常态化缺口**：完整诊断目前只在 1 个真实需求上跑通，尚未形成「每个上线需求都诊断」；FE-993/994/999 在快照里为 Backlog，需复核现状
- CTOOL-637 为代码级判定，未做活体验证（内网不可达、Datadog / Sentry 凭据缺失），报告内已如实标注
- 与 KR1 边界：本 KR 只写覆盖度诊断与上线核对，信号采集与巡检报告归 KR1

### KR3【AI 资产平台】建设团队级 AI 资产平台与 AI 质量评估平台，统一 Skill、MCP、规则等研发资产的发现、安装与发布

**结果：AI Management Platform Phase 1 从 0 到 1 建成并部署（FE-831 + 12 子任务全 Done），覆盖 agent / skill / mcp 三类资产的发现、详情、发布、版本与个人中心，含企业 SSO，前后端与 IaC 三仓自建；QA Evaluation Platform（FE-930 + 6 子任务全 Done）交付 6 个评估界面**

**一、KR 结果**

| 项 | 内容 |
|---|---|
| 平台能力 | 登录与 SSO 回调、资产发现、资产详情、三类资产发布、发布编辑、版本发布、运营位、个人中心（实测 `src/app/router.tsx`）|
| 技术形态 | React + Vite SPA（由 Nuxt/Vue 迁移，commit e1b0a01）；Azure AD OAuth2 Proxy |
| 三仓自建 | v-ai-platform（前端）、v-ai-platform-backend（domain / application / infrastructure / interfaces / common 五层）、v-ai-platform-iac；staging 与生产流水线、nginx 镜像、生产 base path |
| QA 评估平台 | 仪表盘与能力卡片、评估任务生命周期、Score Overview、Rules Perspective、Version Comparison、Low-Score Samples（FE-967~972）|
| 过程资产 | 中英双语 PRD、SSO 设计规范与实施计划、Nuxt 4 迁移、repoWiki 同步 |

**二、个人亮点贡献**

- 6~8 月最大单项工程产出，技术选型、SSO 方案、市场功能、部署流水线与 IaC 一人从 0 到 1 交付，12 个子任务全 Done
- 中途完成 Nuxt/Vue 到 Vite/React 迁移，并把已交付的资产平台增强整体移植到 React 架构，迁移未丢功能
- SSO 三条路径（登录、回调、鉴权失败）各有独立页面，设计规范与实施计划均留文档
- 产出中英双语 PRD，使平台对非中文团队可用
- QA Evaluation Platform 前端从 0 到 1，为团队 AI 质量评估提供界面载体

注（review 答辩用）：

- **QA 评估平台代码下落待核实**：本地 v-ai-platform 全分支历史搜不到 evaluation / quality / score / dashboard 任何文件，v-ai-frontend 亦无，目前只有 Jira 证据；核实前不写「已上线」
- **域名待核实**：`ai.visable.com`（出处 PIT-3398）未在 v-ai-platform-iac 中 grep 到；本地 feature/qa-platform 分支未合入 main（main 停在 5fb9264），勿把未合并内容写成已交付
- **缺运营数据**：注册资产数、安装次数、活跃用户数是这条 KR 最有说服力的量化项，需从平台后端库取，目前空白
- 与 KR4 边界：KR3 写平台载体（发现、安装、发布入口），KR4 写资产本身（技能、规则、知识库的数量与采用）

### KR4【AI 资产沉淀】沉淀并推广团队级 AI 研发资产，形成团队内可直接复用的资产库

**结果：团队资产库成形——统一分发仓 4 插件 / 56 技能，覆盖 intake、spec、dev、verify、deploy、monitoring 六个阶段，支持 Codex / Cursor / Qoder / Claude Code 四端安装；团队编码规则单源化为 6 个 `.mdc`；repoWiki 我承担 7 仓；marketplace 33 次提交中 13 次来自 4 位同事**

**一、KR 结果**

| 资产 | 内容 |
|---|---|
| 插件与技能 | visable-fe-domain-agents 32（0.5.0）、visable-fe-ai 17（0.5.0）、visable-be-ai 6（0.2.0）、vcn-be-ai 1（0.1.0），合计 56 |
| 四端分发 | 每插件四套 manifest（`.codex-plugin` / `.cursor-plugin` / `.qoder-plugin` / `.claude-plugin`）版本对齐，README 给全四端安装更新命令与 Cursor Team Marketplace 托管 rollout 路径 |
| 阶段覆盖 | intake-agent；dev-agent（write-spec / write-plan / red-green / commit-task / orient-in-repo）；verify-agent（smoke-verification）；deploy-agent（staging-deployment / release-plan）；monitoring-agent（orchestrator、coverage 家族、release-guard、requirement-guard）；另 jira-lifecycle 7 技能、知识库 5 技能、cr-frontend、legacy-pd-estimator、d2c、webvital-maxcompute-sql |
| Team AI Rules | 6 个 `.mdc` 单一源（design-tokens / frontend-standards / performance / react / tracking / vue3），CLAUDE.md 与 AGENTS.md 双端同步，配 mcp.json 与 hooks |
| repoWiki | 我承担 supplier 域 6 仓 + product-editor schema v2 重建 = 7 仓，配套 5 个知识库技能（init / refine / archive / verify / writer）|
| cr-frontend | 五项能力迭代：HITL 修复确认（FE-788）、SSR 安全规则（FE-1042）、SEO 评估合并、AB 实验清理评估、防御性埋点契约守护（FE-896）|
| 个人 harness-kit | 6 技能家族（dev / spec / plan / coding / testing / change）+ commands / playbooks / templates / workspaces；harness-data 注册 10 个仓库工作区与全局任务池；my-ai 161 commits（harness-kit 路径 25）|
| 团队采用 | marketplace 仓 33 次提交、5 位提交者：我 20、Bowen Xu 7、Zuo Wang 3、Ning Bei 2、Victor 1 |

**二、个人亮点贡献**

- 建立 visable-plugin-marketplace 统一分发仓，把散在各处的技能收敛为四插件四端可安装的团队资产，并产出使用指南向全团队推广
- 团队采用有提交记录实证：4 位同事共 13 次提交，资产从「只有我在用」变成「团队共同维护」
- cr-frontend 代码评审技能由我搭建并迭代五项能力，覆盖埋点契约、SSR 安全、SEO 与 AB 实验清理等团队高频回归面
- 把 Cursor Rules 升级为 Team AI Rules 单一源，消除多端规则漂移，marketplace 统一分发
- 承担 supplier 域 6 仓 repoWiki 初始化与 product-editor schema v2 重建，为规则与技能提供知识内容源
- harness-kit 沉淀跨仓交付方法论，cross-repo-rollout playbook 从 CTOOL-634（5 仓一次打通）与 CTOOL-679（六应用统一升级）两个真实项目提炼

注（review 答辩用）：

- **版本号以 manifest 为准**：marketplace README 插件表仍写 visable-fe-domain-agents 0.4.2，manifest 实际 0.5.0，建议先修 README
- **repoWiki 计数勿混用**：本地实测 13 个前端仓有 repoWiki（含同事用同一套技能产出的仓），我的承担口径是 7 仓，对外只写 7 仓
- **缺采用率数据**：安装人数、在用仓库数、AI 归因占比是「推广」最有力的量化项，原 AI Lines 80% 已因无口径删除，建议改从 Qoder / Cursor 面板取；目前只有提交者维度可量化
- **harness-kit 是个人工具**：仅本人使用、无同事试用记录，不写「团队级」；团队级资产以 marketplace 为准（与 O1-KR4 注一致）
- 与 O1-KR4 边界：那边只写「用 harness 跨仓方式承接业务需求」的实践验证，工具建设与资产沉淀归本 KR，不重复归因

---

## O3【稳定性】保障前端全域应用稳定性，完善监控告警与应急响应体系，确保持续零 P0/P1 故障

### KR1【监控全覆盖】深化前端稳定性 SDK 集成，打通 ODPS 数据链路，基于 Sunfire 建立日志驱动告警体系。实现前端应用监控 100% 覆盖，支持白屏、API 错误及自定义核心指标的实时告警

**结果：前端监控从「3 个项目有告警」推进到全域覆盖——项目级 Sunfire 30%→100%、Datadog 56%→100%，告警条目级 26/105（25%）→105/105（100%）；api_error / script_error 从零告警到全覆盖；Buyer 侧 8 站点组合 + 5 国站点、Supplier 侧 6 应用全部接入稳定性 SDK，ODPS 数据链路打通至 Sunfire**

**一、KR 结果**

**① SDK 集成覆盖**

| 范围 | 内容 | Jira |
|---|---|---|
| Buyer 侧主站 | 8 站点组合全量推全（ep/de·fr·tr·it·es + wlw/ch·at·de） | FE-849~852 |
| Buyer 侧多国站点 | pt / dk / pl / nl / uk 监控接入 | FE-789 |
| Supplier 侧 | 6 应用补齐 Sentry + 稳定性 SDK + Web Vitals；治理前 5/6 缺 SDK，治理后全部达 product-editor 基线 | FE-1028（子票 FE-1029~1034） |
| SDK 版本升级 | core 2.2.0→2.4.0、server 2.1.0→2.2.0、vue 2.0.0→2.0.3；3 仓 PR（search#483 / homepage#230 / unified-search#1588）09-02 合并 | FE-1045 |

Supplier 侧 6 应用 PR：product-editor#97、business-insights#319、supplier-onboarding#585、ad-center#77、customer-dashboard#32、visitors#243；配套 IaC：ad-center-iac#7、business-insights-iac#11（Sentry）、visitors-iac#21。

**② ODPS 数据链路**

SDK → `POST /web/metrics` → `icbu_de.s_tt_v_web_metrics_tt4`（原始表）→ ETL → `icbu_de.visable_fe_full_monitoring_data_v1`（宽表）→ Sunfire SPM。覆盖 6 类 event_type：white_screen / ssr_error / custom_error / component_error / api_error / script_error，全部可查可告警。

**③ 告警体系与覆盖率**

| 维度 | 补全前 | 补全后 |
|---|---|---|
| Sunfire 项目级覆盖（至少 1 条活跃告警） | 3/10 = 30% | 10/10 = 100% |
| Datadog 项目级覆盖 | 5/9 = 56% | 9/9 = 100% |
| Sunfire 告警条目（6 类 × 10 项目） | 12/60 = 20% | 60/60 = 100% |
| Datadog 告警条目（5 条 × 9 项目） | 14/45 = 31% | 45/45 = 100% |
| **合计** | **26/105 = 25%** | **105/105 = 100%** |

- Sunfire 日志驱动告警体系：6 个共享 SPM 监控项（FE-Api-Error `6_spm_10357`、FE-Script-Error `10359`、FE-Component-Error `10360`、FE-Custom-Error `10361`、FE-Ssr-Error `10362`、FE-White-Screen `10363`）+ 每项目一条 `AppName` label 选择器规则 + 规则级钉钉订阅；另有 Supplier Domain 聚合规则覆盖 4 个长尾应用。治理前仅 3 项目 × 4 类 = 12 项监控 / 12 条规则
- Datadog 统一模板：homepage 5-monitor 标准（Memory / CPU / p75 / Server Errors / Status:error），落成 44 条导入 JSON 覆盖 9 项目 + supplier 域聚合，统一 `env:production` / `team:vcn-frontend` / 钉钉通知口径
- 极端场景补强：新增 12 条 Sunfire 绝对量规则 + Datadog E1~E4 分级
- 盲区消除：product-editor Datadog 0 条 → 5 条（原为最大盲区）
- 两阶段收官：FE-1067 核心 7 应用（09-11）、FE-1068 supplier 4 应用（09-18），归属 Epic FE-1066

**二、个人亮点贡献**

**① 全域基线审计是这轮治理的起点，把"覆盖了多少"从主观感受变成数字台账**

2026-08-26 独立完成 Sunfire / Datadog / Sentry 三平台逐项盘点，产出 `V-Frontend-Monitor-告警能力清单.md`：Sunfire 仅 3 项目 12 项监控、Sentry 12 个前端项目只有 6 个配了告警（共 6 条、其中 1 条处于 Snooze）、Datadog 55+ 条但 product-editor 为 0。审计同时暴露 api_error / script_error 全域无任何告警。没有这份底账，后面的补全计划无从排序、也无法量化"完成"。

**② 主导确立两套告警标准口径，成为后续所有项目建告警的复用模板**

Sunfire = 共享项 + 按项目规则（`AppName` label 选择器），Datadog = homepage 5-monitor 模板；并拍板将 SSR 渲染错误从 Datadog 标准剔除、改由 Sunfire 共享项 `FE-Ssr-Error` 承接，避免两平台重复告警。口径确定后批量复制，不再逐应用各设计一套。

**③ 用 sunfire-cli 打通 API 化建告警链路，并实测排除两个平台级陷阱**

一是 API 创建的 AppName 白名单专项监控项不产数据（10355 / 10356 三小时零序列，spec 落库完好、effect=true），据此确立"新建告警一律走共享模式"的约定；二是 API create 会自动注入 `tenant:"default"` 导致控制台编辑器不渲染评估视图，create 后需 update 去除。两个陷阱都不可从平台文档推导，踩过一次即沉淀为团队约定。

**④ 把补全工作做成可交接的工程产物，而非一次性动作**

`monitoring-alert-补全计划.md`（S-xx / D-xx / R-xx 编号）+ `projects-management/monitor-alert/ROADMAP.md` v1.2 + drawio 可视化，与 Jira FE-1066/1067/1068 双向对齐；44 条 Datadog 导入 JSON 统一通知与 tags 口径，可直接控制台导入。任何人可按编号接续执行。

注（review 答辩用）：

- **100% 为补全计划的口径与目标值，线上实际落地状态需 review 前核实**：截至 2026-09-07 的记录是 Sunfire api/script 规则已由本人在控制台重建为结构化模式（含各项目阈值按实际事件量调整：api 类 unified/search 1000、user 800、homepage 600、conversations 500、requests 400、product-editor 350），Datadog 44 条 JSON 中 conversations 4 条已导入（IDs 319703865 / 319704618 / 319705272 / 319705981，且用旧配置待逐条更新），其余尚未导入。若被问"是否真的 100%"，答"计划口径已 100% 排布，Sunfire 侧规则已在控制台建齐，Datadog 侧导入进度以平台现状为准"
- Sunfire SSR 规则曾由 API 创建 8 条（220240125~133）后按要求全部删除，改由本人在控制台以结构化模式重建；共享项 `FE-Ssr-Error`（6_spm_10362）保留且数据在产
- 覆盖率分母口径：Sunfire 10 项目含 09-04 增补的 user-frontend（不在 08-26 基线审计内，其 Datadog 已有 3 条 ECS 容器全灭 P1 告警，不属标准 5 条模板故条目级计 0/5、项目级计已覆盖）
- 新建总数口径：Sunfire 48 条 + Datadog 30 条 = 78 条（09-07 定版），与"补全后 105 条"的差异是 105 含存量 26 条
- 数据源：`knowledge-base/monitoring-alert-补全计划.md` §4.1、`knowledge-base/V-Frontend-Monitor-告警能力清单.md`（查询时间 2026-08-26）、`knowledge-base/monitor-configs/`（44 个 JSON）、`knowledge-base/extreme-scenario-alert-config.md`（08-28）
- 与 O2 的边界：Monitoring Agent 巡检能力、需求级覆盖度诊断归 O2-KR1 / KR2，本 KR 只写告警体系与 SDK / ODPS 链路建设，不重复归因

### KR2【监控误报治理】主导稳定性监控误报专项治理，识别并消除 SDK 已知误报源，提升告警可信度

**结果：定位并消除 3 类 SDK 误报源，4 个 PR 合入 frontend-monitoring（#47 / #48 / #49 / #50）；清理 3 条失效告警并确立 script_error 同比降噪口径；治理路径为修 SDK 源码而非调阈值压噪音**

**一、KR 结果**

**① 消除的 SDK 误报源**

| 误报源 | 治理动作 | 落地 |
|---|---|---|
| 页面导航中断的 fetch 被记为 api_error | ApiMonitor 跳过导航中断请求 | FE-1037（Done 08-25）→ frontend-monitoring PR #48（310c413f，08-26） |
| 第三方资源与 API 噪音 | SDK 内置忽略列表 | PR #47（c915b2a2，08-18） |
| api_slow 低价值高频上报 | slow check 默认关闭（`enableSlowCheck:false`） | PR #49 / #50（08-27） |

**② 告警噪音清理**

- 停用 unified-search legacy email 告警 3 条（12236842 / 62945068 / 67123179）：收件人已非值班，其中两条正处 Alert 状态无人处理
- 识别 search p75 告警（233667687）阈值 1.2s 贴近常态值、正在持续产生噪声，纳入阈值调整清单
- 确立 `script_error` 用同比（`compareShiftDuration:"1w"`）而非环比 5min 的降噪口径，其余事件类型用环比
- HubSpot 脚本误报过滤 FE-1019 已立项（Backlog，尚未交付）

**③ 线上异常调查**

CloudFront 错误激增调查（2026-08-24）：通过流量构成分析定位为爬虫流量噪音、非 CDN 故障，排除一次误升级，产出报告（Confluence 501711004，08-25）。

**④ 告警有效性反证（该报的照样报得出来）**

- search white_screen 30 天内最大的 5 个告警窗口全部落在 2026-08-07 08:00–08:30（123 / 117 / 114 / 108 / 101 次），对应一次真实事故
- 08-25 search-frontend Sentry 回归事故当天 Datadog 日志 39,642 条 vs 正常日约 1,100 条（35 倍），被告警链路完整捕获

**二、个人亮点贡献**

**① 治理路径的选择：修 SDK 而不是调阈值**

面对噪音有两条路——调高阈值把告警压下去，或回到 SDK 源码修掉误报源。选了后者：代价是要通读 SDK 实现、跨仓库提 PR 并推动发版，但结果是信号本身变干净，阈值不必为了迁就噪音而失真。三类误报源（导航中断 fetch、第三方资源、api_slow）全部在 SDK 层解决，所有接入应用一次性受益，无需各自加过滤配置。

**② 建立"真实事故 vs 噪音"的判别方法**

CloudFront 错误激增当时表征与 CDN 故障一致，靠流量构成分析定位为爬虫，避免了跨团队拉动与无谓的应急响应。方法沉淀成报告，后续同类"错误量突增"先走这套判别再决定是否升级。

**③ 用告警数据反向验证治理成效，而不是只说"噪音少了"**

信噪比两侧都留了证据：一侧是误报源被消除（3 类 + 4 个 PR），另一侧是 white_screen 告警窗口与真实事故时间逐点对齐、Sentry 回归的 35 倍日志量被完整捕获——证明降噪没有以降低灵敏度为代价。

注（review 答辩用）：

- **本 KR 无可用的量化降噪数字**：修订稿已明确「错误总量下降 XX%」口径未定，H2 以 ODPS 稳定性数据环比口径回收。此处只写"消除了哪几类误报源"的定性清单，不补百分比
- FE-1019（HubSpot 脚本误报过滤）状态为 Backlog，属已立项未交付，不计入本期成果
- ④ 的两组数字用于证明告警有效性，不是误报治理的直接产出，答辩时勿混为"治理带来的收益"
- 阈值调整清单（search p75 等）为识别与建议状态，实际调整由本人在 Sunfire 控制台按事件量执行，未逐条留档
- 数据源：`knowledge-base/extreme-scenario-alert-config.md` §2.1 / §5（08-28）、frontend-monitoring 仓库 commit c915b2a2 / 310c413f、Confluence 501711004

### KR3【Supplier 域交接】完成 supplier 前端域知识转移与技术治理盘点，产出项目整合方案与技术重构立项，落地核心技术债务改造工作，确保无线上故障

**结果：VEU→VCN 交接零断点完成（11 篇 Confluence 文档 + 14 项 In-Flight 清单 + 6 应用 repoWiki 全量初始化），并从"接手"推进到"整合方案 + 重构立项 + 首批技术债落地"——6→2-3 应用整合方案分 4 步、FE-1062 重构 Epic 立项、FE-1063 / FE-1064 两项技术债已合并主干（净删 1,997 行死代码）**

**一、KR 结果**

**① 知识转移（11 篇 Confluence，2026-07-28 ~ 09-11）**

| 文档 | 日期 | 页面 |
|---|---|---|
| Supplier 前端工程改造细节（repoWiki / 稳定性盘点） | 07-28 | 388825102 |
| Supplier FE projects - routes（6 应用 19 条路由汇总） | 07-29 | 339247137 |
| Supplier 各项目路由与接口调用分析（BFF vs 同源相对路径） | 07-29 | 391905420 |
| Supplier KT Question list | 08-03 | 389611530 |
| Supplier FE projects - init.sh（本地调试通用流程） | 08-05 | 367230981 |
| Supplier 前端技术改造必要性盘点 | 08-06 | 389218306 |
| Supplier Frontend In-Flight Projects Inventory（14 项） | 08-10 | 387776637 |
| Supplier 前端项目整合方案（6 → 2-3 个应用） | 08-12 | 412254213 |
| VEU Handover / Knowledge Transfer（VEU → VCN） | 08-13 | 393248769 |
| 稳定性现状总览（治理后全量"完整"） | 09-04 | 402587654 |
| Supplier 前端改造清单（P0 / P1 / P2，持续更新） | 09-11 | 447250564 |

**② 方案产出与立项**

- 项目整合方案：6 个应用整合为 2-3 个，分 4 步推进（412254213，08-12）
- 技术重构 Epic 立项：FE-1062 Supplier Domain Technical Refactoring（09-03）
- 改造清单分级：P0 / P1 / P2 三档，持续更新（447250564）
- repoWiki 6/6 supplier 应用初始化完成：product-editor#94、business-insights#317、visitors#242、supplier-onboarding#584、customer-dashboard#31、ad-center#76

**③ 首批核心技术债务改造落地（已合并主干）**

| 项目 | Jira / PR | 结果 |
|---|---|---|
| CI 门禁接入 | FE-1063 / customer-dashboard#36（09-09 合并） | lint / typecheck / build 进入 CI 强制卡口 |
| 死代码清理 | FE-1064 / customer-dashboard#37（09-09 合并） | 16 files +7/−1,997；~1,700 行死代码 + 4 个 unused deps 移除；eslint warnings 5→2；`harness validate --strict` 全绿（含 production build） |

**④ 存量稳定性风险定位（诊断已交付，修复待执行）**

- business-insights 线上内存泄漏：九轮压测定位，task 死亡阈值收敛至约 350 个累计成功请求；prod 09-08~09-12 共 10 次 task 重启、版本全为 287、期间零发布；根因锁定为 monitoring SDK（每请求 app 实例化）× Nuxt 3.19.2 SSR 层 × vue 3.5.2x 的交互，正解为升级 nuxt 4.4.4（对齐 product-editor `ce8bd419` #75 已生产验证 4 个月无泄漏的修复），短期止血方案为回滚 287 摘除 SDK
- visitors-frontend SSR 内存泄漏与自引用 fetch 递归：PR #245（09-09 提出，Open）

**二、个人亮点贡献**

**① 8 月新增的组织职责，一个人把交接做完且无断点**

11 篇文档覆盖路由、接口调用形态、本地调试、稳定性现状、在途项目、改造必要性六个维度，加上 14 项 In-Flight 项目清单与监控告警交接。团队后续可直接按文档上手 6 个此前完全陌生的仓库，不需要再找原团队问。

**② 没有停在"接手"，而是把交接变成治理起点**

主动产出 6→2-3 应用的整合方案（分 4 步）与 P0/P1/P2 改造清单，推动 FE-1062 重构 Epic 立项。这是从"维护别人的代码"到"决定这些代码该长成什么样"的转变——盘点发现的问题不止记录下来，而是形成了有优先级的改造路线并进入 Jira 立项流程。

**③ 方案自己先跑通第一批，用可验证的落地证明不是纸面规划**

FE-1063 CI 门禁 + FE-1064 死代码清理均由本人实现并合并主干：净删 1,997 行、零行为变更、门禁全绿、每一项删除前对树复验无存活引用。整合方案的第一批可执行性由此得到证明。

**④ 内存泄漏排查是本期技术含量最高的一次独立定位**

现象只有"容器内存每天爬满后重启"，延迟曲线死前完全平稳、外部不可观测。自研零依赖压测工具（恒压 / 爬坡 / 开环限速三种模式），九轮压测把模糊现象钉成约 350 req/task 的确定性阈值，并证明死亡与并发、速率无关、纯累计请求驱动（1 rps 温和流量下同样死在 353 请求，可精确预测到分钟）；再做 BI（漏）/ SO（无 SDK，不漏）/ PE（已修复，不漏）三方对照，从 product-editor 历史 commit 找到已生产验证的修复路径。结论交付到可直接决策的程度：正解 + 止血方案 + prod 寿命模型自洽验算（0.1-0.3 req/min ÷ 350 req ≈ 19-58h，与观测约 22h 吻合）。

**⑤ 供应商域 repoWiki 全部 7 仓由本人承担、无欠账**

同时支撑部门 O2-KR1「RepoWiki 标准定稿 + 全应用初始化（Q1）」的 90% 进度。

注（review 答辩用）：

- **"确保无线上故障"这一句需先定级再落笔**：business-insights prod 自 09-08 起有每天一轮的 OOM task 重启（09-08~09-12 共 10 次），仓库内无 P0/P1 故障台账可引用。若该事件在团队定级中不算 P0/P1，可保留原句；否则建议把结果口径改为"识别并定位存量稳定性风险"，把内存泄漏作为主动发现成果而非故障
- ④ 的交付物是诊断结论与修复路径，**修复本身未落地**（nuxt 4.4.4 升级未执行、visitors#245 仍 Open），不写成"已解决"
- 根因结论为三方对照 + 版本线数据包推导出的模型（3.5.21=170-370 req/死、3.5.33≈3.5.42=1015-1017 req/死、PE nuxt4.4.4+3.5.34=4 个月干净），未经内存探针直接取证；答辩若被追问，说明"模型可解释全部观测数据点，直接取证需在 staging 补部署 NODE_OPTIONS 快照开关后进行"
- CTOOL-679 的 8 PR / 六仓组件库 pin 升级不在此重复计入，归 O1-KR4；本 KR 只写交接、治理盘点与技术债改造
- 整合方案（6→2-3 应用）为方案产出，尚未进入执行；FE-1062 状态为 Backlog（已立项未开工），不写成"重构已完成"
- 数据源：`半年总结-2026H1/data/confluence-pages.md` §七、`harness-data/tasks/FE-1064-remove-dead-code/result.md`、`harness-data/tasks/CTOOL-679-*/`、`.scratch/memleak-stress/`（stress.js + 九轮 JSONL 日志，2026-09-12 ~ 09-23）
