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

扫描完成后输出「仓库快照」：

```
仓库快照：
- 项目名：___
- 技术栈：Vue x.x / Nuxt x.x / TypeScript
- UI 库：___（或「未找到，需确认」）
- 路由：N 个，路径：...
- Stores：N 个，名称：...
- i18n：是 / 否
- 测试框架：___
- API Base URL 变量：___（或「未找到」）
- HTTP 封装文件：___（或「未找到」）
```

**关键信息缺失（如 UI 库不明）时，在继续前询问用户确认，不要猜测。**

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

读取各模板文件，按下表填入可确定字段，其余 `[替换]` / `[TODO]` 占位符保留：

| 模板 | 输出 | 用扫描结果填写的字段 |
|------|------|---------------------|
| `repowiki-01-overview.md` | `repowiki/01-项目概述.md` | 项目名、技术栈版本、核心模块（从 package.json 提取） |
| `repowiki-02-tech-spec.md` | `repowiki/02-技术规范.md` | Vue/Nuxt/TS 版本、UI 库名称、目录结构（从扫描结果填） |
| `repowiki-03-routes.md` | `repowiki/03-路由与页面结构.md` | 路由列表（路径 + 文件名，填入表格；其余守卫/布局留占位符） |
| `repowiki-04-components.md` | `repowiki/04-组件库文档.md` | 顶层组件目录列表；Props/Emits 细节留占位符 |
| `repowiki-05-state.md` | `repowiki/05-状态管理.md` | Store 名称列表（填入 Store 列表表格；State/Actions 留占位符） |
| `repowiki-06-api.md` | `repowiki/06-API文档.md` | Base URL（从 `.env` / vite/nuxt 配置提取）、请求封装路径（扫描 `utils/` 或 `composables/`）；接口列表、错误码与类型路径留占位符 |
| `repowiki-07-business.md` | `repowiki/07-业务知识.md` | 仅填项目名；术语与流程全部留占位符（需人工填写） |
| `repowiki-08-tests.md` | `repowiki/08-测试用例.md` | 测试框架名称；环境 URL 与账号留占位符 |

> 原则：**只填能从代码确定的字段**，无法确定的一律保留原始占位符。

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

待人工补充（第一次 onboarding 时完成）：
- [ ] repowiki/01：环境 URL、负责人
- [ ] repowiki/03：路由守卫规则
- [ ] repowiki/04：核心业务组件 Props/Emits
- [ ] repowiki/06：接口列表、鉴权方式、错误码、Mock 配置
- [ ] repowiki/07：领域术语与主业务流程
- [ ] repowiki/08：测试账号与 E2E 用例优先级
- [ ] specs/global-specs.md：补充「待确认」字段
```
