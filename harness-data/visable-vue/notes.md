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

## CTOOL-679 round (2026-09-12)
- New component checklist (validated): `components/Vis*/` with `index.vue`+composables/useTranslations.js+locales/{en,de}.json+spec.js; composable glob MUST be `import.meta.glob('../locales/*.json')` (shared composable looks up `../locales/${locale}.json` keys) and import path `../../shared/composables/useTranslations`; register i18n scripts in package.json `translations` chain — `index.js`/`index.d.ts` at root are BUILD-GENERATED (gitignored, `node build.js` auto-detects component dirs; 44 as of this round) — never hand-edit or commit them.
- `<script setup>` with top-level `await` (useTranslations) = async setup ⇒ spec MUST use `mountAsyncComponent` from `~/tests/utils` (Suspense wrapper); plain `mount` renders nothing and yields "Cannot call text on an empty DOMWrapper" with a Vue warn about missing Suspense boundary.
- Stylelint gates: properties must be ALPHABETICAL (order/properties-alphabetical-order, `--fix` works) and `clip: rect(...)` is banned (property-no-deprecated) — use `clip-path: inset(50%)` alone for visually-hidden.
- Design tokens live in `node_modules/@visable-dev/design-tokens/dist/variables.css` (`--v-color-{palette}-{scale}`, `--v-font-{copy,display}-{100..1000}`, `--v-radius-{xs,s,m,l}`, `--v-size-N`); import via `@use '@visable-dev/design-tokens/dist/tokens' as *;` and consume as CSS vars. Figma campaign colors without token equivalents (e.g. #F0FAF8, #0DAF8E, #5B8200, #A00F32) are kept as raw hex with a comment (AppSceneBanner precedent).
- Repo has no typecheck stage (plain JS + vue SFC) — validate INFO-skips typecheck by design.
- (CTOOL-679 consolidation) Banner+modal in ONE public component: `VisAlibabaOnboardingBanner` owns modal open/step/company-selection internally, driven by `status` prop ('eligible'|'in_progress'|'created'|'failed') + optimistic `awaiting` flag between activate and the status flip; the modal file lives un-exported inside the banner dir (build.js only scans top-level `components/Vis*` dirs → nested files never auto-export; locales merged under one namespace `alibaba_onboarding`). In specs, `setProps` must target the ROOT wrapper — use `mountAsyncComponent(comp, opts, true)` → `{ rootWrapper, componentWrapper }`; componentWrapper rejects setProps.
- (CTOOL-679 spacing round) VisModal internals that bit: the DEFAULT slot renders into `article` which has **no padding** (only the `.body` named slot gets `--_padding-inline`), and `--vis-modal-width` defaults to 480px. Override per-instance via a fallthrough class on `<VisModal>` setting `--vis-modal-width` (inline style attr on the component tag trips stylelint's custom-property rules in templates). Size tokens only go `--v-size-0..20` (≤160px) — anything bigger (600px, 450px) must be a raw value, NOT `--v-size-75` (phantom token, silently invalid). In-app font tokens are re-themed (display-* renders Lato 900 in product-editor), so pick display tokens by METRICS (display-600=24px/32px matches Figma title). max-nesting-depth ≤2 gates SCSS nesting — flatten leaf selectors (e.g. `.brand-lockup .brand-wordmark.wlw .brand-dot`) to top level when the design nests deeper.
