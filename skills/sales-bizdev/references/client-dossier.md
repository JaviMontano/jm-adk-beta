<!-- distilled from alfa skills/client-dossier -->
<!-- > -->
# Client Dossier — Intelligence Brief for High-Stakes Meetings

> TL;DR: Transform public signals about a prospect into a battle-ready dossier — company DNA,
> key contacts, pain hypotheses, and a personalized approach strategy. Output: branded HTML
> dossier (JM Labs dark style) + optional markdown summary.

**Principio Rector:** Prepare like a detective, enter like a consultant. Every fact verified,
every hypothesis labeled. A dossier is not an encyclopedia — it is a decision support tool.

**Tag convention (this file):** `[EXPLICIT]` = stated in a public source the reader can re-open ·
`[INFERRED]` = deduced from signals, not directly stated · `[OPEN]` = unconfirmed, needs validation
before use. One tag per claim; when two could apply, pick the weaker (`[INFERRED]` over `[EXPLICIT]`,
`[OPEN]` over `[INFERRED]`). Do NOT swap in any other taxonomy — these three are the contract for
every dossier output. [EXPLICIT]

**Definition of done:** A dossier is complete when it (a) names a target verified as the right entity,
(b) carries ≥3 pain hypotheses each backed by ≥2 tagged signals, (c) names ≥1 decision-maker with a
reachable channel, (d) ends in a single specific outreach hook, and (e) passes the Validation Gate.
A dossier that lists facts but produces no next action has failed its only job. [INFERRED]

---

## When to Activate

**Activate when:**
- User says "build dossier on [company/person]", "research [company X]", "client profile for [name]"
- User says "quién es [empresa]", "investiga a [empresa]", "perfil de prospecto para [nombre]"
- User says "dossier for sales call", "prep for meeting with [company]", "who is [person] at [company]"
- A sales or BD context is active and a company or executive name is the primary input [INFERRED]
- User provides a company name and asks for entry strategy, pain points, or stakeholder map [INFERRED]
- User has a discovery call in <48h and needs preparation material [INFERRED]

**Do NOT activate when:**
- User is asking for general market research without a named target (use market-intelligence instead)
- The request is about internal team members or employees (use stakeholder-mapping instead)
- The request is about a private individual in a non-business context (privacy concern — decline)
- User wants a competitive landscape across multiple players (use competitive-intelligence instead)
- Input is too vague: "research my industry" — no named target present, clarify first
- User needs legal/financial due diligence for M&A (requires specialized legal tools, not this skill)

**Anti-scope (in-context but explicitly out):** No paid data-broker or people-search lookups (ZoomInfo
contact pulls, Spokeo, BeenVerified). No scraping behind logins or paywalls. No revenue figure
presented as fact for a private company. No personal-life, home-address, family, or health data on any
individual. No bypassing a site's robots.txt or ToS to gather data. If a request needs any of these,
decline the specific element and deliver the rest. [EXPLICIT]

---

## S1: Dossier Types

Three dossier modes, each with a distinct research agenda. Infer the mode from phrasing.
If ambiguous, ask: "Is this a company dossier, an executive profile, or a partnership evaluation?"

**Company Dossier** [EXPLICIT]
Full organizational profile. Used before a first meeting, RFP response, or partnership pitch.
Covers founding story, ownership, revenue signals, headcount trajectory, tech stack, recent
strategic moves, and cultural tone. Most common mode. Output: all 6 sections (S2–S5 + HTML).

**Executive / Public Figure Dossier** [EXPLICIT]
Profile of a named decision-maker. Used to personalize outreach, prepare for a call, or
understand a gatekeeper. Covers career arc, public positions, speaking topics, known priorities,
management style signals, and mutual connections.
Strict scope: public professional information only. No personal life, no private data inference.
Do not include home addresses, personal social media, family data, or non-professional history.

**Partnership Target Dossier** [INFERRED]
Hybrid of company + lead contact. Used when evaluating a channel partner, reseller, or
co-builder. Emphasizes business model alignment, revenue complementarity, integration potential,
and historical partnership behavior: who they partner with, on what terms, and how long those
partnerships last.

**Minimum viable input per mode:**

| Mode | Required | Useful extras |
|---|---|---|
| Company | Company name | Website, LinkedIn URL, industry |
| Executive | Full name + company | LinkedIn URL, role title |
| Partnership | Company name + relationship type | Customer segment, known tech stack |

**Dossier depth options:**

| Mode | Time | Scope | Use case |
|---|---|---|---|
| Flash (30 min) | Fast | Company DNA + 1 contact | Inbound call in <1h |
| Standard (2h) | Medium | Full S2–S5, 2–3 contacts | Tomorrow's discovery call |
| Deep (5h+) | Slow | Full + org chart + competitive context | Strategic account, large deal |

**Why these tiers, not a single flow:** Flash exists because a same-hour inbound dies if you spend 2h
researching; precision loses to timeliness here. Deep exists because on a >$50K account a wrong
decision-maker or missed competitive context costs more than the extra 3h. Default to Standard — it is
the only tier that fits the most common case (a discovery call booked 1–3 days out). [INFERRED]

**Source reliability tiers** — weight every signal by how directly the source states it. When two
sources conflict, the higher tier wins and you note the conflict; never average them. [EXPLICIT]

| Tier | Sources | Tag floor | Trust note |
|---|---|---|---|
| A — primary | Company website, SEC/regulatory filings, official press release, GitHub org | `[EXPLICIT]` | Authoritative but can be aspirational marketing |
| B — verified third-party | Reputable news, funding databases (Crunchbase round data), conference agendas | `[EXPLICIT]` if attributed | Check date; funding DBs lag and miss unannounced rounds |
| C — aggregated/estimated | LinkedIn headcount, BuiltWith, Glassdoor, G2 | `[INFERRED]` | Directional only; LinkedIn headcount ±15-20%, Glassdoor self-selects unhappy reviewers |
| D — inferred/derived | Email-pattern guesses, org-chart reconstruction, pain hypotheses | `[OPEN]` | Must be validated before any external use |

**Conflict resolution:** website says 200 employees, LinkedIn shows 340 → report the LinkedIn figure as
`[est.]` and note the website page may be stale; do not silently pick one. A stale primary source loses
to a fresh aggregated one only on facts that decay (headcount, stack), never on facts that don't (founding
year, ownership). [INFERRED]

---

## S2: Company DNA Framework

Systematic extraction of organizational identity signals. Work through each dimension.
Tag every claim with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`. [EXPLICIT]

**Founding & Ownership**
- Year founded, founding team background (operators vs. investors vs. technologists) [EXPLICIT]
- Current ownership: bootstrapped, VC-backed (series + lead investor), PE-owned, public [EXPLICIT]
- Acquisition history: have they been acquired or acquired others? Signals strategic ambition [EXPLICIT]
- Ownership concentration: founder-led vs. institutional vs. family-controlled [INFERRED]

**Revenue & Growth Signals**
- Public revenue if available; otherwise triangulate from funding rounds + headcount trend [INFERRED]
- Growth stage: pre-PMF, scaling, mature/optimizing, declining/pivoting [INFERRED]
- Geographic footprint: single market, regional, global — matters for solution scope [EXPLICIT]
- Hiring velocity: net new roles in last 90 days signals investment in capability [INFERRED]

**Headcount & Team Composition**
- Total headcount from LinkedIn (snapshot, not exact); engineering % vs. sales % vs. ops % [INFERRED]
- Departures / executive churn: LinkedIn tenure data, Glassdoor reviews as qualitative signal [INFERRED]
- Key department gaps: 5 open data engineer roles → they have an infrastructure problem [INFERRED]
- Note: headcount from LinkedIn can be ±15-20% of actual; label as `[est.]` [EXPLICIT]

**Tech Stack Signals**
- Job posting language: "must know Kubernetes", "experience with Salesforce", "dbt + Snowflake"
- BuiltWith / Wappalyzer (if web-facing product) for frontend/marketing stack [INFERRED]
- GitHub org activity: open-source repos, language distribution, commit frequency [EXPLICIT]
- Integration partners mentioned on their website or in press releases [EXPLICIT]

**Recent News & Strategic Moves (last 90 days)**
- Funding announcements, acquisitions, product launches [EXPLICIT]
- Leadership changes (new CTO/CPO = new agenda, new vendor evaluation cycle) [INFERRED]
- Customer wins / case studies published = proof of strategic direction [EXPLICIT]
- Conference appearances and speaking slots = what narrative they are pushing publicly [INFERRED]
- Regulatory or legal events (SEC filings if public, lawsuit mentions) [EXPLICIT]

**Cultural & Operational Tone**
- Mission language on careers page: "move fast", "customer obsessed", "enterprise-grade" [INFERRED]
- Glassdoor themes: execution culture vs. churn risk; note review recency [INFERRED]
- Social media tone: thought leadership vs. pure broadcast vs. community-engaged [INFERRED]

**Financial Signals Table:**

| Signal | What It Indicates |
|---|---|
| Recent funding round | Available budget, growth phase, investor expectations |
| High job posting volume | Investment areas, team priorities, active pain points |
| Contract announcements | Revenue tiers, deal size norms |
| Downsizing / layoffs | Budget pressure, cost-saving motive, churn risk |
| Awards / rankings | Brand health, employer strength, strategic priorities |
| Re-posted same role 3× | Retention problem or unrealistic hiring bar |

> [OPEN] Revenue figures for private companies are estimates. Flag all inferred revenue
> with `[est. — not verified]` in every output. Never present as confirmed facts.

**Acceptance criteria (S2):** Founding/ownership and growth-stage fields populated or marked `[OPEN]`;
every estimated number date-stamped and `[est.]`-tagged; ≥1 tech-stack signal traced to a concrete
source; recent-moves window limited to last 90 days. [EXPLICIT]

---

## S3: Key Contacts Map

Build a stakeholder map of the target organization focused on the deal or engagement type.
Produce a Contact Card (see template below) for each named person. [EXPLICIT]

**Decision Maker Identification by Deal Type**

| Deal Type | Decision Maker | Influencer | Gatekeeper |
|---|---|---|---|
| Technology / SaaS | CTO, VP Engineering | Engineering Manager | EA, Procurement |
| Consulting / services | CEO, COO | CFO | EA, Legal |
| Training / enablement | CHRO, VP L&D | Department Head | Training Coordinator |
| Data / analytics | CDO, VP Data | Data Lead | Procurement |
| Marketing tech | CMO, VP Marketing | Demand Gen Lead | Marketing Ops |
| Digital transformation | CIO / CDO + C-suite sponsor | COO | PMO, Legal |

**Contact Research Protocol** (execute in this order):
1. LinkedIn search: "[Company] [Title]" — note tenure, previous companies, education [EXPLICIT]
2. Company website team/about page — often lists leadership with bios [EXPLICIT]
3. Search "[Name] [Company] interview" or "[Name] [Company] podcast" for public positions [EXPLICIT]
4. Twitter/X profile for thought leadership signals and engagement patterns [EXPLICIT]
5. Note mutual connections — warm intro is always the highest-value outreach path [INFERRED]

**Email Pattern Inference** (validate before use — never assume confirmed):
- `firstname@company.com` — common at startups and SMB
- `firstname.lastname@company.com` — most common at mid-market and enterprise
- `flastname@company.com` — common in finance and professional services
- `f.lastname@company.com` — frequent in European companies
Use Hunter.io pattern matching (if user has access) or validate via email verification tool.
Label all email patterns as `[INFERRED — not verified]` in output. [EXPLICIT]

Confidence rubric for the pattern: **High** = ≥2 known addresses at the company share the format, or a
verification tool confirms deliverability. **Medium** = inferred from company size/industry norm above,
unverified. **Low** = pure guess, no corroboration. Never send cold to a Low-confidence address — it
risks bounce-rate damage to the sender domain. Prefer LinkedIn or a warm intro when confidence is below
High. [INFERRED]

**Contact Card Template (produce one per person):**
```
Name:              [Full Name]                          [EXPLICIT]
Title:             [Current Title]                      [EXPLICIT]
Tenure:            [X years at company]                 [EXPLICIT]
Prior companies:   [2–3 most relevant past employers]   [EXPLICIT]
Background:        [2-sentence career arc]              [EXPLICIT]
Public positions:  [Key theme they discuss publicly]    [EXPLICIT]
Best channel:      [LinkedIn / email / warm intro via X][INFERRED]
Likely priority:   [What they care about professionally][INFERRED]
Potential concern: [What might make them say no]        [INFERRED]
Email pattern:     [pattern@company.com — confidence: H/M/L] [INFERRED]
Mutual connection: [Name + relationship if applicable]  [EXPLICIT / OPEN]
```

**Org Chart Reconstruction** [INFERRED]
- Map reporting lines from LinkedIn titles and tenure signals
- Identify recently promoted people (likely championing new initiatives)
- Flag who joined from a competitor (may bring vendor preferences with them)
- Note who is actively hiring under them (signals budget ownership)

> [EXPLICIT] Only use publicly available professional information. Do not infer personal
> details, home addresses, or non-professional social media content.

**Acceptance criteria (S3):** ≥1 Contact Card per the depth tier; every card has a verified title +
tenure, a best channel, and a likely-priority line; email pattern carries a confidence level; current
employment confirmed (see EC-7). [EXPLICIT]

---

## S4: Pain Point Hypothesis

Construct a hypothesis of what is hurting the target organization right now.
This drives message-market fit for the outreach or pitch. Produce 3–5 hypotheses. [EXPLICIT]

**Signal-to-Pain Mapping:**

| Signal Observed | Derived Pain Hypothesis |
|---|---|
| 15+ open engineering roles | Scaling pains, team capacity issues, delivery bottleneck |
| 3 CTOs in 24 months | Tech strategy instability, culture/direction tension |
| No data/analytics roles | Low data maturity, spreadsheet-heavy operations |
| Series B raised 12 months ago | Board pressure for growth metrics and unit economics |
| Recent compliance-related press | Regulatory risk, need for audit/governance tooling |
| Legacy tech stack in job postings | Migration need, tech debt, developer experience friction |
| Rapid expansion to new markets | Localization needs, operational complexity, compliance gaps |
| Re-posting the same role 3× | Retention problem or misaligned expectations |
| Competitor launched a feature they lack | Product gap, pressure to close the gap fast |
| Customer forum / G2 complaints visible | Support overload, churn risk, UX debt |

**Pain Point Hypothesis Format (produce per hypothesis):**
```
Hypothesis:    [Company X] likely struggles with [SPECIFIC PAIN]         [INFERRED]
Evidence:      [Signal 1: source] + [Signal 2: source]
Urgency:       [Why this pain is acute NOW vs. chronic background noise]  [INFERRED]
Our hook:      [How our offering maps to this specific pain]              [INFERRED]
Confidence:    High / Medium / Low
Validation Q:  [The one question to ask on the call to confirm or refute]
```

**Worked example (filled):**
```
Hypothesis:    Acme likely struggles to orchestrate its growing data pipeline   [INFERRED]
Evidence:      6 open data-engineer roles, all dbt+Snowflake, none Airflow (LinkedIn jobs)
               + Series B raised 12mo ago (Crunchbase) → board pressure on data-driven metrics
Urgency:       Acute NOW — postings went live this quarter; the gap blocks reporting they owe the board
Our hook:      We install orchestration in <30 days so dbt models run on schedule, not by cron hacks
Confidence:    Medium  (2 signals, but Airflow absence is an inference, not a stated need)
Validation Q:  "How are you scheduling and monitoring dbt runs across teams today?"
```

**Confidence definitions:** **High** = ≥2 Tier A/B signals point the same way and the pain maps to a
named role's KPI. **Medium** = ≥2 signals but at least one is inferred (Tier C/D). **Low** = single
signal or first-principles guess (use only in EC-1, no-footprint companies). Rank hypotheses by
confidence; lead the call with the highest. [INFERRED]

**Acceptance criteria (S4):** 3–5 hypotheses produced; each has ≥2 tagged signals, a validation
question, and a hook that maps to our offering; none presented as confirmed fact. [EXPLICIT]

**Pain Categories Checklist:**
- [ ] Revenue growth blocked (can't acquire, expand, or retain customers)
- [ ] Operational efficiency (manual work, slow processes, high headcount for low output)
- [ ] Technical debt (legacy stack slowing product velocity)
- [ ] Talent (can't hire, retain, or upskill fast enough)
- [ ] Compliance / risk (regulatory pressure, security gaps, audit failures)
- [ ] Data visibility (can't measure what matters, decisions made on gut)
- [ ] Customer experience (churn, NPS decline, support volume growing)

> [EXPLICIT] Pain hypotheses are hypotheses. They must be validated in the discovery call.
> Do not present them as confirmed facts in the dossier or in outreach messages.

---

## S5: Approach Strategy

Synthesize dossier findings into a concrete outreach and engagement plan. [INFERRED]

**Best Entry Angle Selection:**

| Context | Recommended Angle |
|---|---|
| Recent funding round | Congrats + growth/scale challenge framing, budget window open |
| New executive hire | Fresh start, new vendor evaluation cycle, open to change |
| Recent product launch | Integration opportunity, complementary capability |
| Cost pressure signal | ROI-first framing, fast time-to-value, efficiency story |
| Competitor win in their space | Urgency angle, competitive pressure, fear of falling behind |
| Award / milestone | Validation: "how do you maintain this standard at scale?" |
| Pain signal from job postings | Precision hook: "we saw your [X] postings, we solve that" |

**Personalization Layers (stack all four for highest conversion):**
1. **Company layer** — Reference specific company news, milestone, or challenge [EXPLICIT]
2. **Role layer** — Speak to their specific responsibilities and KPIs [INFERRED]
3. **Person layer** — Reference their public content, career moves, or interests [EXPLICIT]
4. **Timing layer** — Connect to a trigger event (funding, launch, Q1 planning cycle) [INFERRED]

**Channel Sequence Recommendation:**
1. LinkedIn connection request (no note, or short note referencing shared context)
2. LinkedIn message after connection (1 paragraph, specific hook, one clear ask)
3. Email follow-up 5 days later (reference the LinkedIn outreach, add new value element)
4. Warm intro via mutual connection if one exists (highest conversion, always preferred)

**Objection Pre-empts:**

| Common Objection | Pre-empt in the Message |
|---|---|
| "We already have a solution" | Acknowledge + differentiate on one specific dimension |
| "Not the right time / budget frozen" | Ask for a 15-min discovery, not a commitment |
| "Send me more info" | Offer a 1-pager tailored to their use case, not a generic deck |
| "We handle this internally" | Validate their approach, offer a benchmark/audit angle |
| "We're in evaluation mode already" | Ask to be included, offer a specific POV or framework |

**Opening Message Draft Formula:**
```
[Trigger event / personalization hook] + [specific pain we solve] +
[1 reference to a peer / analogous company] + [metric or outcome] + [single soft ask]
```

Example:
> "Saw your team posted 6 data engineer roles this quarter — teams scaling data infra
> at your stage usually hit the orchestration wall 60 days after the dbt rollout.
> We helped [Peer Company] cut pipeline failures by 70% in that window.
> Worth a 20-minute call to see if the pattern fits?"

**Acceptance criteria (S5):** One entry angle chosen with a stated reason; ≥2 personalization layers
stacked; a channel sequence; and an opening message naming a trigger event + the specific pain. A
generic opener ("I'd love to connect") fails this gate. [EXPLICIT]

---

## S6: HTML Dossier Output Template

Generate a branded, self-contained HTML dossier. Load full template from `references/html-template.md`. [EXPLICIT]

**Brand tokens**: `--navy: #122562` · `--gold: #FFD700` · `--blue: #137DC5` · dark bg `#0d0d0d` · Poppins headings + Inter body.

**Sections in the HTML output**: Header (company name + date + confidential badge) → TL;DR executive brief (3 bullets) → Company DNA (10-field data grid) → Key Contacts (2 contact cards) → Pain Hypotheses (3 items with confidence badges) → Approach Strategy (4-step numbered list) → Footer (JM Labs attribution).

**Delivery rules** [EXPLICIT]:
- Replace every `[placeholder]` with researched data
- Label inferred fields with `[est.]` inline
- Do not deliver with unfilled placeholders
- Mark `[INFERRED]` on estimated revenue / headcount / tech stack when source is indirect

---

## Trade-off Matrix

| Decision | Option A | Option B | Recommendation |
|---|---|---|---|
| Depth vs. speed | Full 6-section dossier (2-3h) | Quick 2-section brief (30min) | Full for strategic accounts; brief for same-day inbound |
| Public vs. inferred data | Only confirmed facts | Include reasoned inferences | Include inferences, tag clearly with [INFERRED] |
| HTML vs. markdown output | Branded HTML dossier | Plain markdown summary | HTML for client-facing; markdown for internal notes |
| Company vs. person focus | Company-first, then people | Person-first, then company | Company-first unless user specifies a named target |
| One contact vs. full map | Single decision-maker | Full stakeholder map | Full map for deals >$50K; single for fast outreach |
| Hypothesis depth | 1 primary pain | 3–5 ranked hypotheses | 3–5 always; more hypotheses = better discovery call prep |

---

## Assumptions & Limits

- [EXPLICIT] All research is based on publicly available information only. No paid databases,
  no data brokers, no private data inference beyond professional context.
- [INFERRED] Revenue and headcount figures for private companies are estimates. Every such
  figure is labeled `[est. — not verified]` in the output.
- [EXPLICIT] Email patterns are hypotheses, not confirmed addresses. User must validate before use.
- [OPEN] Tech stack inferences from job postings may lag reality by 6–12 months. Directional only.
- [EXPLICIT] This skill does not profile private individuals outside a professional or public-figure
  context. If a request concerns a private person, decline and explain the privacy concern.
- [INFERRED] Pain hypotheses are probabilistic. The validation question in each hypothesis is
  mandatory — do not treat as confirmed until the discovery call verifies it.
- [EXPLICIT] Dossier freshness degrades fast — refresh if >30 days old before any meeting.

---

## Edge Cases

**EC-1: Company with no digital footprint**
Very small or recently founded company has minimal LinkedIn presence, no press, minimal web.
Action: Build a lightweight dossier from whatever is available. Flag the confidence score as
low. Use industry + company size + founding year to construct pain hypotheses from first
principles (e.g., "at 20 employees in SaaS, the most common pain at 18 months is [X]").

**EC-2: Executive with a common name / ambiguous identity**
"John Smith at Acme" — multiple LinkedIn matches, ambiguous results.
Action: Ask user for LinkedIn URL or full title before proceeding. Do not produce a dossier on
the wrong person. Verify company + current title before writing any Contact Card.

**EC-3: Company in a language other than English**
Target is a Latin American or European company with minimal English-language presence.
Action: Research in the native language. Produce the dossier in the language the user requests.
Use `[data-l="es"]` / `[data-l="en"]` HTML markup throughout the output.

**EC-4: User wants a dossier on a competitor (not a prospect)**
Intent is competitive intelligence, not a sales dossier.
Action: Redirect to the competitive-intelligence skill. The dossier framework is optimized for
outreach and entry strategy, not competitive positioning — wrong tool for this use case.

**EC-5: Publicly traded company with overwhelming data volume**
10-K, earnings calls, IR page, analyst coverage — information overload.
Action: Prioritize recency (last 12 months) and strategic relevance (what affects this deal).
Summarize, do not dump. The dossier is a decision tool, not an archive. Cite specific
sections for the user to read if they want more depth.

**EC-6: Sources contradict each other**
LinkedIn, website, and a news article give three different headcounts or funding totals.
Action: Apply source-reliability tiers (S1). Report the higher-tier or fresher figure, tag it
`[est.]`, and add a one-line note on the conflict so the user is not blindsided on the call. Never
silently average or pick the flattering number. [EXPLICIT]

**EC-7: Target contact has left the company**
LinkedIn shows the decision-maker moved on, or the role is now vacant.
Action: Flag it prominently — outreach to a departed contact wastes the opening. Identify the
backfill or the next-most-senior person in that function, and note that a vacancy itself is a buying
signal (new hire = new vendor evaluation cycle). [INFERRED]

**EC-8: User asks you to find a personal email, phone, or home address**
Request crosses from professional OSINT into private data.
Action: Decline that element, explain the privacy/scope boundary, and offer the in-scope alternative
(LinkedIn, work-email pattern, warm intro). Deliver the rest of the dossier normally. [EXPLICIT]

---

## Failure Modes

The ways a dossier goes wrong, and the guardrail that catches each. [INFERRED]

| Failure mode | How it shows up | Guardrail |
|---|---|---|
| Wrong entity | Dossier on a homonym company/person | Verify name + domain + one unique attribute (founding year, HQ city) before writing |
| Confident fabrication | Estimated revenue presented as fact | Every private-co revenue/headcount carries `[est. — not verified]`; no exceptions |
| Stale data | Acting on a funding round or headcount >6 months old | Date-stamp every signal; refresh dossier if >30 days before a meeting |
| Encyclopedia, not tool | 5 pages of facts, no hook, no next action | Definition-of-done check: does it end in one specific ask? If not, it failed |
| Tag laundering | An `[OPEN]` guess written as `[EXPLICIT]` | One tag per claim, pick the weaker; spot-check 3 random `[EXPLICIT]` tags trace to a source |
| Privacy breach | Personal social, home, family data creeps in | Hard scope: public professional only; decline + explain if asked for more |
| Generic outreach | "I'd love to connect" with no personalization | Opening message must name ≥2 of: trigger event, specific pain, peer, metric |
| Over-research | 5h on a same-day inbound | Match depth tier to deadline; Flash when the call is <1h out |
| Single-source pain | Hypothesis rests on one weak signal | Require ≥2 tagged signals per primary hypothesis before presenting |

---

## Good vs. Bad Example

**BAD — Generic, no action value:**
> "Acme Corp is a technology company with around 500 employees. They seem to be growing
> and might be interested in our services. Their CEO is John Doe."

**GOOD — Specific, hypothesis-driven, actionable:**
> "Acme Corp (Series B, $42M raised Jan 2024 [EXPLICIT], 340 → 480 employees in 12 months
> [INFERRED via LinkedIn]) is scaling engineering faster than their data infrastructure
> can support. Evidence: 6 open data engineer roles in Q1 [EXPLICIT], all requiring dbt +
> Snowflake, none requiring Airflow — the orchestration gap [INFERRED]. Decision-maker:
> Maria Gómez, VP Engineering (joined 8 months ago from Stripe [EXPLICIT], previously built
> a data platform team from scratch [EXPLICIT via LinkedIn bio]). Hook: 'We saw your data
> engineer postings — teams at your stage typically hit the orchestration wall 60 days after
> the dbt rollout. We solved this for [Peer Company] and cut pipeline failures by 70%.
> Worth a 20-min call?' [INFERRED pain + EXPLICIT peer reference]."

The good version has: named signals with evidence tags, a specific gap, a named contact with
career context, a peer reference, a metric, and a specific one-ask close. Every element traces
to a real signal source.

---

## Validation Gate

Before delivering any dossier output, verify all of the following:

- [ ] Company name correctly spelled and verified — not a homonym or alias
- [ ] All revenue / headcount figures labeled `[est.]` if not from a public source
- [ ] At least 2 specific signals support the primary pain hypothesis
- [ ] Every named contact drawn from public professional sources only
- [ ] Email patterns labeled as `[INFERRED — not verified]`, not as confirmed addresses
- [ ] Tech stack claims trace to at least one concrete signal (job posting, website, press)
- [ ] Approach strategy includes a specific personalization hook, not a generic opener
- [ ] HTML output uses JM Labs brand tokens (navy `#122562`, gold `#FFD700`, blue `#137DC5`)
- [ ] Bilingual `[data-l]` attributes present on all user-facing strings in HTML output
- [ ] All `[placeholder]` tokens in HTML have been replaced with real researched data

---

## Reference Files

| File | Purpose |
|---|---|
| `knowledge/body-of-knowledge.md` | Sales intelligence and OSINT methodology |
| `knowledge/knowledge-graph.md` | Entity relationships for prospect research |
| `evals/` | Scored dossier examples for quality calibration |

---

## Related Skills

- `market-intelligence` — Broader market/sector context before the dossier
- `b2b-outreach` — Convert dossier findings into outreach sequences
- `client-prospecting` — Identify who to build dossiers for
- `competitive-intelligence` — Competitor profiles (different framework from prospect dossiers)
- `executive-pitch` — Use dossier findings to prepare a pitch narrative
- `stakeholder-mapping` — Internal org mapping when target is an existing client
