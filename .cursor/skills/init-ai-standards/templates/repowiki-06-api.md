# 06 — API 文档

> 本章记录前端消费的所有后端接口约定：请求封装、鉴权方式、接口目录与错误码规范。
> AI 在生成或修改接口调用代码时，**必须先查阅本章**，不得凭空猜测路径或参数。

---

## 基础配置

| 项 | 值 | 说明 |
|----|-----|------|
| Base URL（生产） | [替换: https://api.example.com] | |
| Base URL（测试） | [替换: https://api-staging.example.com] | |
| 超时时间 | [替换: 10000ms] | 超时后统一 toast 提示 |
| 请求封装文件 | [替换: src/utils/request.ts] | 所有接口调用**必须**经过此封装，禁止裸调 `fetch` / `axios` |
| 全局请求头 | [替换: Content-Type: application/json; 其余见鉴权节] | |

---

## 鉴权方式

| 场景 | 方案 | 实现位置 |
|------|------|----------|
| 登录态携带 | [替换: Bearer Token / Cookie Session] | [替换: 封装层 interceptor 自动注入] |
| Token 刷新 | [替换: 401 时静默刷新 / 跳登录页] | [替换: request.ts 响应拦截器] |
| 无需鉴权的接口 | [替换: 白名单列表或不加 Authorization Header] | [替换] |

> **注意**：Token 存储位置与生命周期以 `05-状态管理.md` 中 `useUserStore` 的约定为准。

---

## API 模块列表

> 按业务域分组，每组单独一节。未确认的接口用「待确认」标注，禁止编造。

| 模块 | 路径前缀 | 负责后端 | 文档链接 |
|------|----------|----------|----------|
| [替换: 用户模块] | [替换: /api/v1/users] | [替换: @后端负责人] | [替换: Swagger/Apifox 链接] |
| [替换: 业务模块 A] | [替换: /api/v1/xxx] | [替换] | [替换] |
| [替换: 业务模块 B] | [替换: /api/v1/yyy] | [替换] | [替换] |

---

## 接口文档示例：用户模块

> 以下为完整示例；实际项目请复制本节结构为每个模块补充一节，或拆为独立文件。

### `POST /api/v1/auth/login`

| 项 | 内容 |
|----|------|
| 描述 | 账号密码登录，返回 Token |
| 鉴权 | 不需要 |

**请求体**

```ts
interface LoginRequest {
  email: string;
  password: string;
}
```

**响应体**

```ts
interface LoginResponse {
  token: string;
  refreshToken: string;
  user: UserProfile;
}
```

**错误码**

| code | 含义 | 前端处理 |
|------|------|----------|
| 401001 | 账号或密码错误 | toast 提示「账号或密码不正确」 |
| 429 | 登录频率限制 | toast 提示「请求过于频繁，请稍后重试」 |

---

### `GET /api/v1/users/me`

| 项 | 内容 |
|----|------|
| 描述 | 获取当前登录用户信息 |
| 鉴权 | Bearer Token |

**响应体**

```ts
interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'member' | [替换: '其他角色'];
  [替换: 其他字段];
}
```

---

## 全局错误码约定

| HTTP 状态 / 业务 code | 含义 | 前端统一处理 |
|----------------------|------|-------------|
| 400 | 请求参数校验失败 | toast 显示 `message` 字段 |
| 401 | 未登录 / Token 失效 | 静默刷新失败后跳转登录页 |
| 403 | 权限不足 | toast 提示「暂无权限，请联系管理员」 |
| 404 | 资源不存在 | 页面级 404 或 toast（按上下文） |
| 500 | 服务器错误 | toast 提示「服务异常，请稍后重试」并上报监控 |
| [替换: 业务 code] | [替换: 含义] | [替换: 处理方式] |

> 统一处理逻辑实现位置：[替换: src/utils/request.ts 响应拦截器]

---

## Mock 与本地开发

| 项 | 方案 | 说明 |
|----|------|------|
| Mock 工具 | [替换: MSW / Vite Mock Plugin / Apifox Mock] | [替换: 启动命令或配置文件路径] |
| 开启方式 | [替换: .env.local 中设置 VITE_USE_MOCK=true] | |
| Mock 文件位置 | [替换: src/mocks/] | |
| 数据来源约定 | [替换: 与后端 Apifox / Swagger 保持同步] | 前端不自行维护随意 Mock 数据 |

---

## 类型定义位置

| 类别 | 路径 | 说明 |
|------|------|------|
| 请求 / 响应 DTO | [替换: src/types/api/] | 与后端契约同步，不在组件内内联定义 |
| 通用响应包装 | [替换: src/types/common.ts] | 如 `ApiResponse<T>`、分页 `PageResult<T>` |
| 枚举 / 字典值 | [替换: src/types/enums.ts] | 禁止在多处硬编码同一枚举值 |

---

## AI 使用提示

- 新增接口调用前，先确认本章是否已记录该接口；若无，标注「待确认」并通知人工补充。
- 修改接口路径或参数类型时，**同步更新本章**，避免文档与代码漂移。
- 涉及鉴权敏感接口时，同步核对 `05-状态管理.md` 中 Token 相关逻辑。

---

- 维护人：[替换]
- 最后更新：[替换: YYYY-MM-DD]
