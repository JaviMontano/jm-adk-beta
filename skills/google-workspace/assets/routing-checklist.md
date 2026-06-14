# Routing Checklist — google-workspace

Run top to bottom on every invocation. Stop at the first hard-fail. [DOC]

## A. Resolve

- [ ] Surface(s) named: Sheets / Docs / Slides / Drive / Calendar / Maps / GA4 /
      multi-service.
- [ ] If no Google surface → **decline**. [INFERENCE]
- [ ] One service → its topic. Two+ or "integrate/connect" →
      `google-apis-integration` (or `apis` for Gmail-inclusive automation). [DOC]
- [ ] GA4 *setup/instrumentation* → `analytics-implementation`; GA4 *reporting/
      tagging/DebugView* → `google-analytics`. [DOC]
- [ ] Ambiguous between two topics → ask ONE question, then stop. [INFERENCE]

## B. Load

- [ ] Read EXACTLY ONE `references/<topic>.md`. [DOC]
- [ ] No second route loaded "to be safe". [INFERENCE]

## C. Plan (per operation)

- [ ] Operation maps to an official surface in the playbook's catalog (no
      invented endpoint). [CODE]
- [ ] Least-privilege scope/key chosen; broad write scope has an escalation
      reason. [CODE]
- [ ] Sheets scope binds to the spreadsheet file, never a tab. [DOC]
- [ ] Maps JavaScript uses a restricted API key (referrer + API allowlist), not
      OAuth. [DOC]
- [ ] `append` vs `update` chosen by intent (append = next empty row). [DOC]

## D. Mutation gates

- [ ] Read-only discovery precedes any write. [CODE]
- [ ] `human_confirmation`/`human_consent = confirmed` on each mutation. [CODE]
- [ ] Idempotency key + read-back step on each mutation. [CODE]
- [ ] Calendar invitation `sendUpdates` withheld until consent. [DOC]

## E. Safety & governance

- [ ] No secrets in plan/fixtures/browser config. [CODE]
- [ ] Error/quota taxonomy covers 400/401/403/429/5xx/refresh. [DOC]
- [ ] Alfa evidence tags present; assumptions paired with verify steps. [DOC]
- [ ] No invented quotas/prices; green not asserted as success. [DOC]
- [ ] Output is a plan/checklist; live execution flagged as a separate step. [CODE]
