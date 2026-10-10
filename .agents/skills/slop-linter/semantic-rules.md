---
upstream-rev: 72ed33f
---
# slop-linter 语义规则库（唯一权威源）

格式：`SR-ID | severity | 规则 — 判定要点`。severity：`error`（计入 verdict）/ `advisory`（仅报告）。
种子段（SR-0xx）随上游维护；个人追加从 SR-101 起；显式拒绝的规则移入 rejected 段（tombstone，同步不回塞）。
变更纪律：一律提议-确认后写入，单独成 commit（spec §7.1）。

## 种子段（SR-0xx）

SR-001 | error | 注释只写非显然 WHY — WHAT 复述、任务引用（"for issue#123"）、多段 docstring 均违规；删掉不令读者困惑的注释就该删
SR-002 | error | 无防御性兜底 — 不可能场景的 try/catch、null/undefined 检查、fallback 分支；信任内部契约，边界校验只留系统边界（用户输入、外部 API）
SR-003 | error | 禁过早抽象 — 单实现接口、预防性泛化/DI；三行相似优于提前抽象
SR-004 | error | 禁无需求兼容层 — backward shim、feature flag、re-export 转发、"// removed" 尸体注释
SR-005 | error | 命名业务语义化 — data1/tmp/handler2/res2 类命名违规
SR-006 | error | 禁 emoji 与 AI 腔 — 代码、注释、UI 文案均适用（机械侧对应 slop-local/no-emoji，重复命中以机械层为准）
SR-007 | error | 禁空实现与假文档 — 空函数、描述与实现不符的注释、膨胀注释

## 个人追加段（SR-1xx+）

（空 — 运行时纠正经提议-确认后追加于此）

## rejected

（空 — 格式：`SR-0xx: rejected — 理由`）
