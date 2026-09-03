# visable-plugin-marketplace 仓库经验笔记

> 该仓库的栈、命令实测、坑与约定。任务级过程写 tasks/<需求名>/history.md，
> 跨仓库通用的经验提练到 kit 的 playbooks/<主题>.md。

## 栈与命令实测
- 纯文档/JSON 仓库（无 package.json）：lint/typecheck/build/test 无从配置，`harness validate` 自动跳过，arch/lock 门禁有效
- 纯 Markdown 改动无单测可跑，验证手段 = 文本一致性 diff + 子代理行为盲评（见 tasks/FE-1042-ssr-unsafe-api-detection/evidence/）

## 坑与约定
- 规则是**双层结构**：源 `plugins/<plugin>/rules/*.mdc`（带 frontmatter）+ cr-frontend 读取的生成副本 `plugins/<plugin>/skills/cr-frontend/references/rules/*.md`（带 AUTO-GENERATED 头）。**改规则必须两处同步**，仓库没有 sync-rules.sh（md 头部引用的脚本不存在，路径也是重构前的 `plugins/rules/`；FE-1042 已顺手修正 2 个规则对的头部，performance/react 两个 md 头部仍是旧路径）
- 插件版本升级是独立 chore 提交（见 #7），feat 提交不捆绑版本号（#11 未升版本）
- 插件间结构：vcn-be-ai / visable-be-ai / visable-fe-ai，cr-frontend 技能在 visable-fe-ai 下
