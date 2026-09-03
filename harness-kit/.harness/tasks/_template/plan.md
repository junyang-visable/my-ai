# plan — verifiable task breakdown

> Derived from spec.md: spec = what & boundaries (frozen once confirmed),
> plan = how (frozen for scope once confirmed; step-level adjustments during
> execution stay in this file with a note at the step).
> Every step must carry a verification command and an expected output —
> **output not matching expectation = not done**. Checkboxes are the progress;
> a fresh session can resume from them (a personal edition of superpowers
> writing-plans).

- Task name:
- Based on spec: spec.md (status should be confirmed)
- status: draft # draft / confirmed — confirmed must come from explicit user agreement (standard mode gate before coding; harness-coding refuses an unconfirmed plan)

## Task 1: <title, commit granularity>

- [ ] Step 1: <action>
  - Verify: `<command>`
  - Expect: `<concrete output / exit code, e.g. "OK" / exit 0 / contains a line>`

- [ ] Step 2: <action>
  - Verify: `<command>`
  - Expect: `<...>`

## Task 2: <title>

- ...

## Definition of done

- [ ] all Tasks/Steps checked, every verification matched its expectation
- [ ] `bash <kit>/harness validate` all green (add --strict for cross-file changes)
