# Body of Knowledge — sales-bizdev

Domain foundations for the seven sales/bizdev deliverable families this skill routes to. Concepts here are the shared substrate the playbooks draw on; the playbooks add the step-by-step execution.

## 1. The pre-sale value chain

The skill covers a single arc — **find → research → reach → persuade → propose** — and stops before delivery and billing.

```
client-prospecting → client-dossier → b2b-outreach → executive-pitch / proposal-writing
        ↑                                                          ↑
   lead-generation (inbound feed)                         sales-collateral (supports all stages)
```

Each topic is a distinct deliverable, not a phase you must run in order. The router picks one by the *artifact the user needs*, not by where the account sits in the funnel.

## 2. Ideal Customer Profile (ICP) — the foundation

A weak ICP produces a weak everything-downstream. A complete ICP has four dimension classes:

- **Firmographic:** industry, headcount, revenue range, geography, business model, growth stage, ownership.
- **Technographic:** stack compatibility, maturity (spreadsheets = early buyer), cloud provider, key platforms, budget signals.
- **Behavioral / intent:** job postings in the pain category, recent funding, new exec hire, conference attendance, competitor-customer churn, content engagement.
- **Negative ICP (disqualifiers):** a hard gate that removes a prospect *regardless* of fit score. An ICP with zero disqualifiers is incomplete — every real ICP excludes someone.

Decision rule: start **narrow** (one segment, one market) and expand only after the first ~3 customers confirm the ICP. A wide ICP makes scoring weights ambiguous and dilutes learning.

## 3. Qualification frameworks

### BANT + Fit composite (client-prospecting)
- **BANT (0-40):** Budget, Authority, Need, Timing — 0/5/10 per dimension, scored from cited evidence.
- **Fit (0-60):** industry (15) + size (15) + tech signal (10) + geography (10) + behavioral (10).
- **Tiers:** 80-100 = T1 Hot · 60-79 = T2 Warm · 40-59 = T3 Cool · <40 = Disqualified.
- **Gate:** no Tier 1 without a *dated* trigger event ("why now").

### Fit × Intent (lead-generation)
- Score = fit (ICP match) × intent (observed signal). Bands: Hot (strong fit + explicit intent) → route same-day; Warm → nurture, re-score; Cold → hold; Disqualified → drop.
- Never auto-promote on intent alone — high intent + poor fit wastes sales capacity.

### Scoring discipline (both models)
- Evidence over optimism: a job posting is intent ≤5, not a confirmed Need of 10.
- Scores decay — re-score on every new trigger; a stale snapshot is a perishable artifact.
- A disqualifier caps the total no matter the points earned.

## 4. Source reliability tiers (client-dossier)

| Tier | Sources | Tag floor | Trust note |
|------|---------|-----------|------------|
| A — primary | company site, regulatory filings, official PR, GitHub org | `[EXPLICIT]` | authoritative but can be aspirational |
| B — verified 3rd-party | reputable news, funding DBs, conference agendas | `[EXPLICIT]` if attributed | check date; DBs lag |
| C — aggregated/estimated | LinkedIn headcount, BuiltWith, Glassdoor, G2 | `[INFERRED]` | directional; ±15-20% |
| D — inferred/derived | email-pattern guesses, org-chart reconstruction, pain hypotheses | `[OPEN]` | validate before any external use |

Conflict resolution: higher tier or fresher source wins; **never average**. Facts that decay (headcount, stack) defer to the fresh source; facts that don't (founding year, ownership) defer to the primary.

## 5. Outreach mechanics (b2b-outreach)

- **5-touch cadence:** LinkedIn note → cold email → follow-up → social-proof → break-up, with widening day gaps. Each touch adds *new* value; alternate channels.
- **Personalization layers:** (1) company specificity — mandatory; (2) role specificity — map to their KPIs; (3) person specificity — public content only, never fabricated.
- **Deliverability is a precondition:** warm the domain, authenticate (SPF/DKIM/DMARC — operator setup), one ask per email, treat replies as the only hard metric (opens are unreliable).
- **Compliance:** B2B cold email is not uniformly legal — CASL/Canada and some EU states require prior consent. Flag, don't assume.

## 6. Persuasion architecture (executive-pitch)

- **PAS:** Problem (≥3 current-state metrics) → Agitate (per-month inaction burn rate) → Solve (each benefit maps back to a Problem metric).
- **Financial model:** NPV (discount 10-15%, default 12% and tag it), IRR (target >25%, fall back to NPV when cash-flow signs alternate), payback (target <12 mo; report simple + discounted when >$1M), sensitivity (±20% cost / ±10% benefit as a grid).
- **Audience ordering:** CFO → financial case first; CTO → modernization/risk; CEO → strategy; Board → governance + sensitivity (strictest superset).
- The Section-5 budget is the one input that must never be auto-filled — a fabricated number anchors the whole negotiation wrong.

## 7. Proposal anatomy (proposal-writing)

Canonical order: Problem → Outcome → Scope/Anti-scope → Approach → Timeline → Team → Risks → Commercial structure → Next step. Hard requirements: non-empty anti-scope (the margin-killer guard), effort in FTE-months with confidence band, each risk owned + mitigated, exactly one recommended option. **Decline test:** would a skeptical CFO sign?

## 8. Collateral types (sales-collateral)

One artifact answers exactly one buying question: one-pager ("what is this, why now?"), battle card ("how do I win vs. X?"), ROI calculator ("what return, on what assumptions?"), competitive positioning ("where do we win, where do we cede?"). Name a real cede-zone — strawmen kill champion trust.

## 9. Standards & governance (cross-cutting)

- **Evidence taxonomy:** Alfa-core `[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`; some playbooks use `[EXPLICIT]`/`[INFERRED]`/`[OPEN]`. One family, one spelling per output.
- **No invented prices:** FTE-months + disclaimer; route price asks to a human.
- **Single brand:** identify first; stay on the MetodologIA brand.
- **No green-as-success:** state confidence, don't style it.
- **No client PII:** public professional context only; decline personal-data requests and deliver the rest.
- **Every `[SUPUESTO]`/`[OPEN]` carries a verification next step.**

## 10. Common failure modes (and the fix)

- *Score inflation* → require a cited source per non-zero point.
- *Trigger-less Tier 1* → enforce the dated-trigger gate; demote to T2.
- *Confident fabrication* → tag every private-co estimate `[est. — not verified]`.
- *Encyclopedia, not tool* → every dossier/brief must end in one specific next action.
- *Benefit double-count* → reconcile value pillars against the comparison matrix in pitches.
- *Multi-route load* → re-read tie-break rules; if still tied, ask one question.
