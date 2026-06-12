# Checklist operativa — context-window-engineering

Lista de verificación previa a marcar la skill como aplicada. Úsala junto al gate de SKILL.md.

## Partición y orden
- [ ] Cada bloque clasificado como estático o dinámico, con justificación.
- [ ] Orden estático-first: rol, herramientas, políticas, esquema, few-shot al inicio.
- [ ] Prefijo serializado byte-idéntico (orden y whitespace estables entre turnos).

## Prefijo limpio
- [ ] `grep -nE 'timestamp|now|request_id|uuid|counter'` sobre el bloque estático: sin coincidencias.
- [ ] Tool definitions en el prefijo solo si son estables en la sesión.
- [ ] Few-shot largos en el prefijo, no intercalados con estado por-turno.

## Estado volátil
- [ ] Todo valor por-turno renderizado únicamente en el bloque `<reminder>` final.

## Edge placement
- [ ] Reglas críticas en el borde inicial.
- [ ] Solo las irrenunciables reafirmadas en el borde final (sin sobre-rellenar).
- [ ] Ninguna regla crítica sepultada en el centro.

## Compactación
- [ ] Umbral fijo explícito (>55% u otro justificado).
- [ ] La compactación resume el intermedio y no toca/reordena los bordes.
- [ ] Decisión compactar vs truncar documentada con su trade-off.

## Validación medida
- [ ] Cache-hit rate medido (no asumido).
- [ ] Prueba de retención de la regla crítica en contexto largo ejecutada.

## Gobernanza
- [ ] Tags de evidencia en cada afirmación.
- [ ] Sin promesa de factor de ahorro sin medición.
- [ ] Veredicto del guardian: PASA/RECHAZA con evidencia.
