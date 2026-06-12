# Google Workspace Routing Plan — <request title>

> Offline plan/checklist only. No live Google/OAuth/HTTP/MCP call is made here.
> Live execution is a separate human-reviewed step. [DOC]

## 1. Request & surface

- **Request restated:** <one-line restatement>
- **Google surface(s):** <Sheets | Docs | Slides | Drive | Calendar | Maps | GA4 | multi-service>
- **Depth:** <quick | deep>

## 2. Routing decision

- **Chosen topic:** `<topic>` → `references/<topic>.md`
- **Why:** <rule applied, e.g. "single service named", "GA4 reporting not setup">
- **Rejected alternatives:** <topic(s) considered and why not>
- **Routes loaded:** exactly one. [DOC]

## 3. Operation plan

| # | Operation (official surface) | Auth profile | Least-privilege scope/key | Mutating? | Idempotency key | Read-back step |
|---|---|---|---|---|---|---|
| 1 | <e.g. spreadsheets.values.get> | <OAuth / API key> | <scope or key profile> | <yes/no> | <key or n/a> | <get/list call or n/a> |

## 4. Read-before-write & confirmation

- **Discovery (read-only first):** <get/list operations run before any write>
- **Human confirmation:** <confirmed / pending> for each mutating op
- **Consent text / phrase:** <if required, e.g. Calendar invites>

## 5. Retry & error handling

- User-fix (400): <handling>
- Auth (401/403, refresh/re-consent): <handling>
- Quota/rate (429, backoff): <handling>
- Transient (5xx, bounded retry): <handling>

## 6. Secrets posture

- [ ] No client secret, refresh token, or key-file path in this plan or fixtures. [CODE]

## 7. Residual risks (each with a verify step)

- <risk> → verify: <step>

## 8. Acceptance gate

- [ ] Exactly one route loaded; topic matches surface. [DOC]
- [ ] Scopes least-privilege; Sheets bound to file not tab; Maps uses API key. [DOC]
- [ ] Mutations gated by consent + read-before-write + idempotency. [CODE]
- [ ] Secrets policy honored. [CODE]
- [ ] Error/quota taxonomy covered. [DOC]
- [ ] Evidence tags present; assumptions paired with verify. [DOC]

_Evidence tags: `[DOC]` `[CONFIG]` `[CÓDIGO]`/`[CODE]` `[INFERENCE]` `[ASSUMPTION]`. No invented quotas/prices._
