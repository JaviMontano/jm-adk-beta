<!-- distilled from alfa skills/multi-model-routing -->
<!-- > -->
# Multi Model Routing
> "Method over hacks."
## TL;DR
Route each task to the cheapest model that clears its quality bar; chain fallbacks for failures; cap cost and latency explicitly. [DOC]

## Routing model
Tier tasks by complexity, then bind a model class — not a fixed model — so swaps don't break routes. [INFERENCIA]

| Tier | Task shape | Model class | Why |
|---|---|---|---|
| Light | Extract, classify, format, short rewrite | Small/fast | Sub-tier capability wastes budget on solved tasks. [INFERENCIA] |
| Standard | Summarize, draft, single-tool calls, RAG answer | Mid | Default; escalate only on measured failure. [SUPUESTO] |
| Heavy | Multi-step reasoning, planning, code synthesis, judge | Large | Quality gap dominates cost here. [INFERENCIA] |

Decide per Constitution XIII/XIV. Bind the class at config, resolve the concrete model at call time. [CONFIG]

## Procedure
### Step 1: Discover
- Gather task inputs, the quality bar (acceptance test), and hard cost/latency ceilings. [DOC]
- Missing ceiling → default Standard, never Heavy (fail cheap, escalate on evidence). [SUPUESTO]
### Step 2: Analyze
- Map task → tier using the table; record the deciding signal. [INFERENCIA]
- Pick model class per Constitution XIII/XIV; list the fallback chain (primary → cheaper-retry → escalate). [CONFIG]
### Step 3: Execute
- Call primary with evidence tags on outputs. On failure (timeout, refusal, malformed, low-confidence), advance the chain. [DOC]
- Escalate a tier only after a same-tier retry fails — not on first error. [INFERENCIA]
### Step 4: Validate
- Run the acceptance test from Step 1. Log model, tier, attempts, cost, latency for routing-table tuning. [DOC]

## Trade-offs (decided)
- **Class-binding over model-pinning**: survives provider/model churn; costs an indirection layer. [INFERENCIA]
- **Escalate-on-failure over route-to-best**: ~order-of-magnitude cheaper at scale; adds retry latency on the unlucky path. [SUPUESTO]
- **Same-tier retry before escalation**: absorbs transient errors without overpaying; one extra call worst case. [INFERENCIA]

## Quality Criteria
- [ ] Every task mapped to a tier with a recorded deciding signal
- [ ] Fallback chain defined before first call
- [ ] Cost/latency ceilings set or explicit default applied
- [ ] Evidence tags applied; routing telemetry logged
- [ ] Constitution-compliant, actionable output

## Usage

Example invocations:

- "/multi-model-routing" — Run the full multi model routing workflow
- "multi model routing on this project" — Apply to current context

## Assumptions & Limits
- Assumes ≥2 model classes are reachable; single-model setup makes routing a no-op (only fallback/retry applies). [SUPUESTO]
- Assumes access to project artifacts (code, docs, configs). [DOC]
- English output unless specified; no pricing emitted — reason in relative cost tiers only. [DOC]
- Does not pick a concrete model or vendor, and does not replace domain-expert judgment on final decisions. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements (cheap + heavy-quality) | Flag the conflict; propose tier + acceptance test, let caller resolve |
| Full fallback chain exhausted | Stop, return last error + attempts; do not fabricate output |
| No model class meets the ceiling | Surface the gap; relax ceiling or accept lower tier explicitly |
| Out-of-scope request | Redirect to appropriate skill or escalate |
