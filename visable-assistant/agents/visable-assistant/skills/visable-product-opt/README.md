# Visable Product Optimization Skill

Diagnose and optimize wlw/ep product listings — titles, descriptions, and product attributes.

**Batch processing:** Scans products in configurable batches (default 50, max 200). All diagnosis, attribute extraction, content optimization, and update operations are processed in parallel within each batch — no sequential polling.

Author: David

---

## Directory Structure

```
visable-product-opt/
├── SKILL.md                              # Main skill entry — workflow, MCP tools, pagination logic
├── display.txt                           # Skill metadata (name, icon, version)
├── README.md                             # This document (English)
├── README-CN.md                          # 中文文档
└── reference/
    ├── quality-checker.md                # Diagnosis rules (title, description, attributes, images, staleness, price/MOQ)
    ├── content-optimizer.md              # Title & description optimization prompts (hard constraints)
    └── product-structure.md              # Product JSON key fields & edit link format
```

### File Responsibilities

| File | Role |
|------|------|
| `SKILL.md` | Orchestration: batch pagination → parallel diagnosis → parallel attribute extraction → batch optimization → approval → parallel update |
| `quality-checker.md` | Diagnosis rules (title, description, attributes, images, staleness, price/MOQ) |
| `content-optimizer.md` | Two self-contained prompts (title + description) with hard filters, evidence-only, sanitization |
| `product-structure.md` | Maps product JSON fields to diagnosis variables; defines edit link URLs for ep/wlw |

---

## Workflow Flowchart

```mermaid
flowchart LR
    A([Start]):::se --> C[1 Fetch batch]:::fet --> D[2 Diagnose ∥]:::dia

    D --> E{Issues?}:::dec
    E -- No --> F{More?}:::dec
    F -- Yes --> C
    F -- No --> G([No issues]):::ok

    E -- Yes --> H[3 Attr extract ∥]:::pv --> I[4 Optimize]:::opt --> J[5 Report]:::rpt

    J --> K{6 Which fields?}:::dec
    K -- "title / desc / attr" --> L[7 Push MCP ∥]:::upd --> M{8 Next?}:::dec
    K -- Skip --> M

    M -- Yes --> C
    M -- No --> N([End]):::se

    classDef se fill:#6C757D,color:#fff,stroke:#495057
    classDef fet fill:#6610F2,color:#fff,stroke:#520DC2
    classDef dia fill:#D63384,color:#fff,stroke:#AB296A
    classDef dec fill:#FFC107,color:#000,stroke:#E0A800
    classDef pv fill:#20C997,color:#fff,stroke:#1AA179
    classDef opt fill:#0DCAF0,color:#000,stroke:#0AA2C0
    classDef rpt fill:#198754,color:#fff,stroke:#146C43
    classDef upd fill:#FD7E14,color:#fff,stroke:#CA6510
    classDef ok fill:#198754,color:#fff,stroke:#146C43
```

> The `∥` symbol indicates parallel processing steps (multiple items processed at the same time).

---

## Diagnosis Rules Overview

```mermaid
flowchart LR
    subgraph Title["Title (TTL)"]
        style Title fill:#EBF5FB,stroke:#2E86C1,stroke-width:2px
        T1[Not empty ≥10]:::critical
        T2[Core term]:::critical
        T3[No stuffing]:::high
        T4[Spelling]:::high

    end

    subgraph Desc["Description (DESC)"]
        style Desc fill:#FDF2E9,stroke:#E67E22,stroke-width:2px
        D1[Min 100 words]:::medium
        D2[No stuffing]:::medium
        D3[No placeholder]:::high
    end

    subgraph Info["Other Checks"]
        style Info fill:#EAFAF1,stroke:#27AE60,stroke-width:2px
        P1[Attributes missing]:::high
        P2[Images missing]:::high
        P3[Outdated 180d]:::medium
        P4[Price missing]:::low
        P5[MOQ missing]:::low
    end

    Title --> Score
    Desc --> Score
    Info -.-> Score

    Score[/"Detect issues\nReport to supplier"/]:::scoring

    classDef critical fill:#DC3545,color:#fff,stroke:#B02A37,stroke-width:2px
    classDef high fill:#FD7E14,color:#fff,stroke:#CA6510,stroke-width:2px
    classDef medium fill:#FFC107,color:#000,stroke:#E0A800,stroke-width:2px
    classDef low fill:#6C757D,color:#fff,stroke:#495057,stroke-width:1px
    classDef scoring fill:#6610F2,color:#fff,stroke:#520DC2,stroke-width:2px
```

---

## Simulated Interaction

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant A as Agent
    participant API as MCP API

    rect rgb(235, 245, 251)
    Note over U,API: Turn 1 — Trigger & Fetch
    U->>A: I want to diagnose product quality for a wlw supplier
    A->>API: visable_list_products(page=1, pageSize=50)
    API-->>A: 50 products returned
    A->>A: Run quality-checker rules on batch
    A->>U: Batch 1 complete: 8 products with issues
    end

    rect rgb(253, 243, 226)
    Note over U,API: Turn 2 — Diagnosis Report
    A->>API: visable_extract_pv (2 products, in parallel)
    API-->>A: Suggested product attributes
    A->>A: Generate optimized titles & descriptions (all at once)
    Note right of A: Report includes:<br/>- Batch summary<br/>- Outdated products table<br/>- Missing images/price/MOQ tables<br/>- Missing attributes + suggestions<br/>- Title issues + suggested titles<br/>- Description before/after sections<br/>- All rows have [Edit] links
    A->>U: 8 products with issues found.<br/>Would you like me to apply these<br/>and update them in Product Editor?<br/>(title / description / attributes, pick any)
    end

    rect rgb(244, 236, 247)
    Note over U,API: Turn 3 — User Decision
    U->>A: Update titles + attributes for #1 and #2. Skip the rest.
    A->>API: visable_update_product (#1 + #2, parallel)
    API-->>A: Both success
    A->>U: 2 updated (title + attributes), 6 skipped.<br/>M more products remaining.<br/>Continue scanning?
    end

    rect rgb(235, 245, 251)
    Note over U,API: Turn 4 — Continue Scanning
    U->>A: Yes, continue
    A->>API: visable_list_products(page=2, pageSize=50)
    API-->>A: 50 products returned
    A->>A: All 50 no issues — auto next page
    A->>API: visable_list_products(page=3, pageSize=50)
    API-->>A: 35 products returned (last page)
    A->>A: 2 products with issues found
    A->>U: Found 2 issues on page 3.<br/>Would you like me to update them<br/>in Product Editor?<br/>(title / description / attributes, pick any)
    end

    rect rgb(234, 250, 241)
    Note over U,A: Turn 5 — Finish
    U->>A: Ignore. I'm done.
    A->>U: Final summary:<br/>135 scanned, 10 issues,<br/>2 updated, 8 skipped, 3 pages
    end
```

### Full Conversation Example

Below is a complete multi-turn conversation showing exactly what the user sees.

---

**🧑 User:**

> Help me check my product listings

**🤖 Agent:**

> Scanning your product catalog... First batch of 50 products loaded. Running quality checks...
>
> Batch 1 scanned: **6 products** with issues found.

**Batch Summary:**

| Metric | Count |
|--------|-------|
| Products scanned (this batch) | 50 |
| Products with issues | 6 |
| Title issues | 2 |
| Description issues | 2 |
| Missing attributes | 2 |
| Missing images | 1 |
| Outdated (180+ days) | 2 |
| Missing price | 1 |
| Missing MOQ | 1 |

**Outdated Products (180+ days since last edit):**

| # | Product Title | Last Updated | Link |
|---|--------------|-------------|------|
| 1 | Industrieventil DN50 | 2024-09-12 | [Edit](https://www.wlw.de/de/...) |
| 2 | Dichtungsring NBR | 2024-08-03 | [Edit](https://www.wlw.de/de/...) |

**Products Missing Images:**

| # | Product Title | Link |
|---|--------------|------|
| 1 | Stahlrohr nahtlos | [Edit](https://www.wlw.de/de/...) |

**Products Missing Price:**

| # | Product Title | Link |
|---|--------------|------|
| 1 | Trennscheibe 125 mm | [Edit](https://www.wlw.de/de/...) |

**Missing Attributes (with Suggested Attributes):**

| # | Product Title | Suggested Attributes | Link |
|---|--------------|---------------------|------|
| 1 | Hydraulikpumpe | Material: Stahl, Gusseisen; Druck: 250 bar; Typ: Zahnradpumpe | [Edit](https://www.wlw.de/de/...) |
| 2 | Stahlrohr nahtlos | Material: Edelstahl, Kohlenstoffstahl; Durchmesser: 50 mm, 100 mm; Norm: DIN 2448 | [Edit](https://www.wlw.de/de/...) |

**Title Issues:**

| # | Current Title | Issues | Suggested Title | Link |
|---|--------------|--------|----------------|------|
| 1 | BEST Cutting Disc!! FREE SHIPPING | Promotional phrases, special characters | Trennscheibe - Stahl - 125 mm | [Edit](https://www.wlw.de/de/...) |
| 2 | Pumpe | Title too short | Hydraulikpumpe - Zahnradpumpe - 250 bar | [Edit](https://www.wlw.de/de/...) |

**Description Optimization:**

---

**Product #1: [BEST Cutting Disc!! FREE SHIPPING](https://www.wlw.de/de/...)**

Issues: Placeholder text, too short (23 words, minimum 100)

**Current description:**
> coming soon, more details to follow...

**Suggested description:**
> Die Trennscheibe eignet sich fuer den Einsatz bei Stahlwerkstoffen bis 5 mm Materialstaerke. Hohe Schnittleistung und lange Standzeit durch optimierte Kornmischung.
> - Durchmesser: 125 mm
> - Dicke: 1 mm
> - Max. Drehzahl: 12.250 U/min
> - Sicherheitsnorm: EN 12413

---

**Product #2: [Pumpe](https://www.wlw.de/de/...)**

Issues: Too short (15 words, minimum 100), missing technical details

**Current description:**
> Hochwertige Pumpe fuer industrielle Anwendungen. Kontaktieren Sie uns fuer Details.

**Suggested description:**
> Die Hydraulikpumpe vom Typ Zahnradpumpe eignet sich fuer den Einsatz in hydraulischen Antriebssystemen mit einem Betriebsdruck von bis zu 250 bar.
> - Typ: Zahnradpumpe
> - Max. Betriebsdruck: 250 bar
> - Foerdervolumen: 20 l/min
> - Anschluss: G 1/2"

---

> **Would you like me to apply these suggestions and update them directly in Product Editor?**
>
> You can choose what to update:
> - **Title** — apply suggested title improvements
> - **Description** — apply suggested description improvements
> - **Attributes** — apply extracted product attributes
>
> Pick any combination, e.g. "update titles and attributes for all", "update everything for #1 and #2", or "only update descriptions".

---

**🧑 User:**

> Update titles and attributes for #1 and #2

**🤖 Agent:**

> Done! 2 products updated (titles + attributes). 4 products skipped.
>
> You have **85 more products** remaining. Would you like me to continue scanning the next batch?

---

**🧑 User:**

> Yes, continue

**🤖 Agent:**

> Scanning batch 2 (50 products)... no issues found. Auto-scanning batch 3...
>
> Batch 3 scanned (35 products, last page): **2 products** with issues found.
>
> *(shows report for batch 3...)*
>
> Would you like me to update them in Product Editor?

---

**🧑 User:**

> No thanks, I'm done

**🤖 Agent:**

> **Final Summary:**
>
> | Metric | Count |
> |--------|-------|
> | Total products scanned | 135 |
> | Total issues found | 8 |
> | Products updated | 2 |
> | Products skipped | 6 |
> | Batches scanned | 3 |
>
> All done! You can click the [Edit] links above anytime to manually review the remaining products.

---

## Key Features

| Feature | Description |
|---------|-------------|
| Batch parallel processing | Diagnosis, attribute extraction, content generation, and updates all run in parallel — no sequential polling |
| Configurable batch size | Default 50, max 200, user can customize |
| Selective checks | User can specify which checks to run (e.g. "only check titles", "only check attributes"), skip the rest |
| Granular field updates | Title, description, and attributes can be updated in any combination; user can also pick specific products by row number |
| Auto-pagination | If no issues found in current batch, automatically scan the next batch until issues are found or all products are scanned |
| Long description display | Description before/after comparisons are shown as separate sections, not crammed into table cells |
| Multi-value attribute merging | When an attribute has multiple values, they are combined into one line (e.g. Material: Steel, Cast Iron) |
| Multi-language support | Conversation language follows the user; product optimization language follows the product's own language |
