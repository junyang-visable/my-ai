---
name: slop-linter
description: AI-slop detection for completed requirement development. Use when the user asks to lint or slop-check a finished requirement, branch or PR ("lint 这个需求", "跑一下 slop 检测", "check this branch for slop"), or names a repo for standalone detection. Two layers - deterministic oxlint+anti-slop scan via engine/runner.sh, then agent semantic review against semantic-rules.md - producing a tiered report and verdict, with an optional in-session fix loop after explicit user confirmation.
version: 1.0.0
---

# Slop Linter — post-development slop detection

You are the **detector**. Role isolation: you never judge code you wrote in this
session; you judge from rules + diff + findings only (same discipline as
harness-testing).

## Step 0: locate

Resolve this skill's real directory (symlink-safe):

```bash
AGENT="$(cd "$(dirname "$(readlink -f <this-SKILL.md-path>)")" && pwd)"
```

- Engine: `$AGENT/engine/`（runner.sh · oxlintrc.json · rules · fixtures）
- Semantic rules: `$AGENT/semantic-rules.md`
- Workspace mode only（目标仓库无 .harness install-mode 支持，遇到时说明并仍按直连模式跑）

## Invocation modes

- **Task mode** — 用户点名 harness 任务：repo 从 `<hd>/tasks/<task>/current.md` 解析
  （`<hd>` = harness-data 根，kit 的同级目录；解析不出就问用户，勿猜）。
  findings 与报告写 `<hd>/tasks/<task>/lint-findings.json` 与 `lint-report.md`。
- **Direct mode** — 用户给仓库路径或说"当前仓库"：base 默认 origin 默认分支 merge-base；
  报告呈现于对话，用户指定路径才落文件。

## Order（严格顺序）

1. 解析 repo + base（或用户给的文件集）。先跑第 2 步再看别的。
2. 机械层：
   `bash $AGENT/engine/runner.sh --repo <repo> [--base <base>] --out <findings.json>`
   - oxlint 缺失 → 告知一次性 `cd $AGENT/engine && npm install`，停。
   - 插件加载失败 / 非法 JSON → **显式失败报告**（spec §11：静默降级 = 假阴性；
     插件/版本漂移对照 `engine/anti-slop/VENDORED.md` 的 upstream rev 记录）；
     die 的具体原因走 **stderr**——调用时必须保留并转述 stderr（exit 2 的细节在那里）。
   - oxlint 崩溃/超时 → 保留原始输出与 exit code，agent 判定 escalate（spec §11）。
   - `nothingToLint: true` → 报告 "nothing to lint"，正常终止。
3. 读规则：`semantic-rules.md` 全文（每次运行必读，不跨会话缓存）+
   `<hd>/<alias>/notes.md` 存在 "lint" 段则并入（仓特有规则）。
4. 读 diff 全文：`git -C <repo> diff <base>...HEAD`。
5. 新旧行区分：诊断行号（取 `labels[0].span.line`，spec §13 实测）落在该文件 changedLines 内 →
   计入 verdict（仅 severity=error；机械 warn 级 → warn 档，不计入，spec §9）；
   落在存量行 → advisory（列出、注明"非本次引入"、不阻卡）。
6. 语义审查：逐条 SR-* 与仓特有规则对照**新增/修改行**。每条 finding 必须含
   规则 ID + file:line + 原文引用 + 建议修法；低置信 → warn 档。
7. 写报告（三档表：error / warn / advisory + verdict + 修复循环记录区）。
8. verdict：**clean** = 零 error 档；**needs-fix** = ≥1。needs-fix → 列修复清单，
   问用户"会话内修 / 仅报告"。
9. 修复循环（用户确认后）：
   - 先 autofix：`cd <repo> && $AGENT/engine/node_modules/.bin/oxlint --config
     $AGENT/engine/oxlintrc.json --disable-nested-config --fix <files>`
   - 剩余项逐个手修（小步、最小 diff）。
   - 出口条件（两查都过才算完）：复跑 runner error 档清零 **且** 目标仓自身 lint 通过
     （`HARNESS_LINT_CMD` 取自 `<hd>/<alias>/config.sh`，空则跳过并注明）。
   - 有界：修复轮 ≤3；同一 finding 3 轮不消 → needs_human，出 ESCALATED handoff
     （路径/证据/当前假设/建议下一步）。
   - **不自动 commit**：修完汇总改动，建议 slop 清理单独成 commit，由用户决定。
10. lessons：漏判/误判 → 按 spec §7.1 提议（SR 增改或毕业进 slop-local JS 规则），
    用户确认后写入并单独 commit。
