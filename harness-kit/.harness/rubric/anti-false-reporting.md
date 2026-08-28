# Anti-false-reporting trio

> Near-zero cost, maximum payoff — install this first.
> Multiple independent reports hit the same trap: agents will "pass" validation
> by **deleting assertions, changing test expectations, or creating new test
> files**. These three measures close exactly those three paths.

## Piece 1: role information isolation

Two independent sub-agents, each with a fresh context:

- **Implementer (writes the implementation)**: **never sees the Rubric** —
  prevents hardcoding to specific cases. Gets only the requirement / technical
  design / code context.
- **Evaluator (writes acceptance)**: **never sees the technical design** —
  prevents being anchored by the implementation's approach. Gets only the
  requirement / Rubric / run results / evidence.
- Optionally use models from different vendors as Maker–Checker to dodge a
  single model's early-stop and self-flattery biases.

Mapped to this kit: the Implementer uses the `harness-coding` skill, the
Evaluator uses `harness-testing`; the two never share session context.

## Piece 2: RED must run red first

Before letting the agent fix anything, prove the test **can actually fail**.

- Hard constraint: the smoke set is frozen, and the first case (TC-001) must
  fail first — "an acceptor must be falsified before it earns the right to judge".
- In practice: run new cases once against no/old implementation, confirm RED,
  then enter the implement-to-green loop.
- This kit freezes smoke-test function bodies with the assertion lock
  (lock-tests.py) to prevent "fix the test to force green".

## Piece 3: explicit prompt declaration

The prompt handed to the implementation session must contain this sentence
(without it, models have been observed editing unit tests or creating new
test files to bypass the check):

> **"These tests are expected to fail right now. Do not modify the tests to
> make them pass. Your job is to change the implementation so the tests go
> green; if you believe a test itself is wrong, stop and explain — never edit
> the test yourself."**

## Companion: the assertion-lock workflow

```bash
# 1) once the smoke set is stable, record the baseline (SHA of test function bodies)
python3 .harness/feedback/lock-tests.py update

# 2) every validate verifies automatically; or manually:
python3 .harness/feedback/lock-tests.py verify   # mismatch exits 2

# 3) when a smoke test genuinely must change, pick one and leave an audit trail:
HARNESS_LOCK_BYPASS=1 python3 .harness/feedback/lock-tests.py verify
# or add a comment above that test: // @lock-bypass <reason…>, then update again
```
