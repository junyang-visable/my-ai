# SDD 规范（前端版）

SDD（Spec-Driven Development，规范驱动开发）是本团队 AI 协作的核心工作方式。其运转依赖**四个支柱**的协同：

| 支柱 | 角色 | 核心职责 |
|------|------|----------|
| **OpenSpec** | 定方向 | 在动代码前，将需求落成可评审、可版本化的结构化 Spec（功能范围 / 数据模型 / 交互细节 / 技术约束）；**只负责 Spec 产出，不负责执行** |
| **Superpower** | 带节奏 | 接管 OpenSpec apply 之后的全部实施节奏：`brainstorming` 探方案 → `writing-plans` 写计划 → `subagent-driven-development` / `executing-plans` 执行 → `verification-before-completion` 验收 |
| **RepoWiki** | 提供知识库 | 生成 Spec 与制订计划时，AI 先读 `repowiki/` 获取路由、技术规范、业务约束，避免脱离仓库真实情况的臆测 |
| **.cursorrules** | 纪律约束 | `.cursorrules` 中声明的规则在整个编码过程中持续生效，是不依赖人工 Review 也能执行的硬约束 |

---

## 典型迭代节奏

```
需求到达
    ↓
【OpenSpec 定方向】
  ① 先读 repowiki/ — 核实路由路径、Store 名称、API 约定，避免 Spec 脱节
  ② 产出结构化 Spec（功能范围 / 数据模型 / 交互 / 技术约束）
  ③ 人工评审，确认 Spec
    ↓（Spec 确认后，OpenSpec 完成使命；apply 命令不使用，交棒 Superpower）

【Superpower 带节奏】
  brainstorming（可选，方案不明时）：
    ① 先读 repowiki/ — 了解现有组件、composable、状态管理，作为方案选型依据
    ② 提 2–3 种实现方案与取舍，产出设计文档，再触发 writing-plans
         ↓
  writing-plans：
    ① 先读 repowiki/ 技术规范与路由章节 — 确认文件路径与命名约定
    ② 结合 .cursorrules 约束，生成含准确文件清单与逐步操作的实施计划
       （存至 docs/superpowers/plans/）
         ↓
  subagent-driven-development（推荐）或 executing-plans：
    按计划逐步执行；repowiki/ 作为参考文档随时可查
         ↓
  verification-before-completion → finishing-a-development-branch：
    验收通过后提 PR 或合并
    ↓

【合并后：RepoWiki 同步闭环】
  将新路由、新 Store、新业务规则同步回 repowiki/ 对应章节
  同步更新 specs/（global-specs 或功能级 Spec）
  → 下次迭代时 repowiki/ 仍是准确的知识来源
```

> **关键区分**：OpenSpec 的 `apply` 命令**不在本团队流程中使用**；Spec 确认后直接进入 Superpower 节奏，由 Superpower 技能链驱动实施。

---

## 四支柱分工说明

### OpenSpec — 定方向

统一采用 **[OpenSpec](https://github.com/Fission-AI/OpenSpec)** 产出结构化 Spec。Spec 分三个粒度：

| Spec 类型 | 粒度 | 建议存放 |
|-----------|------|----------|
| **全局 Specs** | 整个仓库页面与功能地图 | `specs/global-specs.md` |
| **页面级 Specs** | 单个页面的入口、布局、路由、权限 | `specs/pages/<route>.md` |
| **功能级 Specs** | 单个功能点的用户故事、验收场景、接口契约 | `openspec/changes/<feature>/` 或 `specs/features/<name>.md` |

Spec 产出后由人工评审，确认后**不再使用 OpenSpec 命令执行**，交由 Superpower 接管。

> OpenSpec 安装与详细 Prompt 模板见 **[openspecs-frontend-guide.md](./openspecs-frontend-guide.md)**。

### Superpower — 带节奏

Spec 确认后，由以下技能链驱动全部实施过程：

| 技能 | 触发时机 | 作用 |
|------|----------|------|
| `brainstorming` | 实现方案不明确时（可选） | 协作探方案、提 2–3 种实现方式及取舍，产出设计文档，再触发 `writing-plans` |
| `writing-plans` | Spec 确认后（或 brainstorming 完成后） | 基于 Spec + repowiki/ 生成含文件清单与逐步操作的实施计划（存至 `docs/superpowers/plans/`） |
| `subagent-driven-development` | 计划评审通过后（推荐） | 每个任务派发独立子 Agent 执行，两阶段 Review，高速迭代 |
| `executing-plans` | 计划评审通过后（无子 Agent 时） | 在当前会话中逐任务执行，含 Checkpoint |
| `verification-before-completion` | 所有任务完成后 | 运行验证命令，确认无遗漏，再宣布完成或提 PR |
| `finishing-a-development-branch` | 验收通过后 | 验证测试、整理分支、提 PR 或合并 |

> 其他辅助技能：`dispatching-parallel-agents`（多个独立子任务并行）、`requesting-code-review`（提 PR 前 Review）、`receiving-code-review`（处理 Review 意见）。

### RepoWiki — 提供知识库

RepoWiki 在流程中有三个具体介入点：

| 阶段 | 读什么 | 用来干什么 |
|------|--------|-----------|
| **OpenSpec Spec 生成前** | `repowiki/INDEX.md` → 路由、技术规范、业务章节 | 核实页面路径、Store 名称、接口约定，保证 Spec 与代码一致 |
| **Superpower writing-plans 前** | `repowiki/` 技术规范、路由与页面结构章节 | 生成准确的文件路径与 import，避免计划中出现臆造模块 |
| **合并后（闭环）** | 写入 `repowiki/` 路由、状态、业务章节 | 将本次新增的路由、Store、业务规则更新回 Wiki，保证下次迭代仍有准确上下文 |

- RepoWiki 结构与模板见 **[02-repowiki/README.md](../02-repowiki/README.md)**。

### .cursorrules — 纪律约束

- `.cursorrules` 中的规则在所有 AI 对话中**持续生效**，无需每次 Prompt 重申。
- 典型约束：使用规定的组件库、禁止直接操作 DOM、命名约定、Store 写法等。
- Cursorrules 模板见 **[01-cursor-rules/](../01-cursor-rules/README.md)**。

---

## 下一步

- **OpenSpec 安装与 Prompt 模板**：[openspecs-frontend-guide.md](./openspecs-frontend-guide.md)
- **RepoWiki 填写规范**：[02-repowiki/README.md](../02-repowiki/README.md)
- **Cursorrules 模板**：[01-cursor-rules/README.md](../01-cursor-rules/README.md)
