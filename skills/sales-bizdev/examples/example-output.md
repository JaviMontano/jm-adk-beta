# Example Output — sales-bizdev

The dossier the skill produces for the `example-input.md` request (Pagomático, JM Labs brand). All company facts below are illustrative placeholders for a fictional account; in a real run each would trace to a cited public source.

> **Brand:** JM Labs · **Topic routed:** client-dossier · **Depth:** Standard (2h tier) · **Date:** 2026-06-12
> **Tag family:** `[EXPLICIT]` (re-openable public source) · `[INFERRED]` (deduced) · `[OPEN]` (validate before use)

## Routing rationale

Request is a one-account prep brief for a specific meeting → `client-dossier`, not `b2b-outreach` (user asked for the brief, not the messages) and not `client-prospecting` (single named target, not a list). `[INFERRED]`

## Input gap flagged

VP of Engineering name not provided. Contact Card below is built against the *role*; **confirm the person via LinkedIn URL before outreach** — do not profile a homonym. `[OPEN]`

## TL;DR (executive brief)

- Pagomático is scaling its payments platform faster than its data/reliability tooling can keep up. `[INFERRED]`
- The clearest "why now": a Series A round closed ~70 days ago, with engineering hiring spiking since. `[EXPLICIT — Crunchbase, illustrative]`
- Opening hook below leads with that trigger, not a generic intro.

## Company DNA

| Field | Value | Tag |
|-------|-------|-----|
| Founded | 2019, founder ex-payments operators | `[EXPLICIT]` (illustrative) |
| Ownership | VC-backed, Series A ~70 days ago | `[EXPLICIT]` (illustrative) |
| Headcount | ~95, eng ~45% | `[est. — not verified, INFERRED via LinkedIn]` |
| Geography | Colombia primary; Mexico expansion signaled | `[EXPLICIT]` (illustrative) |
| Tech stack signal | dbt + Snowflake in job posts; no Airflow listed | `[INFERRED]` |
| Recent move (≤90d) | 5 backend + 3 data-eng roles opened post-round | `[EXPLICIT]` (illustrative) |

## Key contact (role-level — confirm person)

```
Title:           VP of Engineering                              [EXPLICIT — role from request]
Likely priority: Reliability + scaling the payments core as volume grows  [INFERRED]
Best channel:    LinkedIn (warm intro via JM Labs network preferred)      [INFERRED]
Email pattern:   firstname.lastname@pagomatico.co — confidence: Low       [INFERRED — not verified]
Note:            Confirm identity before any outreach                     [OPEN]
```

## Pain hypotheses (ranked)

1. **Data-pipeline orchestration gap.** Evidence: 3 dbt+Snowflake data-eng roles, none Airflow `[EXPLICIT]` + Series A board pressure on metrics `[INFERRED]`. Urgency: acute — postings live this quarter. Hook: install orchestration in <30 days so dbt runs on schedule, not cron hacks. Confidence: Medium. **Validation Q:** "How are you scheduling and monitoring dbt runs across teams today?"
2. **Payments reliability under volume growth.** Evidence: backend hiring spike post-round `[EXPLICIT]` + market expansion to Mexico `[INFERRED]`. Urgency: chronic-becoming-acute. Hook: reliability instrumentation before the next traffic step-change. Confidence: Medium. **Validation Q:** "What's your current p99 on the payment-authorization path during peak?"
3. **Reporting cadence owed to the new board.** Evidence: Series A 70 days ago `[EXPLICIT]` + data-eng hiring `[INFERRED]`. Urgency: quarterly. Hook: trustworthy metrics layer. Confidence: Low (single strong signal). **Validation Q:** "What metrics is the board asking for that are hard to produce today?"

## Approach strategy

- **Entry angle:** recent funding round → growth/scale framing, budget window open. `[INFERRED]`
- **Channel sequence:** LinkedIn connection → message referencing the data-eng postings → warm intro if available.
- **Opening hook:** "Saw Pagomático opened 3 data-engineer roles this quarter — teams scaling payments infra at your stage usually hit the orchestration wall ~60 days after a dbt rollout. We helped a peer cut pipeline failures by 70% in that window. Worth 20 minutes to see if the pattern fits?" `[INFERRED pain + illustrative peer reference]`

## Validation gate — result

- [x] Entity named; person flagged for confirmation (no homonym shipped)
- [x] Private-co headcount tagged `[est.]`; email pattern `[INFERRED — not verified]`
- [x] 3 hypotheses, each ≥2 tagged signals + a validation question
- [x] Public professional data only; no PII
- [x] Single brand (JM Labs); no currency figures
- [x] Ends in one specific opening hook
- [ ] **Blocked until:** VP identity confirmed via LinkedIn URL `[OPEN]`
