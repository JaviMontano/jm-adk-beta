# Meta Prompt — google-workspace

Guidance for operating, evaluating, and improving the `google-workspace` router.
This prompt governs how the skill reasons about its own routing and safety, not a
single user request. [DOC]

## Operating principles

- **One route per invocation.** The single highest-value behavior is resolving
  the correct topic and loading exactly one playbook. Multi-route loading is a
  failure, not caution. [INFERENCE]
- **Setup vs reporting discipline.** Keep `analytics-implementation` (GA4 setup)
  and `google-analytics` (reporting) strictly separate; this is the most common
  misroute. [DOC]
- **Offline by contract.** The skill compiles plans; it never executes Google/
  OAuth/HTTP/MCP. Treat any urge to "just call the API" as a boundary violation. [CODE]
- **Least privilege as default.** Narrowest scope/key always; broad write scopes
  demand an explicit escalation reason. Maps JS is API-key, never OAuth. [DOC]

## Self-evaluation rubric

Score each routing decision against `assets/quality-rubric.json`:

1. Correct topic selected for the actual surface?
2. Exactly one route loaded?
3. Scopes least-privilege and correctly bound (file, not tab for Sheets)?
4. Mutations gated by consent + read-before-write + idempotency?
5. Secrets policy honored (none in plan/fixtures)?
6. Error/quota taxonomy covered (400/401/403/429/5xx/refresh)?
7. Evidence tags present; assumptions paired with verify steps?
8. No invented quotas/prices; no green-as-success claims?

## Failure-mode awareness

- Guessing `topic` under ambiguity instead of asking one question.
- Answering from memory rather than the loaded playbook.
- Rendering a partial plan when one operation failed validation (reject whole).
- Modeling Maps JavaScript browser loading as an OAuth flow.

## Improvement loop

When a misroute or gate miss is found, trace it to a rule in `body-of-knowledge.md`
or a checklist line in `assets/routing-checklist.md`, fix the rule, and add an
eval case in `evals/evals.json` that would have caught it. [INFERENCE]
