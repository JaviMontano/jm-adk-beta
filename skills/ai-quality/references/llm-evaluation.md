<!-- distilled from alfa skills/llm-evaluation -->
<!-- > -->
# Llm Evaluation
> "Method over hacks."
## TL;DR
Model output quality assessment, hallucination detection, benchmark suites. Pick the eval method by failure cost: cheap reversible outputs tolerate reference-free LLM-judge; high-stakes outputs need labeled references + human spot-check. [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather context and requirements: target task, output schema, acceptable failure modes, who consumes the output. [EXPLICIT]
- Decide eval type — reference-based (gold labels exist) vs reference-free (judge rubric only). Default reference-free when labels cost more than the error they catch. [INFERENCE]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV.
- Choose metrics: exact-match/F1 for closed tasks; rubric-scored LLM-judge for open generation; groundedness (claim-vs-source) for RAG. Trade-off: LLM-judge scales but inherits judge bias — pin judge model+prompt and report it. [INFERENCE]
- Set a baseline (prior model / human / trivial heuristic). A score without a baseline is not a result. [EXPLICIT]
### Step 3: Execute
- Implement with evidence tags. Run on a frozen, versioned eval set; record model id, params, prompt hash, dataset hash for reproducibility. [EXPLICIT]
- Detect hallucination by grounding each factual claim against source; unsupported claims fail regardless of fluency. [EXPLICIT]
### Step 4: Validate
- Verify quality criteria met. Human-review a sample (≥20 items or all failures) to confirm the metric tracks real quality. [INFERENCE]
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Baseline reported alongside every score [EXPLICIT]
- [ ] Eval set + model + prompt versioned and re-runnable [EXPLICIT]
- [ ] Judge config (model, rubric, scale) disclosed when LLM-judge used [EXPLICIT]

## Usage

Example invocations:

- "/llm-evaluation" — Run the full llm evaluation workflow
- "llm evaluation on this project" — Apply to current context

### Worked example
RAG summarizer, no gold labels. Method: reference-free groundedness — for each summary, split into atomic claims, check each against retrieved chunks, score = supported/total. Baseline: prior prompt = 0.71. New prompt = 0.88, but human spot-check of 20 finds 2 fluent-but-unsupported claims the judge passed → tighten judge rubric, re-run before shipping. [INFERENCE]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: not model training/fine-tuning, not latency/cost benchmarking, not red-teaming/jailbreak testing — route those elsewhere. [EXPLICIT]
- A passing aggregate score does not certify per-item safety; rare high-severity failures need their own gate. [INFERENCE]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No gold labels available | Use reference-free LLM-judge with pinned rubric; flag as lower-confidence [INFERENCE] |
| Eval set too small (<30) | Report wide uncertainty; treat deltas as directional, not conclusive [INFERENCE] |
| Judge agrees with itself (same model generated + grades) | Use a different judge model or human arbitration to break the correlation [ASSUMPTION] |
| Non-deterministic output (temp>0) | Fix seed or average ≥3 samples per item; report variance [INFERENCE] |
