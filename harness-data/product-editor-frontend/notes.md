# product-editor-frontend — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in tasks/<task>/history.md under this dir;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- Nuxt 3 (`nuxi`), pnpm, vitest, Pinia, @nuxtjs/i18n, Tailwind via `@visable-dev/wlw-tailwindcss-config`; app code under `app/`, locales in `app/locales` (i18n-cli, tag `product-editor`).
- lint: `pnpm lint` (eslint && prettier --check .) · typecheck: `pnpm typecheck` (nuxi typecheck) · build: `pnpm build` (nuxi build) · test: `pnpm test:ci` (vitest run --silent; plain `pnpm test` adds coverage, slower). Verified from package.json @ v1.0.1.

## Pitfalls & conventions
- pnpm needs the private registry token from ~/.zshrc → wrap with `zsh -ic`, and `cd` into the repo first (zsh -ic starts at kit cwd).
- API clients are generated: `pnpm openapi:generate` from `data/api-schema/*.json` into `open-api/` — new backend endpoints need schema update + regeneration; don't hand-edit `open-api/`.
- Onboarding 2026-09-07: repo was on branch `feat/monitoring-plugin-update` (not main).
