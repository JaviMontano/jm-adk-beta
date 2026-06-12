<!-- distilled from alfa skills/seo-content -->
<!-- > -->
# Seo Content

> "Method over hacks. Evidence over assumption."

## TL;DR

Generates content-level SEO assets: meta titles/descriptions, Open Graph + Twitter Card tags, JSON-LD structured data for rich snippets, keyword-driven content structure (heading hierarchy, internal links), and XML sitemap entries. Complements `seo-architecture` (technical/rendering SEO) — this skill owns what users and crawlers *read*, not how pages render. [EXPLICIT]

## Anti-Scope

- Rendering strategy (SSR/SSG/ISR), robots.txt, canonical infra, crawl-budget tuning → `seo-architecture`. [EXPLICIT]
- Keyword *research* (volume, difficulty, intent discovery) — assumes a target keyword set is supplied; this skill applies them, it does not source them. [EXPLICIT]
- Paid/SEM copy, A/B conversion testing → `conversion-optimization`. [EXPLICIT]

## Procedure

### Step 1: Discover
- Inventory existing pages and their type (Article, Product, FAQ, LandingPage, Collection) — type drives which structured-data schema applies. [EXPLICIT]
- Pull current `<title>`, meta description, OG/Twitter tags, and any JSON-LD; record gaps and duplicates. Duplicate titles/descriptions are the most common ranking leak. [INFERENCIA]
- Confirm the target keyword set and primary intent per page (informational / transactional / navigational). [EXPLICIT]

### Step 2: Analyze
- Map one primary keyword + 2-3 secondary per page; reject keyword cannibalization (two pages chasing the same primary). [EXPLICIT]
- Select schema.org type per page; validate required vs. recommended properties before drafting. [EXPLICIT]
- Plan heading hierarchy: exactly one `<h1>` carrying the primary keyword, `<h2>/<h3>` for secondary terms and answerable sub-questions. [EXPLICIT]
- Constitution principles XIII (Think First) and XIV (Simple First): prefer the minimal schema that earns the rich result over exhaustive markup. [EXPLICIT]

### Step 3: Execute
- Title: ≤60 chars, primary keyword front-loaded, brand suffix optional. Description: 140-160 chars, action-oriented, includes primary keyword once. [EXPLICIT]
- OG tags: `og:title`, `og:description`, `og:image` (1200×630), `og:type`, `og:url`; Twitter: `twitter:card=summary_large_image` + image. [EXPLICIT]
- JSON-LD: emit valid schema for the page type; one `@graph` per page; absolute URLs; dates in ISO 8601. [EXPLICIT]
- Content: front-load the answer (featured-snippet target), keep keyword density natural (~1-2%, never stuffed), add descriptive internal anchor text (not "click here"). [INFERENCIA]
- Sitemap: add/update entry with `lastmod`; exclude noindex, redirected, and canonicalized-away URLs. [EXPLICIT]
- Apply evidence tags to every claim; render via brand template if output is HTML. [EXPLICIT]

### Step 4: Validate
- Structured data passes Google Rich Results Test (or schema.org validator) with zero errors. [EXPLICIT]
- Title/description within length limits and unique across the site. [EXPLICIT]
- OG image resolves at a public absolute URL and meets 1200×630 minimum. [EXPLICIT]
- Exactly one `<h1>`; heading levels are not skipped. [EXPLICIT]
- All evidence tags applied; output is Constitution-compliant. [EXPLICIT]

## Worked Example — Article page

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Reduce Crawl Budget Waste",
  "datePublished": "2026-06-11",
  "dateModified": "2026-06-11",
  "author": {"@type": "Organization", "name": "Acme"},
  "image": "https://acme.example/og/crawl-budget.png",
  "mainEntityOfPage": "https://acme.example/blog/crawl-budget"
}
```

```html
<title>Reduce Crawl Budget Waste — Acme</title>
<meta name="description" content="Cut crawl-budget waste with five concrete fixes: noindex thin pages, fix redirect chains, and prune duplicate URLs. A practical checklist.">
<meta property="og:image" content="https://acme.example/og/crawl-budget.png">
<meta name="twitter:card" content="summary_large_image">
```

## Quality Criteria

- [ ] Structured data validates with zero errors for the declared page type
- [ ] Title ≤60 chars, description 140-160 chars, both unique site-wide
- [ ] OG/Twitter tags complete; image absolute URL, ≥1200×630
- [ ] One `<h1>`; no skipped heading levels; primary keyword in `<h1>` + title + description
- [ ] Sitemap entry present with current `lastmod`; no noindex/canonicalized URLs included
- [ ] Evidence tags applied to all claims; Constitution-compliant

## Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Rich result not showing | Invalid/incomplete JSON-LD, or page noindexed | Re-validate schema; confirm indexability via `indexability-validator` |
| Two pages compete for one term | Keyword cannibalization | Consolidate or differentiate primary keyword per page |
| Social share shows wrong/no image | Missing/relative `og:image` or wrong dimensions | Use absolute URL, 1200×630, re-scrape via platform debugger |
| Truncated SERP snippet | Title/description over length | Trim to limits, front-load keyword |

## Related Skills

- `seo-architecture` — Technical SEO foundation
- `html-semantic` — Semantic HTML for SEO
- `google-analytics` — Track SEO performance
- `indexability-validator` — Confirm pages are crawlable/indexable before optimizing content

## Usage

Example invocations:

- "/seo-content" — Run the full seo content workflow
- "seo content on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and a supplied target keyword set [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Markup correctness ≠ guaranteed ranking/rich result; search engines decide eligibility [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No keyword set supplied | Flag as blocking; do not invent keywords — defer to keyword research |
| Page type ambiguous | Default to no structured data over wrong-type schema; confirm with author |
