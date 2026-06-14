# Example Output — validation-retry-design

Worked design for the invoice-JSON extract-validate-retry loop. Tags: `[DOC]` from SKILL.md/policies, `[INFERENCE]` derived.

## 1. Contract under validation

- base_prompt: "Extract the invoice fields from the attached PDF as JSON."
- Contract: `invoice_number:string`, `issue_date:YYYY-MM-DD`, `currency:ISO-4217`, `total:number>=0`, `line_items:array len>=1`.
- max_retries: **3**. Determinism: offline=true, network_required=false, deterministic=true. [DOC]

## 2. Validator (actionable, not boolean)

Returns `{ok, code, message, path, recoverable}`:

| code | layer | message | path | recoverable |
|------|-------|---------|------|-------------|
| `total_not_number` | schema-shape | "total must be a JSON number, got string '1.234,00'" | `total` | true |
| `date_format` | schema-shape | "issue_date must be YYYY-MM-DD, got '12/06/2026'" | `issue_date` | true |
| `missing_source_invoice_number` | semantic | "invoice_number not present in source page; do not invent" | `invoice_number` | false |

## 3. Recoverability classification

| code | recoverable? | fix-only instruction | converges? |
|------|--------------|----------------------|------------|
| `total_not_number` | recoverable | "Re-emit total as a numeric value (1234.00)." | yes |
| `date_format` | recoverable | "Re-emit issue_date as YYYY-MM-DD." | yes |
| `missing_source_invoice_number` | not_recoverable | escalate now — no retry can fix a missing datum | n/a |

## 4. Informed feedback (attempt 2 prompt)

```
Extract the invoice fields from the attached PDF as JSON.

Your previous output failed validation:
  code=total_not_number path=total
  message="total must be a JSON number, got string '1.234,00'"
Previous output:
  {"invoice_number":"INV-7781","issue_date":"2026-06-12","currency":"COP","total":"1.234,00","line_items":[...]}
Fix only what failed; keep everything else.
```

Blind retry is impossible: the builder requires `prev_output` and `last_error`; with both present it cannot emit the unchanged base_prompt. [DOC]

## 5. Budget & error chain

- Counter on `attempt`, cap at 3. Error chain appends each `{code,message,path,recoverable}`. [DOC]

## 6. Systematic detection

- If `date_format` recurs on attempts 1 and 2 identically -> break with `fix_hint="prompt: state the date format in the base_prompt"` instead of spending attempt 3. [DOC]

## 7. Terminal states observed

- **Recoverable run:** attempt 1 fails `total_not_number`, attempt 2 passes ->
  `{"status":"ok","output":{...},"attempts":2}`
- **Not-recoverable run (blank page):** attempt 1 returns `missing_source_invoice_number` ->
  `{"status":"escalated","reason":"not_recoverable","error_chain":[{"code":"missing_source_invoice_number",...}],"last_output":{...}}`
  No loop, no invented number accepted as success. [DOC]

## 8. Gate sign-off

error_feedback ✓ · specific_error ✓ · quality_criteria ✓ · recoverability ✓ · retry_budget/budget_limit ✓ · systematic_detection ✓ · silent_failure_blocker ✓ · blind_retry_blocker ✓ · assets/deterministic_scripts ✓ · upgrade_safety ✓

_Single-brand: JM Labs. No prices. Never green-as-success — gate verified item by item._
