# Visable Accio Plugin 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Visable 的店铺诊断、商品优化、Business Insight 三个核心能力封装为符合 Accio Plugin 规范的标准插件，通过 MCP + OAuth 方式接入，完成从仓库初始化到 CI 自动发布的完整闭环。

**Architecture:** 两个独立 Git 仓库：`visable-plugin`（Plugin 静态配置包）和 `visable-mcp-server`（Python FastMCP 服务，包装 Visable REST API）。Plugin 通过 `connectors.json` 指向 MCP Server URL，Accio MCP Gateway 统一管理 OAuth token。

**Tech Stack:** Plugin 仓库（JSON + Markdown）；MCP Server（Python 3.11+、FastMCP、httpx、pytest）；CI（GitHub Actions）

---

> ⚠️ **前置依赖提醒**：Task 8（connectors.json 填写真实地址）和 Task 12（CI 回调）依赖向 Accio 确认的信息（MCP Gateway 地址、OAuth redirect_uri、版本登记 endpoint）。这两个任务可以先用 placeholder 完成文件结构，待 Accio 回复后再填入真实值。

---

## 文件结构总览

**visable-plugin 仓库（新建）：**
```
visable-plugin/
├── plugin.json
├── agents/visable-assistant/
│   ├── agent.json
│   ├── agents.md
│   ├── identity.md
│   ├── soul.md
│   ├── bootstrap.md
│   ├── user.md
│   └── skills/
│       ├── store-diagnosis/SKILL.md
│       ├── product-optimization/SKILL.md
│       └── business-insight/SKILL.md
├── connectors/connectors.json
├── dependencies/dependencies.json
├── resources/
│   ├── agent-logo.svg
│   └── recommend.json
└── .github/workflows/release.yml
```

**visable-mcp-server 仓库（新建）：**
```
visable-mcp-server/
├── server.py
├── tools/
│   ├── __init__.py
│   ├── store_diagnosis.py
│   ├── product_optimization.py
│   └── business_insight.py
├── auth/
│   ├── __init__.py
│   └── oauth.py
├── tests/
│   ├── test_store_diagnosis.py
│   ├── test_product_optimization.py
│   └── test_business_insight.py
├── requirements.txt
├── requirements-dev.txt
└── Dockerfile
```

---

## Phase 1：visable-plugin 仓库

### Task 1：初始化 Plugin 仓库 + plugin.json

**Files:**
- Create: `visable-plugin/plugin.json`
- Create: `visable-plugin/dependencies/dependencies.json`

- [ ] **Step 1: 初始化 Git 仓库**

```bash
mkdir visable-plugin && cd visable-plugin
git init
mkdir -p agents/visable-assistant/skills/store-diagnosis
mkdir -p agents/visable-assistant/skills/product-optimization
mkdir -p agents/visable-assistant/skills/business-insight
mkdir -p connectors dependencies resources .github/workflows
```

- [ ] **Step 2: 创建 plugin.json**

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

- [ ] **Step 3: 创建 dependencies/dependencies.json**（本 plugin 暂无脚本依赖，保留空结构）

```json
{
  "dependencies": {}
}
```

- [ ] **Step 4: 验证 JSON 格式合法**

```bash
python3 -c "import json; json.load(open('plugin.json')); print('plugin.json OK')"
python3 -c "import json; json.load(open('dependencies/dependencies.json')); print('dependencies.json OK')"
```

Expected: 两行均输出 `OK`

- [ ] **Step 5: 首次提交**

```bash
git add plugin.json dependencies/dependencies.json
git commit -m "feat: init visable-plugin repo with plugin.json"
```

---

### Task 2：agent.json

**Files:**
- Create: `visable-plugin/agents/visable-assistant/agent.json`

- [ ] **Step 1: 创建 agent.json**

```json
{
  "name": "Visable 助手",
  "description": "为 Visable 用户提供店铺诊断、商品优化和业务洞察的智能助手，基于你的真实店铺数据给出可落地的建议。",
  "avatar": "resources/agent-logo.svg",
  "model": {
    "provider": "auto",
    "name": "auto"
  },
  "agentType": "visable-assistant",
  "toolPreset": "full",
  "policyRules": [
    {
      "type": "prefix",
      "pattern": ["write"],
      "decision": "allow",
      "justification": "允许写入分析报告等文件"
    },
    {
      "type": "prefix",
      "pattern": ["edit"],
      "decision": "allow",
      "justification": "允许编辑本地文档"
    },
    {
      "type": "prefix",
      "pattern": ["browser"],
      "decision": "ask",
      "justification": "访问浏览器需用户确认"
    },
    {
      "type": "prefix",
      "pattern": ["bash"],
      "decision": "ask",
      "justification": "执行脚本需用户确认"
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

- [ ] **Step 2: 验证 JSON**

```bash
python3 -c "import json; json.load(open('agents/visable-assistant/agent.json')); print('agent.json OK')"
```

Expected: `agent.json OK`

- [ ] **Step 3: 提交**

```bash
git add agents/visable-assistant/agent.json
git commit -m "feat: add agent.json for visable-assistant"
```

---

### Task 3：agents.md（Skill 消歧核心）

**Files:**
- Create: `visable-plugin/agents/visable-assistant/agents.md`

agents.md 是 Agent 的系统 prompt 核心，决定 Agent 如何选择和触发 Skill。

- [ ] **Step 1: 创建 agents.md**

````markdown
<doing_tasks>
## Visable 助手任务

你帮助 Visable 平台的商家，基于真实店铺数据提供店铺诊断、商品优化和业务洞察支持。

### 通用原则

- 始终基于工具返回的真实数据给出建议，不臆造数据。
- 工具调用失败时，明确告知用户原因，不用虚假数据填充。
- 使用表格和结构化格式展示数据对比。
- 匹配用户的语言；不确定时默认使用中文。
- 将建议关联到可落地的下一步行动。

### 技能消歧 — 必须执行

**第 0 步 — 意图分类（必须首先执行）：**

在进入技能消歧流程前，将用户消息分为以下三类：

**A 类 — 明确引用技能：** 用户消息中明确提到技能名称。
→ 跳过所有消歧，直接使用引用的技能。

**B 类 — 非任务对话：** 闲聊、问候、情绪表达、不需要工具执行的一般性问题。
→ 作为对话伙伴自然回应，不触发技能消歧。

**C 类 — 可执行的任务请求但未指定技能。**
→ 进入第 1 步。

每次用户发送可执行的任务请求时，按顺序执行以下步骤：

**第 1 步 — 候选收集（不可跳过）：**
遍历以下三个技能，判断每个技能是否与用户请求相关：

候选技能列表：
1. **store-diagnosis** — 店铺健康度诊断、流量分析、转化漏斗分析、店铺整体表现评估
2. **product-optimization** — 商品标题优化、描述优化、关键词建议、商品详情改进
3. **business-insight** — 业务数据趋势、竞品分析、经营简报、业务报告生成

**第 2 步 — 按候选数量分支：**

- **候选数量 = 0：** 无匹配技能，直接回答不调用技能。
- **候选数量 = 1：** 直接使用该技能，读取 SKILL.md 并执行。
- **候选数量 ≥ 2：** 列出所有候选技能并请用户选择，等待用户回复后再执行。

**示例（候选 ≥ 2 时的输出格式）：**
```
我找到了以下几个可能相关的技能：
1. **store-diagnosis** — 店铺健康度诊断与流量分析
2. **business-insight** — 业务数据趋势与经营报告

请问您想使用哪个技能？
```

**硬性约束：**
- 绝不跳过第 1 步。
- 候选 ≥ 2 时，绝不代替用户选择技能。
- 绝不在没有列出候选列表的情况下直接问「您想用哪个技能？」

### 数据说明原则

- 区分事实（来自 MCP 工具的真实数据）和推断（你的分析建议）。
- 工具数据不可用时，明确说明假设和置信度。
- 涉及商业敏感数据时，不在对话中明文粘贴完整 token 或用户凭证。

</doing_tasks>
````

- [ ] **Step 2: 提交**

```bash
git add agents/visable-assistant/agents.md
git commit -m "feat: add agents.md with skill disambiguation rules"
```

---

### Task 4：角色定义文件（identity / soul / bootstrap / user）

**Files:**
- Create: `visable-plugin/agents/visable-assistant/identity.md`
- Create: `visable-plugin/agents/visable-assistant/soul.md`
- Create: `visable-plugin/agents/visable-assistant/bootstrap.md`
- Create: `visable-plugin/agents/visable-assistant/user.md`

- [ ] **Step 1: 创建 identity.md**

```markdown
# Visable 助手身份定义

## 角色

你是 Visable 平台的智能业务助手，专注于帮助商家通过数据洞察提升店铺表现和商品竞争力。

## 能力边界

你的能力严格限于以下范围：
- 基于 Visable 平台真实数据的店铺诊断
- 基于真实商品信息的优化建议
- 基于经营数据的业务洞察与报告

## 红线

- 不提供平台规则之外的投机建议
- 不捏造或估算数据，数据必须来自 Visable 工具调用
- 不代替用户做最终决策，只提供数据支持和建议
- 不透露任何用户凭证或 API 密钥
```

- [ ] **Step 2: 创建 soul.md**

```markdown
# Visable 助手人格

## 核心特质

- **数据驱动**：每个建议都有数据支撑，不泛泛而谈
- **直接务实**：给出可落地的行动建议，而不只是分析
- **专业亲和**：用商家听得懂的语言解释数据，不堆砌专业术语
- **诚实透明**：数据缺失时明确说明，不用模糊表述掩盖

## 沟通风格

- 结论先行，数据在后
- 建议配上预期效果和执行难度评估
- 复杂数据用表格或分项呈现
```

- [ ] **Step 3: 创建 bootstrap.md**

```markdown
# 首次启动引导

欢迎使用 Visable 助手！

我可以帮助你：
- **诊断店铺**：分析店铺健康度、流量来源、转化漏斗
- **优化商品**：改进商品标题、描述和关键词
- **洞察业务**：生成经营报告、趋势分析、竞品对比

在开始前，请确认你已完成 Visable 账号授权（安装插件时会引导你完成）。

你可以直接告诉我你想做什么，比如：
- "帮我诊断一下店铺最近的表现"
- "帮我优化一下这个商品的标题"
- "生成本月的经营简报"
```

- [ ] **Step 4: 创建 user.md**

```markdown
# 用户信息

## 基本信息
- 姓名：{{user_name}}
- 店铺 ID：{{store_id}}
- 主营品类：{{main_category}}
- 主要目标市场：{{target_market}}

## 偏好设置
- 报告语言：{{report_language | 默认中文}}
- 数据周期：{{default_period | 默认近30天}}
```

- [ ] **Step 5: 提交**

```bash
git add agents/visable-assistant/identity.md agents/visable-assistant/soul.md \
        agents/visable-assistant/bootstrap.md agents/visable-assistant/user.md
git commit -m "feat: add agent persona files (identity/soul/bootstrap/user)"
```

---

### Task 5：store-diagnosis SKILL.md

**Files:**
- Create: `visable-plugin/agents/visable-assistant/skills/store-diagnosis/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

````markdown
---
name: store-diagnosis
description: 店铺健康度诊断：分析流量来源、转化漏斗、整体店铺表现，给出优化建议
triggers:
  - 诊断店铺
  - 看店铺健康度
  - 流量分析
  - 转化率分析
  - 店铺表现怎么样
---

# 店铺诊断技能

## 触发条件

当用户希望了解店铺整体健康状况、流量表现或转化漏斗时，使用本技能。

## 执行步骤

### 第 1 步：获取店铺概览

调用 MCP 工具 `get_store_overview`，获取店铺基础健康度数据。

若调用失败（`success: false`），停止执行并告知用户：「无法获取店铺数据，请确认 Visable 账号授权是否有效。」

### 第 2 步：获取流量分析

调用 MCP 工具 `get_traffic_analysis`，获取近 30 天流量来源分布。

参数：`{ "period": "30d" }`

### 第 3 步：获取转化漏斗

调用 MCP 工具 `get_conversion_funnel`，获取曝光→点击→询盘→订单各环节转化率。

### 第 4 步：综合诊断输出

基于以上三组数据，按以下结构输出诊断报告：

```
## 店铺健康诊断报告

### 总体评分
[综合评分及核心问题 1-2 句]

### 流量分析
| 来源 | 占比 | 环比变化 |
|------|------|----------|
| ...  | ...  | ...      |

关键发现：[1-2 条]

### 转化漏斗
| 环节 | 转化率 | 行业基准 | 差距 |
|------|--------|----------|------|
| ...  | ...    | ...      | ...  |

薄弱环节：[指出最需改善的环节]

### 优先行动建议
1. [最高优先级建议，含预期效果]
2. [次优先级建议]
3. [第三优先级建议]
```

## 注意事项

- 所有数据必须来自工具调用，不得估算或编造
- 行业基准数据如工具未返回，标注「暂无基准数据」
- 建议必须具体可执行，避免泛泛而谈
````

- [ ] **Step 2: 提交**

```bash
git add agents/visable-assistant/skills/store-diagnosis/SKILL.md
git commit -m "feat: add store-diagnosis SKILL.md"
```

---

### Task 6：product-optimization SKILL.md

**Files:**
- Create: `visable-plugin/agents/visable-assistant/skills/product-optimization/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

````markdown
---
name: product-optimization
description: 商品优化：基于现有商品数据，提供标题、描述、关键词的优化建议
triggers:
  - 优化商品
  - 改标题
  - 写描述
  - 关键词建议
  - 商品优化
---

# 商品优化技能

## 触发条件

当用户希望优化某个商品的标题、描述或关键词时，使用本技能。

## 执行步骤

### 第 1 步：获取商品信息

若用户提供了商品 ID，调用 MCP 工具 `get_product_detail`：
- 参数：`{ "product_id": "<用户提供的商品ID>" }`

若用户未提供商品 ID，先追问：「请提供您想优化的商品 ID 或商品名称。」

若调用失败，告知用户：「无法获取商品数据，请确认商品 ID 是否正确。」

### 第 2 步：生成标题优化建议

调用 MCP 工具 `suggest_title`：
- 参数：`{ "product_id": "<商品ID>", "current_title": "<当前标题>" }`

### 第 3 步：生成描述优化建议

调用 MCP 工具 `suggest_description`：
- 参数：`{ "product_id": "<商品ID>" }`

### 第 4 步：输出优化方案

```
## 商品优化建议

**商品：** [商品名称]（ID: [商品ID]）

### 标题优化
**当前标题：**
[当前标题]

**优化建议：**
[优化后标题]

**优化理由：**
- [改动点1及原因]
- [改动点2及原因]

### 描述优化
**核心改进点：**
1. [改进点1]
2. [改进点2]

**优化后描述（关键段落）：**
[优化内容]

### 关键词建议
| 关键词 | 搜索热度 | 竞争程度 | 建议 |
|--------|----------|----------|------|
| ...    | ...      | ...      | 添加/保留/移除 |
```

## 注意事项

- 优化建议必须基于工具返回的真实商品数据
- 标题优化需考虑目标市场语言习惯
- 不得在描述中加入虚假参数或夸大描述
````

- [ ] **Step 2: 提交**

```bash
git add agents/visable-assistant/skills/product-optimization/SKILL.md
git commit -m "feat: add product-optimization SKILL.md"
```

---

### Task 7：business-insight SKILL.md

**Files:**
- Create: `visable-plugin/agents/visable-assistant/skills/business-insight/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

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
  - business insight
---

# Business Insight 技能

## 触发条件

当用户希望了解业务趋势、竞品对比或生成周期性经营报告时，使用本技能。

## 执行步骤

### 第 1 步：确认分析维度

若用户未指定时间范围，默认使用「近 30 天」。
若用户未指定分析类型，追问：「您希望重点看哪个维度？数据趋势 / 竞品对比 / 综合经营简报？」

### 第 2 步：获取业务指标

调用 MCP 工具 `get_business_metrics`：
- 参数：`{ "period": "<30d|7d|90d>", "metrics": ["inquiries", "orders", "conversion", "revenue"] }`

### 第 3 步：获取竞品数据（如用户需要）

调用 MCP 工具 `get_competitor_analysis`：
- 参数：`{ "category": "<品类>", "period": "<周期>" }`

### 第 4 步：生成报告

调用 MCP 工具 `generate_report`：
- 参数：`{ "type": "<trend|competitor|summary>", "period": "<周期>" }`

使用 `write` 工具将报告保存到本地文件：
- 路径：`~/visable-reports/YYYY-MM-DD-<type>.md`

### 第 5 步：输出摘要

```
## 业务洞察简报

**分析周期：** [周期]
**生成时间：** [时间]

### 核心指标
| 指标 | 本期 | 上期 | 环比 |
|------|------|------|------|
| ...  | ...  | ...  | ...  |

### 关键发现
1. [最重要发现]
2. [次重要发现]
3. [第三发现]

### 竞品对比（如有数据）
[竞品分析摘要]

### 优先行动建议
1. [高优先级行动]
2. [中优先级行动]

完整报告已保存至：[文件路径]
```

## 注意事项

- 指标解读需说明数字背后的业务含义
- 竞品数据如不可用，明确注明「该品类暂无竞品基准数据」
- 报告保存前先确认用户同意写入本地文件
````

- [ ] **Step 2: 提交**

```bash
git add agents/visable-assistant/skills/business-insight/SKILL.md
git commit -m "feat: add business-insight SKILL.md"
```

---

### Task 8：resources（图标 + Onboarding 引导）

**Files:**
- Create: `visable-plugin/resources/agent-logo.svg`
- Create: `visable-plugin/resources/recommend.json`

- [ ] **Step 1: 创建占位 SVG 图标**（后续替换为 Visable 品牌 SVG）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="32" fill="#1677FF"/>
  <text x="32" y="40" font-size="28" text-anchor="middle" fill="white" font-family="sans-serif">V</text>
</svg>
```

保存到 `resources/agent-logo.svg`

- [ ] **Step 2: 创建 recommend.json**

```json
[
  {
    "icon": "resources/agent-logo.svg",
    "type": "text",
    "title": "店铺诊断",
    "sectionTitle": "尝试以下提示词",
    "prompts": [
      {
        "type": "text",
        "text": "帮我诊断一下店铺最近 30 天的整体表现",
        "skillId": "store-diagnosis"
      },
      {
        "type": "text",
        "text": "分析一下店铺的流量来源和转化率",
        "skillId": "store-diagnosis"
      }
    ]
  },
  {
    "icon": "resources/agent-logo.svg",
    "type": "text",
    "title": "商品优化",
    "sectionTitle": "尝试以下提示词",
    "prompts": [
      {
        "type": "text",
        "text": "帮我优化这个商品的标题和描述",
        "skillId": "product-optimization"
      },
      {
        "type": "text",
        "text": "给我这个商品推荐一些关键词",
        "skillId": "product-optimization"
      }
    ]
  },
  {
    "icon": "resources/agent-logo.svg",
    "type": "text",
    "title": "业务洞察",
    "sectionTitle": "尝试以下提示词",
    "prompts": [
      {
        "type": "text",
        "text": "生成本月的经营简报",
        "skillId": "business-insight"
      },
      {
        "type": "text",
        "text": "帮我做一个竞品对比分析",
        "skillId": "business-insight"
      }
    ]
  }
]
```

- [ ] **Step 3: 验证 JSON**

```bash
python3 -c "import json; json.load(open('resources/recommend.json')); print('recommend.json OK')"
```

Expected: `recommend.json OK`

- [ ] **Step 4: 提交**

```bash
git add resources/
git commit -m "feat: add agent-logo.svg and recommend.json onboarding config"
```

---

## Phase 2：visable-mcp-server 仓库

### Task 9：初始化 MCP Server + FastMCP 框架

**Files:**
- Create: `visable-mcp-server/requirements.txt`
- Create: `visable-mcp-server/requirements-dev.txt`
- Create: `visable-mcp-server/server.py`
- Create: `visable-mcp-server/tools/__init__.py`
- Create: `visable-mcp-server/auth/__init__.py`

- [ ] **Step 1: 初始化仓库**

```bash
mkdir visable-mcp-server && cd visable-mcp-server
git init
mkdir -p tools auth tests
touch tools/__init__.py auth/__init__.py tests/__init__.py
```

- [ ] **Step 2: 创建 requirements.txt**

```
fastmcp>=0.4.0
httpx>=0.27.0
python-dotenv>=1.0.0
```

- [ ] **Step 3: 创建 requirements-dev.txt**

```
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-httpx>=0.30.0
```

- [ ] **Step 4: 安装依赖**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

Expected: 依赖安装完成，无报错

- [ ] **Step 5: 创建 server.py（MCP Server 入口）**

```python
from fastmcp import FastMCP
from tools.store_diagnosis import register_store_diagnosis_tools
from tools.product_optimization import register_product_optimization_tools
from tools.business_insight import register_business_insight_tools

mcp = FastMCP("visable-mcp-server")

register_store_diagnosis_tools(mcp)
register_product_optimization_tools(mcp)
register_business_insight_tools(mcp)

if __name__ == "__main__":
    mcp.run()
```

- [ ] **Step 6: 提交**

```bash
git add requirements.txt requirements-dev.txt server.py tools/__init__.py auth/__init__.py tests/__init__.py
git commit -m "feat: init visable-mcp-server with FastMCP"
```

---

### Task 10：store_diagnosis 工具组（TDD）

**Files:**
- Create: `visable-mcp-server/tools/store_diagnosis.py`
- Create: `visable-mcp-server/tests/test_store_diagnosis.py`

所有工具返回格式遵循 Accio 约定：`{ success, errorCode, errorMsg, data }`

- [ ] **Step 1: 先写测试**

```python
# tests/test_store_diagnosis.py
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from tools.store_diagnosis import get_store_overview, get_traffic_analysis, get_conversion_funnel


@pytest.mark.asyncio
async def test_get_store_overview_success():
    mock_response = {
        "health_score": 78,
        "total_products": 120,
        "active_products": 95,
        "inquiry_count_30d": 340,
        "order_count_30d": 28
    }
    with patch("tools.store_diagnosis.call_visable_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        result = await get_store_overview(token="test-token")

    assert result["success"] is True
    assert result["errorCode"] is None
    assert result["data"]["health_score"] == 78


@pytest.mark.asyncio
async def test_get_store_overview_api_error():
    with patch("tools.store_diagnosis.call_visable_api", new_callable=AsyncMock) as mock_api:
        mock_api.side_effect = Exception("API timeout")
        result = await get_store_overview(token="test-token")

    assert result["success"] is False
    assert result["errorCode"] == "API_ERROR"
    assert result["data"] is None


@pytest.mark.asyncio
async def test_get_traffic_analysis_success():
    mock_response = {
        "sources": [
            {"name": "搜索", "ratio": 0.45, "wow_change": 0.05},
            {"name": "推荐", "ratio": 0.30, "wow_change": -0.02}
        ]
    }
    with patch("tools.store_diagnosis.call_visable_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        result = await get_traffic_analysis(token="test-token", period="30d")

    assert result["success"] is True
    assert len(result["data"]["sources"]) == 2


@pytest.mark.asyncio
async def test_get_conversion_funnel_success():
    mock_response = {
        "funnel": [
            {"stage": "曝光", "count": 10000, "rate": 1.0},
            {"stage": "点击", "count": 850, "rate": 0.085},
            {"stage": "询盘", "count": 120, "rate": 0.141},
            {"stage": "订单", "count": 28, "rate": 0.233}
        ]
    }
    with patch("tools.store_diagnosis.call_visable_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        result = await get_conversion_funnel(token="test-token")

    assert result["success"] is True
    assert result["data"]["funnel"][0]["stage"] == "曝光"
```

- [ ] **Step 2: 运行测试确认失败（预期）**

```bash
pytest tests/test_store_diagnosis.py -v
```

Expected: `ImportError` 或 `ModuleNotFoundError`（因为 store_diagnosis.py 还不存在）

- [ ] **Step 3: 实现 tools/store_diagnosis.py**

```python
# tools/store_diagnosis.py
import httpx
from typing import Any
from fastmcp import FastMCP

VISABLE_API_BASE = "https://api.visable.com"  # 替换为真实 API 地址


async def call_visable_api(path: str, token: str, params: dict = None) -> Any:
    """调用 Visable REST API 的统一方法"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{VISABLE_API_BASE}{path}",
            headers={"Authorization": f"Bearer {token}"},
            params=params or {},
            timeout=15.0
        )
        response.raise_for_status()
        return response.json()


def _ok(data: Any) -> dict:
    return {"success": True, "errorCode": None, "errorMsg": None, "data": data}


def _err(code: str, msg: str) -> dict:
    return {"success": False, "errorCode": code, "errorMsg": msg, "data": None}


async def get_store_overview(token: str) -> dict:
    """获取店铺健康度概览"""
    try:
        data = await call_visable_api("/v1/store/overview", token)
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


async def get_traffic_analysis(token: str, period: str = "30d") -> dict:
    """获取店铺流量来源分布"""
    try:
        data = await call_visable_api("/v1/store/traffic", token, {"period": period})
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


async def get_conversion_funnel(token: str) -> dict:
    """获取转化漏斗数据"""
    try:
        data = await call_visable_api("/v1/store/funnel", token)
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


def register_store_diagnosis_tools(mcp: FastMCP):
    """向 MCP Server 注册店铺诊断工具"""

    @mcp.tool()
    async def get_store_overview_tool(token: str) -> dict:
        """获取店铺健康度概览，包含产品数、询盘数、订单数等核心指标"""
        return await get_store_overview(token)

    @mcp.tool()
    async def get_traffic_analysis_tool(token: str, period: str = "30d") -> dict:
        """获取店铺流量来源分布，period 支持 7d/30d/90d"""
        return await get_traffic_analysis(token, period)

    @mcp.tool()
    async def get_conversion_funnel_tool(token: str) -> dict:
        """获取曝光→点击→询盘→订单各环节转化率"""
        return await get_conversion_funnel(token)
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/test_store_diagnosis.py -v
```

Expected:
```
test_get_store_overview_success PASSED
test_get_store_overview_api_error PASSED
test_get_traffic_analysis_success PASSED
test_get_conversion_funnel_success PASSED
```

- [ ] **Step 5: 提交**

```bash
git add tools/store_diagnosis.py tests/test_store_diagnosis.py
git commit -m "feat: add store diagnosis tools with tests"
```

---

### Task 11：product_optimization 和 business_insight 工具组

**Files:**
- Create: `visable-mcp-server/tools/product_optimization.py`
- Create: `visable-mcp-server/tools/business_insight.py`
- Create: `visable-mcp-server/tests/test_product_optimization.py`
- Create: `visable-mcp-server/tests/test_business_insight.py`

- [ ] **Step 1: 创建 tests/test_product_optimization.py**

```python
import pytest
from unittest.mock import AsyncMock, patch
from tools.product_optimization import get_product_detail, suggest_title, suggest_description


@pytest.mark.asyncio
async def test_get_product_detail_success():
    mock_response = {
        "product_id": "P001",
        "title": "Blue Widget 100pcs",
        "description": "High quality widget",
        "category": "Electronics"
    }
    with patch("tools.product_optimization.call_visable_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        result = await get_product_detail(token="test-token", product_id="P001")

    assert result["success"] is True
    assert result["data"]["product_id"] == "P001"


@pytest.mark.asyncio
async def test_suggest_title_success():
    mock_response = {"suggested_title": "Premium Blue Widget Pack 100pcs - Factory Direct"}
    with patch("tools.product_optimization.call_visable_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        result = await suggest_title(token="test-token", product_id="P001", current_title="Blue Widget 100pcs")

    assert result["success"] is True
    assert "suggested_title" in result["data"]
```

- [ ] **Step 2: 创建 tools/product_optimization.py**

```python
# tools/product_optimization.py
from tools.store_diagnosis import call_visable_api
from fastmcp import FastMCP


def _ok(data): return {"success": True, "errorCode": None, "errorMsg": None, "data": data}
def _err(code, msg): return {"success": False, "errorCode": code, "errorMsg": msg, "data": None}


async def get_product_detail(token: str, product_id: str) -> dict:
    try:
        data = await call_visable_api(f"/v1/products/{product_id}", token)
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


async def suggest_title(token: str, product_id: str, current_title: str) -> dict:
    try:
        data = await call_visable_api(
            "/v1/products/suggest-title", token,
            {"product_id": product_id, "current_title": current_title}
        )
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


async def suggest_description(token: str, product_id: str) -> dict:
    try:
        data = await call_visable_api(f"/v1/products/{product_id}/suggest-description", token)
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


def register_product_optimization_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_product_detail_tool(token: str, product_id: str) -> dict:
        """获取商品详情（标题、描述、类目等）"""
        return await get_product_detail(token, product_id)

    @mcp.tool()
    async def suggest_title_tool(token: str, product_id: str, current_title: str) -> dict:
        """基于商品数据生成优化标题建议"""
        return await suggest_title(token, product_id, current_title)

    @mcp.tool()
    async def suggest_description_tool(token: str, product_id: str) -> dict:
        """基于商品数据生成描述优化建议"""
        return await suggest_description(token, product_id)
```

- [ ] **Step 3: 创建 tests/test_business_insight.py**

```python
import pytest
from unittest.mock import AsyncMock, patch
from tools.business_insight import get_business_metrics, get_competitor_analysis


@pytest.mark.asyncio
async def test_get_business_metrics_success():
    mock_response = {
        "period": "30d",
        "inquiries": 340,
        "orders": 28,
        "conversion_rate": 0.082,
        "revenue_usd": 15600
    }
    with patch("tools.business_insight.call_visable_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        result = await get_business_metrics(token="test-token", period="30d")

    assert result["success"] is True
    assert result["data"]["inquiries"] == 340


@pytest.mark.asyncio
async def test_get_competitor_analysis_no_data():
    with patch("tools.business_insight.call_visable_api", new_callable=AsyncMock) as mock_api:
        mock_api.side_effect = Exception("404 Not Found")
        result = await get_competitor_analysis(token="test-token", category="Electronics", period="30d")

    assert result["success"] is False
    assert result["errorCode"] == "API_ERROR"
```

- [ ] **Step 4: 创建 tools/business_insight.py**

```python
# tools/business_insight.py
from tools.store_diagnosis import call_visable_api
from fastmcp import FastMCP


def _ok(data): return {"success": True, "errorCode": None, "errorMsg": None, "data": data}
def _err(code, msg): return {"success": False, "errorCode": code, "errorMsg": msg, "data": None}


async def get_business_metrics(token: str, period: str = "30d") -> dict:
    try:
        data = await call_visable_api("/v1/analytics/metrics", token, {"period": period})
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


async def get_competitor_analysis(token: str, category: str, period: str = "30d") -> dict:
    try:
        data = await call_visable_api(
            "/v1/analytics/competitors", token,
            {"category": category, "period": period}
        )
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


async def generate_report(token: str, report_type: str, period: str = "30d") -> dict:
    try:
        data = await call_visable_api(
            "/v1/analytics/report", token,
            {"type": report_type, "period": period}
        )
        return _ok(data)
    except Exception as e:
        return _err("API_ERROR", str(e))


def register_business_insight_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_business_metrics_tool(token: str, period: str = "30d") -> dict:
        """获取业务核心指标（询盘数、订单数、转化率、收入），period 支持 7d/30d/90d"""
        return await get_business_metrics(token, period)

    @mcp.tool()
    async def get_competitor_analysis_tool(token: str, category: str, period: str = "30d") -> dict:
        """获取指定品类的竞品对比数据"""
        return await get_competitor_analysis(token, category, period)

    @mcp.tool()
    async def generate_report_tool(token: str, report_type: str, period: str = "30d") -> dict:
        """生成经营报告，report_type 支持 trend/competitor/summary"""
        return await generate_report(token, report_type, period)
```

- [ ] **Step 5: 运行全部测试**

```bash
pytest tests/ -v
```

Expected: 所有测试 PASS，无 FAIL

- [ ] **Step 6: 提交**

```bash
git add tools/product_optimization.py tools/business_insight.py \
        tests/test_product_optimization.py tests/test_business_insight.py
git commit -m "feat: add product optimization and business insight tools with tests"
```

---

### Task 12：OAuth 中间件

**Files:**
- Create: `visable-mcp-server/auth/oauth.py`
- Modify: `visable-mcp-server/server.py`

Accio MCP Gateway 在每次工具调用时，会在 HTTP Header 中注入 `Authorization: Bearer <token>`。MCP Server 需要从 context 中读取此 token 并传给各工具。

- [ ] **Step 1: 创建 auth/oauth.py**

```python
# auth/oauth.py
from fastmcp import Context


def extract_token(ctx: Context) -> str:
    """从 MCP 请求 context 中提取 OAuth token"""
    auth_header = ctx.request_context.request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    return auth_header[len("Bearer "):]
```

- [ ] **Step 2: 更新 server.py，在工具中注入 token**

```python
# server.py
from fastmcp import FastMCP, Context
from auth.oauth import extract_token
from tools.store_diagnosis import get_store_overview, get_traffic_analysis, get_conversion_funnel
from tools.product_optimization import get_product_detail, suggest_title, suggest_description
from tools.business_insight import get_business_metrics, get_competitor_analysis, generate_report

mcp = FastMCP("visable-mcp-server")


@mcp.tool()
async def get_store_overview_tool(ctx: Context) -> dict:
    """获取店铺健康度概览"""
    token = extract_token(ctx)
    return await get_store_overview(token)


@mcp.tool()
async def get_traffic_analysis_tool(ctx: Context, period: str = "30d") -> dict:
    """获取店铺流量来源分布，period 支持 7d/30d/90d"""
    token = extract_token(ctx)
    return await get_traffic_analysis(token, period)


@mcp.tool()
async def get_conversion_funnel_tool(ctx: Context) -> dict:
    """获取曝光→点击→询盘→订单各环节转化率"""
    token = extract_token(ctx)
    return await get_conversion_funnel(token)


@mcp.tool()
async def get_product_detail_tool(ctx: Context, product_id: str) -> dict:
    """获取商品详情"""
    token = extract_token(ctx)
    return await get_product_detail(token, product_id)


@mcp.tool()
async def suggest_title_tool(ctx: Context, product_id: str, current_title: str) -> dict:
    """生成标题优化建议"""
    token = extract_token(ctx)
    return await suggest_title(token, product_id, current_title)


@mcp.tool()
async def suggest_description_tool(ctx: Context, product_id: str) -> dict:
    """生成描述优化建议"""
    token = extract_token(ctx)
    return await suggest_description(token, product_id)


@mcp.tool()
async def get_business_metrics_tool(ctx: Context, period: str = "30d") -> dict:
    """获取业务核心指标"""
    token = extract_token(ctx)
    return await get_business_metrics(token, period)


@mcp.tool()
async def get_competitor_analysis_tool(ctx: Context, category: str, period: str = "30d") -> dict:
    """获取竞品对比数据"""
    token = extract_token(ctx)
    return await get_competitor_analysis(token, category, period)


@mcp.tool()
async def generate_report_tool(ctx: Context, report_type: str, period: str = "30d") -> dict:
    """生成经营报告，report_type 支持 trend/competitor/summary"""
    token = extract_token(ctx)
    return await generate_report(token, report_type, period)


if __name__ == "__main__":
    mcp.run()
```

- [ ] **Step 3: 本地启动验证**

```bash
python server.py
```

Expected: MCP Server 启动，无报错，输出类似 `Serving MCP server on stdio`

- [ ] **Step 4: 提交**

```bash
git add auth/oauth.py server.py
git commit -m "feat: add OAuth token extraction middleware and wire all tools"
```

---

## Phase 3：Integration（两仓库联动）

### Task 13：connectors.json

**Files:**
- Modify: `visable-plugin/connectors/connectors.json`

> ⚠️ **此任务依赖向 Accio 确认的信息**：MCP Server 部署 URL（需先部署 visable-mcp-server）、OAuth `redirect_uri`（需 Accio 提供）。先填 placeholder，待信息到位后更新。

- [ ] **Step 1: 创建 connectors.json（placeholder 版本）**

切换回 `visable-plugin` 仓库：

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

- [ ] **Step 2: 验证 JSON**

```bash
python3 -c "import json; json.load(open('connectors/connectors.json')); print('connectors.json OK')"
```

Expected: `connectors.json OK`

- [ ] **Step 3: 提交**

```bash
git add connectors/connectors.json
git commit -m "feat: add connectors.json (placeholder URLs, pending Accio confirmation)"
```

- [ ] **Step 4: 待 Accio 确认后，用真实地址替换**

收到 Accio 提供的以下信息后，更新对应字段：
- `mcpServers.visable-server.url` → 真实 MCP Server 部署地址
- `oauth.visable.authorization_url` → 真实 OAuth 授权地址
- `oauth.visable.token_url` → 真实 token 地址

```bash
git add connectors/connectors.json
git commit -m "chore: update connectors.json with real MCP and OAuth URLs"
```

---

### Task 14：CI Pipeline（release.yml）

**Files:**
- Create: `visable-plugin/.github/workflows/release.yml`

> ⚠️ **此任务依赖向 Accio 确认的信息**：`phoenix-gateway` 版本登记 endpoint 和鉴权方式。`ACCIO_CALLBACK_URL` 和 `ACCIO_API_KEY` 先作为 GitHub Secret 占位，待 Accio 提供后填入。

- [ ] **Step 1: 创建 release.yml**

```yaml
name: Release Plugin

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: 读取版本号
        id: version
        run: echo "VERSION=${GITHUB_REF_NAME#v}" >> $GITHUB_OUTPUT

      - name: 打包 plugin.zip（排除 .git、.github）
        run: |
          zip -r plugin.zip . \
            --exclude ".git/*" \
            --exclude ".github/*" \
            --exclude "*.DS_Store"

      - name: 生成 manifest.snapshot.json
        run: |
          cat plugin.json | python3 -c "
          import json, sys
          manifest = json.load(sys.stdin)
          manifest['sourceTag'] = '${{ github.ref_name }}'
          manifest['sourceCommit'] = '${{ github.sha }}'
          manifest['builtAt'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
          print(json.dumps(manifest, indent=2))
          " > manifest.snapshot.json

      - name: 计算 sha256
        run: sha256sum plugin.zip | awk '{print $1}' > plugin.zip.sha256

      - name: 验证制品
        run: |
          echo "=== plugin.zip size ==="
          ls -lh plugin.zip
          echo "=== sha256 ==="
          cat plugin.zip.sha256
          echo "=== manifest.snapshot.json ==="
          cat manifest.snapshot.json

      - name: 上传制品到对象存储
        # TODO: 待 Accio 确认对象存储方案后补充
        # 若使用 OSS：
        # run: ossutil cp plugin.zip oss://accio-plugins/visable-assistant/${{ steps.version.outputs.VERSION }}/
        run: echo "⚠️ 上传步骤待补充（需向 Accio 确认存储方案）"

      - name: 向 phoenix-gateway 发起版本登记回调
        # TODO: 待 Accio 确认回调 endpoint 和鉴权方式后补充
        run: |
          echo "⚠️ 回调步骤待补充（需向 Accio 确认 endpoint 和鉴权）"
          # 示例结构（待替换）：
          # curl -X POST "${{ secrets.ACCIO_CALLBACK_URL }}" \
          #   -H "Authorization: Bearer ${{ secrets.ACCIO_API_KEY }}" \
          #   -H "Content-Type: application/json" \
          #   -d "{
          #     \"pluginId\": \"visable-assistant\",
          #     \"version\": \"${{ steps.version.outputs.VERSION }}\",
          #     \"sha256\": \"$(cat plugin.zip.sha256)\",
          #     \"artifactUrl\": \"<待填入>\",
          #     \"sourceTag\": \"${{ github.ref_name }}\",
          #     \"sourceCommit\": \"${{ github.sha }}\"
          #   }"
```

- [ ] **Step 2: 提交**

```bash
git add .github/workflows/release.yml
git commit -m "feat: add CI release workflow (artifact upload and callback pending Accio info)"
```

- [ ] **Step 3: 本地验证打包逻辑（不需要触发 GitHub Actions）**

```bash
zip -r /tmp/plugin-test.zip . --exclude ".git/*" --exclude ".github/*"
ls -lh /tmp/plugin-test.zip
unzip -l /tmp/plugin-test.zip | head -30
```

Expected: zip 包存在，内容包含 `plugin.json`、`agents/`、`connectors/`、`resources/` 等目录，不包含 `.git/`

---

## 验收清单

- [ ] `visable-plugin` 仓库：所有 JSON 文件格式合规，可通过 `python3 -c "import json; json.load(open(...))"` 验证
- [ ] `visable-plugin` 仓库：三个 SKILL.md 触发条件清晰，执行步骤具体可执行
- [ ] `visable-mcp-server` 仓库：`pytest tests/ -v` 全部 PASS
- [ ] `visable-mcp-server` 仓库：`python server.py` 本地启动无报错
- [ ] CI：本地打包逻辑验证通过（plugin.zip 内容正确，不含 .git）
- [ ] 待 Accio 确认后：connectors.json 填入真实 URL，CI 补全上传和回调步骤
