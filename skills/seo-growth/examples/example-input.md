# Example Input — seo-growth

A documentation site on Next.js migrated from `/docs/*` to `/guides/*` last month and
organic traffic to the docs dropped sharply. Pages are rendered client-side (CSR). The
team also notices several pages showing "Discovered – currently not indexed" in Search
Console, and the old `/docs/*` URLs return 200 (no redirects were added).

The request: *"Figure out why our docs traffic tanked after the URL move and tell me the
technical SEO fixes — rendering, redirects, and indexing. Apply it thoroughly."*

Context provided:
- Stack: Next.js, currently CSR for docs pages.
- Canonical host: both `https://acme.dev` and `https://www.acme.dev` resolve (no 301).
- Old URLs `/docs/getting-started` etc. still return 200 alongside new `/guides/getting-started`.
- No XML sitemap submitted; robots.txt currently blocks `/_next/`.
- depth: deep.

Expected routing: `topic = seo-architecture`, `depth = deep`. This is structure /
rendering / redirects / indexing — not on-page copy (`seo-content`) and not a
README/navigation audit (`indexability-validator`).
