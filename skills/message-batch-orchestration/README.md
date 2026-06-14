# message-batch-orchestration

Builds orchestrators for the Anthropic **Message Batches API** that process
offline, latency-tolerant workloads with a unique `custom_id` per request,
selective fragmentation of partial failures, and capped retry of only the failed
items. [DOC]

## What it does

Takes a list of work items with a stable business ID and turns them into a batch
run: assemble requests → validate `custom_id` uniqueness → `create` → poll
`processing_status` with backoff → stream `results()` → fragment by
`result.type` → retry only the failed `custom_id`s under a cap. Output is a
`custom_id → message` map of successes plus the list of unresolved IDs after the
cap is exhausted, and (when evidence is required) a JSON report that passes
`scripts/check.sh`. [DOC]

## When to use

- **Offline / latency-tolerant** loads: mass classification, dataset
  enrichment, evals, backfills — no user waiting on the line. [DOC]
- Volume that justifies async processing and **fail isolation** over synchronous
  one-by-one calls (batch mode also cuts cost ~50% at volume). [DOC]
- You need **selective retry** of failed items without reprocessing the
  successes. [DOC]

## When NOT to use

- Interactive / streaming paths where a user waits in line → `false_positive_realtime`. [CONFIG]
- Unrelated tasks (e.g. relational DB schema design) → do not activate. [CONFIG]
- A request to skip `custom_id` uniqueness validation, drop `custom_id`, or
  disable fail isolation → **reject**, never degrade the pattern. [CONFIG]

## How it executes

The skill drives the Discover → Analyze → Execute → Validate spine:

1. **Discover** the workload shape: offline vs. realtime, item count, stable
   business ID field, `model`, `max_tokens`, `max_retries`.
2. **Analyze** against the offline gate and the `custom_id` uniqueness gate;
   reject conflicting requirements before any send.
3. **Execute** the lifecycle `create → poll processing_status → results →
   fragment → selective retry` with a retry cap and persisted `batch.id`
   checkpoint.
4. **Validate** the deliverable against the acceptance gate and, when evidence
   is required, `scripts/check.sh` / `scripts/validate_message_batch_orchestration.py`.

## Agents

- `agents/lead.md` — orchestrates the spine and owns the acceptance gate.
- `agents/specialist.md` — Batches API + `custom_id` correlation depth.
- `agents/support.md` — assembles requests, runs the lifecycle, persists output.
- `agents/guardian.md` — validation gates (offline, uniqueness, retry cap, evidence).

## References and assets

- Domain knowledge: `knowledge/body-of-knowledge.md`, `knowledge/knowledge-graph.json`.
- Prompts: `prompts/primary.md`, `prompts/meta.md`, `prompts/variations/{quick,deep}.md`.
- Deliverable scaffold: `templates/output.md`.
- Worked example: `examples/example-input.md`, `examples/example-output.md`.
- Determinism bundle: `assets/` (rubric + acceptance checklist + manifest).
- Eval suite: `evals/evals.json`.

The contract policies referenced by `SKILL.md`
(`assets/message-batch-orchestration-contract.json`, `assets/workload-policy.json`,
`assets/custom-id-policy.json`, `assets/lifecycle-policy.json`,
`assets/retry-fragmentation-policy.json`, `assets/evidence-policy.json`) define
the JSON report contract and gates. [CONFIG]
