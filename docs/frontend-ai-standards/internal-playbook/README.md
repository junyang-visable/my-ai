# 内部 Playbook · 前端 AI 协作指南

欢迎来到团队的前端 AI 协作内部 Playbook。这是一份**面向内部研发团队**的实操手册：无论你是刚加入的新人，还是已经熟悉业务的老同事，都可以在这里找到统一的流程、模板与审查标准，让 AI 辅助开发更稳、更快、更可复盘。

**这份 Playbook 解决什么问题？**

- 让 Cursor、RepoWiki、OpenSpecs（SDD）和 Prompt 模板在同一套叙事里串起来，而不是零散文档。
- 把「写代码」扩展为「需求 → 规格 → 上下文 → 编码 → 审查 → 合并 → 知识回写」的完整闭环。

---

## 推荐开发流程

按下面顺序走一遍，就是一次标准的前端 AI 协作迭代。**核心原则：更新完 Specs 和 RepoWiki 才算是一次完整的代码改动**——代码合并只是中间节点，知识资产也要跟上。

```
需求确认
   ↓
生成 / 更新 Specs（OpenSpecs）→ 参见 03-sdd/
   ↓
配置项目上下文（RepoWiki + .cursorrules）→ 参见 01-cursor-rules/ 和 02-repowiki/
   ↓
使用 Prompt 模板进行 AI 编码 → 参见 04-prompt-templates/
   ↓
按 Review Checklist 审查代码 → 参见 05-review-checklist/
   ↓
合并代码
   ↓
同步更新 Specs + RepoWiki   ← 完整的一次改动
```

建议把「合并后同步 Specs + RepoWiki」当作 Definition of Done 的一部分，避免文档与实现长期漂移。

---

## 模块导航

| 模块 | 说明 | 适用时机 |
|------|------|----------|
| [01 Cursor 配置规范](./01-cursor-rules/README.md) | `.cursorrules` 模板、MCP 配置指引 | 项目初始化或新人加入时 |
| [02 RepoWiki 规范](./02-repowiki/README.md) | 项目知识库模板（7 类文档） | 项目初始化；后续持续维护 |
| [03 SDD 规范](./03-sdd/README.md) | OpenSpecs 使用指南 | 每次开发新功能或较大改动前 |
| [04 Prompt 模板库](./04-prompt-templates/README.md) | 6 类场景的 Prompt 模板 | 日常 AI 编码时 |
| [05 Review Checklist](./05-review-checklist/README.md) | AI 生成代码的审查标准 | PR Review 时 |

---

## 新人快速入门

1. **Day 1** — 阅读 [01 Cursor 配置规范](./01-cursor-rules/README.md)，在本地按指引配置 Cursor（含 `.cursorrules` 与可选 MCP），确保 AI 在统一约束下工作。
2. **Day 2** — 阅读当前业务仓库中的 `repowiki/`，建立对项目结构、规范与业务语料的体感；若项目尚未建库，可参考 [02 RepoWiki 规范](./02-repowiki/README.md) 从模板起步。
3. **Day 3 及以后** — 新功能前先走 [03 SDD 规范](./03-sdd/README.md) 补齐或更新 Specs，日常编码优先使用 [04 Prompt 模板库](./04-prompt-templates/README.md)，提交前用 [05 Review Checklist](./05-review-checklist/README.md) 自检或互评。

---

## 老人对齐 Checklist

已有成员可用下面几项快速对齐团队约定（勾选即表示当前仓库/流程已满足）：

- [ ] 项目根目录有 `.cursorrules`？
- [ ] 项目有 `repowiki/`？
- [ ] 开发前先生成 / 更新 Specs？
- [ ] PR 时有 Review Checklist（或等价审查清单）？

全部对齐后，新人 onboarding 与跨项目协作会轻松很多；若有缺口，优先补 [01](./01-cursor-rules/README.md) 与 [02](./02-repowiki/README.md)，再收紧 [03](./03-sdd/README.md) 与 [05](./05-review-checklist/README.md)。

---

**一句话**：先定规格与上下文，再用模板编码、用清单审查，合并后把 Specs 和 RepoWiki 一并更新——这就是内部 Playbook 期望的一次完整改动。需要深入某一模块时，直接从上方导航表进入对应目录即可。
