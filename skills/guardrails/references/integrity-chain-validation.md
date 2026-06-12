<!-- distilled from alfa skills/integrity-chain-validation -->
<!-- > -->
# Integrity Chain Validation

> "A chain is only as strong as its weakest link — find the weak links before they break."

## TL;DR

Validates the complete governance chain (Intent → RQL → Plan → ADR → Spec → Tests → Code) for a feature or the entire project. Produces a traceability matrix showing each requirement's chain status. Flags broken links (missing documents, orphaned code, tests without requirements) with severity. Essential for Constitution compliance and quality gate G1. [EXPLICIT]

**Use when**: before a gate (G1/G2/G3), pre-merge, or auditing inherited code. **Skip when**: no `.specify/` governance artifacts exist yet (chain not yet established — bootstrap requirements first). [SUPUESTO]

## Procedure

### Step 1: Discover
- Scan `.specify/requirements/` for RQL files
- Scan `.specify/plans/` for plan files
- Scan `.specify/adr/` for Architecture Decision Records
- Scan `.specify/specs/` for feature specifications
- Scan `tests/` or `*.test.*` files for test files
- Scan source code for implementation files
- Record what each scan returned, including empty dirs — an absent directory is itself a chain gap, not a skip. [INFERENCIA]

### Step 2: Analyze
- For each RQL, trace forward through the chain:
  - RQL-NNN → referenced in plan-DATE? → referenced in ADR-NNN? → referenced in spec? → test file exists? → code implements it?
- For each code file, trace backward:
  - Code → has tests? → has spec? → has plan? → traces to RQL?
- Classify gaps by severity:
  - **Critical**: Code without tests (violates Constitution IX)
  - **High**: Code without spec (violates Constitution XIII)
  - **Medium**: Spec without ADR (architecture decision undocumented)
  - **Low**: RQL without plan (requirement acknowledged but not scheduled)
- Identify orphans: artifacts that reference nothing or are referenced by nothing
- Match links by stable IDs (RQL-NNN, ADR-NNN), not filenames or paths, so renames/moves don't manufacture false breaks. [INFERENCIA]
- When one artifact serves many requirements (or vice versa), record every edge — a shared `utils.js` is healthy only if **each** RQL it serves traces to it. [SUPUESTO]

### Step 3: Execute
- Generate traceability matrix:
  ```
  | RQL | Plan | ADR | Spec | Tests | Code | Status |
  |-----|------|-----|------|-------|------|--------|
  | RQL-001 | plan-2026-03-22-auth | ADR-001 | spec-auth | auth.test.js | auth.js | COMPLETE |
  | RQL-002 | plan-2026-03-22-cms | — | — | — | — | CRITICAL: No downstream |
  | — | — | — | — | — | utils.js | HIGH: Orphaned code |
  ```
- Count chain completeness: `{complete}/{total}` = chain health %
- Generate remediation tasks for each gap:
  - Critical gaps → must be resolved before G3
  - High gaps → must be resolved before G2
  - Medium/Low → documented, tracked, resolved in next iteration

**Worked example — health math.** 20 RQLs: 16 COMPLETE, 2 CRITICAL (code, no tests), 2 LOW (no plan). Health = 16/20 = 80% → passes G2, **blocks G3** (needs ≥95% AND zero critical). The 2 critical gaps gate G3 regardless of the percentage — severity overrides the ratio. [EXPLICIT]

### Step 4: Validate
- Every code file traces to at least one RQL
- Every RQL has a corresponding plan file
- Zero critical gaps remain (code without tests)
- Chain health % >= 80% for G2 passage, >= 95% for G3
- Remediation tasks created for all remaining gaps

## Acceptance Criteria

- [ ] Matrix covers 100% of discovered RQLs and code files — no silent omissions [EXPLICIT]
- [ ] Every row has an explicit Status (no blanks); orphans appear as their own rows [EXPLICIT]
- [ ] Chain health % is reproducible: same inputs → same number [INFERENCIA]
- [ ] Each gap links to exactly one remediation task with an owner-resolvable action [EXPLICIT]
- [ ] Gate verdict (PASS/BLOCK per G2/G3) stated explicitly with the deciding rule cited [EXPLICIT]
- [ ] Zero critical gaps before a G3 PASS is ever emitted [EXPLICIT]

## Quality Criteria

- [ ] All RQL files scanned and traced forward
- [ ] All code files scanned and traced backward
- [ ] Gaps classified by severity (critical, high, medium, low)
- [ ] Traceability matrix generated
- [ ] Chain health % calculated
- [ ] Remediation tasks created for gaps
- [ ] Zero critical gaps (code without tests)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Only tracing forward (RQL → Code) | Misses orphaned code | Also trace backward (Code → RQL) |
| Ignoring test-to-requirement links | Tests without purpose drift | Every test must trace to a requirement |
| Accepting "we'll add tests later" | Technical debt compound interest | Block at G2 until tests exist |
| Manual chain tracking | Error-prone, doesn't scale | Automate with grep/glob scanning |
| Treating all gaps equally | Wastes time on low-impact items | Severity classification guides priority |
| Counting a test file's existence as "tested" | Empty/skipped tests pass the scan but assert nothing | Verify the test references the RQL and actually executes |
| Averaging severity into the % to "pass" | Hides critical gaps behind a healthy ratio | Gate on zero-critical AND threshold, never the % alone |

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| False break from renamed artifact | COMPLETE chain flips to broken after a move | Match on stable IDs, not paths [INFERENCIA] |
| Generated/vendored code flagged as orphan | Noise floods the matrix | Exclude `dist/`, `vendor/`, `node_modules/`, generated dirs before scanning [SUPUESTO] |
| Circular reference (A→B→A) | Trace never terminates | Detect visited-set cycles; report as a distinct anomaly, not COMPLETE |
| Partial scan on permission error | Silent undercount inflates health % | Fail loud: report unreadable paths, never treat unread as absent [EXPLICIT] |

## Related Skills

- `requirements-engineering` — Creating RQL files that start the chain
- `test-strategy` — Ensuring tests exist for the chain
- `discovery-orchestration` — Generating plan files as part of the chain
- `socratic-debate` — Resolving ambiguities found during chain validation

## Usage

Example invocations:

- "/integrity-chain-validation" — Run the full integrity chain validation workflow
- "integrity chain validation on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Validates link *presence* and traceability, not link *correctness* — a code file that cites the wrong RQL passes the scan; semantic alignment is out of scope [EXPLICIT]
- Health % measures chain completeness, not test quality or coverage depth [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Greenfield repo, no `.specify/` artifacts | Report "chain not established"; recommend bootstrapping RQLs, do not emit a misleading 0% |
| Monorepo with multiple chains | Scope per package/service; one matrix per chain, never merged |
| Legacy code predating governance | Tag as "pre-chain"; quarantine from health % or report as a separate baseline [SUPUESTO] |
