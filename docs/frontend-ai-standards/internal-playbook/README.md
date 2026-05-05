# 前端 AI 协作规范 · 内部 Playbook

> 本页即宣讲主线。按章节向下阅读可完整传达框架；子目录为各模块的操作细则与可复制模板。

---

## 一、为什么需要这套规范

AI 编码工具已在各项目中独立使用，但团队普遍遇到三类问题：

| 痛点 | 典型表现 |
|------|----------|
| **理解偏差** | AI 与开发者各自脑补需求，实现与产品预期不一致，反复返工 |
| **上下文丢失** | 换人接手或会话过长，AI 不了解项目约束，生成与仓库风格格格不入的代码 |
| **节奏失控** | 跳过规格直接让 AI 写代码，边界不清、场景遗漏、合并后文档马上过期 |

本 Playbook 的目标：**让 AI 在每个项目中都有一致的约束边界、准确的上下文、可追溯的开发节奏**。

---

## 二、核心框架：四支柱模型

每次功能迭代由四个支柱协同驱动，缺任何一个都会走样：

```
┌──────────────────────────────────────────────────────┐
│                   一次功能迭代                        │
│                                                      │
│  OpenSpec          Superpower        RepoWiki        │
│  ─────────         ──────────        ─────────       │
│  定方向            带节奏             提供知识库       │
│  产出结构化        brainstorming      生成 Spec 前     │
│  Spec 文档         → writing-plans   先读 repowiki/  │
│  (评审通过后       → subagent /      制订计划前        │
│  才动代码)         executing-plans   再读 repowiki/   │
│                   → verification    合并后回写        │
│                                                      │
│               .cursorrules                           │
│               ────────────                           │
│               纪律约束（每次对话自动生效）              │
└──────────────────────────────────────────────────────┘
```

| 支柱 | 角色 | 一句话说明 |
|------|------|-----------|
| **OpenSpec** | 定方向 | 实现前产出结构化 Spec，Spec 评审通过后才动代码 |
| **Superpower** | 带节奏 | 接管实施全程：探方案 → 写计划 → 执行 → 验收 |
| **RepoWiki** | 提供知识库 | AI 在三个关键节点读取项目知识，避免臆测 |
| **.cursorrules** | 纪律约束 | 命名、禁用 API、流程纪律在每次对话中自动生效 |

---

## 三、标准迭代节奏

```
需求到达
    ↓
【OpenSpec 定方向】
  ① 先读 repowiki/ — 核实路由、Store、接口约定
  ② 产出 Spec（功能范围 / 数据模型 / 交互 / 技术约束）
  ③ 人工评审，确认 Spec
    ↓（Spec 确认后交棒 Superpower，不使用 OpenSpec apply）

【Superpower 带节奏】
  brainstorming（方案不明时）：
    先读 repowiki/ 了解现有模块 → 提 2–3 种方案 → 产出设计文档
  writing-plans：
    先读 repowiki/ 技术规范与路由 → 生成含文件清单的分步计划
  subagent-driven-development / executing-plans：
    按计划逐步执行（.cursorrules 全程约束）
  verification-before-completion → finishing-a-development-branch：
    验收通过后提 PR
    ↓

【合并后：闭环必做】
  将新路由、新 Store、新业务规则 → 同步回 repowiki/
  同步更新 specs/
  → 下次迭代仍有准确上下文
```

**Definition of Done**：代码合并 ≠ 完整交付；**Specs 与 RepoWiki 同步更新后**才算一次完整改动。

---

## 四、五个模块说明

| 模块 | 谁来建 | 作用 | 入口 |
|------|--------|------|------|
| **01 Cursor 配置（.cursorrules）** | 项目 Owner | 设定编码纪律与 SDD 流程约束，每次 AI 对话自动生效 | [01-cursor-rules/](./01-cursor-rules/README.md) |
| **02 RepoWiki** | 项目 Owner 主导，全员维护 | 沉淀路由、技术规范、业务知识，供 AI 与新人检索 | [02-repowiki/](./02-repowiki/README.md) |
| **03 SDD（OpenSpec + Superpower）** | 全员 | 四支柱协同框架：Spec 先行 + Superpower 带节奏 | [03-sdd/](./03-sdd/README.md) |
| **04 Prompt 模板库** | 全员参考 | 组件、页面重构、排障等场景的结构化 Prompt | [04-prompt-templates/](./04-prompt-templates/README.md) |
| **05 Review Checklist** | 全员 | PR 合并前的结构化自检清单，🔴 项未闭环不建议合并 | [05-review-checklist/](./05-review-checklist/README.md) |

**落地优先级**：先夯实 **01 + 02**（工具与知识库就绪）→ 再推 **03**（SDD 节奏）→ **05** 门禁收紧 → **04** 随能力建设并行推广。

---

## 五、各角色入口

### 项目 Owner

1. 用 `init-ai-standards` skill 一键初始化 `.cursorrules` + `repowiki/` + `specs/`（见 `.cursor/skills/init-ai-standards/`）
2. 评审并完善 `repowiki/` 中业务知识与路由章节（04、06 章节需人工填写）
3. 将「合并后同步 Specs + RepoWiki」写入团队 Definition of Done

### 开发人员

1. 接到新需求 → 先确认 Spec 是否存在（`specs/` 或 `openspec/changes/`）
2. 有 Spec → Superpower `writing-plans` 写计划 → 执行 → 验收
3. 无 Spec → 先走 OpenSpec 生成 Spec，评审通过后再开始
4. 合并后 → 同步 `repowiki/` 与 `specs/`

---

## 六、新成员 Onboarding

| 阶段 | 操作 |
|------|------|
| **第 1 日** | 拷贝项目 `.cursorrules`，确认 SDD 流程纪律章节已就位 |
| **第 2 日** | 读当前仓库 `repowiki/INDEX.md`，顺序浏览各章节了解项目约束 |
| **第 3 日起** | 新功能走 [03-sdd/](./03-sdd/README.md) 节奏；提交前对照 [05-review-checklist/](./05-review-checklist/README.md) 自检 |

---

## 七、仓库基线检查

新建或存量项目对齐时，逐项确认：

- [ ] 根目录有 `.cursorrules`，含 `SDD 流程纪律` 章节
- [ ] 存在 `repowiki/`，INDEX 可导航到全部 7 章
- [ ] 重大改动前有可评审的 Spec（`specs/` 或 `openspec/changes/`）
- [ ] 团队 Definition of Done 中已包含「合并后同步 Specs + RepoWiki」

---

## 附录：模块索引

| 模块 | 核心内容 |
|------|----------|
| [01 Cursor 配置规范](./01-cursor-rules/README.md) | `.cursorrules` 模板（含 SDD 流程纪律与 Superpower 约束） |
| [02 RepoWiki 规范](./02-repowiki/README.md) | 三条写作原则、`templates/` 下 01–07 模板与 INDEX |
| [03 SDD 规范](./03-sdd/README.md) | 四支柱模型详解；Spec Prompt 模板见 [openspecs-frontend-guide.md](./03-sdd/openspecs-frontend-guide.md) |
| [04 Prompt 模板库](./04-prompt-templates/README.md) | 组件、页面重构、API、样式、单元测试、排障等场景模板 |
| [05 Review Checklist](./05-review-checklist/README.md) | `frontend-review-checklist.md`；合并前结构化自检 |
