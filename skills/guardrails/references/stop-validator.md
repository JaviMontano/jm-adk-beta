<!-- distilled from alfa skills/stop-validator -->
<!-- > -->
# Stop Validator
> "Method over hacks."
## TL;DR
Final gate before delivery: block output until evidence tags, Constitution compliance, and completeness all pass. A validator, not a generator — it never edits content, only PASS/FAIL with reasons. [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather the candidate output plus its source context (requirements, artifacts).
- Resolve the active tag family (Alfa kit vs Jarvis operator) from `references/verification-tags.md`; one family per document. [DOC]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV; record the decision and its trade-off, not just the choice. [EXPLICIT]
### Step 3: Execute
- Apply each Quality Criterion as a hard check; on any FAIL, stop and return reasons — do not silently repair. [EXPLICIT]
### Step 4: Validate
- Confirm every criterion PASSes; emit verdict with the failing items named. [EXPLICIT]
## Quality Criteria
- [ ] Every non-obvious claim carries exactly one evidence tag from a single family [EXPLICIT]
- [ ] No `{WEB}` without citation; no `{VACIO_CRITICO}` followed by fabricated data [DOC]
- [ ] Each `{SUPUESTO}`/`{POR_CONFIRMAR}` paired with a concrete verification step [DOC]
- [ ] Constitution-compliant (XIII/XIV); single-brand; no invented prices; no client PII [EXPLICIT]
- [ ] Output is actionable and self-contained [EXPLICIT]

## Acceptance Criteria (the validator's own contract)
- Verdict is binary PASS/FAIL with each failing criterion named; never a vague "looks good". [EXPLICIT]
- A FAIL halts delivery; the validator returns reasons and does NOT mutate the output. [EXPLICIT]
- A PASS asserts every checkbox above held at check time — no partial passes. [INFERENCIA]

## Usage

Example invocations:

- "/stop-validator" — Run the full stop validator workflow
- "stop validator on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Validates form and provenance, not factual truth of tagged claims — a well-tagged falsehood passes. [SUPUESTO]
- Does not replace domain-expert judgment for final sign-off, nor re-run upstream skills. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Mixed tag families in one doc | FAIL; homologate Jarvis → Alfa, never reverse [DOC] |
| Untagged non-obvious claim | FAIL; name the claim, demand a tag |
| `{VACIO_CRITICO}` present | Terminal FAIL; stop and ask, never auto-fill past it [DOC] |
| Output already partially delivered | Validate remainder; flag the unvalidated prefix as risk |
