# Checklist — gate de la retro semanal

Espejo operativo del gate de `SKILL.md`. El guardian bloquea el "hecho" hasta
que cada casilla este marcada. Mapea a `evals/evals.json`.

## evidence
- [ ] Cada item de Ayudo/Friccion lleva **exactamente un** tag Jarvis `{...}`.
- [ ] Ningun `{WEB}` sin cita; ningun item firme sin fuente citable.
- [ ] Todo `{SUPUESTO}`/`{POR_CONFIRMAR}` lleva su paso de verificacion.
- [ ] Una sola familia de tags (sin Alfa `[...]`).

## quality_criteria
- [ ] >=1 accion concreta para la proxima semana, con primer paso ejecutable.
- [ ] Si no hubo regla, una linea justifica por que (no todo patron asciende).
- [ ] Toda regla promovida esta en imperativo, una linea, con destino nombrado.
- [ ] El umbral >=2 ocurrencias se cumple para cada promocion.

## upgrade_safety
- [ ] Ninguna promocion P12 escribio memoria sin diff mostrado + confirmacion.
- [ ] Persistencia aditiva; historico y ediciones locales intactos.
- [ ] `--force` no usado a ciegas.
- [ ] Marca unica: un solo workspace por bloque y por destino.

Veredicto: `pass` solo si todas las casillas estan marcadas. Falla nombrada → de
vuelta al lead.
