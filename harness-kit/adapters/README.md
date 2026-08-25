# 适配层说明

同一套 `.harness/` 骨架（validate.sh / lock-tests.py / 钩子 / 模板）是**纯 shell + markdown，
CLI 无关**。这里只放两家 CLI 各自的接线方式。

## 先选工作模式

- **workspace 模式（默认，仓库零安装）**：在 kit 目录跑 `./harness link` 接好技能后，
  在工具集仓库（my-ai）会话里直接调 harness-dev / harness-coding / harness-testing
  驱动任意仓库；命令行则用 `./harness add/use/validate ...`。会话开场也可贴
  `./harness context` 的输出，不强制在仓库放文件。
- **install 模式**：`install.sh` 按所选 CLI 把命令/钩子/技能接进目标仓库，适合希望
  agent 一进仓库就自动读到 `AGENTS.md` 的场景。两种模式的命令对照见各 SKILL.md 的
  「第 0 步：定位」表格。

## Qoder / QoderWork

- **技能**：`adapters/qoder/skills/{harness-dev,harness-coding,harness-testing}`。
  推荐用 kit 目录的 `./harness link` 软链到工具集仓库的 `.agents/skills/`
  （个人工具集跟仓库走，换机 clone 后重跑一次 link 即恢复）；也可手动软链到
  `~/.qoderwork/skills/` 全局生效。harness-dev 是跨仓库开发总控入口；
  coding/testing 两个角色对应防谎报的角色信息隔离，均已适配双模式。
- **命令**：`adapters/qoder/commands/*.md` → 项目内命令目录，触发 `/harness-validate`、`/harness-verify`。
- **钩子**：Qoder 侧在项目 hook 配置里，让编辑类工具后执行
  `bash .harness/hooks/post-edit.sh <file>`。

## Claude Code

- **命令**：`adapters/claude-code/commands/*.md` → 目标仓库 `.claude/commands/`。
- **钩子**：把 `adapters/claude-code/settings.hooks.json` 的 `hooks` 段合并进
  目标仓库 `.claude/settings.json`（PostToolUse 匹配 Edit|Write|MultiEdit，
  跑 `bash .harness/hooks/post-edit.sh`，stdin 收 tool_input.file_path）。
- **契约层**：`AGENTS.md` 即可；如需 Claude 专用指针，加一个 `CLAUDE.md` 内容为
  `See @AGENTS.md`。

## 两家共用的心智模型

- 契约层（AGENTS.md）常驻且短 → 上下文层（docs / context）按需 → 工具层（skills/commands/hooks）
  → 验证层（validate/lock）机械执法 → 循环层（tasks/*）存状态。
- 实现者与验收者是**两个不共享上下文的角色**，这是防谎报的地基。
