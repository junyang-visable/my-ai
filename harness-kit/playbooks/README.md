# playbooks/ — cross-repo methodology library

> Division of labor with `<kb>/<alias>/notes.md` (project-specific):
> **only conclusions that hold in a different repo belong here**. A repo's
> commands, selectors, environment quirks → notes.md; transferable methodology
> (patterns, anti-patterns, decision heuristics) → this directory.

## Organization

- **One topic per file**, the filename is the topic: `<topic>.md` (e.g. `red-first.md`, `cypress-selector-strategy.md`).
- Start from `_template.md`; when done, link the source task (`tasks/<task>/`) at the
  bottom under "Basis" so every lesson traces back to a real case.
- Lessons come from skill wrap-up write-backs (harness-coding / harness-dev
  wrap-up steps) or manual retrospectives; base anti-false-reporting material
  lives in `.harness/rubric/anti-false-reporting.md` and is not repeated here.

## Naming suggestions

- Action-oriented: `<how-to-do-x>.md` (e.g. `collect-evidence-priority.md`)
- Anti-pattern-oriented: `avoid-<what>.md` (e.g. `avoid-editing-tests-to-green.md`)

## Freshness

- Review quarterly: delete what expired, merge what overlaps. Better few and
  precise than many and watery.
