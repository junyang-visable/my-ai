---
name: ga4-tracking-validation
description: >-
  3-step workflow for validating GA4 tracking events: generate a validation checklist HTML from Cypress scripts, capture actual dataLayer JSON from staging, then compare and update the HTML with check results. Use when validating GA4 tracking, checking cy.validateEvent calls, running tracking QA, or working with blueprint/config/cy.js files in a GA4 tracking project.
---

# GA4 Tracking Validation

3-step workflow for validating GA4 tracking implementation against contracts.

## File naming conventions

Given a Cypress script `{abcd}.cy.js`:
- **Blueprint**: `ga4-1platform-tracking/{abcd}.js`
- **Config JSON**: `tracking-contracts/implementations/web/{abcd}.json`
- Blueprint is the **single source of truth** when config and blueprint conflict.

---

## Step 1 — Generate Validation Checklist HTML

Analyze all `cy.validateEvent` calls in the target `.cy.js` script and produce a 5-column HTML table.

### Table columns

| Column | Content |
|--------|---------|
| `config_title` | First arg of `cy.validateEvent('title', config)` |
| `config` | Second arg as a JavaScript object (actual config) |
| `good case` | A complete JS object that passes the config validation |
| `description` | Concise English description of the case for developers |
| `comment` | Notes; flag any config↔blueprint conflicts here |

### Rules
- **Skip** events whose `config_title` starts with `app_banner`.
- **Deduplicate** — list each unique event once.
- If config and blueprint conflict, use blueprint values and note in `comment`.
- Save as an HTML file in the **project root directory**.

### Prompt template

```
Help me analyze all cy.validateEvent calls in the target Cypress script below and produce a 5-column HTML table following these rules:
1. config_title: first arg of cy.validateEvent (skip events starting with 'app_banner')
2. config: second arg as a JS object
3. good case: a complete JS object that passes validation
4. description: concise English description of the case
5. comment: notes; flag config↔blueprint conflicts (blueprint = source of truth)
Deduplicate events. Save output as HTML to project root.

The target cy script is: @{abcd}.cy.js
```

---

## Step 2 — Capture DataLayer JSON from Staging

1. Open the staging environment page and **log in first** (avoids triggering logged-in-only event checks).
2. Perform interactions to trigger events.
3. Run the filter in the browser console and copy the result:

```js
dataLayer.filter(item => {
  if (!item.event || item.event === 'genericEvent' || item.event === 'pageView'
      || item.event.startsWith('CookieScript') || item.event.startsWith('gtm.')) return false;
  if (item.ecommerce !== null) return true;
  const keys = Object.keys(item);
  return !(keys.length === 1 && keys[0] === 'ecommerce');
})
```

4. Save the copied JSON as a `.json` file in the project directory.

---

## Step 3 — Compare and Update HTML

Add / overwrite a **"Check Result"** column in the HTML table.

### Matching logic
Match each checklist row to the most relevant JSON event using: `event`, `event_type`, `event_position`, `ecommerce.item_list_name`, `ecommerce.items[].item_name / item_variant / promotion_name`.

### Result values

| Result | Condition |
|--------|-----------|
| `checked` | Found and passes all validations |
| `not found` | No matching event in JSON |
| error description | Found but has issues (see below) |

### Validation error format
Number each issue, one per line:
1. Missing parameter `xx`
2. Parameter `xx` should be `[allowed enums]`, but got `actual value`

Distinguish between **"parameter missing"** and **"parameter value is empty (null/undefined)"**.

For content not explicitly in config, apply Layer 1 and Layer 2 checks.

**Append the raw matched JSON object** at the end of every non-`not found` cell.

### Known issues to ignore
- `Schema /internal_user: must be boolean`
- `Schema /app_version: must match pattern "^\d+(\.\d+)*$"`
- Config missing Layer 3 expected values for loose fields
- Previous dataLayer entry should be `ecommerce: null`
- Transformation rules in `tracking-contracts/parameters/policy.json`

### Prompt template

```
You now have the HTML checklist. I will provide a JSON file of all actually reported events.
Search the JSON for matching events per checklist row. Add/overwrite a "Check Result" column:
- not found: no matching event
- checked: found and passes all validations
- otherwise: numbered list of issues (distinguish missing vs null; show allowed enum + actual value for enum mismatches)
Apply Layer 1 & 2 checks for fields not explicitly in config.
Append the raw matched JSON object at end of every non-not-found cell.
Ignore known issues listed in the skill.
Match using: event, event_type, event_position, ecommerce.item_list_name, ecommerce.items[].item_name/item_variant/promotion_name.

The JSON file is: @{filename}.json
The checklist is: @{filename}.html
```
