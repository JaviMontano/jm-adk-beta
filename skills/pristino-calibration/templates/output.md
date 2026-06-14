<!--
Deliverable scaffold for pristino-calibration (full + substantive).
For bypass / solo_* / full+trivial, ship only the slice the mode requires
(see prompts/variations/quick.md). Quality gates: assets/quality-rubric.json.
-->

{{PERSONA_LABEL}}

## 1) Pedido original
{{verbatim user text}}

## 2) Prompt optimizado
- **Objetivo:** {{objective}}
- **Contexto:** {{context}}
- **Restricciones:** {{constraints}}
- **Faltantes / VACIO_CRITICO:** {{missing data — tag [ASSUMPTION] or stop-and-ask}}
- **Definition of Done:** {{DoD}}
- **Forma de salida + clamp:** {{output shape; length limit}}
- **Anti-drift:** Incluye {{...}}. NO incluye {{...}}.

## 3) Respuesta — Canvas output contract
- **Resumen:** {{1–3 lines}}
- **Evidencia (con fuentes):** {{claim — [CONFIG]/[DOC]/[CODE]; source}}
- **Decisiones y criterios:** {{decision — why}}
- **Opciones (2–3):**
  | Opción | Impacto | Esfuerzo | Riesgo |
  |--------|---------|----------|--------|
  | {{A}}  | {{...}} | {{...}}  | {{...}} |
  | {{B}}  | {{...}} | {{...}}  | {{...}} |
  - **Recomendación:** {{which + why}}
- **Plan con DoD:** {{steps, each with a done-criterion}}
- **Riesgos / límites / validación:** {{risks; what to verify next}}
- **Estado:** {{success | degraded | rejected}} · **Confianza:** {{0–1}}

<!--
Pre-ship gate (mirror of agents/guardian.md):
persona_line · mode shape · canvas_contract · evidence · precedence_order ·
delegate_agents_known · guardian_block · degraded_self_calibration.
One tag family. No invented delegates. No green-as-success. No hidden reasoning.
-->
