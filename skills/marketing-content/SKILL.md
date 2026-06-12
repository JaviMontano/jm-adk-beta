---
name: marketing-content
version: 1.0.0
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

Router skill: maps a marketing-content request to exactly one specialist playbook. [DOC]

## When to use
Producing or revising marketing artifacts: case studies, content calendars,
copywriting, events, podcasts, press releases, video scripts, whitepapers. [DOC]
NOT for: brand voice/tone defaults, internal comms, or sales decks — those are
separate skills; routing them here loads the wrong playbook. [INFERENCE]

## Inputs / outputs
- In: `topic` (one of the 8 enum values), `depth` (`quick`|`deep`). [CONFIG]
- Out: the artifact the resolved playbook specifies — never produced inline here. [DOC]

## Procedure
1. Resolve `topic` from the request; if two topics plausibly fit, ask — do not
   guess (wrong route wastes the whole run). [INFERENCE]
2. Read EXACTLY ONE playbook from `routes:`. Never load the cluster. [CONFIG]
3. Execute that playbook along the spine: Discover → Analyze → Execute → Validate. [DOC]
4. `depth=deep` → apply exhaustively, verify each step; `quick` → essentials only. [CONFIG]

## Topic routing (mirror of `routes:` — keep in sync)
case-study-writing · content-calendar · copywriting-frameworks · event-marketing
· podcast-prep · press-release · video-script · whitepaper-creation [CONFIG]

## Validation gate (before returning)
- Exactly one playbook was read; no sibling references loaded. [CONFIG]
- Output matches the resolved `topic`; `depth` honored. [DOC]
- Evidence tags present (Alfa set, see `references/verification-tags.md`); no
  invented prices; single-brand. [DOC]

## Anti-patterns
- Routing on a keyword match without confirming intent. [INFERENCE]
- Producing the artifact in this file instead of delegating to the playbook. [DOC]
- Loading multiple playbooks "to compare" — defeats the router. [INFERENCE]

Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule. [DOC]
Routing rubric + checklist: `assets/` (quality-rubric.json, checklist.md). [CONFIG]
