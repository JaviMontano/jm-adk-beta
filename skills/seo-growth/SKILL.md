---
name: seo-growth
description: "SEO and conversion growth: technical SEO, content SEO, landing pages, funnels, CRO, and trust patterns. Topics: conversion-optimization, funnel-design, indexability-validator, landing-page-builder, landing-pages, seo-architecture, seo-content, social-proof."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
