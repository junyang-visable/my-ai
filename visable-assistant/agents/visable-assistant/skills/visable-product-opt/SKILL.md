---
name: visable-product-opt
author: David
version: 1.1.0
description: |
  Diagnose and optimize wlw/Europages product listings — titles, descriptions, and product attributes.
  Scans a supplier's catalog in batches of 50, checks each product against quality rules, generates improved
  titles and descriptions, detects missing attributes/price/MOQ, and optionally pushes updates back to the platform.

  Trigger scenarios (case-insensitive) — activate when user mentions ANY of:
    - General product/listing references: "product", "products", "listing", "listings", "catalog", "product content", "my products", "my listings"
    - Optimization: "optimize", "optimization", "improve", "fix", "better titles", "better descriptions", "batch optimization", "bulk optimization"
    - Diagnosis/audit: "diagnose", "diagnosis", "audit", "check", "scan", "review", "quality", "HQ status", "completeness"
    - Specific issues: "missing information", "missing attributes", "missing images", "missing price", "missing MOQ", "outdated", "not updated"
  Important: This skill focuses on diagnosis and optimization of existing products.
enabled: true
---

# Visable Product Optimization

Diagnose product quality and generate optimized titles/descriptions for a Visable(wlw/Europages) supplier's catalog.

## Workflow Overview

```
1. Fetch products in batch (default 50, max 200)
2. Diagnose batch in parallel (all checks at once, or only user-selected checks)
3. If no issues → auto-fetch next batch; repeat until issues found or all done
4. For attribute-missing products → call attribute extraction in parallel
5. Generate optimized title/description for all products with issues (in one pass)
6. Present diagnosis report (summary tables + description before/after sections)
7. Ask supplier: which fields to update? (title / description / attributes — any combination)
8. User selects fields + products → push updates; or user skips
9. Ask: "Continue scanning next batch?" → yes: go to 1; no: final summary + end
```

> **Authentication:** Token is managed automatically by the Accio orchestrator. The agent does not need to request or handle tokens — they are injected at MCP call time.

## Step 1: Fetch Products (Batch of 50)

**MCP Tool:** `visable_list_products` *(placeholder — MCP not yet available)*

```
Parameters:
  - page: <currentPage>
  - pageSize: <batchSize, default 50>
```

> **Batch size:** Default is 50. If the user requests a different batch size, accept it but recommend no more than 200 to avoid performance issues.

**Key fields to extract per product:**

| Field | Source Path | Used For |
|-------|-----------|----------|
| `title` | `data.name` | Title diagnosis |
| `description` | `data.description` | Description diagnosis |
| `attributes` | `data.cpv.attributes` | Attribute completeness check |
| `images` | `data.images` | Image missing check |
| `updateTime` | `updateTime` | Staleness check (>180 days) |
| `price` | `data.price` | Price missing check |
| `moq` | `data.moq` | MOQ missing check |
| `categoryId` | `data.cpv.categoryId` | Attribute extraction |
| `language` | `data.language` | Attribute extraction, content optimization |
| `id` / `slug` / `supplierId` | top-level | Product link |

See [reference/product-structure.md](reference/product-structure.md) for full JSON structure.

> **Note:** Price and MOQ are listed separately if missing. The exact field paths may vary by API version.

## Step 2: Diagnose Batch

Read [reference/quality-checker.md](reference/quality-checker.md) for the full rule set.

### Selective Diagnosis

By default, all checks are enabled. If the user specifies they only want certain checks (e.g. "only check titles and descriptions", "only check attributes", "only check MOQ"), run ONLY the requested checks and skip the rest.

### Parallel Processing

Diagnose ALL products in the batch in parallel — do NOT evaluate products one by one sequentially. All diagnosis rules should be applied to the entire batch at once to minimize response time.

### Batch Decision Logic

- **Issues found** (any product fails the active checks) → proceed to Step 3
- **No issues found** → automatically fetch next page (go to Step 1 with `page + 1`). Repeat until issues are found or all pages exhausted.
- **All pages exhausted with no issues** → report "All products meet quality standards" and end.

## Step 3: Attribute Extraction (for attribute-missing products)

For products with empty `data.cpv.attributes`, call the attribute extraction MCP tool.

**Parallel processing:** If multiple products need attribute extraction, call `visable_extract_pv` for ALL of them in parallel — do NOT call one by one.

**MCP Tool:** `visable_extract_pv` *(placeholder — MCP not yet available)*

```
Parameters:
  - site: "wlw"
  - lang: <data.language>
  - title: <data.name>
  - description: <data.description>
  - categoryId: <data.cpv.categoryId>
  - image: <data.images[0].file.url> (omit if no images)
```

**Response format:**

```
{
  "code": 200,
  "data": {
    "result": [
      {
        "valueId": <number>,
        "valueName": <string>,
        "propertyName": <string>,
        "propertyId": <number>
      }
    ],
    "logId": <string>
  },
  "message": "success"
}
```

### Attribute Display Format

Present extracted attributes to the user as **propertyName: valueName** pairs — do NOT show IDs (`valueId`, `propertyId`).

When the same `propertyName` has multiple `valueName` values, combine them into one line:

```
Material: Stainless Steel, Carbon Steel, Aluminum
Color: Red, Blue, Green
Weight: 2.5 kg
```

> **Note:** Results are AI-generated and may vary between calls. Present them as suggestions for the supplier to review. When talking to the supplier, always say "attributes" or "product attributes" — never use internal terms like "PV", "CPV", "propertyId", or "valueId".

## Step 4: Generate Optimized Content

Read [reference/content-optimizer.md](reference/content-optimizer.md) for title/description optimization guidelines and output format.

Generate improved title and description for ALL products with detected issues in one pass — do NOT generate one product at a time sequentially.

### User-Provided Optimization Context

If the user provides their own optimization preferences or ideas during the conversation (e.g. "I want to emphasize sustainability", "add the material to the title"), treat them as **priority context** and re-generate the optimized content incorporating those preferences.

However, if the user's request would result in lower quality (e.g. adding promotional phrases, keyword stuffing, exceeding length limits, or violating any rules in content-optimizer.md), the agent MUST:
1. **Warn the user** — explain which quality rule would be violated and why it is not recommended.
2. **If the user insists** — proceed with their request, but note the quality concern in the report.

## Step 5: Present Diagnosis Report

Group findings into categorized tables with product links. Only show tables for the checks that are enabled (see Selective Diagnosis in Step 2).

### Product Edit Link Format

Determine the link based on the product's `site` field:

- **Europages (ep):**
  ```
  https://www.europages.co.uk/<lang>/my-account/supplier/<supplierId>/products-services/product?productId=<offerId>
  ```
- **wlw:**
  ```
  https://www.wlw.de/<lang>/my-account/supplier/<supplierId>/products-services/product?productId=<offerId>
  ```

Where `<lang>` = `data.language`, `<supplierId>` = `supplierId`, `<offerId>` = `id` from the product object.

### Batch Summary

Only list metrics for enabled checks:

| Metric | Count |
|--------|-------|
| Products scanned (this batch) | N |
| Products with issues | N |
| Title issues | N |
| Description issues | N |
| Missing attributes | N |
| Missing images | N |
| Outdated (180+ days) | N |
| Missing price | N |
| Missing MOQ | N |

### Outdated Products (180+ days since last edit)

| # | Product Title | Last Updated | Link |
|---|--------------|-------------|------|
| 1 | ... | 2025-06-25 | [Edit](...) |

### Products Missing Images

| # | Product Title | Link |
|---|--------------|------|
| 1 | ... | [Edit](...) |

### Products Missing Price

| # | Product Title | Link |
|---|--------------|------|
| 1 | ... | [Edit](...) |

### Products Missing MOQ

| # | Product Title | Link |
|---|--------------|------|
| 1 | ... | [Edit](...) |

### Products Missing Attributes (with Extracted Suggestions)

For each product missing attributes, show the suggested attributes as `propertyName: valueName` pairs:

| # | Product Title | Suggested Attributes | Link |
|---|--------------|---------------------|------|
| 1 | ... | Material: Stainless Steel, Carbon Steel; Color: Red, Blue | [Edit](...) |

### Title & Description Optimization

For title issues, show the comparison in the table:

| # | Product Title | Issues | Suggested Title | Link |
|---|--------------|--------|----------------|------|
| 1 | ... | Keyword stuffing, placeholder text | ... | [Edit](...) |

### Long Description Display

Do NOT put long description text (before/after) inside a markdown table cell — it is unreadable. Instead, after the summary tables above, list each product's description comparison as a separate section:

```
---
**Product #1: [Product Title](edit-link)**
Issues: Incomplete information, missing call-to-action

**Current description:**
> (original description text)

**Suggested description:**
> (optimized description text)
---
```

This ensures readability for descriptions that can be hundreds of characters long.

## Step 6: Supplier Decision

After presenting the batch report (title/description/attributes suggestions), the agent MUST ask:

> "Would you like me to apply these suggestions and update them directly in Product Editor?
>
> You can choose what to update:
> - **Title** — apply suggested title improvements
> - **Description** — apply suggested description improvements
> - **Attributes** — apply extracted product attributes
>
> You can pick any combination, e.g. 'update titles and attributes for all', 'update everything for #1, #3, #5', or 'only update descriptions'."

**Key rules:**
- The user can select any combination: title only, description only, attributes only, title + description, title + attributes, description + attributes, or all three.
- The user can also pick specific row numbers from the tables.
- Wait for explicit confirmation before executing ANY update.
- This question is **mandatory** — never skip asking for update confirmation after showing the report.

### If user agrees → execute updates (Step 7), then proceed to Step 8.

### If user declines updates

Do NOT end the session. Instead ask:

> "OK, no updates applied. There are still **M** more products to scan. Would you like me to continue checking the next batch?"

- **Yes** → go to Step 1 with `page + 1`
- **No** → present final summary and end

## Step 7: Push Updates via MCP

Based on the user's field selection from Step 6, construct the update payload with ONLY the chosen fields.

**Parallel processing:** If updating multiple products, call `visable_update_product` for ALL of them in parallel.

**MCP Tool:** `visable_update_product` *(placeholder — MCP not yet available)*

### Title Update (if user selected "title")

```
Parameters:
  - productId: <product ID>
  - updates:
      name: <new title>
```

### Description Update (if user selected "description")

```
Parameters:
  - productId: <product ID>
  - updates:
      description: <new description>
```

### Title + Description Update (if user selected both)

```
Parameters:
  - productId: <product ID>
  - updates:
      name: <new title>
      description: <new description>
```

### Attribute Update (if user selected "attributes")

Pass extracted attributes to the MCP tool using this data format:

- **Input type** (`valueId` = 0 in extraction response): `value_id` = 0, `value_text` = extracted text
- **Checkbox type** (`valueId` > 0 in extraction response): `value_id` = matched ID, `value_text` = null

```
{
  "attributes": [
    {
      "value_id": <valueId from extraction response>,
      "value_text": <valueName if valueId is 0, otherwise null>,
      "property_id": <propertyId from extraction response>,
      "property_text": null
    }
  ],
  "category_id": <data.cpv.categoryId>
}
```

All values **MUST** come from the attribute extraction API response (`data.result[]`). Do NOT use hardcoded or example values.

| Type | `value_id` | `value_text` | `property_id` | `property_text` |
|------|-----------|-------------|--------------|----------------|
| Input (valueId = 0) | 0 | Extracted text | Required | null |
| Checkbox (valueId > 0) | Matched ID | null | Required | null |

For each approved product, call the update MCP and log success/failure.

> **Note:** Update MCP endpoint is not yet implemented. Replace placeholder when available.

## Step 8: Continue or Stop

After the user has updated or skipped the current batch, ask:

> "Batch complete. You have **M** more products remaining. Would you like to continue scanning the next batch?"

- **Yes** → go to Step 1 with `page + 1`
- **No** → present a final cumulative summary and end

### Final Summary (on exit)

| Metric | Count |
|--------|-------|
| Total products scanned | N |
| Total issues found | N |
| Products updated | N |
| Products skipped | N |
| Pages scanned | N |

## Error Handling

- **API rate limit:** Back off with exponential delay
- **Partial fetch failure:** Report failed pages, continue with successful ones
- **Attribute extraction timeout:** Skip that product, note in report

## Important Notes

1. **Scope:** Current phase covers title/description optimization, attribute extraction, image/staleness checks, and price/MOQ detection.
2. **Attribute extraction coverage:** The attribute extraction model does not yet cover all product categories. If results are incomplete, note this in the report.
3. **User language:** Detect the language of the user's first message. All conversation, reports, issue descriptions, and suggestions shown to the user MUST be in the user's language. Internal processing (rules, prompts) stays in English.
4. **Product language:** Diagnose and optimize title/description in the product's primary language (`data.language`). Use `data.translations.*.en` as fallback when primary is not English. The optimized title/description output language follows the product's language, NOT the user's conversation language.
5. **Priority:** Always present the most important issues first.
6. **Performance — parallel processing is mandatory:**
   - **Diagnosis:** Apply all rules to the entire batch at once, NOT one product at a time.
   - **Attribute extraction:** Call `visable_extract_pv` for all attribute-missing products in parallel.
   - **Content generation:** Generate optimized titles/descriptions for all products with issues in one pass.
   - **Updates:** Call `visable_update_product` for all approved products in parallel.
   - **Never poll / loop sequentially** when items are independent — always batch or parallelize.
7. **Selective diagnosis:** If the user specifies which checks to run (e.g. "only check titles"), skip all other checks. The batch summary and report tables should only show the enabled checks.
8. **No IDs in user-facing output:** Never show `valueId`, `propertyId`, `propertyText`, or any internal identifier to the user. Show only `propertyName: valueName` pairs for attributes.
