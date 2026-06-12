<!-- distilled from alfa skills/whitepaper-creation -->
<!-- > -->
# Whitepaper Creation
> "Method over hacks."

## TL;DR
Long-form gated artifact: problem framing → methodology → evidence-backed findings → recommendations → citations. Authority piece, not a sales sheet — claims earn trust through traceable sourcing, not adjectives. [DOC]

## Procedure
### Step 1: Discover
- Gather context, audience tier (practitioner vs. executive), thesis, source corpus
- Lock the single claim the paper must prove; everything else is support [INFERENCIA]

### Step 2: Analyze
- Evaluate angles/structure per Constitution XIII/XIV; reject framings unsupported by the corpus
- Map each intended finding to ≥1 citable source before drafting [DOC]

### Step 3: Execute
- Draft sections; attach an evidence tag from the Constitution evidence-tag family to every non-obvious claim
- Quantitative claims cite a source or are marked `[SUPUESTO]` with a verification step [DOC]

### Step 4: Validate
- Run Quality Criteria; resolve every `[SUPUESTO]`/`[POR_CONFIRMAR]` or disclose it

## Quality Criteria
- [ ] Single thesis stated in first 150 words and revisited in conclusion
- [ ] Every non-obvious claim carries exactly one tag from the Constitution evidence-tag family
- [ ] Methodology section lets a reader reproduce the findings
- [ ] Citations resolve (no dead/placeholder references)
- [ ] Constitution-compliant; no invented prices; single-brand voice throughout
- [ ] Recommendations are actionable and tied to stated findings

## Usage
Example invocations:
- "/whitepaper-creation" — Run the full whitepaper creation workflow
- "whitepaper creation on this project" — Apply to current context

## Worked Example
Input: thesis "RAG cuts hallucination in support bots."
- Discover: audience = eng leads; corpus = 3 internal eval runs + 2 papers
- Analyze: framing "measured reduction" (corpus-backed) over "eliminates" (unsupported)
- Execute: "Hallucination rate fell from X to Y across 3 runs `[CÓDIGO]` (eval logs); aligns with [paper] `[DOC]`"
- Validate: both numbers trace to logs; no naked superlatives [INFERENCIA]

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and a citable source corpus [SUPUESTO]
- English output unless otherwise specified [SUPUESTO]
- Does not replace domain-expert sign-off on final claims [DOC]
- Anti-scope: not a blog post, datasheet, or pitch deck — those have own skills [DOC]
- Length target is depth-driven, not padded to a page count [INFERENCIA]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Thesis unsupported by corpus | Stop; narrow the thesis or request more sources, do not pad |
| Citation cannot be resolved | Mark `[SUPUESTO]` + verification step; never fabricate a reference |
| Source conflicts with another | Surface both, state which the paper relies on and why [INFERENCIA] |
| Reads as sales copy | Reframe to evidence-led; strip superlatives lacking a tag |
