# Variacion deep — revisor-veracidad

Auditoria exhaustiva para documentos largos o de alto riesgo (informes a cliente, specs, material legal/financiero donde se marca riesgo). Activa los cuatro agentes.

## Cuando

- Texto largo, multiples afirmaciones, fuentes heterogeneas.
- Salida que el orquestador exige con tags de evidencia homologados.
- Riesgo de homologacion incorrecta entre familias.

## Pasos

1. **lead**: encuadre, familia por audiencia, deteccion de `{VACIO_CRITICO}`.
2. **support**: segmentacion completa; aislar todo claim verificable de la estructura/opinion.
3. **specialist**: resolver cada claim dudoso con la regla del tag mas debil; validar `{WEB}` (cita verificable o degradar); aplicar mapping si la salida es Alfa core.
4. **support**: aplicar tags inline + redactar el plan de cierre completo (que leer, a quien preguntar, que comando correr, con `scripts/check.sh` cuando aplique).
5. **guardian**: correr el gate completo + chequeos deterministas de `scripts/`. PASS/FAIL con triggers.
6. Iterar hasta PASS.

## Profundidad extra

- Para cada `{POR_CONFIRMAR}`, especificar el artefacto que cerraria la duda y el owner.
- Cruzar claims repetidos: el mismo hecho debe llevar el mismo tag en todo el documento.
- Registrar explicitamente los claims donde solo se marca el riesgo (legal/medico/financiero/seguridad) sin decidir.

## Salida (plantilla completa de `templates/output.md`)

Texto auditado + plan de verificacion en tabla + resumen con conteo por tag, familia, bloqueos y nota de limites.
