---
name: harness-dev
description: Orchestrator entry point of the personal harness toolkit. Use when you want to develop another repo from the toolkit repo's session (e.g. "use harness-dev to work on repo X / do Y for repo X / cross-repo development") or mention harness-dev or registering a new workspace. Locates the kit, decides the execution mode (standard = default full flow with a multi-app design doc; minimal = skip design and patch directly, only on explicit request), registers or switches the target repo, runs health checks, creates tasks, enters the coding loop as the implementer, and distills lessons back into the kit at wrap-up.
version: 1.4.0
---

# Harness Dev — cross-repo development orchestrator

You drive development of any target repo from your **personal toolkit repo**:
engine, tasks, and lessons all live in the kit, while target repos need zero
installation (workspace mode). This skill is the **implementer** only — never
the acceptor. Development runs in two modes, **standard** and **minimal**;
decide the mode before routing (§3).

## 1. Locate the kit

kit root = two levels up from this skill's physical dir (`skills/harness-dev`).
With symlinked deployment, resolve the real path first, then walk up:

```bash
cd "$(dirname "$(readlink -f <this SKILL.md path>)")/../.." && pwd
```

Fallback (edit this line when switching machines): `/Users/yangjun/Desktop/my-ai/harness-kit`.
Below, `<kit>` refers to it.

## 2. Pick the target repo

- User gave an **alias**: `bash <kit>/harness use <alias>` (if unknown, show `harness list` and ask whether to register)
- User gave a **path**: `bash <kit>/harness add <alias> <path>` (alias defaults to the repo name; add a suffix on collision)
- **Neither**: `bash <kit>/harness list` and let the user pick; if none exist, guide registration
- If the target repo root contains `.harness/config.sh` (install mode), tell the user both modes work and follow their preference

## 3. Decide the mode (before any flow)

- **Standard is the default.** Switch to minimal only when the user explicitly
  says so — "minimal mode / keep it minimal / just a small fix / skip the full
  flow / just change it directly". Strictly explicit: never suggest switching,
  never judge task size on the user's behalf.
- Standard mode: full flow (clarify → design doc → task breakdown → coding),
  multi-app capable, see §6.
- Minimal mode: skip design and planning; create a light task, then locate and
  patch directly. **Branch creation and validate are never waived.**
- Record the mode in the task's `current.md` ("mode" field). If the user asks
  to switch mid-flight: continue under the new mode's flow and wrap-up rules;
  never delete spec/plan artifacts already produced.

## 4. New-workspace onboarding (first registration only)

1. Read the target repo's `package.json` / `Makefile` / `pyproject.toml` etc.
   and **infer** the lint / typecheck / build / test commands; write them into
   the project's knowledge-base config `<kb>/<alias>/config.sh` (created by
   `harness add`). Tell the user the inference basis and ask for confirmation
   (leave uncertain ones empty — empty stages are skipped automatically).
2. Run `bash <kit>/harness doctor` for a health check, and
   `bash <kit>/harness validate selfcheck` to prove the guardrails are real.
3. Jot the repo's stack and pitfalls into `<kb>/<alias>/notes.md`; add
   `<kb>/<alias>/context/e2e-context.md` when E2E needs arise.

`<kb>` = the knowledge-base root: the kit's sibling `knowledge-base/` dir by
default, overridable via `HARNESS_KB_HOME`. One tree per project alias; it
holds repo knowledge and task process state — a task's spec/plan, by
contrast, are project artifacts committed in the target repo at
`docs/changes/<task>/`.

## 5. Tasks and write permissions

- **Write-permission precheck**: when the target repo is not part of the
  current Qoder workspace, file writes get blocked by the sandbox. Ask the
  user to add the repo to the workspace (Add Folder to Workspace) before
  starting — don't trial-and-error.
- Harness-generated data splits by nature: **process state** (current /
  result / history / evidence / rubric) lives in the knowledge base under
  `<kb>/<alias>/tasks/<name>/`; **spec/plan are project artifacts** written
  into the target repo at `docs/changes/<name>/` (committed with the feature
  branch; multi-app tasks: one copy in the primary repo, cross-read by the
  other apps' sessions). Create tasks with
  `bash <kit>/harness task new <name>` — it creates both dirs.
  If a task with the same name exists, read its `current.md` (mode + stage +
  single next step) and resume — never start a parallel one.
- Legacy tasks (created before 2026-09) keep spec/plan inside their KB task
  dir — read them where they are; don't migrate.
- **Kickoff pack**: `bash <kit>/harness brief <keywords>` — contract, the
  active repo's notes, and matching playbooks in one shot. Required reading
  before starting work.
- **Resume validation (backfill)**: when current.md disagrees with reality
  (code already written, plan already checked, relevant commits in git log),
  reconstruct the true stage from observable state (git log/diff, task
  artifacts), confirm with the user, fix current.md, then continue. Never
  trust the file blindly.

## 6. Routing (the orchestrator dispatches; specialists do the heavy lifting)

### Standard mode (default)

1. **Clarify & design**: route to harness-spec, which produces
   `<repo>/docs/changes/<name>/spec.md` (this *is* the design doc).
   - Single app: the spec covers that app.
   - **Multi-app: the spec must cover every involved app** — the app list,
     per-app changes/boundaries, and cross-app contracts (interfaces /
     ordering / dependencies). Missing any of these blocks kickoff. Every
     involved repo must be a registered workspace (run §4 onboarding first).
2. **Confirm**: the spec reaches `confirmed` (explicit user agreement).
3. **Break down**: route to harness-plan to produce plan.md; for multi-app
   tasks, group Tasks by app and annotate cross-app dependency order.
4. **Code**: per app, enter the coding loop — `bash <kit>/harness use <app>`
   to switch the active repo, then harness-coding executes spec+plan Task by
   Task, checking items off.
5. **Wrap up**: per-app validate + evidence; write lessons back to each
   app's `<kb>/<app>/notes.md`.

### Minimal mode (explicit user request only)

1. `bash <kit>/harness task new <name>` creates a light task (process state in
   the KB, spec/plan skeleton at `<repo>/docs/changes/<name>/`): current.md
   records "mode: minimal" plus a one-line requirement; clarification Q&A
   conclusions go into spec.md as a few lines (no confirmed gate).
2. Create a branch (hard prerequisite, same as §7).
3. Locate the code (search/read), tell the user which files you intend to
   change, then change them.
4. `bash <kit>/harness validate` + a one-line completion claim (validate
   summary + number of files changed).

### Cross-cutting routes

| Situation                            | Route                                                              |
| ------------------------------------ | ------------------------------------------------------------------ |
| Requirement change (standard task)   | harness-change (demote spec to draft, mark affected Tasks)         |
| Requirement change (minimal task)    | update current.md one-liner and spec.md Q&A conclusions, continue  |
| Acceptance                           | separate session with harness-testing (role isolation)             |

## 7. The coding loop (implementer role)

Same discipline as the harness-coding skill; the core:

**Create a branch before any work (hard prerequisite; never develop on the main branch's working tree):**

```bash
git fetch origin
git symbolic-ref refs/remotes/origin/HEAD   # confirm the default branch; on failure fall back to whichever of master/main exists
git checkout --no-track -b <branch> origin/<default>
```

- Branch naming (slash-separated; `:` is illegal in git refs — verified with
  `git check-ref-format`): with a ticket id → `<ticket-id>/<short-desc>`
  (e.g. `FE-1042/ssr-unsafe-api-detection`); without → `feat/<short-desc>` or
  `chore/<short-desc>` (pick by change nature).
- All commits happen on the branch; push with `git push -u origin <branch>`
  to establish tracking.
- Skip branch creation when resuming a task that is already on the right
  branch; if changes were accidentally written in the main-branch working
  tree (uncommitted), `git checkout --no-track -b <branch> origin/<default>`
  carries them over to the new branch.

- Clarify the requirement and acceptance boundaries before writing code; stop
  and ask when unsure.
- Standard mode: before starting, check the spec status line = `confirmed`;
  draft or missing → back to harness-spec, never start on a shaky spec. With
  plan.md, execute Task/Step by Task/Step, ticking items off and running each
  step's verification command against its expected output.
- Unit-test TDD (whenever the change is unit-testable, regardless of mode):
  write the test first, run it once to confirm RED (record the failing
  assertion in the task's `history.md`), then implement to green; for bugfix
  start with a failing test that reproduces the bug. Pure copy/style changes
  are exempt.
- Small steps; before claiming completion, run the single validation entry:

  ```bash
  bash <kit>/harness validate        # add --strict for cross-file changes
  ```

- A blocking failure means not done. **Never** delete assertions / change test
  expectations / add `@ts-ignore` / create new test files to force green; if
  you believe a test itself is wrong, stop and explain. Build cannot be
  skipped.
- On failure, collect evidence as the next round's input:
  `bash <kit>/harness evidence <task> <layout|api|render|generic>`

## 8. Wrap-up

1. Update the task's `current.md` (mode + stage + single next step) and
   `history.md` (append one line).
2. File completion evidence per `<kit>/.harness/rubric/evidence-template.md`
   (reproducible numbers; honestly declare uncovered scope; minimal mode may
   compress to a one-line validate summary).
3. **Write lessons back** (this is the toolkit's whole value — never skip):
   - repo-specific pitfalls / verified commands / conventions → `<kb>/<alias>/notes.md`
   - practices that hold across repos → `<kit>/playbooks/<topic>.md` (start from `_template.md`)
   - task-level detail → the task's `history.md`
4. Remind the user: acceptance must happen in a **separate session** using the
   harness-testing skill (role isolation; never self-accept in this session).

## Three-way exit

- `success`: validate all green + evidence complete → hand off to an independent session.
- `failed`: no progress on the same error for 3 consecutive rounds → stop blind retries.
- `needs_human`: produce an ESCALATED handoff (paths tried, failure evidence, current best hypothesis, suggested next step).
