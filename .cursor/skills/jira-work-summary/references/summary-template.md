# 工作总结输出模板（按变动事件）

## 标准版（默认）

```markdown
# 工作变动总结 · {display_name}

**统计周期**：{start} – {end}（{timezone}）
**统计口径**：周期内发生的变动事件（非 ticket 当前状态）
**数据源**：{site_name} · Jira
**用户相关规则**：{filter_rule_description}

---

## 概览

| 变动类型 | 事件数 |
|----------|--------|
| 新增 ticket | {created_count} |
| 状态变更 | {status_change_count} |
| ├ 完成（→ Done/Resolved 等） | {completed_count} |
| ├ 重新打开 | {reopened_count} |
| ├ 启动/进行中 | {started_count} |
| └ 其他状态流转 | {other_transition_count} |
| 指派变更 | {assignee_change_count} |
| 优先级 / Sprint / 其他 | {other_field_count} |
| **涉及 ticket（去重）** | {unique_ticket_count} |

---

## 新增 ticket（{created_count}）

| 时间 | Key | 类型 | 摘要 | 创建人 |
|------|-----|------|------|--------|
| {at} | {KEY} | {issuetype} | {summary} | {reporter} |

本周期无新增 ticket 时写：「本周期无新增 ticket。」

---

## 状态变更（{status_change_count}）

### 完成（{completed_count}）

| 时间 | Key | 流转 | 操作人 |
|------|-----|------|--------|
| {at} | {KEY} | {from} → {to} | {author} |

### 其他状态流转

| 时间 | Key | 流转 | 操作人 | 备注 |
|------|-----|------|--------|------|
| {at} | {KEY} | {from} → {to} | {author} | {started/reopened/…} |

本周期无状态变更时写：「本周期无状态变更。」

---

## 其他变动

### 指派变更（{assignee_change_count}）

| 时间 | Key | 变更 | 操作人 |
|------|-----|------|--------|
| {at} | {KEY} | {from_assignee} → {to_assignee} | {author} |

### 优先级 / Sprint / _resolution 等（{other_field_count}）

| 时间 | Key | 字段 | 变更 | 操作人 |
|------|-----|------|------|--------|
| {at} | {KEY} | {field} | {from} → {to} | {author} |

---

## 按项目分布

| 项目 | 新增 | 状态变更 | 其他变动 | 涉及 ticket |
|------|------|----------|----------|-------------|
| {PROJECT} | {n} | {m} | {k} | {u} |

---

## 数据说明

- 候选池 JQL：`{candidate_jql}`
- 候选 ticket：{candidate_count}；changelog 拉取失败：{failed_keys}
- 事件总数：{total_events}；去重 ticket：{unique_ticket_count}
- 生成时间：{generated_at}
```

## 简要版

```markdown
# 变动摘要 · {start} – {end}

**新增 {created_count}**：{KEY1} {summary1}（{at1}）；…

**状态变更 {status_change_count}**：
- 完成：{KEY2} {from}→{to}（{at2}）；…
- 其他：{KEY3} {from}→{to}（{at3}）；…

**其他**：{assignee/priority 一行概括}

涉及 {unique_ticket_count} 个 ticket。
```

## 填写规则

1. **状态变更必须写 from → to**，禁止只写「已更新」或「已完成」而无流转路径。
2. **完成数** = 子类 `completed` 的事件数，不等于「当前 status 为 Done 的 ticket 数」。
3. **新增** = `issue.created` 在周期内，与 changelog 无关。
4. 空章节保留标题并写「本周期无此项」。
5. Key 有 URL 时用 `[KEY](url)`。
