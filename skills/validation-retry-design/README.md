# validation-retry-design

## What it does

Designs deterministic `extract -> validate -> retry-with-error-feedback` loops that never retry blindly. The loop reinjects the exact validation error into the next attempt, classifies failures as **recoverable** (retry) vs **not-recoverable** (escalate now), enforces a bounded retry budget (`1 <= max_retries <= 3`), detects systematic repeat errors, and emits a complete escalation packet instead of silently accepting a failed output. [DOC]

## When to use

Use when **all three** hold (otherwise the skill is overkill): [INFERENCE]

- A model/agent/pipeline emits a **structured contract** (JSON, schema, fixed format) that is sometimes invalid.
- A retry can be **informed** — the model can plausibly fix the output if told exactly *what* failed.
- Cost/latency must be **bounded** — a finite budget with a legible escalation path, not an infinite loop.

Do **not** use for: one-shot tasks with no validator (marketing copy), failures no retry can fix (missing source data), flaky-infra/transport backoff (network, 5xx, rate-limit), or boolean pass/fail gates with no error payload to reinject. [DOC]

## How it routes and executes

1. **Validator first** — write the function that returns `{ok, code, message, path, recoverable}`, never a bare boolean. The error is the retry's only fuel.
2. **Classify** — mark each error `recoverable` (format, parse, range, schema shape) or `not_recoverable` (missing datum, source contradiction).
3. **Informed feedback** — compose the next prompt as `previous output + exact error + fix-only instruction`. Never resend the original prompt unchanged.
4. **Cap** — fix `max_retries` (2–3), keep a counter and an accumulated error chain.
5. **Systematic detection** — if the same error recurs (>= 2 identical), break the loop and report a structural fix hint instead of burning retries.
6. **Escalate on exhaustion** — at the budget cap or on a not-recoverable failure, return the escalation packet `{status, reason, error_chain, last_output, fix_hint?}` where `reason ∈ {not_recoverable, systematic, budget_exhausted}`.

Terminal states are exactly two: `{"status":"ok", ...}` or an escalation packet. Returning the last failed output as success is a defect, never an output. [DOC]

## References

- `SKILL.md` — full contract, build steps, acceptance gate, GOOD/ANTI patterns, edge cases.
- `knowledge/body-of-knowledge.md` — concepts, standards, decision rules.
- `knowledge/knowledge-graph.json` — concept graph over the loop's key nodes.
- `prompts/` — `primary.md`, `meta.md`, `variations/quick.md`, `variations/deep.md`.
- `templates/output.md` — retry-loop design deliverable scaffold.
- `examples/` — a worked JSON-repair loop (`example-input.md`, `example-output.md`).
- `assets/` — the six policy JSONs plus quality rubric and checklist (see `assets/README.md`).

## Agents

- `agents/lead.md` — orchestrates the design flow and selects terminal states.
- `agents/specialist.md` — validator + classification + systematic-detection depth.
- `agents/support.md` — emits feedback prompts, error chains, escalation packets.
- `agents/guardian.md` — enforces the acceptance gate and blocks blind retry / silent failure.

## Evidence taxonomy

Tag every claim: `[DOC]` (stated in SKILL.md / policies), `[INFERENCE]` (derived), `[SUPUESTO]` (assumption to confirm). No invented prices. Never green-as-success. Single-brand: JM Labs.
