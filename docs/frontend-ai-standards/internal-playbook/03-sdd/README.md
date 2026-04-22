# SDD 规范（前端版）

SDD（Spec-Driven Development，规范驱动开发）指在写代码之前，先把**可评审、可版本化**的需求与行为说明（Specs）写清楚，再让 AI 或人工按 Spec 实现与验收。本仓库前端栈为 **Vue 3 / Nuxt 3**，团队在 **Cursor** 中编码；Specs 与 [RepoWiki](../02-repowiki/README.md) 配合，可显著降低「猜需求」带来的浪费。

## 为什么团队需要 SDD

| 痛点 | 表现 | SDD 如何缓解 |
|------|------|----------------|
| **理解偏差** | 口头/聊天里的需求含糊，AI 与开发者各自脑补，实现与产品预期不一致 | 先把页面路径、交互、数据与接口约束写成 Spec，评审对齐后再动代码 |
| **返工成本** | 做完才发现漏场景、边界未约定，重构与联调反复 | Spec 中固定「功能范围、数据模型、交互、技术约束」，变更可 diff、可追踪 |
| **上下文丢失** | 会话过长或换人接手时，决策依据散落在聊天记录里 | Spec 与 RepoWiki 留在仓库里，PR 与后续迭代都能检索到「当时为什么这样定」 |

## 工具选型：OpenSpec

团队统一采用 **[OpenSpec](https://github.com/Fission-AI/OpenSpec)** 作为 SDD 的载体与 CLI：它提供 `openspec init`、变更目录结构、以及与多种 AI 工具配合的斜杠命令工作流，适合**存量项目（brownfield）**迭代与**新需求**并行。安装与三种典型用法见 **[OpenSpecs 前端实践指南](./openspecs-frontend-guide.md)**。

> **说明**：OpenSpec 要求 **Node.js 20.19.0 及以上**。全局安装包名为 `@fission-ai/openspec`，安装后终端命令为 `openspec`。详细步骤见指南第一节。

## Spec 类型一览

| Spec 类型 | 粒度 | 典型内容 | 建议存放 / 命名 |
|-----------|------|----------|-----------------|
| **全局 Specs** | 整个仓库 | 按页面或功能点罗列：路由/页面路径、功能说明、核心交互、涉及的 Store 与 API；可与 RepoWiki 索引对应 | 例如 `specs/global-specs.md`（或团队约定的 `specs/` 下总表） |
| **页面级 Specs** | 单个页面 | 该页的入口、布局、区块、路由参数、页面级状态、埋点、权限 | 例如 `specs/pages/<route-segment>.md` 或与页面同目录的 `SPEC.md`（团队二选一统一即可） |
| **功能级 Specs** | 单个功能点 | 用户故事、验收场景、边界与错误态、接口契约、与组件/Store 的映射 | 例如 `openspec/changes/<feature-name>/` 下由 OpenSpec 生成的 proposal / specs / tasks，或 `specs/features/<name>.md` |

全局 Specs 负责**地图与索引**；页面级与功能级负责**可执行的细节**。新需求优先落功能级（或 OpenSpec 变更目录），合并后把结论同步回全局 Specs 与 RepoWiki。

## 下一步

- **操作步骤、可复制 Prompt 模板、验收清单**：请阅读 **[openspecs-frontend-guide.md](./openspecs-frontend-guide.md)**。
- **项目背景与约束**：生成或更新 Spec 前，应结合 **[RepoWiki](../02-repowiki/README.md)** 与模板章节（路由、状态、业务等）核对，避免 Spec 与仓库真实情况脱节。
