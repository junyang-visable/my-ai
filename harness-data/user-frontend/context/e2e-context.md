# E2E case-context knowledge base

> The most-skipped yet most-critical step of the testing harness — its whole
> purpose: hand the AI real page entries, stable selectors, and test accounts,
> so it can't invent unexecutable cases. Organize by **business capability**,
> never by page or technical layer — capability organization measurably lifts
> AI code-location precision from ~5% to ~100% and recall from ~14% to ~86%.

## Environment & login state

- Target environment URL: `<staging base url>`
- Test account: `<username>` / how to get the password: `<where from; never commit in plaintext>`
- How login state is obtained: `<UI login / token injection / cypress session reuse>`
- Mock / bypass plan: `<which external dependencies are mocked, how to enable>`

## Business capability list

### Capability: <e.g. user login>

- Page entry URL: `<path>`
- Stable selectors for key regions (prefer data-testid):
  | Element | Selector |
  | ------- | -------- |
  | username input | `[data-testid="login-username"]` |
  | password input | `[data-testid="login-password"]` |
  | submit button | `[data-testid="login-submit"]` |
- Happy path: <steps>
- Boundary / error paths: <empty input, wrong password, lockout…>
- Historical pitfalls: <e.g. async redirect after login — wait for url to contain /home>

### Capability: <next capability>

...

## Selector-robustness conventions (three layers stacked)

1. **Base**: give key interactive elements stable `data-testid`s — turns the AI
   from "guessing classes" into "looking up a contract".
2. **Middle**: locate via a11y snapshot + ref (e.g. `textbox "password" [ref=e28]`);
   LLMs should use refs, not CSS.
3. **Top**: DOM first, visual fallback — with a control tree, never go
   pure-visual; only when structure is unavailable, use screenshot-ruler
   interpolation and mark `[clickable]` to prevent misclicks.

## Freshness mechanism (preventing case-library rot)

- Testing a new feature: explore in natural language first; don't rush to freeze.
- Freezing: each round, harden 1–2 **verified-passing** cases into scripts and
  add them to the trunk regression set (`HARNESS_SMOKE_GLOB`).
- The trunk regression runs only frozen scripts; assign an owner to review
  quarterly.
