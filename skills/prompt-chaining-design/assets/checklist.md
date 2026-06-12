# Checklist determinística — prompt-chaining-design

Contrato offline para validar un diseño de cadena de pases. Espejo de los gates en
`quality-rubric.json`. Cualquier "no" es bloqueante. [CÓDIGO]

## Gates de diseño

- [ ] El pase de integración nunca ve datos crudos, solo resúmenes.
- [ ] Cada pase tiene un schema de salida explícito y tipado.
- [ ] El estado de error está tipado por unidad (`status="error"`), no excepción global.
- [ ] El pase local procesa una sola unidad y es idempotente y paralelizable.
- [ ] Existe un schema de transición explícito (colección tipada).
- [ ] El chaining se justifica frente a single-pass (volumen / paralelismo / aislamiento).

## Gates de gobernanza

- [ ] Activación correcta: la tarea es procesamiento por lote, no una tarea puntual.
- [ ] Inputs requeridos presentes; si falta el lote, la unidad o el objetivo → `{VACIO_CRITICO}`.
- [ ] Upgrade seguro: solo se completan archivos faltantes; no se sobrescriben ediciones
      locales ni se tocan otras skills.
- [ ] Sin precios inventados, sin PII de cliente, marca única.
- [ ] Ningún gate verde sin evidencia adjunta (`[DOC]`/`[CÓDIGO]`).
