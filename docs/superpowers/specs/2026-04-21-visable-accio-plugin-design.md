# Visable Accio Plugin 技术实现方案

**日期**：2026-04-21  
**作者**：Visable AI Team  
**状态**：草稿待评审

---

## 一、背景与目标

Accio Work 推出 Plugin 系统，允许第三方业务以标准化 Plugin 包的形式接入，用户可在 Accio 桌面端 Marketplace 安装、授权并绑定到 Agent 使用。

本方案目标是将 Visable 的核心业务能力（店铺诊断、商品优化、Business Insight）封装为符合 Accio Plugin 规范的标准插件，通过三阶段方式完成从零到生产可发布版本的完整闭环。

### P0 成功标准

- Accio Marketplace 可查到 `visable-assistant` 插件
- 用户可完成「OAuth 授权 → 下载安装 → 绑定 Agent」全流程
- 三个 Skill（店铺诊断、商品优化、Business Insight）均可通过 MCP 工具调用 Visable 真实数据
- CI 可通过打 Tag 自动产出 `plugin.zip` 并触发版本登记

---

## 二、方案选择

**方案三：一体化集成方案（已选定）**

以"从零到第一次端到端成功安装"为主线，MCP Server 与 Plugin 结构同步串行推进，分三阶段交付。不拆分为并行工作流，避免因 connectors.json 与 MCP Server URL 解耦导致集成风险。

---

## 三、Plugin 能力层说明

### 3.1 Accio Plugin 支持的能力层

Accio Plugin 系统支持多种能力接入方式，各层独立可用，也可按需组合：

| 能力层 | 接入方式 | 核心文件 | 是否需要外部服务 |
|---|---|---|---|
| **Agent** | 定义 Agent 身份、人格、行为规范 | `agent.json`、`agents.md`、`identity.md` 等 | 不需要 |
| **Skill** | SKILL.md 指导 Agent 用内置工具（bash、write、browser 等）完成任务 | `SKILL.md` | 不需要 |
| **CLI 工具** | 通过 `dependencies.json` 声明 npm 包，脚本在用户本机执行 | `dependencies.json` | 不需要 |
| **Connector（MCP）** | 注册 MCP Server，Agent 通过 Accio MCP Gateway 调用后端服务 | `connectors.json` | 需要部署 MCP Server |
| **Resource** | 静态资源（图标、引导配置等） | `resources/` | 不需要 |

文档中标注的「最简单」接入示例（Vibe Selling）仅包含 `plugin.json + agents + skills`，没有任何 MCP — 说明 **MCP 不是 Plugin 的必须项**。

---

### 3.2 Agent + Skill 方式 vs Connector（MCP）方式对比

| 维度 | Agent + Skill（纯本地） | Connector（MCP） |
|---|---|---|
| **数据来源** | LLM 自身知识 + 用户本机工具（bash、文件、浏览器） | 调用后端真实业务数据 |
| **部署成本** | 零 — Plugin 仓库自包含，无需部署任何服务 | 需要单独部署并维护 MCP Server |
| **认证管理** | 复杂 — token 需在脚本或文件中手动管理，安全性低 | Accio MCP Gateway 统一管理 OAuth token，每次调用自动注入 |
| **数据实时性** | 无法获取实时数据 | 可实时调用后端 API，数据准确 |
| **维护成本** | 低（只维护 SKILL.md 和脚本） | 中（需维护 Plugin 仓库 + MCP Server 两个仓库） |
| **适用场景** | 内容生成、文案优化、本地文件操作、不需要账号数据的任务 | 需要读取/操作用户账号真实数据的任务 |
| **扩展性** | 差 — 逻辑分散在脚本中，难以统一管理 | 好 — 工具集中在 MCP Server，易于扩展和版本管理 |

---

### 3.3 Visable 选择 MCP 方式的原因

Visable 三个核心 Skill 的数据需求如下：

| Skill | 数据需求 | 能否用纯 Skill 实现 |
|---|---|---|
| `store-diagnosis` | 需要读取真实店铺流量、转化率、健康度数据 | 不能 — 数据在 Visable 后端 |
| `product-optimization` | 需要读取现有商品详情，才能给出针对性优化建议 | 部分不能 — 纯文案生成可以，但脱离真实商品则无意义 |
| `business-insight` | 需要读取历史经营数据、竞品信息，生成趋势分析 | 不能 — 数据在 Visable 后端 |

基于以上分析，**选择 Connector（MCP）方式**的具体理由：

1. **业务数据强依赖**：三个 Skill 的核心价值都在于"基于用户真实数据给出洞察"，没有真实数据则退化为通用 LLM 回复，失去差异化价值。
2. **认证安全性（Skill 脚本方案的根本缺陷）**：Skill 中虽然可以通过 bash 工具执行脚本（如 Node.js `fetch`、`curl`）来调用 Visable REST API，但这意味着用户的 Visable token 必须存储在用户本机（本地文件或环境变量），存在 token 泄露风险。MCP 方式将 token 完全交由 Accio MCP Gateway 持有和注入，用户机器上不存储任何凭证，安全性本质上更高。
3. **环境可控性**：Skill 脚本方案的请求从用户本机发出，依赖用户的 Node/Python 版本、网络环境，调试复杂且行为不一致。MCP 方式请求由 Accio MCP Gateway 统一发出，环境由 Accio 管控，稳定性更高。
4. **长期可维护性**：MCP Server 将 API 调用逻辑集中管理，后续 Visable REST API 变更时只需更新 MCP Server，无需重新打包发布 Plugin。Skill 脚本方案则需要同步修改 SKILL.md 和脚本并重新发版。
5. **符合 Accio 推荐路径**：Okki（小满）的生产接入方案同样采用 MCP + OAuth 方式，是 Accio 验证过的可靠路径。

> **补充说明**：Skill 脚本（bash fetch）和 CLI 工具（`dependencies.json` 声明的 npm 包）并非同一层。前者是 Agent 使用内置 bash 工具执行临时脚本；后者是 Plugin 安装时在用户机器上预装的 npm 包，供脚本调用。两者都属于"本地执行"范畴，同样面临上述 token 安全问题，不适合 Visable 的数据接入场景。

---

## 四、整体架构

### 4.1 双仓库结构

| 仓库 | 职责 | 发布方式 |
|---|---|---|
| `visable-plugin` | Plugin 静态配置资产：agent、skills、connectors、resources | Git Tag → CI → plugin.zip → Accio 版本登记 |
| `visable-mcp-server` | MCP Server HTTP 服务，包装 Visable REST API | Docker 镜像 → 独立部署，提供稳定 HTTPS URL |

**连接点**：`connectors/connectors.json` 中的 `mcpServers.url` 指向 MCP Server 部署地址。

### 4.2 Plugin 仓库目录结构

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
│           │   └── SKILL.md
│           ├── product-optimization/
│           │   └── SKILL.md
│           └── business-insight/
│               └── SKILL.md
├── connectors/
│   └── connectors.json
├── dependencies/
│   └── dependencies.json
├── resources/
│   ├── agent-logo.svg
│   └── recommend.json
└── .github/
    └── workflows/
        └── release.yml
```

### 4.3 MCP Server 仓库目录结构

```
visable-mcp-server/
├── server.py
├── tools/
│   ├── store_diagnosis.py
│   ├── product_optimization.py
│   └── business_insight.py
├── auth/
│   └── oauth.py
├── requirements.txt
└── Dockerfile
```

### 4.4 整体数据流

```
用户对话
  └─→ visable-assistant (Agent)
        └─→ agents.md 消歧 → 选定 Skill
              └─→ 读取 SKILL.md，执行工具调用
                    └─→ Accio MCP Gateway（Accio 托管）
                          └─→ visable-mcp-server（Visable 部署）
                                └─→ Visable REST API
```

### 4.5 认证链路（ON_INSTALL）

```
用户点击安装
  └─→ Accio 触发 OAuth 授权流程
        └─→ 跳转 Visable 授权页（authorization_url）
              └─→ 用户登录 Visable 账号，完成授权
                    └─→ 回调 Accio MCP Gateway（redirect_uri）
                          └─→ Gateway 换取并缓存 access_token
                                └─→ 后续每次 MCP 调用自动注入 Authorization Header
```

---

## 四、核心配置文件设计

### 4.1 plugin.json

```json
{
  "name": "visable-assistant",
  "displayName": "Visable 助手",
  "version": "0.1.0",
  "description": "Visable 业务助手：店铺诊断、商品优化与业务洞察（需完成 Visable 账号授权）",
  "author": "Visable",
  "icon": "resources/agent-logo.svg",
  "category": "e-commerce",
  "tags": ["visable", "store", "product", "b2b", "insight"]
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
    { "type": "prefix", "pattern": ["browser"], "decision": "ask" }
  ],
  "catalogSkillIds": [
    "store-diagnosis",
    "product-optimization",
    "business-insight"
  ],
  "onboarding": "resources/recommend.json"
}
```

### 4.3 connectors.json

```json
{
  "mcpServers": {
    "visable-server": {
      "type": "stream",
      "url": "https://mcp.visable.com/mcp"
    }
  },
  "oauth": {
    "visable": {
      "adapter": "mcp-oauth",
      "toolName": "start_visable_oauth",
      "enabled": true,
      "authorization_url": "https://auth.visable.com/authorize",
      "token_url": "https://auth.visable.com/token",
      "scopes": ["openid", "profile", "store:read", "product:read", "analytics:read"]
    }
  }
}
```

### 4.4 MCP 工具返回格式约定

所有 MCP 工具返回统一格式（Accio 要求）：

```json
{
  "success": true,
  "errorCode": null,
  "errorMsg": null,
  "data": { }
}
```

---

## 五、三阶段实施计划

### Phase 1：Plugin 骨架 + MCP Server 基础

**目标**：Plugin 结构完整可识别，MCP Server 本地可调通至少 1 个工具

| # | 任务 | 产出 |
|---|---|---|
| 1 | 创建 `visable-plugin` 仓库，初始化完整目录结构 | Git 仓库 |
| 2 | 填写 `plugin.json`、`agent.json` | 插件清单 |
| 3 | 编写 `agents.md`（三个 Skill 消歧规则） | Agent 行为规范 |
| 4 | 编写 `identity.md`、`soul.md`、`bootstrap.md`、`user.md` | Agent 人格文件 |
| 5 | 编写三个 `SKILL.md`（触发条件 + 执行步骤） | Skill 说明 |
| 6 | 编写 `recommend.json`（每 Skill 2-3 条示例提示词） | Onboarding 引导 |
| 7 | 创建 `visable-mcp-server` 仓库，用 FastMCP 搭框架 | MCP Server 骨架 |
| 8 | 实现第一个工具：`get_store_overview` | 可调通的 MCP 工具 |

**验收**：Plugin 目录合规；MCP Server 本地启动，`get_store_overview` 返回正确格式 JSON。

---

### Phase 2：OAuth 打通 + Connector 接入

**目标**：用户可在 Accio 测试环境完成「授权 → 安装 → 绑定 Agent」全流程

| # | 任务 | 产出 |
|---|---|---|
| 1 | Visable 后端创建 OAuth App，配置 `authorization_url`、`token_url`、`redirect_uri` | OAuth App |
| 2 | 在 `redirect_uri` 白名单配置 Accio MCP Gateway 回调地址 | OAuth 白名单 |
| 3 | MCP Server 增加 token 验证中间件（读取 Authorization Header） | 认证中间件 |
| 4 | 将 MCP Server 部署到测试环境，提供稳定 HTTPS URL | 测试环境服务 |
| 5 | 用真实地址填写 `connectors.json` | 完整 Connector 配置 |
| 6 | 向 Accio 申请 Plugin 注册，获取 `pluginId` | pluginId |
| 7 | 在 Accio 测试环境走完整安装链路 | 联调验证 |

**验收**：授权弹窗正常 → 安装成功 → 绑定 Agent → `get_store_overview` 返回真实数据。

---

### Phase 3：Skills 填充 + CI 发布流水

**目标**：三个 Skill 完整可用，CI 自动产出 plugin.zip，生产版本可登记

#### Skill 与 MCP 工具对照

| Skill | 触发场景 | MCP 工具 |
|---|---|---|
| `store-diagnosis` | 诊断店铺/看健康度/流量分析 | `get_store_overview`、`get_traffic_analysis`、`get_conversion_funnel` |
| `product-optimization` | 优化商品/改标题/写描述/关键词建议 | `get_product_detail`、`suggest_title`、`suggest_description` |
| `business-insight` | 数据趋势/竞品分析/生成业务报告 | `get_business_metrics`、`get_competitor_analysis`、`generate_report` |

#### CI Pipeline（release.yml 核心逻辑）

```yaml
on:
  push:
    tags:
      - 'v*.*.*'
jobs:
  release:
    steps:
      - 打包 plugin.zip（排除 .git、.github）
      - 生成 manifest.snapshot.json
      - 计算 sha256
      - 上传制品到对象存储
      - 向 phoenix-gateway 发起版本登记回调
```

**验收**：打 `v1.0.0` Tag → CI 绿色 → Accio Marketplace 可查到版本 → 三个 Skill 均正常。

---

## 六、缺失信息 & 需向 Accio 确认的问题

### 第一类：Plugin 注册与发布流程

1. **Plugin 注册方式**：自助注册还是需要提工单/联系同学人工注册？注册后 `pluginId` 格式是什么？
2. **CI 回调接口**：`phoenix-gateway` 版本登记的 endpoint、请求体字段（`pluginId`、`version`、`sha256`、`artifactUrl` 等）、鉴权方式（签名 / API Key）是什么？
2a. **认证策略字段位置**：`policy_authentication = ON_INSTALL` 是在 CI 回调请求体里传，还是在 `plugin.json` 里声明，还是在 Accio 后台手动配置？
3. **对象存储**：`plugin.zip` 上传到哪里？Accio 提供 bucket 还是我们自己的 OSS 均可？需要申请什么权限？
4. **测试 / 预发环境**：是否有独立的 Plugin 测试环境可供联调？对应 `phoenix-gateway` 测试域名是什么？
5. **Diamond 操作权限**：版本登记成功后，Visable 侧是否可自己操作 Diamond 推版本到测试环境，还是需要 Accio 运维操作？

### 第二类：Connector / MCP / OAuth 接入

6. **MCP Gateway 地址**：测试和生产环境的 MCP Gateway 地址分别是什么？我们的 MCP Server URL 需要在哪里注册？
7. **OAuth redirect_uri**：Accio MCP Gateway 在 OAuth 授权完成后的 `redirect_uri` 是什么？需要提前配置到 Visable OAuth App 白名单。
8. **`adapter` 字段枚举**：`connectors.json` 中 `oauth.adapter` 除 `mcp-oauth` 外还支持哪些类型？
9. **`toolName` 命名规范**：`start_visable_oauth` 是我们自己起名还是需要在 Accio 侧注册？有没有命名约束？
10. **MCP Server 部署要求**：公网可达？内网白名单？是否强制 HTTPS？证书有要求吗？

### 第三类：Agent 与 Skill 配置

11. **`catalogSkillIds` 来源**：填写 Plugin 内部 Skill 目录名（如 `store-diagnosis`），还是需要在技能市场注册后拿到平台分配的 ID？
12. **`agentType` 唯一性**：`visable-assistant` 需要提前在 Accio 注册，还是 Plugin 仓库自定义即可？有没有全局冲突检测？
13. **`policyRules` 安全规范**：调用 MCP 工具的 Agent，Accio 是否有推荐的 policyRules 配置规范或文档？

### 第四类：版本管理与止血

14. **版本状态流转**：从 `REGISTERED` 到 `RELEASE_READY` 需要经过什么审核？预计需要多长时间？
15. **止血流程**：线上版本出问题时，Visable 侧需要执行什么操作？是否有自助的 Diamond 回切入口？

### 第五类：时间节点与接入 SLA

16. **Plugin 系统当前状态**：测试环境是否已经可以接受接入方联调？
17. **接入 SLA**：从 Plugin 注册申请到 Marketplace 可见，预计需要多久完成审核流程？
