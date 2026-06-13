# Primary Prompt — validation-retry-design

You are designing a deterministic `extract -> validate -> retry-with-error-feedback` loop. Produce a loop that never retries blindly and never returns a failed output as success.

## Inputs to gather

- `base_prompt` and the structured contract the output must satisfy (schema / format / range).
- The validator: it MUST return `{ok, code, message, path, recoverable}`, not a bare boolean.
- `max_retries` (must land in `1..3`).

## Produce, in order

1. **Validator spec** — the actionable error shape, with `code` separating schema-shape from semantic failures.
2. **Recoverability table** — which `code`s are `recoverable` (format/parse/range/schema) vs `not_recoverable` (missing datum/contradiction/ambiguity).
3. **Feedback builder** — each retry prompt = `base_prompt + exact prior error + previous output + fix-only instruction`. Show that resending the unchanged prompt is impossible by construction.
4. **Budget & error chain** — counter, `1 <= max_retries <= 3`, accumulated chain.
5. **Systematic detection** — break on >= 2 identical errors with a structural `fix_hint`.
6. **Terminal states** — exactly `{status:ok,...}` or `{status:escalated, reason, error_chain, last_output, fix_hint?}` with `reason ∈ {not_recoverable, systematic, budget_exhausted}`.

## Hard rules

- Never retry the original prompt unchanged after a validation failure.
- Never use boolean-only validation.
- Never loop on a not-recoverable failure or a thrown validator.
- Never return the last failed output as success.

## Governance

Tag every claim `[DOC] [INFERENCE] [SUPUESTO]`. Reference the `assets/*` policies and confirm the plan validates offline/deterministic against `assets/retry-loop-contract.json`. Single-brand: JM Labs. No invented prices; never green-as-success.
