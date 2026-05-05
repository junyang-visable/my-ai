# =============================================================================
# 项目基础信息（请按实际填写）
# =============================================================================
# 项目名称: [替换: 项目中文/英文名称]
# 技术栈: Vue 3 + Nuxt 3 + TypeScript + Pinia
# UI 组件库: [替换: 例如 Element Plus / Naive UI / 自研组件库]
# 设计规范 / Repowiki: repowiki/
# =============================================================================

## 组件规范

- 使用 Vue 3 Composition API；新组件一律使用 `<script setup lang="ts">`。
- 组件文件名、单文件组件的 `name`（若需）使用 PascalCase，与导出一致。
- 单个 `.vue` 文件建议不超过 400 行；超出时拆分子组件或抽取 composable / 工具函数。
- Props 必须显式声明类型：使用 `defineProps` 配合 TypeScript 类型或 `withDefaults`；禁止仅依赖运行时 prop 定义而无类型。
- Emits 必须使用 `defineEmits` 声明事件名及载荷类型；调用处与声明保持一致。
- 优先组合式函数抽取可复用逻辑；避免在多个组件中复制粘贴相同逻辑。

## TypeScript 规范

- 导出函数、composable 的返回值、复杂数据结构必须有明确类型注解。
- 禁止使用 `any`；确属未知结构时使用 `unknown` 并做窄化，或使用泛型约束。
- 对象形状优先使用 `interface` 扩展与合并；联合类型、交叉类型、工具类型场景使用 `type`。
- 枚举优先使用 `const enum` 或字面量联合类型，避免运行时枚举体积与反向映射问题（团队有统一枚举策略时从其规定）。

## 状态管理（Pinia）

- Store 放在约定目录（如 `stores/`），按领域拆分；文件名与 store id 使用清晰、一致的命名（如 `useUserStore`）。
- 禁止在组件中直接赋值修改 store 的 state；变更须通过 store 的 action 完成；批量字段更新应在 action 内部使用 `$patch`，不要从组件调用 `$patch`。
- Getter 保持纯函数语义；异步与副作用放在 action 中。

## 样式规范

- 组件样式使用 `<style scoped>`（或 CSS Modules / 团队约定方案），避免全局污染。
- 颜色、间距、圆角等使用 CSS 变量或设计 Token，禁止在业务组件中硬编码十六进制色值（除非设计 Token 未覆盖且已评审）。
- 响应式使用项目统一的断点变量或 mixin；避免魔法数字媒体查询散落各处。

## API 与数据获取

- HTTP 与接口封装集中在 composables 或 `services/` / `api/` 等约定层，禁止在展示组件内直接 `fetch` 或散落 axios 调用。
- Nuxt 中优先使用 `useFetch` / `useAsyncData`（及 `$fetch`）与项目封装；保持 key、服务端/客户端行为一致。
- 统一错误处理与用户可见提示策略（toast、错误边界、日志）；不要静默吞掉错误。

## 国际化（i18n）

- 用户可见文案禁止硬编码中文/英文长句在模板与脚本中；使用 i18n key。
- Key 命名使用分段、小写与连字符或点分命名（与项目现有 `locales` 结构一致），例如 `module.feature.action`。

## 安全规范

- 禁止未经消毒的 `v-html`；若必须使用，数据须来自可信后端或经 DOMPurify 等方案处理，并记录评审依据。
- 禁止将 token、密钥、PII 等敏感数据存入 `localStorage` / `sessionStorage`；遵循团队鉴权与存储方案。
- 前端路由与 UI 权限展示不能替代后端鉴权；敏感操作必须由后端校验。

## 注释规范

- 只注释「为什么」、非显而易见的约束、与性能/安全相关的权衡；禁止复述代码语义的无效注释。
- 公共 composable、复杂业务规则可写简短说明；避免大段注释掉的死代码。

## AI 行为约束

- 修改或新增代码前，先阅读项目内的 repowiki/ 架构说明（路径：repowiki/INDEX.md）。
- 不要引用不存在的组件、composable 或路径；以仓库中实际文件为准。
- 保持与现有代码相同的格式化风格、命名与目录约定；不擅自引入新状态管理或新 HTTP 客户端除非任务要求。
- 对需求、接口契约或边界不确定时，先列出假设或向使用者确认，不要猜测业务规则。
- 交付前须通过 TypeScript 类型检查（`vue-tsc` / `nuxi typecheck` 或项目等价命令）；不留下已知类型错误。

## SDD 流程纪律

- 收到新需求时，**必须先确认存在已评审通过的 Spec**（在 `specs/` 或 `openspec/changes/` 下）后，才能创建或修改 `.vue`、`.ts`、`.css` 等业务实现文件；Spec 尚未确认前只允许产出文档。
- 生成 Spec 或制订实施计划前，**必须先读 `repowiki/INDEX.md`** 并按索引阅读相关章节（至少：技术规范、路由与页面结构），以仓库实际结构为准，禁止凭空推断路径或 Store 名称。
- 实现方案不明确时，须先调用 `superpowers:brainstorming` 探方案（HARD-GATE：设计文档未产出并获用户确认前，禁止调用任何实现技能）。
- Spec 确认后进入实施阶段，须按 Superpower 节奏执行：`writing-plans`（结合 repowiki/ 生成分步计划）先于任何代码改动；计划确认后由 `subagent-driven-development` 或 `executing-plans` 执行；全部任务完成后须运行 `verification-before-completion` 再宣布完成。
- 宣布完成或提 PR 前，**禁止跳过验证步骤**；如无法运行验证命令，须向使用者说明原因。
- 功能合并进主分支后，同步更新 `repowiki/` 中受影响的章节（路由、状态、业务知识等）及对应 `specs/` 文件；未更新视为交付不完整。
