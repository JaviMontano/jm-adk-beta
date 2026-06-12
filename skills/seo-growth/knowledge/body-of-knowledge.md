# seo-growth — Body of Knowledge

Domain knowledge for the `seo-growth` router: technical SEO, content SEO, indexability,
landing pages, CRO, funnel design, and social proof. Every claim is evidence-tagged with
the Alfa core set. [DOC]

## 1. The router model

`seo-growth` resolves one `topic` (eight enums) and reads exactly one playbook. Topics
fall into four families: **technical** (`seo-architecture`, `indexability-validator`),
**content** (`seo-content`), **page/funnel** (`landing-page-builder`, `landing-pages`,
`funnel-design`), and **trust/CRO** (`conversion-optimization`, `social-proof`). The
spine is always Discover → Analyze → Execute → Validate, and Validate is never skipped. [DOC]

## 2. Technical SEO — rendering & indexing

**Rendering decision table.** [INFERENCE]

| Page type | Strategy | Rationale |
|---|---|---|
| Stable marketing/docs/blog | SSG | Fastest, cacheable, bot-friendly |
| Frequently-changing catalog/listings | ISR | Static speed + periodic revalidation |
| Personalized/auth'd, low SEO value | CSR | No SEO need; never for indexable content |
| Real-time, must-index | SSR | Fresh + crawlable; higher server cost |

**Indexing rules.** One canonical host (www vs apex, http vs https) enforced via 301.
Every indexable page reachable in ≤3 clicks from home. Sitemap lists only canonical,
200-status, indexable URLs — never redirected, noindex, or non-canonical URLs. robots.txt
must allow CSS/JS (blocking them de-ranks). `noindex` + `canonical` on the same URL is a
conflicting signal. Chained/looping redirects bleed crawl budget. [DOC]

**Structured data.** Match schema.org type to page intent: Article, Product, FAQPage,
BreadcrumbList, Organization. JSON-LD `headline` must match the visible `<h1>`; dates must
be real emitted ISO-8601 values, not build placeholders. Validate via Rich Results Test,
zero errors. [DOC]

## 3. Content SEO — on-page

- One primary keyword + 2–3 secondary per page; reject cannibalization (two pages chasing
  one primary). [EXPLICIT]
- Title ≤60 chars, primary keyword front-loaded; description 140–160 chars, action-oriented,
  primary keyword once; both unique site-wide. [EXPLICIT]
- OG tags (`og:title/description/image/type/url`, image 1200×630) + Twitter
  `summary_large_image`. [EXPLICIT]
- Exactly one `<h1>` carrying the primary keyword; no skipped heading levels;
  descriptive internal anchor text (never "click here"). [EXPLICIT]
- Prefer the minimal schema that earns the rich result over exhaustive markup
  (Constitution XIII Think First, XIV Simple First). [EXPLICIT]
- Keyword *research* is out of scope — a target keyword set is assumed supplied. [EXPLICIT]

## 4. Indexability (Constitution XVIII)

Every directory MUST have a `README.md`. Classify each into exactly one bucket by priority:
**Missing README > Orphan > Stale > Complete**. Score = `complete / total scanned`.
Exit signal: score ≥ 95% **and** zero orphans → G3-ready. Orphans are held at 0 regardless
of score (a broken navigation edge is not a rounding gap). Stale (>30 days) is advisory,
never auto-fails. Stub READMEs are generated only where none exists, idempotently, dry-run
by default. [EXPLICIT]

## 5. CRO — friction, trust, testing

**Friction taxonomy.** cognitive (unclear value/next step) · effort (form length, steps,
load) · trust (risk, credibility, ambiguity). [EXPLICIT]

**Prioritization.** ICE = Impact × Confidence × Ease (1–5 each); act on the top item only. [EXPLICIT]

**Trust-gap → signal map.** social proof (testimonials/logos) · risk reversal
(guarantees/returns) · safety (security badges/HTTPS) · credibility (specificity/numbers). [EXPLICIT]

**Test discipline.** One hypothesis ("Because [evidence], changing [element] will
[direction] [metric] for [segment]"), one variable per arm. Pre-register primary metric,
MDE, sample size/arm, and stop date *before* launch. Read results only at the registered
sample and after ≥1 full business cycle (~2 weeks). A flat/negative result is a kept
learning. Never report a lift below the pre-registered sample. [EXPLICIT]

## 6. Funnel design (pre-launch)

**Stages & intent altitude.** TOFU = attention (subscribe/read) · MOFU = consideration
(compare/demo) · BOFU = commitment (trial/buy/call). CTA must match its stage. [EXPLICIT]

**Lead scoring.** Three axes — fit (firmographic), intent (declared need), engagement
(behavior). Map to lifecycle states (cold → engaged → MQL → SQL → sales-ready) each with a
numeric threshold and entry condition. Negative scoring is explicit (competitors,
job-seekers, students, free-mail B2B lose points). [EXPLICIT]

**Nurture flow.** Triggers, delays, branch conditions, messages, exit criteria. Every path
must terminate: convert, recycle, or suppress. Honor a global frequency cap + cross-flow
suppression list. Handoff must be deterministic: SLA + routing + fallback owner. [EXPLICIT]

## 7. Decision rules (cross-topic)

1. One topic, one playbook. Spanning 2+ topics or ambiguity → ask once. [DOC]
2. Default `quick`; choose `deep` for exhaustive application with per-step verification. [DOC]
3. Script-first: prefer a deterministic script over manual steps. [DOC]
4. Markup/design correctness ≠ guaranteed ranking or conversion — search engines and real
   traffic decide. Tag outcome claims accordingly. [SUPUESTO]
5. Never fabricate metrics, traffic, or baselines; mark the gap and name its source. [EXPLICIT]

## 8. Anti-scope (route elsewhere)

Keyword research, link-building/off-page, paid search → marketing/keyword skills.
Post-launch drop-off diagnosis → `funnel-analytics`. Legal/privacy review of email/consent
(GDPR/CAN-SPAM/CASL) → out of scope. [EXPLICIT]
