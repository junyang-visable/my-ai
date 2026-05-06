# Quality Checker — Diagnosis Rules

Based on **Visable Product Quality Scoring Rules — Phase 1**.

The agent evaluates each product against these rules. Any rule that fails is reported as a plain-language issue. Scores are **not shown** to suppliers — severity levels guide which issues to highlight first.

Severity: **Critical** > **High** > **Medium** > **Low**.

---

## 1. Title Rules

| ID | Name | Condition | Severity |
|----|------|-----------|----------|
| TTL-001 | Title not empty | `len(title) >= 10` | Critical |
| TTL-002 | Max length | `len(title) <= 150` | High |
| TTL-003 | Recommended length | `len(title) >= 30` | Low |
| TTL-004 | Core product term | At least 1 category noun in title | Critical |
| TTL-005 | No keyword stuffing | No word repeated > 3 times | High |
| TTL-006 | No all-caps | Uppercase ratio <= 30% (excl. acronyms) | Medium |
| TTL-007 | No promo phrases | No "best/hot/free shipping/sale/discount/cheapest" | Medium |
| TTL-008 | No special chars | No `~ ! * $ ? _ { } ^ \` in title | Low |
| TTL-009 | Spelling check | Max 1 misspelled word (excl. brands/acronyms) | High |

---

## 2. Description Rules

| ID | Name | Condition | Severity |
|----|------|-----------|----------|
| DESC-001 | Min word count | `word_count(desc) >= 100` | Medium |
| DESC-002 | Recommended words | `word_count(desc) >= 300` | Low |
| DESC-003 | Structured elements | Has table, bullet list, or numbered list | Low |
| DESC-004 | No keyword stuffing | No keyword > 5% of word count | Medium |
| DESC-005 | No placeholder text | No "lorem ipsum / TBD / coming soon" | High |

---

## 3. Attribute Check

The agent checks whether `data.cpv.attributes` is empty. If empty, call the attribute extraction API (`visable_extract_pv`) to get suggested attributes.

---

## 4. Image Check

| Check | Condition | Report Action |
|------|-----------|---------------|
| No images | `data.images` is empty or absent | List in "Missing Images" table |

---

## 5. Staleness Check

| Check | Condition | Report Action |
|------|-----------|---------------|
| Not updated for 180+ days | `updateTime` is more than 180 days ago | List in "Outdated Products" table |

---

## 6. Price & MOQ (Detection Only)

> **Per the Phase 1 spec, Price and MOQ are NOT part of the base quality score.** They belong in the Phase 2 Competitiveness Bonus layer. Visable is inquiry-driven — many legitimate products do not have fixed pricing or MOQ.
>
> The agent **lists** missing price/MOQ as separate items in the report so suppliers are aware.

| Check | Condition | Report Action |
|------|-----------|---------------|
| Missing price | `price` is absent or zero | List in "Missing Price" table |
| Missing MOQ | `moq` is absent or zero | List in "Missing MOQ" table |

---

## How the Agent Uses These Rules

The agent evaluates each rule against the product data. Any rule that fails is reported as a plain-language issue to the supplier. **Scores and tiers are NOT shown to the supplier** — the agent only presents the detected issues and suggested fixes.

The severity levels guide **which issues to highlight first** (Critical/High before Medium/Low).

---

## Constants

```
PROMO_PHRASES = ["best", "hot", "free shipping", "sale", "discount", "cheapest",
                 "buy now", "limited offer", "best seller", "top selling",
                 "wholesale", "factory price", "lowest price"]

SPECIAL_CHARS = {'~', '!', '*', '$', '?', '_', '{', '}', '^', '\\'}

KNOWN_ACRONYMS = ["ISO", "CE", "LED", "LCD", "USB", "HDMI", "PVC", "UV",
                  "AC", "DC", "OEM", "ODM", "CNC", "FDA", "SGS", "BPA",
                  "ROHS", "UL", "TUV", "DIN", "ANSI", "ASTM", "EN", "IP"]

PLACEHOLDER_PATTERNS = [r"lorem\s+ipsum", r"\bTBD\b", r"coming\s+soon",
                        r"to\s+be\s+(added|updated|completed)",
                        r"insert\s+(text|description|content)\s+here",
                        r"placeholder"]
```
