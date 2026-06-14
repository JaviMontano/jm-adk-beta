# Example output — market-intel → partnership-strategy (depth=quick)

> Snapshot as of 2026-06-12. Point-in-time; partner data decays.

## Routing decision

- **Topic:** partnership-strategy
- **Depth:** quick
- **Playbook loaded:** references/partnership-strategy.md
- **Evidence family:** Alfa core ([DOC] [CONFIG] [INFERENCIA] [SUPUESTO]) +
  playbook-local [INFERENCE]/[ASSUMPTION]
- **Why this topic:** "co-marketing / score candidates / kill criteria" → partner
  qualification, not positioning or pricing. [INFERENCIA]

## Discover — inputs

| Input | Source | As-of | Tag |
|---|---|---|---|
| ICP = mid-market delivery leads | user brief | 2026-06-12 | [CONFIG] |
| 3 named candidates + overlap notes | user brief | 2026-06-12 | [DOC] |
| Goal = extend reach via co-marketing | user brief | 2026-06-12 | [CONFIG] |

## Analyze — fit score (5 axes, default weights)

| Candidate | Overlap (.30) | Reach (.20) | Fit (.20) | Effort (.15) | Reputation (.15) | Score | Verdict |
|---|---|---|---|---|---|---|---|
| Agile-coaching newsletter | 5 | 4 | 5 | 4 | 4 | **4.40** | Pursue (≥3.5) |
| BI consultancy | 3 | 3 | 3 | 3 | 4 | **3.15** | Park (2.5–3.5) |
| Competing PM tool | 1 | 4 | 1 | 2 | 3 | **1.95** | Drop (<2.5) |

Scoring notes:
- Newsletter scores overlap 5: same ICP, **non-overlapping** customers — the
  ideal co-marketing profile. [INFERENCE]
- Competing PM tool scores fit 1: directly competing offer → channel conflict /
  cannibalization, not partnership. Drop regardless of reach. [INFERENCE]
- BI consultancy is adjacent — parked pending a net-new-audience estimate. [SUPUESTO]

## Findings

- Pursue the **agile-coaching newsletter** (4.40); it closes the reach gap with
  least new machinery (Simple First). [INFERENCE]
- The competing PM tool is disqualified on strategic fit, not reach. [INFERENCE]

## Recommendation / next steps (quick pass — program design deferred to deep)

1. Co-marketing motion with the newsletter: first artifact = one co-branded
   guide + one joint webinar; reward = **audience swap (symmetric, no cash)** —
   structure only, no dollar figures. [CONFIG]
2. **Kill criteria** (set with partner at launch): two joint events with **no
   net-new signups → stop**. An undefined kill trigger is an open-ended cost. [INFERENCE]
3. Before activating the BI consultancy, require a net-new-audience estimate to
   resolve the parked score. [SUPUESTO]

## Evidence summary

- Tags: [CONFIG] 27%, [DOC] 9%, [INFERENCE] 45%, [SUPUESTO] 18%. Below the >30%
  assumption-banner threshold (only [SUPUESTO] counts), no WARNING needed. [DOC]
- No dollar figures emitted; reward expressed as structure per governance. [CONFIG]
- Single brand (MetodologIA); no client PII. [CONFIG]
