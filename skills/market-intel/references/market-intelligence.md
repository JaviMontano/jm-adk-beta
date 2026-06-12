<!-- distilled from alfa skills/market-intelligence -->
<!-- > -->
# Market Intelligence — Deep Research with Evidence Architecture

> TL;DR: Full-spectrum market intelligence on any entity — company, person, territory, or sector — delivered as a branded JM Labs HTML report with evidence chips.

**Principio Rector:** Evidence over assumption. Every claim carries an evidence tag. No speculation presented as fact.

**Evidence taxonomy (this skill's local convention — do not swap for the kit-wide Alfa set):** `[EXPLICIT]` = stated by a primary source; `[INFERRED]` = derived from signals; `[OPEN]` = unknown, needs research. These three drive the S6 protocol, the HTML chip CSS classes (`.src.explicit/.inferred/.open`), and the Validation Gate. They are intentionally domain-specific to OSINT confidence and are NOT interchangeable with `[DOC]`/`[CONFIG]`/`[SUPUESTO]`. [EXPLICIT]

**Definition of done (one line):** entity classified → matching track(s) executed → every claim tagged → `[OPEN]` items carry a resolution path → branded bilingual HTML emitted with an evidence log → trade-off level declared and honored. [EXPLICIT]

---

## When to Activate

**Activate when:**
- User says "market intelligence", "market research", "geographic analysis", "sector analysis"
- User says "competitive landscape", "research X company", "profile on X person"
- User says "contact points for", "entry strategy for [market]", "who are the players in [sector]"
- User needs a structured evidence-backed report on a market, company, or public figure [EXPLICIT]

**Do NOT activate when (anti-scope, with the right tool):**
- Quick one-liner fact → `WebSearch` directly. Threshold: if one query answers it, do not spin up a report. [INFERRED]
- Internal company data the user already owns → `input-analysis` skill (this skill is for *external* OSINT). [EXPLICIT]
- Purely financial modeling (DCF, unit economics, pricing) → `cost-estimation` / `pricing-strategy`. [EXPLICIT]
- Deep single-account dossier with contacts → hand to `client-dossier`; this skill is the breadth pass, not the depth pass. [INFERRED]
- Target is a minor, or request needs non-public data → refuse (see Edge Cases + Assumptions). [EXPLICIT]

**Pre-flight (run before S1):** confirm real-time web access is available; if static-knowledge-only, declare the cutoff and downgrade every time-sensitive claim to `[OPEN]` rather than presenting stale facts as `[EXPLICIT]`. [EXPLICIT]

---

## S1 — Input Classification

Classify the target entity before starting research. This determines the research path and data sources. [EXPLICIT]

| Entity Type | Definition | Primary Sources |
|------------|-----------|----------------|
| **Company** | Legal entity, product or service org | LinkedIn, Crunchbase, official site, news |
| **Person** | Executive, politician, influencer, decision maker | LinkedIn, Twitter/X, press, company bios |
| **Territory** | City, region, country, metro area | Government data, chamber of commerce, World Bank |
| **Sector** | Industry vertical, market segment | Gartner, IBISWorld, Statista, trade associations |

**Classification Protocol:**
1. Parse user input for entity name and type [EXPLICIT]
2. If ambiguous (e.g., "Amazon" — company or territory?), ask one clarifying question [INFERRED]
3. If entity has multiple dimensions (e.g., a sector in a territory), run both tracks [INFERRED]
4. Log classification decision with rationale before proceeding [OPEN]

**Decision rule (no clarifying question needed when):** the user supplied a disambiguator (URL, ticker, country, role) — proceed and state the chosen reading. Ask only when two readings would change the data sources used. Trade-off: one extra question costs a round-trip but a wrong classification wastes the whole research budget — when in doubt, ask once. [INFERRED]

**Worked example:** input "research Stripe in Brazil" → classify as Company (Stripe) × Territory (Brazil), run tracks 2a + 2b, intersect findings in the Opportunity Map. Input "Stripe" alone → Company track only. [INFERRED]

**Edge:** entity does not exist / typo / zero web footprint → do not fabricate a profile; return `[OPEN]` with "entity not found in public sources, confirm spelling or provide a URL." [EXPLICIT]

---

## S2 — Research Framework

### 2a. Company Research Track

**Layer 1 — Company DNA**
- Full legal name, founding year, HQ location [EXPLICIT]
- Business model (B2B/B2C/B2B2C, product/service/platform) [INFERRED]
- Revenue signals (public data, funding rounds, employee count proxies) [INFERRED]
- Ownership structure (private, VC-backed, PE, public, family) [EXPLICIT]

**Layer 2 — Competitive Position**
- Direct competitors (same ICP, same solution category) [INFERRED]
- Indirect competitors (different approach, same problem) [INFERRED]
- Market share signals (web traffic, app store rankings, media coverage volume) [INFERRED]
- Differentiation claims (website messaging, PR positioning) [EXPLICIT]

**Layer 3 — Tech Ecosystem**
- Known tech stack (BuiltWith, job postings analysis, GitHub signals) [INFERRED]
- Integrations and partnerships declared publicly [EXPLICIT]
- AI/automation adoption signals [INFERRED]

**Layer 4 — Momentum Signals**
- Recent funding rounds (last 24 months) [EXPLICIT]
- Key hires and departures (LinkedIn signals) [INFERRED]
- Product launches, pivots, press releases [EXPLICIT]
- Customer wins, case studies, testimonials [EXPLICIT]

### 2b. Territory Research Track

**Demographics Layer**
- Population, age distribution, urbanization rate [EXPLICIT]
- Education levels, literacy, language landscape [EXPLICIT]
- Income distribution, middle class size, purchasing power parity [EXPLICIT]

**Economic Layer**
- GDP, GDP per capita, growth rate (last 3 years) [EXPLICIT]
- Key industries by GDP contribution [EXPLICIT]
- Unemployment rate, informal economy size [EXPLICIT]
- FDI attractiveness, ease of doing business ranking [EXPLICIT]

**Tech Ecosystem Layer**
- Internet penetration rate, mobile-first vs desktop [EXPLICIT]
- Startup ecosystem maturity (unicorns, accelerators, VCs) [INFERRED]
- Digital payment adoption (fintech penetration) [INFERRED]
- Government digitalization index [EXPLICIT]

**Regulatory Layer**
- Data protection laws (GDPR equivalent, LGPD, etc.) [EXPLICIT]
- Industry-specific regulations relevant to user's sector [INFERRED]
- Tax regime highlights for business entry [EXPLICIT]

### 2c. Sector Research Track

- Market size (TAM, SAM, SOM) with source and date [EXPLICIT]
- Growth rate (CAGR, last 5-year trend) [EXPLICIT]
- Key players and concentration (HHI proxy) [INFERRED]
- Technology disruption vectors in the sector [INFERRED]
- Buyer behavior patterns (procurement cycles, decision makers) [INFERRED]
- Regulatory tailwinds and headwinds [EXPLICIT]

**Track failure modes & guards** (apply across 2a/2b/2c):
- *Stale signal mistaken for current* — a funding round or headcount from 3 years ago read as "now". Guard: every momentum claim carries an as-of date; no date ⇒ `[OPEN]`. [EXPLICIT]
- *Single-source inflation* — one blog's TAM figure repeated as consensus. Guard: market-size claims need source + vintage year; a lone uncorroborated figure is `[INFERRED]`, never `[EXPLICIT]`. [EXPLICIT]
- *Namespace collision in headcount/traffic* — wrong same-name entity's metrics. Guard: pin the canonical URL/legal name in S1 before pulling any quantitative signal. [INFERRED]
- *Vendor-marketing as fact* — a company's own "leader" claim. Guard: self-positioning is `[EXPLICIT]` only as "claims X," never as verified market share. [EXPLICIT]

---

## S3 — Public Figure Profile

Use when entity type = Person (executive, politician, investor, influencer, SME). [EXPLICIT]

**Identity Map**
- Full name, current role and organization [EXPLICIT]
- Career trajectory (last 3 positions minimum) [EXPLICIT]
- Education credentials (university, field) [EXPLICIT]
- Geographic base and mobility signals [INFERRED]

**Social Presence**
- LinkedIn URL, connection count proxy, posting frequency [EXPLICIT]
- Twitter/X handle, follower count, engagement style [EXPLICIT]
- Public speaking: conferences, podcasts, panels [EXPLICIT]
- Published content: articles, whitepapers, books [EXPLICIT]

**Credibility Map**
- Professional recognition (awards, board memberships, advisory roles) [EXPLICIT]
- Media coverage volume and tone [INFERRED]
- Controversies or public criticism (if publicly documented) [EXPLICIT]
- Thought leadership topics (recurring themes in public statements) [INFERRED]

**Influence Map**
- Who follows/endorses them publicly [INFERRED]
- Organizational networks (alumni, industry groups) [INFERRED]
- Investment portfolio or board seats (if public) [EXPLICIT]

---

## S4 — Commercial Contact Points

Extract actionable contact intelligence from public sources only. [EXPLICIT]

**Email Pattern Detection**
- Infer corporate email pattern from known public emails [INFERRED]
- Common patterns: firstname@domain, f.lastname@domain, firstname.lastname@domain
- Never fabricate — mark as [INFERRED] with confidence level (High/Medium/Low)
- **Anti-scope:** do NOT use breach dumps, leaked credential indices, or scrapers that bypass auth — public-source-only is a hard governance limit (see Assumptions). A pattern is a *guess to verify by the user*, not a delivered address. [EXPLICIT]
- Confidence calibration: High = ≥2 confirmed public addresses share the pattern; Medium = 1 confirmed; Low = pattern assumed from domain conventions only. [INFERRED]

**LinkedIn Channel**
- Direct InMail eligibility (premium connection) [INFERRED]
- Mutual connections that could facilitate warm intro [INFERRED]
- Group memberships for indirect engagement [EXPLICIT]

**Direct Channels**
- Company contact forms, sales inquiry pages [EXPLICIT]
- Event attendance (upcoming conferences, webinars) [EXPLICIT]
- Press/PR contact (for media-adjacent outreach) [EXPLICIT]

**Gatekeeper Mapping**
- EA/PA names if publicly visible (LinkedIn, company site) [EXPLICIT]
- Receptionist/front-desk contacts for physical outreach [EXPLICIT]
- Junior team members who manage comms for decision makers [INFERRED]

---

## S5 — Output — Branded HTML Report

Generate a self-contained HTML file using JM Labs brand system. [EXPLICIT]

**Brand Tokens to Apply:**
```css
:root {
  --jml-navy:  #122562;
  --jml-gold:  #FFD700;
  --jml-blue:  #137DC5;
  --jml-bg:    #0d1b3e;
  --jml-surface: rgba(255,255,255,0.05);
  --font-head: 'Poppins', sans-serif;   /* 600-900 weight */
  --font-body: 'Inter', sans-serif;     /* 400-800 weight */
}
```

**HTML Structure:**
```
<div class="jml-doc">
  <header class="slide">   <!-- Hero with title, subtitle, date -->
  <section class="bridge"> <!-- Executive summary / key findings -->
  <section class="mv">     <!-- Main content sections (S1-S4 findings) -->
  <section class="ml">     <!-- Evidence log / sources -->
  <footer class="cta">     <!-- Next steps / recommended actions -->
</div>
```

**Evidence Chips Pattern:**
```html
<span class="src explicit">[EXPLICIT]</span>
<span class="src inferred">[INFERRED]</span>
<span class="src open">[OPEN]</span>
```

**Bilingual Support (ES/EN):**
```html
<span data-l="es">Inteligencia de Mercado</span>
<span data-l="en">Market Intelligence</span>
```
JavaScript toggle between `data-l="es"` and `data-l="en"` via `.gold` button.

**Report Sections:**
1. Executive Summary (key findings, 3-5 bullets)
2. Entity Profile (classification + core facts)
3. Market Position / Competitive Landscape
4. Contact Intelligence (S4 output)
5. Opportunity Map (where to engage, why, how)
6. Evidence Log (all sources with URLs and access date)
7. Recommended Next Steps

**Output acceptance criteria:** self-contained single `.html` (fonts via Google Fonts CDN, no other external CSS/JS); brand tokens applied verbatim; every chip class maps to a real S6 tag; ES/EN toggle flips all `data-l` nodes; evidence log rows each have URL + access date; passes the Validation Gate below. [EXPLICIT]

**Design decision — single self-contained file over a multi-asset bundle.** Trade-off: a single file is heavier and not cache-friendly, but it is portable (email/share without breakage) and has zero dependency on a server or asset path — the right call for a deliverable the client opens once. Use the Deep tier's `HTML + CSV` split only when the user needs the raw rows for their own tooling. [INFERRED]

**Failure modes:** (a) untoggled `data-l` node ⇒ mixed-language render — guard: toggle script selects by attribute, not by id. (b) chip with no backing tag in the evidence log ⇒ broken provenance — guard: chips are generated from tagged claims, never hand-typed. (c) CDN font blocked offline ⇒ fallback to the `sans-serif` stack already declared in the tokens. [INFERRED]

---

## S6 — Evidence Tagging Protocol

Apply evidence tags to **every factual claim** in all outputs. No exceptions. [EXPLICIT]

| Tag | Meaning | Usage Rule |
|----|--------|-----------|
| `[EXPLICIT]` | Directly stated by a primary source | Use for facts from official sites, filings, press releases |
| `[INFERRED]` | Derived logically from available signals | Use for estimates, pattern-based conclusions |
| `[OPEN]` | Unknown — requires further research | Use when data gap exists but matters to the user |

**Tagging Discipline:**
- Untagged claims are forbidden in MOAT-grade outputs [EXPLICIT]
- If a claim cannot be tagged, it must be removed or converted to a question [INFERRED]
- [OPEN] tags must include a note on how to resolve them [EXPLICIT]
- One tag per claim; when two could apply, pick the weaker (less-certain) one — an `[INFERRED]` dressed as `[EXPLICIT]` is the failure that erodes trust. [EXPLICIT]
- Do not tag the report's own structure, restated user input, or self-evident statements — over-tagging kills scannability. [INFERRED]

**Why a local 3-tag set (decision + trade-off):** OSINT confidence is the axis that matters here, so the file uses `[EXPLICIT]/[INFERRED]/[OPEN]` rather than the kit-wide Alfa set (`[DOC]/[CONFIG]/[SUPUESTO]`). Trade-off: it diverges from the kit canon, but the HTML chip classes, S6 table, and Validation Gate are all wired to these three names — renaming them would silently break the rendered report. Keep them. [EXPLICIT]

---

## Trade-off Matrix

| Dimension | Quick (1h) | Standard (4h) | Deep (8h+) |
|-----------|-----------|--------------|-----------|
| Source depth | Top 10 web results | 30+ sources, cross-validated | Full OSINT + database sweep |
| Person profile | LinkedIn + basic bio | + Social + media coverage | + Network map + influence score |
| Contact intel | Email pattern only | + LinkedIn + gatekeeper | + Event calendar + warm intro path |
| Output format | Markdown summary | Branded HTML report | HTML + CSV + exec briefing |
| Confidence level | Medium | High | Very High |

---

## Assumptions & Limits

- Public data only — no hacking, no social engineering, no dark web [EXPLICIT]
- Email patterns are inferred, never verified without testing [EXPLICIT]
- Territory data accuracy depends on recency of government data sources [INFERRED]
- Sector size figures (TAM/SAM/SOM) must cite source and vintage year [EXPLICIT]
- Person profiles respect privacy: only publicly available information [EXPLICIT]
- Real-time web search required for current signals; static knowledge has cutoff [EXPLICIT]

---

## Edge Cases

| Scenario | Handling |
|----------|---------|
| Entity has same name as another (e.g., "Amazon" river vs. company) | Clarify with one question before starting; log disambiguation decision |
| Company is stealth / pre-launch with minimal public presence | Flag as [OPEN], deliver what exists, list data gaps explicitly |
| Public figure has scrubbed their online presence | Document what was found, note the scrubbing as signal, do not speculate |
| Territory has unreliable government data (conflict zone, sanctions) | Use World Bank / IMF as primary; flag reliability concern |
| User requests information on a minor (person under 18) | Refuse the person profile; redirect to the organization they're associated with |
| Sources conflict (two figures for the same fact) | Present both with sources, tag the synthesis `[INFERRED]`, never silently pick one |
| User pushes for private data (home address, personal phone, non-public email) | Refuse the private item, deliver the public-channel equivalent, cite the governance limit |
| Multi-dimensional target but budget is Quick tier | Pick the dimension with highest decision-value, declare the deferral, list the skipped track as `[OPEN]` |
| Target is a direct competitor of the user's own firm | Proceed (public OSINT is fair); flag any claim that would imply non-public knowledge and drop it |

---

## Good vs Bad Example

**BAD (untagged, vague):**
> "Company X is growing fast and has about 500 employees. They use Salesforce."

**GOOD (tagged, sourced, specific):**
> "Company X had 487 employees as of Q3 2024 per LinkedIn headcount [EXPLICIT]. Revenue estimated at $40-60M based on Series B raise of $15M (2023) and SaaS multiples [INFERRED]. Salesforce usage confirmed via BuiltWith scan [EXPLICIT]. Hiring 12 open roles in Engineering as of research date [EXPLICIT]."

---

## Validation Gate

- [ ] Entity type classified (company/person/territory/sector) with rationale
- [ ] Research framework section(s) executed matching entity type
- [ ] All factual claims carry evidence tags ([EXPLICIT] / [INFERRED] / [OPEN])
- [ ] [OPEN] items include resolution path
- [ ] Contact intelligence section completed (even if partial)
- [ ] HTML report uses JM Labs brand tokens (navy `#122562`, gold `#FFD700`, blue `#137DC5`)
- [ ] HTML report is self-contained (fonts via Google Fonts CDN, no external CSS dependencies)
- [ ] Bilingual ES/EN toggle implemented in HTML output
- [ ] Evidence log section present with source URLs and access dates
- [ ] Trade-off level declared (Quick / Standard / Deep) and scope honored

---

## Reference Files

- `knowledge/body-of-knowledge.md` — Market research methodology foundations
- `knowledge/knowledge-graph.md` — Entity relationship map for research paths
- `references/research-framework.md` — OSINT sources, B2B databases, signal detection methods
- `evals/` — Test cases with known entities for validation

---

## Related Skills

- `client-dossier` — Deeper company + contacts dossier (next step after market-intelligence)
- `client-prospecting` — Systematic lead generation using market intelligence output
- `b2b-outreach` — Convert contact intelligence into outreach sequences
- `competitive-positioning` — Strategic positioning informed by competitive landscape research
