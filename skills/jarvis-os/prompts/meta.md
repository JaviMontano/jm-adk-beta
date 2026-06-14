# Prompt — meta (jarvis-os)

Meta-prompt para razonar **sobre** el ruteo de Jarvis OS antes de ejecutarlo. Úsalo para auditar la decisión, no para producir el entregable.

## Preguntas de calibración

1. **Ambigüedad de ubicación** — ¿El input deja claro el sector (N0–N4), la estación y el proyecto? Si no, ¿qué paso de la cascada lo resuelve, o hay que preguntar?
2. **Frontera de delegación** — ¿El usuario ya nombró una skill concreta? Si sí, NO re-enrutar.
3. **Producción vs. derivación** — ¿La petición pide el artefacto de dominio? Entonces el pack deriva, no produce.
4. **Estado leído** — ¿Se leyeron `docs/jarvis-os/` y el routing-map antes de inferir? ¿O hay riesgo de inferir desde caché/historial?
5. **Guardrails** — ¿Se respetan Rule-9, NOW≤3, una sola familia de tags y la frontera `user-context/`?
6. **Madurez** — ¿El nivel de adopción actual es estable antes de subir? ¿La skill tiene 3+ ejecuciones (Regla de 3) y 14 días supervisados si se automatiza?

## Auto-chequeo de evidencia
Cada conclusión debe llevar familia **kit** (`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`), una sola por documento. Marca dónde falta evidencia y conviértelo en una pregunta al usuario en lugar de un supuesto silencioso.

## Salida
Un veredicto de ruteo razonado: ruta elegida + justificación de la cascada + riesgos/guardrails verificados, o la pregunta explícita que desbloquea la ambigüedad.
