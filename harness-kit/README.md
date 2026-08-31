# harness-kit

A reusable, stack-agnostic orchestration scaffold that plugs **Coding Harness +
Testing Harness (E2E-first)** into any repo. It is not a homegrown engine: it sits
on top of your agent CLI (Qoder / Claude Code) and uses **contract + commands +
hooks + context conventions + mechanical validation** to close the "environment"
half of the "model capability × environment capability" equation.

> Positioning: a **personal development toolkit**. Three pillars:
>
> 1. **Knowledge that compounds** — every task leaves notes, playbooks, and history behind.
>    Per-project knowledge lives in your central knowledge base (`knowledge-base/<project>/`);
>    cross-repo methodology lives in the kit (`playbooks/`). Your work writes your own
>    best practices.
> 2. **Skill orchestration** — bring your favorite skills. Stage-keyed local routing
>    (`skill-routes.local.yaml`) plugs grill/diagnosis/design skills into the workflow.
> 3. **A harness loop with teeth** — clarify → design doc → verifiable plan → TDD coding →
>    independent acceptance, with mechanical gates instead of prompt-nagging.

## Data model

```
<kb>/                              ← your central knowledge base (one tree per project)
├── <alias>/                       ← per-project data (committable, follows YOU not the repo)
│   ├── config.sh                  # that repo's commands (the only file to adapt per stack)
│   ├── notes.md                   # repo stack, verified commands, pitfalls
│   ├── context/e2e-context.md     # E2E case context (entries/selectors/accounts)
│   ├── tasks/<task>/              # spec / plan / current / result / history + evidence/
│   └── .lock-baseline.json        # assertion-lock baseline
└── (your own topic docs…)         # the KB is yours — top-level notes coexist freely

harness-kit/                       ← pure tool (this repo)
├── workspaces/<alias>.conf.sh     # thin registry: repo path (+ optional env defaults)
├── playbooks/                     # cross-repo methodology (your distilled practices)
└── skill-routes.local.yaml        # local skill-routing config (gitignored)
```

`<kb>` defaults to the kit's sibling `knowledge-base/` dir; relocate it via
`HARNESS_KB_HOME`. Target repos need zero installation and receive zero
writes — the kit drives them from outside (workspace mode), while all
knowledge accumulates centrally in your KB.

## Five layers

| Layer          | Purpose                        | In this kit                                                                                                      |
| -------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| Contract       | 30-second boundaries, short    | `templates/AGENTS.md` (~100 lines, index + red lines only)                                                        |
| Context        | knowledge loaded on demand     | `templates/docs/`, `.harness/context/`                                                                            |
| Tooling        | reusable skills/commands/hooks | `skills/`, `commands/`, `.harness/hooks/`                                                                         |
| Validation     | mechanical enforcement         | `.harness/feedback/` (validate / lint-arch / lock-tests / collect-evidence)                                       |
| Loop           | state & resume                 | `<kb>/<alias>/tasks/<task>/{spec,plan,current,result,history}.md + evidence/` (spec = boundary contract, plan = verifiable breakdown) |

## Quick start (workspace mode: drive any repo from the kit's repo; targets need zero install)

```bash
# 0) once: symlink kit skills into this repo's skills dir (relative links survive clones)
./harness link

# 1) register a repo — creates its KB tree <kb>/my-app/ (config + notes + e2e context)
./harness add my-app /path/to/your-repo

# 2) fill in that repo's commands (per stack)
$EDITOR knowledge-base/my-app/config.sh   # HARNESS_LINT_CMD / TEST_CMD / BUILD_CMD / E2E_CMD ...

# 3) prove the guardrails are real, then run the full pipeline
./harness validate selfcheck
./harness validate
```

Day-to-day, **talk to the skills directly** from the kit repo's session:

> "Use harness-dev to add an XX feature to my-app" / "harness-dev, switch to another-repo and continue the XX task"

The skill locates the kit, decides the execution mode (**standard = default full flow**:
clarify → design doc covering all involved apps → breakdown → coding;
**minimal = explicit switch**: skip design, locate and patch directly, branch + validate
guardrails kept), confirms the active repo, routes to specialist skills, runs the coding
loop, and distills lessons at wrap-up. After implementation, open a separate session and
say "use harness-testing to accept XX" (role isolation).
Note: the target repo must be part of your Qoder workspace, or writes get sandbox-blocked.

### The skill family (6, wired up by `./harness link`)

| Skill           | Role                                                            | When                 |
| --------------- | --------------------------------------------------------------- | -------------------- |
| harness-dev     | orchestrator/routing + workspace mgmt + dual-mode decision     | cross-repo entry     |
| harness-spec    | clarify → spec.md (confirmed gate; can route grill-type skills) | new/vague requirement |
| harness-plan    | spec → plan.md (per-step verify command + expected output)      | after spec confirmed |
| harness-coding  | implementer: TDD + validate + tick plan Steps                  | coding               |
| harness-testing | acceptor: separate session, Rubric + RED-first + assertion lock | acceptance           |
| harness-change  | requirement change: demote spec to draft, mark plan            | requirement changed  |

Standard-mode flow (default): vague requirement → spec (clarify + confirm; multi-app
specs cover every involved app) → plan (verifiable breakdown, grouped by app) → coding
(TDD + gates, per app) → testing (independent acceptance); requirement changes route
through harness-change at any time, demoting the spec back to draft for re-confirmation.
Minimal mode (explicitly tell harness-dev "minimal / just change it"): light task →
locate & patch → validate, skipping design and planning. Every skill runs
`./harness brief` first to pull repo knowledge into context.

### Enhanced skill routing (optional, local config)

At specific stages (clarify, approach, diagnosis…) harness skills can call general-purpose
skills already present in your environment (e.g. Qoder's `grilling` interrogation or
`design-an-interface` parallel exploration). Mappings live in `skill-routes.local.yaml`
at the kit root — personal local config, gitignored, not committed; format and docs in
`templates/skill-routes.yaml`:

```yaml
harness-spec:
  clarify: grilling
  explore-approaches: design-an-interface
```

Rules: no mapping, or the mapped skill is not in **this session's available-skills list** →
silently use the default logic; no errors, no interruptions. Availability follows the
session-injected list (file exists ≠ available in session). Switching environments means
editing that one local file — the skills themselves never change.

CLI commands all act on the active repo:

```bash
./harness list                      # registered repos; * marks the active one
./harness use another-repo          # switch the active repo
./harness doctor                    # health: configured commands, smoke set, lock baseline
./harness validate --strict         # full pipeline, three gate levels (blocking/warning/info)
./harness lock update               # record baseline once the smoke set is stable; verify detects tampering
./harness evidence task api         # collect evidence after failure; produces the next fix prompt
./harness task new my-task          # create a task dir under <kb>/<active-repo>/tasks/
./harness context                   # print the contract text; paste it into agent sessions
./harness brief <keywords>          # kickoff pack: contract + repo notes + matching playbooks + tasks
```

## Knowledge compounding (the toolkit's core value)

| Layer        | Location                                       | What goes there                                                         |
| ------------ | ---------------------------------------------- | ------------------------------------------------------------------------ |
| Project-specific | `<kb>/<alias>/notes.md`                    | that repo's stack, verified commands, pitfalls, conventions              |
| Cross-repo   | `playbooks/<topic>.md`                        | methodology that holds in any repo; one topic per file, traceable to tasks |
| Task-level   | `<kb>/<alias>/tasks/<task>/history.md`        | append-only process record                                               |

The skills (harness-dev / harness-coding / harness-testing) write back to all three
layers at wrap-up. Division of labor with agent built-in memory: memory is isolated per
session-project and unreadable when developing other repos; this kit is plain files, in
git, following you across all your projects — which is exactly why the knowledge lives
in your central KB.

### Optional: install mode

If you want a repo to carry its own harness (agents read AGENTS.md on entering), run
`./install.sh <repo>`. Both modes coexist; workspace mode writes nothing into the
target repo at all. Commands land in `.qoder/commands/` (Claude Code copies
to `.claude/commands/`; the files are universal); the post-edit hook needs wiring in your
CLI's hook config: `bash .harness/hooks/post-edit.sh <file>`.

## Coverage (P0–P2)

- **P0**: contract layer `AGENTS.md`; `validate.sh` composes lint→typecheck→arch→build→test
  with three gate levels; `selfcheck` deliberately plants a violation to prove the
  guardrails actually fire.
- **P1**: `post-edit.sh` incremental post-edit quick-check + output truncation;
  `evidence-template.md` completion-evidence template.
- **P2**: E2E case context library, four-level Rubric, the anti-false-reporting trio,
  assertion lock `lock-tests.py`, automatic failure-evidence collection `collect-evidence.sh`.

## How "stack-agnostic" works

Every script reads only the command variables in the project's `<kb>/<alias>/config.sh`
(install mode: `.harness/config.sh`); empty stages are skipped automatically. Switching
stacks means editing config, never the engine. Skills and commands are agent-universal
markdown (Qoder / Claude Code both read SKILL.md); the engine itself is pure shell +
markdown.

## Directory

```
harness-kit/
├── harness                    workspace-mode console (add/use/link/validate/lock/evidence/task/...)
├── workspaces/                thin repo registry: <alias>.conf.sh = repo path (+ optional env defaults)
├── install.sh                 optional: install harness into a repo (engine symlinks / config copies)
├── skill-routes.local.yaml    local enhanced-skill routing (gitignored; template: templates/skill-routes.yaml)
├── playbooks/                 cross-repo methodology library (one topic per file, traceable to tasks)
├── templates/                 contract layer & docs templates
│   ├── AGENTS.md
│   ├── skill-routes.yaml
│   └── docs/{ARCHITECTURE,DEVELOPMENT}.md
├── .harness/
│   ├── config.sh              default wiring point (workspace mode: overridden by <kb>/<alias>/config.sh)
│   ├── feedback/              validate / lint-arch / lock-tests / collect-evidence
│   ├── hooks/post-edit.sh     incremental post-edit quick-check
│   ├── context/testing/       E2E case-context template
│   ├── rubric/                four-level Rubric + anti-false-reporting trio + evidence template
│   └── tasks/_template/       loop-state templates
├── skills/                    6 skills (agent-universal SKILL.md; link symlinks them into .agents/skills/)
└── commands/                  /harness-validate etc. slash commands (agent-universal markdown)
```

## Boundaries

The dual modes are the pressure valve: standard mode (default) never short-changes the
flow because a task looks small; for trivial changes (single-file bugfix / log line /
copy tweak) tell harness-dev **explicitly "minimal mode"** to skip design and patch
directly — branch + validate guardrails are never waived. Gate levels exist
(blocking/warning/info) precisely to avoid the "everything blocks" dynamic that breeds
workarounds.
