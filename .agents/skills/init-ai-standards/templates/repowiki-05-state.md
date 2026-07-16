# 05 — 状态管理（Pinia）

## Store 列表

| Store ID | 文件路径 | 职责 |
|----------|----------|------|
| `useUserStore` | [替换: stores/user.ts] | 登录态、当前用户资料 |
| [替换: useXxxStore] | [替换] | [替换] |
| [替换] | [替换] | [替换] |

---

## 示例文档：`useUserStore`

> 以下为完整示例；实际项目请复制本节结构为每个 Store 写一节或拆文件。

### State

| 字段 | 类型 | 初始值 | 说明 |
|------|------|--------|------|
| `user` | `User \| null` | `null` | 当前登录用户；未登录为 `null` |
| `token` | `string \| null` | `null` | 访问令牌；持久化策略见注意事项 |
| `isLoading` | `boolean` | `false` | 登录 / 拉取资料中的全局加载态 |

### Getters（如有）

| Getter | 返回值 | 说明 |
|--------|--------|------|
| `isLoggedIn` | `boolean` | `!!token && !!user` |
| [替换] | [替换] | [替换] |

### Actions

| Action | 参数 | 行为 |
|--------|------|------|
| `login` | `credentials: { email: string; password: string }` | 调登录接口，写入 `token` 与 `user` |
| `logout` | — | 清 `token` / `user`，跳转登录页 |
| `fetchProfile` | — | 用当前 `token` 拉取用户详情并更新 `user` |

### 注意事项

- **持久化**：`token` 是否写入 `localStorage` / Cookie 以安全方案为准；禁止把刷新令牌明文暴露在可被 XSS 读取的位置（按团队安全基线执行）。
- **并发**：`fetchProfile` 与 `login` 可能并发时需防抖或 `isLoading` 互斥，避免状态错乱。
- **SSR**：若使用 Nuxt，`localStorage` 仅在客户端可用；初始化逻辑放在 `onMounted` 或客户端插件中。
- **与路由守卫关系**：未登录时由 [替换: middleware] 读取 `useUserStore` 决定是否放行。

---

## 跨 Store 依赖

| 场景 | 推荐做法 |
|------|----------|
| Store A 需要 Store B | [替换: 在 action 内 `useBStore()` / 或上提 composable] |
| 派生状态 | [替换: 优先 getter / composable，避免重复存一份] |

---

- 维护人：[替换]
- 最后更新：[替换: YYYY-MM-DD]
