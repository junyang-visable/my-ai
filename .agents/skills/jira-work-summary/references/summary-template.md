# 工作总结输出模板（状态变更 + 工时 = 工作进展）

## 标准版（默认）

```markdown
# 工作进展总结 · {display_name}

**统计周期**：{start} – {end}（{timezone}）
**统计口径**：周期内 **status 流转** + **本人登记工时**（timespent）；不含 description、timeestimate 联动等
**数据源**：{site_name} · Jira
**用户相关规则**：{filter_rule_description}

---

## 概览

| 指标 | 数量 |
|------|------|
| 状态变更 | {status_change_count} |
| ├ 完成 | {completed_count} |
| ├ 重新打开 | {reopened_count} |
| ├ 启动/进行中 | {started_count} |
| └ 其他流转 | {other_transition_count} |
| 工时登记（条数） | {worklog_count} |
| 登记工时合计 | {worklog_total_human} |
| 新增任务 | {created_count} |
| **涉及 ticket（去重）** | {unique_ticket_count} |

---

## 状态变更（{status_change_count}）

### 完成（{completed_count}）

| 时间 | Key | 摘要 | 流转 | 操作人 |
|------|-----|------|------|--------|
| {at} | {KEY} | {summary} | {from} → {to} | {author} |

### 启动 / 重新打开 / 其他流转

| 时间 | Key | 摘要 | 流转 | 操作人 | 备注 |
|------|-----|------|------|--------|------|
| {at} | {KEY} | {summary} | {from} → {to} | {author} | {subtype} |

本周期无状态变更时写：「本周期无状态变更。」

---

## 工时登记（{worklog_count}，合计 {worklog_total_human}）

| 时间 | Key | 摘要 | 登记量 | 登记人 |
|------|-----|------|--------|--------|
| {at} | {KEY} | {summary} | +{delta_human} | {author} |

本周期无工时登记时写：「本周期无工时登记。」

---

## 新增任务（{created_count}）

| 时间 | Key | 类型 | 摘要 | 创建人 |
|------|-----|------|------|--------|
| {at} | {KEY} | {issuetype} | {summary} | {reporter} |

本周期无新建任务时写：「本周期无新建任务。」

---

## 按项目分布

| 项目 | 状态变更 | 工时条数 | 工时合计 | 新增 | 涉及 ticket |
|------|----------|----------|----------|------|-------------|
| {PROJECT} | {n} | {w} | {wt} | {m} | {u} |

---

## 工作要点

{仅描述：状态流转成果、工时投入重点、新建任务；不写 description 维护}

---

## 数据说明

- 候选池 JQL：`{candidate_jql}`
- 工时来源：changelog `timespent` 增量（非 timeestimate）
- 未计入：description / Link / IssueParentAssociation / …
- 生成时间：{generated_at}
```

## 简要版

```markdown
# 进展摘要 · {start} – {end}

**完成 {completed_count}**：{KEY1} {from}→{to}；…

**推进 {started_count}**：{KEY2} {from}→{to}；…

**工时 {worklog_total_human}**（{worklog_count} 条）：{KEY3} +4h；…

**新建 {created_count}**：{KEY4} {summary}；…
```

## 填写规则

1. 状态变更必须 **from → to**；工时必须 **+{delta_human}**。
2. **完成数** = `completed` 事件数；**工时合计** = 各 `delta_seconds` 之和。
3. 不写 description、timeestimate 单独变动。
4. 空章节保留并写「本周期无此项」。
