# Commit hygiene when a validate/build stage rewrites tracked generated files

## When to apply

- Any flow where a build runs between the code change and the commit (harness validate with a build stage, `nuxi build` smoke checks, generate steps) in a repo that **tracks build output in git**.
- Trigger signal: after a build, `git status` shows modified files you never edited — e.g. `public/**/favicons/*` on Nuxt apps (SVG attribute reorder + PNG re-encode; content-equivalent but byte-different). Seen on product-editor AND business-insights → repo-agnostic Nuxt behavior, not a repo quirk.

## The practice

1. After any build, run `git status --porcelain` BEFORE staging; diff every unexpected file (`git diff <file>`) to classify noise vs. real change.
2. Stage with **explicit paths only** (`git add package.json pnpm-lock.yaml docs/...`) — never `git add -A` / `git add .` in a post-build worktree.
3. If noise slipped into an unpushed commit: `git checkout <default-branch-remote> -- <noisy-path>/ && git commit --amend --no-edit` (no reset needed).
4. Clean worktree residue the same way: `git checkout origin/<default> -- <noisy-path>/`.

## Anti-pattern (don't do this)

- `git add -A` after a build stage "because status looked small" — the commit then carries 8-9 favicon re-encodes as phantom changes; reviewers see binary diffs that don't belong to the ticket (happened on business-insights CTOOL-718; fixed via amend).
- Judging noise by mtime ("must be mine, it changed today") — favicons' mtimes just track the build; content diff is the only honest classifier.

## Basis

- Source task: tasks/CTOOL-718-header-component-upgrade/ (BI amend fix + PE worktree residue, both 2026-10-09)
- Verified: 2026-10-09, on product-editor-frontend (8 files, ep/wlw favicon sets) and business-insights-frontend (9 files)
