---
name: seo-growth
version: 1.0.0
description: "SEO and conversion growth router: technical SEO, content SEO, landing pages, funnels, CRO, trust patterns. Topics: conversion-optimization, funnel-design, indexability-validator, landing-page-builder, landing-pages, seo-architecture, seo-content, social-proof."
params:
  topic:
    enum: [conversion-optimization, funnel-design, indexability-validator, landing-page-builder, landing-pages, seo-architecture, seo-content, social-proof]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  conversion-optimization: references/conversion-optimization.md
  funnel-design: references/funnel-design.md
  indexability-validator: references/indexability-validator.md
  landing-page-builder: references/landing-page-builder.md
  landing-pages: references/landing-pages.md
  seo-architecture: references/seo-architecture.md
  seo-content: references/seo-content.md
  social-proof: references/social-proof.md
---

# seo-growth

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`.
Never load the whole cluster — one topic, one file. [DOC]

## Inputs / Outputs
- **In:** `topic` (one enum), `depth` (quick|deep), the growth goal + any
  URL/page/funnel context. Route to the narrowest topic the request names. [INFERENCE]
- **Out:** the single playbook's deliverable. `quick` → essentials; `deep` →
  apply exhaustively with verification at each step. [DOC]

## Topic disambiguation [INFERENCE]
- **landing-page-builder** = build a new page end-to-end; **landing-pages** =
  patterns/critique for existing pages.
- **seo-architecture** = structure/indexing/internal links; **seo-content** =
  on-page copy/keywords; **indexability-validator** = audit crawl/index status.
- **conversion-optimization** = CRO experiments on a page; **funnel-design** =
  multi-step journey; **social-proof** = trust elements.

## Spine
Discover → Analyze → Execute → Validate. Don't skip Validate even on `quick`. [DOC]

## Quality gates [DOC]
Constitution v6.0.0 enforcement; evidence tags (Alfa core set, single family);
script-first rule (prefer a script over manual steps).
Routing + acceptance rubric and signal→topic matrix live in `assets/` (see `assets/README.md`).

## Acceptance (route is correct when)
- Exactly one playbook Read; topic matches an enum verbatim. [DOC]
- Deliverable matches the playbook's contract; gates satisfied. [DOC]

## Anti-patterns / self-correction [INFERENCE]
- Reading multiple playbooks "to be safe" — pick one or ask once.
- Inventing metrics/traffic figures: tag derived numbers, never fabricate.
- Request spans 2+ topics or topic is ambiguous → ask, don't guess. Missing
  playbook for the resolved topic → stop and report.
