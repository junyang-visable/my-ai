---
description: Run the harness validation entry (lint→typecheck→arch→build→test, three gate levels)
---

Run the harness validation entry (lint→typecheck→arch→build→test, three gate
levels) and report the result to me.

First locate the mode:
- Repo root has `.harness/config.sh` (install mode) → run `bash .harness/feedback/validate.sh`
- Otherwise, in the toolkit repo's session (workspace mode) → first `bash harness-kit/harness current`
  to confirm the active repo, then run `bash harness-kit/harness validate`

Steps:
1. Run the command above (add `--strict` when this change spans more than 3 files).
2. On blocking failures, list the failing stage, file:line, reason, and fix suggestion verbatim, and propose the next fix step based on them.
3. Never force green by deleting assertions, changing test expectations, adding @ts-ignore, or creating new test files.
4. When all green, remind me to file completion evidence per `.harness/rubric/evidence-template.md`.

$ARGUMENTS
