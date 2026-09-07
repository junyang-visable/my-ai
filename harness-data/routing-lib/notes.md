# routing-lib — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in tasks/<task>/history.md under this dir;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- Plain JS lib `@visable-dev/routing` (published dist via vite build), npm (package-lock), jest, eslint 9. No typecheck.
- lint: `npm run lint` · build: `npm run build` · test: `npm run test:ci` (jest --runInBand). Verified from package.json (version field is 0.0.0-placeholder; real versions only exist as git tags vX.Y.Z).
- Route constants live in `src/constants/routes.js` as `{ default: generateLocalizedRoutes((locale) => \`/${locale}/...\`) }`; path params like `:supplierId`; DE-specific overrides possible (see CATEGORIES_ROUTE).

## Pitfalls & conventions
- npm install needs tokens from ~/.zshrc (devDeps include `github:eslint/js`) → wrap with `zsh -ic`, cd into repo first.
- Publishing is tag-driven (git tags vX.Y.Z, no version bump commit in repo); releasing a new constant = tag a new version, consumers bump the semver range (visable-vue requires ^22.7.3 as of 2026-09).
- Cloned 2026-09-07 for CTOOL-634 (SUPPLIER_SETTINGS_ROUTE addition).
