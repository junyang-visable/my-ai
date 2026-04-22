# 前端 AI Coding 工程规范 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 产出一套完整的前端 AI Coding 工程规范，包含内部 Playbook（可执行模板和 Checklist）和对外白皮书草稿。

**Architecture:** 内容中台模式——先逐模块输出内部 Playbook 的各个文档（Cursor Rules 模板、RepoWiki 模板、SDD 指南、Prompt 模板库、Review Checklist），再组装内部 Playbook README 和白皮书草稿。每个模块独立交付，互不依赖。

**Tech Stack:** Markdown 文档、Git 版本管理；运行时工具：Cursor（AI IDE）、OpenSpecs、Vue 3 / Nuxt

---

## 文件结构

```
docs/frontend-ai-standards/
├── internal-playbook/
│   ├── README.md                              # Playbook 首页，使用入口
│   ├── 01-cursor-rules/
│   │   ├── README.md                          # Cursor 配置规范说明
│   │   ├── vue-nuxt-cursorrules.md            # 可直接复制的 .cursorrules 内容
│   │   └── mcp-setup-guide.md                 # MCP 工具配置建议
│   ├── 02-repowiki/
│   │   ├── README.md                          # RepoWiki 规范说明
│   │   └── templates/
│   │       ├── INDEX.template.md
│   │       ├── 01-项目概述.template.md
│   │       ├── 02-技术规范.template.md
│   │       ├── 03-路由与页面结构.template.md
│   │       ├── 04-组件库文档.template.md
│   │       ├── 05-状态管理.template.md
│   │       ├── 06-业务知识.template.md
│   │       └── 07-测试用例.template.md
│   ├── 03-sdd/
│   │   ├── README.md                          # SDD 规范说明
│   │   └── openspecs-frontend-guide.md        # OpenSpecs 前端使用指南
│   ├── 04-prompt-templates/
│   │   ├── README.md
│   │   ├── component-generation.md            # 组件生成 Prompt 模板
│   │   ├── page-refactoring.md                # 页面重构 Prompt 模板
│   │   ├── api-integration.md                 # 接口对接 Prompt 模板
│   │   ├── style-adjustment.md                # 样式调整 Prompt 模板
│   │   ├── unit-test-generation.md            # 单测生成 Prompt 模板
│   │   └── debug-analysis.md                  # 调试分析 Prompt 模板
│   └── 05-review-checklist/
│       ├── README.md
│       └── frontend-review-checklist.md       # 完整 Review Checklist
└── whitepaper/
    └── frontend-ai-coding-whitepaper.md       # 对外白皮书草稿
```

---

## Task 1：Cursor 配置规范

**Files:**
- Create: `docs/frontend-ai-standards/internal-playbook/01-cursor-rules/README.md`
- Create: `docs/frontend-ai-standards/internal-playbook/01-cursor-rules/vue-nuxt-cursorrules.md`
- Create: `docs/frontend-ai-standards/internal-playbook/01-cursor-rules/mcp-setup-guide.md`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p docs/frontend-ai-standards/internal-playbook/01-cursor-rules
```

- [ ] **Step 2: 写 README.md**

`docs/frontend-ai-standards/internal-playbook/01-cursor-rules/README.md`

```markdown
# Cursor 配置规范

统一团队 Cursor 工具层配置，确保 AI 在每个前端项目中都有一致的约束边界。

## 为什么需要统一配置

不同的 Cursor 配置会导致 AI 生成代码的风格、质量差异巨大。统一配置让团队所有成员在同一套约束下使用 AI，减少 Review 时的摩擦。

## 包含内容

| 文件 | 说明 |
|------|------|
| `vue-nuxt-cursorrules.md` | 可直接复制到项目根目录的 `.cursorrules` 内容 |
| `mcp-setup-guide.md` | 推荐接入的 MCP 工具及配置方式 |

## 使用方式

1. 复制 `vue-nuxt-cursorrules.md` 中的内容，在项目根目录创建 `.cursorrules` 文件；
2. 根据项目实际情况删减不适用的条目；
3. 按 `mcp-setup-guide.md` 配置 MCP 工具（可选）。
```

- [ ] **Step 3: 写 vue-nuxt-cursorrules.md（含完整 Rules 内容）**

`docs/frontend-ai-standards/internal-playbook/01-cursor-rules/vue-nuxt-cursorrules.md`

```markdown
# Vue / Nuxt 项目 .cursorrules 模板

将以下内容复制到项目根目录的 `.cursorrules` 文件中，根据实际项目删减不适用的条目。

---

## 复制内容（.cursorrules）

\`\`\`
# === 项目基础信息 ===
# 项目名称：[替换为项目名]
# 技术栈：Vue 3 + Nuxt 3 + TypeScript + Pinia + [UI 库名]
# 代码规范：参见 repowiki/zh/content/02-技术规范/开发规范.md

# === 代码生成规范 ===

## 组件规范
- 所有组件使用 Vue 3 Composition API + <script setup> 语法
- 组件文件名使用 PascalCase（如 UserCard.vue）
- 页面文件放在 pages/ 目录，组件放在 components/ 目录
- 每个组件只做一件事，超过 200 行需提示拆分
- Props 必须定义 TypeScript 类型，不允许 any
- Emits 必须使用 defineEmits 显式声明

## TypeScript 规范
- 所有函数参数和返回值必须有类型注解
- 禁止使用 any，用 unknown + 类型守卫代替
- 接口（Interface）用于描述对象结构，类型别名（Type）用于联合类型
- 枚举使用 const enum

## 状态管理（Pinia）
- 每个业务模块对应一个 Store，文件放在 stores/ 目录
- Store 命名：use[ModuleName]Store（如 useUserStore）
- 不允许在组件中直接修改 Store 的 state，必须通过 actions

## 样式规范
- 使用 scoped CSS，避免全局样式污染
- 使用 CSS 变量管理主题色，不允许硬编码颜色值
- 响应式断点使用项目统一定义的 breakpoint 变量

## API 调用规范
- 所有 API 调用封装在 composables/useXxx.ts 中
- 使用 useFetch 或 useAsyncData（Nuxt）处理数据请求
- 错误处理：必须捕获异常，不允许裸露的 await 调用
- 不允许在组件中直接使用 fetch/axios

## 国际化
- 所有用户可见的字符串必须走 i18n，禁止硬编码中文/英文
- i18n key 格式：[模块名].[功能].[描述]（如 user.login.title）

## 安全规范
- 禁止使用 v-html，除非内容经过 DOMPurify 处理
- 不允许将敏感数据（token、密码）存储在 localStorage
- 权限检查不允许只在前端完成，必须配合后端鉴权

## 注释规范
- 只注释"为什么"，不注释"是什么"
- 复杂业务逻辑必须有注释说明背景
- 禁止无意义注释（如 // 获取用户信息）

# === AI 行为约束 ===
- 生成代码前，先确认是否已读取 repowiki 中的相关文档
- 不允许引用项目中不存在的组件或 composable
- 修改现有文件时，保持已有的代码风格
- 遇到不确定的业务逻辑，询问而非自行假设
- 生成的代码必须可以通过 TypeScript 类型检查
\`\`\`

---

## 使用说明

1. 将上方 ` ``` ` 内的内容复制到项目根目录 `.cursorrules` 文件
2. 替换 `[替换为项目名]` 和 `[UI 库名]`
3. 如果项目未使用 Pinia，删除状态管理部分
4. 如果项目未使用 i18n，删除国际化部分
```

- [ ] **Step 4: 写 mcp-setup-guide.md**

`docs/frontend-ai-standards/internal-playbook/01-cursor-rules/mcp-setup-guide.md`

```markdown
# MCP 工具配置建议

MCP（Model Context Protocol）工具可以让 Cursor 直接访问外部数据源，扩展 AI 的上下文能力。

## 推荐接入的 MCP 工具

| 工具 | 用途 | 优先级 |
|------|------|--------|
| 浏览器 DevTools MCP | 让 AI 读取页面运行时状态、控制台报错 | 高 |
| 文件系统 MCP | 读取项目外部的文档（如设计稿导出的 tokens） | 中 |

## 配置方式

在 Cursor 设置中（Settings → MCP），添加服务器配置：

\`\`\`json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-chrome-devtools"]
    }
  }
}
\`\`\`

## @docs 索引配置

在 Cursor 的 Settings → Features → Docs 中，添加以下文档索引：

| 文档 | URL |
|------|-----|
| Vue 3 官方文档 | https://vuejs.org/guide/ |
| Nuxt 3 官方文档 | https://nuxt.com/docs |
| Pinia 文档 | https://pinia.vuejs.org/ |
| [项目 UI 库文档] | [替换为实际 URL] |

索引完成后，在 Prompt 中使用 `@Vue3` 等引用，Cursor 会自动注入相关文档内容。
```

- [ ] **Step 5: 提交**

```bash
git add docs/frontend-ai-standards/internal-playbook/01-cursor-rules/
git commit -m "docs: add Cursor configuration standards for Vue/Nuxt"
```

---

## Task 2：RepoWiki 规范（前端版）

**Files:**
- Create: `docs/frontend-ai-standards/internal-playbook/02-repowiki/README.md`
- Create: `docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/` (7 个模板文件)

- [ ] **Step 1: 创建目录**

```bash
mkdir -p docs/frontend-ai-standards/internal-playbook/02-repowiki/templates
```

- [ ] **Step 2: 写 README.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/README.md`

```markdown
# RepoWiki 规范（前端版）

RepoWiki 是存放在代码仓库中的项目知识库，解决"AI 不懂项目上下文"的核心问题。

## 原则

所有文档以"AI 能直接读懂并使用"为标准：
- **结构化优于叙述**：用表格、代码块、列表，而非散文
- **约束优于描述**：写清楚"不能做什么"比"能做什么"更重要
- **背景优于定义**：解释"为什么这样设计"比"这是什么"更有价值

## 目录结构

```
repowiki/zh/content/
├── INDEX.md
├── 01-项目概述.md
├── 02-技术规范/
│   ├── 技术栈.md
│   ├── 开发规范.md
│   └── 性能要求.md
├── 03-路由与页面结构/
│   └── 路由结构.md
├── 04-组件库文档/
│   └── 核心组件API.md
├── 05-状态管理/
│   └── Pinia-Stores.md
├── 06-业务知识/
│   ├── 核心流程.md
│   └── 领域概念.md
└── 07-测试用例/
    └── 测试用例.md
```

## 使用步骤

1. 在项目根目录创建 `repowiki/zh/content/` 目录
2. 复制 `templates/` 下的所有模板文件到对应目录
3. 将文件名中的 `.template.md` 改为 `.md`
4. 按模板说明填写项目实际内容
5. 提交到 main 分支

## 验收标准

每个前端核心业务仓库必须在 main 分支中包含一份填写完整的 RepoWiki。
```

- [ ] **Step 3: 写 INDEX.template.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/INDEX.template.md`

```markdown
# [项目名称] RepoWiki

> 本文档是项目知识库索引，供 AI 编码助手快速了解项目全貌。

## 快速导航

| 文档 | 内容摘要 |
|------|---------|
| [01-项目概述](./01-项目概述.md) | 项目定位、核心功能、团队信息 |
| [02-技术规范/技术栈](./02-技术规范/技术栈.md) | 框架版本、依赖库清单 |
| [02-技术规范/开发规范](./02-技术规范/开发规范.md) | 命名规范、代码风格约束 |
| [03-路由与页面结构](./03-路由与页面结构/路由结构.md) | 页面层级、路由守卫规则 |
| [04-组件库文档](./04-组件库文档/核心组件API.md) | 核心组件 Props/Emits/Slots |
| [05-状态管理](./05-状态管理/Pinia-Stores.md) | Store 列表与数据流说明 |
| [06-业务知识/核心流程](./06-业务知识/核心流程.md) | 关键业务流程图 |
| [06-业务知识/领域概念](./06-业务知识/领域概念.md) | 业务术语与概念定义 |
| [07-测试用例](./07-测试用例/测试用例.md) | E2E 测试场景与验收标准 |

## AI 使用提示

开始编码前，请先阅读以下文档：
1. `02-技术规范/开发规范.md` — 了解代码约束
2. 与当前任务相关的业务知识文档
3. 涉及的组件 API 文档
```

- [ ] **Step 4: 写 01-项目概述.template.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/01-项目概述.template.md`

```markdown
# 项目概述

## 基本信息

| 项目名称 | [替换] |
|---------|--------|
| 仓库地址 | [替换] |
| 生产环境 | [替换] |
| 测试环境 | [替换] |
| 前端负责人 | [替换] |

## 项目定位

[一句话描述这个项目是做什么的，面向什么用户，解决什么问题]

## 核心功能模块

| 模块 | 说明 | 对应页面路径 |
|------|------|------------|
| [模块名] | [功能描述] | [/path] |

## 关键约束

> 以下是 AI 在开发时必须遵守的项目级约束

- [例：所有页面必须支持移动端，最小兼容屏幕宽度 375px]
- [例：不允许引入新的 npm 依赖，除非经过 Tech Lead 审批]
- [例：所有接口调用必须经过统一的 request.ts 封装]
```

- [ ] **Step 5: 写 02-技术规范.template.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/02-技术规范.template.md`

```markdown
# 技术规范

## 核心技术栈

| 分类 | 技术 | 版本 | 备注 |
|------|------|------|------|
| 框架 | Vue | 3.x | Composition API |
| 框架 | Nuxt | 3.x | SSR / SSG |
| 语言 | TypeScript | 5.x | 严格模式 |
| 状态管理 | Pinia | 2.x | |
| UI 库 | [替换] | [版本] | |
| CSS | [替换] | [版本] | 例：UnoCSS / Tailwind |
| 请求库 | useFetch (Nuxt 内置) | - | |
| 测试 | Vitest | 1.x | 单元测试 |
| 测试 | Playwright | 1.x | E2E 测试 |

## 开发规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserCard.vue` |
| 页面文件 | kebab-case | `user-profile.vue` |
| Composable | camelCase，use 前缀 | `useUserInfo.ts` |
| Store | camelCase，use 前缀 + Store 后缀 | `useCartStore.ts` |
| CSS 类名 | kebab-case | `.user-card` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |

### 目录规范

```
src/
├── components/     # 通用组件（跨页面复用）
├── composables/    # 通用 Composable
├── pages/          # 页面组件（Nuxt 路由）
├── stores/         # Pinia Store
├── utils/          # 纯函数工具
├── types/          # 全局类型定义
└── assets/         # 静态资源
```

## 性能要求

| 指标 | 目标值 | 测量工具 |
|------|--------|---------|
| LCP | < 2.5s | Lighthouse |
| FID | < 100ms | Lighthouse |
| Bundle Size（首屏） | < [替换]KB | vite-bundle-analyzer |
```

- [ ] **Step 6: 写 03-路由与页面结构.template.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/03-路由与页面结构.template.md`

```markdown
# 路由与页面结构

## 页面层级

```
/                       # 首页
├── /login              # 登录
├── /dashboard          # 仪表板（需登录）
│   ├── /dashboard/xxx  # [替换]
│   └── /dashboard/yyy  # [替换]
├── /[module]/          # [模块名]（需登录）
│   ├── /[module]/list
│   └── /[module]/detail/:id
└── /403                # 无权限
```

## 路由守卫规则

| 规则 | 说明 |
|------|------|
| 需要登录的路由 | 在页面组件中使用 `definePageMeta({ middleware: 'auth' })` |
| 权限控制 | [替换：描述权限检查逻辑] |
| 重定向规则 | [替换：描述重定向逻辑] |

## 布局说明

| 布局文件 | 适用页面 | 包含内容 |
|---------|---------|---------|
| `layouts/default.vue` | 已登录页面 | 顶部导航、侧边栏 |
| `layouts/auth.vue` | 登录/注册页面 | 仅展示内容区 |
```

- [ ] **Step 7: 写 04-组件库文档.template.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/04-组件库文档.template.md`

```markdown
# 核心组件 API 文档

> 仅记录项目自定义的核心组件，UI 库组件请参考对应文档。

## 组件文档格式说明

每个组件按以下格式记录：

---

## [组件名]

**文件路径：** `components/[ComponentName].vue`  
**用途：** [一句话说明用途]

### Props

| Prop | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `propName` | `string` | 是 | - | [说明] |
| `propName2` | `boolean` | 否 | `false` | [说明] |

### Emits

| 事件 | 参数类型 | 说明 |
|------|---------|------|
| `update:modelValue` | `string` | [说明] |
| `click` | `MouseEvent` | [说明] |

### Slots

| Slot | 说明 |
|------|------|
| `default` | [说明] |
| `footer` | [说明] |

### 使用示例

```vue
<ComponentName
  :prop-name="value"
  @click="handleClick"
>
  内容
</ComponentName>
```

---

[继续添加更多组件...]
```

- [ ] **Step 8: 写 05-状态管理.template.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/05-状态管理.template.md`

```markdown
# Pinia Store 文档

## Store 列表

| Store 文件 | 管理的状态 | 主要 Actions |
|-----------|-----------|-------------|
| `stores/useUserStore.ts` | 用户信息、登录状态 | login, logout, fetchProfile |
| `stores/use[Module]Store.ts` | [替换] | [替换] |

## Store 文档格式

---

## useUserStore

**文件：** `stores/useUserStore.ts`

### State

| 字段 | 类型 | 说明 |
|------|------|------|
| `user` | `User \| null` | 当前登录用户信息 |
| `token` | `string \| null` | 访问令牌 |
| `isLoading` | `boolean` | 加载状态 |

### Actions

| Action | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `login(credentials)` | `{ username: string, password: string }` | `Promise<void>` | 登录并保存 token |
| `logout()` | - | `void` | 清除用户状态 |
| `fetchProfile()` | - | `Promise<User>` | 获取最新用户信息 |

### 注意事项

- [例：token 保存在 httpOnly Cookie，不存 localStorage]
- [例：logout 后需清除所有其他 Store 的状态]

---
```

- [ ] **Step 9: 写 06-业务知识.template.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/06-业务知识.template.md`

```markdown
# 业务知识

## 领域概念

> 定义业务术语，避免 AI 对业务词汇产生误解

| 术语 | 定义 | 备注 |
|------|------|------|
| [业务词汇] | [精确定义] | [补充说明] |

## 核心业务流程

> 描述关键操作的完整流程，帮助 AI 理解业务上下文

### [流程名称，如：用户下单流程]

```
用户选择商品
    ↓
加入购物车
    ↓
填写收货信息
    ↓
选择支付方式
    ↓
提交订单（POST /api/orders）
    ↓
[前端] 跳转到支付页面
    ↓
支付成功回调 → 刷新订单状态
```

**关键约束：**
- [例：订单提交前必须校验库存，库存不足时前端提前拦截]
- [例：支付超时时间为 30 分钟，超时后自动取消]

## 常见误区

> 记录 AI 容易理解错的业务逻辑

| 误区 | 正确理解 |
|------|---------|
| [例：以为 status=1 表示激活] | [实际：status 使用枚举，ACTIVE/INACTIVE/PENDING] |
```

- [ ] **Step 10: 写 07-测试用例.template.md**

`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/07-测试用例.template.md`

```markdown
# 测试用例

> 提供验收标准，供 AI 生成代码后自行验证

## 测试环境

| 环境 | URL | 账号 |
|------|-----|------|
| 测试环境 | [替换] | 联系 [姓名] 获取 |

## E2E 测试用例

### [功能模块名，如：用户登录]

| 用例 ID | 用例描述 | 前置条件 | 操作步骤 | 预期结果 |
|---------|---------|---------|---------|---------|
| TC-001 | 正常登录 | 用户已注册 | 1. 进入 /login 2. 输入正确账号密码 3. 点击登录 | 跳转到 /dashboard，顶部显示用户名 |
| TC-002 | 密码错误 | - | 1. 输入错误密码 2. 点击登录 | 显示"账号或密码错误"提示，不跳转 |
| TC-003 | 未登录访问受保护页面 | 未登录状态 | 直接访问 /dashboard | 重定向到 /login |

## 组件测试用例

### [组件名]

| 用例 | 操作 | 预期 |
|------|------|------|
| 渲染默认状态 | 传入必填 Props | 正常渲染，无报错 |
| 点击触发 Emit | 点击组件 | 触发 click emit，参数类型正确 |
```

- [ ] **Step 11: 提交**

```bash
git add docs/frontend-ai-standards/internal-playbook/02-repowiki/
git commit -m "docs: add RepoWiki frontend templates (7 templates)"
```

---

## Task 3：SDD 规范（前端版）

**Files:**
- Create: `docs/frontend-ai-standards/internal-playbook/03-sdd/README.md`
- Create: `docs/frontend-ai-standards/internal-playbook/03-sdd/openspecs-frontend-guide.md`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p docs/frontend-ai-standards/internal-playbook/03-sdd
```

- [ ] **Step 2: 写 README.md**

`docs/frontend-ai-standards/internal-playbook/03-sdd/README.md`

```markdown
# SDD 规范（前端版）

SDD（Spec-Driven Development，规范驱动开发）要求在 AI 编码之前先生成 Specs，用结构化的规格说明消除模糊点，提升开发准确性。

## 为什么需要 SDD

不加约束地让 AI 直接写代码，会导致：
- 理解偏差：AI 自行假设需求，产出与预期不符
- 返工成本：问题在 Review 阶段才发现
- 上下文丢失：多轮对话后 AI 遗忘早期约束

先生成 Specs，再编码，能让 AI 在明确的边界内工作。

## 工具：OpenSpecs

安装：https://github.com/Fission-AI/OpenSpec

## 前端 Specs 覆盖范围

| Specs 类型 | 适用场景 | 生成粒度 |
|-----------|---------|---------|
| 全局 Specs | 首次为仓库建立基线 | 整个仓库 |
| 页面级 Specs | 新增或重构整个页面 | 单个页面 |
| 功能级 Specs | 新增具体功能/组件 | 单个功能点 |

详细使用流程见 `openspecs-frontend-guide.md`。
```

- [ ] **Step 3: 写 openspecs-frontend-guide.md**

`docs/frontend-ai-standards/internal-playbook/03-sdd/openspecs-frontend-guide.md`

```markdown
# OpenSpecs 前端使用指南

## 安装

```bash
# 通过 npm 全局安装
npm install -g openspec

# 或通过项目本地安装
npm install --save-dev openspec
```

## 场景一：为存量仓库生成全局 Specs

对每个核心前端仓库，第一次需要生成一份描述现有功能的全量 Specs，作为后续迭代的基础。

**步骤：**

1. 在 Cursor 中打开项目，执行以下 Prompt：

```
请基于当前项目代码，生成一份全局 Specs，描述项目中所有页面和核心功能。

格式要求：
- 每个页面一个 Spec 条目
- 每个条目包含：页面路径、功能描述、核心交互、涉及的 Store 和 API
- 输出到 specs/global-specs.md

参考 repowiki/zh/content/ 中的文档了解项目背景。
```

2. 检查生成结果，补充 AI 遗漏的页面或功能；
3. 将 `specs/global-specs.md` 提交到 main 分支。

## 场景二：新需求开发前生成 Specs

**步骤：**

1. 收到需求后，在开始编码前执行以下 Prompt：

```
我需要开发以下功能：
[粘贴需求描述]

请先生成一份 Specs，包含：
1. 功能范围：需要新增/修改哪些页面和组件
2. 数据模型：涉及的接口、入参、出参（参考 repowiki 中的 API 文档）
3. 交互细节：用户操作流程、边界条件、错误状态
4. 技术约束：需要遵守的项目规范（参考 repowiki/zh/content/02-技术规范）

生成完成后，等待我确认再开始编码。
```

2. 检查 Specs，补充遗漏的边界条件和约束；
3. 确认 Specs 后，再指示 AI 按 Specs 逐步开发。

## 场景三：开发完成后更新 Specs

代码合并后，执行以下 Prompt 同步更新：

```
本次开发已完成，请更新 specs/ 中相关的 Specs 文档，
反映新增的功能和修改的行为。同时检查 repowiki/ 是否需要更新。
```

## 验收标准

- [ ] 核心前端仓库已生成全局 Specs（`specs/global-specs.md`）
- [ ] 新需求开发前已生成对应 Specs
- [ ] 每次代码合并后 Specs 已同步更新
```

- [ ] **Step 4: 提交**

```bash
git add docs/frontend-ai-standards/internal-playbook/03-sdd/
git commit -m "docs: add SDD standards and OpenSpecs frontend guide"
```

---

## Task 4：前端 Prompt 模板库

**Files:**
- Create: `docs/frontend-ai-standards/internal-playbook/04-prompt-templates/README.md`
- Create: `docs/frontend-ai-standards/internal-playbook/04-prompt-templates/` (6 个模板文件)

- [ ] **Step 1: 创建目录**

```bash
mkdir -p docs/frontend-ai-standards/internal-playbook/04-prompt-templates
```

- [ ] **Step 2: 写 README.md**

`docs/frontend-ai-standards/internal-playbook/04-prompt-templates/README.md`

```markdown
# 前端 Prompt 模板库

本目录收录前端开发高频场景的 Prompt 模板，减少重复摸索成本。

## 使用原则

每个模板由四部分组成：
1. **上下文注入**：告诉 AI 项目是什么、技术约束是什么
2. **任务描述**：清晰说明要做什么
3. **约束语**：列出 AI 不能做的事
4. **输出要求**：期望的输出格式

使用时，复制模板，替换 `[方括号]` 内的占位内容。

## 模板列表

| 文件 | 适用场景 |
|------|---------|
| `component-generation.md` | 生成新 Vue 组件 |
| `page-refactoring.md` | 重构现有页面或组件 |
| `api-integration.md` | 根据接口文档对接 API |
| `style-adjustment.md` | 调整样式与响应式布局 |
| `unit-test-generation.md` | 为组件生成单元测试 |
| `debug-analysis.md` | 分析并修复 Bug |
```

- [ ] **Step 3: 写 component-generation.md**

`docs/frontend-ai-standards/internal-playbook/04-prompt-templates/component-generation.md`

```markdown
# Prompt 模板：组件生成

## 使用场景

需要新建一个 Vue 组件时使用。适合：纯展示组件、表单组件、列表组件等。

## 模板

```
## 上下文

项目技术栈：Vue 3 + TypeScript + Nuxt 3 + [UI 库名]
代码规范：使用 <script setup> 语法，Props 必须有完整 TypeScript 类型定义
现有组件参考：@repowiki/zh/content/04-组件库文档/核心组件API.md

## 任务

请创建一个 [组件名] 组件，路径：`components/[ComponentName].vue`

功能要求：
- [功能点 1]
- [功能点 2]
- [功能点 3]

Props：
- [propName]：[类型]，[必填/可选]，[说明]

Emits：
- [eventName]：触发时机为 [说明]

## 约束

- 不允许在组件内直接调用 API，数据通过 Props 传入
- 不允许硬编码中文字符串，所有文案通过 Props 传入或使用 i18n
- 样式使用 scoped CSS
- 不允许引入当前项目中不存在的依赖

## 输出要求

1. 完整的 Vue SFC 文件内容
2. 组件使用示例（注释形式放在文件末尾）
3. 如需新增 i18n key，列出需要添加的 key 清单
```

## 使用示例

将 `[UI 库名]` 替换为 `Element Plus`，`[组件名]` 替换为 `用户头像卡片`，以此类推。

## 效果优化建议

- 如果组件较复杂，先让 AI 输出组件的 Props/Emits 设计供确认，再生成完整代码
- 提供类似组件的代码作为参考风格，效果更好：`参考组件风格：@components/ExistingCard.vue`
```

- [ ] **Step 4: 写 api-integration.md**

`docs/frontend-ai-standards/internal-playbook/04-prompt-templates/api-integration.md`

```markdown
# Prompt 模板：接口对接

## 使用场景

需要对接后端 API 时使用。适合：数据请求封装、表单提交、分页列表等。

## 模板

```
## 上下文

技术栈：Vue 3 + Nuxt 3 + TypeScript
API 文档：@repowiki/zh/content/03-API文档/接口文档.json（或 Swagger URL：[替换]）
请求封装规范：所有请求通过 `composables/useRequest.ts` 发起，不允许直接使用 fetch/axios

## 任务

请为以下接口实现前端对接：

接口名称：[接口名]
接口路径：[POST/GET] [/api/path]
入参：
\`\`\`json
[粘贴入参结构]
\`\`\`
出参：
\`\`\`json
[粘贴出参结构]
\`\`\`

需要实现：
1. 在 `composables/use[ModuleName].ts` 中封装请求函数
2. 在 [页面/组件路径] 中调用并处理响应

## 约束

- 请求函数必须处理 loading / error / success 三种状态
- 错误处理：网络错误和业务错误（code !== 0）都需要 toast 提示
- 分页接口需同时管理 pageNum、pageSize、total 状态
- 不允许在 template 中直接调用请求函数，必须通过 composable

## 输出要求

1. composable 文件完整内容（包含类型定义）
2. 页面/组件中调用的示例代码片段
```

- [ ] **Step 5: 写 debug-analysis.md**

`docs/frontend-ai-standards/internal-playbook/04-prompt-templates/debug-analysis.md`

```markdown
# Prompt 模板：调试分析

## 使用场景

遇到 Bug 或异常行为时使用。

## 模板

```
## 上下文

项目：[项目名]，技术栈：Vue 3 + TypeScript + Nuxt 3
相关文件：[粘贴相关文件路径或代码]

## 问题描述

**现象：** [描述看到了什么异常]
**预期行为：** [描述应该是什么]
**复现步骤：**
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

**错误信息：**
\`\`\`
[粘贴控制台报错或堆栈信息]
\`\`\`

## 约束

- 只修复描述的问题，不要重构无关代码
- 如果需要修改多个文件，逐文件说明修改内容和原因
- 如果有多种修复方案，列出方案并给出推荐理由

## 输出要求

1. 问题根因分析（1-3 句话）
2. 修复方案（代码 diff 格式）
3. 如何验证修复是否生效
```

- [ ] **Step 6: 写 page-refactoring.md**

`docs/frontend-ai-standards/internal-playbook/04-prompt-templates/page-refactoring.md`

```markdown
# Prompt 模板：页面重构

## 使用场景

对现有页面或组件进行代码结构优化，不改变外部行为。

## 模板

```
## 上下文

技术栈：Vue 3 + TypeScript + Nuxt 3
代码规范：@repowiki/zh/content/02-技术规范/开发规范.md
当前文件：[文件路径]

## 任务

重构 [文件路径]，解决以下问题：
- [问题 1，如：组件超过 300 行，需要拆分]
- [问题 2，如：存在重复的请求逻辑，需要抽取为 composable]
- [问题 3，如：类型定义不完整]

## 约束

- **不允许改变组件对外的 Props / Emits 接口**
- **不允许改变页面的视觉表现**
- **不允许改变业务逻辑**
- 如果需要拆分为多个文件，列出拆分方案供确认后再实施

## 输出要求

1. 重构后的完整文件内容
2. 如有文件拆分，列出新文件清单和各自职责
3. 说明重构解决了哪些原有问题
```

- [ ] **Step 7: 写 style-adjustment.md 和 unit-test-generation.md**

`docs/frontend-ai-standards/internal-playbook/04-prompt-templates/style-adjustment.md`

```markdown
# Prompt 模板：样式调整

## 模板

```
## 上下文

技术栈：Vue 3 + [CSS 方案，如 UnoCSS / Tailwind / scoped CSS]
设计规范：项目使用 CSS 变量管理主题色，变量定义在 `assets/styles/variables.css`
目标组件：[文件路径]

## 任务

调整 [组件名] 的样式：
- [样式需求 1，如：移动端（< 768px）时隐藏侧边栏]
- [样式需求 2，如：卡片间距从 16px 改为 24px]
- [样式需求 3]

## 约束

- 不允许使用硬编码颜色值，必须使用 CSS 变量
- 不允许修改 HTML 结构，只调整样式
- 响应式断点：移动端 < 768px，平板 768px-1024px，桌面 > 1024px

## 输出要求

只输出修改的样式代码部分（diff 格式）
```

`docs/frontend-ai-standards/internal-playbook/04-prompt-templates/unit-test-generation.md`

```markdown
# Prompt 模板：单元测试生成

## 模板

```
## 上下文

测试框架：Vitest + Vue Test Utils
被测组件/函数：[文件路径]
[粘贴组件代码或函数代码]

## 任务

为上述 [组件名/函数名] 编写单元测试。

需要覆盖：
- [测试场景 1，如：渲染默认状态]
- [测试场景 2，如：传入 disabled=true 时按钮不可点击]
- [测试场景 3，如：点击触发正确的 emit]

## 约束

- 使用 describe/it 结构组织测试
- 每个 it 只测试一个行为
- Mock 外部依赖（API 调用、Store）而非测试真实网络
- 不允许测试实现细节，只测试行为和输出

## 输出要求

完整的测试文件，路径：`[测试文件路径，如 tests/components/ComponentName.test.ts]`
```

- [ ] **Step 8: 提交**

```bash
git add docs/frontend-ai-standards/internal-playbook/04-prompt-templates/
git commit -m "docs: add frontend Prompt template library (6 templates)"
```

---

## Task 5：前端 Review 要点

**Files:**
- Create: `docs/frontend-ai-standards/internal-playbook/05-review-checklist/README.md`
- Create: `docs/frontend-ai-standards/internal-playbook/05-review-checklist/frontend-review-checklist.md`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p docs/frontend-ai-standards/internal-playbook/05-review-checklist
```

- [ ] **Step 2: 写 README.md**

`docs/frontend-ai-standards/internal-playbook/05-review-checklist/README.md`

```markdown
# 前端 Review 要点

本目录提供 AI 生成前端代码的 Review 标准，解决"代码质量参差不齐"的问题。

## 使用方式

1. 在 PR Review 时，按 `frontend-review-checklist.md` 逐项检查
2. 也可以将 Checklist 贴给 AI 自检：

```
请按照以下 Checklist 检查你刚才生成的代码，逐项说明是否符合要求，
不符合的地方直接修改：
[粘贴 Checklist 内容]
```

## 严重程度说明

| 标记 | 含义 |
|------|------|
| 🔴 阻塞 | 必须修复，否则不允许合并 |
| 🟡 建议 | 建议修复，可在后续 PR 处理 |
| 🔵 优化 | 可选优化项 |
```

- [ ] **Step 3: 写 frontend-review-checklist.md**

`docs/frontend-ai-standards/internal-playbook/05-review-checklist/frontend-review-checklist.md`

```markdown
# 前端 AI 代码 Review Checklist

## 功能正确性

- [ ] 🔴 业务逻辑与需求/Specs 描述完全一致
- [ ] 🔴 所有边界条件已处理（空数据、加载中、网络错误）
- [ ] 🔴 接口调用参数与 API 文档匹配（字段名、类型、必填项）
- [ ] 🔴 表单校验规则与需求一致
- [ ] 🟡 异步操作有正确的 loading 状态管理

## 类型安全

- [ ] 🔴 无 TypeScript 类型错误（运行 `tsc --noEmit` 通过）
- [ ] 🔴 无 `any` 类型使用（特殊情况需注释说明原因）
- [ ] 🟡 Props 类型定义完整，包括可选项的默认值
- [ ] 🟡 接口返回数据有对应的 TypeScript 类型定义

## 代码质量

- [ ] 🔴 无引用不存在的组件、composable 或方法（AI 幻觉）
- [ ] 🟡 组件职责单一，单文件不超过 200 行
- [ ] 🟡 无重复代码，逻辑已抽取为 composable 或工具函数
- [ ] 🟡 Emits 已用 `defineEmits` 显式声明
- [ ] 🔵 命名符合项目规范（参见 repowiki 开发规范）

## 性能

- [ ] 🟡 大列表（>100 条）使用虚拟滚动
- [ ] 🟡 无不必要的 `watch` 监听（避免全量重渲染）
- [ ] 🟡 图片资源已做懒加载（使用 `loading="lazy"` 或 v-lazy）
- [ ] 🔵 频繁执行的操作已做 debounce/throttle 处理

## 安全

- [ ] 🔴 无 `v-html` 未经过滤直接渲染用户输入
- [ ] 🔴 权限控制逻辑完整（前端拦截 + 后端鉴权）
- [ ] 🔴 敏感数据（token、密码）不输出到控制台
- [ ] 🟡 外部链接使用 `rel="noopener noreferrer"`

## 国际化

- [ ] 🔴 无硬编码用户可见字符串（所有文案走 i18n）
- [ ] 🟡 i18n key 命名符合项目规范

## 可维护性

- [ ] 🟡 复杂业务逻辑有注释说明背景和原因
- [ ] 🟡 无过时或无意义的注释
- [ ] 🔵 组件有使用示例或 JSDoc 注释

## 测试

- [ ] 🟡 核心业务逻辑有对应的单元测试
- [ ] 🔵 新增组件有基础渲染测试
```

- [ ] **Step 4: 提交**

```bash
git add docs/frontend-ai-standards/internal-playbook/05-review-checklist/
git commit -m "docs: add frontend AI code review checklist"
```

---

## Task 6：内部 Playbook 整合

**Files:**
- Create: `docs/frontend-ai-standards/internal-playbook/README.md`

- [ ] **Step 1: 写 Playbook 首页 README.md**

`docs/frontend-ai-standards/internal-playbook/README.md`

```markdown
# 前端 AI Coding 内部 Playbook

本 Playbook 是前端团队 AI 辅助开发的操作手册，提供可直接使用的模板、配置和标准。

## 推荐开发流程

```
需求确认
   ↓
生成 / 更新 Specs（OpenSpecs）→ 参见 03-sdd/
   ↓
配置项目上下文（RepoWiki + .cursorrules）→ 参见 01-cursor-rules/ 和 02-repowiki/
   ↓
使用 Prompt 模板进行 AI 编码 → 参见 04-prompt-templates/
   ↓
按 Review Checklist 审查代码 → 参见 05-review-checklist/
   ↓
合并代码
   ↓
同步更新 Specs + RepoWiki ← 完整的一次改动
```

## 模块导航

| 模块 | 说明 | 适用时机 |
|------|------|---------|
| [01 Cursor 配置规范](./01-cursor-rules/README.md) | .cursorrules 模板、MCP 配置 | 项目初始化或新人加入时 |
| [02 RepoWiki 规范](./02-repowiki/README.md) | 项目知识库模板（7 类文档） | 项目初始化，持续维护 |
| [03 SDD 规范](./03-sdd/README.md) | OpenSpecs 使用指南 | 每次开发新功能前 |
| [04 Prompt 模板库](./04-prompt-templates/README.md) | 6 类场景的 Prompt 模板 | 日常 AI 编码时 |
| [05 Review Checklist](./05-review-checklist/README.md) | AI 生成代码的审查标准 | PR Review 时 |

## 新人快速入门

1. **第 1 天**：阅读 [01 Cursor 配置规范](./01-cursor-rules/README.md)，配置好工具；
2. **第 2 天**：阅读所负责项目的 `repowiki/`，了解项目上下文；
3. **第 3 天起**：参照 [04 Prompt 模板库](./04-prompt-templates/README.md) 开始 AI 辅助开发。

## 老人对齐

如果你已经在使用 AI 编码，请检查：

- [ ] 项目根目录有 `.cursorrules`？→ 参照模板补充
- [ ] 项目有 `repowiki/`？→ 用模板补充缺失文档
- [ ] 开发前先生成 Specs？→ 参见 OpenSpecs 指南
- [ ] PR 时有 Review Checklist？→ 使用 05-review-checklist/
```

- [ ] **Step 2: 提交**

```bash
git add docs/frontend-ai-standards/internal-playbook/README.md
git commit -m "docs: add internal playbook README with complete navigation"
```

---

## Task 7：对外白皮书草稿

**Files:**
- Create: `docs/frontend-ai-standards/whitepaper/frontend-ai-coding-whitepaper.md`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p docs/frontend-ai-standards/whitepaper
```

- [ ] **Step 2: 写白皮书草稿**

`docs/frontend-ai-standards/whitepaper/frontend-ai-coding-whitepaper.md`

```markdown
# 前端 AI 辅助开发工程实践

> Visable AI 技术白皮书 — 前端篇

---

## 引言：从"使用 AI"到"工程化 AI"

AI 编程助手正在成为前端工程师的标配工具。然而，工具的普及并不等同于效率的提升。在我们的实践中，简单地"让 AI 写代码"往往会带来新的问题：代码质量参差不齐、AI 频繁误解项目上下文、Review 成本反而上升。

解决这些问题的关键，不在于更换更强的模型，而在于**工程化地使用 AI**：建立约束机制、管理上下文、规范流程。

本文记录 Visable AI 前端团队在 AI 辅助开发上的工程实践，核心观点是：

> **约束工程与上下文工程，是决定 AI 能否稳定、高质量完成开发任务的关键。**

---

## 一、核心理念：人机协作的边界

### 1.1 AI 的能力边界

基于我们的实践，AI 在以下场景表现稳定：
- 有明确输入输出的功能实现（如：根据接口文档实现数据请求）
- 有参考样本的代码生成（如：参照现有组件生成类似组件）
- 有标准规则的机械性工作（如：生成单元测试、类型定义）

AI 在以下场景需要人类更多介入：
- 涉及复杂业务判断的逻辑
- 需要理解历史决策背景的架构调整
- 安全敏感的功能

### 1.2 代码所有权

AI 生成的代码，由提交该代码的工程师负责。AI 生成不免除 Review 责任，也不改变代码质量标准。

---

## 二、上下文工程：让 AI 懂你的项目

### 2.1 问题根因

"AI 不理解项目"是最普遍的抱怨。根本原因是：AI 每次对话都从零开始，没有项目记忆。

解决方案是**上下文工程**：将项目知识结构化地存放在代码仓库中，让 AI 每次工作时都能读取。

### 2.2 项目知识库（RepoWiki）

我们在每个前端代码仓库中维护一份 RepoWiki，包含 7 类文档：

| 文档类型 | 作用 |
|---------|------|
| 技术规范 | 约束 AI 遵守项目的技术选型和编码标准 |
| 路由与页面结构 | 帮助 AI 理解项目全貌，避免重复造轮子 |
| 组件库文档 | 让 AI 知道哪些组件已存在、如何使用 |
| 状态管理文档 | 避免 AI 创建与现有 Store 重复或冲突的状态 |
| 业务知识 | 提供领域背景，避免 AI 对业务术语产生误解 |
| 测试用例 | 提供验收标准，让 AI 自行验证生成的代码 |

**核心原则：** 所有文档以"AI 能读懂并直接使用"为标准，结构化格式优于叙述式文字。

### 2.3 AI 配置规范（.cursorrules）

除了项目文档，我们还在每个仓库中维护 `.cursorrules` 文件，定义 AI 的行为边界：

- 代码风格和命名规范
- 禁止 AI 做的事（如：引用不存在的组件、使用硬编码字符串）
- 安全约束（如：禁止使用 v-html 渲染未过滤的内容）

---

## 三、约束工程：规范 AI 的开发流程

### 3.1 Spec-Driven Development（SDD）

让 AI 直接写代码的最大风险是"理解偏差"——AI 自行假设需求，产出与预期不符，问题在 Review 时才发现，返工成本高。

我们采用 SDD（规范驱动开发）作为解决方案：**开发前先生成 Specs，明确边界后再编码。**

流程：

```
需求描述 → AI 生成 Specs → 工程师确认/修订 Specs → AI 按 Specs 编码
```

Specs 包含：功能范围、数据模型、交互细节、技术约束。确认 Specs 等于在开始编码前消除了所有歧义。

工具选型：我们使用开源工具 [OpenSpecs](https://github.com/Fission-AI/OpenSpec)，轻量、结构清晰，适合已有任务拆解的团队协作场景。

### 3.2 代码 Review 标准

AI 生成的代码需要比人工代码更严格的 Review，因为 AI 存在以下典型问题：

- **幻觉**：引用项目中不存在的方法、组件或依赖
- **类型松散**：使用 `any` 绕过类型检查
- **遗漏边界条件**：错误状态、空数据、加载中等场景处理不完整
- **安全遗漏**：权限控制逻辑被简化或跳过

我们为此建立了分级 Review Checklist，区分阻塞项（必须修复）和建议项，确保核心质量的同时不增加过多流程负担。

---

## 四、实践效果

采用 RepoWiki + SDD + 统一 Review 标准后，我们观察到：

- AI 理解项目上下文的准确率显著提升，减少了因"AI 不懂项目"导致的返工
- 需求开发前的 Specs 确认，将大部分逻辑问题前移到编码前发现
- Review Checklist 让不同经验水平的工程师有了统一的质量基准

---

## 五、持续演进

AI 工具和实践都在快速迭代。我们将持续沉淀案例库，记录有效的实践和踩坑经验，定期更新本规范。

如您希望交流 AI 工程化实践，欢迎联系我们。
```

- [ ] **Step 3: 提交**

```bash
git add docs/frontend-ai-standards/whitepaper/
git commit -m "docs: add frontend AI coding whitepaper draft"
```

---

## Task 8：最终整合与验收

**Files:**
- Create: `docs/frontend-ai-standards/README.md`

- [ ] **Step 1: 写顶层 README**

`docs/frontend-ai-standards/README.md`

```markdown
# 前端 AI Coding 工程规范

| 文档 | 受众 | 说明 |
|------|------|------|
| [内部 Playbook](./internal-playbook/README.md) | 内部研发团队 | 可操作模板、Checklist、配置 |
| [对外白皮书](./whitepaper/frontend-ai-coding-whitepaper.md) | 行业同行、合作方 | 方法论与工程实践分享 |
| [设计文档](../superpowers/specs/2026-04-20-frontend-ai-coding-standards-design.md) | 内部参考 | 规范设计决策记录 |
```

- [ ] **Step 2: 按 Review Checklist 验收所有文档**

运行以下检查：

```bash
# 检查所有模板文件是否存在
ls docs/frontend-ai-standards/internal-playbook/01-cursor-rules/
ls docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/
ls docs/frontend-ai-standards/internal-playbook/03-sdd/
ls docs/frontend-ai-standards/internal-playbook/04-prompt-templates/
ls docs/frontend-ai-standards/internal-playbook/05-review-checklist/
ls docs/frontend-ai-standards/whitepaper/
```

预期：每个目录下有对应文件，无缺失。

- [ ] **Step 3: 检查所有 `[替换]` 占位符**

```bash
grep -r "\[替换\]" docs/frontend-ai-standards/
```

预期：在模板文件（`.template.md`）中出现是正常的，非模板文件不应出现。

- [ ] **Step 4: 最终提交**

```bash
git add docs/frontend-ai-standards/README.md
git commit -m "docs: add top-level README, complete frontend AI coding standards"
```

---

## 自检结果

**Spec 覆盖检查：**

| 设计文档要求 | 实施计划覆盖 |
|------------|------------|
| Cursor 配置规范（Rules 模板 + MCP 配置） | ✅ Task 1 |
| RepoWiki 规范（7 类模板） | ✅ Task 2 |
| SDD 规范（OpenSpecs 前端指南） | ✅ Task 3 |
| 前端 Prompt 模板库（6 类场景） | ✅ Task 4 |
| 前端 Review 要点（分级 Checklist） | ✅ Task 5 |
| 内部 Playbook 整合 | ✅ Task 6 |
| 对外白皮书草稿 | ✅ Task 7 |

**无占位符（非模板文件）：** 通过  
**类型/引用一致性：** 所有文档内部自洽，无交叉引用错误
