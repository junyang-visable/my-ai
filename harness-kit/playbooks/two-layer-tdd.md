# two-layer-tdd — the two-layer TDD split (implementer unit tests + acceptor E2E)

## When to apply

When working with harness-kit and wondering "given the Evaluator's RED-first,
does the implementer still write tests?"; also for how the implement/accept
roles each own one test layer without breaking role information isolation.

## The practice

1. **Acceptor layer (Evaluator, already present)**: E2E cases RED-first +
   four-level Rubric + assertion lock freezing the smoke set. This layer
   answers "is the whole chain right"; anti-false-reporting via mechanical
   enforcement.
2. **Implementer layer (Implementer, self-discipline)**: for unit-testable
   logic changes (utility functions, state machines, data transforms), write
   the unit test first, run it once to confirm RED (record the failing
   assertion in the task's history.md as red-run evidence), then implement to
   green; for bugfixes start with a failing test reproducing the bug. Pure
   copy/style changes are exempt.
3. The implementer writes **their own unit tests** and still never sees the
   Rubric — no role-isolation violation; what they cannot touch is the smoke
   set (the assertion lock guards it), while their own new unit tests evolve
   with the implementation.
4. Companion spec split: the implementer holds `tasks/<task>/spec.md`
   (approach & boundaries), the Evaluator holds `rubric.md` (acceptance
   criteria) — the two write independently and compare afterwards; mismatch is
   a clarification signal.

## Anti-pattern (don't do this)

- Skipping unit tests because "E2E acceptance exists": accepting pure-logic
  modules via E2E is too heavy, the feedback loop is slow, and the quality
  guardrail idles.
- The implementer editing E2E smoke cases to pass acceptance: the assertion
  lock blocks it (exit 2) — that's an ESCALATED verdict.
- One shared spec for implement and accept: breaks information isolation; the
  Evaluator gets anchored by the implementation's approach.

## Basis

- Source task: `tasks/*` (kit construction, discussed 2026-08; lived under
  workspaces/*/tasks/ before the data-model migration)
- Origin: the kit's research notes "Coding & Testing Harness self-build plan",
  `.harness/rubric/anti-false-reporting.md` (role isolation / RED-first)
- Verified: 2026-08-25
