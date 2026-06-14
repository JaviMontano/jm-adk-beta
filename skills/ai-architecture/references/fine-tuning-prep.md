<!-- distilled from alfa skills/fine-tuning-prep -->
<!-- > -->
# Fine Tuning Prep
> "Method over hacks."
## TL;DR
Curate, label, split, and quality-gate a training corpus so a fine-tune measurably beats the base-model + prompt-engineering baseline. [EXPLICIT]

## When to fine-tune (anti-scope)
Fine-tune only after RAG + few-shot prompting are exhausted. [EXPLICIT]
- Use it for: fixed output format/style/tone, a narrow task with stable schema, latency/cost cuts via a smaller model. [EXPLICIT]
- Do NOT use it for: injecting fresh/changing facts (use RAG), one-off tasks, or <~50 clean examples. [EXPLICIT]

## Procedure
### Step 1: Discover
- Define the task, success metric, and the baseline number to beat. [EXPLICIT]
- Scope sources, licensing, and PII exposure before collecting anything. [EXPLICIT]
### Step 2: Curate
- Dedupe (exact + near-dup); near-duplicates inflate train scores and leak into eval. [EXPLICIT]
- Balance classes/intents; cap over-represented buckets so rare cases survive. [EXPLICIT]
- Target diversity over volume: 100s of varied examples beat 1000s of redundant ones. [EXPLICIT]
### Step 3: Label
- Write a labeling guideline with positive/negative examples and tie-breakers. [EXPLICIT]
- Measure inter-annotator agreement; arbitrate disagreements, fold rulings back into the guideline. [EXPLICIT]
### Step 4: Split
- Split BEFORE augmentation; split by entity (user/doc), not by row, to stop leakage. [EXPLICIT]
- Hold out a frozen test set never seen during iteration. [EXPLICIT]
### Step 5: Validate
- Verify schema/format conformance on 100% of rows; reject malformed examples. [EXPLICIT]
- Compare fine-tune vs baseline on the held-out test set; ship only on a real lift. [EXPLICIT]

## Quality Criteria
- [ ] Baseline-to-beat recorded before training [EXPLICIT]
- [ ] Train/val/test split entity-disjoint, no leakage [EXPLICIT]
- [ ] Dedup + class balance applied and logged [EXPLICIT]
- [ ] Labeling guideline + agreement score captured [EXPLICIT]
- [ ] PII scrubbed / licensing cleared [EXPLICIT]
- [ ] Evidence tags applied; Constitution-compliant; actionable output [EXPLICIT]

## Worked Example
Support-reply classifier, 8 intents. Pull 6 mo of tickets → dedupe (12k→3.1k) → cap top intent to 400, up-sample 2 rare intents → 2 annotators label, κ=0.81 after arbitration → split by customer_id 80/10/10 → JSONL schema check passes → fine-tune lifts macro-F1 0.71→0.86 vs base+few-shot; ship. [EXPLICIT]

## Usage

Example invocations:

- "/fine-tuning-prep" — Run the full fine tuning prep workflow
- "fine tuning prep on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes the chosen provider supports fine-tuning for the target model and exposes its required data format [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Prepares data only; does not run training jobs, set hyperparameters, or host the model [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| <~50 usable examples | Stop; recommend RAG/few-shot instead of fine-tuning |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Severe class imbalance | Cap majority + up-sample/synthesize minority; report residual skew |
| PII or licensed data found | Quarantine, scrub or exclude, log the decision |
| Train/test overlap detected | Re-split by entity; invalidate prior eval numbers |
| Out-of-scope request | Redirect to appropriate skill or escalate |
