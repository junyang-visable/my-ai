# 接口对接 Prompt 模板

## 使用场景

在前端接入新的或已有的 **HTTP 接口**：封装类型安全的请求函数、统一错误与加载态、列表分页等。项目约定**所有请求经 composable 层**（如 `composables/useRequest.ts` 或团队统一封装），**不在模板或任意组件内散落 `fetch`/axios**。

---

## Prompt 模板

````markdown
## 上下文

- 所有数据请求必须通过项目的统一请求封装完成，入口为：`[替换：如 composables/useRequest.ts 或 composables/api/useHttpClient.ts]`；**禁止**在 `.vue` 的 template 或随意位置直接调用 `fetch` / `axios` / `$fetch`（除非团队规范明确允许的极少数场景，此处默认不允许）。
- 技术栈：Nuxt 3、TypeScript；错误提示使用项目统一的 Toast / notification（`[替换：如 useToast、ElMessage]`）。
- 相关已有类型或枚举（可粘贴）：`[替换：可选]`

## 任务

实现接口 **`[替换：接口业务名称]`**：

- 方法与环境路径：`[替换：GET|POST|PUT|DELETE] [替换：/api/v1/...]`
- 请求体 / Query 参数结构（JSON 或表格说明）：

```json
[替换：请求 JSON 示例或 {}]
```

- 响应体结构（JSON 示例，含列表分页字段若存在）：

```json
[替换：响应 JSON 示例]
```

- 业务说明：`[替换：幂等性、是否需要携带 Token、特殊 Header、调用场景]`

## 约束

1. 调用方应能区分 **loading / error / success** 三种状态（Composable 返回 ref 或对象字段，或返回可 `await` 的函数并在内部维护状态，与项目现有模式一致）。
2. **错误时**使用统一 Toast 展示用户可读信息；必要时同时 `console.error` 或接入日志规范（按项目惯例）。
3. 若为列表接口：**分页状态**（page、pageSize、total、列表数据）应在 composable 内集中管理，提供 `refresh`、`loadMore` 或 `setPage` 等与现有列表页一致的方法命名。
4. **禁止在 Vue 模板中写请求调用**；模板只绑定 composable 暴露的数据与方法。
5. TypeScript：为请求参数与响应体定义 `interface` 或 `type`；避免 `any`。

## 输出要求

1. **完整的 composable 文件源码**（路径建议：`[替换：如 composables/api/useXxxQuery.ts]`），含类型定义与导出函数。
2. **在 Vue 组件中的使用片段**（`<script setup>` 内如何引入、如何绑定 loading/error/list 到模板）。
3. 若需 Pinia 协同：说明数据应留在 composable 还是 store，并给出推荐做法的一句话理由。
````

---

## 效果优化建议

- **粘贴真实 JSON**：响应里字段命名、嵌套、分页字段名（`items` vs `list`）务必与后端一致，减少对接偏差。
- **对齐现有 composable**：先打开一个同目录下已有接口文件，在「上下文」中写明「模仿 `useYyy.ts` 的写法」，风格更统一。
- **401 / 网络失败**：若项目有全局拦截器，在「约束」中注明「业务 composable 内不重复处理 401」，避免双重 Toast。
- **Mock / 联调**：可要求输出附带「临时 mock 数据」或 MSW 片段（若团队使用），便于前后端并行。
