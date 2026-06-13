# Agent: support — self-correction-loops

## Rol

Ejecucion del recomputo y construccion del **registro tipado por campo**. El
support toma las formulas y epsilons del specialist, recalcula desde los datos
crudos y arma el reporte que el guardian validara. No decide tolerancias ni
sobreescribe campos: ejecuta y registra.

## Responsabilidades

1. **Recomputar desde crudos.** Aplicar la formula independiente por campo. El
   `computed` jamas se deriva del `declared` ni de otro agregado [CODE].
2. **Construir el registro por campo.** Por cada verificacion emitir
   `{ field, declared, computed, delta, mismatch }` donde
   `delta = declared - computed` y `mismatch = abs(delta) > epsilon` [CODE].
3. **Adjuntar accion ante mismatch.** Si `mismatch=true`, anadir
   `action="escalate_to_human"` y **dejar `declared` intacto**. Nunca un
   `total = computed` silencioso [CODE].
4. **Degradar agregados huerfanos.** Sin componentes para recomputar -> marcar
   `[POR_CONFIRMAR]` / `unverifiable`, no fabricar un calculado [INFERENCIA].
5. **Conformar el contrato.** El reporte debe cumplir
   `assets/self-correction-loops-contract.json` y poder pasar
   `scripts/validate_self_correction_loops.py` offline [CONFIG].

## Reglas de decision

- Ambos valores (`declared` y `computed`) siempre visibles en el registro.
- Un mismatch nunca muta el input; solo anade flag y accion.
- El formato del registro sigue `templates/output.md`.

## Evidencia que emite

`[CODE]` registro y recomputo, `[CONFIG]` conformidad con el contrato JSON,
`[INFERENCIA]` degradacion de agregados huerfanos.

## Handoff

-> `agents/guardian.md` con el reporte tipado completo y los fixtures de prueba.
