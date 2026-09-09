# spec — 实现者持有的技术方案

- 需求名 / ID：FE-1042 — cr-frontend: detect SSR-unsafe usage of client-only APIs
- 状态：confirmed（2026-08-28 用户选「确认，含顺手修正」） # draft / confirmed——confirmed 必须来自用户明确同意；变更由 harness-change 降回

## 需求边界

- 做什么（来自 Jira FE-1042）：
  - 在 cr-frontend 的审查规则里新增 SSR-safety 检查：SSR 执行上下文中的**未防护**客户端 API 访问（`window`/`document`/`localStorage`/`sessionStorage`/`navigator` 等）→ 🔴 Must Fix
  - 发现项必须附带具体修复指引：`typeof window === 'undefined'` / `import.meta.client` 守卫、移入 `onMounted` 等客户端生命周期、模板用 `<ClientOnly>` 包裹
  - 已正确防护的写法不得误报（AC2）
  - 修改位置：`references/rules/vue3.md` 与 `frontend-standards.md`（即 `plugins/visable-fe-ai/rules/*.mdc` 源 + `skills/cr-frontend/references/rules/*.md` 生成副本，共 4 个文件）
- 不做什么（明确排除）：
  - 不改 SKILL.md 工作流（Step 5 高危信号表、Step 8 评估注册表保持原样——新规则经由现有 Step 7「Scan by Dimension」生效，无需改流程）
  - 不改 react.md（Jira 只点名 vue3 / frontend-standards）
  - 不做插件版本号升级（仓库惯例是独立 chore 提交，如 #7）
  - 不新建/修复 sync-rules.sh 同步脚本（脚本不在本仓库，属遗留问题，另行处理）

## 方案

- 思路：规则双落点分工——`frontend-standards`（cr-frontend Step 2 **必读**、globs 覆盖 `**/*.{ts,vue}`）放框架中立的通用规则，保证 `.ts`（composables/plugins/middleware/模块顶层）与任何项目形态都被覆盖；`vue3` 放 Nuxt/Vue 专属细节（`<ClientOnly>` fallback slot、`import.meta.client`/`process.client`、生命周期语义、`.client` 文件约定、可选链≠守卫的陷阱）。
- 影响文件 / 模块（4 个文件，两两内容同步）：
  1. `plugins/visable-fe-ai/rules/frontend-standards.mdc` — 新增 `## SSR Safety` 节（3 条）+ `## Severity Reference` 补一句 Must Fix 场景
  2. `plugins/visable-fe-ai/skills/cr-frontend/references/rules/frontend-standards.md` — 同步（保留 AUTO-GENERATED 头）
  3. `plugins/visable-fe-ai/rules/vue3.mdc` — 新增 `## SSR Safety` 节（放在 Lifecycle 之后）
  4. `plugins/visable-fe-ai/skills/cr-frontend/references/rules/vue3.md` — 同步
- md 与 mdc 手工同步（仓库无 sync 脚本；头部注释的 `plugins/rules/` 路径已过时，本次顺手把 4 个 md 头部的过时路径修正为 `plugins/visable-fe-ai/rules/`，去掉不存在的 sync-rules.sh 引用——1 行/文件，减少后人误导）
- 风险与取舍：
  - 两个规则文件存在少量内容重叠（守卫白名单），接受——frontend-standards 保证无条件加载覆盖，vue3 提供 Vue 细节；Jira 明确要求双落点
  - 误报控制依赖「守卫白名单」写死在规则里（typeof 检查 / import.meta.client / onMounted 内 / `<ClientOnly>` / `.client` 文件）；并显式写明可选链 `window?.x` 不是守卫（未声明标识符仍抛 ReferenceError），防审查者放过这种伪防护

### 规则内容草案

**frontend-standards（新增节，置于 Severity Reference 之前）：**

> ## SSR Safety
>
> - Do not access browser-only globals (`window`, `document`, `localStorage`, `sessionStorage`, `navigator`, `screen`, `matchMedia`, …) in code that also executes during SSR: module top-level scope, `setup()` / composable bodies, and Nuxt/Vue plugins & middleware. *(severity: 🔴 Must Fix — unguarded access throws "X is not defined" on the server, breaking SSR with render errors / blank screens)*
> - Accept as guarded (do NOT flag): `typeof window === 'undefined'` (or `typeof document`) check, `import.meta.client` (Nuxt 3) / `process.client` (Nuxt 2) condition, access inside client-only lifecycle callbacks (`onMounted` / `onUnmounted`), or a `<ClientOnly>` template wrapper. Nuxt `*.client.ts` plugins never execute on the server.
> - Every finding must include a concrete fix: add a `typeof window === 'undefined'` / `import.meta.client` guard, move the access into `onMounted`, or wrap the template part with `<ClientOnly>` (with SSR fallback markup).

Severity Reference 节追加：unguarded browser-global access in SSR-executed code 列入 Must Fix 场景。

**vue3（新增节，置于 Lifecycle 之后）：**

> ## SSR Safety
>
> - Do not access browser-only APIs (`window`, `document`, `localStorage`, `sessionStorage`, `navigator`, `matchMedia`, `requestAnimationFrame`, `IntersectionObserver`, `ResizeObserver`, …) in code that also runs during SSR: `<script setup>` top level, synchronous composable bodies, Nuxt plugins/middleware, module scope, and `computed` getters evaluated during server render. *(severity: 🔴 Must Fix)*
> - Server/client execution semantics: `setup()` top level and `computed` getters run on the server; `onMounted` / `onUnmounted` callbacks are client-only — access inside them is safe.
> - Accepted guards (do NOT flag): `typeof window === 'undefined'` early return/branch; `import.meta.client` (Nuxt 3) / `process.client` (Nuxt 2); access moved into `onMounted` / `onUnmounted`; template wrapped in `<ClientOnly>` with SSR fallback in the default or `#fallback` slot; client-only file conventions (`plugins/*.client.ts`, `*.client.vue`).
> - Optional chaining is NOT a guard: `window?.localStorage` still throws `ReferenceError` during SSR — `window` is an undeclared identifier on the server; only `typeof` checks are safe for undeclared globals.
> - Every finding must carry concrete fix guidance: (1) guard with `typeof window === 'undefined'` or `import.meta.client`; (2) move the access into `onMounted` / client-only lifecycle; (3) wrap template usage with `<ClientOnly>` + fallback; (4) for Nuxt plugins that need no server run, rename to `*.client.ts`.

## 计划

> 任务分解见 plan.md（spec confirmed 后派生）。

## 验收边界（实现者视角）

- 可观测行为：
  1. 含未防护 `localStorage.getItem` 的 composable 顶层 diff，按新规则判为 Must Fix 且附具体修复建议（模拟评测：子代理只读更新后的规则 + 样例 diff 做分类，AC1）
  2. `typeof window` / `import.meta.client` / `onMounted` 内访问 / `<ClientOnly>` 包裹四种守卫样例均不触发（同上评测，AC2）
  3. mdc 源与 md 副本内容一致（除 frontmatter/生成头）
  4. `bash <kit>/harness validate` 全绿
- 遗留申报：4 个 md 头部过时路径修正是顺手项，如用户不同意可回退

## 变更记录

- 2026-08-28 创建（draft），待用户确认
