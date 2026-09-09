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
- **Tailwind preset scales are NOT default Tailwind (CTOOL-634 round-4 lesson, 2026-09-08)**: `@visable-dev/wlw-tailwindcss-config` redefines `theme.spacing` as `--v-size-N` = **N × 8px** (spacing-1=8px, 2=16, 3=24, 4=32, 6=48...). Writing `mt-4` "expecting 16px" yields 32px — every default-Tailwind mental-model spacing value renders 2×. Convert: px/8 = class number (24px → 3, 16px → 2, 32px → 4, 20px → 2.5, 12px → 1.5, 8px → 1, 4px → 0.5). Non-multiple-of-8 px → arbitrary `[Npx]`.
- **fontSize scale is emptied** in the preset (`fontSize: {}`) so `text-sm`/`text-base`/`text-xs`/`text-2xl` etc. are DEAD classes (only arbitrary `text-[14px]` works). Font utilities are the preset's custom `font-copy-100..600` / `font-display-300..1000` (e.g. 16px→`font-copy-400`, 14px→`font-copy-300`, 20/600→`font-display-500`, 16/600→`font-display-400`). `text-copy-*` (used in older repo code) is NOT a utility — it does nothing.
- **borderRadius scale only defines none/xs/sm/md/lg/full/DEFAULT** → `rounded-lg` = `--v-radius-l` = **12px**, `rounded-md` = 8px; `rounded-xl`/`rounded-2xl`/`rounded-3xl` don't exist — use arbitrary `rounded-[24px]`.
- Build/dev pipeline regenerates `public/product-editor-frontend/favicons/` with content differing from the committed files → favicon churn appears in `git status` after every build/validate. Always `git restore -- public/product-editor-frontend/favicons/` before staging.
- Tests mock `$t` to return i18n KEYS (params ignored) — assert keys, not translated strings.
- i18n: only `en.json` carries feature keys; other 21 locales fall back (verified de.json lacks them).

