# visable-assistant Accio Plugin 设计文档

**日期**: 2026-05-06  
**状态**: 已批准，待实现

---

## 一、背景与目标

Visable 平台需要一个 Accio Plugin，为商家用户提供 AI 助手能力，核心覆盖：
1. **店铺诊断** — 分析流量、转化、店铺健康度
2. **商品优化** — 标题、描述、图片优化建议
3. **商家数据查询** — 订单、访客、运营数据查询

参考 okki-assistant 作为样板，当前阶段先建立完整的基础框架（无真实 MCP 接入），待 MCP 开发完成后直接填充。

---

## 二、目录结构

```
/Users/yangjun/Desktop/my-ai/visable-assistant/    ← 根目录直接放置
├── plugin.json                        # 插件根清单
├── connectors/
│   └── connectors.json               # MCP 占位 + OAuth 框架
├── dependencies/
│   └── dependencies.json             # 依赖声明
├── resources/
│   ├── agent-logo.svg                # 插件图标（占位）
│   └── recommend.json               # 三大能力的示例提示词块
└── agents/
    └── visable-assistant/
        ├── agent.json               # Agent 运行时元数据
        ├── identity.md              # Visable 平台立场 + 商业红线
        ├── soul.md                  # 务实助手人格
        ├── agents.md                # 三大任务模块 + 技能消歧规则
        ├── bootstrap.md             # 首次启动指引
        ├── user.md                  # 用户信息模板
        └── skills/
            ├── store-diagnostics/
            │   └── SKILL.md         # 店铺诊断技能骨架
            ├── product-optimization/
            │   └── SKILL.md         # 商品优化技能骨架
            └── data-query/
                └── SKILL.md         # 数据查询技能骨架
```

---

## 三、核心文件设计

### 3.1 plugin.json

| 字段 | 值 |
|------|-----|
| name | `visable-assistant` |
| displayName | `Visable 助手` |
| version | `0.0.1` |
| category | `e-commerce` |
| tags | `visable`, `store-diagnostics`, `product-optimization` |
| icon | `resources/agent-logo.svg` |

### 3.2 agent.json 关键字段

- `agentType`: `visable-assistant`
- `toolPreset`: `full`
- `catalogSkillIds`: `["store-diagnostics", "product-optimization", "data-query", "skill-finder", "mcp-tools"]`
- `policyRules`: write/edit/apply_patch → allow；browser → ask
- `onboarding`: `resources/recommend.json`

### 3.3 Agent 身份与人格（identity.md + soul.md）

**平台立场**：
- 不贬低 Visable 平台及其服务
- 不编造数据、平台规则、商家运营数据
- 若工具数据不可用，如实说明而非虚构

**人格**：务实、数据驱动、支持性，始终把建议关联到业务结果（GMV、转化率、利润率）

### 3.4 agents.md — 三大任务模块

**店铺诊断**：
- 店铺信息完整度检查（必填/推荐字段缺失检测）
- 缺失信息的优化建议与补全引导
- 店铺健康度综合评分（基于信息完整度）

**商品优化**：
- SEO 友好标题优化
- 商品描述生成与改写
- 图片优化建议

**商家数据查询**：
- 订单量、客单价、退款率等核心指标
- 访客来源与国家分布
- 产品维度排名

**技能消歧规则**：沿用 okki-assistant 的三类意图分类（A：明确引用技能 → 直接执行；B：非任务对话 → 自然回应；C：可执行任务未指定技能 → 列出候选让用户选）

### 3.5 Skills 骨架（SKILL.md × 3）

每个 SKILL.md 包含：
- 触发条件（何时调用此技能）
- 执行步骤（当前为占位，注明"待 MCP 接入后填充"）
- 输出格式规范
- MCP 接入说明（placeholder）

### 3.6 connectors.json

```json
{
  "mcpServers": {
    "visable-data-server": {
      "type": "stream",
      "url": "https://api.placeholder-visable-mcp.com/mcp"
    }
  },
  "oauth": {
    "visable": {
      "adapter": "mcp-oauth",
      "toolName": "start_visable_oauth",
      "enabled": true,
      "authorization_url": "https://auth.placeholder-visable.com/authorize",
      "token_url": "https://auth.placeholder-visable.com/token",
      "scopes": ["openid", "profile"]
    }
  }
}
```

### 3.7 recommend.json

三个区块，分别对应：
1. 店铺诊断示例提示词 → skillId: `store-diagnostics`
2. 商品优化示例提示词 → skillId: `product-optimization`
3. 数据查询示例提示词 → skillId: `data-query`

---

## 四、扩展路径

| 阶段 | 动作 |
|------|------|
| P0（当前） | 建立完整文件框架，所有 MCP 为 placeholder |
| P1 | MCP 开发完成后：填充 connectors.json 真实 URL + 完善三个 SKILL.md 执行步骤 |
| P2 | 按需新增 Skills 目录 + 更新 agents.md 消歧逻辑 |

---

## 五、与 okki-assistant 的关键差异

| 项目 | okki-assistant | visable-assistant |
|------|---------------|-------------------|
| 业务场景 | Okki CRM + 阿里巴巴国际站 | Visable 平台商家运营 |
| 技能方向 | 询盘/客户跟进/选品/发品 | 店铺诊断/商品优化/数据查询 |
| Skills 位置 | 无 skills/ 子目录 | agents/visable-assistant/skills/ |
| MCP 状态 | 示例 placeholder | 示例 placeholder（待填充） |
