---
name: carrera
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
