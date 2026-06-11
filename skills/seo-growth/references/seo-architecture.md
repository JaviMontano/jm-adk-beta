<!-- distilled from alfa skills/seo-architecture -->
<!-- > -->
# SEO Architecture

> "The best place to hide a dead body is page 2 of Google search results." — Anonymous

## TL;DR

Implements technical SEO architecture including structured data (JSON-LD), XML sitemaps, robots.txt, canonical URLs, Open Graph tags, and rendering strategies (SSR/SSG) for maximum search discoverability. Use this skill when building content-driven sites, fixing SEO issues, or establishing technical SEO standards. [EXPLICIT]

## Procedure

### Step 1: Discover
- Audit current SEO state: indexing status, search console errors, crawl budget
- Review page rendering strategy: CSR, SSR, SSG, ISR — and its SEO implications
- Check existing meta tags, structured data, and sitemap coverage
- Identify target keywords and content strategy alignment

### Step 2: Analyze
- Evaluate rendering strategy for SEO: SSR/SSG preferred for content pages
- Map URL structure: clean, hierarchical, keyword-relevant slugs
- Identify structured data opportunities per page type (Article, Product, FAQ, BreadcrumbList)
- Assess internal linking structure and crawl depth

### Step 3: Execute
- Implement meta tags: title, description, canonical, Open Graph, Twitter Cards
- Add structured data using JSON-LD for all applicable page types
- Generate XML sitemap with priority and lastmod for all indexable pages
- Configure robots.txt with proper allow/disallow and sitemap reference
- Implement hreflang for multi-language sites
- Set up SSR or SSG for content pages that need SEO indexing
- Configure proper 301 redirects for URL changes

### Step 4: Validate
- Test structured data with Google Rich Results Test
- Verify sitemap includes all indexable pages and excludes non-indexable ones
- Check canonical URLs resolve correctly and point to preferred versions
- Validate rendering with "View as Googlebot" in Search Console

## Quality Criteria

- [ ] Every page has unique title, description, and canonical URL
- [ ] Structured data validates without errors in Rich Results Test
- [ ] XML sitemap is auto-generated and submitted to Search Console
- [ ] Robots.txt correctly controls crawler access
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Client-side rendered content pages that Googlebot cannot index
- Duplicate content without canonical URL resolution
- Blocking important resources in robots.txt that crawlers need

## Related Skills

- `performance-architecture` — Core Web Vitals are a ranking factor
- `html-semantic` — semantic HTML supports SEO understanding
- `pwa-architecture` — SSR/prerendering for PWA SEO

## Usage

Example invocations:

- "/seo-architecture" — Run the full seo architecture workflow
- "seo architecture on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
