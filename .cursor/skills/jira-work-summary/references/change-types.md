# 变动事件类型定义

本 skill 的统计单元是 **ChangeEvent**，不是 Issue。

## 事件结构（内部归一化）

```json
{
  "type": "created | status_change | assignee_change | priority_change | sprint_change | resolution_change | field_change | comment",
  "subtype": "completed | reopened | started | other_transition | null",
  "at": "ISO8601",
  "ticket": { "key", "summary", "issuetype", "project", "status" },
  "author": { "accountId", "displayName" },
  "field": "status",
  "from": "In Progress",
  "to": "Done",
  "relation_to_me": "actor | assignee | assignee_received | reporter | watcher"
}
```

## type 枚举

| type | 来源 | 说明 |
|------|------|------|
| `created` | `issue.fields.created` | 期内新建 ticket |
| `status_change` | changelog `field=status` | 状态流转 |
| `assignee_change` | changelog `field=assignee` | 指派人变更 |
| `priority_change` | changelog `field=priority` | 优先级变更 |
| `sprint_change` | changelog field 含 Sprint | Sprint 进出 |
| `resolution_change` | changelog `field=resolution` | 解决结果变更 |
| `field_change` | 其他 changelog field | 通用字段变更 |
| `comment` | comment.created | 仅按需启用 |

## status_change 子类 subtype

| subtype | 规则（to / from 匹配实例文案） |
|---------|------------------------------|
| `completed` | to ∈ Done, Closed, Resolved, 已完成, 已关闭, … |
| `reopened` | from ∈ 完成态 AND to ∈ 进行中态 |
| `started` | from ∈ Open, To Do, 待办, Backlog, … AND to ∈ In Progress, 进行中, … |
| `other_transition` | 其余 |

完成态、进行中态列表在首次运行时从 changelog 样本归纳，报告中可附「完成态匹配词」说明。

## 用户相关 relation_to_me

| 值 | 含义 |
|----|------|
| `actor` | 当前用户是 changelog author 或 reporter |
| `assignee` | 变更时我是 assignee |
| `assignee_received` | assignee 变更为我 |
| `reporter` | 我创建的 ticket |
| `watcher` | 我关注（仅当启用 watcher 召回时） |

默认过滤：至少一个 relation 非空即计入。

## 去重规则

- 同一 ticket、同一 `at`、同一 `field`、相同 from/to：**一条事件**
- 同一 ticket 多次 status 变更：**多条事件**（各计一次）
- `created` 与首条 changelog 可能同时存在：分别计入「新增」与对应变更

## 工作总结叙述映射

| 事件 | 报告中的表述示例 |
|------|------------------|
| `created` | 新建 FE-123：实现登录页埋点校验 |
| `status_change` + `completed` | 完成 FE-120：In Progress → Done（6-03 14:20） |
| `status_change` + `started` | 启动 FE-125：To Do → In Progress |
| `status_change` + `reopened` | 重新打开 FE-118：Done → In Progress |
| `assignee_change` + `assignee_received` | FE-130 指派给我 |
| `priority_change` | FE-122 优先级 High → Highest |
