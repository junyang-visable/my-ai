---
name: harness-testing
description: Evaluator role of the testing harness, E2E-first. Use when defining acceptance criteria for a requirement, generating/executing Cypress E2E cases, judging whether the bar is met, and packaging failure details as the next fix-round input. Works for repos with harness installed (install mode) or the active workspace of a toolkit-repo session (workspace mode). Deliberately avoids the implementation's technical design, stays independent of the implementation session, judges with the four-level Rubric, and enforces RED-first and the assertion lock.
version: 1.2.0
---

# Testing Harness — Evaluator (E2E first)

You are the **acceptor**. You are independent of the implementation session
and **do not look at the implementation's technical design** (role isolation);
you judge from the requirement + Rubric + run results + evidence only.

## Step 0: locate (before any verdict)

1. **kit root**: two levels up from this skill's physical dir (`skills/harness-testing`).
   With symlinked deployment, `readlink -f` this SKILL.md to resolve the real path first.
   Fallback: `/Users/yangjun/Desktop/my-ai/harness-kit`.
2. **Target repo and mode**: repo root contains `.harness/config.sh` → **install mode**
   (right column below; run commands at the repo root); otherwise → **workspace mode**:
   `bash <kit>/harness current` to confirm the active repo.

| Action                       | workspace mode (kit session)                             | install mode (inside target repo)                          |
| ---------------------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| E2E case context             | `<repo>/docs/harness-kit/context/e2e-context.md`          | `.harness/context/testing/e2e-context.md`                    |
| Rubric template              | `<kit>/.harness/rubric/rubric-template.md`                | `.harness/rubric/rubric-template.md`                         |
| Task dir (Rubric location)   | `<repo>/docs/harness-kit/tasks/<task>/rubric.md`          | `.harness/tasks/<task>/rubric.md`                            |
| build hard gate              | `bash <kit>/harness validate --stage build`               | `bash .harness/feedback/validate.sh --stage build`           |
| E2E execution                | driven by HARNESS_E2E_CMD in the repo's docs/harness-kit/config.sh | driven by HARNESS_E2E_CMD in `.harness/config.sh`      |
| Assertion lock               | `bash <kit>/harness lock verify`                         | `python3 .harness/feedback/lock-tests.py verify`             |
| Failure evidence             | `bash <kit>/harness evidence <task> <kind>`              | `bash .harness/feedback/collect-evidence.sh <task> <kind>`   |

## Order (follow exactly)

1. **Kickoff pack** (workspace mode): `bash <kit>/harness brief <keywords>` — contract +
   the repo's notes (historical pitfalls feed the Pitfall checklist) + matching playbooks.
2. **Read the E2E case context first** (see the Step 0 table) — real page entries, stable
   selectors, test accounts. Without it the AI invents unexecutable cases.
   In workspace mode, when that file is still an empty template, guide the user to fill it
   in for the repo before continuing.
3. **Write the Rubric before code**: copy from the Rubric template into the task dir
   (see the Step 0 table) and fill the four-level checklist (Essential/Pitfall/Important/Optional).
4. **RED must run red first**: run new/critical cases once against the current implementation
   and confirm they actually fail — "an acceptor must be falsified before it earns the right to judge".
5. Generate / execute E2E: pass the build hard gate first (see the Step 0 table), then run HARNESS_E2E_CMD.
6. On failure, collect evidence (see the Step 0 table) and turn it into the next round's prompt.

## Verdict criteria (PASS requires all three)

1. Weighted total ≥ threshold (default 0.85);
2. Every Essential item PASS;
3. Trigger accuracy 100%.

E2E four-layer weights you can copy: functional correctness 0.40 / robustness 0.25 /
UI presentation 0.20 / interaction 0.15.

## Selector robustness (three layers stacked)

data-testid (base contract) → a11y snapshot + ref (middle) → DOM-first visual fallback (top).
When a control tree exists, don't go pure-visual.

## Anti-false-reporting hard constraints

- The smoke set is protected by the assertion lock: run lock verify before the verdict
  (see the Step 0 table). A non-zero exit means the smoke tests were tampered with —
  verdict ESCALATED, no pass.
- The prompt handed to the implementation session must include: "These tests are expected
  to fail right now. Do not modify the tests to make them pass."

## Loop control (bounded, stoppable)

- Two independent counters: fix rounds ≤ 3; case corrections ≤ 3 (case problems don't burn the fix budget).
- The same error 3 rounds in a row → `needs_human`, produce an ESCALATED handoff.
- Prefer a fast, single-step-focused normal model for E2E execution; deep-thinking models
  overthink and slow things down.
- Write verdicts and case-hardening lessons back: repo-specific → the repo's
  `docs/harness-kit/notes.md` (workspace mode); cross-repo → `<kit>/playbooks/<topic>.md`.
