# playbooks/ — 跨仓库通用经验库

> 与 `workspaces/<alias>/notes.md`（仓库专属）的分工：**只有换个仓库仍然成立的结论才放这里**。
> 某个仓库的命令、选择器、环境坑 → notes.md；可迁移的方法论（套路、反模式、决策依据）→ 本目录。

## 组织方式

- **一主题一文件**，文件名即主题：`<主题>.md`（如 `red-first.md`、`cypress-selector-strategy.md`）。
- 从 `_template.md` 复制起稿；写完在文末「依据」里链接来源任务（`tasks/<需求名>/`），
  让每条经验都能回溯到真实案例。
- 经验来自 skill 收尾回写（harness-coding / harness-dev 收尾步骤）或人工复盘；
  防谎报类基础经验另见 `.harness/rubric/anti-false-reporting.md`，不在此重复。

## 命名建议

- 动作类：`<怎么做某事>.md`（如 `collect-evidence-priority.md`）
- 反模式类：`avoid-<什么>.md`（如 `avoid-editing-tests-to-green.md`）

## 保鲜

- 季度 review 一次：失效的删掉，互相重复的合并。宁可少而准，不要多而水。
