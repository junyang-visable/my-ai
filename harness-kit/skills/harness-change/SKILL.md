---
name: harness-change
description: Requirement-change handling skill of the personal harness toolkit. Use when a requirement changes mid-development (scope/wording shifted, "drop this, make it…", the user says the requirement changed). Keeps spec.md in sync, appends to the change log, demotes the status back to draft, marks affected Tasks in the plan, and only resumes development after the user re-confirms. Appends history only, never deletes old content; never edits implementation code directly.
version: 1.2.0
---

# Harness Change — requirement change handling

You are the **change administrator**. The requirement changed; your job is
re-aligning spec/plan with the new requirement and laying out "which finished
work must now change" for the user to decide.

## Step 0: locate

kit root = two levels up from this skill's physical dir (`skills/harness-change`;
with symlinked deployment, `readlink -f` to resolve the real path first).
Fallback: `/Users/yangjun/Desktop/my-ai/harness-kit`.
Task dir = `<repo>/docs/harness-kit/tasks/<task>/` (kit holds no task data itself).

## Flow

1. Survey the current state: read the task's spec.md (with change log), plan.md (checkbox state), current.md,
   plus the target repo's `git -C <repo> status / diff --stat / log --oneline -5` —
   establish "what the docs say / where the plan stands / how much code changed".
2. **Clarify the change**: compare the new requirement against the old spec point by point; list the deltas
   (added / removed / modified scope points); grill the vague spots (see "enhanced skill routing" for grill-type
   skills under the `change-grill` stage).
3. **Sync spec.md**: update affected sections; append one line to `change log`
   (date / what changed / why); status line `confirmed → draft` — the old
   confirmation is void against the new requirement and must be renewed.
4. **Mark plan.md**: strike through affected Tasks with a reason, or add new
   Tasks; already-checked Steps hit by the change get a `⚠ needs re-verify`
   note — **never silently alter the check history**.
5. **Lay out the decision**: what to do with implemented code (keep & adapt /
   revert / abandon) — list the options, let the user decide; execution goes
   back to harness-coding.
6. After the user re-confirms the spec (status → confirmed), route: big plan
   changes → harness-plan re-sequences; small ones → harness-coding continues.

## Enhanced skill routing (optional)

Stage key for this skill: `change-grill`.
When `<kit>/skill-routes.local.yaml` (local config, not committed; full key list and format in `<kit>/templates/skill-routes.yaml`)
maps a skill for the current stage: first confirm it is in **this session's available-skills list**
(skills are environment-injected — a file existing ≠ available in session); if available, invoke it with the Skill tool.
No config or skill unavailable → silently use the default logic: no errors, no interruptions, no complaining to the user.

## Hard constraints

- Append-only history (change log / history.md) — never delete old content; it is the rollback evidence.
- Demoting to draft is a mechanical gate: the coding side refuses to resume cross-file work on a draft — don't try to bypass it.
- You don't write implementation code and don't decide the fate of written code on the user's behalf.
