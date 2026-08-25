---
description: 跑 harness 统一验证入口（lint→typecheck→arch→build→test，三级门禁）
---

跑 harness 统一验证入口（lint→typecheck→arch→build→test，三级门禁），并把结果汇报给我。

先定位模式：
- 当前仓库根有 `.harness/config.sh`（install 模式）→ 执行 `bash .harness/feedback/validate.sh`
- 否则在工具集仓库（my-ai）会话里（workspace 模式）→ 先 `bash harness-kit/harness current`
  确认活跃仓库，再执行 `bash harness-kit/harness validate`

步骤：
1. 执行上述命令（若本次改动跨 3 个以上文件，加 `--strict`）。
2. 如有阻断级失败，把失败 stage、file:line、原因、修复建议原样列出，并据此提出下一步修复。
3. 不要通过删断言、改测试预期、加 @ts-ignore、新建测试文件来让它变绿。
4. 全绿后，提醒我按 `.harness/rubric/evidence-template.md` 补完成证据。

$ARGUMENTS
