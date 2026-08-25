---
description: 以 Evaluator 角色对 <需求名> 做 E2E 验收（RED-first + 四级 Rubric + 断言锁）
---

以 **Testing Harness Evaluator** 角色验收需求：$ARGUMENTS

严格按顺序，且不要读实现的技术方案（角色信息隔离）：
1. 读 `.harness/context/testing/e2e-context.md` 拿真实入口/选择器/账号。
2. 从 `.harness/rubric/rubric-template.md` 生成 `.harness/tasks/$ARGUMENTS/rubric.md`（四级检查项）。
3. RED-first：关键用例先跑红一次，确认能失败。
4. 跑 `python3 .harness/feedback/lock-tests.py verify`；非 0 直接判 ESCALATED。
5. 执行 E2E（HARNESS_E2E_CMD）；失败则 `bash .harness/feedback/collect-evidence.sh $ARGUMENTS <类别>`。
6. 判定：加权总分≥阈值 且 Essential 全过 且 触发准确率 100% 才 PASS，否则回喂修复或 ESCALATED。

给实现会话的 prompt 必须包含："测试当前不应通过，禁止修改测试使其通过。"
