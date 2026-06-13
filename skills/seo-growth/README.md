# seo-growth — Skill Overview

`seo-growth` is a **router skill** for SEO and conversion growth work. It resolves one
`topic` from the request, reads exactly one playbook, and produces that playbook's
deliverable under the Discover → Analyze → Execute → Validate spine. It never loads
the whole cluster — one topic, one file. [DOC]

## What it does

Covers eight tightly-scoped growth domains, split into technical SEO, content SEO,
page/funnel building, and trust/CRO:

| Topic | What it owns | Playbook |
|---|---|---|
| `seo-architecture` | Crawlability, rendering (SSR/SSG/ISR), structured data, canonicals, sitemap/robots, hreflang, redirects | `references/seo-architecture.md` |
| `seo-content` | Meta titles/descriptions, OG/Twitter, JSON-LD, heading hierarchy, keyword application | `references/seo-content.md` |
| `indexability-validator` | README-presence + navigation-chain audit (Constitution XVIII), indexability score | `references/indexability-validator.md` |
| `landing-page-builder` | Build a new high-conversion page end-to-end (hero→CTA→footer), SEO-optimized | `references/landing-page-builder.md` |
| `landing-pages` | Patterns/critique for existing landing pages | `references/landing-pages.md` |
| `conversion-optimization` | CRO on one page: friction/trust analysis, ICE ranking, A/B test design | `references/conversion-optimization.md` |
| `funnel-design` | Pre-launch TOFU/MOFU/BOFU map, lead scoring, nurture flow, sales handoff | `references/funnel-design.md` |
| `social-proof` | Trust elements: testimonials, logos, guarantees, security signals | `references/social-proof.md` |

## When to use it

Use when a growth goal names one of the eight topics: fixing indexing, writing on-page
SEO, building or critiquing a landing page, raising conversion on a page, designing a
funnel before launch, or placing trust signals. Do **not** use it for keyword research,
link-building, paid media, or post-launch funnel analytics — those route elsewhere
(`seo-content` and `conversion-optimization` headers name the boundaries). [INFERENCE]

## How it routes / executes

1. **Resolve `topic`** to one enum verbatim (see disambiguation in `SKILL.md`). If the
   request spans 2+ topics or is ambiguous, ask once — never read two playbooks "to be safe".
2. **Read exactly one** playbook from `routes:` in `routes.json`.
3. **Run the spine** Discover → Analyze → Execute → Validate. `quick` = essentials;
   `deep` = apply exhaustively with verification at each step. Validate is never skipped.
4. **Emit** the playbook's deliverable, with evidence tags on every non-obvious claim.

## Disambiguation quick-rules

- `landing-page-builder` = build new; `landing-pages` = critique existing.
- `seo-architecture` = structure/rendering/indexing; `seo-content` = on-page copy/markup;
  `indexability-validator` = audit the navigation/README chain.
- `conversion-optimization` = one-page CRO; `funnel-design` = multi-step journey;
  `social-proof` = trust elements alone.

## Quality gates

Constitution v6.0.0 enforcement; Alfa core evidence taxonomy (single family per output);
script-first rule (prefer a deterministic script over manual steps). The route is correct
only when exactly one playbook was read, the topic matches an enum verbatim, and the
deliverable satisfies that playbook's Quality Criteria.

## Bundle map

- Domain knowledge → `knowledge/body-of-knowledge.md`, `knowledge/knowledge-graph.json`
- Role contracts → `agents/lead.md`, `agents/specialist.md`, `agents/support.md`, `agents/guardian.md`
- Prompts → `prompts/primary.md`, `prompts/meta.md`, `prompts/variations/{quick,deep}.md`
- Output scaffold → `templates/output.md`
- Worked example → `examples/example-input.md`, `examples/example-output.md`
- Evaluations → `evals/evals.json`
- Deterministic assets → `assets/` (rubric + routing matrix; see `assets/README.md`)
