# Example Output — google-workspace

Rendered from `templates/output.md` for the request in `example-input.md`.

## 1. Request & surface

- **Request restated:** On each completed test run, append a row to the QA
  tracking sheet's `Log` tab, then create a next-morning 30-minute review invite
  with a Google Meet link, holding the invitation send until confirmed.
- **Google surface(s):** Sheets + Calendar (multi-service).
- **Depth:** deep.

## 2. Routing decision

- **Chosen topic:** `google-apis-integration` → `references/google-apis-integration.md`
- **Why:** two Google services in one workflow → multi-service integration rule. [DOC]
- **Rejected alternatives:** `google-sheets-mcp` and `google-calendar-mcp` alone
  each cover only half the workflow; loading both would violate one-route. [INFERENCE]
- **Routes loaded:** exactly one. [DOC]

## 3. Operation plan

| # | Operation (official surface) | Auth profile | Least-privilege scope/key | Mutating? | Idempotency key | Read-back step |
|---|---|---|---|---|---|---|
| 1 | `sheets.spreadsheets.values.get` (`Log!A1:E1`) | OAuth | `spreadsheets.readonly` | no | n/a | confirms header shape [DOC] |
| 2 | `sheets.spreadsheets.values.append` (`Log!A:E`, `USER_ENTERED`) | OAuth | `drive.file` if app-opened, else `spreadsheets` | yes | `sheet-append-<runId>` | `values.get` on appended range [CODE] |
| 3 | `calendar.events.insert` (Meet via `conferenceData`) | OAuth | `calendar.events` | yes | `cal-<eventHash>` | `events.get` on new id [CODE] |

## 4. Read-before-write & confirmation

- **Discovery (read-only first):** op #1 reads the header before any append. [CODE]
- **Human confirmation:** op #2 and op #3 both `pending` until the user confirms;
  `sendUpdates=all` on op #3 is withheld until consent = confirmed. [DOC]
- **Consent text / phrase:** required for the Calendar invitation (it emails
  attendees). [DOC]

## 5. Retry & error handling

- 400 `INVALID_ARGUMENT` → fix A1 range / `valueInputOption`; do not retry. [DOC]
- 401/403 → refresh token or re-consent; 403 `PERMISSION_DENIED` likely scope
  too narrow (e.g. `readonly` for the append). [INFERENCE]
- 429 → exponential backoff, batch where possible. [DOC]
- 5xx → bounded retry reusing the same idempotency key. [DOC]

## 6. Secrets posture

- [x] No client secret, refresh token, or key-file path appears in this plan. [CODE]

## 7. Residual risks (each with a verify step)

- `Log` header may have fewer columns than the write body → verify: stop and
  re-confirm the target range after op #1. [INFERENCE]
- "Next morning" depends on the owner's timezone → verify: echo the absolute
  RFC3339 start time back before op #3. [ASSUMPTION]
- App may not have created/opened the sheet → verify: confirm before defaulting
  to `drive.file`; escalate to `spreadsheets` only if cross-file edit is needed. [INFERENCE]

## 8. Acceptance gate

- [x] Exactly one route loaded; topic matches surface. [DOC]
- [x] Scopes least-privilege; Sheets bound to file not tab; no broad `drive`. [DOC]
- [x] Mutations gated by consent + read-before-write + idempotency. [CODE]
- [x] Secrets policy honored. [CODE]
- [x] Error/quota taxonomy covered. [DOC]
- [x] Evidence tags present; assumptions paired with verify. [DOC]

_Live execution (the actual append and invite) is a separate human-reviewed step.
No quotas or prices invented._
