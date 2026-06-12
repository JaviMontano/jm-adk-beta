<!-- distilled from alfa skills/schema-evolution -->
<!-- > -->
# Schema Evolution
> "Method over hacks."
## TL;DR
Evolve a live schema without breaking readers/writers: expand-then-contract migrations, backward/forward compatibility, explicit versioning, zero-downtime cutover. [EXPLICIT]

## Anti-Scope
Not for: greenfield schema design, one-off ad-hoc DDL with no live consumers, or data-quality rules (see `data-quality`). [EXPLICIT]

## Compatibility Contract
- **Backward** = new schema reads old data. **Forward** = old schema reads new data. **Full** = both. [EXPLICIT]
- Default target: **backward-compatible** changes only on shared tables/topics. [EXPLICIT]
- Safe (non-breaking): add nullable/defaulted column, add table, widen type (int→bigint), add enum value at end. [INFERENCIA]
- Breaking (forbidden without contract bump): drop/rename column, narrow type, add NOT NULL without default, reorder positional fields, remove enum value. [INFERENCIA]

## Procedure
### Step 1: Discover
- Inventory consumers (services, jobs, BI, replicas) and the version each pins. Map who reads vs. writes the target. [EXPLICIT]
- Classify the change as safe or breaking against the Compatibility Contract above. [EXPLICIT]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV; choose the migration pattern (below) with the least-breaking path. [EXPLICIT]
- **Expand → Migrate → Contract**: add new shape, dual-write/backfill, switch reads, then remove old shape only after all consumers cut over. [EXPLICIT]
### Step 3: Execute
- Apply DDL/registry change with evidence tags; deploy code that tolerates both old and new shapes before data moves. [EXPLICIT]
- Backfill in idempotent, resumable batches; keep dual-write until reader cutover is verified. [EXPLICIT]
### Step 4: Validate
- Verify quality criteria; confirm no consumer errors across a full read/write cycle, then schedule contract (drop) for a later release. [EXPLICIT]

## Migration Patterns (decision)
| Pattern | When | Trade-off |
|---------|------|-----------|
| Expand/contract | Rename, type change, NOT NULL | Safest; needs 2+ releases + backfill window [INFERENCIA] |
| Dual-write | Splitting/merging columns or tables | Temporary write amplification + drift risk [INFERENCIA] |
| Versioned schema (v1/v2 side-by-side) | Event/API contracts, registry | More surfaces to maintain until v1 retired [INFERENCIA] |
| In-place additive | Pure add (nullable col, new topic field) | Cheapest; only valid when strictly non-breaking [INFERENCIA] |

## Versioning
- Bump a contract version on every breaking change; never mutate a published version in place. [EXPLICIT]
- Registry compat mode: set BACKWARD (consumers upgrade first) or FORWARD (producers upgrade first) — pick per who deploys first. [INFERENCIA]

## Quality Criteria
- [ ] Change classified safe/breaking against Compatibility Contract
- [ ] All consumers + pinned versions inventoried
- [ ] Rollback path defined (additive change reversible without data loss)
- [ ] Backfill idempotent and resumable
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output

## Usage

Example invocations:

- "/schema-evolution" — Run the full schema evolution workflow
- "schema evolution on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes a maintenance/backfill window exists for contract steps [SUPUESTO]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Unknown/unreachable consumers | Block contract step; treat as breaking until inventory complete |
| Backfill fails mid-run | Resume from last committed batch; never re-run non-idempotently |
| Reader cutover incomplete | Hold dual-write; do not drop old shape |
| Type widening with overflow risk | Validate max values before in-place change |
