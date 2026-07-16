---
name: init-ai-standards
description: Initializes a frontend project's AI engineering standards: generates .cursorrules, repowiki/ knowledge base (7 chapters + INDEX), and SDD specs/ structure. Self-contained with all templates included. Use when setting up a new project for AI-assisted development, or when the user says "初始化 AI 工程标准", "init AI standards", "生成 repowiki", "setup cursorrules", "初始化 SDD", or asks to onboard a project to AI standards.
---

# init-ai-standards

初始化前端项目 AI 工程标准三件套：**.cursorrules + repowiki/ + SDD specs/**。

所有模板位于本 skill 目录的 `templates/` 下，skill 完全自包含，可复制到任意项目的 `.cursor/skills/` 或 `~/.cursor/skills/` 使用。

---

## 执行前声明

宣布："正在按 init-ai-standards skill 初始化 AI 工程标准，分四个阶段执行。"

---

## Phase 1：扫描仓库

### 1.1 基础扫描

依次读取以下文件（不存在则跳过，记录「未找到」）：

| 读取目标 | 提取内容 |
|----------|----------|
| `package.json` | 项目名、Vue/Nuxt 版本、UI 组件库（dependencies 中查找 element-plus / naive-ui / ant-design-vue 等）、测试框架（devDependencies） |
| `nuxt.config.ts` 或 `vite.config.ts` | 路由模式、别名、插件 |
| `pages/`（列一层） | 路由路径与文件名列表 |
| `stores/`（列一层） | Pinia Store 文件名列表 |
| `components/`（列一层） | 顶层组件目录结构 |
| `composables/`（列一层） | 公共组合式函数列表 |
| `server/api/`（列一层，可选） | Server Route 结构 |
| `locales/` 或 `i18n/` 是否存在 | 是否启用 i18n |
| `.env` / `.env.example`（可选） | API Base URL 环境变量（如 `VITE_API_BASE_URL` / `NUXT_PUBLIC_API_BASE`） |
| `utils/request*` 或 `composables/use*Fetch*`（可选） | HTTP 封装文件路径 |

输出「仓库快照」（结构化摘要），**关键信息缺失（如 UI 库不明）时询问用户确认，不要猜测。**

### 1.2 深度读取关键源文件

> 目的：让 AI 真正理解代码，后续 repowiki 能写出有意义的内容，而非全部留空。

逐一读取下列文件并提取语义内容：

| 文件类型 | 读取策略 | 提取内容 |
|----------|----------|----------|
| `pages/*.vue`（前 8 个，按文件大小或名称优先） | 读取 `<script setup>` / `<script>` 块 | 页面功能描述（一句话）、调用了哪些 Store / composable / API、主要用户操作 |
| `stores/*.ts`（全部） | 完整读取 | state 字段名与类型、actions 名称及用途（一句话）、getters 名称 |
| `composables/use*.ts`（前 6 个） | 完整读取 | 函数签名、入参说明、返回值、主要用途（一句话） |
| HTTP 封装文件（`utils/request*` / `composables/use*Fetch*`） | 完整读取 | baseURL 来源、鉴权方式（请求头 / Cookie / Token）、拦截器主要逻辑 |
| `server/api/` 文件（前 5 个，可选） | 读取文件名 + 前 30 行 | 接口路径、HTTP method、返回结构摘要 |
| `components/` 顶层 `.vue` 文件（前 5 个） | 读取 `defineProps` / `defineEmits` 定义 | Props 名称 + 类型、Emits 事件名 |

**原则：**
- 读取后，用自己的语言总结，不复制粘贴代码。
- 无法理解的字段写「待确认」，**不编造**。
- 读取量较大时，优先保证 stores、HTTP 封装、pages 全覆盖。

深度读取完成后，输出「代码语义摘要」，格式示例：

```
代码语义摘要：
- Pages（8 个）：
  · /dashboard → 展示数据统计概览，使用 useStatStore、useDashboardApi
  · /user/list → 用户列表与搜索，使用 useUserStore，调用 GET /api/users
  · ...
- Stores（3 个）：
  · useStatStore：state={ stats, loading }，action=fetchStats()
  · useUserStore：state={ list, total, current }，actions=fetchList/updateUser
  · ...
- Composables（4 个）：
  · useDashboardApi：封装 /api/dashboard/* 请求，返回 { data, refresh }
  · usePermission：检查当前用户角色权限，返回 { can(action) }
  · ...
- HTTP 封装：ofetch 实例，baseURL 来自 NUXT_PUBLIC_API_BASE，请求头注入 Bearer token
- 业务组件：AppTable（Props: columns/data/loading，Emits: sort-change/page-change）
```

---

## Phase 2：生成 .cursorrules

1. **检查 `.cursorrules` 是否已存在**：
   - 若**不存在**：直接进入第 2 步生成。
   - 若**已存在**：读取现有文件内容，判断是否已包含 `SDD 流程纪律` 章节。
     - 若**已包含**：跳过本 Phase，输出 `.cursorrules 已存在且包含 SDD 流程纪律，跳过生成。`
     - 若**不包含**：向用户询问：
       ```
       .cursorrules 已存在，是否将模板内容追加到现有文件末尾？
       (a) 追加到末尾  (b) 覆盖替换  (c) 跳过，保持不变
       ```
       等待用户选择后按选择执行；选 (c) 则跳过本 Phase。
2. 读取模板：`.cursor/skills/init-ai-standards/templates/cursorrules.md`
3. 替换占位符：
   - `[替换: 项目中文/英文名称]` → 仓库快照中的项目名
   - `[替换: 例如 Element Plus / Naive UI / 自研组件库]` → 扫描到的 UI 库
4. 按第 1 步的选择写入 `.cursorrules`（追加 / 覆盖）。
5. 确认：`.cursorrules 已生成/更新。`

---

## Phase 3：初始化 repowiki/

### 3.1 创建目录

检查 `repowiki/` 是否已存在：
- 若**不存在**：`mkdir -p repowiki`，继续生成所有文件。
- 若**已存在**：只生成 `repowiki/` 中**尚不存在**的文件，已存在的文件跳过并在汇总中列出。

### 3.2 生成 INDEX.md

读取 `.cursor/skills/init-ai-standards/templates/repowiki-INDEX.md`，替换：
- `[替换: 项目名称]` → 项目名
- `[替换: 姓名 / 角色]` → `待填写`
- `[替换: YYYY-MM-DD]` → 今天日期

写入 `repowiki/INDEX.md`。

### 3.3 生成 01–08 章节

读取各模板文件，结合 **Phase 1 仓库快照 + 代码语义摘要**，按下表写入内容：

| 模板 | 输出 | 写入策略 |
|------|------|----------|
| `repowiki-01-overview.md` | `repowiki/01-项目概述.md` | 用仓库快照填写项目名、技术栈版本；用语义摘要中 Pages 信息概述核心模块（2–4 句话）；环境 URL / 负责人留占位符 |
| `repowiki-02-tech-spec.md` | `repowiki/02-技术规范.md` | 填 Vue/Nuxt/TS 版本、UI 库、目录结构；从 HTTP 封装摘要补充「请求规范」（baseURL 来源、鉴权方式）；其余约定留占位符 |
| `repowiki-03-routes.md` | `repowiki/03-路由与页面结构.md` | **逐条填写**每条路由：路径 + 对应文件 + 功能描述（来自语义摘要）+ 主要使用的 Store/API；守卫规则、布局细节留占位符 |
| `repowiki-04-components.md` | `repowiki/04-组件库文档.md` | 填写已读到的组件 Props/Emits（来自语义摘要）；未读到的组件只填名称，Props/Emits 留占位符 |
| `repowiki-05-state.md` | `repowiki/05-状态管理.md` | **逐 Store 填写**：Store 名称 + state 字段 + 每个 action 的用途一句话（来自语义摘要）；getter 和跨 Store 依赖留占位符 |
| `repowiki-06-api.md` | `repowiki/06-API文档.md` | 填写 baseURL 来源与取值、HTTP 封装路径与鉴权方式（来自语义摘要）；已扫描到的 server/api 接口填入接口列表；错误码、Mock 配置留占位符 |
| `repowiki-07-business.md` | `repowiki/07-业务知识.md` | 从 Pages 语义摘要推断主要业务流程（写 2–4 条流程描述）；领域术语从 Store/Composable 名称推断并列出（标注「待确认」）；常见误区全留占位符 |
| `repowiki-08-tests.md` | `repowiki/08-测试用例.md` | 填测试框架名称；从 Pages 语义摘要列出建议 E2E 测试场景（标注「建议」）；账号/环境 URL 留占位符 |

> **写入原则**：
> - 来自代码的信息直接写入，措辞用第三方视角（「该 Store 管理…」「该页面负责…」）。
> - 无法从代码确定的字段保留原始 `[TODO]` 占位符，不编造。
> - 每个章节写完后在文件顶部加注：`> ⚠️ 由 init-ai-standards 自动生成，请人工核查标注「待确认」的字段。`

### 3.4 输出汇总

```
repowiki/ 初始化完成（9 个文件）。
待人工补充：
- 01：生产/测试环境 URL、负责人
- 03：路由守卫规则、布局说明
- 04：业务组件 Props / Emits 详情
- 06：接口列表、鉴权方式、错误码、Mock 配置
- 07：领域术语、核心流程、常见误区
- 08：测试环境账号、E2E 用例
```

---

## Phase 4：初始化 SDD

### 4.1 创建目录

检查 `specs/` 是否已存在：
- 若**不存在**：`mkdir -p specs`，继续生成。
- 若**已存在且 `specs/global-specs.md` 已存在**：跳过 4.3，输出 `specs/global-specs.md 已存在，跳过生成。`

### 4.2 运行 openspec init（若已安装）

```bash
openspec init
```

若命令不存在，跳过并提示：`openspec 未安装，可运行 npm install -g @fission-ai/openspec@latest 后再执行。`

### 4.3 生成 specs/global-specs.md

基于 Phase 1 仓库快照与已生成的 `repowiki/`，生成初始全局 Specs：

- 文件顶部：技术栈、路由约定、状态管理方案说明（与 repowiki 一致）
- 主体 Spec 条目表：每个已扫描的路由占一行，列：`页面路径 | 功能描述（从路径名推断，标注「待确认」）| 核心交互（留空）| 涉及 Stores（按名称关联推断）| 涉及 APIs（留空）`
- 无法确认的字段写「待确认」，不编造接口或 Store

写入 `specs/global-specs.md`。

---

## 最终汇总

```
✅ AI 工程标准初始化完成

已生成：
- .cursorrules
- repowiki/INDEX.md + 01-08.md（共 9 个文件）
- specs/global-specs.md

待人工核查与补充（第一次 onboarding 时完成）：
- [ ] repowiki/01：生产/测试环境 URL、负责人、SLA
- [ ] repowiki/02：命名约定细节、禁用 API 补充
- [ ] repowiki/03：路由守卫规则、嵌套布局说明；核查 AI 生成的功能描述
- [ ] repowiki/04：未被扫描到的组件 Props/Emits；核查已生成内容
- [ ] repowiki/05：getter 逻辑、跨 Store 依赖；核查 AI 生成的 action 描述
- [ ] repowiki/06：完整接口列表（AI 只能覆盖 server/api 部分）、错误码、Mock 配置
- [ ] repowiki/07：领域术语核准、常见误区、标注「待确认」的流程
- [ ] repowiki/08：测试账号与环境 URL；核查 AI 建议的 E2E 场景
- [ ] specs/global-specs.md：补充「待确认」字段
```
