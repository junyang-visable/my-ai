# 知识库结构最终建议

> 综合 knowledge-base skill 体系与 RepoWiki（frontend-ai-coding 白皮书）的设计，给出统一落地方案。

---

## 一、核心矛盾分析

两套体系的根本分歧在于**维护主体不同**：

| 维度 | knowledge-base skill | RepoWiki（白皮书） |
|------|---------------------|------------------|
| 维护主体 | AI agent 自动生成与更新 | 工程师人工维护 |
| 内容来源 | 从代码中提取 | 从业务理解和规范中沉淀 |
| 适用范围 | 技术栈无关 | 前端专属 |
| 版本追踪 | META.md 锚定 git commit | 依赖 git 历史 |
| 覆盖盲区 | 业务知识、编码规范、性能基线、测试用例 | 模块边界、符号索引、代码导航 |

**结论**：两套体系不是竞争关系，而是互补关系。统一方案的核心原则是：  
**AI 管代码层，人管规范层与业务层；合并到一个目录，按维护主体分区。**

---

## 二、统一目录结构

```text
docs/
│
│  ── 元数据 ──────────────────────────────────────────────────────
├── META.md                        # [A] 版本锚点：last_commit、last_synced
├── RUNBOOK.md                     # [A] 全局导航入口（agent 首先读取）
│
│  ── 代码层（AI 自动生成与维护）────────────────────────────────────
├── 00_overview/
│   ├── big_picture.md             # [A] 系统做什么、核心流、约束
│   └── tech_stack.md              # [A] runtime/frontend/backend/storage/infra
│
├── 01_maps/
│   ├── system_map.md              # [A] 系统层级 Mermaid 图
│   ├── feature_map.md             # [A] 功能名 → 模块链接
│   └── module_map.md              # [A] 模块名 → 入口文件 Mermaid 图
│
├── 02_guides/
│   ├── dev.md                     # [A] 安装、启动、测试命令
│   ├── deploy.md                  # [A] 构建与部署命令 + Mermaid pipeline
│   └── debug.md                   # [A] 常见问题 → 解法、日志路径
│
├── 03_index/
│   ├── file_index.md              # [A] path → 一行含义
│   └── api_index.md               # [A] METHOD /path → 用途（有后端时）
│
├── 04_modules/
│   └── <name>.md                  # [A] 职责、入口、关键文件、约束、Scope Table
│
├── 05_symbols/
│   └── <module-slug>.md           # [A] 函数/符号级索引（按需，只写不预生成）
│
├── 06_features/
│   └── <kebab-name>.md            # [A] 已完成功能：概述、Mermaid 架构图、决策
│
│  ── 规范层（工程师人工维护）────────────────────────────────────────
├── 07_standards/
│   ├── coding-conventions.md      # [H] 命名、目录、组件约定、禁用 API
│   ├── performance-baseline.md    # [H] 核心指标与阈值
│   └── review-checklist.md        # [H] CR 阻断项与建议项清单
│
│  ── 前端专项（前端项目维护，非前端可省略）──────────────────────────
├── 08_frontend/
│   ├── routes.md                  # [H] 信息架构、路由表、权限守卫、关键导航路径
│   ├── components.md              # [H] 核心组件 Props/事件/插槽说明
│   └── state.md                   # [H] Store 划分、数据流与副作用边界
│
│  ── 业务层（工程师人工维护）────────────────────────────────────────
└── 09_business/
    ├── domain-concepts.md         # [H] 领域术语与概念解释
    └── core-processes.md          # [H] 核心业务流程（「为何如此设计」的答案）
```

**图例**：`[A]` = AI agent 自动维护　`[H]` = 工程师人工维护

---

## 三、各区职责说明

### 代码层（00–06）：AI 自动维护

由 knowledge-base skill 体系全程负责：

| Skill | 负责区域 |
|-------|---------|
| `initialize-knowledge-base` | 首次生成 00–06 全部文件 + META.md + RUNBOOK.md |
| `explore-repository` | 读取导航，检测版本，触发 refine |
| `archive-knowledge-base` | 功能合并后更新 06_features + feature_map + file_index + META |
| `refine-knowledge-base` | 按需填补任意 00–06 中的 gap |

**约束**：AI 只写 `[A]` 区域，永不覆盖 `07_standards/`、`08_frontend/`、`09_business/`。

---

### 规范层（07）：工程师维护，一次写好长期有效

`07_standards/` 的内容来自团队共识，不来自代码，因此无法自动生成：

- **coding-conventions.md**：命名规范、目录约定、禁用的 API/模式、组件书写规范。对应白皮书中 `.cursorrules` 的落盘版本——规则文件的作用是「每次对话自动生效」，而本文件的作用是「可检索、可引用、可随项目修订」。
- **performance-baseline.md**：LCP/FID/CLS 阈值、包体积限制、接口超时基准。AI 在 Spec 评审和 Review 时读取，作为「可证伪的约束」而非口头标准。
- **review-checklist.md**：CR 阻断项（正确性、安全、合规）与建议项（可读性、一致性）分级清单。

---

### 前端专项（08）：前端项目必填，其他项目省略

`08_frontend/` 对应白皮书 RepoWiki 中最有价值的前端专属内容：

- **routes.md**：路由表、页面层级、权限守卫逻辑、关键导航路径。AI 在 `writing-plans` 阶段读取，生成含真实路由的实施计划。
- **components.md**：核心共享组件的 Props/事件/插槽约定。AI 在生成组件调用代码时对照此文件，避免接口不一致。
- **state.md**：Store 模块划分、数据流向、副作用边界。AI 在涉及状态的功能实施前读取，避免跨 Store 越界。

这三个文件**无法从代码自动生成**——Props 类型可以扫描，但「为什么这样设计」「这个参数的业务语义是什么」只有人知道。

---

### 业务层（09）：最稳定，也最无法替代

`09_business/` 是整个知识库中唯一与代码实现完全脱钩的部分：

- **domain-concepts.md**：领域术语表（「订单」「结算」「工单」在本系统中的精确定义）。
- **core-processes.md**：核心业务流程的全景描述（用户侧视角，解释「为何如此设计」，而不是「代码如何实现」）。

这两个文件一旦写好，改动频率极低；但一旦缺失，AI 在涉及业务逻辑的功能实施中会系统性地猜测，产生看起来正确却偏离真实业务约定的输出。

---

## 四、维护责任矩阵

| 事件 | 执行者 | 动作 | 涉及区域 |
|------|--------|------|---------|
| 新项目启动 | AI | 运行 `initialize-knowledge-base` | 00–06、META、RUNBOOK |
| 新项目启动 | Owner | 填写 07、08、09 | 07–09 |
| 功能开发前 | AI | `explore-repository` 读取 KB | 只读全部 |
| 功能实施中 | AI | 遇到 gap → `refine-knowledge-base` | 00–06 |
| 功能合并后 | AI | `archive-knowledge-base` | 06、01、03、META |
| 功能合并后 | 开发者 | 同步新路由/组件/Store/业务规则 | 08、09 |
| 规范变更 | Owner | 直接编辑 | 07 |
| 架构调整 | Owner | 更新 08 + 触发 `refine-knowledge-base` | 08 + 00–06 |

---

## 五、与现有 skill 的兼容说明

### knowledge-base skill 体系

**无需修改任何 skill**。现有 skill 只写 `00_overview/` 至 `06_features/`，天然不触碰 `07_standards/` 至 `09_business/`。唯一需要更新的是 `RUNBOOK-template.md`，在导航区增加指向 `07–09` 的链接：

```markdown
### Standards & Business Context
- [Coding Conventions](./07_standards/coding-conventions.md)
- [Performance Baseline](./07_standards/performance-baseline.md)
- [Routes & Pages](./08_frontend/routes.md)          ← 前端项目
- [Domain Concepts](./09_business/domain-concepts.md)
```

### init-ai-standards skill

`init-ai-standards` 初始化时应同步创建 `07_standards/`、`08_frontend/`（前端项目）、`09_business/` 的**占位文件**，内容留空，提示工程师填写——避免 KB 建完后人工区仍是空白。

---

## 六、迁移路径（已有 repowiki/ 的项目）

1. 运行 `initialize-knowledge-base` → 生成 `docs/00–06`
2. 将 `repowiki/02-技术规范/` 内容迁移到 `docs/07_standards/`
3. 将 `repowiki/03-路由与页面结构.md` → `docs/08_frontend/routes.md`
4. 将 `repowiki/04-组件库文档.md` → `docs/08_frontend/components.md`
5. 将 `repowiki/05-状态管理.md` → `docs/08_frontend/state.md`
6. 将 `repowiki/07-业务知识/` → `docs/09_business/`
7. 将 `repowiki/08-测试用例/` 内容并入各 `06_features/<name>.md` 的 `Implementation Notes` 节，或单独保留为 `09_business/test-scenarios.md`
8. 更新 `.cursorrules` 中 RepoWiki 路径引用，指向新 `docs/` 路径
9. 归档或删除 `repowiki/`
