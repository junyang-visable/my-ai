# OpenSpecs 前端实践指南

面向 **Vue 3 / Nuxt 3** 与 **Cursor** 团队：如何用 OpenSpec CLI 与 Superpower 技能链完成「存量补 Specs → 新需求先 Spec → 合并后同步」的完整闭环。官方仓库：<https://github.com/Fission-AI/OpenSpec>。

> **本指南在四支柱模型中的位置**：专注 **OpenSpec（定方向）** 的具体操作；Superpower 节奏在每个场景末尾给出衔接指引。

---

## 1. 安装方式

**环境要求**：Node.js **20.19.0 或更高**。

**全局安装（推荐，任意仓库直接用 `openspec` 命令）**：

```bash
npm install -g @fission-ai/openspec@latest
```

安装完成后可在项目根目录执行：

```bash
cd /path/to/your-frontend-repo
openspec init
openspec --help
```

**仅当前仓库本地开发依赖（不污染全局，适合 CI 或单项目锁定版本）**：

```bash
cd /path/to/your-frontend-repo
npm install -D @fission-ai/openspec@latest
```

通过 `npx` 调用（示例）：

```bash
npx openspec init
npx openspec update
```

升级全局版本：

```bash
npm install -g @fission-ai/openspec@latest
```

在项目内刷新 AI 指令与斜杠命令配置：

```bash
openspec update
```

> **包名说明**：npm 上的官方包为 `@fission-ai/openspec`；安装后 CLI 名称是 `openspec`。请勿与 npm 上无关的同名包混淆。

---

## 2. 场景一：为存量仓库生成全局 Specs

### 2.1 前置条件

- 目标仓库已具备 `repowiki/`（并与 [RepoWiki 模板](../02-repowiki/templates/) 章节对应）。
- 已在仓库根目录执行过 `openspec init`（若团队暂不用 OpenSpec 变更目录，至少保证存在 `specs/` 目录）。

### 2.2 推荐步骤

1. 在 Cursor 中打开目标仓库，确认 `repowiki/` 最新。
2. 新建或确保存在目录 `specs/`。
3. 将 **2.3 节完整 Prompt** 粘贴到新对话（Composer / Agent），发送后等待生成 `specs/global-specs.md`。
4. **生成后人工评审**（见 2.4）。
5. 通过后按 **2.5** 提交 Git。
6. **衔接 Superpower**：全局 Specs 就绪后，后续新需求可直接进入「场景二」节奏，无需每次重新梳理全局。

### 2.3 完整 Prompt 模板（复制即用）

```text
你是资深前端架构师，熟悉 Vue 3、Nuxt 3、Pinia（或本仓库实际状态方案）。请为本仓库生成一份「全局 Specs」文档，用于 SDD（Spec-Driven Development）与 AI 编码时的单一事实来源。

## 输入来源（必须阅读）
1. 先阅读本仓库的 RepoWiki：从 `repowiki/INDEX.md`（若不存在则从 `repowiki/` 目录下索引文件）开始，按其中指引依次阅读 01–07（或等价章节）：项目概述、技术规范、路由与页面结构、组件库、状态管理、业务知识、测试等。
2. 结合代码验证：对照 `pages/`、`app/`、`layouts/`、`components/`、`stores/`、`composables/`、`server/api/`（以本仓库实际目录为准）与 Wiki 是否一致；若 Wiki 与代码冲突，以代码为准并在 Spec 中标注「Wiki 待更新」。

## 输出要求
1. 输出文件路径（若目录不存在请说明需要创建）：`specs/global-specs.md`。
2. 文档语言：中文为主，专有名词可保留英文。
3. 结构要求：
   - 文件顶部用简短段落说明本仓库前端技术栈、路由约定、状态管理方案（与 Wiki 一致）。
   - 主体为「Spec 条目表」：**每个独立页面或独立功能点占一行（或一块）**，不要合并成模糊的大段叙述。
4. 每个 Spec 条目必须包含以下列（用 Markdown 表格呈现；若某字段不适用写「无」）：
   - **页面路径**：Nuxt/Vue Router 路径或文件路由路径，例如 `/orders`、`/products/[id]`。
   - **功能描述**：一句话说明用户价值与业务场景。
   - **核心交互**：列表或编号列出关键用户操作、加载/空/错状态、主要表单校验规则（如有）。
   - **涉及的 Stores**：Pinia store 名称或文件路径，以及读写的 state/getter/action 要点。
   - **涉及的 APIs**：REST/GraphQL/Server Route 路径、方法、关键 query/body 字段；注明是否需鉴权。
5. 覆盖范围：尽量覆盖 Wiki「路由与页面结构」中出现的全部页面；对 Wiki 未写但代码中存在的页面也要补齐，并标记「RepoWiki 缺失，已从代码推断」。
6. 不要编造不存在的接口或 Store：凡不确定处，标注「待确认」并列出建议核对文件路径。
7. 不要在此时编写实现代码；只输出 `specs/global-specs.md` 的完整 Markdown 正文（从一级标题开始）。

请开始执行：先说明你将阅读哪些 Wiki 与代码路径，然后给出完整的 `specs/global-specs.md` 内容。
```

### 2.4 生成后评审（必做）

- [ ] 抽查 2–3 个核心页面，核对表格中的路径、Store、API 是否与真实代码一致。
- [ ] 确认无「凭空接口」：所有「待确认」项有负责人或跟进 issue。
- [ ] 若发现 RepoWiki 滞后，另开任务更新 Wiki（Spec 与 Wiki 应长期一致）。

### 2.5 提交建议

```bash
git add specs/global-specs.md repowiki/
git status
git commit -m "docs: add global SDD specs from RepoWiki and codebase"
```

（若本次只新增 Spec、未改 Wiki，可只 `git add specs/global-specs.md`。）

---

## 3. 场景二：新需求开发前生成 Specs

### 3.1 推荐步骤

1. 产品/业务方提供需求说明（可粘贴到 Prompt 的「需求原文」区）。
2. 将 **3.2 完整 Prompt** 粘贴到 Cursor，把需求原文贴入指定位置后发送。
3. 人工评审 AI 输出的四个章节，补充边界与验收标准。
4. **明确回复 AI「确认 Spec，可以开始编码」之前，禁止开始写业务实现代码**（允许 AI 只改文档或 OpenSpec 变更目录下的 markdown）。
5. **Spec 确认后，交棒 Superpower**（OpenSpec apply 不再使用）：
   - **方案不明时**（可选）：先调用 `superpowers:brainstorming` 探实现方案，产出设计文档后自动衔接 `writing-plans`。
   - **方案明确时**：直接调用 `superpowers:writing-plans`，基于确认后的 Spec + `repowiki/` 生成分步实施计划。
   - 计划评审通过后，调用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans` 执行。
   - 全部任务完成后，调用 `superpowers:verification-before-completion` 确认无遗漏，再进入 `superpowers:finishing-a-development-branch`。

### 3.2 完整 Prompt 模板（复制即用）

```text
你正在协助一个 Vue 3 / Nuxt 3 前端仓库做 Spec-Driven Development。以下是一条新需求，请先产出 Spec 文档，**不要编写或修改任何业务实现代码**（允许创建/更新 `specs/` 或 `openspec/changes/<name>/` 下的 markdown 说明文件）。

## 需求原文（由人类粘贴）
"""
[在此粘贴完整需求描述：背景、目标用户、入口、验收标准、已知约束、设计稿或原型链接（如有）]
"""

## 上下文（必须先读）
请先阅读 `repowiki/INDEX.md`，按索引阅读与本次需求相关的章节（至少：技术规范、路由与页面结构、状态管理），再结合 `.cursorrules` 中的约束，生成与仓库实际情况一致的 Spec。

## 你必须输出的 Spec 结构（四个章节，中文）
请输出一份独立的 Markdown Spec（若团队已有 OpenSpec 变更目录，可说明建议文件名，例如 `openspec/changes/feature-xxx/specs.md`；否则用 `specs/feature-<short-name>.md`）。四个章节如下：

### 1. 功能范围
- In scope：明确列出本次要做的事。
- Out of scope：明确列出本次不做的事，避免范围蔓延。
- 依赖与假设：依赖其他团队/接口/配置时写清楚。

### 2. 数据模型
- 领域对象与字段：前端关心的实体、字段类型、是否可选、默认值。
- 与后端/API 的映射：endpoint、method、请求与响应形状（用 TypeScript interface 或表格描述均可）。
- 缓存与同步：是否写入 Pinia、localStorage、URL query 等。

### 3. 交互细节
- 页面/路由：路径、布局、关键组件层级（简要）。
- 用户流程：逐步列出点击、跳转、提交、返回。
- 状态机：加载中、成功、空数据、错误、无权限等如何展示与恢复。
- 可访问性与文案：关键按钮、错误提示、loading 文案要点（如有设计规范请遵守）。

### 4. 技术约束
- 必须使用的组件库/组合式函数/已有模块（从 repowiki/ 与 .cursorrules 推断；不确定则写「待对照 RepoWiki」）。
- 性能与安全：列表虚拟化、防抖节流、XSS、敏感字段脱敏等要求。
- 埋点/监控：若需求涉及分析事件，列出建议事件名与属性（与团队 GA/埋点规范一致时再定稿）。
- 测试：建议的单元/E2E 覆盖点（不写具体测试代码）。

## 流程约束（极其重要）
1. 先输出完整 Spec 四个章节。
2. 在 Spec 末尾增加「开放问题」列表，列出你需要人类补充澄清的点。
3. 输出结束后停止，并写明：「请人类评审并回复：确认 Spec 后我才会开始编码。」
4. 在我方明确回复「确认 Spec，可以开始编码」之前，你不要创建或修改 `.vue`、`.ts` 等业务源码文件。

请现在开始：先说明你将阅读哪些 RepoWiki 章节与 .cursorrules，然后生成上述 Spec。
```

---

## 4. 场景三：开发完成后更新 Specs

在 PR 合并或发布完成后，用下列**短 Prompt** 同步文档与 Wiki，避免 Spec 与代码再次分叉。

> **节奏提示**：此步骤通常在 `superpowers:verification-before-completion` 确认无误、准备提 PR 前或合并后执行。

### 短 Prompt 模板（复制即用）

```text
本次功能已合并进主分支。请根据当前代码与已合并的 PR 做文档同步，不要重构无关代码。

1. 阅读本次改动涉及的源码（diff 或文件列表若我贴在下方请一并参考）。
2. 更新对应的 Spec 文件（全局 `specs/global-specs.md`、页面/功能级 Spec、或 `openspec/changes/` 中未归档条目）：修正页面路径、交互、Store、API 等与实现不一致之处。
3. 若 `repowiki/` 中路由、状态、业务章节与实现不一致，给出具体修改片段或完整替换段落（优先最小 diff）。
4. 输出：① 变更文件清单；② 每个文件的更新摘要；③ 是否仍有「待确认」项。

【可选：粘贴 PR 链接、commit SHA、或改动文件路径列表】
```

---

## 5. 验收标准

在评审一份 Spec 或一次 SDD 流程是否合格时，至少满足：

- [ ] **可对码**：Spec 中能定位到具体路由/页面、主要交互步骤、以及关键 API 与 Store，工程师或 AI 无需再猜「在哪改」。
- [ ] **可验收**：功能范围与 Out of scope 清楚；交互含成功/失败/空/加载；与需求原文无明显遗漏或冲突（开放问题已闭环或有负责人）。
- [ ] **可维护**：合并后已同步 `specs/` 与 `repowiki/`（或已建 issue 跟踪 Wiki 更新），避免「代码已变、文档仍旧」长期存在。
- [ ] **Superpower 已完整走过**：`writing-plans` → `subagent-driven-development` / `executing-plans` → `verification-before-completion` → `finishing-a-development-branch` 均已执行（方案不明时 `brainstorming` 应在 `writing-plans` 前执行），无跳跃。

---

## 相关链接

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [本目录 README：SDD 四支柱规范](./README.md)
- [RepoWiki（前端版）](../02-repowiki/README.md)
- [Cursorrules 模板](../01-cursor-rules/README.md)
