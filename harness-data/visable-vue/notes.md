# visable-vue — repo notes

> Stack, verified commands, pitfalls, and conventions for this repo.
> Task-level history lives in tasks/<task>/history.md under this dir;
> cross-repo lessons graduate to the kit's playbooks/.

## Stack & verified commands
- Vue 3 SFC component library, published as `@visable-dev/vue` (v43.x), yarn 1, vitest, Storybook 10, stylelint; plain JS + vue SFC — no typecheck script.
- Components under `components/Vis*/`, each with its own `locales/` dir (i18n-cli, tags `visable-vue:<component>`); exports: `@visable-dev/vue` (index) and `@visable-dev/vue/components/*`.
- lint: `yarn lint` (eslint && stylelint && prettier --check) · build: `yarn build` (node build.js) · test: `yarn test:ci` (vitest run). Verified from package.json @ v43.41.2.

## Pitfalls & conventions
- yarn needs the private registry token from ~/.zshrc → wrap with `zsh -ic`, and `cd` into the repo first (zsh -ic starts at kit cwd).
- Onboarding 2026-09-07: repo was on branch `master` (default).
- Nav-related components include VisAccountHeader, VisPageNavigation, VisActionsSidebar — settings-entry work must first identify the nav component actually consumed by product-editor-frontend before editing.
- CTOOL-634 (2026-09-07): `node_modules/@visable-dev/routing` is a manual symlink to the local `~/Desktop/project/routing-lib` clone (dev-only machine state; after any `yarn install` re-check it — re-create with `rm -rf` of the real dir then plain `ln -s`, `ln -sfn` nests inside real dirs). Vite resolves routing imports inside this repo's sources through THIS node_modules, so the link must exist for consumers building against local visable-vue sources.
