---
description: Accept requirement $ARGUMENTS as the Evaluator (RED-first + four-level Rubric + assertion lock)
---

Accept requirement **$ARGUMENTS** in the **testing-harness Evaluator** role.

Follow this order strictly, and never read the implementation's technical
design (role information isolation):

First locate the mode: repo root has `.harness/config.sh` (install mode) → the
paths below are relative to the repo root; otherwise, in the toolkit repo's
session (workspace mode) → first `bash harness-kit/harness current` to confirm
the active repo, and the paths become: E2E context
`knowledge-base/<active-repo>/context/e2e-context.md`,
Rubric location `knowledge-base/<active-repo>/tasks/$ARGUMENTS/rubric.md`,
assertion lock / evidence collection via `bash harness-kit/harness lock|evidence ...`.

1. Read the E2E case context for real entries/selectors/accounts.
2. Generate `.harness/tasks/$ARGUMENTS/rubric.md` (or the workspace-mode path above) from `.harness/rubric/rubric-template.md` (four-level checklist).
3. RED-first: run key cases once against the current state and confirm they fail.
4. Run the assertion lock verify (install mode: `python3 .harness/feedback/lock-tests.py verify`;
   workspace mode: `bash harness-kit/harness lock verify`); non-zero → verdict ESCALATED immediately.
5. Execute E2E (HARNESS_E2E_CMD); on failure collect evidence (install mode:
   `bash .harness/feedback/collect-evidence.sh`; workspace mode: `bash harness-kit/harness evidence`).
6. Verdict: PASS only when weighted total ≥ threshold AND all Essential pass AND
   trigger accuracy is 100%; otherwise feed back for a fix or ESCALATED.

The prompt handed to the implementation session must include: "These tests are
expected to fail right now. Do not modify the tests to make them pass."
