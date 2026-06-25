# AI 辅助开发的知识库工程与 SDD 实践

> Visable AI 技术白皮书 — 知识库与规格驱动开发篇

## 引言

常见失败：**约束缺位、不懂业务语境、边界与安全留白**。归因于模型能力容易忽略一点：模型不记得本仓库，跨会话也不继承隐含前提——只靠粘贴片段时，输出容易和仓库内约定脱节。

两件事一起做：**代码知识库（RepoWiki）**把项目知识结构化落盘，便于检索与核对；**规格驱动开发（SDD）**在写代码前把规格写清楚。缺一则容易在稀薄上下文里「想当然」。

---

## 一、知识库的定位与设计原则

### 1.1 RepoWiki 不是代码的第二份拷贝

定位是**索引**，不是长篇叙述。每条记录只做三件事之一：

- 全局说明（某个功能/模块/系统做什么，1–3 行）
- 链到另一条 RepoWiki
- 链到源码（精确路径 + 一行说明）

推论：要用多行解释一个函数，就改成「路径 + 一行」。代码是唯一真相来源；叙事型 RepoWiki 易腐化、易误导检索，索引型最多「过时」——后者更容易被发现和修补。

### 1.2 可验证优于堆砌篇幅

不靠篇幅撑门面，每条尽量能对照代码核实。`META.md` 记最后一次对齐的 git commit SHA，使用前可判断 RepoWiki 是否过期。

### 1.3 写作约束（无例外）

- 单文件少于 200 行
- 用条目，不写长段落
- 不虚构功能：只摘录、不揣测
- `06_features/` 须含 Mermaid 流程图
- `04_modules/` 须含 Scope Table（Implementation / Consumer）
- `05_symbols/` 按需写，不预生成
- 不用 emoji

---

## 二、RepoWiki 目录结构

按**知识粒度**分层，不按话题堆目录：

```text
repowiki/
├── META.md                  # schema_version、last_commit、last_synced
├── RUNBOOK.md               # 全局入口，按意图导航
├── 00_overview/
│   ├── big_picture.md
│   └── tech_stack.md
├── 01_maps/
│   ├── system_map.md        # 须 Mermaid
│   ├── feature_map.md
│   └── module_map.md        # 须 Mermaid（入口视图）
├── 02_guides/
│   ├── dev.md
│   ├── deploy.md            # 须含 pipeline Mermaid
│   └── debug.md
├── 03_index/
│   ├── file_index.md
│   └── api_index.md
├── 04_modules/
│   └── <name>.md
├── 05_symbols/
│   └── <module-slug>.md
└── 06_features/
    └── <kebab-name>.md
```

层级分工：`00` 全貌，`01` 功能/模块在哪，`03` 文件在哪，`04` 边界，`05` 符号，`06` 功能实现要点。

---

## 三、四个 Skill 与生命周期

```
explore-repository（入口）
      │
      ├─ 无 META / RUNBOOK ──► initialize-knowledge-base
      ├─ last_commit ≠ HEAD ──► refine-knowledge-base
      └─ 文档答不上 ──► refine-knowledge-base

交付完成 ──► archive-knowledge-base
```

### 3.1 explore-repository

总入口：**能查 RepoWiki 就不先扫源码**。流程纲要：version-check → `RUNBOOK.md` → 按 navigation-guide 落点 → answer-format；若读写代码则走 verification-protocol；发现缺口则 refine。

`explore-repository` **不写** `./repowiki/`；补文档用 `refine-knowledge-base`，功能归档用 `archive-knowledge-base`。

| 问题类型     | 路线 |
| ------------ | ---- |
| 项目做什么   | `00_overview/big_picture.md` → `01_maps/system_map.md` |
| 功能在哪     | `01_maps/feature_map.md` → `04_modules/<name>.md` |
| 某路径做什么 | `03_index/file_index.md` → Scope Table → `feature_map.md` |
| 符号做什么   | `05_symbols/<slug>.md`；无则读后 refine |
| 运行/部署    | `02_guides/` 下对应文件 |

### 3.2 initialize-knowledge-base

**触发**：`./repowiki/RUNBOOK.md` 不存在。主 agent 收 subagent 的结构化产出再落盘（避免把整个仓库塞进上下文）。

步骤顺序固定（节选）：

| 阶段 | 产出 |
| ---- | ---- |
| Stack/Structure（subagent） | TECH_STACK、分层、模块边界等 |
| Main | `00_overview`、`01_maps` |
| File Indexer（sub） | `03_index/` |
| Module Extractors 并行（sub） | `04_modules/` |
| Guide Extractor（sub） | `02_guides/` |
| Main | `RUNBOOK.md`、`META.md`（最后写，对齐写完后的 HEAD） |

`heuristics.md` 可从 `package.json`、`go.mod` 等推断栈，减少手工配置。

### 3.3 archive-knowledge-base

**触发**：用户完成信号 + `06_features/<name>.md` 尚不存在，或钩子要求同步。

概要：提取功能名 → `git diff --name-only main` → **先读变更代码**，再套 `feature-doc-template.md` 写 feature 文档 → 更新 `feature_map`、`file_index`、`RUNBOOK`、`META`。

### 3.4 refine-knowledge-base

**触发**：问的模块/路径在 RepoWiki 里缺或不完整。

`gap-detection.md`：`feature_map` → `04_modules/` → `file_index`（符号级再加 `05_symbols/`）。确认为缺口再派范围受限 subagent；主 agent 据 FINDINGS 写回 RepoWiki。**与 archive 同属对 Repowiki 的写路径**，规范和 explore 的分工不变。

---

## 四、SDD 与知识库

SDD：**Spec 未定不动手**。RepoWiki：**Spec 和实施阶段都踩在真实约束上**。

```
需求 → explore-repository（读 overview / feature_map / 相关模块）
     → Spec（OpenSpec，人工确认）
     → 实施（如 writing-plans / executing-plans，阶段内可再对照 RepoWiki）
     → 合并 → archive-knowledge-base
```

### 关键读库节点

| 节点           | 读什么                         | 作用           |
| -------------- | ------------------------------ | -------------- |
| Spec 前        | `00_overview`、相关 `04_modules` | 边界与既有架构 |
| 拆计划时       | `module_map`、`file_index`     | 路径真实可查   |
| 实施中         | `05_symbols`、`06_features`    | 签名与既有行为 |

### Definition of Done

合并后建议同时满足：**Spec 已更新、`archive-knowledge-base` 已跑**（含 `06_features`、`feature_map`、`file_index`、`META`）。否则下次 explore 仍会碰到 stale/refine；主动归档比事后补缺便宜。

---

## 五、落地与分工

### 优先级

1. `initialize-knowledge-base` 建库  
2. 习惯上 **先 explore**  
3. 固定「读库 → Spec → 实施 → 归档」节奏  
4. DoD 写上「合并后 archive」  

### Owner

- 立项时跑一次初始化，检查 `META` / `RUNBOOK`  
- 人工核对 `big_picture`、业务侧目录（若有）  
- DoD 含归档  

### 开发者在需求上的极简路径

需求 → explore → Spec → writing-plans（真实路径）→ 实施 → 缺口则 refine → 合并后 archive。

---

## 六、持续演进

1. **先改 RepoWiki（地图与模块边界），再让 AI 做大范围改写**——文档掉队时，改写面越大越乱。  
2. **每次 refine 显性化一块知识**：缺口被写进 RepoWiki，同类问题少反复。  
3. **`05_symbols/` 读后写入**：不设全量生成，只靠实际接触过的符号积累高频入口。  
4. **Skill 成熟后可收敛为 Plugin**：打包安装、统一版本，降低逐文件拷贝与漏配成本。
