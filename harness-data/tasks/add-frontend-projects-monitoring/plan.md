# plan — 可验证任务分解

> 从 spec.md 派生：spec=做什么与边界（confirmed 后冻结），plan=怎么做（执行中可调整，
> 调整不必重新确认）。每步必须带验证命令与预期输出——**跑不出预期 = 没做完**。
> 勾选即进度，换会话可续跑（superpowers writing-plans 的个人版）。

- 需求名：
- 依据 spec：spec.md（状态应为 confirmed）

## Task 1：<标题，一次提交粒度>

- [ ] Step 1：<动作>
  - 验证：`<命令>`
  - 预期：`<具体输出 / 退出码，如 "OK" / exit 0 / 包含某行>`

- [ ] Step 2：<动作>
  - 验证：`<命令>`
  - 预期：`<...>`

## Task 2：<标题>

- ...

## 完成定义

- [ ] 全部 Task/Step 勾选，验证均达预期
- [ ] `bash <kit>/harness validate` 全绿（跨文件改动加 --strict）
