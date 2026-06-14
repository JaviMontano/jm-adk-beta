<!-- distilled from alfa skills/knowledge-management -->
<!-- > -->
# Knowledge Management
> "Method over hacks."
## TL;DR
Turn scattered project knowledge into a deterministic knowledge register:
source-backed entries, owners, retrieval paths, decay signals, next actions. [EXPLICIT]

Optimizes for *reproducibility* over coverage — a register a second operator can
regenerate offline beats an exhaustive one that drifts with the live clock. [INFERENCE]

## Procedure
### Step 1: Discover
- Inventory source artifacts: decisions, docs, tasklogs, changelogs, runbooks,
  conversations, specs, handoff notes.
- Record each candidate with source path, owner, evidence tag, freshness date,
  retrieval terms, and relationship to active work.
- **Done when:** every candidate has a resolvable source path; items without one
  are queued as gaps, not silently dropped. [DOC]

### Step 2: Analyze
- Classify each item with the taxonomy in `assets/knowledge-taxonomy.json`.
- Score searchability and decay risk via `assets/searchability-policy.json` and
  `assets/freshness-policy.json`.
- Flag contradictions, orphan knowledge, duplicate sources, stale entries, uncited claims.
- **Decay is computed from the report's `reference_date`, never the live clock** —
  this is what makes two runs of the same inputs produce identical output. [CONFIG]
- **Done when:** every item has a taxonomy class, a searchability score, and a
  decay verdict traceable to a policy window. [DOC]

### Step 3: Execute
- Produce the report using the contract in `assets/report-contract.json`.
- Include: register, gaps, decay review, retrieval map, action log, validation, risks.
- **Done when:** report validates against the contract and every register row
  carries source + owner + status + freshness + retrieval terms + next action. [DOC]

### Step 4: Validate
- Verify quality criteria met.
- For JSON reports run `bash skills/knowledge-management/scripts/check.sh`; use
  `scripts/validate_knowledge_management_report.py` for offline validation.
- **Done when:** validator exits clean with no network access required. [CONFIG]

## Deterministic Assets
- `assets/manifest.json` — lists every local asset and its consumer.
- `assets/evidence-policy.json` — allowed evidence tags.
- `assets/knowledge-taxonomy.json` — canonical item and gap types.
- `assets/searchability-policy.json` — retrieval-metadata requirements.
- `assets/freshness-policy.json` — decay windows keyed to report `reference_date`,
  never the live clock.
- `assets/report-contract.json` — report fields enforced by the offline validator.

## Key Decisions & Trade-offs
| Decision | Why | Trade-off accepted |
|----------|-----|--------------------|
| Decay keyed to `reference_date`, not `now()` | Determinism: same inputs → same output, reproducible in review/CI | Register can look "fresh" past its real shelf life if `reference_date` is stale — operator must set it honestly [INFERENCE] |
| Offline validation (no network) | Runs in CI and air-gapped review; no flaky external calls | Cannot verify live external links resolve; link-rot is a separate check [ASSUMPTION] |
| Missing source path → gap, not entry | Keeps the register source-backed; blocks unverifiable claims | Real-but-undocumented knowledge is excluded until someone files the source [INFERENCE] |
| Owner required before closure | Decay needs an accountable human to act | Orphaned-but-true items stall until an owner/escalation path is named [DOC] |

## Quality Criteria
- [ ] Evidence tags applied (single family, consistent spelling)
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Register includes source, owner, status, freshness, retrieval terms, and
      next action for every item.
- [ ] Decay decisions computed from explicit report dates, not the current date.
- [ ] Searchability findings reproducible without network access.

## Usage
- "/knowledge-management" — Run the full knowledge-management workflow
- "knowledge management on this project" — Apply to current context
- "Build a knowledge register for these docs and flag stale entries"
- "Audit project decisions for searchability and decay risk"

### Worked example (abbreviated register row)
Input: a 14-month-old ADR at `decisions/0007-auth.md`, owner unset, `reference_date: 2026-06-01`,
freshness policy window for `decision` = 365 days.
Output row: `source=decisions/0007-auth.md`, `class=decision`, `status=STALE`
(age 425d > 365d window), `owner=UNASSIGNED → block closure`, `retrieval=[auth, oauth, ADR-0007]`,
`next_action=confirm owner + re-validate against current auth flow`. [DOC]

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]
- **Anti-scope:** not a search index or vector store — it audits and registers
  knowledge, it does not serve queries at runtime. [INFERENCE]
- **Anti-scope:** does not author the missing knowledge; it flags gaps and owners,
  not the content that fills them. [INFERENCE]
- Freshness reflects policy windows, not semantic correctness — a "fresh" entry
  can still be wrong; staleness ≠ falsity. [ASSUMPTION]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Missing source path | Mark as gap; do not promote the claim to register |
| Stale item without owner | Block closure until owner or escalation path exists |
| Decay review mentions "today" | Replace with explicit `reference_date` |
| No `reference_date` supplied | Halt — do not fall back to `now()`; ask for the date [CONFIG] |
| Duplicate sources for one fact | Keep canonical source, link duplicates, flag for merge |
| Contradictory sources | Register both with `status=CONTESTED`; do not silently pick one |
| Item cited only from conversation | Allowed but tag the provenance; downgrade to gap if unrecoverable |
| Validator passes but register empty | Treat as failure — empty register ≠ success [INFERENCE] |
