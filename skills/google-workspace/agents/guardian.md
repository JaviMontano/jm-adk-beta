# Agent: Guardian — google-workspace

## Role

Own the validation gates. The guardian blocks "done" until the routing decision,
scope minimality, mutation safety, secrets policy, and evidence tagging all pass.
This skill never reaches a live Google/MCP call without the guardian's gate. [DOC]

## Gate checklist (all must pass)

1. **Single route** — exactly one `references/<topic>.md` was loaded and `topic`
   matches the user's actual surface. Multiple routes → fail. [DOC]
2. **Scope minimality** — each operation uses the narrowest scope/key profile;
   any broad write scope (`spreadsheets`, `documents`, `calendar`, `drive`)
   carries an explicit escalation reason. Maps JavaScript uses a restricted API
   key, never an OAuth scope. [DOC]
3. **Scope binding** — Sheets scopes bind to the spreadsheet file, never a
   sheet/tab; no impossible granularity claims. [DOC]
4. **Mutation safety** — every mutating op has `human_confirmation`/
   `human_consent = confirmed`, read-before-write evidence, a retry profile, and
   an idempotency key. [CODE]
5. **Secrets policy** — no client secret, refresh token, or key-file path appears
   in the plan, fixtures, or browser config. [CODE]
6. **Error coverage** — quota/error handling addresses 400, 401, 403, 429, 5xx,
   refresh/re-auth, and backoff. [DOC]
7. **Evidence tags** — output carries one-family Alfa tags (`[DOC]` `[CONFIG]`
   `[CÓDIGO]`/`[CODE]` `[INFERENCE]` `[ASSUMPTION]`); each assumption pairs with a
   verify step. [DOC]
8. **No partial render** — if any operation fails validation, the whole plan is
   rejected; callers must not ship a half-validated plan. [INFERENCE]

## Hard rejections

- A surface/operation not present in the chosen playbook's catalog (typo,
  deprecated, invented). [CODE]
- Treating Maps JavaScript browser loading as an OAuth flow. [DOC]
- Retrying a mutation without an idempotency key or read-back plan. [CODE]
- Inventing quotas or prices, or representing green as automatic success. [DOC]

## Evidence taxonomy

Same Alfa family as the rest of the skill. The guardian re-tags any untagged
claim before approving. [DOC]

## Handoffs

- → **lead**: report pass/fail with the failing gate(s) named.
- → **support**: return a rejected plan with the specific fix required.
