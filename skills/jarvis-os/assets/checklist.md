# Checklist del acceptance gate — jarvis-os

Lista determinista que `guardian` recorre antes de marcar un ruteo completo. Marca todo o autocorrige.

## Lectura de estado
- [ ] Leí `docs/jarvis-os/` (playbook + runbook).
- [ ] Leí `user-context/context/routing-map.md` (solo lectura).
- [ ] No inferí arquitectura desde caché/historial.

## Ruteo COOL
- [ ] Clarify: input capturado con timestamp + intención.
- [ ] Organize: cascada de ruteo recorrida; sector N0–N4 asignado.
- [ ] Optimize: gate verificado por evidencia.
- [ ] Liberate: scaffolder/cadencia invocado o skill concreta derivada.

## Guardrails
- [ ] Nombres en kebab-case; sectores N0–N4.
- [ ] NOW ≤ 3 por `TAREAS.md`.
- [ ] Rule-stacking preservado (root → estación → proyecto).
- [ ] Rule-9: root ≤200 / sector ≤60 / estación ≤50 / proyecto ≤70.
- [ ] Sin secretos; íntimo en `user-context/`, no en `skills/` tracked.
- [ ] Verification tags de una sola familia por documento.

## Anti-patrones (deben estar ausentes)
- [ ] No se produjo artefacto de dominio dentro del pack.
- [ ] No se re-enrutó tras una skill ya nombrada por el usuario.
- [ ] No se automatizó antes de 14 días supervisados ni se codificó skill con < 3 ejecuciones.
