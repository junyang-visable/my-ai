# 项目差异速览

| 项目 | 安装依赖 | 启动命令 | 快速路由 |
|------|----------|----------|----------|
| supplier-onboarding-frontend | `pnpm install` | `pnpm dev` | `localhost:3000/en/company-editor/<supplier-id>/basic-info` |
| business-insights-frontend | `yarn install` | `yarn dev` | `localhost:3000/en/my-account/business-insights/<supplier-id>` |
| visitors-frontend | `npm install` | `npm run dev` | `localhost:3000/en/my-account/visitors/<supplier-id>` |
| ad-center-frontend | `npm install` | `npm run dev` | `localhost:3000/en/campaigns/<supplier-id>` |
| product-editor-frontend | `pnpm install` | `pnpm dev` | `localhost:3000/en/my-account/supplier/<supplier-id>/products-services` |
| customer-dashboard-frontend | `pnpm install` | `pnpm dev` | `localhost:3000/en/company-overview/<supplier-id>` |

执行 skill 时由用户提供 `<supplier-id>`；未提供时 Agent 会询问。所有项目均需注入 `_user_session` 登录态，无需手动复制 cookie 或操作 DevTools。
