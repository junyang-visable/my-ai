---
name: rules-audit
description: Audit Qoder rules for configuration errors and quality problems — invalid frontmatter, silently-failing glob rules, glob patterns matching no files, 100k character quota and always_on resident cost, plus semantic issues (rule conflicts, duplication with AGENTS.md, vague or low-value rules). Use when the user asks to audit, check, or review their Qoder rules quality (e.g. "检查/审计我的 rules", "rules 有没有问题", "audit my rules"). Explicit invocation only; report-only, never edits rule files.
argument-hint: [project-path] [--user]
---

# Rules Audit

## Overview

Two-layer audit of Qoder rules: a deterministic script (config errors, dead globs, quota) plus your own semantic review (conflicts, duplication, vagueness). Report-only — never edit rule files unless the user explicitly asks for fixes afterward.

## Step 0 — Confirm scope

Scope must be explicitly specified before running: which project path to audit, and whether to include user-level rules (`~/.qoder/rules`). If the user's request already names a project or says 用户级/全局/both, that is the specified scope — proceed without re-asking. Only when genuinely unspecified, list the candidates (current project path; whether `~/.qoder/rules` exists) and ask. Never assume a default scope. Both scopes can be audited in one run.

## Step 1 — Deterministic checks (script)

```bash
node "<this skill's base dir>/scripts/audit_rules.mjs" --base <project-root> --project-rules [--user-rules ~/.qoder/rules]
```

- `--base <project-root>` — required; glob patterns are matched against real files under this root (user-level globs also resolve relative to the current project root).
- `--project-rules` — audit `<base>/.qoder/rules/**/*.md`.
- `--user-rules <dir>` — audit that rules dir (normally `~/.qoder/rules`).
- Node ≥ 18, zero dependencies. Exits 0 even with findings; exit 2 = usage error.
- Run the script; do not read it into context. Carry every ERROR/WARN/INFO line from its output into the final report. When both scopes are audited, tell the user which findings come from which scope.

## Step 2 — Semantic checks (review yourself)

Read every rule file in scope, plus `AGENTS.md` at the project root if present, and judge:

1. **Conflicts** — two rules (or a rule vs `AGENTS.md`) giving opposite instructions on the same topic. On conflict, `.qoder/rules` takes precedence over `AGENTS.md`.
2. **Duplication** — the same instruction restated in several rules, or also present in `AGENTS.md`. Costs tokens twice; recommend consolidating.
3. **Vague rules** — instructions that cannot be objectively checked ("write high-quality code"). Recommend rewriting as decidable statements.
4. **Low-value rules** — restating what the model does by default; suggest removal.
5. **always_on bloat** — use the script's `always_on_chars` stat; every char is paid on every turn. Large resident bodies should move to `glob`/`model_decision` triggers.
6. **glob dead zones** — a glob rule never fires in discussion-only turns (no matching file is read or edited). If a rule must also govern discussion, suggest `model_decision` or `always_on`.

## Report format

In-chat markdown, grouped by severity — Errors / Warnings / Info — then a Stats section (per-scope file counts, quota usage, always_on resident cost). Each finding: file, problem, one concrete fix suggestion. Report only; fixes happen in a separate, explicitly confirmed pass if the user asks.
