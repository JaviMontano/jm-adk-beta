<!-- distilled from alfa skills/audit-trail-design -->
<!-- > -->
# Audit Trail Design
> "Method over hacks."

## TL;DR
Design append-only, tamper-evident audit logs: qualified resource paths, a fixed
record schema, retention + legal-hold policy, and a forensic replay path. [DOC]

## Procedure
### Step 1: Discover
- Inventory auditable events (who/what/when/where) and the systems that emit them. [DOC]
- Capture regulatory drivers (retention horizon, residency, immutability mandate). [SUPUESTO]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV; choose store + integrity mechanism. [DOC]
- Decide sync vs async write path against the latency/durability trade-off below. [INFERENCIA]
### Step 3: Execute
- Implement the record schema and integrity chain; tag every design claim. [DOC]
### Step 4: Validate
- Replay a sample window; confirm tamper detection fires on a mutated record. [INFERENCIA]

## Record Schema (minimum viable)
Every entry MUST carry: `event_id` (unique), `timestamp` (UTC, ISO-8601),
`actor` (authenticated principal, never inferred), `action`, qualified
`resource` path, `outcome` (allow/deny/error), `source_ip`/`session`, and a
`prev_hash` linking to the prior record. [DOC] Omitting `actor` or `prev_hash`
breaks non-repudiation and tamper-evidence respectively. [INFERENCIA]

## Decisions & Trade-offs
- **Append-only store over mutable table.** Immutability is the point; a row you
  can `UPDATE` is not an audit trail. Cost: storage growth — bound it with
  retention, not deletion-in-place. [INFERENCIA]
- **Hash chain over per-record signature.** Chaining detects deletion/reorder,
  not just edits, at lower cost than signing each row. Cost: verification is
  sequential. Sign periodic checkpoints if you need random-access proof. [INFERENCIA]
- **Async write (queue) over inline.** Keeps the audited operation fast; cost is
  a durability window — a crash can drop in-flight events. Inline write only
  where a lost event is unacceptable (e.g. consent changes). [SUPUESTO]

## Anti-Scope (explicitly NOT this skill)
- Application/debug logging, metrics, and tracing — different retention, no
  integrity guarantee. [DOC]
- Access-control enforcement: the trail records decisions, it does not make them. [DOC]
- PII minimization in payloads — governed upstream; never copy raw PII into logs. [DOC]

## Quality Criteria
- [ ] Evidence tags applied (Alfa core set: `[CÓDIGO]/[CONFIG]/[DOC]/[INFERENCIA]/[SUPUESTO]`)
- [ ] Constitution-compliant
- [ ] Record schema complete; actor authenticated, not inferred
- [ ] Integrity chain verifiable end-to-end
- [ ] Retention + legal-hold policy stated with a horizon
- [ ] Actionable output

## Usage
Example invocations:
- "/audit-trail-design" — Run the full audit trail design workflow
- "audit trail design on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [SUPUESTO]
- Assumes a trustworthy clock source; skewed timestamps corrupt ordering —
  verify NTP sync before relying on `timestamp`. [SUPUESTO]
- Requires English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain-expert judgment for final decisions, nor counsel on
  jurisdiction-specific retention law. [SUPUESTO]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Clock skew / non-monotonic timestamps | Order by ingest sequence, not wall-clock; flag the gap |
| Log store outage mid-operation | Fail closed for high-risk actions; buffer + replay for the rest |
| Retention expiry vs active legal hold | Hold wins — suspend purge until released |
| Hash-chain break detected on replay | Treat as tamper/loss; quarantine window, alert, do not silently re-link |
| High-volume actor floods the trail | Sample non-security events; never sample security/consent events |
