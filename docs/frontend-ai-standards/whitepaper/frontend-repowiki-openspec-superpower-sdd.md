# 前端 RepoWiki × OpenSpec × Superpower：SDD 实践说明

> Visable 前端 AI 工程 — 与 [知识库与 SDD 总览](./knowledge-base-sdd-whitepaper.md) 配套的操作层文档；侧重 **RepoWiki 怎么放、怎么长出来**，以及 **Custom Skills / OpenSpec / Superpower** 编排下的前端迭代节奏。

---

## 引言：三件事一起转

| 组件 | 回答的问题 |
|------|------------|
| **RepoWiki（或统一 KB 中的人造层）** | 仓库的真实约定在哪：路由、状态、组件、业务术语 |
| **OpenSpec（定方向）** | 本轮「做什么」已写成可评审的 Spec，未确认不动业务代码 |
| **Superpower（带节奏）** | Spec 确认后由技能链拆解计划、执行、验收 |

Custom Skills（如 Repo 探索、knowledge-base 写入、前端 CR）把流程变成可重复调用的规程；与白皮书中的 **四层 skill 闭环**（`explore-repository` → `initialize` / `refine` / `archive-knowledge-base`）可并行存在：前者偏 **仓库根 `repowiki/` 模板与人类规范**，后者偏 **`docs/` 下 00–06 索引层的自动维护**。统一目录构想见 [knowledge-base-structure-recommendation.md](../knowledge-base-structure-recommendation.md)。

---

## 一、RepoWiki

### 1.1 目录结构（前端落地形态）

团队在业务仓库 **`repowiki/`**（项目根目录）中维护结构化 Wiki，章节与模板一一对应，便于检索与批量更新：

```text
repowiki/
├── INDEX.md                    # 知识索引与 AI 阅读顺序
├── 01-项目概述.md
├── 02-技术规范.md
├── 03-路由与页面结构.md
├── 04-组件库文档.md
├── 05-状态管理.md
├── 06-API文档.md
├── 07-业务知识.md
└── 08-测试用例.md
```

模板源文件路径（本仓库）：`docs/frontend-ai-standards/internal-playbook/02-repowiki/templates/*.template.md`。

若团队采用白皮书推荐的 **单层 `docs/` 统一知识库**，可将上述「规范 / 前端专项 / 业务」迁入 `07_standards/`、`08_frontend/`、`09_business/`，由 AI 维护的代码索引层放在 `00_overview/`–`06_features/`；迁移步骤见 [knowledge-base-structure-recommendation.md §六](../knowledge-base-structure-recommendation.md)。

### 1.2 如何生成与保持新鲜

**路径 A — 从零按模板建站（人或 AI 填空）**

- 复制 `templates/` 下各 `.template.md` 到目标仓 `repowiki/`，去掉 `.template` 后缀，与上一节文件名对齐。
- 替换占位符；删或标「不适用」的空节。
- 维护 `INDEX.md`：链接与摘要与 01–08 标题一致。
- 前端 Owner 做一次完整性评审后随 PR 演进；自检项可把「RepoWiki / Spec 是否同步」写入 DoD。

详细步骤见 [internal-playbook/02-repowiki/README.md](../internal-playbook/02-repowiki/README.md)。

**路径 B — 代码索引层自动生成（Knowledge-base skill）**

- 触发条件与白皮一致：`./repowiki/RUNBOOK.md` 语义下若项目在 `docs/` 建库可用 `initialize-knowledge-base`，日常问题入口用 `explore-repository`，过时或缺口用 `refine-knowledge-base`，功能交付后用 `archive-knowledge-base`。
- 写入边界：AI skill **不写**工程师维护的规范区（等价于 `repowiki/` 中 02–07 里偏「共识与业务」的段落时需人工评审），具体分区见白皮 **§RepoWiki 不是代码的第二份拷贝** 与结构建议文档 **[A]/[H] 图例**。

**与 OpenSpec 的衔接**

- 生成或更新 `specs/global-specs.md`、功能级 Spec 前，应 **先读 `repowiki/INDEX.md` 再顺藤摸瓜**；Prompt 范本见 [openspecs-frontend-guide.md §2–3](../internal-playbook/03-sdd/openspecs-frontend-guide.md)。

---

## 二、前端 AI Coding 规范：Custom Skills × OpenSpec × Superpower

### 2.1 四支柱（前端版 SDD）

| 支柱 | 职责 |
|------|------|
| **OpenSpec** | 动代码前产出结构化 Spec；**团队流程不使用 `openspec apply` 执行代码**，确认后交棒 Superpower |
| **Superpower** | `brainstorming`（可选）→ `writing-plans` → `subagent-driven-development` / `executing-plans` → `verification-before-completion` → `finishing-a-development-branch` |
| **RepoWiki / KB** | Spec 生成前、`writing-plans` 前、合并后三路读/写上下文 |
| **.cursorrules + Custom Skills** | 持续纪律 + 可复用规程（explore、knowledge-base、frontend CR 等） |

节奏总图与表格说明：[internal-playbook/03-sdd/README.md](../internal-playbook/03-sdd/README.md)。

### 2.2 与白皮「标准节奏」的对照

- 白皮 **§4.1** 强调的 **「Spec 确认前不动代码」** 与本节 OpenSpec 约定一致。
- **`writing-plans` 生成计划前必读 RepoWiki**：保证文件路径、命名、Store/API 指向真实仓库，而非对话内臆测。

### 2.3 OpenSpec 操作入口

- CLI 安装、全局 Spec / 新需求 Spec / 合并后同步三组场景与可复制 Prompt：[openspecs-frontend-guide.md](../internal-playbook/03-sdd/openspecs-frontend-guide.md)。

---

## 三、前端专属能力（在 SDD 中的位置）

以下能力不改变 **「先 Spec → 再 Superpower」** 主轴，而是在 **产出 Spec、实施计划、Review、验收** 各阶段多出可验证的抓手：

| 能力 | SDD 中的典型用法 |
|------|-------------------|
| **D2C（Design-to-code）** | Spec 已定稿并有设计交付物时：在 **`brainstorming` / `writing-plans`** 中显式引用设计令牌、组件分区与响应式约束，避免实现阶段自由发挥偏离设计系统 |
| **（Kiki）AI-test** | 在 Spec 的 **测试与验收** 小节写清覆盖场景；合并前由 **`verification-before-completion`** 驱动生成/补强用例清单，人机共审高危路径 |
| **Data-claw 埋点贯通** | 在 Spec **技术约束** 中写明事件名与属性契约；实现后对照数据层（如 dataLayer / 埋点配置）做一次性核对，避免「代码已上、分析侧对不上」 |
| **cr-frontend / CR Skill** | PR 就绪前：用 **`requesting-code-review`** 或挂载 **Frontend PR Code Review** 类 Skill，对照结构、Vue 惯例、回归清单；Reviewer 反馈用 **`receiving-code-review`** 逐项核实再改 |

检查项示例可参考：[internal-playbook/05-review-checklist/frontend-review-checklist.md](../internal-playbook/05-review-checklist/frontend-review-checklist.md)。

---

## 四、两种演进策略：Spec 迭代 vs RepoWiki 迭代

| 维度 | Spec-based iteration | RepoWiki iteration |
|------|---------------------|---------------------|
| **主要载体** | `specs/`、`openspec/changes/`、功能级 markdown | `repowiki/` 或与 KB 中的人造章节（07–09） |
| **驱动时机** | 每个需求：范围、契约、交互、边界先变 | 架构 / 路由 / Store / 业务术语变更：先更正 Wiki |
| **优势** | 版本化意图清晰；适合评审与对齐产品 | 长期上下文稳定；下一轮 AI **读 RepoWiki** 成本低 |
| **风险** | Spec 归档不及时会与代码分叉 | Wiki 纯手工易滞后 → 需在 DoD 中强制合并后刷新 |
| **推荐组合** | 迭代中 **Spec 先行**；合入后与 **RepoWiki / global-specs** 双向对齐（白皮书 **Definition of Done**） |

白皮 **§持续演进** 的补充视角：大范围改代码前先更新模块边界叙述（等价于 Wiki 侧），可把「被动 refine」转成「主动的 RepoWiki-first 变更」。

---

## 五、Skill Hub：`v-ai-frontend`

**`v-ai-frontend`** 定位为团队前端的 **Skill Hub（技能枢纽）**：在统一版本与管理面下分发与前端 SDD 相关的 Custom Skills（含 RepoWiki / OpenSpec 提示模版、Superpower 链、sdd-flow 资产、前端 CR、埋点校验等）。

- **使用方式**：各业务仓通过 Hub 约定的安装路径（Plugin / `.cursor/skills` / AGENTS 声明）挂载同一批技能版本，避免「每人拷贝一份 SKILL.md」导致漂移。
- **与 Plugin 演进**：白皮 **§六** 提出将协作 skill **打包为可安装 Plugin**；Hub 可作为 Plugin 清单与 semver 的来源，滚动升级而不逐仓改文件名。

本地 Playbook（模板与 SDD README）与本白皮书保持 **引用关系**；Hub 负责 **编排哪些技能进入默认包、版本号与变更说明**。

---

## 六、延伸阅读

| 文档 | 用途 |
|------|------|
| [knowledge-base-sdd-whitepaper.md](./knowledge-base-sdd-whitepaper.md) | 方法论与知识库分层总述 |
| [internal-playbook/02-repowiki/README.md](../internal-playbook/02-repowiki/README.md) | RepoWiki 原则、模板树、验收 |
| [internal-playbook/03-sdd/README.md](../internal-playbook/03-sdd/README.md) | 四支柱与 Superpower 技能表 |
| [openspecs-frontend-guide.md](../internal-playbook/03-sdd/openspecs-frontend-guide.md) | OpenSpec 安装与三类 Prompt |
| [knowledge-base-structure-recommendation.md](../knowledge-base-structure-recommendation.md) | `docs/` 统一分层与 `[A]`/`[H]` 分工 |
