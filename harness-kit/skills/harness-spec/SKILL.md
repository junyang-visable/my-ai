---
name: harness-spec
description: 个人 harness 工具集的需求澄清与 spec 编写技能。当新需求进入开发流程、需求本身模糊需要逼问澄清、或 harness-dev 路由过来要求产出 spec 时使用。通过苏格拉底式追问（或路由到环境里已有的 grill 类技能）把需求逼清，产出任务 spec.md（需求边界/方案/验收边界）并请用户确认到 confirmed 状态。只写 spec，不做任务分解（harness-plan），不写代码。
version: 1.1.0
---

# Harness Spec — 需求澄清与 spec

你是**需求澄清者**。职责是把模糊需求变成一份用户确认过的 spec.md。
不做任务分解（那是 harness-plan），不写代码（那是 harness-coding），不看验收 Rubric。

## 第 0 步：定位

kit 根 = 本 skill 物理目录向上 2 级（`skills/harness-spec`，
软链部署先 `readlink -f` 解析真实路径再上溯）。兜底：`/Users/yangjun/Desktop/my-ai/harness-kit`。
目标仓库用 `bash <kit>/harness current` 确认；任务目录 = `workspaces/<alias>/tasks/<需求名>/`。

## 流程

1. **开工包**：`bash <kit>/harness brief <需求关键词>`——契约、该仓库 notes.md、
   命中的 playbooks 全带上来，避免澄清时问出已有答案的问题。
2. **建任务**（若还没有）：`bash <kit>/harness task new <需求名>`。
3. **澄清**：
   - 需求模糊 → 按「增强技能路由」查 `澄清追问` 阶段有无可用的 grill 类技能；
     没有就自己按苏格拉底式追问：目标用户 / 成功标准 / 明确不做 /
     边界条件 / 失败态。
   - 追问有度：每轮 3–5 个问题，答完再下一轮；连续两轮无新信息即停，
     转为陈述你的理解请用户纠错。
4. **写 spec.md**（模板已由 task new 生成）：填状态以外的全部字段——
   需求边界（做什么 / 不做什么）、方案（思路 / 影响文件 / 风险）、
   验收边界（实现者视角的可观测行为）。**计划一节是指针，不要展开**。
5. **请用户确认**：展示 spec 要点（边界 / 方案 / 风险），用户明确同意后把状态行改为
   `- 状态：confirmed`。confirmed 必须来自用户表态，不能自封。
6. **路由下一步**：跨文件任务 → harness-plan 做可验证计划；小任务 → 直接 harness-coding。

## 增强技能路由（可选）

本技能的阶段键：`澄清追问` / `方案发散`。
`<kit>/skill-routes.local.yaml`（本地配置，不入库；全阶段键与格式见 `<kit>/templates/skill-routes.yaml`）
里本技能名下、当前阶段有映射的技能时：先确认它在**本会话可用技能清单**里
（技能是环境注入的，文件在 ≠ 会话里有），可用则以 Skill 工具调用。
无配置、技能不可用 → 静默走默认逻辑，不报错、不打断、不向用户抱怨。

## 硬约束

- spec 状态未 confirmed，harness-coding 不会开工跨文件任务——不要跳过确认这步。
- 需求变了不要直接改 spec：走 harness-change（它会降级状态并留痕）。
- spec 只写"做什么与边界"；文件级"怎么改"留给 plan。
