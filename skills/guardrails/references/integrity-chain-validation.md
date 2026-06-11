<!-- distilled from alfa skills/integrity-chain-validation -->
<!-- > -->
# Integrity Chain Validation

> "A chain is only as strong as its weakest link — find the weak links before they break."

## TL;DR

Validates the complete governance chain (Intent → RQL → Plan → ADR → Spec → Tests → Code) for a feature or the entire project. Produces a traceability matrix showing each requirement's chain status. Flags broken links (missing documents, orphaned code, tests without requirements) with severity. Essential for Constitution compliance and quality gate G1. [EXPLICIT]

## Procedure

### Step 1: Discover
- Scan `.specify/requirements/` for RQL files
- Scan `.specify/plans/` for plan files
- Scan `.specify/adr/` for Architecture Decision Records
- Scan `.specify/specs/` for feature specifications
- Scan `tests/` or `*.test.*` files for test files
- Scan source code for implementation files

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

### Step 4: Validate
- Every code file traces to at least one RQL
- Every RQL has a corresponding plan file
- Zero critical gaps remain (code without tests)
- Chain health % >= 80% for G2 passage, >= 95% for G3
- Remediation tasks created for all remaining gaps

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

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
