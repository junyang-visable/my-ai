# plan — 可验证任务分解

- 需求名：FE-1042 — cr-frontend SSR-unsafe client API detection
- 依据 spec：spec.md（confirmed 2026-08-28）

## Task 1：frontend-standards 规则新增 SSR Safety

- [x] Step 1：编辑 `plugins/visable-fe-ai/rules/frontend-standards.mdc`——在 `## Severity Reference` 之前插入 `## SSR Safety` 节（3 条：未防护访问 Must Fix / 守卫白名单不报 / 发现项必须附修复指引），并在 Severity Reference 的 Must Fix 场景里追加 SSR 一句
  - 验证：`grep -c "SSR Safety" plugins/visable-fe-ai/rules/frontend-standards.mdc`
  - 预期：`1`
- [x] Step 2：同步生成副本 `plugins/visable-fe-ai/skills/cr-frontend/references/rules/frontend-standards.md`（同内容 + AUTO-GENERATED 头，头部路径修正为 `plugins/visable-fe-ai/rules/`，去掉 sync-rules.sh 引用）
  - 验证：`diff <(tail -n +4 plugins/visable-fe-ai/rules/frontend-standards.mdc) <(tail -n +3 plugins/visable-fe-ai/skills/cr-frontend/references/rules/frontend-standards.md)`
  - 预期：无输出（正文逐行一致；mdc 头 3 行 frontmatter、md 头 2 行注释被跳过）

## Task 2：vue3 规则新增 SSR Safety

- [x] Step 1：编辑 `plugins/visable-fe-ai/rules/vue3.mdc`——在 `## Lifecycle` 节之后追加 `## SSR Safety` 节（5 条：检测范围+Must Fix / 服务端客户端执行语义 / 守卫白名单 / 可选链≠守卫 / 修复指引）
  - 验证：`grep -c "SSR Safety" plugins/visable-fe-ai/rules/vue3.mdc`
  - 预期：`1`
- [x] Step 2：同步生成副本 `plugins/visable-fe-ai/skills/cr-frontend/references/rules/vue3.md`（同上，含头部路径修正）
  - 验证：`diff <(tail -n +6 plugins/visable-fe-ai/rules/vue3.mdc) <(tail -n +3 plugins/visable-fe-ai/skills/cr-frontend/references/rules/vue3.md)`
  - 预期：无输出（mdc frontmatter 为 5 行）

## Task 3：行为评测 + 护栏

- [x] Step 1：子代理行为评测（AC1/AC2）——只给更新后的 4 个规则文件 + 6 个样例代码片段（1 个未防护 composable、1 个未防护 setup 顶层、1 个 `window?.` 伪防护、4 个守卫写法），要求按规则输出 Must Fix/不报判定
  - 验证：评测结果对照预期矩阵
  - 预期：2 个未防护 + 1 个伪防护 = Must Fix；4 个守卫样例 = 不报
- [x] Step 2：`bash <kit>/harness validate --strict`
  - 预期：全绿 exit 0

## Task 4：收尾

- [x] Step 1：更新 current.md（阶段→完成）、history.md 追加一行、`workspaces/visable-plugin-marketplace/notes.md` 记录仓库坑（mdc/md 双层结构、无 sync 脚本、版本 bump 惯例）
  - 验证：文件存在且含新条目
  - 预期：grep 命中
- [x] Step 2：按 evidence-template 申报完成证据，提醒用户另开会话用 harness-testing 验收

## 完成定义

- [x] 全部 Task/Step 勾选，验证均达预期
- [x] `bash <kit>/harness validate --strict` 全绿
