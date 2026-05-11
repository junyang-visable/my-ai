# Version Check

## When to Run

Run this check BEFORE opening any KB file or source code.
If `./docs/META.md` does not exist → skip this check and trigger `initialize-knowledge-base` instead.

---

## Step 1 — Read META

Open `./docs/META.md`. Extract:

- `last_commit`

---

## Step 2 — Detect Source Changes

Run:

```
git diff --name-only last_commit HEAD -- ':!docs'
```

This lists source files that changed between `last_commit` and `HEAD`, excluding the `docs/` directory.

If `last_commit` is unreachable (rebased away, force-pushed) → treat as full mismatch, trigger `refine-knowledge-base`.

---

## Step 3 — Evaluate Changes

### No changes

```
git diff returns empty output
```

→ No source files changed since last sync. KB is current.
Update `last_commit` in META to current HEAD. Proceed to navigation.

---

### Changes found — check KB coverage

Run through each changed file path and check whether it appears in KB index files:

1. `./docs/03_index/file_index.md`
2. `./docs/04_modules/*.md` — Entry Points, Key Files, and Scope Table sections

For each changed file path, search these KB files for a reference to that path (full path or matching filename).

| Coverage result                            | Meaning                                     | Action                                                                                                                 |
| ------------------------------------------ | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| No changed file has KB coverage            | Changes are irrelevant to documented topics | Update `last_commit` in META to HEAD. Proceed to navigation.                                                           |
| One or more changed files have KB coverage | Documented code may have drifted            | Trigger `refine-knowledge-base` with the list of covered changed files. After refine completes, proceed to navigation. |

---

## Why Diff-Based Instead of Commit Equality

Storing `last_commit` and checking equality fails when updating META itself creates a new commit — the stored SHA is always behind HEAD. Using `git diff --name-only` instead avoids false mismatches because it excludes `docs/` from the diff, so META-only commits produce no output (no changes). This also directly answers the right question: "Has source code that the KB tracks changed since last sync?"
