---
name: carrera
version: 1.0.0
description: "Pack de carrera (es): proceso de seleccion, entrevistas, negociacion, CV, onboarding, red. Topics: acta-formal, cierre-conversacion, cv-cover-optimizer, cv-enhancement, follow-up-email, gratitud-post-proceso, negociacion-oferta, onboarding-90-dias, proceso-seleccion-orchestrator, red-y-referencias, simulador-entrevista, validar-liquidacion-co."
params:
  topic:
    enum: [acta-formal, cierre-conversacion, cv-cover-optimizer, cv-enhancement, follow-up-email, gratitud-post-proceso, negociacion-oferta, onboarding-90-dias, proceso-seleccion-orchestrator, red-y-referencias, simulador-entrevista, validar-liquidacion-co]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  acta-formal: references/acta-formal.md
  cierre-conversacion: references/cierre-conversacion.md
  cv-cover-optimizer: references/cv-cover-optimizer.md
  cv-enhancement: references/cv-enhancement.md
  follow-up-email: references/follow-up-email.md
  gratitud-post-proceso: references/gratitud-post-proceso.md
  negociacion-oferta: references/negociacion-oferta.md
  onboarding-90-dias: references/onboarding-90-dias.md
  proceso-seleccion-orchestrator: references/proceso-seleccion-orchestrator.md
  red-y-referencias: references/red-y-referencias.md
  simulador-entrevista: references/simulador-entrevista.md
  validar-liquidacion-co: references/validar-liquidacion-co.md
---

# carrera

Router skill for the Spanish career cluster. Resolve `topic`, then Read EXACTLY
ONE playbook from `routes:` and follow it. Never load the whole cluster. [DOC]

## When to use
Trigger on candidate-side career work: selection-process tracking, mock
interviews, offer evaluation, CV/cover optimization, follow-ups, 30/60/90
onboarding, reference networks, gratitude notes, formal acta, conversation
closeout, or Colombian liquidación validation. [DOC] If the ask is hiring-side
(JD authoring, sourcing, screening rubrics for an employer), this is out of
scope — route to a recruiting skill instead. [INFERENCIA]

## Inputs → Outputs
- **In:** request + supplied evidence (emails, notes, CV, offer, payslip);
  `topic` (required, inferred); `depth` (default `quick`). [CONFIG]
- **Out:** exactly the chosen playbook's contract, each non-obvious claim tagged
  from one tag family: `[DOC]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]`. [DOC]

## Routing
1. Match the request to one topic enum. Ambiguous between two → ask one
   disambiguating question; never guess silently. [INFERENCIA]
2. Read the single `routes:` playbook for that topic. Do not preload siblings. [DOC]
3. `depth=deep` → apply exhaustively, verify at each step; `quick` →
   essentials only, same gates. [CONFIG]

Spine (every playbook): Discover → Analyze → Execute → Validate, under
constitution v6.0.0 enforcement, evidence tags, and the script-first rule. [CONFIG]

## Validation gate (before returning)
- [ ] Exactly one playbook loaded; no cross-cluster reads. [DOC]
- [ ] Output shape matches that playbook's contract. [DOC]
- [ ] Tags present, one family, consistent ES/EN spelling. [DOC]
- [ ] No invented numbers, prices, or live-market claims; `[SUPUESTO]`/
      `{POR_CONFIRMAR}` each paired with a verification step. [DOC]
- [ ] Missing critical input → stop and ask (`{VACIO_CRITICO}`), never auto-fill. [DOC]

## Anti-patterns
- Loading several playbooks "to compare" — defeats the router. [INFERENCIA]
- Fabricating salary/market figures or settlement amounts to fill gaps. [INFERENCIA]
- Mixing tag families, `{WEB}` without citation, or free-handing past a
  playbook's script-first steps. [DOC]

## Assets
Router-level support lives in `assets/` (see `assets/README.md`):
`assets/quality-rubric.json` (guardian gates) and `assets/routing-keywords.json`
(topic disambiguation). Per-topic policy assets stay in each playbook. [CONFIG]