---
name: 记住你的偏好
version: "2.0.0"
description: |
  供应商自进化能力。支持多供应商记忆隔离，自动追踪全局偏好、规则以及每个供应商的业务画像，使 Agent 对同一用户越用越精准。

  触发场景：
    - 每次新 session 启动时自动加载全局偏好、规则和当前供应商画像
    - 用户切换供应商时加载对应供应商的画像和历史
    - 用户对话中隐含或显式表达身份信息、操作偏好、硬性约束时自动采集
    - 用户主动要求"记住"、"忘记"、"清除"记忆数据时立即执行
    - 任务完成或用户发送结束信号时执行闲时反思
  重要限制：不存储密码、API Key、银行账号等敏感信息；所有数据本地存储，不上传外部。
enabled: true
---

# Supplier Self-Evolving

## 概述

你具备多供应商自进化能力，覆盖两个层级：

**全局层**（适用于所有供应商）：
1. **操作偏好** — 记住用户「怎么用」（交互风格、输出格式等）
2. **全局规则** — 记住「全局约束」（适用于所有供应商的规则）

**供应商层**（按供应商隔离）：
3. **供应商画像** — 记住每个供应商「是谁」（平台、品类、市场、规模等）
4. **供应商规则** — 记住针对特定供应商的约束
5. **任务历史** — 记住针对该供应商「做了什么」

---

## 数据文件架构

```
memory/
├── GLOBAL_PREFERENCES.json    ← 全局操作偏好（适用于所有供应商）
├── GLOBAL_RULES.json           ← 全局规则（适用于所有供应商）
├── suppliers/
│   ├── INDEX.json              ← 供应商列表（id → name 映射 + 最后活跃时间）
│   └── <supplier_id>/
│       ├── SUPPLIER_PROFILE.json
│       ├── LEARNED_RULES.json  ← 该供应商专属规则
│       └── TASK_HISTORY.json
├── state_snapshot.json         ← 技能执行结果全局快照
└── diary/YYYY-MM-DD.md         ← 反思日记
```

### 文件职责边界

| 文件 | 存什么 | 不存什么 |
|------|--------|---------|
| GLOBAL_PREFERENCES.json | 用户希望 agent 怎么做（输出方式、参数默认值） | 供应商信息、硬规则 |
| GLOBAL_RULES.json | 全局硬规则（跨所有供应商生效） | 可灵活调整的偏好 |
| suppliers/INDEX.json | 供应商 id→name 映射、最后活跃时间 | 详细画像 |
| suppliers/<id>/SUPPLIER_PROFILE.json | 该供应商的业务身份信息 | 用户偏好 |
| suppliers/<id>/LEARNED_RULES.json | 针对该供应商的专属规则 | 全局规则 |
| suppliers/<id>/TASK_HISTORY.json | 针对该供应商的任务摘要 | 画像、偏好 |

---

## 供应商识别与切换

### suppliers/INDEX.json 格式

```json
{
  "version": "1.0",
  "lastUpdated": "2026-05-06T10:00:00Z",
  "lastActiveId": "supplier-001",
  "suppliers": {
    "supplier-001": {
      "name": "ABC 五金",
      "platform": "wlw",
      "lastActiveAt": "2026-05-06T10:00:00Z"
    },
    "supplier-002": {
      "name": "XYZ 机械",
      "platform": "Europages",
      "lastActiveAt": "2026-05-05T14:30:00Z"
    }
  }
}
```

### 供应商识别规则

每次执行涉及供应商的技能（visable-supplier-diagnostics / visable-product-opt / visable-business-insight）时，按以下顺序确认当前供应商（**不主动追问，静默完成**）：

1. **用户明确提到供应商名称** → 在 INDEX.json 中匹配，确认后使用，更新 `lastActiveId`。
2. **用户明确要求切换**（「换成…」「切换到…」）→ 列出供应商名称供选择，等待用户回复。
3. **其余情况（包括多供应商但用户未说明）** → 直接使用 `lastActiveId`，**不追问**，回复时自然带出当前供应商名称。
4. **INDEX.json 不存在（首次使用）** → 询问供应商名称，创建 INDEX.json 和对应的 `suppliers/<id>/` 目录。

### 最后活跃供应商

- 每次确认使用某供应商后，更新 `INDEX.json` 的 `lastActiveId` 和该供应商的 `lastActiveAt`。
- 下次 session 启动时，将 `lastActiveId` 对应的供应商作为默认候选。

---

## 1. 供应商画像：SUPPLIER_PROFILE.json

### 字段

**Slots**（7 个）：`supplier_name`(string), `platform`(string/string[]), `categories`(string/string[]), `target_markets`(string/string[]), `monthly_orders`(string), `team_size`(string), `pain_points`(string[])

每个 slot 含元数据：`confidence`("explicit"/"inferred"), `updatedAt`(ISO 8601), `source`("conversation"/"mcp")

```json
{
  "version": "1.0",
  "lastUpdated": "2026-05-06T10:00:00Z",
  "slots": {
    "supplier_name": { "label": "供应商名称", "value": "ABC 五金", "confidence": "explicit", "updatedAt": "2026-05-06T10:00:00Z", "source": "conversation" },
    "platform": { "label": "经营平台", "value": "wlw", "confidence": "explicit", "updatedAt": "2026-05-06T10:00:00Z", "source": "conversation" },
    "categories": { "label": "主营品类", "value": ["五金工具", "机械零件"], "confidence": "explicit", "updatedAt": "2026-05-06T10:00:00Z", "source": "conversation" }
  }
}
```

### 画像追问策略

- **前 3 轮不追问**，先建立信任
- **每次最多问 1-2 个 slot**
- 追问优先级：supplier_name = platform = categories > target_markets = pain_points > monthly_orders > 其他

---

## 2. 全局操作偏好：GLOBAL_PREFERENCES.json

```json
{
  "version": "1.0",
  "lastUpdated": "2026-05-06T10:00:00Z",
  "interaction": {
    "output_format": { "value": "table", "confidence": "explicit", "updatedAt": "2026-05-06T10:00:00Z" },
    "response_style": { "value": "concise", "confidence": "explicit", "updatedAt": "2026-05-06T10:00:00Z" }
  },
  "product_optimization": {
    "title_style": { "value": "简洁精准", "confidence": "explicit", "updatedAt": "2026-05-06T10:00:00Z" }
  }
}
```

### 偏好采集信号

| 用户说的话 | 字段 | 值 |
|-----------|------|-----|
| "直接说结论" | interaction.response_style | "concise" |
| "用表格对比" | interaction.output_format | "table" |
| "标题简洁一点" | product_optimization.title_style | "简洁精准" |

---

## 3. 规则（全局 + 供应商级）

### GLOBAL_RULES.json（全局生效）

```json
{
  "version": "1.0",
  "lastUpdated": "2026-05-06T10:00:00Z",
  "rules": [
    {
      "id": "rule-g001",
      "rule": "商品描述不要超过200字",
      "context": "product_optimization",
      "source": "用户纠正",
      "createdAt": "2026-05-06T10:00:00Z",
      "reinforceCount": 1
    }
  ]
}
```

### suppliers/<id>/LEARNED_RULES.json（供应商专属）

结构相同，但仅对特定供应商生效。

### 判断写入哪里

- 用户说"所有供应商都不要..." → 写入 GLOBAL_RULES.json
- 用户说"这家供应商不要..." 或未说明但当前有活跃供应商 → 写入该供应商的 LEARNED_RULES.json

---

## 生命周期

### 1. Session 启动

1. 读取 GLOBAL_PREFERENCES.json、GLOBAL_RULES.json
2. 读取 suppliers/INDEX.json，了解供应商列表
3. 将 lastActiveId 对应的供应商画像作为默认候选加载

### 2. 持续采集

**主动记忆触发**：

| 触发句式 | 动作 |
|---------|------|
| "记住：ABC 五金主要做欧洲市场" | → suppliers/supplier-001/SUPPLIER_PROFILE.json |
| "记住：所有供应商描述不超过200字" | → GLOBAL_RULES.json |
| "新增一个供应商，叫 XYZ 机械" | → 在 INDEX.json 注册，创建目录 |
| "删除 ABC 五金" | → 从 INDEX.json 移除，询问是否删除数据 |
| "你记住了 ABC 五金什么" | → 读取该供应商目录下的文件，自然语言概述 |
| "你记住了我什么" | → 读取全局偏好/规则 + 所有供应商画像，逐一概述 |

### 3. 闲时反思（用户发送结束信号后，同一 session 最多 1 次）

反思步骤：
1. 补写未写入的全局偏好/规则
2. 补写当前供应商的画像更新
3. 写入 suppliers/<id>/TASK_HISTORY.json
4. 写入 `diary/YYYY-MM-DD.md`

---

## 隐私与边界

- **不存储敏感信息**：不记录密码、API Key、银行账号等
- **本地存储**：所有数据在记忆目录下，不上传到外部
- **用户可控**：用户可随时查询、清除任何供应商的记忆数据
