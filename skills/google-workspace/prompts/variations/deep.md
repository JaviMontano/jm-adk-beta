# Deep Variation — google-workspace

`depth=deep`. Apply the chosen playbook exhaustively with verification at each
step. Use when the request mutates data, spans multiple services, or feeds
downstream automation. [DOC]

## Steps

1. Resolve `topic` and load EXACTLY ONE `references/<topic>.md`. If the request
   spans services, prefer `google-apis-integration` or `apis` and enumerate every
   service operation.
2. For each operation, fully specify: resource id, auth profile, least-privilege
   scope/key, retry profile (user-fix / re-auth / quota-backoff / transient-5xx),
   idempotency key, and read-back step.
3. For every mutation: read-before-write evidence, `human_confirmation`/
   `human_consent = confirmed`, and the exact rollback/verify plan.
4. Enumerate edge cases from the playbook (e.g. Sheets protected ranges,
   mismatched header rows, recurring-event instance ids, Maps key restrictions).
5. Build the test matrix: unit, contract, integration-sandbox, e2e-preview,
   security, quota-error, consent-gate.
6. Run the acceptance gate; reject the whole plan if any operation fails. Prefer
   the deterministic compiler (`compile-<topic>.py`) and `check.sh` where shipped.
7. Render the full deliverable with residual risks and verify steps.

## Deep example

Request: "append a row to a tracking sheet AND create a Calendar invite for the
owner." → topic `google-apis-integration`. Operations:
`sheets.spreadsheets.values.append` (scope `spreadsheets`, idempotency
`sheet-append-<runId>`, read-back via `values.get`) and `calendar.events.insert`
(scope `calendar.events`, consent required, `sendUpdates=all` only post-consent).
Whole plan blocks until consent confirmed; reject if scopes broaden to full
access. [CODE]
