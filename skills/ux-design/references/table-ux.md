<!-- distilled from alfa skills/table-ux -->
<!-- > -->
# Table Ux
> "Method over hacks."
## TL;DR
Audit and improve data tables: column model, sorting, filtering, pagination vs infinite scroll, responsive collapse, row selection, bulk actions, and empty/loading/error states. Output a prioritized, evidence-tagged plan. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather table context: row volume (typical + max), column count, data types per column, primary user task (scan / compare / act), device mix, and whether rows are selectable/actionable. [DOC]
- If row volume and primary task are unknown, stop and ask — a 20-row reference table and a 500k-row admin grid need opposite patterns. [INFERENCIA]
### Step 2: Analyze
- Audit against the task: is the default sort meaningful, are filters reachable, is pagination sized to the task, do bulk actions exist where rows are actionable, does the layout survive a narrow viewport.
- Classify each column: identifier, sortable metric, filterable category, or action. Right-align numerics, left-align text, never center body data. [INFERENCIA]
### Step 3: Execute
- Produce a prioritized plan: blocking issues first (no empty state, no loading state, unusable on mobile), then friction (weak sort defaults, hidden filters), then polish.
- Specify the responsive strategy explicitly (see Decisions) rather than letting the table overflow horizontally by default. [INFERENCIA]
### Step 4: Validate
- Verify every state renders: populated, empty, loading, error, single-row, and max-volume. Verify keyboard reachability of sort, filter, pagination, and bulk actions.

## Quality Criteria
- [ ] Evidence tags applied (Alfa core set, one tag per claim)
- [ ] Constitution-compliant
- [ ] Actionable output (every finding maps to a concrete change)
- [ ] Empty, loading, and error states all specified — not just the happy path
- [ ] Responsive strategy named (not implicit horizontal scroll)
- [ ] Bulk actions present wherever rows are individually actionable

## Acceptance Criteria (measurable)
- Default sort is meaningful for the primary task (recency, priority, or relevance), never arbitrary insertion order. [INFERENCIA]
- Numeric columns are right-aligned and share a decimal/unit convention per column. [DOC]
- Pagination page size matches the task; "select all" on a paged table clarifies whether it spans the page or the full result set. [INFERENCIA]
- Filtering and sorting state survives navigation back to the table; the user does not re-filter from scratch. [INFERENCIA]
- Empty state explains why it is empty (no data yet vs filtered-to-zero) and offers the next action. [DOC]
- Every bulk action shows the affected count and is reversible or confirmed before destructive execution. [INFERENCIA]

## Decisions & Trade-offs
- **Pagination vs infinite scroll** → pagination when users compare, jump, or cite a position; infinite scroll for exploratory feeds. Infinite scroll breaks "page 3", deep-linking, and footers. [INFERENCIA]
- **Horizontal scroll vs column priority vs stacked cards (mobile)** → drop low-priority columns or stack rows into cards; horizontal scroll hides data off-screen and is the worst default. Pick by how many columns are task-critical. [INFERENCIA]
- **Client-side vs server-side sort/filter/page** → client-side only when the full set fits in memory (~hundreds of rows); beyond that, server-side, and the UI must show loading per fetch. [SUPUESTO] Verify against actual row volume.
- **Sticky header / first column** → sticky header once rows exceed a viewport; sticky identifier column when horizontal scroll is unavoidable, so rows stay legible. [INFERENCIA]
- **Row click vs explicit action** → make the whole row clickable only when there is one obvious action; otherwise use explicit controls so selection and navigation do not collide. [INFERENCIA]

## Worked Example
Table: 500-row order admin, single default insertion sort, 14 columns overflowing horizontally on mobile, no empty/loading state, delete is per-row only. [SUPUESTO]
Audit output:
1. Default-sort by order date descending; make status and total sortable. [INFERENCIA]
2. Mobile: keep order id + status + total, drop the rest behind a row expander. [INFERENCIA]
3. Add loading skeleton and a filtered-to-zero empty state with a "clear filters" action. [DOC]
4. Add row selection + bulk "mark shipped" / "cancel" with affected-count confirmation. [INFERENCIA]
5. Server-side sort/filter/page (500 rows is borderline; grows). [SUPUESTO]

## Usage

Example invocations:

- "/table-ux" — Run the full table ux workflow
- "table ux on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Anti-scope: does not write production table code, run virtualization benchmarks, or measure real scan/comparison times — it audits and recommends. [INFERENCIA]
- Accessibility is in scope at the structural level (semantic table, sortable headers, keyboard reach); full WCAG audit is a separate skill. [SUPUESTO]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Unknown / unbounded row volume | Assume server-side; require loading + virtualization before approving client-side |
| Single row or single column | Question whether a table is the right component at all |
| Very wide table (>10 columns) | Apply column priority; never approve raw horizontal scroll on mobile |
| Mixed selection + row-navigation | Separate the checkbox/affordance from the row-click target |
| Destructive bulk action | Require affected count + confirm; offer undo where feasible [INFERENCIA] |
| Async sort/filter latency | Show per-fetch loading; preserve prior rows until new data arrives [INFERENCIA] |
