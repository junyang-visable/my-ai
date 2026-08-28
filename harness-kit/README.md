# harness-kit

一套**可复用、不限栈**的编排层脚手架，把「Coding Harness + Testing Harness（E2E 优先）」
接入任意仓库。它不是自研引擎，而是在现有 agent CLI（Qoder / Claude Code）之上，用
**契约 + 命令 + 钩子 + 上下文约定 + 机械化验证**把「模型能力 × 环境能力」里的环境这一半补齐。

> 配套调研见 Obsidian 笔记《Coding 与 Testing Harness 自建方案》。本 kit 实现其中 P0–P2。
>
> 定位：**个人开发 harness 工具集**。kit 随本仓库（my-ai）走，任意目标仓库零安装即可被驱动；
> 引擎、任务状态与经验都沉淀在本仓库；技能经 `./harness link` 以相对软链接入，clone 后即用。

## 五层结构

| 层       | 作用                    | 本 kit 对应                                                                                                     |
| -------- | ----------------------- | --------------------------------------------------------------------------------------------------------------- |
| 契约层   | 30 秒讲清边界，常驻且短 | `templates/AGENTS.md`（~100 行，只做索引与红线）                                                                |
| 上下文层 | 按需加载的知识          | `templates/docs/`、`.harness/context/`                                                                          |
| 工具层   | 可复用技能/命令/钩子    | `skills/`、`commands/`（agent 通用 markdown）、`.harness/hooks/`                                                |
| 验证层   | 机械化执法，不靠提示词  | `.harness/feedback/`（validate / lint-arch / lock-tests / collect-evidence）                                    |
| 循环层   | 状态与续跑              | `tasks/<需求>/{spec,plan,current,result,history}.md + evidence/`（kit 一级维度；spec=边界契约，plan=可验证任务分解） |

## 快速开始（workspace 模式：在 kit 所在仓库直接驱动任意仓库，目标仓库零安装）

```bash
# 0) 一次性：把 kit 技能软链进本仓库的技能目录（相对软链，clone 后无需重跑）
./harness link

# 1) 注册一个仓库，生成它的专属配置 + 经验笔记 + E2E 上下文
./harness add my-app /path/to/your-repo

# 2) 填这个仓库的命令（按栈）
$EDITOR workspaces/my-app.conf.sh    # HARNESS_LINT_CMD / TEST_CMD / BUILD_CMD / E2E_CMD ...

# 3) 先验证护栏本身，再跑全套
./harness validate selfcheck
./harness validate
```

日常开发**优先在本仓库会话里直接调技能**，说人话即可：

> “用 harness-dev 给 my-app 加一个 XX 功能” / “harness-dev，切到 another-repo 继续 XX 任务”

技能会自己定位 kit、判定开发模式（**标准=默认全流程**：澄清→设计文档→拆分→编码，
支持多应用一份设计文档；**极简=显式切换**：跳过设计直接定位改码）、确认活跃仓库、
路由到专职技能、进编码循环、收尾沉淀经验；
实现完成后另开会话说“用 harness-testing 验收 XX”（角色信息隔离）。
注意：目标仓库需已加入 Qoder 工作区，否则写文件会被沙箱拦。

### 技能家族（6 个，`./harness link` 一次接线）

| 技能            | 角色                                                      | 何时用           |
| --------------- | --------------------------------------------------------- | ---------------- |
| harness-dev     | 总控/路由 + workspace 管理 + 双模式判定（标准默认 / 极简显式） | 跨仓库开发入口   |
| harness-spec    | 澄清 → spec.md（confirmed gate，可路由 grill 类技能）     | 新需求、需求模糊 |
| harness-plan    | spec → plan.md（每步验证命令+预期输出，superpowers 风格） | spec 确认后      |
| harness-coding  | 实现者：TDD + validate + 逐 Step 勾 plan                  | 编码             |
| harness-testing | 验收者：独立会话，Rubric+RED-first+断言锁                 | 验收             |
| harness-change  | 需求变更：spec 降 draft、plan 标记、重新确认              | 需求变了         |

流程（标准模式，默认）：模糊需求 → spec（澄清+确认；多应用覆盖全部应用）→ plan
（可验证分解，多应用按应用分组）→ coding（TDD+门禁，逐应用执行）→ testing
（独立验收）；需求变更随时走 change 把 spec 打回 draft 重新确认。
极简模式（对 harness-dev 显式说"极简/直接改"）：建轻任务 → 定位改码 → validate，
跳过设计与计划。开工时各技能都会先跑 `./harness brief` 把仓库经验带进上下文。

### 增强技能路由（可选，本地配置）

harness 各技能在特定阶段（澄清、方案、诊断……）可以调用环境里已有的通用技能来增强自己
（如 Qoder 里的 `grilling` 逼问、`design-an-interface` 并行发散）。映射关系写在 kit 根的
`skill-routes.local.yaml`——本地个人配置，已 gitignore，不入库；格式与说明见
`templates/skill-routes.yaml`：

```yaml
harness-spec:
  澄清追问: grilling
  方案发散: design-an-interface
```

规则：无配置、或配置的技能不在**当前会话可用技能清单**里 → 静默走默认逻辑，不报错、
不打断。可用性以会话注入的清单为准（文件在 ≠ 会话里有）；换环境只改这份本地文件，
不动技能本体。

命令行操作也都作用于当前活跃仓库：

```bash
./harness list                      # 看注册了哪些仓库，* 是当前活跃
./harness use another-repo          # 切换活跃仓库
./harness doctor                    # 体检：命令是否配置、冒烟集、断言锁基线
./harness validate --strict         # 三级门禁全套（阻断/警告/提示）
./harness lock update               # 冒烟集稳定后记基线；verify 校验是否被篡改
./harness evidence 需求名 api       # 失败后收集证据，产出下一轮修复的 prompt
./harness task new 需求名           # 建循环层任务目录（current/result/history/evidence）
./harness context                   # 打印契约层文本，贴进 agent 会话开场
./harness brief <关键词>            # 开工包：契约 + 仓库 notes + 命中 playbooks + 任务列表
```

每仓库的配置、断言锁基线、经验笔记在 `workspaces/<alias>/` 下互不干扰；
任务与证据是 kit 一级维度，统一在 `tasks/<需求名>/`（不分单应用/跨应用）。

## 经验沉淀（工具集的核心价值）

| 层         | 落点                                           | 放什么                                               |
| ---------- | ---------------------------------------------- | ---------------------------------------------------- |
| 仓库专属   | `workspaces/<alias>/notes.md`                  | 该仓库的栈、命令实测、坑与约定（add 时生成）         |
| 跨仓库通用 | `playbooks/<主题>.md`                          | 换个仓库仍成立的方法论，一主题一文件，可回溯来源任务 |
| 任务过程   | `tasks/<需求名>/history.md`                    | 只追加的过程记录                                     |

技能（harness-dev / harness-coding / harness-testing）收尾都会回写这三层。
与 agent 内置 memory 的分工：memory 按会话项目隔离、开发其他仓库时读不到；
本库是纯文件、进 git、跟着仓库走——这正是把经验放在这里的原因。

### 可选：install 模式

如果你希望某个仓库自带 harness（agent 进仓库即读到 AGENTS.md），也可 `./install.sh <repo>`。
两种模式可共存；workspace 模式不在目标仓库写任何文件。命令落到 `.qoder/commands/`
（Claude Code 复制到 `.claude/commands/`，文件通用）；post-edit 钩子需在 CLI 的 hook
配置里接 `bash .harness/hooks/post-edit.sh <file>`。

## 覆盖范围（P0–P2）

- **P0**：契约层 `AGENTS.md`；`validate.sh` 合成 lint→typecheck→arch→build→test 并分三级门禁；
  `selfcheck` 故意造违规确认护栏不是纸糊的。
- **P1**：`post-edit.sh` 编辑后增量快检 + 输出截断；`evidence-template.md` 完成证据模板。
- **P2**：E2E 用例上下文库、四级 Rubric、防谎报三件套、断言锁 `lock-tests.py`、
  失败证据自动收集 `collect-evidence.sh`。

## 不限栈怎么做到的

所有脚本只读 `.harness/config.sh` 里的命令变量；留空的阶段自动跳过。换栈只改 config，
不动引擎。skill 与命令均为 agent 通用 markdown（Qoder / Claude Code 都读 SKILL.md），
引擎本身是纯 shell + markdown。

## 目录

```
harness-kit/
├── harness                    workspace 模式控制台（add/use/link/validate/lock/evidence/task/...）
├── tasks/                     任务一级维度：<需求名>/{spec,plan,current,result,history}.md + evidence/（gitignore）
├── workspaces/                每仓库一份：conf.sh 配置 + notes.md 经验 + context/ + 断言锁基线
├── install.sh                 可选：把 harness 装进仓库（引擎软链 / 配置拷贝）
├── skill-routes.local.yaml      本地增强技能路由（gitignore；格式模板见 templates/skill-routes.yaml）
├── playbooks/                 跨仓库通用经验库（一主题一文件，可回溯来源任务）
├── templates/                 契约层与 docs 模板
│   ├── AGENTS.md
│   ├── skill-routes.yaml
│   └── docs/{ARCHITECTURE,DEVELOPMENT}.md
├── .harness/
│   ├── config.sh              默认接线点（workspace 模式下被 workspaces/*.conf.sh 覆盖）
│   ├── feedback/              validate / lint-arch / lock-tests / collect-evidence
│   ├── hooks/post-edit.sh     编辑后增量快检
│   ├── context/testing/       E2E 用例上下文库模板
│   ├── rubric/                四级 Rubric + 防谎报三件套 + 完成证据模板
│   └── tasks/_template/       循环层状态模板
├── skills/                    6 个技能（agent 通用 SKILL.md；link 相对软链到 .agents/skills/）
└── commands/                  /harness-validate 等斜杠命令（agent 通用 markdown）
```

## 边界

双模式就是负担出口：标准模式（默认）全流程不因任务小而打折；琐碎改动
（单文件 bugfix / 加日志 / 改文案）对 harness-dev **显式说"极简模式"**跳过设计直接改，
但建分支与 validate 保底不豁免。门禁分级（阻断/警告/提示）就是为了避免
「所有检查都阻断」引发的绕过冲动。
