# Body of Knowledge — market-intel

Domain knowledge for the eight market/competitive-intelligence topics this
router covers. Concepts, standards, and decision rules — not procedure (that
lives in each `references/*.md` playbook).

## 1. Core concepts by topic

### Competitive intelligence
- **Feature matrix** — capabilities × competitors grid. Cell ∈ {Yes, No,
  Partial, Unknown}. `Unknown` is a tagged gap, never a silent `No`. [DOC]
- **SWOT** — each entry one tagged line; Opportunities/Threats must trace to a
  matrix row or a sourced claim, not free-form opinion. [DOC]
- **Differentiation** — a capability where we are `Yes` and ≥50% of the
  competitor set is `No`/`Partial`. Ranked by feasibility. [INFERENCIA]

### Competitive positioning
- **Competitor classes** — *direct* (same JTBD + buyer), *indirect* (different
  solution, same JTBD), *substitute* (status quo / build-it-yourself). Always
  include the status quo. [INFERENCIA]
- **Positioning statement** — _For [buyer] who [need], [product] is the
  [category] that [differentiator], unlike [alternative]._ [DOC]
- **Decision-criteria axes** — comparison axes must map to what the *buyer*
  weighs, not your feature list. Differentiation = differentiated ∧
  buyer-valued. [INFERENCIA]

### Benchmarking analysis
- **Normalization first** — same unit, period, segment, definition before any
  comparison. [EXPLICIT]
- **Gap** = subject − reference, reported absolute AND % of reference, with
  sign convention (higher- vs lower-is-better). [EXPLICIT]
- **Prioritization** — rank by impact × closability, not raw gap size. Prefer
  median/quartile to mean on skewed metrics. [EXPLICIT]

### Market intelligence (OSINT)
- **Entity classes** — company / person / territory / sector; each has distinct
  primary sources (LinkedIn/Crunchbase; press; World Bank/gov; Gartner/Statista).
- **TAM / SAM / SOM** — market size needs source + vintage year; a lone figure is
  `[INFERRED]`, never `[EXPLICIT]`. [EXPLICIT]
- **Momentum signals** — funding, hires, launches; every one carries an as-of
  date or becomes `[OPEN]`. [EXPLICIT]

### Sector intelligence
- **Sub-segment + jurisdiction** — "fintech → EU cross-border B2B payments", not
  "fintech". "Global" is not a jurisdiction. [DOC]
- **Regulatory matrix** — requirement, source, jurisdiction, deadline, tech
  impact; primary-sourced and point-in-time (it expires). [DOC]
- **Integration rails** — name real ones (SEPA Instant, FHIR), not "bank API". [DOC]

### Marketing context
- **One primary value prop** + 2 supporting; a benefit without a proof point is
  a `[SUPUESTO]`, not a benefit. [EXPLICIT]
- **Message hierarchy** — no competing primary claims. [EXPLICIT]

### Partnership strategy
- **Partner taxonomy** — referral/affiliate, co-marketing, technology/
  integration, reseller/channel, strategic/OEM; mechanics differ by type. [INFERENCE]
- **Fit score** — 5 axes (audience overlap 0.30, reach 0.20, strategic fit 0.20,
  effort 0.15, reputation 0.15); pursue ≥3.5, park 2.5–3.5, drop <2.5. [ASSUMPTION]
- **Kill criteria** — defined with the partner at launch; an undefined kill
  trigger is an open-ended cost. [INFERENCE]

### Pricing strategy
- **Levers** — anchor, decoy, value-based framing, feature fencing, tier count
  (3 default). [INFERENCIA]
- **Value metric** — must scale with customer success (seats, transactions), not
  with vendor cost. [INFERENCIA]
- **No concrete price** — recommend structure + ranges/placeholders; client sets
  the number. [DOC]

## 2. Standards & conventions

- **Evidence tagging** — one tag per claim; when two apply, pick the weaker.
  Families do not mix in one artifact. Alfa core: `[CÓDIGO] [CONFIG] [DOC]
  [INFERENCIA] [SUPUESTO]`. OSINT local (market-intelligence):
  `[EXPLICIT] [INFERRED] [OPEN]`. CI/benchmark local: `[EXPLICIT] [CODE]
  [CONFIG] [DOC] [INFERENCE] [ASSUMPTION]`. [DOC]
- **No invented prices** — FTE-months + disclaimers / ranges only (global hard
  rule). [CONFIG]
- **Single brand per artifact** — JM Labs tokens (navy `#122562`, gold
  `#FFD700`, blue `#137DC5`) for market-intelligence HTML; MetodologIA brand for
  others. Never blend. [CONFIG]
- **Public-source-only** — no breach dumps, no scrapers bypassing auth, no
  non-public PII; contact patterns are guesses to verify, not delivered. [EXPLICIT]
- **Point-in-time** — every deliverable is a snapshot; date-stamp it; regulatory
  and competitor facts decay. [DOC]

## 3. Decision rules

1. **Topic ambiguity** — ask one question only when two readings load different
   playbooks; otherwise proceed and state the chosen reading. [INFERENCIA]
2. **Depth** — `deep` runs the playbook's Validate step exhaustively; `quick`
   delivers essentials only. [CONFIG]
3. **Source confidence** — no source + no date ⇒ downgrade the tag. A claim that
   cannot be tagged is removed or converted to a question. [DOC]
4. **Anti-scope guard** — drift into pricing dollars / architecture / GTM /
   financial modeling ⇒ stop and re-route. [CONFIG]
5. **Threshold guards** — CI: >30% `[ASSUMPTION]` ⇒ WARNING banner. OSINT:
   `[OPEN]` items carry a resolution path. Benchmark: stale figure (older than
   metric cycle) flagged, not used silently. [DOC]
