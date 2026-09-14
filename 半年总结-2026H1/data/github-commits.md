# GitHub 提交记录（2026-03-30 ~ 2026-09-30）

- 作者：junyang-visable（Jun Yang）
- 统计：**236 commits** = visable-dev org **132** + 个人仓库 my-ai **104**
- 说明：GitHub Commits API 仅覆盖**默认分支**，squash 合并的 PR 计为 1 条提交；完整工作面以 `github-prs.md`（130 PR）为准
- org 提交月度分布：4月 20 · 5月 25 · 6月 32 · 7月 24 · 8月 25 · 9月 6
- 采集方式：REST API `repos/{repo}/commits?author=junyang-visable&since=2026-03-30&until=2026-10-01`，按 PR 涉及的 27 个仓库逐一抓取

## visable-dev org 提交（132，按仓库）

### frontend-monitoring（10）

| 日期 | SHA | 说明 |
|---|---|---|
| 04-02 | 20d795e5 | Release 2.0.1：pageId handling in reporting (#43) |
| 04-02 | 901c206a | Refactor server error reporting to unify API with client SDK (#44) |
| 04-10 | 3dfe12c7 | Feature/report data rebuild (#45) |
| 04-15 | 3956763e | Release 2.2.0：white screen detection (#46) |
| 08-18 | c915b2a2 | built-in error ignore lists for third-party noise (#47) |
| 08-21 | cb02390d | ci: pin pnpm 10 in npm_publish |
| 08-21 | 86673099 | bump monitoring-core to 2.3.1 |
| 08-26 | 310c413f | skip fetch requests aborted by page navigation (FE-1037) (#48) |
| 08-27 | 7c0267c5 | disable slow check by default (#49) |
| 08-27 | d14a419b | disable slow check by default (#50) |

### product-editor-frontend（14）

| 日期 | SHA | 说明 |
|---|---|---|
| 04-01 | c41f6c88 | Refactor custom report context in monitoring client plugin (#59) |
| 04-02 | 6d84b827 | fully roll out AB test (#60) |
| 04-08 | 70f149fd | Feat/monitor 2.0 (#61) |
| 04-13 | cd4bba29 | PR template (#62) |
| 04-13 | 60271775 | PR template (#64) |
| 04-14 | 766090f8 | monitoring 2.1.0 (#65) |
| 04-15 | a1333890 | monitoring-core 2.2.0 (#67) |
| 05-07 | 48d1d7d7 | handle 403 in membership data fetch (#73) |
| 05-12 | 818f3ecd | Product edit ga4 (#77) |
| 06-11 | 3ae887a2 | vue 43.37.0 (#84) |
| 06-24 | 4bb67852 | initialize knowledge base (#88) |
| 08-20 | 81948852 | remove quick-editor AB, free wlwTestGroup7 (#95) |
| 08-21 | 7781bfdb | repoWiki rebuild on schema v2 (#94) |
| 08-27 | f8131653 | FE-1029 remove Sentry reporter + upgrade (#97) |

### search-frontend（10）

| 日期 | SHA | 说明 |
|---|---|---|
| 04-08 | 6047f696 | Feat/monitor 2.0 (#360) |
| 04-13 | 4dc93ec0 | PR template (#367) |
| 04-14 | 5529087a | monitoring 2.1.0 (#368) |
| 04-15 | 1eb70610 | monitoring-core 2.2.0 (#372) |
| 05-14 | 51cb8450 | virtual page context fix in monitoring server plugin (#391) |
| 06-10 | 9bdd0f64 | FE-789 monitoring for pt/dk/pl/nl/uk (#416) |
| 06-23 | fd6e45e2 | Stability SDK ep/de, ep/fr, wlw/ch (#434) |
| 07-02 | d04361ec | FE-851 ep/tr, ep/it, wlw/at (#450) |
| 07-08 | ead2c0b4 | FE-852 ep/es, wlw/de (#454) |
| 09-02 | 8130ad37 | FE-1045 stability SDK upgrade (#483) |

### v-ai-platform（20）

| 日期 | SHA | 说明 |
|---|---|---|
| 06-15 | d1d19c16 | init react project with vite |
| 06-15 | 301cee99 | Docker image + Visable CI workflows |
| 06-15 | 70dad3d2 | update configuration and workflows |
| 06-15 | 100d326c | trigger push pipeline on main |
| 06-15 | 63ff57ab | fix visable.yaml quotes |
| 06-15 | fdc85c95 | prettierignore (#1) |
| 06-16 | c641895f | antd UI library (#2) |
| 06-18 | b554caf9 | routing scaffold, global nav, market page (#3) |
| 06-24 | 3747513a | FE-837 open market homepage (#4) |
| 06-24 | 789cb44e | staging/production deploy workflows (#5) |
| 06-24 | b02bd671 | FE-862 deployment (#6) |
| 06-26 | 9b474feb | FE-839 asset detail page (#7) |
| 06-26 | a79b2445 | fix deploy issue (#8) |
| 06-29 | ffcbdef2 | migrate to Nuxt 4 (#9) |
| 06-30 | 1bf57388 | repoWiki sync to Nuxt 4 (#11) |
| 07-01 | 900743fb | FE-840 publish asset flows (#12) |
| 07-23 | bc89968b | QA platform entry (#16) |
| 07-23 | cd451eba | QA platform (#18) |
| 07-24 | d1ad9509 | QA platform backend APIs (#20) |

（注：上表 19 条，另 1 条为 06-24 部署修复相关，明细见原始数据。）

### v-agent-hub-bamboo（18）

| 日期 | SHA | 说明 |
|---|---|---|
| 05-06 | b9090625 | Feature/accio plugin (#1) |
| 05-08 | 9716e51d | update plugin for clarity |
| 05-08 | 15055e48 | update skill IDs in recommend.json |
| 05-08 | 358d34e1 | supplier skill documentation |
| 05-08 | c6fe975d | supplier management flow docs |
| 05-08 | 64173a9d | product terminology update |
| 05-08 | 88338cf3 | Business Insights / Store Profile skills docs |
| 05-09 | a46d44ec | Feature/accio plugin update (#2) |
| 05-09 | 643476ce | disable Visable OAuth in connectors.json |
| 05-09 | 486ca599 | update data server URL |
| 05-09 | 991e8026 | remove Visable OAuth config |
| 05-09 | 0b669bda | supplier ID handling docs |
| 05-09 | f18e58ac | local data server URL fix |
| 05-12 | 031a0053 | add plugin ID to visable-assistant |
| 05-13 | 1ada4dee | Feature/plugin memory (#3) |
| 06-16 | e9bd7244 | memory policy guidelines (#20) |
| 06-26 | 906bfd0a | streamline plugin.json + logo (#33) |

（注：上表 17 条，另 1 条为 05-08 文档更新。）

### visable-plugin-marketplace（13）

| 日期 | SHA | 说明 |
|---|---|---|
| 07-03 | 23fd6652 | initialize marketplace with visable-fe-ai plugin |
| 07-03 | 5378ccd2 | move plugins into plugins/ |
| 07-03 | e780ece1 | remove standalone md files |
| 07-03 | 999b9237 | simplify root README |
| 07-06 | 970e60c9 | remove fe-stability skills |
| 07-06 | 9180edcb | docs: remove fe-stability references |
| 07-07 | ee1e31f5 | bump version 0.3.0 |
| 07-07 | e1128bab | fix repository URL (#1) |
| 07-09 | 00927834 | sync cr-frontend skill (#2) |
| 08-10 | b76a0246 | merge cr-seo into cr-frontend (#9) |
| 08-10 | 4cb93da4 | Qoder marketplace support (#10) |
| 08-17 | ba5214c5 | AB experiment cleanup assessment (#11) |
| 09-01 | 5f702534 | SSR-safety rules (FE-1042) (#12) |

### my-ai 以外的其他 org 仓库（合计 30）

| 仓库 | 日期 | SHA | 说明 |
|---|---|---|---|
| ad-center-frontend | 08-21 | 0117d895 | repoWiki init (#76) |
| ad-center-frontend | 08-28 | ab46c34e | stability + web vitals SDKs (#77) |
| ad-center-frontend-iac | 08-28 | 1f3269f3 | NUXT_PUBLIC_STAGE (#7) |
| business-insights-frontend | 08-21 | 552cb113 | repoWiki init (#317) |
| business-insights-frontend | 08-28 | 3f3fea18 | Sentry + stability SDK (#319) |
| business-insights-frontend-iac | 08-28 | bfab79e6 | Sentry integration (#11) |
| customer-dashboard-frontend | 05-14 | 5e78af7b | GA4 migration (#22) |
| customer-dashboard-frontend | 08-21 | 53b798ea | repoWiki init (#31) |
| customer-dashboard-frontend | 08-27 | 7fca8b1c | stability SDK + web vitals (#32) |
| customer-dashboard-frontend | 09-09 | b9813397 | lint/typecheck gates (#36) |
| customer-dashboard-frontend | 09-09 | 2460acd2 | dead code removal FE-1064 (#37) |
| homepage-frontend | 04-08 | e11db117 | monitor 2.0 (#158) |
| homepage-frontend | 04-13 | 2aa36ba6 | PR template (#163) |
| homepage-frontend | 04-14 | 512f78ac | monitoring 2.1.0 (#165) |
| homepage-frontend | 04-15 | b70d9dd8 | monitoring-core 2.2.0 (#166) |
| homepage-frontend | 09-02 | c92446f1 | FE-1045 SDK upgrade (#230) |
| manage_github | 06-12 | 6bbcc620 | add v-ai-platform repos (#998) |
| manage_github | 07-03 | bbc8f7ab | marketplace repo config (#1047) |
| product-editor-frontend-iac | — | — | （PR #6 open，未合并） |
| supplier-backend-mcp-service | 05-07 | a3715215 | README + MCP tool registration (#2) |
| supplier-backend-mcp-service | 05-07 | a6313d9d | fix accio tool (#4) |
| supplier-backend-mcp-service | 05-13 | a4e76f1b | rename getCompanyById |
| supplier-onboarding-frontend | 05-15 | e26b25c2 | GA4 migration (#567) |
| supplier-onboarding-frontend | 08-21 | 79ba13ac | repoWiki init (#584) |
| supplier-onboarding-frontend | 08-27 | 410342d3 | FE-1031 stability + web vitals (#585) |
| unified-search-frontend | 09-02 | 0beacb05 | FE-1045 SDK upgrade (#1588) |
| user-frontend | 05-22 | 1fd6119f | FE-761 GA4 migration (#204) |
| user-frontend | 07-09 | c0ed6593 | GA4 user (#217) |
| user-frontend | 07-14 | fa7b0b57 | refactor user session management (#222) |
| v-ai-frontend | 04-21 | 2227626c | Feature/cr frontend (#7) |
| v-ai-frontend | 06-09 | 8e44bb6a | FE-788 HITL fix (#12) |
| v-ai-frontend | 07-02 | 8d44c228 | Team AI Rules SSOT (#19) |
| v-ai-frontend | 07-02 | 8f070f88 | fe stability report (#20) |
| v-ai-frontend | 07-02 | 23ba7f44 | skills symlink (#21) |
| v-ai-frontend | 07-02 | addf0e7b | plugin content update (#22) |
| v-ai-frontend | 07-08 | af0d0faa | remove plugins dir (#25) |
| v-ai-frontend | 07-14 | faffbfb1 | fe stability scope (#30) |
| v-ai-platform-iac | 06-15 | 45a6e69c | initial IaC scaffolding |
| v-ai-platform-iac | 06-15 | 7cfb7676 | default_tags Team=bamboo (#1) |
| v-ai-platform-iac | 06-23 | 2b8ffd37 | enable production env (#2) |
| v-ai-platform-iac | 06-24 | 8e63c362 | datadog_log_source → javascript (#3) |
| v-ai-platform-iac | 06-24 | 18510b2b | Fargate deployment config |
| v-ai-platform-iac | 06-24 | 0082ee0b | revert Fargate config |
| v-ai-platform-iac | 06-25 | 784fe879 | fix deploy issue (#4) |
| v-ai-platform-iac | 06-25 | b7ead653 | revert fix (#5) |
| v-ai-platform-iac | 06-25 | a9f5aac3 | health check paths (#6) |
| visable-vue | — | — | （PR #737 open，未合并） |
| visitors-frontend | 08-21 | 41d4cd5b | repoWiki init (#242) |
| visitors-frontend | 08-28 | 9be0adfc | stability + Web Vitals SDKs (#243) |
| visitors-frontend-iac | 08-28 | 412955eb | NUXT_PUBLIC_STAGE (#21) |
| wlw_nginx | — | — | （PR #586 open，未合并） |

（注：routing-lib、web_analytics_maintenance 有 PR 但默认分支无本人署名提交。）

## my-ai 个人仓库提交（104，按月）

### 2026-04（10）— 前端 AI 编码标准体系

- f8306901（04-21）frontend AI coding standards design spec
- 40990e4d（04-22）AI coding standards implementation plan
- fa4ac583（04-22）Cursor configuration standards for Vue/Nuxt
- f02a9fa3（04-22）RepoWiki frontend templates (7 templates)
- 8c5e641f（04-22）SDD standards and OpenSpecs frontend guide
- e5d82ddc（04-22）frontend AI code review checklist
- 0b9da394（04-22）frontend Prompt template library (6 templates)
- 484ceac3（04-22）internal playbook README
- 5f98c283（04-22）whitepaper draft and top-level README
- bf990320（04-22）README links + complete AI coding standards

### 2026-05（34）— AI 协作标准完善 + Visable Assistant 插件

- ce9cc3a6 ~ d0c86240（05-05，8 条）：AI standards 扫描/阅读阶段更新、API/业务知识/测试模板、SDD flow 图、AI 协作标准、init-ai-standards skill、cursor rules、GA4 validation skill 文档
- 44ea16a5 ~ 099681a9（05-06，22 条）：visable-assistant 插件全套（design spec、implementation plan、plugin.json、connectors/dependencies、resources、agent.json、identity/soul/bootstrap/user/agents.md、三个 skill 脚手架、记忆管理、skill 重命名、数据查询 skill 改名等）
- 68a169b8 / 8f6a7d15（05-11，2 条）：AI 白皮书与统一知识库结构
- f56ddd6a / 36e82b7e（05-14，2 条）：RepoWiki 术语统一与 Plugin 概念

### 2026-06（4）— Jira 工作汇总技能

- 580286af / c9559d2e / a9f8ed3b / c04dd40a（06-25）：jira-work-summary skill（change-event 统计）、排他日期边界修复、status+worklog 聚焦、RepoWiki 章节

### 2026-07（6）— GA4 校验技能与整理

- a138dacb / 94f769e0 / 00ef1e6f / b9f94283 / 121011d5（07-16）：GA4 tracking validation skill、移除 init-ai-standards、模板路径修复
- 161c9e1f（07-15）Merge PR #1（jira-work-summary skill）

### 2026-08（23）— harness-kit 工程化 + drawio 技能 + 监控规划

- 342b3105 / ab1c0372 / ed854887 / 85e19ae6（08-25）：harness-kit 雏形（reusable coding/testing harness、个人 toolkit、6-skill family、表格格式化）
- 2e1bedc3（08-26）frontend monitoring alert capability catalog
- 0f8524fc（08-27）drawio-best-practice skill 加固
- 4676b900（08-28）Nexus project roadmap + drawio 可视化
- 5493b6a7（08-28）Sentry 表状态列重构
- ed648dbc（08-28）harness-dev 强制 feature branch
- ade47e7f（08-28）skill-enhancement 路由本地 YAML 配置
- 653cb986（08-28）移除 jira-work-summary skill
- 3b877936（08-28）注册 monitoring-agent workspace
- 8605c1f2 / 8c748f68 / e1d2517e / 47ea8e96 / c13a262d / 9e0378d4（08-28）：harness 数据目录调整、英文重写、数据出库
- 186b91ef / fdb57993 / c3574fb5（08-31）：knowledge-base 集中化、doctor 修复、注册 search-frontend workspace

### 2026-09（27）— roadmap 可视化、全局任务池、报告技能

- 709b9ab1（09-01）roadmap v0.7：WhatsApp / AI Lead Enrichment / BV Process
- d624ca94（09-01）roadmap v0.9：stage 配色与时间轴
- 74121ad1（09-01）drawio-roadmap skill（含验证 harness）
- 4e487a22 / 5d1874f5 / 6b3564bc（09-01）格式化、告警完成计划、BV 窗口调整
- d230809b / d55fe77c（09-02）roadmap 文档归位、告警 v1.1
- be7e1c40 / 948fe4b6 / 1dbf8660 / 5ac3cf7d / 7d55d352（09-03）spec/plan 入库 docs/changes/、harness-data 拆分、注册 customer-dashboard workspace、plan 确认闸门
- fde5f915 / 0fa15bfd / f399a8f0（09-04）monitor 计划加 user-frontend、FE-1064 范围、roadmap v1.2
- 0fb01ff9 / c4444d8f（09-07）Datadog 标准模板（homepage 5-monitor）、注册 CTOOL-634 三个 workspace
- 1beeeec7（09-08）全前端应用 Datadog monitor 导入 JSON
- 6c36ecb4 / 9cecd40f / f48279e5 / 39538424 / 5a24bd50（09-09）CTOOL-634 msite 重构记录、task new 支持 ticket、全局任务池、gitignore、result.md 三段式模板
- 973a5ca6（09-10）CTOOL-634 BFF proxy round 记录
- bed63afd（09-12）executive-reporting skill
