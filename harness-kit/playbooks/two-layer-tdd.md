# two-layer-tdd — 两层 TDD 分工（实现侧单测 + 验收侧 E2E）

## 适用场景

用 harness-kit 做需求开发、纠结"既然有 Evaluator 的 RED-first，实现者还要不要写测试"时；
以及实现/验收两个角色如何各管一层测试而不破坏角色信息隔离。

## 做法

1. **验收侧（Evaluator，已有）**：E2E 用例 RED-first + 四级 Rubric + 断言锁冻结冒烟集。
   这层解决"整条链路对不对"，防谎报靠机械执法。
2. **实现侧（Implementer，dev agent 自律）**：可单测的逻辑改动（工具函数、状态机、
   数据转换）先写单测跑一次确认 RED（失败断言记入任务 history.md 作跑红证据），
   再实现变绿；bugfix 先写能复现 bug 的失败测试。纯文案/样式不强制。
3. 实现者写的是**自己的单测**，依然看不到 Rubric——不违反角色隔离；他不能改的是
   冒烟集（断言锁管着），自己新写的单测随实现一起演进。
4. 配套 spec 分工：实现者持 `tasks/<需求名>/spec.md`（方案与边界），
   Evaluator 持 `rubric.md`（验收标准），两侧独立写、事后对照——不一致即澄清信号。

## 反例（不要这样做）

- 因为"有 E2E 验收了"就不写单测：纯逻辑模块用 E2E 验收太重，反馈环慢，质量护栏空转。
- 实现者为通过验收去改 E2E 冒烟用例：断言锁会拦（exit 2），该判 ESCALATED。
- spec 只写一份、实现和验收共用：违反信息隔离，Evaluator 会被实现思路带偏。

## 依据

- 来源任务：`tasks/*`（本 kit 建设过程，2026-08 讨论；迁移前位于 workspaces/*/tasks/）
- 原理出处：kit 调研笔记《Coding 与 Testing Harness 自建方案》、
  `.harness/rubric/anti-false-reporting.md`（角色隔离 / RED-first）
- 验证时间：2026-08-25
