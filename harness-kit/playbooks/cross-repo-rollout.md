# Coordinating a multi-repo rollout along a dependency chain

## When to apply

A single requirement spans a producer→consumer chain of repos: shared library →
component library → edge/gateway config + per-env infra config → N consuming
apps. Trigger signals: a new export needed from a shared lib before any
consumer can build; a shared UI change that appears in many apps on their next
bump; new page paths that need gateway routing; "every app using component X
needs a version bump".

## The practice

1. **Map the blast radius before coding.**
   - Enumerate repos by tier: dependency producers, edge/gateway config,
     per-env infra (iac) config, consuming apps.
   - Scan for *indirect* consumers: a layout that embeds the shared component
     pulls in apps that never import it directly. Grep direct imports and
     wrapper components alike.
2. **Anchor every repo to its own ticket.**
   - Epic + one Task sub-ticket per repo; branch/PR titles carry the per-repo
     ticket key so the GitHub↔Jira integration auto-links PRs into the
     Development panel.
   - PR→ticket linking falls back to comments: issue-link APIs only do
     issue-to-issue. Use markdown links (`[repo #123](url)`) — bare URLs are
     stored as plain text, not clickable links.
3. **Release the chain upstream-first: tag → CI → verify.**
   - Lib change → push version tag → CI publish → **verify** (registry query +
     CI run list). A pushed tag is not a published version; the publish job
     can fail after the tag.
   - Prerelease phase: consumers pin **exact** versions (semver ranges don't
     match prerelease tags); switch to the repo's normal range style at GA.
   - Transitive pins: if lib A declares lib B with an exact pin, a consumer
     bumping A without bumping its own B resolves a nested duplicate — bump
     both to keep one version in the tree.
4. **Merge order = dependency topology.**
   - Leaf lib → component lib → edge route + iac + the app owning the new page
     **in the same window** (entry visibility, routing and config must appear
     together) → consuming-app bumps last, after staging verification.
   - Edge routing is a hidden prerequisite: both the new page path and its
     server-proxy path need gateway whitelisting. Edge repos can run
     dual-track: PR against the main branch + cherry-pick into the current
     staging deployment branch.
5. **Layer config deliberately.**
   - App repo runtimeConfig default → iac per-env override (staging/prod
     differ) → local `.env` for dev-only identity injection; dev-only keys
     never reach iac.
   - Before adding a config key, check how sibling apps reach the same
     backend — an existing key may carry per-cluster values that don't match
     yours. Reuse only if the values coincide; otherwise a dedicated key.
6. **Verify contracts empirically, end-to-end.**
   - Don't trust spec pages for request shape: probe the real BFF (query vs
     body parameter placement, error body shape) — a 400 "request body
     missing" settles what docs leave ambiguous.
   - Prove the full chain with a temp instance pointed at the real edge and
     watch an upstream error pass through every layer before committing to
     the architecture.
   - On gateway 403/401, attribute the cause first (auth header vs app
     credential vs IP allowlist) before writing code for any specific one.
7. **Parallelize the app bumps mechanically.**
   - Branch from each repo's latest default branch; name requirement-related,
     not version-locked (`<ticket>/navigation-update`, not
     `<ticket>/bump-x-43.44.0-beta.2`).
   - Lockfile-only updates per package manager (pnpm `--lockfile-only`, yarn
     berry `--mode=update-lockfile`, npm `--package-lock-only`), run in
     background on a throttled registry. Verify the repo's *actual* lockfile
     type — the `packageManager` field can lie.
   - Keep package.json edits in the same checkout where the lockfile is
     generated: editing the main checkout while a worktree generates the
     lockfile silently no-ops (and risks colliding with uncommitted WIP).
   - PR body carries: why the exact pin, what the entry depends from (edge /
     iac / lib PR links), rollback path.

## Anti-pattern (don't do this)

- **Renaming a branch that has open PRs** — the rename API *closes* the
  referencing PRs instead of redirecting them. Decide branch names before
  opening PRs, or accept close-and-reopen (new PR notes "Supersedes #old").
- Bumping only the direct dependency and shipping a nested duplicate of the
  transitive one.
- Letting a navigation entry go live before its target page's edge route
  exists — the entry appears on every consumer bump; a dead entry is broken
  UX in *all* apps at once.
- Leaking upstream API paths through a BFF proxy: expose your own first-level
  route contract (`/my-feature-api/*`), keep upstream paths in route-file
  comments.
- Running lockfile generation against a stale package.json in a worktree — an
  empty diff looks like success.

## Basis

- Source task: product-editor-frontend tasks/CTOOL-634/ (WhatsApp settings
  rollout: routing-lib → visable-vue → wlw_nginx + iac + product-editor-
  frontend + 5 app bumps); CTOOL-679 six-app beta rollout
- Verified: 2026-09-22
