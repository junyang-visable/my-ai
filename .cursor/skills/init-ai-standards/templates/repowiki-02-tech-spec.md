# 02 — 技术规范

## 核心技术栈

| 技术 | 版本（约定） | 说明 |
|------|----------------|------|
| Vue | 3.x | 组合式 API 为主；选项式仅遗留代码 |
| Nuxt | 3.x | [替换: 如非 Nuxt 项目，改为 Vite / 其他并删此行] |
| TypeScript | 5.x | `strict` 建议开启；新文件必须为 `.ts` / `.vue` + `<script setup lang="ts">` |
| Pinia | 2.x | 全局状态唯一推荐方案 |
| UI 组件库 | [替换: 如 Element Plus / Naive UI] | 版本：[替换]；定制主题路径：[替换] |
| CSS 方案 | [替换: 如 Tailwind / UnoCSS / SCSS Modules] | 全局变量与断点定义位置：[替换] |
| 单元测试 | Vitest | 1.x |
| E2E | Playwright | 1.x |

## 命名规范

| 类别 | 规范 | 示例 |
|------|------|------|
| 组件文件 / 注册名 | PascalCase | `UserAvatar.vue` |
| 页面路由路径 | kebab-case | `/user-profile` |
| Composable | camelCase，`use` 前缀 | `useTableQuery.ts` |
| Pinia Store | camelCase；导出 `useXxxStore` | `useUserStore` |
| 样式类名 / BEM | kebab-case | `block__element--modifier` |
| 常量 | UPPER_SNAKE_CASE | `MAX_UPLOAD_SIZE` |

## 目录规范

业务仓库以团队约定为准；以下为 **Nuxt 3 / 常见 Vue 项目** 的参考结构，请按实际调整并列在表中。

```text
src/
├── assets/           # 静态资源（图片、字体）；大资源走 CDN 需注明
├── components/       # 通用与业务组件；可按 domain 分子目录
├── composables/      # useXxx 逻辑复用
├── pages/            # 文件系统路由（Nuxt）或 views（Vite）
├── stores/           # Pinia stores
├── utils/            # 纯函数、request 封装、格式化
├── types/            # 全局 TS 类型、与后端契约
└── [替换: 其他如 middleware/, plugins/, layouts/]
```

| 路径 | 用途 | 禁止 |
|------|------|------|
| `components/` | 可复用 UI | 不写仅单次使用的巨型页面组件（应下沉到 `pages` 或拆子组件） |
| `utils/request` | HTTP 封装 | 业务页面直接 `fetch` 绕过封装（除非 Wiki 明确例外） |

## 性能要求

| 指标 | 目标 | 说明 |
|------|------|------|
| LCP | < 2.5s | 核心列表页 / 首页在标准网络下的目标 |
| FID / INP | FID < 100ms（或 INP 按团队口径） | 交互响应；具体以监控定义为准 |
| Bundle Size | [替换: 如 main chunk < 300KB gzip] | 超阈值需拆包或懒加载并登记原因 |
| 度量工具 | [替换: Lighthouse CI / RUM / 自建] | 报告位置或 Dashboard：[替换] |

## 代码风格与工具

| 项 | 约定 |
|----|------|
| Lint / Format | [替换: ESLint + Prettier 配置路径] |
| Git 提交 | [替换: Conventional Commits / 内部规范] |
| 环境变量 | 前缀 `[替换: NUXT_PUBLIC_ / VITE_]`；密钥不得入库 |

## AI / 协作提示

- 新增文件时**先查**本目录与 `INDEX` 是否已有同类模式，避免重复造轮子。
- 性能敏感路径（首屏、大列表）变更时，更新本页「性能要求」或链接到专项文档。

---

- 维护人：[替换]
- 最后更新：[替换: YYYY-MM-DD]
