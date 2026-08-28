# Acceptance Rubric template (four levels + E2E four-layer weighting)

> Acceptance criteria must exist **before the code**, and the session writing
> the implementation never reads this (role isolation — see
> anti-false-reporting.md). Copy to `.harness/tasks/<task>/rubric.md`; the
> Evaluator role fills it in and rules on it.

## Four levels & weights

| Level | Weight | Meaning | On FAIL |
| ----- | ------ | ------- | ------- |
| Essential | 1.0 | core functionality; missing = failure | any FAIL → feed back for a fix, until all PASS |
| Pitfall | 0.9 | known high-frequency pitfalls that must be avoided | any FAIL → feed back for a fix |
| Important | 0.7 | important but not fatal | counts against the score |
| Optional | 0.3 | nice-to-have | counts against the score |

**Pass criteria (all three at once)**:
1. weighted total ≥ threshold (0.85 suggested; tune as needed);
2. every Essential item PASS;
3. trigger accuracy 100% (what should trigger, triggers; what shouldn't, doesn't).

## E2E four-layer score (copy as-is)

| Dimension | Weight |
| --------- | ------ |
| Functional correctness | 0.40 |
| Robustness (errors / boundaries / concurrency) | 0.25 |
| UI presentation | 0.20 |
| Interaction quality | 0.15 |

## Checklist (fill per requirement)

### Essential (weight 1.0)

- [ ] E-1: <core behavior, an observable assertion>
- [ ] E-2: <...>

### Pitfall (weight 0.9)

- [ ] P-1: <guard against a historical pitfall, e.g. "login failure must not swallow the exception">

### Important (weight 0.7)

- [ ] I-1: <...>

### Optional (weight 0.3)

- [ ] O-1: <...>

## Verdict record (filled by the Evaluator)

| Item | Result | Evidence (screenshot/assertion/log path) |
| ---- | ------ | ----------------------------------------- |
| E-1 | PASS/FAIL | `.harness/tasks/<task>/evidence/...` |

- weighted total: `<x.xx>` / threshold `<0.85>`
- all Essential passed: `<yes/no>`
- trigger accuracy: `<100%/...>`
- **verdict**: `PASS / feed back for a fix / ESCALATED`
