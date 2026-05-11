# AI 辅助开发的知识库工程与 SDD 实践

> Visable AI 技术白皮书 — 知识库与规格驱动开发篇

## 引言：上下文是质量的底盘

AI 辅助编码失败的方式是高度相似的：输出偏离约束、不懂业务语境、在边界与安全细节上留洞。将问题归咎于模型能力，往往掩盖了真正的短板——**上下文工程的缺失**。模型没有对本代码库的持久记忆；跨会话不继承隐含前提；若仅依赖临时粘贴的片段，输出主要依据公开常识，与项目已生效约定之间容易产生系统性偏差。

解决路径有两条，需同步推进：其一，把项目知识结构化落盘，形成 AI 可检索、可验证的**代码知识库（KB）**；其二，用**规格驱动开发（SDD）**在动手前先确认规格，使每次实施都站在明文约束上。二者缺一，都会让 AI 在真空中编造。

---

## 一、知识库的定位与设计原则

### 1.1 KB 不是代码的第二份拷贝

知识库的核心定位是**索引层**，不是叙述层。每一条 KB 记录做且只做三件事之一：

- 描述全局（一个功能/模块/系统做什么，1–3 行）
- 指向另一个 KB 文件（跨层级导航链接）
- 指向原始代码（精确文件路径 + 一行角色说明）

这一原则的推论是：如果解释一个函数体超过一行，就用文件路径 + 一行描述替代。代码是真相的来源，KB 是进入代码的索引。叙述性的 KB 很快会腐化并误导 AI，而索引性的 KB 只会「过期」——过期可被检测，误导不易察觉。

### 1.2 可验证性优于完整性

KB 不追求篇幅或版式，而追求**可验证性**：每一条记录都应能对照代码核实。KB 引入了 `META.md` 作为版本锚点——记录最后一次同步时的 git commit SHA，使 agent 在每次使用前能精确判断 KB 是否过期，而不是靠猜测。

### 1.3 写作约束

以下约束对所有 KB 文件强制执行，无例外：

- 每文件 < 200 行
- 使用 bullet points，不用段落散文
- 不发明不存在的功能，只提取，不假设
- `06_features/` 文件必须包含 Mermaid 流程图
- `04_modules/` 文件必须包含 Scope Table（Implementation 行与 Consumer 行）
- `05_symbols/` 文件只按需写入，不预生成
- 不使用 emoji

---

## 二、KB 目录结构与分层逻辑

KB 按「知识层次」分层，而非按「话题」分类：

```text
docs/
├── META.md                  # 版本锚点：schema_version、last_commit、last_synced
├── RUNBOOK.md               # 全局路由器：导航入口，按意图组织
├── 00_overview/
│   ├── big_picture.md       # 系统做什么、核心流、约束
│   └── tech_stack.md        # 技术栈：runtime / frontend / backend / storage / infra
├── 01_maps/
│   ├── system_map.md        # 系统层级 Mermaid 图（必须）
│   ├── feature_map.md       # 功能名 → 模块链接
│   └── module_map.md        # 模块名 → 入口文件 Mermaid 图（必须）
├── 02_guides/
│   ├── dev.md               # 本地开发：安装、启动、测试命令
│   ├── deploy.md            # 构建与部署：命令 + Mermaid pipeline 图（必须）
│   └── debug.md             # 常见问题 → 解法，日志路径
├── 03_index/
│   ├── file_index.md        # path → 一行含义，按顶层目录分组
│   └── api_index.md         # METHOD /path → 用途（有后端时生成）
├── 04_modules/
│   └── <name>.md            # 模块职责、入口、关键文件、约束、Scope Table
├── 05_symbols/
│   └── <module-slug>.md     # 函数/符号级索引，按需写入
└── 06_features/
    └── <kebab-name>.md      # 已完成功能：概述、Mermaid 架构图、关键文件、决策
```

每一层解决不同粒度的问题：`00_overview` 回答「系统是什么」，`01_maps` 回答「功能在哪」，`03_index` 回答「文件在哪」，`04_modules` 回答「模块的边界」，`05_symbols` 回答「函数做什么」，`06_features` 回答「功能怎么实现」。

---

## 三、KB 生命周期：四个 Skill 的协作

KB 的全生命周期由四个 Agent Skill 覆盖，形成闭环：

```
explore-repository（所有问题的入口）
      │
      ├─ ./docs/META.md 不存在 ──► initialize-knowledge-base（从零建库）
      │
      ├─ KB 过期（last_commit 对不上 HEAD）
      │         └─► refine-knowledge-base（修复 stale 条目）
      │
      └─ KB 有 gap（问题无法从 docs/ 回答）
                └─► refine-knowledge-base（填补缺失）

功能开发完成 ──► archive-knowledge-base（归档新功能）
```

### 3.1 explore-repository：先问 KB，再看代码

`explore-repository` 是所有代码库问题的总入口。其核心原则只有一条：**读源代码是最后手段，而非第一动作**。

执行流程：

```
Step 0  加载 version-check.md — 用 META.md 中的 last_commit 比对当前 HEAD
        若有 KB 覆盖的源文件发生变更 → 触发 refine-knowledge-base 后继续
Step 1  打开 RUNBOOK.md — 获取导航起点
Step 2  用 navigation-guide.md 路由到对应 KB 文件
Step 3  用 answer-format.md 模板组织答案
Step 4  若需读/改代码 → 先跑 verification-protocol.md，对比 KB 与实际代码
Step 5  若 KB 有 gap → 触发 refine-knowledge-base，然后继续
Step 6  若读了代码回答了函数问题 → 触发 refine-knowledge-base（gap type=symbol）
```

`explore-repository` 本身**永不直接写 `./docs/`**，所有写操作都通过 `refine-knowledge-base` 完成。这个约束确保 KB 的写入路径是单一的，格式不会因调用方不同而漂移。

导航路由按问题类型分流：

| 问题类型 | 路由路径 |
|----------|----------|
| 项目做什么 | `00_overview/big_picture.md` → `01_maps/system_map.md` |
| 功能 X 在哪 | `01_maps/feature_map.md` → `04_modules/<name>.md` |
| 文件路径 X 做什么 | `03_index/file_index.md` → Scope Table → `feature_map.md` |
| 函数/符号 X 做什么 | `05_symbols/<slug>.md` → 有则直接答，无则读源码后 refine |
| 如何运行/部署 | `02_guides/dev.md` / `deploy.md` / `debug.md` |

### 3.2 initialize-knowledge-base：全量建库

**触发条件**：`./docs/RUNBOOK.md` 不存在（全新项目）。

设计上，主 agent 不直接读源码——所有代码探索由 subagent 完成，主 agent 只接收结构化输出并写 KB 文件。这个分工防止大量原始代码填满主 agent 的 context。

九步顺序不可跳越、不可乱序：

| 步骤 | 执行者 | 产出 |
|------|--------|------|
| Step 1+2 | Subagent（Stack & Structure Scanner） | TECH_STACK / SYSTEM_LAYERS / FEATURE_CLUSTERS / MODULE_BOUNDARIES |
| Step 3 | Main agent | `00_overview/big_picture.md` + `tech_stack.md` |
| Step 4 | Main agent | `01_maps/system_map.md` + `feature_map.md` + `module_map.md` |
| Step 5 | Subagent（File Indexer） | `03_index/file_index.md` + `api_index.md` |
| Step 6 | Subagent × N（Module Extractors，并行） | `04_modules/<name>.md`（每模块一个） |
| Step 7 | Subagent（Guide Extractor） | `02_guides/dev.md` + `deploy.md` + `debug.md` |
| Step 8 | Main agent | `RUNBOOK.md` |
| Step 9 | Main agent | `META.md`（写入 last_commit SHA） |

Step 1+2 的 subagent 由 `heuristics.md` 驱动：根据项目文件（`package.json`、`go.mod`、`requirements.txt`、`pom.xml`、`Cargo.toml` 等）自动识别后端框架、前端框架、样式方案、UI 库、数据库、CI/CD、基础设施，无需人工配置。

Step 6 并行派发——有多少模块就起多少 subagent，等全部返回后统一写入，这是初始化阶段最耗时步骤的主要加速手段。

**META.md 在最后写**：确保 `last_commit` 对齐的是 KB 写完后的代码状态，避免版本锚点与 KB 内容错位。

### 3.3 archive-knowledge-base：功能交付后归档

**触发条件**：用户发出完成信号（"done"、"PR is up"、"tests pass"）且 `./docs/06_features/<feature-name>.md` 尚不存在；或 git push hook 触发 `KB_SYNC_REQUIRED` 信号。

六步流程（全部由主 agent 执行，Step 3 读代码）：

```
Step 1  从 git branch 或对话上下文提取功能名（转为 kebab-case）
Step 2  用 git diff --name-only main 列出变更文件
Step 3  读变更代码 — 提取架构决策、数据流、约束、外部依赖
Step 4  用 feature-doc-template.md 创建 ./docs/06_features/<kebab-name>.md
Step 5  更新 feature_map.md（添加条目）+ file_index.md（添加新路径）
Step 6  更新 RUNBOOK.md（添加功能链接）+ META.md（更新 last_commit）
```

关键约束：**必须先读完代码（Step 3）再写 feature doc（Step 4）**，不可凭印象写。RUNBOOK.md 和 META.md 最后更新，确保它们指向的内容已经存在。

### 3.4 refine-knowledge-base：按需填补 gap

**触发条件**：用户询问的功能/模块/代码路径在 `./docs/` 中缺失或不完整。

先确认 gap 再动手——`gap-detection.md` 提供三步检查法：

```
Check 1  01_maps/feature_map.md — 搜索功能名或关键词
Check 2  04_modules/ — 扫描是否有覆盖该模块的文件
Check 3  03_index/file_index.md — 搜索相关文件路径
（Check 4  05_symbols/<slug>.md — 针对函数级 gap）
```

三项均无结果才确认 gap。部分文档存在但不完整，直接跳到 Step 4 补充缺失字段，不重新生成整个文件。

gap 确认后派发一个范围受限的 subagent（只读 Step 2 中确定的最小文件列表），返回结构化 FINDINGS，主 agent 从 FINDINGS 写 KB——这与 initialize 的主/子分工一致。

`refine-knowledge-base` 是**唯一可以写 `./docs/` 的 skill**；`explore-repository` 不写，`archive-knowledge-base` 通过它间接写（实际上 archive 直接写，但遵循同样的写作规范）。

---

## 四、SDD 与知识库的协作节奏

规格驱动开发（SDD）解决的是「方向」问题——在动代码之前，先把可讨论、可确认的规格落到文档中，再驱动编码与验收。知识库解决的是「上下文」问题——让 AI 在制订规格和实施过程中，始终站在项目的真实约束上。二者需要在关键节点协同：

### 4.1 标准节奏

```
需求到达
  │
  ▼
读 KB（explore-repository）
  → ./docs/00_overview/big_picture.md   了解系统全局
  → ./docs/01_maps/feature_map.md       确认相关功能边界
  → ./docs/04_modules/<name>.md         了解涉及模块的约束
  │
  ▼
产出 Spec（OpenSpec）
  → 功能范围、数据模型、交互逻辑、技术约束
  → 人工评审确认
  │
  ▼  ← Spec 确认前不动代码
实施（Superpower：writing-plans → executing-plans）
  → 每阶段读 KB 确认约束仍然有效
  │
  ▼
验收通过 → 合并
  │
  ▼
archive-knowledge-base
  → 归档 ./docs/06_features/<feature>.md
  → 更新 feature_map.md + file_index.md + RUNBOOK.md + META.md
```

**Spec 确认前不动代码**是 SDD 的核心纪律。KB 读取不是形式——它保证 AI 在制订规格前站在当前项目的真实约束上，而不是依赖当次对话里的零星记忆或自行猜测。

### 4.2 KB 的三个关键读取节点

| 节点 | 读取目标 | 目的 |
|------|----------|------|
| **Spec 产出前** | `00_overview/` + 相关 `04_modules/` | 确认功能边界与模块约束，避免 Spec 与现有架构冲突 |
| **writing-plans 阶段** | `01_maps/module_map.md` + `03_index/file_index.md` | 生成含真实文件路径的分步计划，而非凭空编写文件清单 |
| **实施过程中** | `05_symbols/<slug>.md` + `06_features/` | 确认函数签名与已有功能约束，避免引入不一致的实现 |

### 4.3 Definition of Done

**代码合并不等于完整交付**。一次改动的闭环定义：

```
代码合并
  + Spec 同步更新
  + KB 归档（archive-knowledge-base 执行完毕）
    ├── 06_features/<feature>.md 已创建
    ├── feature_map.md 已更新
    ├── file_index.md 已更新
    └── META.md last_commit 已推进
```

若 KB 未归档，下一次 AI 辅助将在过时的上下文中运作，`version-check.md` 会在下次 `explore-repository` 时检测到这一状态并强制触发 `refine-knowledge-base`，但这是被动修复——主动归档的成本远低于事后修复的代价。

---

## 五、落地路径与角色分工

### 5.1 落地优先级

规范不宜一次性全量铺开，建议按以下顺序推进：

1. **先建 KB**（`initialize-knowledge-base`）——有 KB 才有上下文基础
2. **固化 explore 习惯**（`explore-repository` 作为所有问题的第一步）——建立「先查 KB」的反射
3. **推广 SDD 节奏**（读 KB → 产 Spec → 实施 → 归档）——节奏稳定后质量可预期
4. **写入 DoD**（合并后必须跑 archive-knowledge-base）——用流程保底

### 5.2 项目 Owner 职责

- 项目开始时触发 `initialize-knowledge-base`，确认生成的 `META.md` 和 `RUNBOOK.md` 可正常导航
- 评审 `00_overview/big_picture.md` 与 `07_business/`（如有）中的业务知识——这是 KB 中极少数需要人工补充的部分
- 将「合并后运行 archive-knowledge-base」写入团队 DoD

### 5.3 开发人员工作流

1. 接到新需求 → 运行 `explore-repository` → 读 `RUNBOOK.md` → 定位相关模块
2. 产出 Spec，人工评审确认
3. 用 `writing-plans` 生成含真实文件路径的实施计划
4. 按计划执行，过程中遇到 KB gap → `refine-knowledge-base` 自动修复
5. 验收通过，合并 → 运行 `archive-knowledge-base`

---

## 六、持续演进

**KB 不是一次性产物**，它需要与代码同源演进。以下三条节奏有助于保持 KB 长期有效：

1. **先更新 KB，再扩大改动范围**：架构或模块边界发生变化时，应先更新 `04_modules/` 与 `01_maps/`，再交给 AI 做大范围编辑。文档滞后时，改动面越大，与真实约定的偏差积累越快。

2. **gap 是信号，不是故障**：每次 `refine-knowledge-base` 填补一个 gap，都说明有一块知识之前未被显式化。把 gap 写入 KB 后，它就永久消失了——下次同样问题不会再触发 gap 检测。

3. **`05_symbols/` 按需生长**：函数级索引不预生成，只在实际读过某个函数后写入。这保证 `05_symbols/` 中的每一条记录都经过 agent 的实际阅读验证，而不是机械推断。随着项目演进，`05_symbols/` 会自然积累高频被访问的核心符号，形成项目最有价值的精炼知识层。
