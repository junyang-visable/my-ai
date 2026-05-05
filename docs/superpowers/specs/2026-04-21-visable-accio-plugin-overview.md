# Visable × Accio Plugin 技术方案

**版本**：v1.0  
**日期**：2026-04-21  
**作者**：Visable AI Team

---

## 一、我们在做什么

### 一句话说清楚

> 把 Visable 的核心业务能力（店铺诊断、商品优化、Business Insight）打包成一个 **Accio Plugin**，让用户在 Accio Work 桌面端安装授权后，可以直接通过 AI Agent 对话的方式使用 Visable 的数据能力。

### 用户会看到什么

用户在 Accio Work 的 Marketplace 里找到「Visable 助手」，点击安装 → 完成 Visable 账号授权 → 绑定到 Agent → 开始对话：

```
用户：帮我诊断一下店铺最近30天的表现
Agent：正在获取您的店铺数据...

📊 店铺健康诊断报告
综合评分：78/100，主要问题集中在点击转化率偏低。

流量来源：搜索 45%↑、推荐 30%↓、直接 25%
转化漏斗：曝光→点击 8.5%（行业均值 12%，存在差距）

优先建议：
1. 优化主力商品的搜索关键词，预计提升点击率 15-20%
2. 检查推荐位商品图片质量，近期推荐流量下滑明显
3. 跟进 3 个高意向询盘，转化窗口期在本周内
```

---

## 二、为什么要做 Plugin，而不是别的形式

Accio Work 的 Plugin 系统支持三种能力接入方式：

| 接入方式 | 说明 | 适合场景 |
|---|---|---|
| **Agent + Skill** | 纯 LLM + 内置工具（bash、文件等） | 内容生成、文档处理、不需要账号数据的任务 |
| **CLI 工具** | npm 包在用户本机执行脚本 | 本地开发工具、无需用户身份的数据 |
| **Connector（MCP）** | 通过 MCP Gateway 调用后端服务，token 由平台管理 | **需要读取用户账号真实数据** |

**Visable 必须走 MCP 方式**，原因有三：

1. **业务核心是真实数据**：店铺健康度、转化漏斗、竞品分析——这些数据在 Visable 后端，LLM 无法自行生成，没有真实数据则功能无意义。

2. **安全性**：如果用脚本方式调接口，用户的 Visable token 必须存在本机，存在泄露风险。MCP 方式由 Accio MCP Gateway 统一持有和注入 token，用户机器上不存储任何凭证。

3. **可维护性**：API 工具逻辑集中在 MCP Server，Visable 接口变更时只需更新服务，不需要重新打包发布 Plugin。

---

## 三、整体技术架构

### 3.1 两个仓库，一条数据链路

```
[visable-plugin 仓库]              [visable-mcp-server 仓库]
  Plugin 配置包                       Python HTTP 服务
  agent.json                          FastMCP 框架
  SKILL.md × 3                        9 个 MCP 工具
  connectors.json ─────────────────→  包装 Visable REST API
  
  Git Tag → CI → plugin.zip           Docker 镜像 → 独立部署
  → Accio 版本登记                     → 提供 HTTPS URL
```

**两个仓库的连接点**：`connectors.json` 里的 MCP Server URL，仅此一处耦合。

### 3.2 完整数据链路

```
用户对话
  │
  ▼
visable-assistant (Agent)
  │  agents.md 分析意图，选定 Skill
  ▼
SKILL.md（店铺诊断 / 商品优化 / Business Insight）
  │  指导 Agent 调用对应 MCP 工具
  ▼
Accio MCP Gateway（Accio 托管）
  │  自动注入 Authorization: Bearer <token>
  ▼
visable-mcp-server（Visable 部署）
  │  验证 token，调用业务接口
  ▼
Visable REST API
  │
  ▼
返回真实业务数据
```

### 3.3 认证链路（用户视角）

```
用户点击「安装 Visable 助手」
  │
  ▼
弹出 Visable 授权页（标准 OAuth 2.0）
  │
  ▼
用户用 Visable 账号登录并授权
  │
  ▼
授权完成，Accio Gateway 缓存 token
  │
  ▼
插件下载安装成功 ✅
  │
  ▼
绑定到 Agent，开始使用
```

用户只需完成一次授权，后续每次对话自动走认证，无感知。

---

## 四、Plugin 内部结构

### 4.1 仓库目录

```
visable-plugin/
├── plugin.json              ← 插件身份：名称、版本、分类
├── agents/
│   └── visable-assistant/
│       ├── agent.json       ← Agent 配置：模型、权限策略、关联 Skill
│       ├── agents.md        ← 行为规范：如何选择和触发 Skill（核心）
│       ├── identity.md      ← 角色定义与品牌红线
│       ├── soul.md          ← 人格与沟通风格
│       ├── bootstrap.md     ← 首次启动引导
│       ├── user.md          ← 用户信息模板
│       └── skills/
│           ├── store-diagnosis/SKILL.md      ← 店铺诊断
│           ├── product-optimization/SKILL.md ← 商品优化
│           └── business-insight/SKILL.md     ← Business Insight
├── connectors/
│   └── connectors.json      ← MCP Server URL + OAuth 配置（关键）
├── resources/
│   ├── agent-logo.svg       ← 品牌图标
│   └── recommend.json       ← 首屏引导提示词
└── .github/workflows/
    └── release.yml          ← CI：打 Tag → 自动发布
```

### 4.2 三个 Skill 的能力范围

| Skill | 触发词示例 | 调用的 MCP 工具 |
|---|---|---|
| **store-diagnosis**（店铺诊断） | "诊断店铺"、"流量分析"、"转化率" | `get_store_overview`、`get_traffic_analysis`、`get_conversion_funnel` |
| **product-optimization**（商品优化） | "优化商品"、"改标题"、"关键词建议" | `get_product_detail`、`suggest_title`、`suggest_description` |
| **business-insight**（业务洞察） | "数据趋势"、"竞品分析"、"生成报告" | `get_business_metrics`、`get_competitor_analysis`、`generate_report` |

---

## 五、MCP Server 设计

### 5.1 职责

MCP Server 是连接 Accio 和 Visable 业务后端的**唯一入口**：
- 接收 Accio MCP Gateway 的工具调用请求
- 从 HTTP Header 中提取 OAuth token
- 用 token 调用 Visable REST API
- 将结果格式化后返回

### 5.2 统一返回格式（Accio 规范）

所有工具返回格式统一，Accio 通过 `success` 字段判断调用成功率：

```json
// 成功
{ "success": true, "errorCode": null, "errorMsg": null, "data": { ... } }

// 失败
{ "success": false, "errorCode": "STORE_NOT_FOUND", "errorMsg": "店铺不存在", "data": null }
```

### 5.3 工具列表（9 个）

| 工具名 | 所属 Skill | 说明 |
|---|---|---|
| `get_store_overview` | 店铺诊断 | 店铺健康度概览 |
| `get_traffic_analysis` | 店铺诊断 | 流量来源分布 |
| `get_conversion_funnel` | 店铺诊断 | 曝光→点击→询盘→订单漏斗 |
| `get_product_detail` | 商品优化 | 商品详情 |
| `suggest_title` | 商品优化 | 标题优化建议 |
| `suggest_description` | 商品优化 | 描述优化建议 |
| `get_business_metrics` | 业务洞察 | 核心业务指标 |
| `get_competitor_analysis` | 业务洞察 | 竞品对比数据 |
| `generate_report` | 业务洞察 | 生成经营报告 |

---

## 六、发布与版本管理

### 6.1 发布流水线

```
开发者在 visable-plugin 仓库打 Tag（如 v1.0.0）
  │
  ▼
GitHub Actions 自动触发：
  ├── 打包 plugin.zip（排除 .git 等）
  ├── 生成 manifest.snapshot.json
  ├── 计算 sha256
  ├── 上传制品到对象存储
  └── 向 Accio phoenix-gateway 发起版本登记
  │
  ▼
版本进入「可发布候选池」
  │
  ▼
Accio 运维通过 Diamond 推到线上
  │
  ▼
Marketplace 可见，用户可安装 ✅
```

### 6.2 版本止血机制

| 场景 | 处理方式 |
|---|---|
| 新版本有 Bug | Accio 通过 Diamond 快速切回上一个稳定版本 |
| 严重问题需阻断下载 | 设置版本状态为 `STOP_SERVED`，阻断新安装 |
| 用户本地已安装旧版本 | 下次启动时感知更新提示，引导升级 |

---

## 七、三阶段交付计划

### Phase 1：Plugin 骨架 + MCP Server 基础（1-2 周）

**目标**：Plugin 结构完整，MCP Server 本地可调通 1 个工具

- 创建 `visable-plugin` 仓库，完成所有配置文件
- 创建 `visable-mcp-server` 仓库，实现 `get_store_overview` 工具
- 本地验证 MCP 工具可调用，返回格式正确

**交付物**：Plugin 仓库可提交给 Accio 审核注册；MCP Server 本地可 demo

---

### Phase 2：OAuth 打通 + 联调（2-3 周）

**目标**：在 Accio 测试环境完成「授权 → 安装 → 绑定 → 真实数据」全流程

- Visable 后端建立 OAuth App，配置授权地址
- MCP Server 部署测试环境，接入 token 验证
- 与 Accio 完成 Plugin 注册，拿到 `pluginId`
- 端到端联调验证

**需要 Accio 提供**：MCP Gateway 地址、OAuth `redirect_uri`、Plugin 注册方式

---

### Phase 3：Skills 完善 + CI 上线（3-4 周）

**目标**：三个 Skill 完整可用，CI 自动发布，生产版本登记

- 完善 9 个 MCP 工具（对齐三个 Skill 的完整需求）
- 补全 CI release.yml（上传 + 版本登记回调）
- 打 `v1.0.0` Tag，触发 CI，Marketplace 上线

---

## 八、当前阻塞项（需向 Accio 确认）

以下信息缺失，会阻塞 Phase 2-3 的推进，需尽快向 Accio 对接同学确认：

### 🔴 P0（阻塞联调）

| # | 问题 | 影响 |
|---|---|---|
| 1 | **Plugin 注册方式**：自助还是提工单？`pluginId` 格式？ | Phase 2 开始前必须注册 |
| 2 | **MCP Gateway 地址**：测试和生产环境分别是什么？ | `connectors.json` 无法填写 |
| 3 | **OAuth `redirect_uri`**：Accio Gateway 的回调地址？ | Visable OAuth App 需提前配置 |

### 🟡 P1（阻塞 CI 发布）

| # | 问题 | 影响 |
|---|---|---|
| 4 | **CI 回调接口**：`phoenix-gateway` 版本登记 endpoint、请求体格式、鉴权方式？ | CI 最后一步无法完成 |
| 5 | **对象存储方案**：`plugin.zip` 上传到哪里？Accio 提供还是自备 OSS？ | CI 上传步骤无法配置 |
| 6 | **`ON_INSTALL` 策略字段位置**：在 `plugin.json` 里声明还是注册时配置？ | 认证流程可能无法触发 |

### 🟢 P2（可后续确认）

| # | 问题 |
|---|---|
| 7 | `catalogSkillIds` 填 Plugin 内部目录名还是平台注册 ID？ |
| 8 | `agentType` 需要提前在 Accio 注册还是自定义？ |
| 9 | 测试环境是否可以接受接入方联调？上线 SLA？ |
| 10 | Diamond 止血操作是否有 Visable 侧自助入口？ |

---

## 九、技术栈总结

| 组件 | 技术选型 | 原因 |
|---|---|---|
| Plugin 仓库 | JSON + Markdown | Accio 规范，无技术选择空间 |
| MCP Server 语言 | Python 3.11+ | FastMCP 框架成熟，与 Okki 路径一致 |
| MCP 框架 | FastMCP | Accio 推荐，接口简洁 |
| HTTP 客户端 | httpx | 原生 async 支持，适合 FastMCP |
| 测试框架 | pytest + pytest-asyncio | Python 主流异步测试方案 |
| CI | GitHub Actions | Plugin 仓库托管在 GitHub |
| 认证 | OAuth 2.0 Authorization Code Flow | Accio 标准，与 Okki 相同 |

---

*参考文档：[Accio Plugin System 工程侧设计方案](https://aliyuque.antfin.com/g/vh1uut/yihwt7/pvsohtyln7bn6na7) · [完整 Plugin 配置包 Demo（okki-assistant）](https://alidocs.dingtalk.com/i/nodes/YndMj49yWjlAYoxjtwdO0NKpJ3pmz5aA)*
