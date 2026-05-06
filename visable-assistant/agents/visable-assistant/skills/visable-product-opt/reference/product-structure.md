# Product JSON Structure — Key Fields Only

Only the fields needed for diagnosis are listed here.

## Fields Used for Diagnosis

| Field Path | Type | Purpose |
|-----------|------|---------|
| `id` | string (UUID) | Product identifier |
| `slug` | string | URL slug for product link |
| `supplierId` | string (UUID) | Supplier ID for product link |
| `data.name` | string | Product title |
| `data.description` | string | Product description (plain text) |
| `data.language` | string | Primary language (e.g. `de`, `en`) |
| `data.cpv.categoryId` | number | Platform category ID |
| `data.cpv.attributes` | array | Product attributes — empty = missing |
| `data.images` | array | Product images — reported if empty |
| `updateTime` | string (ISO 8601) | Last edit time — reported if >180 days ago |
| `data.price` | number/object | Product price — reported if missing/zero |
| `data.moq` | number | Minimum order quantity — reported if missing/zero |
| `data.translations.name.en` | string | English title (fallback for diagnosis) |
| `data.translations.description.en` | string | English description (fallback) |

## Product Edit Link

Based on the product's `site` field:

- **Europages (ep):**
  `https://www.europages.co.uk/<lang>/my-account/supplier/<supplierId>/products-services/product?productId=<id>`
- **wlw:**
  `https://www.wlw.de/<lang>/my-account/supplier/<supplierId>/products-services/product?productId=<id>`

Where `<lang>` = `data.language` (e.g. `de`, `en`, `fr`).
