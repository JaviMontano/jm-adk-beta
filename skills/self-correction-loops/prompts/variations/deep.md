# Variacion deep — self-correction-loops

Bucle completo con justificacion de epsilon por campo, degradacion de huerfanos,
test estructural y conformidad de contrato. Para lotes de campos en finanzas,
facturacion, inventario o reporting regulatorio.

## Procedimiento extendido

1. **Inventario.** Lista todos los agregados. Clasifica cada uno: `verifiable`
   (tiene componentes) o `unverifiable` (huerfano -> degrada a humano).
2. **Politica de epsilon.** Por `data_type`, deriva el epsilon de
   `assets/epsilon-policy.json` y escribe la **nota de justificacion** (por que
   medio centavo, por que cero, por que 1e-6). Un epsilon sin nota es defecto.
3. **Recomputo independiente.** Por campo, deriva `computed` desde los crudos.
   Documenta la formula usada para el rastro de auditoria.
4. **Comparacion tipada.** `delta = declared - computed` (signo), comparador
   estricto `> epsilon`. Registra por campo.
5. **Mismatch -> escalada.** Adjunta `action="escalate_to_human"` y deja el
   declarado intacto. Politica en `assets/mismatch-policy.json` y
   `assets/escalation-policy.json`.
6. **Test estructural.** Inyecta un mismatch en un fixture y verifica que produce
   el flag; jamas un `total=computed` silencioso. Pruebas en
   `assets/structural-test-policy.json` deben quedar en `true`.
7. **Contrato + offline.** Conforma `assets/self-correction-loops-contract.json` y
   deja el reporte listo para `scripts/validate_self_correction_loops.py` y
   `scripts/check.sh` (fixtures positivas y negativas).

## Gates de cierre

Recomputo independiente · epsilon justificado · mismatch escalado sin
sobreescritura · declared y computed visibles · delta con signo · huerfanos
degradados · test estructural en verde · contrato cumplido. Tags de evidencia en
cada paso. Sin precios. Single-brand JM Labs.
