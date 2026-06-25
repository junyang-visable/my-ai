# Jira JQL 参考（候选 ticket 池）

JQL 只用于**召回候选 ticket**，最终统计以 changelog / `created` 时间为准。

## 默认候选池（推荐）

```
(
  assignee = currentUser()
  OR reporter = currentUser()
  OR assignee was currentUser()
)
AND (
  updated >= "{start}" AND updated < "{end_exclusive}"
  OR created >= "{start}" AND created < "{end_exclusive}"
)
ORDER BY updated DESC
```

`{end_exclusive}` = 统计结束日的 **次日**（如周期至 6-25 → 用 `2026-06-26`）。**不要用** `updated <= "{end}"`：Jira 将其视为 ≤ 当日 00:00，会漏掉结束日当天所有变更。

`updated` 与 `created` 的 OR 确保：期内新建的、以及期内有任意字段更新的 ticket 都能进入候选池。

## 仅期内新建（辅助查询，可选）

与用户相关的期内新建，用于交叉校验 `created` 事件：

```
reporter = currentUser()
AND created >= "{start}" AND created < "{end_exclusive}"
```

```
assignee = currentUser()
AND created >= "{start}" AND created < "{end_exclusive}"
```

## 状态变更近似召回（JQL 无法按 changelog 时间过滤）

Jira JQL **不能**表达「status 在某日变更」。以下仅作补充召回，**不能**作为状态变更计数依据：

```
assignee = currentUser()
AND status changed AFTER "{start}" BEFORE "{end_exclusive}"
```

召回后仍必须用 changelog 验证 `status_change` 的 `at` 是否在范围内。

## 用户相关条件

| 场景 | JQL |
|------|-----|
| 当前指派给我 | `assignee = currentUser()` |
| 我创建的 | `reporter = currentUser()` |
| 曾指派给我 | `assignee was currentUser()` |
| 我关注的 | `watcher = currentUser()` |

## 项目与类型过滤

```
AND project in (FE, WEB)
AND issuetype in (Story, Bug, Task)
```

## 日期格式

```
updated >= "2026-06-01" AND updated < "2026-06-08"
created >= "2026-06-01" AND created < "2026-06-08"
```

## 分页

`searchJiraIssuesUsingJql`：`maxResults` 100，循环 `nextPageToken` 直至结束。

## Rovo 降级

JQL 失败时用 MCP `search`，结果仍须 `getJiraIssue` + changelog 做事件抽取。
