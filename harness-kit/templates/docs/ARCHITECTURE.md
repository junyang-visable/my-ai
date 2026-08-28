# ARCHITECTURE.md — architecture knowledge, loaded on demand

> Not part of the always-present AGENTS.md context; agents read this only for
> architecture-touching changes. Organize by **business capability**, never by
> technical layering — organize by tech layer and AI code-location precision
> collapses (measured: single-digit %), organize by capability and it soars.

## System boundaries

<one diagram or paragraph: external systems, upstream/downstream, data flow>

## Business capability map

- Capability A: <what it does> — entry code `<path>`, key concepts `<...>`
- Capability B: <what it does> — entry code `<path>`
- …

## Layers & dependency direction

<allowed dependency directions; which layer must not depend on which —
this part is mechanically enforced by .harness/feedback/lint-arch.sh>

## Key conventions / contracts

<data contracts / API contracts / event contracts, pointing at the SSOT definitions>
