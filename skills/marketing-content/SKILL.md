---
name: marketing-content
description: "Marketing content production: copywriting, calendars, PR, case studies, whitepapers, video scripts, podcasts, and events. Topics: case-study-writing, content-calendar, copywriting-frameworks, event-marketing, podcast-prep, press-release, video-script, whitepaper-creation."
params:
  topic:
    enum: [case-study-writing, content-calendar, copywriting-frameworks, event-marketing, podcast-prep, press-release, video-script, whitepaper-creation]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  case-study-writing: references/case-study-writing.md
  content-calendar: references/content-calendar.md
  copywriting-frameworks: references/copywriting-frameworks.md
  event-marketing: references/event-marketing.md
  podcast-prep: references/podcast-prep.md
  press-release: references/press-release.md
  video-script: references/video-script.md
  whitepaper-creation: references/whitepaper-creation.md
---

# marketing-content

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
