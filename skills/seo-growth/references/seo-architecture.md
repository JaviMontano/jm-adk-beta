<!-- distilled from alfa skills/seo-architecture -->
<!-- > -->
# SEO Architecture

> "The best place to hide a dead body is page 2 of Google search results." — Anonymous

## TL;DR

Implements technical SEO architecture: structured data (JSON-LD), XML sitemaps, robots.txt, canonical URLs, Open Graph/Twitter tags, and rendering strategy (SSR/SSG/ISR) for search discoverability. Use when building content-driven sites, fixing indexing issues, or setting technical SEO standards. [EXPLICIT]

**In scope:** crawlability, indexability, structured data, rendering-for-bots, canonicalization, redirects, hreflang.
**Anti-scope (out):** keyword research and content writing, link-building/off-page, paid search, copy tone, brand voice. Redirect those to content/marketing skills. [SUPUESTO]

## Procedure

### Step 1: Discover
- Audit indexing: coverage report, excluded/error pages, crawl-budget waste (Search Console).
- Identify current rendering mode (CSR/SSR/SSG/ISR) and its SEO impact.
- Inventory existing meta tags, structured data, sitemap and robots.txt coverage.
- Confirm canonical host (www vs apex, http vs https) is singular. [INFERENCIA]

### Step 2: Analyze
- Pick rendering per page type (decision table below); content pages must serve full HTML to bots. [INFERENCIA]
- Map URL structure: lowercase, hyphenated, hierarchical, stable, no query-string-only routing. [DOC]
- Match structured-data type to page intent (Article, Product, FAQPage, BreadcrumbList, Organization).
- Assess crawl depth: every indexable page reachable in ≤3 clicks from home. [SUPUESTO]

### Step 3: Execute
- Meta per page: unique `<title>` (≤60 chars), `description` (≤155), `canonical`, OG, Twitter Card. [DOC]
- Add JSON-LD for each applicable page type (example below).
- Generate XML sitemap with `lastmod`; omit `priority`/`changefreq` (Google ignores them). [DOC]
- robots.txt: allow crawl of CSS/JS, disallow only true non-index paths, reference sitemap.
- hreflang for multi-language; every alternate must link back reciprocally + include self. [DOC]
- 301 (permanent) for moved URLs; 302 only for genuinely temporary moves. [INFERENCIA]

### Step 4: Validate
- Structured data → Rich Results Test, zero errors. [DOC]
- Sitemap includes only canonical, 200-status, indexable URLs (no redirects/noindex/404).
- Each canonical is self-referential or points to a live 200 preferred URL.
- URL Inspection → "rendered HTML" contains the primary content and links. [DOC]

## Rendering decision (trade-offs)

| Page type | Strategy | Why / cost |
|---|---|---|
| Marketing, docs, blog (stable) | SSG | Fastest, cacheable, best for bots; rebuild on content change. [INFERENCIA] |
| Catalog/listings (frequent change) | ISR | Static speed + periodic revalidation; risk of brief staleness. [SUPUESTO] |
| Personalized/auth'd, low SEO value | CSR | No SEO need; never use for indexable content. [INFERENCIA] |
| Real-time, must-index | SSR | Fresh + crawlable; higher server cost/latency. [INFERENCIA] |

Default to SSG/ISR for indexable content; reserve SSR for freshness needs; CSR only behind auth. [SUPUESTO]

## Worked example — Article JSON-LD

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Page title, ≤110 chars",
  "datePublished": "2026-01-15T08:00:00Z",
  "dateModified": "2026-02-01T10:30:00Z",
  "author": { "@type": "Person", "name": "Author Name" },
  "publisher": {
    "@type": "Organization",
    "name": "Brand",
    "logo": { "@type": "ImageObject", "url": "https://site/logo.png" }
  },
  "mainEntityOfPage": "https://site/article-slug"
}
```
`headline` must match the visible `<h1>`/title; `datePublished` must be a real
emitted date, not a build placeholder. [DOC]

## Quality Criteria (acceptance)

- [ ] Every indexable page: unique title, description, self-referential canonical. [DOC]
- [ ] Structured data validates with zero errors in Rich Results Test.
- [ ] XML sitemap auto-generated, only canonical 200 URLs, submitted to Search Console.
- [ ] robots.txt allows CSS/JS, blocks only non-index paths, links sitemap.
- [ ] One canonical host enforced via 301 (www/apex + https decided and redirected).
- [ ] Bot-rendered HTML contains primary content (verified via URL Inspection).
- [ ] Evidence tags applied to all non-obvious claims.

## Anti-Patterns

- CSR-only content pages whose primary text/links never reach Googlebot's rendered HTML.
- Duplicate content across URLs without canonical resolution (params, trailing slash, www).
- Blocking CSS/JS in robots.txt — bot renders a broken page and may de-rank. [DOC]
- `noindex` left on after launch, or `noindex` + `canonical` on the same URL (conflicting signals). [INFERENCIA]
- Sitemap listing redirected, noindex, or non-canonical URLs.
- Chained/looping redirects (301 → 301 → 200) that bleed crawl budget and link equity. [INFERENCIA]

## Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Pages "Discovered, not indexed" | Thin/duplicate or crawl-budget waste | Canonicalize, prune low-value URLs. [SUPUESTO] |
| Rich result not showing | JSON-LD invalid or mismatched visible content | Re-validate; align markup to on-page data. [INFERENCIA] |
| Traffic drop after migration | Redirects missing/wrong (302 vs 301) | Map old→new with 301; resubmit sitemap. [INFERENCIA] |
| Wrong page ranks for query | Internal duplicate; canonical points elsewhere | Fix canonical + internal link targets. [SUPUESTO] |
| Foreign-language page wrong locale | hreflang non-reciprocal or missing self-ref | Add reciprocal + self hreflang. [DOC] |

## Related Skills

- `performance-architecture` — Core Web Vitals are a ranking factor. [DOC]
- `html-semantic` — semantic HTML supports SEO understanding.
- `pwa-architecture` — SSR/prerendering for PWA SEO.

## Usage

Example invocations:

- "/seo-architecture" — Run the full seo architecture workflow
- "seo architecture on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]
- Covers on-page/technical SEO only; ranking outcomes also depend on content quality and off-page factors outside this skill's control. [SUPUESTO]
- Search-engine behavior (Google) is the reference; Bing/others may differ on directives like `priority`. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| SPA with no SSR available | Recommend prerendering/dynamic rendering; flag indexing risk. [SUPUESTO] |
| Staging/preview env | Enforce `noindex` + robots block; never let it get indexed. [DOC] |
| Faceted/filter URLs explode crawl budget | Canonical to base + selectively `noindex`/disallow. [INFERENCIA] |
