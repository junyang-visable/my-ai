# Cross-repo local consumption of unpublished library changes

## When to apply

A multi-repo task needs repo B (consumer) to run against unpublished changes in
repo A (library) — e.g. a new route constant or component entry used by a
consuming app before the library release exists. Trigger signals: build/test
errors like `X is not exported by <lib>/dist/...` from paths inside *another*
repo's `node_modules`, or `ln -sfn` silently not replacing a dependency.

## The practice

1. Identify every resolution path: the consumer resolves a dependency from the
   importing file's real location. If you symlink `consumer/node_modules/libB`
   to a local clone of libB, and libB's code imports libC, then libC resolves
   through **libB's own node_modules** — not the consumer's. Every lib on the
   chain needs the local symlink.
2. Before symlinking, check whether the target is a real directory (yarn/npm
   layouts) or an existing symlink (pnpm layouts: `node_modules/@scope/pkg` →
   `../.pnpm/...`).
   - Real directory: `rm -rf` the package dir first, then `ln -s <clone>
     <path>` (plain `ln -s`, never `-f`).
   - Existing symlink: `ln -sfn <clone> <path>` works.
3. Verify through the link, not at the target:
   `grep -c <NEW_EXPORT> <consumer>/node_modules/<lib>/dist/<file>` must be ≥1.
4. Committed version bumps point at the future released versions (match the
   repo's pin style — some repos pin exact versions, others use caret); the
   dev machine keeps working via symlinks, which are never committed.

## Anti-pattern (don't do this)

- `ln -sfn <clone> <existing-real-dir>`: creates the symlink *inside* the
  directory (`<dir>/<basename>` → clone) and leaves the stale package in
  place — builds keep resolving the old code with no error pointing at your
  link. This produced a 1-blocking-failure build in CTOOL-634 that looked
  like a missing export.
- Symlinking only the direct dependency and assuming the rest of the chain
  resolves through the consumer's node_modules.

## Basis

- Source task: product-editor-frontend tasks/CTOOL-634/ (plan T5/T6.3)
- Verified: 2026-09-07
