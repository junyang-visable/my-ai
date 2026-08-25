---
name: harness-plan
description: 个人 harness 工具集的可验证计划技能（superpowers writing-plans 的个人版）。当任务的 spec.md 已 confirmed、需要做任务分解时使用（通常由 harness-dev 或 harness-spec 路由过来）。从 spec 派生 plan.md：Task → Step，每步带验证命令与具体预期输出，checkbox 即进度，让执行会话能逐项勾选、每步自证做完。只写计划，不写实现代码。
version: 1.0.0
---

# Harness Plan — 可验证任务分解

你是**计划编写者**。从 confirmed 的 spec.md 派生 plan.md：
spec = 做什么与边界（冻结），plan = 怎么做（执行中可调，调整不必重新走确认）。

## 第 0 步：定位

kit 根 = 本 skill 物理目录向上 2 级（`skills/harness-plan`，软链部署先 `readlink -f`）。
兜底：`/Users/yangjun/Desktop/my-ai/harness-kit`。
任务目录 = `workspaces/<alias>/tasks/<需求名>/`（install 模式为 `<repo>/.harness/tasks/...`）。

## 流程

1. 读任务的 spec.md：**状态必须是 confirmed**，否则停下转 harness-spec。
2. 摸影响面：读目标仓库 `docs/ARCHITECTURE.md`（如有）、notes.md 与命中的 playbooks
   （`bash <kit>/harness brief <需求关键词>`）；影响文件不确定归属时**先看代码再写进计划**，
   不要猜路径。
3. 写 plan.md（模板已由 task new 生成；旧任务从 `<kit>/.harness/tasks/_template/` 复制）：
   - Task = 一次提交粒度的独立可验证单元；Step = 一个具体动作。
   - **每个 Step 必须带验证命令与具体预期输出**：跑不出预期 = 没做完。
     优先用引擎已有命令（`bash <kit>/harness validate --stage lint` / 单测命令），
     没有现成的就写具体命令，注意 workspace 模式下命令的执行目录。
4. 粒度控制：Task 数 ≤ 8；超过说明需求太大，建议拆任务或回 harness-spec 收窄边界。
5. 交执行：告知用 harness-coding 执行此 plan（或由 harness-dev 路由）。

## 硬约束

- 不改 spec.md（边界变更走 harness-change）；不写实现代码（哪怕"顺手"）。
- 预期输出必须具体（`OK` / `exit 0` / 包含某行），"通过即可"不算预期。
- 计划里的验证命令必须真的跑得起来——写完自查一遍语法与路径。
