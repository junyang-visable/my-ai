---
description: 以 Evaluator 角色对 <需求名> 做 E2E 验收（RED-first + 四级 Rubric + 断言锁）
---

以 **Testing Harness Evaluator** 角色验收需求：$ARGUMENTS

严格按顺序，且不要读实现的技术方案（角色信息隔离）：

先定位模式：当前仓库根有 `.harness/config.sh`（install 模式）→ 下述路径相对仓库根；
否则在工具集仓库（my-ai）会话（workspace 模式）→ 先 `bash harness-kit/harness current`
确认活跃仓库，路径换成：E2E 上下文 `harness-kit/workspaces/<alias>/context/e2e-context.md`，
Rubric 落点 `harness-kit/workspaces/<alias>/tasks/$ARGUMENTS/rubric.md`，
断言锁/证据收集用 `bash harness-kit/harness lock|evidence ...`。

1. 读 E2E 用例上下文拿真实入口/选择器/账号。
2. 从 `.harness/rubric/rubric-template.md` 生成 `.harness/tasks/$ARGUMENTS/rubric.md`（四级检查项）。
3. RED-first：关键用例先跑红一次，确认能失败。
4. 跑断言锁 verify（install 模式：`python3 .harness/feedback/lock-tests.py verify`；
   workspace 模式：`bash harness-kit/harness lock verify`）；非 0 直接判 ESCALATED。
5. 执行 E2E（HARNESS_E2E_CMD）；失败则收证据（install 模式：
   `bash .harness/feedback/collect-evidence.sh`；workspace 模式：`bash harness-kit/harness evidence`）。
6. 判定：加权总分≥阈值 且 Essential 全过 且 触发准确率 100% 才 PASS，否则回喂修复或 ESCALATED。

给实现会话的 prompt 必须包含："测试当前不应通过，禁止修改测试使其通过。"
