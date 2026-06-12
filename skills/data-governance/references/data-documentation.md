<!-- distilled from alfa skills/data-documentation -->
<!-- > -->
# Data Documentation
> "Method over hacks."
## TL;DR
Produce living data dictionaries, schema docs, and column-level lineage so every field has a known meaning, owner, and source. [EXPLICIT]
**Done = no orphan columns**: each column has type, description, owner, and upstream source recorded. [EXPLICIT]

## Deliverables
- **Data dictionary** — per dataset: column, type, nullability, description, PII flag, owner, source. [EXPLICIT]
- **Schema doc** — DDL/contract + version + change history; the source of truth for shape. [EXPLICIT]
- **Lineage map** — source → transform → sink at column grain, enough to answer "where did this number come from?". [EXPLICIT]
- **Glossary** — business terms ↔ physical columns, to kill synonym drift (e.g. `rev` vs `revenue_usd`). [EXPLICIT]

## Procedure
1. **Inventory** — enumerate datasets/tables; capture schema from DDL, catalog API, or profiling, not memory. [EXPLICIT]
2. **Annotate** — fill meaning, owner, PII flag, allowed values per column; flag unknowns rather than guessing. [EXPLICIT]
3. **Trace lineage** — follow each field upstream; record transforms (joins, derivations, filters). [EXPLICIT]
4. **Cross-check** — reconcile docs vs live schema; every mismatch is a defect to resolve. [EXPLICIT]
5. **Publish + version** — store next to the data, version it, set a re-review cadence. [INFERENCIA]

## Acceptance Criteria
- [ ] Every column has type, description, and owner; zero blanks. [EXPLICIT]
- [ ] All PII/sensitive fields flagged and classified. [EXPLICIT]
- [ ] Lineage resolves to a named source system per field (no "unknown"). [EXPLICIT]
- [ ] Doc schema == live schema at publish time (drift = 0). [EXPLICIT]
- [ ] Business glossary terms map 1:1 to physical columns. [EXPLICIT]
- [ ] Evidence tags applied; Constitution XIII/XIV compliant. [EXPLICIT]

## Worked Example
Dictionary row: `orders.total_amount` · `DECIMAL(12,2)` · NOT NULL · "Order gross in USD incl. tax" · PII=no · owner=`@data-rev` · source=`stripe.charges.amount/100`. [EXPLICIT]
Lineage: `stripe.charges.amount` (cents) → `stg_charges` (÷100) → `fct_orders.total_amount`. The `÷100` transform must be documented or the figure reads 100x high. [EXPLICIT]

## Decisions & Trade-offs
- **Auto-generated vs hand-written**: generate skeleton from catalog/profiling for coverage, then hand-annotate meaning — generators capture shape but never intent. [INFERENCIA]
- **Docs-as-code (in-repo) vs catalog UI**: in-repo wins for review/version/diff; catalog UI wins for discovery. Default to docs-as-code, sync to catalog. [SUPUESTO]
- **Column-grain lineage vs table-grain**: column-grain costs more upfront but is the only grain that answers impact-analysis questions. Prefer column-grain for regulated/financial fields. [EXPLICIT]

## Failure Modes
- **Drift** — docs silently diverge from schema → gate publish on a doc-vs-schema diff in CI. [EXPLICIT]
- **Tribal knowledge** — meaning lives only in one engineer's head → owner field forces accountability. [EXPLICIT]
- **Synonym sprawl** — same concept, many column names → glossary as single source. [EXPLICIT]
- **PII leakage** — undocumented sensitive field exported → PII flag is mandatory, default unknown→treat as PII. [EXPLICIT]

## Usage

Example invocations:

- "/data-documentation" — Run the full data documentation workflow
- "data documentation on this project" — Apply to current context

## Assumptions & Limits
- Assumes read access to schemas/catalog/sample data; profiling needs a representative sample. [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Documents structure and lineage; does **not** fix data-quality defects (see data-quality) or set retention (see audit-trail-design). [EXPLICIT]
- Generated descriptions are drafts; a domain owner must confirm semantics before sign-off. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request schema/catalog access before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Doc vs live schema mismatch | Treat as defect; trust live schema, fix the doc |
| Undocumented / ambiguous column | Mark `unknown`, assign owner to resolve; never invent meaning |
| Sensitive field, unclear class | Default to PII/restricted until classified |
