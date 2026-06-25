# 变动事件类型定义

本 skill 区分 **工作进展事件**（写入报告）与 **维护性变更**（丢弃）。

## 工作进展事件（计入报告）

| type | 来源 | 说明 |
|------|------|------|
| `status_change` | changelog `field=status` | 状态流转 |
| `worklog_logged` | changelog `field=timespent` 且 `delta > 0` | 登记工时（增量） |
| `created` | `issue.fields.created` | 期内新建（默认保留；可省略） |

## 维护性变更（不提取）

| field / 模式 | 说明 |
|--------------|------|
| `description`、`summary` | 文档维护 |
| `timeestimate` | 登记工时时常自动调整，不单独列 |
| `assignee`、`priority`、`resolution` | 元数据 |
| `Link`、`IssueParentAssociation` | 关联维护 |
| Sprint、labels、components、`comment` | 其他 |

## status_change 结构

```json
{
  "type": "status_change",
  "subtype": "completed | reopened | started | other_transition",
  "at": "ISO8601",
  "ticket": { "key", "summary", "issuetype", "project" },
  "author": { "accountId", "displayName" },
  "from": "Backlog",
  "to": "In Progress"
}
```

## worklog_logged 结构

```json
{
  "type": "worklog_logged",
  "at": "ISO8601",
  "ticket": { "key", "summary" },
  "author": { "accountId", "displayName" },
  "delta_seconds": 14400,
  "delta_human": "4h",
  "total_after_seconds": 14400
}
```

### timespent 解析规则

- `fromString` / `toString` 为**秒**数字符串；`from` 为空或 null → 0
- `delta_seconds = parseInt(toString) - parseInt(fromString)`；`delta_seconds <= 0` 丢弃
- `delta_human`：秒 → `Xh Ym`（如 14400 → `4h`，1800 → `30m`）

### 数据源说明

Atlassian MCP 无只读 getWorklog 工具；工时事件来自 changelog 的 `timespent` 增量，与 Jira 登记工时在 UI 中的记录一致。

## status_change 子类

| subtype | 规则 |
|---------|------|
| `completed` | to ∈ Done, Closed, Resolved, 已完成, … |
| `reopened` | from 完成态 → to 进行中 |
| `started` | from ∈ Backlog, To Do, Open, 待办 → to ∈ In Progress |
| `other_transition` | 其余 |

## 用户相关过滤（默认）

| 事件 | 默认计入 |
|------|----------|
| `status_change` | `author` = 我，或我是 assignee |
| `worklog_logged` | **`author` = 我**（本人登记） |
| `created` | 我 reporter 或 assignee = 我 |

## 去重与同 history

- 同一 `at`、同一 field、相同变更：**一条**
- 同一 history 含 `status` + `timespent`：**两条独立事件**（关单同时记工时常见）
- 同一 history 含 `timespent` + `timeestimate`：**只记 timespent**

## 报告叙述映射

| 事件 | 表述示例 |
|------|----------|
| `status_change` + `completed` | 完成 FE-850：Backlog → Done（6-23 17:20） |
| `status_change` + `started` | 启动 FE-837：Backlog → In Progress |
| `worklog_logged` | FE-850 登记工时 +4h（6-23 17:21） |
| `created` | 新建 FE-862：FE – Domain deployment |

## 反例

| changelog | 处理 |
|-----------|------|
| description 更新 | 忽略 |
| timeestimate：3600 → 0 | 忽略（不单独列） |
| timespent：0 → 14400 | 记 `worklog_logged` +4h |
