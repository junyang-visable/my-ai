---
name: jira-work-summary
description: >-
  Queries Jira via Atlassian MCP and aggregates ticket change events (created,
  status transitions, assignee/priority changes) that occurred within a user-
  specified date range on the current user's tickets, then synthesizes a work
  summary. Use for work summaries, weekly reports, sprint recaps, Jira changelog
  analysis, or when the user mentions ticket changes, status updates, new issues,
  or a time range (本周、上周、本月、最近N天).
---

# Jira 工作总结（按变动事件统计）

通过 `user-atlassian-visable` MCP，统计**用户给定时间范围内实际发生的 ticket 变动**（新增、状态变更、指派变更等），并生成工作总结。

## 核心原则

**统计对象是「变动事件」，不是 ticket 当前快照。**

| 正确 | 错误 |
|------|------|
| 6 月 3 日 status 从 In Progress → Done | ticket 当前是 Done，故计入本周期 |
| 6 月 1 日新建的 FE-123 | 指派给我且 `updated` 在范围内，但期内无实质变更 |
| changelog `created` 落在 `[start, end]` 内的每条变更 | 仅用 JQL `updated` 作为最终统计依据 |

JQL `updated` / `created` 仅用于**缩小候选 ticket 集合**；最终计数与归类必须以 **changelog 时间戳** 或 **issue.created** 为准。

## 前置条件

1. MCP `user-atlassian-visable` 已启用且已认证。
2. 调用 MCP 工具前先读取 schema（`mcps/user-atlassian-visable/tools/*.json`）。
3. 只读：不创建、编辑、流转 ticket，不写 worklog。

## 编排流程

```
Phase 1: 身份与连接
Phase 2: 时间范围 → start / end（事件过滤边界）
Phase 3: JQL 候选 ticket 池（宽召回）
Phase 4: 变动事件抽取与分类（changelog + created）
Phase 5: 按变动类型汇总输出
```

---

## Phase 1：身份与连接

并行调用 `getAccessibleAtlassianResources`、`atlassianUserInfo`，取得 `cloudId`、`accountId`、`displayName`。

---

## Phase 2：时间范围

解析闭区间 `[start, end]`（含首尾日）。默认时区 `Asia/Shanghai`（报告中标注）。

| 用户表述 | 规则 |
|----------|------|
| 本周 / 上周 / 本月 / 最近 N 天 | 按自然语义 |
| 明确日期 | 用户起止日 |
| 未指定 | 默认上周一至上周日 |

产出：

- `start_iso` / `end_iso`：过滤 changelog、comment、`created` 用
- `start_jql` / `end_jql`：`YYYY-MM-DD`，候选池 JQL 用

---

## Phase 3：候选 ticket 池（宽召回）

用 JQL 拉取「期内**可能**有变动」的 ticket，避免漏掉「很久未更新但期内有状态变更」的 edge case（`updated` 与 changelog 通常一致，但召回要宽）。

### 默认候选 JQL

```
(
  assignee = currentUser()
  OR reporter = currentUser()
  OR assignee was currentUser()
)
AND (
  updated >= "{start_jql}" AND updated <= "{end_jql}"
  OR created >= "{start_jql}" AND created <= "{end_jql}"
)
ORDER BY updated DESC
```

用户指定项目时加 `AND project = {KEY}`。更多模式见 [references/jql-patterns.md](references/jql-patterns.md)。

### 检索

`searchJiraIssuesUsingJql`：`maxResults` 100，分页至结束。

```json
{
  "fields": ["summary", "status", "issuetype", "priority", "project", "assignee", "reporter", "created", "updated", "resolution", "comment"],
  "responseContentFormat": "markdown"
}
```

候选数 > 50 时提示用户是否缩小项目范围，或继续全量。

---

## Phase 4：变动事件抽取

对每个候选 ticket 调用 `getJiraIssue`：`expand=changelog`，`responseContentFormat=markdown`。

### 4.1 新增（Created）

若 `fields.created` ∈ `[start_iso, end_iso]`，记为 **新增事件**：

| 字段 | 值 |
|------|-----|
| type | `created` |
| at | `created` |
| ticket | key, summary, issuetype, project |
| actor | `reporter`（创建人） |
| 与我关系 | reporter=我 / assignee=我 / 仅创建 |

### 4.2 Changelog 事件

遍历 `changelog.histories`，仅保留 `history.created` ∈ `[start_iso, end_iso]`。

对每条 `history`，遍历 `items[]`，按 `field` 拆成独立事件（一条 history 含多个 field 则多条事件）：

| field（常见） | type | 记录内容 |
|---------------|------|----------|
| `status` | `status_change` | `fromString` → `toString`，时间、操作人 |
| `assignee` | `assignee_change` | 原指派人 → 新指派人；是否指派给我 |
| `priority` | `priority_change` | from → to |
| Sprint 相关 | `sprint_change` | from → to |
| `resolution` | `resolution_change` | from → to |
| 其他 | `field_change` | field + from → to |

每条事件附带：`at`、`author`、`ticket` 上下文。

### 4.3 用户相关过滤（默认）

默认只统计与**当前用户**相关的变动：

| 事件类型 | 计入条件（满足任一） |
|----------|----------------------|
| `created` | 我创建的，或创建时指派给我，或当前指派给我 |
| `status_change` 等 changelog | `author.accountId` = 我，**或** 变更发生时我是 assignee（指派给我后的变更） |
| `assignee_change` | 新 assignee 是我（指派给我），或 author 是我 |

用户明确要求「我操作过的全部」→ 仅 `author` = 我。  
用户明确要求「我名下 ticket 的全部变动」→ 候选池内 ticket 的期内所有 changelog 均计入。

### 4.4 状态变更子类（工作总结常用）

在 `status_change` 上进一步标记：

| 子类 | 判定 |
|------|------|
| `completed` | `toString` 为 Done / Closed / Resolved / 已完成 等完成态 |
| `reopened` | 从完成态回到进行中 |
| `started` | 从 Open / To Do / 待办 → In Progress / 进行中 |
| `other_transition` | 其余状态流转 |

完成态名称因实例而异，以 changelog 原文匹配。

### 4.5 评论（可选）

仅当用户要求「评论/协作」时：过滤 `comment.created` ∈ 范围。默认报告可不单独成章，合并进协作备注。

### 4.6 降级

`changelog` 不可用：标注该 key，**不臆造**状态变更；若 `created` 在范围内仍可记新增。

---

## Phase 5：汇总输出

### 统计口径（概览表）

| 指标 | 含义 |
|------|------|
| 新增 ticket | `created` 事件数 |
| 状态变更 | `status_change` 事件数 |
| 其中：完成 | 子类 `completed` |
| 其中：重新打开 | 子类 `reopened` |
| 指派变更 | `assignee_change`（含指派给我） |
| 其他字段变更 | priority / sprint / resolution / field_change |
| 涉及 ticket 数 | 至少有一条期内事件的去重 key 数 |

**禁止**用「候选 JQL 返回条数」或「当前 status=Done 的数量」代替上表。

### 输出结构

使用 [references/summary-template.md](references/summary-template.md)。章节按**变动类型**组织，而非仅「已完成 / 进行中」：

1. 概览（上表）
2. **新增 ticket**（期内创建）
3. **状态变更**（按子类或按目标状态分组，附 from → to）
4. **其他变动**（指派、优先级、Sprint 等）
5. 按项目分布（各类型事件数）
6. 数据说明（时间范围、过滤规则、候选 JQL、事件总数）

### 呈现要求

- 每条事件：`[KEY]` + 摘要 + 变动描述 + 时间 + 操作人（若非本人且相关则标注）
- 状态变更写清 **from → to**，不写仅「已更新」
- 保存文件：`jira-work-summary-{start}-{end}.md`

变动类型细则见 [references/change-types.md](references/change-types.md)。

---

## 错误处理

| 情况 | 处理 |
|------|------|
| MCP 认证失败 | 提示检查 Atlassian MCP 连接 |
| JQL 失败 | 简化为 `assignee = currentUser() AND updated >= ...` 重试 |
| 单条 issue 失败 | 记入失败列表，继续其余 |
| 零事件 | 说明可能原因（范围过窄、过滤过严），建议放宽用户相关条件或扩大日期 |

## 附加资源

- [references/change-types.md](references/change-types.md) — 变动类型与分类规则
- [references/jql-patterns.md](references/jql-patterns.md) — 候选池 JQL
- [references/summary-template.md](references/summary-template.md) — 报告模板
