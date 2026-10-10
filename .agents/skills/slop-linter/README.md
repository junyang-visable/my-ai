# slop-linter

需求开发完成后的 AI-slop 检测 agent：确定性机械层（oxlint + anti-slop + slop-local）
+ agent 语义层（semantic-rules.md）。设计 spec 见
`docs/superpowers/specs/2026-10-10-slop-linter-design.md`。

## 边界契约

- **engine/runner.sh**：`--repo <path> [--base <ref>] [--files <p1,p2>] [--out <file>]`
  → findings JSON（files+changedLines+diagnostics+oxlintExitCode）。
  exit 0 clean/empty · 1 error 档 · 2 用法/环境失败。对目标仓库只读。
- **规则宿主**：机械层全部在 engine（oxlintrc.json 唯一调优点）；语义层唯一源是
  semantic-rules.md（格式：`SR-ID | severity | 规则 — 判定要点`，含种子段/个人段/
  rejected 段，frontmatter 记 upstream-rev）。
- **零仓库侵入**：目标仓库不装依赖、不改配置、不提交文件；唯一写操作是修复循环
  且须用户显式确认。
- **自检**：`bash engine/selfcheck.sh` —— 规则调整、插件升级、engine 整替后必跑。

## 更新（两份合同，spec §12.1）

- **可整替（全域无个人状态）**：runner.sh、fixtures/、vendored anti-slop/、
  package.json 的版本 pin。整替后跑 selfcheck。
- **永不整替（个人判定依据）**：engine/rules/、oxlintrc.json 调级、
  semantic-rules.md。只接受条目级整合 + 提议-确认。

### vendored anti-slop 更新流程（六律，agent 会话执行）

1. 新源 clone 到临时目录，**单独 staging**，不直接覆盖。
2. 三方合并，基准 = `anti-slop/VENDORED.md` 记录的 revision。
3. 本地定制保留（我们的纪律是不改 vendored，此项通常为空）。
4. 冲突 → 问询用户，不自动裁决。
5. 更新后回写 VENDORED.md 的 revision 与日期。
6. 绝不 force-replace；更新后 selfcheck 必须绿。

## 推广 / 接入

- **拷贝整个 `.agents/skills/slop-linter/` 目录**即 standalone：`cd engine && npm install`
  一次即活（package.json 已精确 pin）。
- **接入自己的 harness/流程**：只对接 runner.sh 窄接口；本仓 SKILL.md 是编排参考实现。
- **同事首次接入**：拷目录后把 semantic-rules.md 的 `upstream-rev` 改成你拷贝时的
  本仓 rev；种子规则照你的审美改（vendor 哲学：拷进来就是你的）。
- **多人规则同步**（将来落地）：拉上游 → 对比 upstream-rev 之后的规则 diff → 逐条
  adopt/reject（reject 写 rejected 段）→ 本地改过的种子冲突人工裁决。个人段（SR-1xx+）
  上游命名空间永不写入——结构性保证整文件覆盖不可能发生。
