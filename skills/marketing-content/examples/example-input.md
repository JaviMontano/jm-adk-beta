# Example Input — marketing-content

A representative request that exercises routing, disambiguation, and a topic
playbook end to end.

## User request
"We just wrapped a project with a regional retailer — we reduced their support
ticket resolution time from 9 days to 2.6 days in a quarter and CSAT went from
3.2 to 4.5. The Head of Support said 'We finally got ahead of it.' Turn this
into something our sales team can send to prospects."

## Provided context
- Brand: MetodologIA (single brand confirmed). [EXPLICIT]
- Baseline metrics: 9d → 2.6d resolution; CSAT 3.2 → 4.5. [EXPLICIT]
- Quote: "We finally got ahead of it." — Head of Support. [EXPLICIT]
- Quote approval status: not yet confirmed on file. [SUPUESTO]
- Depth requested: quick.

## What the router must decide
- Topic: this is a before/after outcome with a quote and a baseline — a
  `case-study-writing` request, not a `press-release` (no newsworthy launch) and
  not `copywriting-frameworks` (no landing page / CTA-driven offer). [INFERENCIA]
- Runner-up rejected: press-release — there is no external news hook. [INFERENCIA]
- Gate to watch: the client quote is not yet approved; it must be held as
  `[NEEDS APPROVAL]` and the piece cannot publish until cleared. [DOC]
