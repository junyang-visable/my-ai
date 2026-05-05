# 内部 Playbook · 前端 AI 协作指南

本 Playbook 为内部研发团队提供统一的前端 AI 协作基准。共享本页并按章节向下浏览，即可作为主要讲解路径；如需模板与细则，再进入下方各子文档。

适用范围：在多前端项目中落实一致的工程实践——涵盖 **Cursor 配置、RepoWiki（项目知识库）、OpenSpecs / SDD、Prompt 使用方式，以及评审与交付定义**，避免工具链与文档体系碎片化。

---

## 范围与原则

- **一致性范围**：不仅对齐代码风格，而将 **工具边界、上下文资产（RepoWiki）、规格资产（Specs）、Prompt 规范与评审门禁** 纳入同一套协作框架。
- **变更闭环与交付定义（Definition of Done）**：代码合并至主分支仅表示实现阶段结束；同一变更还须 **同步更新 Specs 与 RepoWiki**，使规格与知识与实现保持一致，便于审计与后续迭代。未满足文档同步的变更视为交付不完整。
- **职责分工**：技术负责人 / 项目负责人优先落实模块 **01（工具）、02（上下文）** 的初始化与运维；开发人员按 **03（规格）→ 04（日常编码）→ 05（评审）** 执行；全体将「合并后的规格与 RepoWiki 同步」纳入该变更的 Definition of Done。

---

## 文档结构（与子目录映射）

| 模块 | 作用 | 入口 |
|------|------|------|
| **工具层** | 约束 Cursor 在各仓库中的行为边界（允许 / 禁止 / 优先级） | [01 Cursor 配置规范](./01-cursor-rules/README.md) |
| **上下文** | 通过 RepoWiki 沉淀架构、约束与术语，可供检索并对齐人机理解，降低歧义成本 | [02 RepoWiki 规范](./02-repowiki/README.md) |
| **规格** | 在实现前产出可评审、可版本化的需求与行为说明（OpenSpecs / SDD） | [03 SDD 规范](./03-sdd/README.md) |
| **日常编码** | 采用结构化 Prompt（上下文 / 任务 / 约束 / 输出），稳定 AI 产出质量 | [04 Prompt 模板库](./04-prompt-templates/README.md) |
| **质量** | 合并前依据统一清单执行 PR Review 或自检 | [05 Review Checklist](./05-review-checklist/README.md) |

推荐执行顺序：**工具与维基就绪 → Spec 就位 → 按模板开发与自检 → Review 门禁**。各模块操作规程见对应目录。

---

## 协作流程（标准迭代）

以下为前端 AI 协作的**最小闭环**。原则：**Specs 与 RepoWiki 的更新与代码变更同属一次交付；** 仅以合并表征代码入库，不构成完整交付。

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

若团队在 Definition of Done 中明确列出「合并后同步 Specs 与 RepoWiki」，可降低文档与代码长期分叉的风险。

---

## 仓库自检（新建与存量对齐）

可作为各仓库基线检查的参考项：

- [ ] 根目录存在 `.cursorrules`（或等价 Cursor 规则），且与栈一致（模板见 [01](./01-cursor-rules/README.md)）
- [ ] 具备项目 Wiki（例如 `repowiki/`），章节与 INDEX 完整（规范见 [02](./02-repowiki/README.md)）
- [ ] 重大或结构性改动前产出可评审的 Spec（见 [03](./03-sdd/README.md)）
- [ ] 复杂任务在 Prompt 中引用 Wiki 节选，日常可参考 [04](./04-prompt-templates/README.md)
- [ ] PR 对照 [05](./05-review-checklist/README.md)，🔴 项未闭环前不建议合并

**落地优先级**：通常先夯实 **01、02**，再收紧 **03、05**；**04** 可与能力建设并行推广。

---

## 新成员 Onboarding（建议节奏）

| 阶段 | 内容 |
|------|------|
| 第 1 日 | 阅读 [01](./01-cursor-rules/README.md)，配置本地 Cursor（`.cursorrules`） |
| 第 2 日 | 阅读当前业务的 RepoWiki；若尚未建立，可参考 [02](./02-repowiki/README.md) 从模板初始化 |
| 第 3 日起 | 新功能前先遵循 [03](./03-sdd/README.md)；日常编码使用 [04](./04-prompt-templates/README.md)；提交前依据 [05](./05-review-checklist/README.md) 自检或 Peer Review |

---

## 附录：模块索引

需要复制模板或查阅清单时，从下列入口进入。

| 模块 | 内容摘要 |
|------|----------|
| [01 Cursor 配置规范](./01-cursor-rules/README.md) | `.cursorrules` 示例（如 `vue-nuxt-cursorrules.md`） |
| [02 RepoWiki 规范](./02-repowiki/README.md) | 撰写原则、`templates/` 下 01–07 模板与 INDEX |
| [03 SDD 规范](./03-sdd/README.md) | OpenSpec 与 Spec 粒度；操作流程见 [openspecs-frontend-guide.md](./03-sdd/openspecs-frontend-guide.md) |
| [04 Prompt 模板库](./04-prompt-templates/README.md) | 组件、页面重构、API、样式、单元测试、排障等场景模板 |
| [05 Review Checklist](./05-review-checklist/README.md) | `frontend-review-checklist.md`；可用于合并前的结构化自检 |

---

**结论**：在规格与上下文明确的前提下，以模板规范化 AI 编码、以清单门禁保障质量，并在合并后一并更新 **Specs** 与 **RepoWiki**，即本 Playbook 所定义的前端变更完整交付。
