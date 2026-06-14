# Example Input — validation-retry-design

## Scenario

An extraction agent reads invoice PDFs and must emit a JSON object matching this contract:

```json
{
  "invoice_number": "string",
  "issue_date": "YYYY-MM-DD",
  "currency": "ISO-4217 code",
  "total": "number >= 0",
  "line_items": "array, length >= 1"
}
```

Across a batch, the agent's output is sometimes invalid in three observed ways:

1. `total` comes back as the string `"1.234,00"` instead of a number (parse failure).
2. `issue_date` comes back as `12/06/2026` instead of `2026-06-12` (format failure).
3. On scanned-but-blank pages, the agent invents an `invoice_number` even though no number is present in the source (missing source datum).

## Request

> Design an extract-validate-retry loop for this invoice JSON. The validator must return an actionable error (not a boolean). Reinject the exact validation error on each retry instead of resending the original prompt. Classify the parse and format failures as recoverable and the missing invoice number as not-recoverable. Cap retries at 3, break early if the same error repeats twice, and on exhaustion or a not-recoverable failure return an escalation packet with the full error chain — never the last failed output as success.

## Constraints

- Validation must run offline and deterministic (same plan, same verdict).
- Stay inside the `validation-retry-design` skill; do not touch related kata skills.
