# spec — the implementer's technical design

> Standard mode: required. Minimal mode: keep only the clarification Q&A
> conclusions (no confirmed gate). For multi-app requirements this file *is*
> the design doc covering every involved app. You (the implementer) never see
> the acceptance Rubric (role isolation) — this file is **your** understanding
> of the requirement and your approach; the acceptance side judges
> independently, and the two get compared afterwards — mismatches are
> clarification signals.

- Task name / ID:
- status: draft # draft / confirmed — confirmed must come from explicit user agreement; changes are demoted back by harness-change

## Involved apps

- App list: <workspace alias; one for single-app, list them all for multi-app>
- Per-app changes / boundaries:
- Cross-app contracts (required for multi-app: interfaces / ordering / dependencies):

## Requirement boundary

- Do:
- Don't (explicitly excluded):

## Approach

- Idea: <one line on the choice and why>
- Affected files / modules:
- Risks & trade-offs:

## Plan

> Task breakdown lives elsewhere — see `plan.md` in this dir (harness-plan derives it from this spec).
> Once confirmed, the spec is frozen: execution drift goes into the plan; requirement changes go through harness-change, never direct edits here.

## Acceptance boundary (implementer's view)

- Observable behavior: <what should be observable when done. Write your own understanding; never go ask the Rubric>

## Change log

- <date: which field changed, why>
