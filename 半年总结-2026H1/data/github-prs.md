# GitHub PR 记录（2026-03-30 ~ 2026-09-30）

- 作者：junyang-visable（Jun Yang）
- 统计：PR 共 **130** 个，其中**已合并 101**（合并率 77.7%），覆盖 **27 个仓库**（visable-dev org 26 个 + 个人仓库 my-ai 1 个）
- 月度分布：3月 1 · 4月 23 · 5月 11 · 6月 28 · 7月 17 · 8月 29 · 9月 21
- 采集方式：GitHub Search API（`author:junyang-visable type:pr created:2026-03-30..2026-09-30`），采集时间 2026-09-12
- 状态说明：`merged`=已合并（标注合并日）；`open`=仍开启；`closed`=关闭未合并（多为同内容重复 PR，被后续版本替代）

## product-editor-frontend（20）

- #59（03-31，merged 04-01）Refactor custom report context handling in monitoring client plugin
- #60（04-01，merged 04-02）feat: fully roll out AB test
- #61（04-02，merged 04-08）Feat/monitor 2.0
- #62（04-10，merged 04-13）chore: Add pull request template
- #63（04-13，closed）monitoring-core/monitoring-server 2.1.0（重复，被 #65 替代）
- #64（04-13，merged 04-13）Chore/pr template
- #65（04-13，merged 04-14）monitoring-core/monitoring-server 2.1.0
- #67（04-15，merged 04-15）monitoring-core 2.2.0
- #72（05-06，closed）Handle 403 errors in membership store（被 #73 替代）
- #73（05-06，merged 05-07）feat: handle 403 error in membership data fetch
- #77（05-12，merged 05-12）Product edit ga4
- #83（06-11，closed）vue 43.37.0（被 #84 替代）
- #84（06-11，merged 06-11）Update @visable-dev/vue to 43.37.0
- #88（06-23，merged 06-24）Chore/initialize knowledge base
- #94（08-12，merged 08-21）docs(repoWiki): rebuild knowledge base from scratch on schema v2
- #95（08-13，merged 08-20）remove unused quick-editor AB experiment to free wlwTestGroup7 bucket
- #96（08-21，closed）initialize repoWiki + upgrade monitoring SDK（被 #94/#97 替代）
- #97（08-24，merged 08-27）FE-1029: remove Sentry reporter from monitoring SDK and upgrade monitoring packages
- #100（09-08，closed）CTOOL-637 WhatsApp settings page（早期版本）
- #103（09-10，open）Ctool 637/whatsapp settings page

## v-ai-platform（15）

- #1（06-15，merged 06-15）chore: add prettierignore
- #2（06-16，merged 06-16）feat: add antd UI component library
- #3（06-18，merged 06-18）feat: app routing scaffold, global nav, and market page (Phase 1)
- #4（06-24，merged 06-24）FE-837 open market homepage
- #5（06-24，merged 06-24）feat: add staging and production deployment workflows
- #6（06-24，merged 06-24）Fe 862/deployment
- #7（06-26，merged 06-26）Fe 839 asset detail page
- #8（06-26，merged 06-26）Fix/deploy issue
- #9（06-29，merged 06-29）refactor: migrate v-ai-platform to Nuxt 4
- #10（06-29，closed）repoWiki sync（被 #11 替代）
- #11（06-29，merged 06-30）Sync repoWiki to Nuxt 4 migration
- #12（06-30，merged 07-01）FE-840 feat(publish): Publish Asset flows
- #16（07-23，merged 07-23）feat: initialize QA platform entry
- #18（07-23，merged 07-23）Feature/qa platform
- #20（07-24，merged 07-24）feat: integrate QA platform with backend APIs

## search-frontend（11）

- #360（04-02，merged 04-08）Feat/monitor 2.0
- #366（04-13，closed）monitoring 2.1.0（重复）
- #367（04-13，merged 04-13）chore: add pull request template
- #368（04-13，merged 04-14）monitoring-core/monitoring-server 2.1.0
- #372（04-15，merged 04-15）monitoring-core 2.2.0
- #391（05-14，merged 05-14）fix: update virtual page context handling in monitoring server plugin
- #416（06-09，merged 06-10）FE-789: enable monitoring for pt, dk, pl, nl, uk sites
- #434（06-23，merged 06-23）feat: enable Stability SDK for ep/de, ep/fr, and wlw/ch
- #450（07-01，merged 07-02）FE-851: enable Stability SDK for ep/tr, ep/it, and wlw/at
- #454（07-07，merged 07-08）Fe 852/stability sdk ep es wlw de
- #483（08-31，merged 09-02）chore(deps): upgrade stability SDK packages (FE-1045)

## v-ai-frontend（9）

- #7（04-15，merged 04-21）Feature/cr frontend
- #12（06-09，merged 06-09）Feat/fe 788 cr frontend hitl fix
- #19（07-01，merged 07-02）feat: Visable FE AI plugin — Team AI Rules SSOT
- #20（07-02，merged 07-02）Feat/fe stability report
- #21（07-02，merged 07-02）chore: replace plugins/skills with symlink to root skills/
- #22（07-02，merged 07-02）Chore/update plugin content and skills
- #23（07-07，closed）update plugin content and skills（被 #22 后续替代）
- #25（07-08，merged 07-08）chore: remove plugins directory
- #30（07-14，merged 07-14）Feat/fe stability scope

## frontend-monitoring（8）

- #43（04-02，merged 04-02）Release 2.0.1：pageId handling in reporting
- #44（04-02，merged 04-02）Refactor server error reporting to unify API with client SDK
- #45（04-10，merged 04-10）Feature/report data rebuild
- #46（04-15，merged 04-15）Release 2.2.0：white screen detection 改进
- #47（08-18，merged 08-18）feat: add built-in error ignore lists for third-party resource & API noise
- #48（08-26，merged 08-26）fix(core): skip fetch requests aborted by page navigation in ApiMonitor (FE-1037)
- #49（08-27，merged 08-27）Feature/disable slow check by default
- #50（08-27，merged 08-27）Feature/disable slow check by default

## customer-dashboard-frontend（7）

- #31（08-17，merged 08-21）chore: initialize repoWiki knowledge base
- #32（08-24，merged 08-27）feat: integrate stability SDK and web vitals reporting
- #35（09-03，closed）lint/typecheck gates（重复）
- #36（09-03，merged 09-09）chore(ci): add lint and typecheck gates to PR pipeline
- #37（09-03，merged 09-09）chore: remove dead code and unused dependencies [FE-1064]
- #38（09-11，closed）bump @visable-dev/vue 43.44.0-beta.2（重复）
- #39（09-11，open）chore: bump @visable-dev/vue to 43.44.0-beta.2

## visable-plugin-marketplace（6）

- #1（07-07，merged 07-07）chore: fix repository URL
- #2（07-09，merged 07-09）chore(cr-frontend): sync skill from v-ai-frontend
- #9（08-07，merged 08-10）Merge cr-seo into cr-frontend: SEO assessment, mandatory HITL, English translation
- #10（08-10，merged 08-10）feat: add Qoder plugin marketplace support
- #11（08-17，merged 08-17）feat(cr-frontend): add AB experiment cleanup assessment as Step 9
- #12（08-31，merged 09-01）feat(cr-frontend): add SSR-safety rules for client-only APIs (FE-1042)

## homepage-frontend（5）

- #158（04-02，merged 04-08）Feat/monitor 2.0
- #163（04-10，merged 04-13）chore: add pull request template
- #165（04-13，merged 04-14）monitoring 2.1.0
- #166（04-15，merged 04-15）monitoring-core 2.2.0
- #230（08-31，merged 09-02）chore(deps): upgrade stability SDK packages (FE-1045)

## supplier-onboarding-frontend（5）

- #567（05-12，merged 05-15）Pgs 134/ga4 migration
- #584（08-17，merged 08-21）docs: initialize repoWiki knowledge base
- #585（08-24，merged 08-27）FE-1031: Integrate stability monitoring and web vitals SDKs
- #588（09-11，closed）bump vue+routing（重复）
- #589（09-11，open）chore: bump @visable-dev/vue to 43.44.0-beta.2 and routing to 22.10.0-beta.1

## visitors-frontend（5）

- #242（08-17，merged 08-21）docs: initialize repoWiki knowledge base
- #243（08-24，merged 08-28）feat: integrate stability monitoring and Web Vitals SDKs
- #245（09-09，open）fix: stop SSR memory leak and self-referencing fetch recursion
- #246（09-11，closed）bump vue+routing（重复）
- #247（09-11，open）chore: bump @visable-dev/vue to 43.44.0-beta.2 and routing to 22.10.0-beta.1

## v-agent-hub-bamboo（5）

- #1（05-06，merged 05-06）Feature/accio plugin
- #2（05-09，merged 05-09）Feature/accio plugin update
- #3（05-13，merged 05-13）Feature/plugin memory
- #20（06-16，merged 06-16）Add memory policy guidelines to Visable Assistant prompt
- #33（06-26，merged 06-26）refactor: streamline plugin.json and update logo references

## v-ai-platform-iac（6）

- #1（06-15，merged 06-15）Set default_tags Team to bamboo
- #2（06-23，merged 06-23）Enable production environment in run_against config
- #3（06-24，merged 06-24）datadog_log_source nodejs → javascript
- #4（06-25，merged 06-25）Fix/deploy issue
- #5（06-25，merged 06-25）Revert "Fix/deploy issue"
- #6（06-25，merged 06-25）update health check paths

## business-insights-frontend（5）

- #317（08-13，merged 08-21）docs: initialize repoWiki knowledge base
- #318（08-21，closed）integrate Sentry（被 #319 替代）
- #319（08-21，merged 08-28）feat: integrate Sentry and stability monitoring SDK
- #322（09-11，closed）bump vue+routing（重复）
- #323（09-11，open）chore: bump @visable-dev/vue to 43.44.0-beta.2 and routing to 22.10.0-beta.1

## ad-center-frontend（4）

- #76（08-17，merged 08-21）docs: initialize repoWiki knowledge base
- #77（08-24，merged 08-28）feat: integrate stability monitoring and web vitals SDKs
- #78（09-11，closed）bump vue+routing（重复）
- #79（09-11，open）chore: bump @visable-dev/vue to 43.44.0-beta.2 and routing to 22.10.0-beta.1

## user-frontend（3）

- #204（05-12，merged 05-22）Fe 761/ga4 migration
- #217（06-30，merged 07-09）Feat/ga4 user
- #222（07-09，merged 07-14）Refactor user session management

## supplier-backend-mcp-service（2）

- #2（05-07，merged 05-07）feat: enhance README and refactor MCP tool registration
- #4（05-07，merged 05-07）Fix/tool for accio

## manage_github（2）

- #998（06-12，merged 06-12）Add v-ai-platform and v-ai-platform-iac repositories
- #1047（07-03，merged 07-03）feat: add visable-plugin-marketplace repo config

## routing-lib（2）

- #158（09-10，closed）CTOOL-635: add SUPPLIER_SETTINGS_ROUTE（早期版本）
- #159（09-10，open）CTOOL-635: add SUPPLIER_SETTINGS_ROUTE constant

## visable-vue（1）

- #737（09-10，open）CTOOL-636: add Settings entry to VisPageNavigation

## 其他 org 仓库（各 1）

- ad-center-frontend-iac #7（08-24，merged 08-28）feat: add NUXT_PUBLIC_STAGE env for monitoring SDKs
- business-insights-frontend-iac #11（08-21，merged 08-28）feat: add Sentry error tracking integration
- product-editor-frontend-iac #6（09-10，open）CTOOL-637: add conversationsBffApiUrl per environment
- unified-search-frontend #1588（08-31，merged 09-02）chore(deps): upgrade stability SDK packages (FE-1045)
- visitors-frontend-iac #21（08-24，merged 08-28）feat: add NUXT_PUBLIC_STAGE for stability and Web Vitals SDKs
- web_analytics_maintenance #17（04-07，open）feat: update product posting test cases
- wlw_nginx #586（09-10，open）CTOOL-637: edge routes for supplier settings pages and settings BFF proxy

## 个人仓库

- junyang-visable/my-ai #1（07-15，closed）Cursor/jira work summary skill
