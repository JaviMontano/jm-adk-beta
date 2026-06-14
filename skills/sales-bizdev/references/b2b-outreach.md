<!-- distilled from alfa skills/b2b-outreach -->
<!-- > -->
# B2B Outreach — Sequences That Start Conversations

> TL;DR: Design a multi-touch B2B outreach sequence — cold intro to follow-up — with persona-specific hooks, channel strategy, response handlers, and a ready-to-deploy CSV tracking template.

**Principio Rector:** Personalization at scale beats volume. One relevant message outperforms ten generic ones.

**Tag convention:** This file uses the Alfa-style inline tags `[EXPLICIT]` (stated in this playbook or by the user) and `[INFERRED]` (deduced practice, validate against your own data). Structural labels `[FIXED]`/`[PERSONALIZED]` mark message-block reuse, not provenance. Do not mix in other tag families. [EXPLICIT]

---

## When to Activate

**Activate when:**
- User says "outreach sequence", "cold email", "B2B outreach", "prospecting messages" [EXPLICIT]
- User says "contact X company", "sales sequence", "follow-up cadence" [EXPLICIT]
- User needs to reach a specific persona or company with a product/service offer [EXPLICIT]
- User is launching a new sales motion and needs templates [INFERRED]

**Do NOT activate when:**
- User needs a single one-off email (use a writing skill instead) [EXPLICIT]
- User needs legal/compliance review of outreach (consult legal counsel) [EXPLICIT]
- User is targeting consumers (B2C) — this skill is B2B-specific [EXPLICIT]

**Anti-scope (explicitly out of bounds):**
- Email-sending infrastructure setup (SPF/DKIM/DMARC config, warm-up tooling) — name the requirement, hand off to the operator [EXPLICIT]
- Buying or scraping contact lists — provenance and consent are the user's legal responsibility [EXPLICIT]
- Guaranteeing reply/open rates — all benchmarks here are directional, not commitments [EXPLICIT]

**Inputs required before generating (stop and ask if missing):**
- Offer / value proposition and the proof point (case study, metric, integration) [EXPLICIT]
- Target persona and at least one named account [EXPLICIT]
- Sender identity and a real sending channel (domain, LinkedIn profile) [EXPLICIT]
- Missing any of these → produce a partial draft and flag the gap; never fabricate the proof point [EXPLICIT]

---

## S1 — Prospect Qualification

Before writing a single message, qualify the prospect and identify buying signals. [EXPLICIT]

### 1a. ICP Fit Check

Score the prospect against the Ideal Customer Profile before investing in outreach: [INFERRED]

| Dimension | Questions to Answer |
|-----------|-------------------|
| Firmographic fit | Industry? Company size? Revenue range? Geography? |
| Technographic fit | Do they use tech we integrate with or replace? |
| Behavioral fit | Are they hiring for roles that signal the pain we solve? |
| Timing fit | Recent trigger event? (funding, launch, exec change, expansion) |
| Budget signals | Series B+? PE-backed? Public company? |

**Qualification Score (1-5 per dimension, 5 dimensions → 5-25 total):** [INFERRED]
- 20-25: Priority target — invest full personalization effort
- 14-19: Mid-tier — use semi-personalized templates
- Below 14: Low fit — exclude or use lowest-cost channel only

**Scoring discipline:** Score against evidence you can cite, not optimism. If two dimensions are unknown, cap the score and tag the gap rather than guessing high — an inflated score wastes the most expensive (high-touch) effort on the wrong account. [INFERRED]

### 1b. Buying Signals (Trigger Events)

Trigger events dramatically increase response rates because they create a credible reason to reach out *now*. Look for: [INFERRED]

| Signal | What It Means | Outreach Angle |
|-------|--------------|----------------|
| Series A/B funding | New budget, new initiatives | "Congrats on the raise — scaling challenges are next..." |
| New C-suite hire | New priorities, open to evaluation | "Fresh eyes often see what has been missing..." |
| Job postings in pain area | Budget allocated to solve this problem | "You are hiring for X — that usually means..." |
| Product launch | Expansion mode, new use cases | "Your launch creates an interesting opportunity..." |
| Competitor win in their space | Fear of missing out | "Your competitor just achieved X..." |
| Conference attendance | Warmer context for connection | "I saw you were at [event] last week..." |

**Trigger freshness:** A trigger older than ~90 days reads as stale ("congrats on the raise" six months late signals you are recycling a list). Prefer triggers from the last 30-45 days; if the only signal is older, drop to an industry-level hook (see Edge Cases). [INFERRED]

---

## S2 — Outreach Sequence Design

The 5-Touch Model: structured cadence across multiple channels. [EXPLICIT]

### 5-Touch Sequence Framework

```
Touch 1 (Day 1):   LinkedIn connection request + short personal note
Touch 2 (Day 3):   Cold email — value hook + one relevant insight + soft CTA
Touch 3 (Day 7):   LinkedIn InMail or email follow-up — add a new piece of value
Touch 4 (Day 12):  Email — case study or social proof + direct ask
Touch 5 (Day 18):  Break-up message — low pressure, keep the door open
```

**Why this shape:** Each touch must add *new* value, never "just following up." Alternating channels (LinkedIn ↔ email) increases the chance one lands and avoids fatiguing a single inbox. Day gaps widen toward the end so the cadence does not feel like pressure. [INFERRED]

**Timing Principles:**
- Never send Touch 1 and Touch 2 on the same day [EXPLICIT]
- Tuesday-Thursday, 7-9am or 1-3pm local time yields highest open rates [INFERRED]
- Avoid Mondays (inbox chaos) and Fridays (disengaged) [INFERRED]
- If any touch gets a response, pause the sequence immediately [EXPLICIT]
- Honor the recipient's time zone, not the sender's — a 7am local send computed in the wrong zone lands at 2am [INFERRED]

**Trade-off — shorter vs longer cadence:** Compressing to 3 touches (volume play) trades reply rate for reach; most replies arrive on Touches 2-4, so cutting Touch 4/5 forfeits the case-study and break-up moments that recover otherwise-lost prospects. Extend the gaps (not the count) for senior personas who decide slowly. [INFERRED]

### Channel Mix by Persona

| Persona | Best Primary | Best Secondary | Avoid |
|---------|-------------|---------------|-------|
| Founder / CEO | Email (direct) | LinkedIn | Mass sequences |
| VP / Director | LinkedIn InMail | Email | Cold calls without context |
| Manager | Email | LinkedIn | Over-formal procurement tone |
| Technical Lead | LinkedIn (content comment) | Email | Generic business pitch |
| Enterprise Procurement | Formal email | Phone | Social messages |

### Deliverability Guardrails (cold email)

A perfect message that lands in spam has a 0% reply rate, so treat deliverability as a precondition, not an afterthought: [INFERRED]
- Warm the sending domain/mailbox before volume; sudden spikes from a cold domain trip spam filters [INFERRED]
- Keep cold-email volume modest per mailbox per day; split across mailboxes rather than blasting one [INFERRED]
- Avoid spam-trigger patterns: heavy links, image-only bodies, "FREE"/"$$$", misleading subject lines [INFERRED]
- Authenticate the domain (SPF/DKIM/DMARC) — this is operator setup, flag it as a dependency [EXPLICIT]
- One clear ask per email; multiple links and attachments depress both deliverability and replies [INFERRED]

---

## S3 — Personalization Framework

Personalization must be real — not just inserting a first name into a template. [EXPLICIT]

### Personalization Layers

**Layer 1 — Company Specificity (mandatory for all touches):**
- Reference a specific product, news item, or milestone of their company [EXPLICIT]
- Mention a competitor or industry trend directly relevant to them [INFERRED]
- Do NOT use: "I was checking out your website and noticed..." (overused, signals automation) [EXPLICIT]

**Layer 2 — Role Specificity (for Touches 1-3):**
- Map your value to their specific KPIs and responsibilities [INFERRED]
- VP Sales cares about: pipeline, conversion rates, rep ramp time
- VP Engineering cares about: velocity, technical debt, incident rate
- CFO cares about: unit economics, burn rate, cost of capital
- CHRO cares about: retention, time-to-hire, L&D ROI

**Layer 3 — Person Specificity (for high-priority targets):**
- Reference their LinkedIn post, podcast appearance, or published article [EXPLICIT]
- Note a shared connection, alumni network, or event [EXPLICIT]
- Never fabricate a personal detail — only use publicly confirmed information [EXPLICIT]

### Personalization Efficiency

For high-volume sequences (50+ targets), use a semi-personalized approach: [INFERRED]

```
[FIXED]        Generic value proposition paragraph
[PERSONALIZED] Company-specific hook (1 sentence, researched per target)
[FIXED]        CTA and sign-off
```

This allows 80% of the message to be reused while the key hook remains specific. The hook must lead the message — a generic opener followed by a buried personal line reads as templated. [INFERRED]

**Worked example — turning research into a Layer-1 hook:**
- Raw signal: "Pedidos Ya press release: expansion into 3 new LatAm markets" [EXPLICIT]
- Weak hook (restates the fact): "I saw you expanded into 3 new markets." [INFERRED]
- Strong hook (fact → implied pain → your value): "Expanding into 3 markets at once usually surfaces retention gaps that were invisible at smaller scale." [INFERRED]
The strong version earns the reply because it connects the public fact to a problem the reader feels. [INFERRED]

---

## S4 — Message Templates by Persona

### Template A: Founder / CEO (Concise, peer-level)

**Touch 1 — LinkedIn note:**
> Hi [Name], saw [Company] just [trigger event]. Building something in the [space] as well — would love to connect.

**Touch 2 — Cold email:**
> Subject: [Company] + [Your Company] — quick thought
>
> [Name],
>
> [1-sentence company-specific hook based on trigger event].
>
> We help [ICP description] [specific result] — [Reference Company] went from [before state] to [after state] in [timeframe].
>
> Worth a 20-minute call to see if there is a fit?
>
> [Your Name]

**Touch 4 — Social proof follow-up:**
> [Name], following up from my earlier note.
>
> We just published a case study on how [Similar Company] [achieved result]. Thought it might be relevant given [company-specific reason].
>
> Still happy to show you how it applies to [Company] specifically.

**Touch 5 — Break-up:**
> [Name], I will stop reaching out after this. If [pain point] becomes a priority, I am one message away.
>
> Best of luck with [specific initiative].

### Template B: VP / Director (Results-oriented)

**Touch 2 — Cold email:**
> Subject: [Specific metric] for [their company name]
>
> Hi [Name],
>
> [Company-specific hook: what you noticed about their situation].
>
> [Your company] helps [role title] at [company type] [achieve metric outcome]. One example: [Reference Company] reduced [metric] by [X]% in [timeframe].
>
> I have 3 ideas specific to [Company] that might help. 15 minutes this week?
>
> [Your Name]

### Template C: Technical Lead (Credibility-first)

**Touch 2 — Cold email:**
> Subject: [Their tech stack tool] + [your product] integration
>
> Hi [Name],
>
> I saw [Company] is using [specific tool from their stack] — we built a native integration that [specific technical outcome].
>
> Happy to share the integration docs if useful. No pitch — just the technical context.
>
> [Your Name]

### Subject Line Variants (A/B test, 3 per email touch)

Ship three angles so the user can test which resonates; never auto-pick a winner without data: [EXPLICIT]

| Angle | Pattern | Example |
|-------|---------|---------|
| Curiosity | "[Reference]'s [outcome] — relevant for [Company]?" | "Rappi's churn fix — relevant for Pedidos Ya?" |
| Metric | "[Metric] for [Company]" | "34% lower churn for Pedidos Ya" |
| Question | "[Pain point as a question]?" | "Retention slipping as you expand LatAm?" |

Keep subjects under ~50 characters (mobile truncation), lowercase-leaning, and never clickbait the body can't pay off. [INFERRED]

---

## S5 — Output — Scripts + CSV Tracker Template

### Sequence Output Format

For each sequence, deliver:
1. **Sequence brief** — ICP fit score, trigger event used, personalization notes [EXPLICIT]
2. **Touch 1-5 scripts** — complete message text, ready to copy-paste [EXPLICIT]
3. **Subject line variants** — 3 options per email touch for A/B testing [EXPLICIT]
4. **Response handlers** — what to say if they respond positively, negatively, or ask for more info [EXPLICIT]

### Response Handlers (referenced by the Validation Gate — deliver these every time)

| Reply type | Goal | Response pattern |
|-----------|------|-----------------|
| Positive ("interested / let's talk") | Convert to a booked meeting fast | Thank them, propose two concrete time slots + a booking link, restate the value in one line. Do not re-pitch. [INFERRED] |
| Asks for info ("send a deck / pricing") | Keep momentum, avoid a doc black-hole | Send the minimum that answers, then anchor to a call: "Quick deck attached — 15 min is faster than email for the parts specific to [Company]?" [INFERRED] |
| Objection ("we use [competitor] / no budget") | Reframe, don't argue | Acknowledge, offer one differentiated angle or a relevant case, leave the door open: "Makes sense — many [Reference] teams ran [competitor] until [specific gap]. Worth 10 min if that ever bites?" [INFERRED] |
| Negative ("not interested / stop") | Exit cleanly, protect reputation | Honor immediately, confirm removal, log a 90-day window. Never push past an explicit no — it risks spam reports and brand damage. [EXPLICIT] |
| Wrong person ("talk to [name]") | Get the warm referral | Thank them, ask for a quick intro to the named person, reference the referrer in the new thread. [INFERRED] |
| No response (after Touch 5) | Preserve the relationship | Stop the active sequence; move to a low-frequency nurture or re-trigger on the next buying signal. [INFERRED] |

### CSV Tracker Template

```csv
Prospect,Company,Title,LinkedIn,Email,ICP Score,Trigger Event,T1 Date,T1 Status,T2 Date,T2 Status,T3 Date,T3 Status,T4 Date,T4 Status,T5 Date,T5 Status,Response,Response Date,Next Step,Notes
[Name],[Co],[VP Role],linkedin.com/in/...,[email],22,Series B funding,2024-01-15,Sent,2024-01-17,Opened,,,,,,,Positive,2024-01-18,Discovery call booked,[note]
```

**Status values:** Sent / Opened / Clicked / Replied / Bounced / Not sent
**Response values:** Positive / Negative / Neutral / No response
**Next Step values:** Discovery call / Follow-up in 30d / Disqualified / Closed

**Tracker hygiene:** A `Bounced` status on any email touch invalidates the address — stop the sequence for that row and do not retry, repeated bounces damage sender reputation. Open/Click tracking via pixels is increasingly unreliable (privacy proxies pre-fetch images); treat opens as weak signal and replies as the only hard metric. [INFERRED]

---

## Trade-off Matrix

| Mode | Personalization | Sequence Length | Volume | Output | Pick when |
|------|---------------|----------------|--------|--------|-----------|
| **High-touch** | Full 3-layer | 5 touches | 5-10 targets/week | Custom scripts per person | High ACV / few strategic accounts; reply quality > reach [INFERRED] |
| **Semi-personalized** | Company hook only | 5 touches | 20-50/week | Template + variable fields | Defined ICP, repeatable motion; the default mode [INFERRED] |
| **Volume play** | Name + industry only | 3 touches | 100+/week | Pure template + A/B variants | Low ACV / large TAM; accept lower reply rate for reach [INFERRED] |

**Decision rule:** Match mode to deal economics — high-touch on a $2k ACP is unprofitable; volume play on a six-figure enterprise deal under-invests and burns the account. When unsure, start semi-personalized and move a replying account to high-touch. [INFERRED]

---

## Assumptions & Limits

- Message content must be truthful — no fabricated social proof, case studies, or metrics [EXPLICIT]
- GDPR/CAN-SPAM compliance: include unsubscribe mechanism and a valid physical address in email sequences; B2B cold email is *not* uniformly legal (CASL/Canada and some EU member states require prior consent — flag, don't assume) [EXPLICIT]
- LinkedIn has connection and InMail limits and prohibits automation tools — respect platform rules; aggressive automation risks account restriction [EXPLICIT]
- Response rate benchmarks are indicative — actual results vary by industry, list quality, and offer; never present them as guarantees [EXPLICIT]
- This skill produces scripts — actual sending, deliverability setup, and list provenance are the user's responsibility [EXPLICIT]
- Timing/open-rate guidance is inferred from general practice; validate against the user's own send data before treating as fact [INFERRED]

---

## Edge Cases

| Scenario | Handling |
|----------|---------|
| Target is a sole founder with no public contact | Use LinkedIn DM as primary; note limited scalability [INFERRED] |
| Company has stated no-cold-email policy | Respect it; use LinkedIn or warm intro only [EXPLICIT] |
| Target replied negatively to Touch 2 | Pause sequence; log for 90-day re-engage window [EXPLICIT] |
| Target works at a direct competitor | Flag to user; proceed only if user confirms specific use case [EXPLICIT] |
| No trigger event found for prospect | Use industry-level hook instead; lower personalization layer [INFERRED] |
| Email bounces / address unverifiable | Stop the row; switch to LinkedIn or skip — never guess address permutations and retry [INFERRED] |
| Region requires opt-in consent (CASL/EU) | Do not cold-email; switch to consent-based or warm channels and flag the legal constraint to the user [EXPLICIT] |
| Out-of-office / on leave reply | Not a real engagement; reset the cadence to resume after the stated return date [INFERRED] |
| Auto-reply "I've left the company" | Treat as wrong-person; mark row disqualified and seek the replacement contact [INFERRED] |

---

## Good vs Bad Example

**BAD Touch 2 email** (no hook, generic value, weak CTA — signals a blast):
> "Hi [Name], I hope this message finds you well. I am reaching out to introduce our solution which helps companies improve their processes. Would you like to schedule a call?"

**GOOD Touch 2 email** (trigger-led hook → quantified proof → single low-friction ask):
> Subject: Rappi's churn fix — relevant for Pedidos Ya?
>
> Hi Maria,
>
> Pedidos Ya just expanded into 3 new LatAm markets — that usually surfaces retention challenges not visible at smaller scale.
>
> We helped Rappi reduce early churn by 34% in 6 months by instrumenting the activation funnel they could not measure before.
>
> 20 minutes to walk through whether the same approach fits your situation?
>
> Javier

**Why the good one works:** named trigger (specificity), implied pain (relevance), one concrete proof with a number (credibility), exactly one ask with a small time commitment (low friction). Strip any of the four and reply rate drops. [INFERRED]

---

## Validation Gate

- [ ] ICP fit score calculated before writing the sequence
- [ ] Trigger event identified, fresh (<90d), and used in Touch 1 and Touch 2 hooks
- [ ] 5-touch sequence complete with dates, channels, and recipient-local timing specified
- [ ] Touch 1 and Touch 2 fully written (complete text, not just described)
- [ ] 3 subject line variants provided for each email touch (curiosity / metric / question)
- [ ] Personalization layer declared (full / company-hook / name-only) and matched to mode
- [ ] Break-up message (Touch 5) included
- [ ] Response handlers written for positive, info-request, objection, negative, and no-response outcomes
- [ ] CSV tracker template delivered alongside scripts
- [ ] No fabricated metric, case study, or personal detail (every proof point is real)
- [ ] GDPR/CAN-SPAM/region compliance acknowledged (unsubscribe + consent constraints noted)

---

## Reference Files

- `knowledge/body-of-knowledge.md` — Sales methodology and outreach frameworks
- `knowledge/knowledge-graph.md` — Persona-to-pain-to-message mapping
- `evals/` — Scored sequence examples
- `../../references/verification-tags.md` — Tag taxonomy (this file uses the `[EXPLICIT]`/`[INFERRED]` Alfa-style convention)

---

## Related Skills

- `client-dossier` — Research the target before writing the sequence
- `client-prospecting` — Build the lead list that feeds this skill
- `market-intelligence` — Identify trigger events and company signals for personalization
- `executive-pitch` — Extend the sequence into a full pitch for qualified leads
