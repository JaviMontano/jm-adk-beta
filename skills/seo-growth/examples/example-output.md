# Example Output — seo-growth → seo-architecture (deep)

## 1. Route resolution
- **Resolved topic:** `seo-architecture`
- **Depth:** deep
- **Playbook read:** references/seo-architecture.md (exactly one) [DOC]
- **Why this topic:** request is about rendering, redirects, canonical host, and indexing
  after a URL migration — technical SEO, not on-page copy or a README audit. [INFERENCE]

## 2. Discover
- Goal: recover organic docs traffic lost after `/docs/*` → `/guides/*` move.
- Rendering: docs pages are **CSR** — primary content may not reach Googlebot's rendered
  HTML, a likely root cause of "Discovered – not indexed." [INFERENCE]
- Canonical host: both apex and `www` resolve with no 301 → duplicate-host signal. [DOC]
- Old `/docs/*` URLs return 200 with no redirect → link equity stranded, duplicate content. [DOC]
- No sitemap; robots.txt blocks `/_next/` → blocks the JS bundle the CSR pages need to render. [DOC]
- Baseline: pre-move organic sessions = GAP — pull from Search Console "Pages" report
  (16-month window) before claiming a recovery figure. [SUPUESTO]

## 3. Analyze
| Decision point | Choice | Rationale | Tag |
|---|---|---|---|
| Rendering for docs | SSG (or ISR) | Stable docs; serve full HTML to bots; CSR-only must-index content is wrong | [INFERENCE] |
| Old→new URLs | 301 permanent | Move is permanent; 301 transfers equity, 302 would not | [INFERENCE] |
| Canonical host | Pick `https://acme.dev`, 301 `www`→apex | One singular canonical host required | [DOC] |
| robots.txt | Unblock `/_next/` | Blocking JS makes the bot render a broken page | [DOC] |

## 4. Execute
```text
1. Rendering: convert /guides/* to SSG (getStaticProps/Paths) so bot-rendered HTML
   contains the primary content and internal links.
2. Redirects: add 301 map /docs/:slug -> /guides/:slug (no chains, single hop -> 200).
3. Canonical host: enforce https://acme.dev; 301 https://www.acme.dev/* -> https://acme.dev/*.
   Self-referential <link rel="canonical"> on every /guides/* page.
4. robots.txt:
     User-agent: *
     Allow: /_next/
     Disallow: /admin/
     Sitemap: https://acme.dev/sitemap.xml
5. Sitemap: generate sitemap.xml with <lastmod>; only canonical 200 /guides/* URLs
   (exclude old /docs/*, noindex, redirected). Submit in Search Console.
6. JSON-LD: add TechArticle/Article per guide; headline must match visible <h1>;
   datePublished/dateModified as real ISO-8601 values.
```

## 5. Validate
| Quality criterion | Result | Evidence |
|---|---|---|
| Bot-rendered HTML contains primary content | pass | URL Inspection on `/guides/getting-started` shows full text + links after SSG |
| Structured data zero errors | pass | Rich Results Test on a sample guide |
| One canonical host via 301 | pass | `www`→apex returns 301; canonical self-references apex |
| Sitemap only canonical 200 URLs | pass | No `/docs/*`, noindex, or redirected URLs listed |
| robots.txt allows CSS/JS, links sitemap | pass | `/_next/` allowed; `Sitemap:` line present |
| No `noindex`+`canonical` conflict | pass | Guides carry canonical, no `noindex` |

## 6. Gaps, risks & next step
- Gap: pre-move traffic baseline — instrument via Search Console before reporting recovery. [SUPUESTO]
- Risk: redirect chains if any `/docs/*` already pointed elsewhere — verify single-hop. [INFERENCE]
- Next step: once indexed, route on-page title/description optimization to `seo-content`.

## 7. Governance footer
- Alfa core evidence tags, single family. Constitution v6.0.0. No prices · no PII · single brand. [DOC]
