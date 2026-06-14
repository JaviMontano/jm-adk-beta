# Prompt — Meta (auto-evaluacion)

Usa este prompt para auditar tu propio output de provenance-engineering antes de entregarlo. Responde cada pregunta con evidencia, no con "si" optimista.

## Checklist de auto-correccion

1. **Source.** ¿Cada claim tiene `source[]` no vacio con `source_id` + `locator` + `as_of`? ¿Algun placeholder ("varias fuentes", "interno")? Si lo hay, bloquea, no emitas.
2. **Inventario.** ¿Cada `source_id` existe en el inventario declarado? Un id desconocido falla duro.
3. **Conflicto.** ¿Hay algun valor agregado (promedio/mediana/concat) que **ninguna fuente afirma**? Si lo hay, revierte: preserva ambas fuentes con `conflict=true`.
4. **Normalizacion.** ¿Marcaste conflicto por una diferencia que es solo de formato (USD 4.2M vs 4,200,000)? Normaliza y desmarca.
5. **Escalacion.** ¿Cada `conflict=true` tiene un item en la cola humana? Conflicto marcado pero no enrutado = invariante rota.
6. **Visibilidad.** ¿El render muestra `as_of` y el marcador de conflicto? Si no, no esta listo para un auditor.
7. **Test.** ¿Existe un test estructural que falla ante claim sin source, id desconocido o conflicto silenciado?
8. **Evidencia.** ¿Cada claim no obvio lleva un solo tag Alfa-core? ¿`[CÓDIGO]` solo donde el patron esta presente? ¿Cada `[SUPUESTO]` con verificacion?

## Senales de "detente y corrige"

- Estas por devolver un valor unico donde habia desacuerdo -> preserva y escala.
- Vas a "normalizar resolviendo" la fecha o cifra ganadora -> resolucion silenciosa; revierte.
- Green/CI verde sin haber verificado los criterios -> no es prueba de exito.

Solo declara done cuando las 8 casillas pasen con evidencia.
