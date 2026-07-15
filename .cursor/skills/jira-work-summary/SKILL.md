---
name: jira-work-summary
description: >-
  Queries Jira via Atlassian MCP and tracks status transitions and worklog
  (timespent) on the current user's tickets within a date range to synthesize a
  work progress summary. Ignores metadata edits (description, links, etc.) as
  non-progress noise. Use for work summaries, weekly reports, sprint recaps,
  status or worklog tracking, or Jira + time range (本周、上周、本月、最近N天).
---

# Jira 工作总结（状态变更 + 工时 = 工作进展）

通过 `user-atlassian-visable` MCP，统计**用户给定时间范围内 ticket 的状态变更与工时登记**，作为工作进展总结。description、Link 等字段编辑属于日常维护，**不计入工作进展**。

## 核心原则

### 什么算「工作进展」

| 计入 | 不计入（changelog 中忽略，不出现在报告） |
|------|----------------------------------------|
| `status` 流转（`status_change`） | `description`、`summary`、评论正文 |
| `timespent` 增加（`worklog_logged`） | `timeestimate`（登记工时时常联动调整，不单独列） |
| 期内**新建** ticket（`created`，默认保留） | `assignee`、`priority`、Sprint |
| | `resolution`（通常与 status→Done 同批，不单独列） |
| | `Link`、`IssueParentAssociation`、labels、components |
| | 其余 `field_change` |

**统计对象**是期内 changelog 中的 **`status_change` 与 `worklog_logged` 事件**，不是 ticket 当前快照，也不是任意 `updated` 编辑。

MCP 无独立读 worklog API；**工时从 changelog `field=timespent` 的增量推断**（与 Jira UI 登记工时的记录方式一致）。

### 事件时间边界

| 正确 | 错误 |
|------|------|
| changelog 中 status 变更的 `created` 落在 `[start, end]` | ticket 当前是 Done 即计入本周期 |
| 6 月 25 日 Backlog → In Progress 记入报告 | description 在 6/25 更新记入工作进展 |
| 6 月 23 日登记 4h 工时（timespent +14400）记入报告 | 仅 timeestimate 联动变化记入报告 |
| 用 `updated < end+1天` 召回候选池 | 用 `updated <= end` 作上界（漏掉结束日当天） |

JQL 仅用于**候选 ticket 池**；进展计数以 changelog 中 `status` / `timespent` 的时间戳为准。

## 前置条件

1. MCP `user-atlassian-visable` 已启用且已认证。
2. 调用 MCP 工具前先读取 schema。
3. 只读：不创建、编辑、流转 ticket。

## 编排流程

```
Phase 1: 身份与连接
Phase 2: 时间范围
Phase 3: JQL 候选 ticket 池
Phase 4: 抽取 status_change + worklog_logged（+ 可选 created）
Phase 5: 按进展类型汇总输出
```

---

## Phase 1：身份与连接

并行调用 `getAccessibleAtlassianResources`、`atlassianUserInfo`，取得 `cloudId`、`accountId`、`displayName`。

---

## Phase 2：时间范围

闭区间 `[start, end]`（含首尾日）。默认时区 `Asia/Shanghai`。

| 用户表述 | 规则 |
|----------|------|
| 本周 / 上周 / 本月 / 最近 N 天 | 按自然语义 |
| 明确日期 | 用户起止日 |
| 未指定 | 默认上周一至上周日 |

产出：

- `start_iso` / `end_iso`：过滤 status / timespent changelog、`created`
- `start_jql`：下界 `YYYY-MM-DD`
- `end_jql_exclusive`：结束日 **次日** `YYYY-MM-DD`

**禁止** `updated <= "{end}"` / `created <= "{end}"`（Jira 视为 ≤ 当日 00:00，会漏掉结束日当天变更）。使用：

```
updated >= "{start_jql}" AND updated < "{end_jql_exclusive}"
created >= "{start_jql}" AND created < "{end_jql_exclusive}"
```

---

## Phase 3：候选 ticket 池

宽召回「期内可能有状态变更」的 ticket：

```
(
  assignee = currentUser()
  OR reporter = currentUser()
  OR assignee was currentUser()
)
AND (
  updated >= "{start_jql}" AND updated < "{end_jql_exclusive}"
  OR created >= "{start_jql}" AND created < "{end_jql_exclusive}"
)
ORDER BY updated DESC
```

补充召回（可选）：`status changed AFTER "{start_jql}" BEFORE "{end_jql_exclusive}"` — 见 [references/jql-patterns.md](references/jql-patterns.md)。

`searchJiraIssuesUsingJql`：`maxResults` 100，分页至结束。fields 无需 `comment`。

候选数 > 50 时提示是否缩小项目范围。

---

## Phase 4：进展事件抽取

对每个候选 ticket：`getJiraIssue`，`expand=changelog`。

遍历 `changelog.histories`，`history.created` ∈ `[start_iso, end_iso]`，在 `items[]` 中按 field 提取：

### 4.1 状态变更（`status_change`）

`field === "status"`（或 `fieldId === "status"`）：

| 记录 | 内容 |
|------|------|
| type | `status_change` |
| at | `history.created` |
| from / to | `fromString` → `toString` |
| author | 操作人 |
| ticket | key, summary, issuetype, project |

### 4.2 工时登记（`worklog_logged`）

`field === "timespent"`：

| 记录 | 内容 |
|------|------|
| type | `worklog_logged` |
| at | `history.created`（登记操作时间） |
| delta | `to` 秒 − `from` 秒（`fromString`/`toString` 为秒数字符串；`from` 为空视为 0） |
| delta_human | 人类可读，如 `4h`、`30m`（`delta` 秒换算） |
| total_after | 登记后累计 `timespent`（可选展示） |
| author | 操作人（登记人） |
| ticket | key, summary, … |

**仅当 `delta > 0`** 时计入（忽略误删/调减工时）。同一 `history` 若含 `timespent` + `timeestimate`，**只记 timespent**，跳过 `timeestimate`。

默认**只统计本人登记的工时**（`author.accountId` = 我）。用户要求「我名下 ticket 全部工时」时，可计入他人代登但 assignee 为我的记录（报告中标注登记人）。

### 4.3 同一 history 多字段

一条 changelog 可能同时含 `status` 与 `timespent`（如关单并登记工时）：**分别提取为独立事件**，各计一条。

### 4.4 显式跳过

description、assignee、priority、resolution、timeestimate、Link、IssueParentAssociation、Sprint、labels、components 及一切非 status / timespent 字段。

### 4.5 新建 ticket

若 `fields.created` ∈ `[start_iso, end_iso]` 且与我相关，记为 `created`。默认报告保留「新增任务」；用户要求「仅状态+工时」时可省略 created 章节。

### 4.6 用户相关过滤（默认）

| 事件 | 计入条件（满足任一） |
|------|----------------------|
| `status_change` | `author` = 我；或变更时我是 assignee |
| `worklog_logged` | **默认** `author` = 我（本人登记） |
| `created` | 我 reporter；或 assignee = 我 |

### 4.7 状态子类

| subtype | 判定 |
|---------|------|
| `completed` | to ∈ Done, Closed, Resolved, 已完成, … |
| `reopened` | from 完成态 → to 进行中 |
| `started` | from ∈ Backlog, To Do, Open, 待办 → to ∈ In Progress, 进行中 |
| `other_transition` | 其余 |

### 4.8 不采集

评论（除非用户明确要求）；非 status/timespent 的 changelog。

### 4.9 降级

changelog 不可用：标注该 key，不臆造状态或工时。

---

## Phase 5：汇总输出

### 概览表（仅进展相关）

| 指标 | 含义 |
|------|------|
| 状态变更 | `status_change` 事件总数 |
| ├ 完成 | subtype `completed` |
| ├ 重新打开 | `reopened` |
| ├ 启动/进行中 | `started` |
| └ 其他流转 | `other_transition` |
| 工时登记 | `worklog_logged` 条数 |
| 登记工时合计 | 各 `delta` 之和（人类可读，如 `12h 30m`） |
| 新增任务 | `created` 事件数 |
| 涉及 ticket | 有 status_change、worklog_logged 或 created 的去重 key 数 |

**禁止**将 description、`timeestimate` 单独变动等计入上表。

### 输出结构

见 [references/summary-template.md](references/summary-template.md)：

1. 概览
2. **状态变更明细**
3. **工时登记明细**（时间、key、登记量、登记人）
4. **新增任务**（可省略）
5. 按项目分布
6. 工作要点（状态流转 + 工时投入 + 新建任务）
7. 数据说明

### 呈现要求

- 状态变更写 **from → to** 与时间
- 工时写 **+{delta_human}**（如 `+4h`），附 ticket key
- 不写 description、Epic 关联、blocked by 等
- 保存：`jira-work-summary-{start}-{end}.md`

细则见 [references/change-types.md](references/change-types.md)。

---

## 错误处理

| 情况 | 处理 |
|------|------|
| MCP 认证失败 | 提示检查 Atlassian 连接 |
| JQL 失败 | 简化为 `assignee = currentUser() AND updated >= ...` |
| 单条 issue 失败 | 记入失败列表 |
| 零条进展事件 | 说明范围内无状态流转且无本人工时登记；勿用 description 充数 |

## 附加资源

- [references/change-types.md](references/change-types.md)
- [references/jql-patterns.md](references/jql-patterns.md)
- [references/summary-template.md](references/summary-template.md)
