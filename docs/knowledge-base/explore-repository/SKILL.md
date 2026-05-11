---
name: explore-repository
description: Use when answering ANY question about this project — understanding how code works, locating files or modules, planning changes, implementing features, or debugging issues. Must be invoked before any response about the codebase. All answers must be based on the knowledge base in ./docs/ — never scan source code directly.
allowed-tools: Read, Grep
---

## Process Flowchart

Follow this flowchart exactly. Every node is mandatory — do not skip or shortcut any branch.

```mermaid
flowchart TD
    START([Question about codebase]) --> META{META.md exists?\n./docs/META.md}

    META -->|No| INIT[Trigger initialize-knowledge-base\nStop here — do not continue]

    META -->|Yes| VER[Step 0 · Load version-check.md\nDiff source changes since last_commit]
    VER --> CURRENT{Source files changed\nAND covered by KB?}

    CURRENT -->|Yes — KB may be stale| REFINE0[Trigger refine-knowledge-base\nthen continue]
    CURRENT -->|No — no changes or not in KB| NAV

    REFINE0 --> NAV[Step 1 · Open RUNBOOK.md\nLoad navigation-guide.md]
    NAV --> LOOKUP[Step 2 · Navigate to relevant KB file\nusing navigation-guide.md routing rules]
    LOOKUP --> KBFOUND{KB has answer?\nfull OR partial}

    KBFOUND -->|Yes — full or partial| FORMAT[Step 3 · Compose answer\nusing answer-format.md template]

    KBFOUND -->|No — confirmed gap| REFINE1[Step 5 · Trigger refine-knowledge-base\ngap type = topic]
    REFINE1 --> FORMAT

    FORMAT --> NEED_CODE{Need to read\nor modify code?}

    NEED_CODE -->|No| DONE([Deliver answer])

    NEED_CODE -->|Yes| VP[Step 4 · Load verification-protocol.md\nRead minimum files KB points to]
    VP --> MATCH{KB matches code?}

    MATCH -->|Yes| ACT([Make change or cite code])

    MATCH -->|No — KB stale or gap| REFINE2[Step 5 · Trigger refine-knowledge-base\nnote exact KB file + what code shows]
    REFINE2 --> ACT

    ACT --> SYMBOL{Did you read code\nto answer a\nfunction/symbol question?}
    SYMBOL -->|Yes| REFINE3[Step 6 · Trigger refine-knowledge-base\ngap type=symbol, pass findings]
    SYMBOL -->|No| DONE2([Done])
    REFINE3 --> DONE2

```

---

## First Principle

**Reading raw source code is the last resort — not the first move.**

You MAY open source code ONLY when ALL of the following are true:

1. You have completed the full KB lookup (steps 0–3 below)
2. The KB does not contain the answer or guide needed
3. No KB file provides a path forward

If the KB has a partial or related answer, that is NOT a gap — use it.
If you are unsure whether the KB covers it, that is NOT a gap — check it first.

**There is no exception to this rule. No shortcut. No "just a quick peek."**
Reading code before exhausting the KB is a protocol violation.

**Default posture: knowledge base first, code second.**

---

## What You Must Do

Follow this loop exactly — do not skip steps:

```
0. Run version-check.md — verify KB is current before reading anything
1. Open ./docs/RUNBOOK.md
2. Navigate to the relevant KB file using navigation-guide.md
3. Compose answer using answer-format.md
4. If you need to touch code → run verification-protocol.md first
5. If KB is wrong or missing → trigger refine-knowledge-base, then continue
6. If you read code to answer a function/symbol question → trigger refine-knowledge-base with:
     gap type = symbol, findings = <your findings>
   (subagent dispatch is skipped when findings are provided)
```

**NEVER open source code before completing steps 0–3. No exceptions.**
**NEVER open source code if the KB provides any answer or guide — even a partial one.**
Never open RUNBOOK.md before completing step 0.
explore-repository NEVER writes to ./docs/ directly — all writes go through refine-knowledge-base.

---

## Sub-files

### Load `version-check.md` first — before navigation-guide.md or any KB file.

It compares `last_commit` from META.md against the current HEAD using `git diff --name-only last_commit HEAD -- ':!docs'` to detect whether source code (excluding docs/) has changed since the last sync.
If changes are found, it checks whether any changed files are referenced in KB index files (`03_index/file_index.md` or `04_modules/*.md`).
Only changes to KB-covered source files trigger a refine; irrelevant changes just update `last_commit`.
If META.md does not exist → skip and trigger `initialize-knowledge-base` instead.

### Load `navigation-guide.md` immediately after version-check passes.

It tells you which KB file to open for each type of question or task.
Without it you will guess file locations — that defeats the purpose of the KB.

### Load `answer-format.md` before composing any answer.

It defines two templates: Function-Level (Chain, Behavior, Signature, Constraints) and
File/Module/Feature (Big Picture, Context, Range). Apply the narrowest-scope template first.
Without it answers will be raw file dumps instead of structured, agent-readable responses.

### Load `verification-protocol.md` only when you are about to read source code.

It tells you how to compare what the KB says against what the code actually does,
and what action to take when they disagree.
If you skip it, you risk silently using stale information or ignoring a KB gap.
