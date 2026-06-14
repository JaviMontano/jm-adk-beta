<!-- distilled from alfa skills/intelligent-routing -->
<!-- > -->
# Intelligent Routing

> "Method over hacks. Evidence over assumption."

## TL;DR

Match user intent to the best domain/Lead-agent using hybrid retrieval: lexical **BM25** + **semantic similarity (cosine)**, blended into one routing score. Orchestration-layer skill used internally by Pristino and the adk-orchestrator; never user-facing on its own. Full protocol in PRISTINO.md. [EXPLICIT]

**Scoring model:** `score = α·bm25_norm + (1-α)·cosine`, default `α=0.4`. Min-max normalize BM25 per query before blending (raw BM25 is unbounded; cosine is [0,1]). Route to top candidate only if `score ≥ 0.95`; else escalate (see Edge Cases). [INFERRED]

## Anti-Scope

Not a planner, not an executor, not a domain solver. It selects *who* acts, never performs the downstream work, rewrites user intent, or overrides a human's final call. One route per invocation. [EXPLICIT]

## Procedure

### Step 1: Discover
- Gather input + context (cwd, active project, recent turns).
- Load candidate index (domain/agent registry) and routing config (`α`, threshold, tie-margin).
- Normalize input: strip noise, expand known acronyms before tokenizing — unexpanded acronyms tank BM25 recall. [INFERRED]

### Step 2: Analyze
- Compute BM25 over candidate corpus; compute cosine over embeddings; blend per scoring model.
- Rank; capture top-2 plus margin (`score₁ − score₂`) for tie detection.
- Evaluate against Constitution XIII/XIV (auditability, no silent override). [DOC]

### Step 3: Execute
- Emit selected route + score + top-2 rationale (the runner-up is the audit trail).
- Tag every output with evidence markers using this file's convention.

### Step 4: Validate
- Confirm `score ≥ 0.95` and `margin ≥ 0.05`; on failure, do not route — escalate.
- Verify the chosen agent's declared scope actually covers the intent (high score ≠ capability match). [INFERRED]

## Worked Example

Input: `"the login button 500s after deploy"`.
- BM25 favors `incident-response` (lexical "500", "deploy"); cosine also lifts `observability`.
- Blend (α=0.4): incident-response 0.97, observability 0.93. Margin 0.04 < 0.05 → **tie** → present both, ask user to disambiguate rather than guess. [INFERRED]

## Quality Criteria

- [ ] Evidence tags applied to every non-trivial claim
- [ ] Constitution XIII/XIV compliant (decision auditable, no silent override)
- [ ] `score ≥ 0.95` AND `margin ≥ 0.05`
- [ ] Top-2 + rationale emitted with the route
- [ ] Selected agent's scope verified against intent
- [ ] Actionable output (route is concrete and usable downstream)

## Failure Modes

| Mode | Cause | Mitigation |
|------|-------|------------|
| Confident-wrong route | High score, scope mismatch | Step-4 scope check; route is advisory, not binding |
| Cold-start (empty index) | Registry unloaded | Fail closed — escalate, never default-route |
| Embedding drift | Index stale vs. model | Version-pin embeddings; flag on mismatch |
| Acronym/jargon miss | Unexpanded tokens | Step-1 normalization + synonym expansion |

## Related Skills

- See PRISTINO.md for full orchestration protocol
- `multi-model-routing.md` — model-tier selection downstream of domain routing

## Usage

Example invocations:

- "/intelligent-routing" — Run the full intelligent routing workflow
- "intelligent routing on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes a populated candidate registry with embeddings; empty registry → fail closed, not default-route [INFERRED]
- English-language output and corpus unless otherwise specified; mixed-language input degrades BM25 [EXPLICIT]
- Threshold/`α` are tuned defaults, not guarantees — recalibrate per corpus [INFERRED]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Tie (margin < 0.05) | Present top-2; let caller/user disambiguate — do not guess |
| All scores < 0.95 | Escalate to human or generalist; never force a route |
| Stale/missing index | Fail closed; surface the error, do not silently degrade |
