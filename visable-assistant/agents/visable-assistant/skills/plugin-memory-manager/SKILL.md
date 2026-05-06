---
name: Plugin级Memory管理器
version: "1.0.0"
description: |
  Plugin 级记忆与联动管理器。包含三个子模块：
  1. 追问记忆（memory_manager.py）— 按 Skill 隔离追踪用户追问过的历史问题
  2. 执行结果（outcome_manager.py）— 按 Skill 存储每次执行的结果摘要
  3. 信息联动（linker.py）— 跨 Skill 读取关联结果，生成全局经营快照
  此技能不由用户直接调用，而是由 agents.md 中的规则在技能执行前后自动触发。
---

## 一、追问记忆

`scripts/memory_manager.py`

```bash
python scripts/memory_manager.py read <skill_name>
python scripts/memory_manager.py update <skill_name> "<query>"
python scripts/memory_manager.py compress <skill_name>
python scripts/memory_manager.py top <skill_name> [N]
python scripts/memory_manager.py distill <skill_name>
```

数据存储：`skills/<skill_name>/memory/queries.json`

---

## 二、执行结果

`scripts/outcome_manager.py`

```bash
python scripts/outcome_manager.py write <skill_name> '<json摘要>'
python scripts/outcome_manager.py read <skill_name>
python scripts/outcome_manager.py read <skill_name> --latest
python scripts/outcome_manager.py clean <skill_name>
```

数据存储：`skills/<skill_name>/memory/outcomes.json`

写入格式（必须包含 `summary` 字段）：

```json
{
  "summary": "店铺健康度 72分，缺少公司认证和产品图片",
  "alerts": ["公司认证未填写"],
  "opportunities": ["补全认证后可提升买家信任度"]
}
```

### 各 Skill 的 outcome 写入规范

| Skill | summary 应包含 | 额外字段 | 保留天数 |
|-------|---------------|---------|---------|
| store-diagnostics | 健康度评分 + 主要缺失项 | alerts | 7 |
| product-optimization | 优化的商品 + 主要优化点 | 无 | 30 |
| business-insight | 核心指标（订单/访客/转化）+ 趋势 | metrics, alerts, opportunities | 7 |

---

## 三、信息联动

`scripts/linker.py`

```bash
python scripts/linker.py context <skill_name>
python scripts/linker.py snapshot
python scripts/linker.py snapshot --read
```

数据存储：`memory/state_snapshot.json`
