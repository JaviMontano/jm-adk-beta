<!-- distilled from alfa skills/documentation-system -->
# Documentation System
> "Method over hacks."

## TL;DR
Doc-as-code workflow: discover → analyze → execute → validate, with versioning, review cycles, and CI publishing. Output is evidence-tagged and Constitution-compliant. [EXPLICIT]

## Scope
- **In:** structured docs derived from project artifacts, doc-as-code pipelines, review/publish cadence. [EXPLICIT]
- **Out (anti-scope):** prose ghostwriting, translation, design/layout, replacing SME sign-off. Redirect these. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather context and requirements; list source artifacts (code, configs, prior docs). [EXPLICIT]
- Record gaps as `[SUPUESTO]` with the step that would confirm them — never fabricate past a critical void. [DOC]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV; record each decision with its trade-off, not just the winner. [EXPLICIT]
### Step 3: Execute
- Implement with one evidence tag per non-obvious claim; pick the weakest tag if two apply. [DOC]
### Step 4: Validate
- Verify quality criteria below; block publish if any unchecked. [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied (one per claim, single family, consistent spelling)
- [ ] Constitution-compliant (XIII/XIV trade-offs logged)
- [ ] Actionable output (every section drives a reader decision or action)
- [ ] Each `[SUPUESTO]` paired with a verification step

## Decisions & Trade-offs
| Decision | Why | Trade-off accepted |
|----------|-----|--------------------|
| Doc-as-code over WYSIWYG | Diffable, reviewable, CI-gated | Steeper authoring ramp [EXPLICIT] |
| Tag every non-obvious claim | Provenance + auditability | Slight density cost; mitigated by not tagging self-evident lines [DOC] |
| Block publish on unchecked criteria | Prevents silent quality drift | Slower first publish [INFERENCIA] |

## Usage
Example invocations:
- "/documentation-system" — Run the full documentation system workflow
- "documentation system on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Tags follow this skill's `[EXPLICIT]`/Alfa-core convention; never mix tag families in one doc. [DOC]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Artifact unreadable / access denied | Mark `[SUPUESTO]`, name the blocker, continue with rest |
| Stale source vs live system | Prefer live; flag the doc section as needing re-sync |
| CI publish fails | Hold version bump; surface the failing gate, do not partial-publish |
