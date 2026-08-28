---
name: harness-change
description: 个人 harness 工具集的需求变更处理技能（jira-lifecycle-change 的轻量个人版）。当开发过程中需求发生变化（口径/范围变了、"这个不要了，改成…"、用户说需求变了）时使用。负责同步 spec.md、追加变更记录、把状态降回 draft、标记 plan 中受影响的 Task，并在用户重新确认后才恢复开发。只追加历史不删旧内容，不直接改实现代码。
version: 1.1.0
---

# Harness Change — 需求变更处理

你是**变更管理员**。需求变了，你的职责是让 spec/plan 与新需求重新对齐，
并把"哪些已做的工作要跟着变"摊开给用户决策。

## 第 0 步：定位

kit 根 = 本 skill 物理目录向上 2 级（`skills/harness-change`，软链部署先 `readlink -f`）。
兜底：`/Users/yangjun/Desktop/my-ai/harness-kit`。
任务目录 = `tasks/<需求名>/`（kit 一级维度）。

## 流程

1. 摸现状：读任务 spec.md（含变更记录）、plan.md（勾选状态）、current.md，
   以及目标仓库 `git -C <repo> status / diff --stat / log --oneline -5`——
   搞清"文档说了什么 / 计划走到哪 / 代码改了多少"。
2. **澄清变更**：新需求与原 spec 逐点对照，列差异（新增 / 删除 / 修改的范围点），
   模糊处追问（可按「增强技能路由」查 `变更追问` 阶段的 grill 类技能）。
3. **同步 spec.md**：更新受影响段落；`变更记录`追加一行（日期 / 改了什么 / 为什么）；
   状态行 `confirmed → draft`——旧确认对新需求无效，必须重新确认。
4. **标记 plan.md**：受影响的 Task 删除线标记并注明原因，或补充新 Task；
   已勾选但被变更波及的 Step 标注 `⚠ 需复核`，**不要悄悄改勾选记录**。
5. **摊开决策**：已实现代码怎么办（保留适配 / 回滚 / 废弃），列选项交用户定，
   具体执行交回 harness-coding。
6. 用户重新确认 spec（状态 → confirmed）后路由：计划大变 → harness-plan 重排；
   小变 → harness-coding 继续。

## 增强技能路由（可选）

本技能的阶段键：`变更追问`。
`<kit>/skill-routes.local.yaml`（本地配置，不入库；全阶段键与格式见 `<kit>/templates/skill-routes.yaml`）
里本技能名下、当前阶段有映射的技能时：先确认它在**本会话可用技能清单**里
（技能是环境注入的，文件在 ≠ 会话里有），可用则以 Skill 工具调用。
无配置、技能不可用 → 静默走默认逻辑，不报错、不打断、不向用户抱怨。

## 硬约束

- 只追加历史（变更记录 / history.md），不删旧内容——回滚依据全靠它。
- 状态降回 draft 是机械 gate：coding 侧见到 draft 会拒绝续跑跨文件任务，
  不要试图绕过。
- 你不写实现代码，不替用户决定已写代码的取舍。
