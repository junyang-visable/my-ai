# Completion evidence template (Definition of Done)

> Copy this into `.harness/tasks/<task>/result.md` or paste it into the session.
> The evidence template is the anti-false-reporting measure that needs the
> **least infrastructure** — no evidence, no completion.
> Key rule: numbers must be reproducible; "tests passed" alone doesn't count.

## Requirement

- Task name / ID:
- One-line goal:

## Code baseline

- Branch: `<branch>`
- Commit: `<commit sha>`
- Files changed: `<n>` (more than 3 files → full validate)

## Execution environment

- Runtime / dependency versions:
- Key env-var provenance: `<staging / mock / real gateway>`

## Modules that actually entered the build

> Guards against "changed A but built the cached B". List the modules/packages
> that genuinely participated in this build/test run.

-

## Commands run & raw reports

```text
$ bash .harness/feedback/validate.sh
<paste the real output summary: per-stage OK/FAIL and the summary line>
```

- Unit tests: `<passed / total>` (link or paste of the raw report)
- E2E smoke: `<passed / total>`, evidence dir: `.harness/tasks/<task>/evidence/`
- Assertion lock: `<verify passed / has @lock-bypass, explained below>`

## Uncovered scope (declare honestly)

> An empty section here is almost always suspicious. State what wasn't tested,
> why, and how much risk that carries.

-

## Residual risks

-
