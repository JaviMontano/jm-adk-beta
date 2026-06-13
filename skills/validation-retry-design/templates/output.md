# Retry-Loop Design — <task name>

> Deliverable scaffold for a deterministic extract-validate-retry loop. Fill every field; do not ship with placeholders. Tag claims `[DOC] [INFERENCE] [SUPUESTO]`.

## 1. Contract under validation

- **base_prompt:** <summary>
- **Structured contract:** <schema / format / range>
- **max_retries:** <1..3>  ·  **Determinism:** offline=true, network_required=false, deterministic=true

## 2. Validator (actionable, not boolean)

Returns `{ok, code, message, path, recoverable}`.

| code | layer (schema-shape / semantic) | message template | path |
|------|----------------------------------|------------------|------|
| <e.g. json_parse> | schema-shape | <…> | <…> |
| <e.g. range_violation> | semantic | <…> | <…> |

## 3. Recoverability classification

| code | recoverable? | fix-only instruction | can converge? |
|------|--------------|----------------------|---------------|
| <…> | recoverable | <…> | yes |
| <…> | not_recoverable | escalate now | n/a |

## 4. Informed feedback builder

```
next_prompt = base_prompt
            + "Your previous output failed validation: " + last_error
            + "Previous output:\n" + prev_output
            + "Fix only what failed; keep everything else."
```

Blind retry impossible because: <explain construction>.

## 5. Budget & error chain

- Counter: <…>  ·  Cap: max_retries = <1..3>
- Error chain accumulation: <…>

## 6. Systematic detection

- Break condition: >= 2 identical errors -> structural fix_hint = "<schema | prompt | source>"
- Oscillation note (A,B,A,B): -> budget_exhausted; tighten fix-instruction.

## 7. Terminal states (exactly two)

- Success: `{"status":"ok","output":<…>,"attempts":<n>}`
- Escalation: `{"status":"escalated","reason":"<not_recoverable | systematic | budget_exhausted>","error_chain":[…],"last_output":<…>,"fix_hint":"<…>"}`

## 8. Acceptance gate sign-off

- [ ] error_feedback / specific_error  [ ] quality_criteria  [ ] recoverability
- [ ] retry_budget / budget_limit  [ ] systematic_detection  [ ] silent_failure_blocker
- [ ] blind_retry_blocker  [ ] assets / deterministic_scripts  [ ] upgrade_safety

## 9. Evidence log

- [DOC] …  ·  [INFERENCE] …  ·  [SUPUESTO] …

_Single-brand: JM Labs. No invented prices. Never green-as-success._
