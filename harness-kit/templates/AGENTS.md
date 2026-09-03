# AGENTS.md — agent contract layer for <project>

> This is the first — and the only — project manual that lives permanently in
> an AI agent's context. Principle: **index and red lines only, ~100 lines /
> ~2.5K tokens max**. Details sink into `docs/` and `.harness/` and load on
> demand, never in here. Past ~32K tokens of context, model accuracy drops
> measurably — the shorter this file, the better.

## 30-second overview

- What this is: <one line>
- Stack: <language / framework / package manager>
- How to run: `<install>` → `<dev>`

## The single validation entry (remember this)

Before claiming any change complete, run this; green means done:

```bash
bash .harness/feedback/validate.sh
```

- It composes lint → typecheck → arch → build → test and reports by gate level.
- A blocking failure means not done. **Never** force green by deleting
  assertions / changing test expectations / adding `@ts-ignore`.
- When claiming "done", attach evidence per `.harness/rubric/evidence-template.md`.

## Red lines (blocking; validate will catch violations)

1. The domain layer must not depend on the infrastructure layer; cross-layer
   access goes through interface inversion (rules in `.harness/feedback/lint-arch.sh`).
2. `build` cannot be skipped; `lint` zero warnings/errors; tests all green.
3. Smoke tests are protected by the assertion lock; changes need
   `// @lock-bypass` + a commit message explaining why, leaving an audit trail.
4. <add per project: no direct production DB access / no committed secrets / must go through gateway …>

## How much process a change needs

- **Full flow (spec/plan when the harness skills are present)**: more than 3
  files, async/concurrent state machines, external-system integration.
- **Direct patch**: single-file bugfix, log lines, copy tweaks — still run
  validate before claiming done.
- Pure type / docs / test changes may skip visual verification but still pass validate.

## Knowledge to load on demand (never all at once)

- Architecture & module boundaries → `docs/ARCHITECTURE.md`
- Local dev / debugging / env vars → `docs/DEVELOPMENT.md`
- E2E case context (page entries / test accounts / stable selectors) → `.harness/context/testing/e2e-context.md`
- Four-level acceptance Rubric → `.harness/rubric/rubric-template.md`
- Anti-false-reporting trio → `.harness/rubric/anti-false-reporting.md`

## The loop layer (for multi-step tasks)

A requirement's spec/plan are project artifacts at `docs/changes/<task>/`
(committed with the feature branch). Its process state lives under
`.harness/tasks/<task>/`: `current.md` (stage + single next step), `result.md`
(valid conclusions + residual risks), `history.md` (append-only), `evidence/`
(screenshots / reports). When resuming in a new session, read `current.md` first.

## Minimal MCP / tool set

Connect only the MCP servers the current task needs. One server with 20–30
tools costs ~4–6K tokens; five servers ≈ 25K tokens (12.5% of a 200K window)
and sit there every turn. Turn off what you don't use.
