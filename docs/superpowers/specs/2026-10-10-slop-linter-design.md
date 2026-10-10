# slop-linter — 需求开发后的 AI-slop 检测 agent 设计

- 日期：2026-10-10
- 状态：draft（待用户 review）
- 来源：brainstorming 会话（architectural path，决策均经用户逐项确认）
- 下游：实现计划（superpowers:writing-plans，spec 获批后启动）

## 1. 背景与问题

AI agent 写码会系统性产出 "slop" 模式：复述代码的注释、为不可能场景写的防御代码、
过早抽象、无需求支撑的兼容层、膨胀命名等。用户过去一年的纠错偏好已大量沉淀在
对话记忆中，但缺少一个**需求开发完成后可显式调用**的检测环节把它们变成可执行的
规则。

现有 harness 的缺口：`harness validate` 只跑目标仓库自身 lint（如 eslint+prettier），
不覆盖 AI slop 模式；harness-testing 是 E2E 验收角色，不管代码质量口味。

技术基座（已核实）：

- **anti-slop**（dmmulroy/anti-slop，MIT）：18 条 opinionated Oxlint JS 插件通用规则
  （+ `oxc/no-accumulating-spread` 合计 19 条显式 entries），
  官方定位为 vendor 分发（拷入自己的仓库，读、改、拥有）。Effect 规则组独立，不适用。
- **oxc/oxlint**：50-100x ESLint；`.vue` 文件 lint 其 `<script>` 块；JS 插件
  （alpha，兼容 ESLint v9 API）；`-c/--config` 接受任意路径配置；jsPlugins 的
  specifier **相对配置文件本身解析**（kit 侧配置可引用 kit 侧插件，目标仓库零侵入的
  依据）；`-f json`（另有 `agent` format）；`--disable-nested-config`；`oxlint [PATH]...`
  接受文件列表。

## 2. 目标 / 非目标

目标：

1. 需求开发完成后，独立会话显式调用，对需求变更集做**双层检测**（确定性机械规则 +
   agent 语义判断），产出报告与 verdict。
2. **目标仓库零侵入**：不装依赖、不改配置、不提交任何文件。
3. 规则体系多层可扩展，且**判定依据的任何变更走提议-确认闸门**。
4. agent 物理独立（`.agents/skills/slop-linter/`），可脱离 harness-kit 被其他
   harness / 开发过程复用，可推广给同事。
5. 检出项经用户确认后可在会话内修复（有界循环）。

非目标见 §14。

## 3. 总体架构

```
独立会话（角色隔离，对齐 harness-testing 模式）
┌────────────────────────────────────────────────────┐
│ Layer 3  SKILL.md —— 编排层（agent 判断）           │
│  任务模式 / 直连模式；读规则 → 读 diff → 新旧行区分   │
│  → 语义审查 → 报告 + verdict → 修复循环 → lessons    │
└──────────────────┬─────────────────────────────────┘
                   │ 消费 findings JSON
┌──────────────────▼─────────────────────────────────┐
│ Layer 1  engine/ —— 确定性核心（零 harness 依赖）   │
│  runner.sh：变更文件集解析 → oxlint 执行 → JSON 产出 │
│  规则宿主：oxlint 原生 + vendored anti-slop +       │
│  slop-local 自定义 JS 插件                          │
└────────────────────────────────────────────────────┘
```

说明：原设计的 Layer 2（`harness lint` CLI 适配器）已删除——engine 独立后，
task→repo 解析由 SKILL.md 指导 agent 读 harness-data 路径约定完成（文本约定，
非代码依赖），harness-kit 引擎与 CLI 零改动（唯一交叉点是 §14 的一行文档提醒）。

**层职责边界**：engine 只做确定性的事（同一输入永远同一输出）；判断、裁决、
修复、lessons 回写全部在 SKILL.md 编排的 agent 侧。

## 4. 目录布局

```
~/Desktop/my-ai/.agents/skills/slop-linter/     ← 真身目录，随 my-ai 入库
├── SKILL.md              编排层：两种调用模式 + 判断流程 + verdict + 修复循环
├── README.md             边界契约（runner 接口、规则宿主、SR 文件格式）
│                         + vendored anti-slop 更新流程 + 推广说明
├── semantic-rules.md     全部自然语言规则（种子 + 追加），唯一权威源
└── engine/               确定性核心，自包含、可整体拷走
    ├── runner.sh         --repo <path> [--base <ref>] [--files <list>] [--out <file>]
    ├── package.json      oxlint + @oxlint/plugins 同版本精确 pin
    ├── oxlintrc.json     机械层唯一调优点
    ├── anti-slop/        vendored src/（README 记 upstream rev；纪律：不修改）
    ├── rules/            slop-local 自定义 JS 插件（毕业规则落点）
    └── fixtures/ + selfcheck.sh
```

部署事实（已核实）：`my-ai/.agents/skills/` 是本工作区技能注册面——非 harness
技能（drawio-roadmap、weekly-report 等）真身直放入库；harness-* 系列是指向
harness-kit 的 symlink。slop-linter 走前者模式。SKILL.md Step 0 用 `readlink -f`
自解析真实路径，为将来 `~/.agents/skills/` symlink 全局调用预留（本期不做）。

## 5. 机械层（engine）

### 5.1 runner.sh 接口

```
runner.sh --repo <path> [--base <ref>] [--files <显式文件列表>] [--out <file>]
```

行为：

1. base 缺省 = 当前分支与 `origin/<default>` 的 merge-base（default 取
   `git symbolic-ref refs/remotes/origin/HEAD`，失败回退 master/main 存在者）。
2. 变更文件集：`git -C <repo> diff --name-only <base>...HEAD`，过滤 oxlint 支持
   的扩展名（`.ts .tsx .js .mjs .cjs .jsx .vue`），排除 ignorePatterns。
   以 HEAD 为准；工作树不干净时在输出 JSON 的 `dirty` 字段注明（不阻断）。
3. 显式 `--files` 传入时跳过 diff 解析（直连模式的窄用法）。
4. 执行：`<engine>/node_modules/.bin/oxlint -c <engine>/oxlintrc.json
   --disable-nested-config -f json <files...>`，cwd = 目标仓库。
5. 产出 JSON（--out 或 stdout）：

```json
{
  "repo": "...", "base": "...", "head": "...", "dirty": false,
  "nothingToLint": false,
  "files": [{ "path": "src/a.ts", "changedLines": [[12,18],[40,41]] }],
  "diagnostics": [ ...oxlint json 原样... ],
  "oxlintExitCode": 1
}
```

`changedLines` 来自 `git diff --unified=0 <base>...HEAD` 的 hunk 解析，供 agent
做新旧行区分（agent 无需自己解析 diff hunk）。

6. exit code：存在 error 级 findings → 非零；空文件集 → 0 且 `nothingToLint: true`。

### 5.2 依赖与版本

`engine/package.json`（private）安装 oxlint 与 `@oxlint/plugins`，**同版本精确 pin**
（anti-slop README 要求两包精确同版、升级一起动）。一次性
`cd <engine> && npm install`；本机 registry 限速，安装一次长期使用。

### 5.3 oxlintrc.json 初始内容

- `ignorePatterns`：`.agent/ .agents/ .claude/ .codex/ .cursor/ .gemini/` 等
  agent 工具目录（参考 anti-slop README，勿广泛忽略所有点目录）。
- `jsPlugins`：`anti-slop`（`./anti-slop/index.ts`）+ `slop-local`（`./rules/index.ts`）。
- `rules`：anti-slop 18 条通用规则全 `error` + `oxc/no-accumulating-spread`
  （合计 19 条显式 entries）+ oxlint correctness 默认预设。Effect 规则组不注册。
- 此文件是机械层唯一调优点（开/关/调级），属个人判定依据，更新不整替（§12）。

## 6. 规则体系

| 规则 | 位置 | 执行者 | 性质 |
|---|---|---|---|
| oxlint 原生 + `oxc/no-accumulating-spread` | `engine/oxlintrc.json` | runner.sh | 确定 |
| anti-slop 18 条通用规则（+ `oxc/no-accumulating-spread` 合计 19 条显式 entries） | `engine/anti-slop/` + oxlintrc 注册 | runner.sh | 确定 |
| 自定义 JS 规则（slop-local） | `engine/rules/` | runner.sh | 确定（来源是判断沉淀） |
| 自然语言规则（SR-*） | `semantic-rules.md` | agent 判断层 | 提议-确认 |
| 仓特有规则 | `<hd>/<alias>/notes.md` lint 段 | agent 判断层 | 提议-确认 |

**毕业路径**：自然语言规则反复命中且模式可 AST 化 → 写成 slop-local JS 规则
（确定性升级）；JS 规则误报多 → oxlintrc.json 调级或关闭。规则在两层间流动。

**原生规则的 `.vue` 兜底**：oxlint 原生规则对 `.vue` script 块天然覆盖；jsPlugins
规则是否覆盖 `.vue` 待 spike（§13），不覆盖则 `.vue` 退回原生规则 + 语义层覆盖。

## 7. semantic-rules.md 格式

```markdown
---
upstream-rev: <本仓 git rev（种子写入时）>
---
## 种子段（SR-0xx，上游维护；同步时新增/修订）
SR-001 | error | 注释只写非显然 WHY — WHAT 复述/任务引用("for issue#123")/多段 docstring 均违规
SR-002 | error | 无防御性兜底 — 不可能场景的 try/catch、null 检查、fallback；边界校验只留系统边界
SR-003 | error | 禁过早抽象 — 单实现接口、预防性泛化；三行相似优于提前抽象
SR-004 | error | 禁无需求兼容层 — backward shim / feature flag / re-export 转发
SR-005 | error | 命名业务语义化 — data1/tmp/handler2 类命名违规
SR-006 | error | 禁 emoji 与 AI 腔 — 代码、注释、UI 文案均适用
SR-007 | error | 禁空实现与假文档 — 空函数、描述与实现不符的注释、膨胀注释
## 个人追加段（SR-1xx+，上游命名空间永不写入）
## rejected
SR-0xx: rejected — <理由>（tombstone；同步遇上游修订不回塞）
```

- severity：`error`（计入 verdict）/ `advisory`（仅报告）。
- 种子来源（按权重）：用户历史纠错（最主要）、anti-slop 哲学的语义侧延伸、
  社区共识 AI-slop 模式。实现时写入，用户 review 后拥有，可改可删。
- **单一权威源**：SKILL.md 零规则内容；全局自然语言规则只在此文件。
  仓特有规则在 notes.md lint 段（本地知识，不随 agent 分发）。

### 7.1 升级机制（提议-确认制）

三条通道，全部收敛到本文件：

1. 运行时纠正回写（主通道）：漏判 → 新增规则或 sharpen 措辞；误判 → 修边界
   （加例外、降 severity、标 advisory）；高频且可 AST 化 → 毕业进 `engine/rules/`。
2. 跨对话沉淀：任何开发会话中的新 slop 纠正，事后汇入。
3. 闸门：agent 提议（ID + severity + 一行 why）→ 用户确认 → 写入，
   单独成 commit（git 历史 = 升级日志）。

不存在：后台自动变更、upstream 自动同步、种子被任何机制覆盖。

## 8. 语义层与技能流程（SKILL.md）

Step 0 自定位：`readlink -f` 解析本 SKILL.md 真实路径 → agent 根 =
`<slop-linter>/`；engine = `<slop-linter>/engine/`。

**两种调用模式**：

- 任务模式：任务名 → 读 `<hd>/tasks/<task>/current.md` 解析 repo（harness-data
  路径约定，文本依赖）；报告与 findings 落 `<hd>/tasks/<task>/`。
- 直连模式：用户给仓库路径（无 harness 任务）；base 默认 merge-base；
  报告落 stdout 或用户指定路径。

仅支持 workspace mode（install mode 留升级路径，SKILL.md 写明）。

**Order（严格顺序）**：

1. 定位任务/仓库；变更文件集为空 → 终止（nothing to lint）。
2. 跑机械层：`runner.sh --repo ... --base ... --out <task>/lint-findings.json`。
3. 读规则：`semantic-rules.md` + `<hd>/<alias>/notes.md` lint 段。
4. 读 diff 全文（行范围表已在 findings JSON）。
5. 新旧行区分：机械违规落在新/改行 → 计入 verdict；落存量行 → advisory。
6. 语义审查：逐条规则对照 diff，只审本次新增/修改行；findings 必须带
   规则 ID + file:line + 证据引用 + 建议修法。
7. 写报告 + verdict。
8. needs-fix → 展示修复清单，问用户：修 / 仅报告。
9. 修复循环（用户确认后，见 §10）。
10. lessons 写回（漏判/误判 → §7.1 通道，走提议-确认）。

## 9. Verdict 与报告

- **clean** = 零 error 级（机械 error·新行 + 语义 SR 命中·非 advisory）。
- **needs-fix** = ≥1 error 级。
- 报告三档：error（计入）/ warn（机械 warn 级、语义低置信）/ advisory（存量行命中）。

报告落 `<hd>/tasks/<task>/lint-report.md`（任务模式）——process state 归任务池，
对齐 harness 既有划分（spec/plan 是项目产物进仓、状态进池）：

```markdown
# Lint Report — <task>
verdict: clean | needs-fix
repo/base/files 数
## 机械层 findings
| severity | rule | file:line | 新/存量 | 建议修法 |
## 语义层 findings
| severity | 规则 ID | file:line | 证据 | 建议修法 |
## advisory（存量命中，不计 verdict）
## 修复循环记录（轮次/已消/剩余）
```

## 10. 修复循环（bounded，可停）

- 先 `oxlint --fix`（可 autofix 项，如 require-readable-spacing）。
- 剩余项 agent 逐项修（Edit、小步、最小 diff）。
- **出口条件**：复扫 error 清零 **且** 目标仓自身 lint（`HARNESS_LINT_CMD`）通过
  ——防 autofix 与仓库 prettier/eslint 冲突。
- 有界：修复轮 ≤3；同一 finding 3 轮不消 → needs_human（ESCALATED handoff：
  路径/证据/当前假设/建议下一步）。
- 修完不自动 commit：提示用户 review；slop 清理建议单独成 commit
  （性质分离，对齐 commit 卫生 playbook）。

## 11. 错误处理

- oxlint 二进制缺失 → 提示一次性 `cd <engine> && npm install`。
- JS 插件加载失败（alpha API 漂移 / 版本不匹配）→ **显式失败**并指向
  anti-slop README 的 upstream rev 记录；绝不静默降级。检测工具静默降级 =
  假阴性。（与用户"缺省静默回退"偏好的边界：功能缺失可静默回退，
  检测失效必须显式失败——判定工具的可信度优先。）
- 变更文件集为空 → 正常退出，非错误。
- oxlint 崩溃/超时 → 保留原始输出与 exit code，agent 判定 escalate。

## 12. 更新与分发

### 12.1 两份更新合同

分界标准：**是否承载个人判定依据**（不是目录位置）。

- **合同 A（全域、无个人状态，可整替）**：`runner.sh`、`fixtures/`、vendored
  `anti-slop/`（纪律：不修改 vendored 文件，个人 JS 规则住 `rules/` 正是为保住
  此性质）、`package.json`（版本 pin 随升级事件同步 bump）。整替后必跑
  `selfcheck.sh` 验证。
- **合同 B（个人判定依据，永不整替）**：`engine/rules/`、`oxlintrc.json` 调级、
  `semantic-rules.md`。只接受条目级整合 + 提议-确认闸门。

对话/运行期间 engine 只读（判定可复现的前提）；engine 变更只发生在显式升级事件，
唯一例外是毕业规则写入 `engine/rules/`（合同 B）。

### 12.2 vendored anti-slop 更新流程（写入 README，升级事件时由 agent 会话执行）

继承 anti-slop update skill 六律：新源单独 staging；三方合并（基准 = 记录的
upstream rev）；保留本地定制（若有）；冲突问询；记录 provenance；绝不
force-replace。适配我们的目录布局，不直接安装运行其 skill。

### 12.3 多人同步（v1 只预埋结构，机制待真实需求落地）

预埋三件：SR-ID 分段（0xx 上游 / 1xx+ 个人）、`upstream-rev` frontmatter、
rejected tombstone 段。

同步（将来落地）= 规则级提议式合并：拉上游、对比 `upstream-rev` 之后的规则
diff → 逐条 adopt/reject（reject 写 tombstone）→ 本地改过的种子冲突人工裁决；
反向流动 = PR 回上游种子段。分发 = git fork/clone。结构性保证：个人段命名空间
上游永不写入 → 整文件覆盖不可能发生。规则 ID 使合并粒度为条目级，比 anti-slop
的源码文本三方合并更稳；且因语义规则是判定依据，合并闸门比 anti-slop 的自动
三方合并更严（必须本人批准）。

### 12.4 推广路径

拷 `.agents/skills/slop-linter/` 整目录即 standalone（engine 自含依赖声明）；
`~/.agents/skills/` symlink 可获得跨工作区全局调用（本期不做）；其他 harness
只对接 `runner.sh` 窄接口，SKILL.md 是编排参考实现。同事拿到后
`semantic-rules.md` 对他们又是一份种子，照自己审美改（vendor 模式同构传播）。

## 13. Spike 验证点（实现计划第一个任务）

| 待验证 | 失败时的降级 | 实测结论 |
|---|---|---|
| `.oxlintrc.json`（json 配置）能加载 `./anti-slop/index.ts` 的 TS 插件 | 换 `oxlint.config.ts`（TS 配置，jiti 运行） | 实测：通过，未用降级。spike 样本（oxlint 1.78.0 + @oxlint/plugins 1.78.0）从 json 配置直接加载 TS 插件，`sloppy.ts` 报 15 条 anti-slop 诊断，含全部预期 code；stderr 仅有 Node 的 `MODULE_TYPELESS_PACKAGE_JSON` 警告（无碍 stdout JSON） |
| jsPlugins 规则覆盖 `.vue` script 块 | `.vue` 退回 oxlint 原生规则 + 语义层覆盖，`.ts` 保持全套 | 实测：覆盖，未用降级。`sloppy.vue` script 块内 `anti-slop(no-runtime-typeof)` 与 `require-readable-spacing` 均触发，行号为 .vue 原文件坐标（非 script 内容相对）（§6 兜底不生效，Task 2 的 .vue 断言走"覆盖"分支） |
| `-f json` schema 稳定可解析 | 换 `-f agent` format | 实测：可解析，未用降级。但顶层是包装对象 `{diagnostics, number_of_files, number_of_rules, threads_count, start_time}` 而非裸数组——jq 提取必须走 `.diagnostics[]`（裸 `.[]` 会报错）；真实字段名见下方记录 |
| `--disable-nested-config` + 显式 `-c` 组合行为符合预期 | 调整为仅显式文件列表传参 | 实测：符合，未用降级。cwd 放 `{"rules":{"anti-slop/no-runtime-typeof":"off"}}` 的 `.oxlintrc.json` 后仍显式 `--config` 运行：该规则仍报 1 条、总诊断 15 条、启用规则 115 条，与无本地配置时完全一致——本地 off 未泄漏，kit 配置完全接管 |

JSON 诊断真实字段（Task 2 的 jq 提取路径依据，修正本 spec 此前的假定）：
`-f json` 输出为包装对象 `{ "diagnostics": [...], "number_of_files": N, "number_of_rules": N, "threads_count": N, "start_time": F }`；
诊断对象字段为 `message` / `code` / `severity` / `filename` / `labels[].span.{offset, length, line, column}`。
与假定的差异：① `code` 用括号形式 `anti-slop(no-runtime-typeof)`（非 `anti-slop/no-runtime-typeof`），jq 匹配与 spec 文中规则 ID 写法需按此转换；② 无 `location.start.line`，行号取 `labels[0].span.line`、列取 `labels[0].span.column`；③ 零违规时输出为 `{ "diagnostics": [], ... }`（包装对象内空数组，既非空串也非裸 `[]`），此时 exit code 0，有 error 级诊断时 exit code 1。

## 14. 边界与非目标

- 不动 `harness validate`、不内嵌 dev 循环；harness-kit 唯一改动 =
  harness-dev SKILL.md §8 wrap-up 提醒列表加一行（lint 检测可在独立会话跑
  slop-linter）。
- 不做：CI 集成、install mode、per-repo 机械规则 overlay（升级路径注明）、
  Effect 规则、anti-slop 上游自动同步、`~/.agents` 全局 symlink、多人同步的
  合并命令本体（只预埋 §12.3 三件）。

## 15. 测试与验收

- `selfcheck.sh`：fixtures 含 `.ts` 违规样本、`.vue` 违规样本、干净样本各一，
  断言预期 findings（对齐 `harness validate selfcheck` 先例）；规则调整、插件
  升级、合同 A 整替后必跑。`.vue` 的期望值随 spike 结果定。
- 真实任务验收：第一个真实需求全流程跑一遍——任务模式调用、报告三档、
  verdict、修复循环（含出口条件两查）、lessons 回写；直连模式至少跑一次。
- 语义层无机械断言，靠真实任务验收。

## 16. 实现顺序概要（供 writing-plans 参考）

1. Spike 四项验证（§13），结论回写本 spec 的 spike 表。
2. engine 骨架：package.json pin → vendored anti-slop 拷入（记 upstream rev）→
   oxlintrc.json → runner.sh → fixtures + selfcheck。
3. `semantic-rules.md` 种子 7 条写入（用户 review）。
4. SKILL.md（两种模式 + Order + verdict + 修复循环 + lessons）。
5. README（边界契约 + 更新流程 + 推广）。
6. harness-dev SKILL.md §8 加一行提醒。
7. 真实任务验收（§15）。
