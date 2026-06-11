<!-- distilled from alfa skills/blog-cms -->
<!-- > -->
# Blog & CMS

> "Content is king, but distribution is queen — and she wears the pants." — Jonathan Perelman

## TL;DR

Guides the implementation of blog and content management features — Markdown/MDX rendering, category and tag taxonomies, full-text search, RSS feeds, and SEO optimization. Use when building content-driven websites, developer blogs, or lightweight CMS solutions. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify content types (posts, pages, tutorials, changelog entries)
- Check existing content sources (Markdown files, headless CMS, database)
- Review content authoring workflow (Git-based, admin panel, API)
- Determine search and filtering requirements

### Step 2: Analyze
- Choose content pipeline: file-based MDX, headless CMS (Contentful, Sanity), or Firestore
- Plan taxonomy structure (categories as hierarchy, tags as flat labels)
- Design URL structure for SEO (`/blog/[category]/[slug]`)
- Evaluate static generation vs server rendering for content pages

### Step 3: Execute
- Set up Markdown/MDX rendering with syntax highlighting (Shiki, Prism)
- Implement category and tag pages with post counts and pagination
- Add full-text search (Algolia, Lunr.js, or Firestore full-text workaround)
- Generate RSS/Atom feed and sitemap.xml automatically
- Add SEO meta tags, Open Graph, Twitter cards, and JSON-LD Article schema
- Build reading time estimation and table of contents generation

### Step 4: Validate
- Verify Markdown renders correctly (headings, code blocks, images, tables)
- Test search returns relevant results with typo tolerance
- Confirm RSS feed validates with W3C Feed Validator
- Check SEO with Lighthouse and social media preview debuggers

## Quality Criteria

- [ ] All content pages have unique meta titles, descriptions, and canonical URLs
- [ ] Code blocks have syntax highlighting and copy-to-clipboard functionality
- [ ] Pagination works correctly on category/tag archive pages
- [ ] RSS feed auto-updates when new content is published
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Rendering Markdown client-side when static generation is possible
- Using database queries for search instead of a proper search index
- Neglecting Open Graph images (every post should have a social preview)

## Related Skills

- `landing-pages` — blog post pages need the same performance and SEO attention
- `firebase-hosting` — deploying static blog content with CDN caching

## Usage

Example invocations:

- "/blog-cms" — Run the full blog cms workflow
- "blog cms on this project" — Apply to current context


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
