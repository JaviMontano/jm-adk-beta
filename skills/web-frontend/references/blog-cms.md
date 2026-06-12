<!-- distilled from alfa skills/blog-cms -->
<!-- > -->
# Blog & CMS

> "Content is king, but distribution is queen — and she wears the pants." — Jonathan Perelman

## TL;DR

Guides implementation of blog/content features: Markdown/MDX rendering, category + tag taxonomies, full-text search, RSS/Atom feeds, SEO. Use for content-driven sites, developer blogs, lightweight CMS. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify content types (posts, pages, tutorials, changelog entries)
- Check content sources (Markdown files, headless CMS, database)
- Review authoring workflow (Git-based, admin panel, API)
- Determine search, filtering, and i18n requirements
- Estimate content volume — drives the pipeline decision in Step 2

### Step 2: Analyze
- Choose content pipeline (see Decision Matrix below)
- Plan taxonomy: categories as hierarchy (one per post), tags as flat labels (many per post)
- Design SEO URL structure (`/blog/[category]/[slug]`); decide canonical when a post lives under multiple tags — pick ONE canonical path, others `rel=canonical` to it
- Evaluate static generation (SSG) vs server rendering (SSR) per route

### Step 3: Execute
- Set up Markdown/MDX rendering with syntax highlighting (Shiki preferred — build-time, zero client JS; Prism if runtime highlighting needed)
- Implement category/tag pages with post counts and pagination
- Add full-text search (Algolia/Pagefind for SSG; Lunr.js for small static; Firestore needs an external index)
- Generate RSS/Atom feed + sitemap.xml at build time
- Add SEO meta, Open Graph, Twitter cards, JSON-LD `Article` schema
- Build reading-time estimate and table-of-contents generation

### Step 4: Validate
- Verify Markdown renders (headings, code, images, tables, embeds)
- Test search returns relevant results with typo tolerance
- Confirm RSS validates (W3C Feed Validator); assert absolute URLs in feed
- Check SEO via Lighthouse and social preview debuggers

## Decision Matrix — content pipeline

| Pipeline | Choose when | Trade-off [INFERENCIA] |
|----------|-------------|-------------------------|
| File-based MD/MDX | Devs author via Git; content volume low–medium; versioning desired | No live preview for non-devs; rebuild per publish |
| Headless CMS (Contentful, Sanity) | Non-technical authors; scheduled/draft workflows; >~100 posts | External dependency + cost; webhook→rebuild plumbing |
| Database (Firestore) | App already DB-backed; dynamic per-user content | Weak native full-text search; needs external search index |

Default for a developer blog: file-based MDX + SSG. [SUPUESTO]

## Acceptance Criteria

- [ ] Every content page has a unique meta title, description, and canonical URL
- [ ] Code blocks have syntax highlighting + copy-to-clipboard
- [ ] Pagination correct on category/tag archives (no orphan/duplicate posts across pages)
- [ ] RSS feed regenerates on publish and uses absolute URLs
- [ ] OG image present on every post (fallback to a generated default)
- [ ] Sitemap excludes draft/unpublished routes
- [ ] Build fails (not warns) on a post missing required frontmatter
- [ ] Evidence tags applied to all claims

## Worked Example — MDX post + SEO head

```mdx
---
title: "Shipping a Static Blog in 2026"
slug: shipping-static-blog
category: engineering
tags: [ssg, mdx, seo]
date: 2026-06-11
description: "How to build a fast, SEO-clean MDX blog."
ogImage: /og/shipping-static-blog.png
draft: false
---
Body in **MDX** with <CustomComponent /> support.
```

```html
<!-- emitted <head> -->
<title>Shipping a Static Blog in 2026</title>
<link rel="canonical" href="https://site.dev/blog/engineering/shipping-static-blog" />
<meta property="og:image" content="https://site.dev/og/shipping-static-blog.png" />
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article",
 "headline":"Shipping a Static Blog in 2026","datePublished":"2026-06-11"}
</script>
```

## Failure Modes

| Failure | Symptom | Fix [INFERENCIA] |
|---------|---------|------------------|
| Relative URLs in RSS/JSON-LD | Feed readers + crawlers 404; rich results rejected | Resolve every URL against an absolute `siteUrl` base |
| Drafts leak to prod | Unpublished posts indexed by Google | Filter `draft:true` in route generation AND sitemap |
| Slug collision | Two posts resolve same URL; one silently wins | Assert slug uniqueness at build; fail the build |
| Client-side MD render | Slow FCP, content invisible to crawlers | Render at build/SSR; ship HTML, not raw Markdown |
| Pagination off-by-one | Duplicate or missing post across pages | Stable sort key + total-count assertion in tests |
| Unsanitized MDX/HTML | XSS via author or imported content | Sanitize/allowlist; treat external content as untrusted |

## Anti-Patterns

- Rendering Markdown client-side when SSG is possible
- Database `LIKE` queries instead of a real search index
- Neglecting OG images (every post needs a social preview)
- Hand-maintaining sitemap/RSS instead of generating from source

## Anti-Scope

- Not a full editorial CMS (roles, approval chains, media DAM) — use a headless CMS
- No comment system, paywall, or auth — out of scope; integrate separately
- No translation/localization workflow beyond routing hooks [EXPLICIT]

## Related Skills

- `landing-pages` — post pages need the same performance/SEO attention
- `firebase-hosting` — deploying static blog content with CDN caching

## Usage

- "/blog-cms" — Run the full blog cms workflow
- "blog cms on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Search-provider choice assumes content is publicly indexable; gated content needs auth-aware indexing [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Post in multiple categories | Enforce one canonical category; surface others as tags |
| Renamed/deleted slug | Emit 301 redirect from old path; keep a redirect map |
| Future-dated post | Exclude from feed/sitemap until publish date passes |
| Very large archive (>1k posts) | Paginate + lazy-build; pre-warm search index at build |
