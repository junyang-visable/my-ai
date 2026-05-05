# Visable × Accio Plugin 技术方案（Plugin + Agent + Skill 模式）

**版本**：v2.0  
**日期**：2026-04-21  
**作者**：Visable AI Team  
**方案定位**：轻量接入方案，无需部署 MCP Server，通过 Browser Session 实现认证

---

## 一、方案概述

### 核心认证思路（参考阿里国际站发品 Skill）

本方案的认证逻辑借鉴阿里国际站 `alibaba-publish-skill` 的成熟模式：

> **不存储 token 到本机文件，而是通过 `browser` 工具打开 Visable 平台页面，Agent 从浏览器 Session 中直接提取认证凭证，再用同源 `fetch` 在浏览器控制台执行 API 调用。**

这样做的好处：
- 浏览器 Session/Cookie 自动携带用户登录态，无需手动管理 token
- 同源 fetch 调用天然受浏览器安全策略保护
- 用户只需正常登录 Visable，无需额外授权步骤

### 与 MCP 方案的对比

| 维度 | 本方案（Skill + Browser） | MCP 方案 |
|---|---|---|
| **是否需要部署服务** | ❌ 不需要 | ✅ 需要部署 MCP Server |
| **认证方式** | Browser Session + 同源 fetch | OAuth 2.0 + MCP Gateway 管理 token |
| **Token 存储位置** | 浏览器内存（不落本机文件） | Accio Gateway（最安全） |
| **上线速度** | 快（1-2 周） | 慢（3-4 周） |
| **用户操作** | 需在 Visable 平台保持登录 | 一次 OAuth 授权，后续无感知 |
| **适合阶段** | MVP 验证、快速上线 | 正式生产环境 |

---

## 二、用户体验

### 安装流程

```
Marketplace 搜索「Visable 助手」→ 安装 → 绑定 Agent → 开始使用
（无 OAuth 弹窗，无需手动填写 token）
```

### 对话流程（以店铺诊断为例）

```
用户：帮我诊断一下店铺最近30天的表现

Agent：正在打开 Visable 平台，检查您的登录状态...
[browser 工具打开 https://seller.visable.com]
[检测到已登录，提取 Session Token]
[执行 fetch 获取店铺数据]

📊 店铺健康诊断报告
健康评分：78/100
近30天询盘：340 单 ↑12%
近30天订单：28 单 ↓3%

关键发现：
1. 点击转化率 8.5%，低于行业均值 12%
2. 推荐流量近期下滑 18%，需关注商品质量

优先建议：...
```

---

## 三、整体架构

### 3.1 单仓库结构

```
visable-plugin/
├── plugin.json
├── agents/
│   └── visable-assistant/
│       ├── agent.json
│       ├── agents.md
│       ├── identity.md
│       ├── soul.md
│       ├── bootstrap.md
│       ├── user.md
│       └── skills/
│           ├── store-diagnosis/
│           │   ├── SKILL.md
│           │   └── references/
│           │       └── api-endpoints.md      ← Visable API 地址备忘
│           ├── product-optimization/
│           │   └── SKILL.md                  ← 纯 LLM，无 browser
│           └── business-insight/
│               ├── SKILL.md
│               └── references/
│                   └── api-endpoints.md
├── connectors/
│   └── connectors.json                       ← mcpServers 为空
├── dependencies/
│   └── dependencies.json                     ← 无额外依赖
├── resources/
│   ├── agent-logo.svg
│   └── recommend.json
└── .github/workflows/
    └── release.yml
```

### 3.2 数据链路

```
用户对话
  │
  ▼
visable-assistant (Agent)
  │  agents.md 分析意图，选定 Skill
  ▼
SKILL.md
  │  Step 1：指导 Agent 用 browser 工具打开 Visable 平台
  ▼
browser 工具（用户本机浏览器）
  │  检测登录态 → 提取 Session Token
  ▼
browser console（同源 fetch）
  │  携带 Session Cookie，调用 Visable API
  ▼
Visable REST API
  │
  ▼
[Result] JSON 数据返回
  │
  ▼
Agent 解析数据，生成诊断报告
```

### 3.3 认证流程

```
Agent 打开 Visable 卖家平台（browser 工具）
  │
  ├── 已登录（检测到 Session Token）
  │     └── 直接执行数据查询脚本
  │
  └── 未登录
        └── 跳转登录页：https://login.visable.com
              └── 每 5 秒轮询一次登录状态
                    └── 登录成功 → 继续执行
```

---

## 四、核心配置文件

### 4.1 connectors.json

本方案不依赖 MCP，`mcpServers` 为空，`oauth` 也不需要配置：

```json
{
  "mcpServers": {},
  "oauth": {}
}
```

### 4.2 agent.json

```json
{
  "name": "Visable 助手",
  "description": "为 Visable 用户提供店铺诊断、商品优化和业务洞察的智能助手",
  "avatar": "resources/agent-logo.svg",
  "model": { "provider": "auto", "name": "auto" },
  "agentType": "visable-assistant",
  "toolPreset": "full",
  "policyRules": [
    { "type": "prefix", "pattern": ["write"], "decision": "allow" },
    {
      "type": "prefix",
      "pattern": ["browser"],
      "decision": "ask",
      "justification": "需要打开 Visable 平台获取您的真实数据"
    }
  ],
  "catalogSkillIds": [
    "store-diagnosis",
    "product-optimization",
    "business-insight"
  ],
  "onboarding": "resources/recommend.json"
}
```

---

## 五、三个 Skill 的实现方式

### 5.1 分类

| Skill | 实现方式 | 是否使用 browser |
|---|---|---|
| `product-optimization`（商品优化） | 纯 LLM，用户提供商品信息即可生成 | ❌ 不需要 |
| `store-diagnosis`（店铺诊断） | Browser Session + 同源 fetch | ✅ 需要 |
| `business-insight`（业务洞察） | Browser Session + 同源 fetch | ✅ 需要 |

---

### 5.2 store-diagnosis SKILL.md

````markdown
---
name: store-diagnosis
description: 店铺健康度诊断：分析流量来源、转化漏斗、整体店铺表现
triggers:
  - 诊断店铺
  - 店铺健康度
  - 流量分析
  - 转化率分析
---

# 店铺诊断技能

## 核心原则
- **接口优先**：直接在浏览器控制台调用 Visable API，不操作页面 UI。
- **健壮性封装**：所有 JS 脚本必须包裹在 `(async () => { ... })()` 中，严禁顶层 `await`。
- **显式结果返回**：所有 console 输出必须带 `[Result]` 前缀，便于 Agent 精准解析。
- **数据完整性**：工具调用失败时立即返回，不用估算数据替代。

## 执行步骤

### 第 1 步：环境与登录态检查

使用 `browser` 工具打开 Visable 卖家平台：
- **目标域名**：`https://seller.visable.com`
- **Token 提取**：检查 `window.__VISABLE_SESSION__?.token` 或 `localStorage.getItem('visable_token')`

在浏览器控制台执行以下脚本检查登录态：

```javascript
(async () => {
  const token = window.__VISABLE_SESSION__?.token || localStorage.getItem('visable_token');
  if (!token) {
    return "[Result] " + JSON.stringify({ status: "failed", reason: "NOT_LOGGED_IN" });
  }
  return "[Result] " + JSON.stringify({ status: "ok", tokenPrefix: token.substring(0, 8) + "..." });
})()
```

**若返回 `NOT_LOGGED_IN`**：
→ 引导至登录页：`https://login.visable.com`，每 5 秒轮询一次，直到登录成功。

### 第 2 步：获取店铺概览

登录态确认后，执行以下脚本获取数据：

```javascript
(async () => {
  const token = window.__VISABLE_SESSION__?.token || localStorage.getItem('visable_token');
  if (!token) return "[Result] " + JSON.stringify({ status: "failed", reason: "NOT_LOGGED_IN" });

  try {
    const res = await fetch("https://seller.visable.com/api/v1/store/overview?period=30d", {
      headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" }
    });
    const data = await res.json();
    if (!data.success) return "[Result] " + JSON.stringify({ status: "failed", reason: data.errorCode, msg: data.errorMsg });
    return "[Result] " + JSON.stringify({ status: "ok", data: data.data });
  } catch (e) {
    return "[Result] " + JSON.stringify({ status: "error", message: e.message });
  }
})()
```

### 第 3 步：获取流量分析

```javascript
(async () => {
  const token = window.__VISABLE_SESSION__?.token || localStorage.getItem('visable_token');
  try {
    const res = await fetch("https://seller.visable.com/api/v1/store/traffic?period=30d", {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();
    return "[Result] " + JSON.stringify({ status: "ok", data: data.data });
  } catch (e) {
    return "[Result] " + JSON.stringify({ status: "error", message: e.message });
  }
})()
```

### 第 4 步：获取转化漏斗

```javascript
(async () => {
  const token = window.__VISABLE_SESSION__?.token || localStorage.getItem('visable_token');
  try {
    const res = await fetch("https://seller.visable.com/api/v1/store/funnel", {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();
    return "[Result] " + JSON.stringify({ status: "ok", data: data.data });
  } catch (e) {
    return "[Result] " + JSON.stringify({ status: "error", message: e.message });
  }
})()
```

### 第 5 步：综合输出诊断报告

基于以上三组数据，按以下结构输出：

```
## 店铺健康诊断报告

### 总体评分
[综合评分及核心问题]

### 流量分析
| 来源 | 占比 | 环比 |
|------|------|------|
| ...  | ...  | ...  |

### 转化漏斗
| 环节 | 转化率 | 行业基准 |
|------|--------|----------|
| ...  | ...    | ...      |

### 优先行动建议
1. [最高优先级，含预期效果]
2. [次优先级]
```

## 错误转译表

| 原始错误码 | 用户侧描述 | 建议操作 |
|---|---|---|
| `NOT_LOGGED_IN` | **未登录** | 请先登录 Visable 卖家平台 |
| `PERMISSION_DENIED` | **权限不足** | 当前账号无权访问该数据，请确认账号类型 |
| `DATA_NOT_READY` | **数据还未准备好** | 新账号需要7天以上经营数据，请稍后再试 |
````

---

### 5.3 business-insight SKILL.md

````markdown
---
name: business-insight
description: 业务洞察：数据趋势分析、竞品对比、经营简报生成
triggers:
  - 业务洞察
  - 数据趋势
  - 竞品分析
  - 生成报告
  - 经营简报
---

# Business Insight 技能

## 核心原则
与 store-diagnosis 相同：接口优先、健壮性封装、显式结果返回。

## 执行步骤

### 第 1 步：环境与登录态检查（与 store-diagnosis 相同）

### 第 2 步：获取业务指标

```javascript
(async () => {
  const token = window.__VISABLE_SESSION__?.token || localStorage.getItem('visable_token');
  const period = "30d"; // 可由用户指定，默认30d
  try {
    const res = await fetch(`https://seller.visable.com/api/v1/analytics/metrics?period=${period}`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();
    return "[Result] " + JSON.stringify({ status: "ok", data: data.data });
  } catch (e) {
    return "[Result] " + JSON.stringify({ status: "error", message: e.message });
  }
})()
```

### 第 3 步：获取竞品数据（如用户需要）

```javascript
(async () => {
  const token = window.__VISABLE_SESSION__?.token || localStorage.getItem('visable_token');
  const category = "用户指定的品类";
  try {
    const res = await fetch(`https://seller.visable.com/api/v1/analytics/competitors?category=${encodeURIComponent(category)}&period=30d`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();
    return "[Result] " + JSON.stringify({ status: "ok", data: data.data });
  } catch (e) {
    return "[Result] " + JSON.stringify({ status: "error", message: e.message });
  }
})()
```

### 第 4 步：生成报告并保存本地

使用 `write` 工具将完整报告保存到：
`~/visable-reports/YYYY-MM-DD-business-insight.md`

### 第 5 步：输出报告摘要（格式同 store-diagnosis）
````

---

### 5.4 product-optimization SKILL.md（纯 LLM，无 browser）

````markdown
---
name: product-optimization
description: 商品标题、描述、关键词优化（基于用户提供信息，无需调用接口）
triggers:
  - 优化商品
  - 改标题
  - 写描述
  - 关键词建议
---

# 商品优化技能

## 说明
本技能不调用任何 API，完全基于 LLM 能力对用户提供的商品信息进行优化。
适合快速生成文案，不依赖 Visable 账号登录状态。

## 执行步骤

### 第 1 步：收集商品信息
询问用户以下信息（未提供的逐一追问）：
- 当前标题
- 主要类目
- 核心卖点（3-5 条）
- 目标市场（国家/地区）

### 第 2 步：生成 3 个标题优化版本
每个版本说明：加入了哪些关键词、针对哪类买家、优化了哪个维度。

### 第 3 步：生成优化后的描述框架
结构：开篇价值主张 → 功能特点分点 → 行动号召

### 第 4 步：输出关键词建议表

| 关键词 | 类型 | 加入建议 |
|--------|------|----------|
| ...    | 核心词/长尾词 | 加入标题/描述/标签 |
````

---

## 六、子代理执行规范（Anti-Loop）

参考阿里国际站发品 Skill 的子代理规范，以下规则同样适用于 Visable Skill：

| 规则 | 说明 |
|---|---|
| **拒绝碎片化测试** | 严禁用 `({ status: 'test' })` 等探测脚本分步调试，应一次性执行完整 IIFE 模板 |
| **显式结果前缀** | 所有 console 输出必须带 `[Result]` 前缀，便于 Agent 精准解析 JSON |
| **提前终止** | 登录态检查失败时立即返回，不进入后续数据查询逻辑 |
| **父代理上下文同步** | 使用子代理时，父代理必须将完整 JS 模板和 API 地址写入 task 参数，子代理无法自动读取 SKILL.md |

---

## 七、发布流水线

与 MCP 方案完全相同（无服务部署步骤，更简单）：

```
开发者在 visable-plugin 打 Tag（v1.0.0）
  │
  ▼
GitHub Actions：
  打包 plugin.zip → sha256 → 上传制品 → 向 Accio 版本登记
  │
  ▼
Accio 审核 → Diamond 推送 → Marketplace 上线 ✅
```

---

## 八、方案局限性与升级路径

### 当前局限

| 问题 | 说明 |
|---|---|
| **需要浏览器打开** | 每次数据查询都要打开 Visable 平台页面，用户体验不如 MCP 方案流畅 |
| **依赖网页 Token 结构** | `window.__VISABLE_SESSION__?.token` 的位置需向 Visable 前端团队确认，网页改版可能导致失效 |
| **无法后台静默运行** | browser 工具需要打开界面，无法在用户无感知的情况下定时获取数据 |
| **browser 弹窗确认** | `policyRules` 中 browser 设为 `ask`，每次需用户确认 |

### 升级到 MCP 方案的时机

当以下任一条件满足时，建议升级：
- 用户反馈"每次都要打开浏览器太麻烦"
- 需要支持定时报告（无感知后台运行）
- Visable 网页改版导致 Token 提取失效
- 需要更高安全标准（token 不能在浏览器 console 中可见）

**升级时两个方案可无缝衔接**：Plugin `name`（`visable-assistant`）和 `agentType` 保持不变，用户不感知迁移。

---

## 九、当前阻塞项（需确认）

### 需向 Visable 前端团队确认

| # | 问题 | 影响 |
|---|---|---|
| 1 | `window.__VISABLE_SESSION__?.token` 是否是正确的 Token 提取路径？ | Skill 脚本能否正确认证 |
| 2 | Visable 卖家平台的 API 基础路径是否为 `https://seller.visable.com/api/v1`？ | 所有 fetch 调用 |
| 3 | API 是否支持同源 fetch（无 CORS 限制）？ | 浏览器内 fetch 是否可行 |

### 需向 Accio 确认

| # | 问题 | 影响 |
|---|---|---|
| 4 | `mcpServers` 为空时，Plugin 仍可正常安装和使用？ | 方案可行性 |
| 5 | `browser` 工具打开的页面是否有域名白名单限制？ | 能否打开 seller.visable.com |
| 6 | Plugin 注册方式、CI 回调接口（与 MCP 方案相同问题） | 发布流程 |

---

## 十、技术栈总结

| 组件 | 选型 |
|---|---|
| Plugin 仓库 | JSON + Markdown |
| 数据获取 | browser 工具 + 浏览器控制台 JavaScript（IIFE 封装）|
| 认证 | 浏览器 Session Token（无需手动管理） |
| 内容生成 | LLM（product-optimization 纯 LLM，无依赖） |
| CI | GitHub Actions |

---

*相关文档：[MCP 方案技术概览](./2026-04-21-visable-accio-plugin-overview.md) · [完整技术设计方案](./2026-04-21-visable-accio-plugin-design.md)*
