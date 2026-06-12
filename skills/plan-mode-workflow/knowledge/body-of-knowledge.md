# Body of Knowledge — plan-mode-workflow

## Problema central

Un agente con permisos de escritura puede mutar un repo desconocido desde el
primer turno, antes de entender su blast radius. El daño (pisar trabajo no
commiteado, romper producción, ejecutar cambios no aprobados) es difícil de
revertir. La defensa no es pedirle al modelo que "tenga cuidado": es un **gate
estructural** que separa exploración de ejecución y exige una **firma auditable**
entre ambas. [INFERENCIA]

## Conceptos clave

- **Plan Mode (read-only).** Estado donde solo se permiten `Read`, `Grep`, `Glob`
  y `Bash` de inspección. Produce un `plan.md`. No hay escritura posible. [CÓDIGO]
- **Execute Mode.** Estado donde la escritura está habilitada. Solo se alcanza tras
  firmar el plan por hash. [CÓDIGO]
- **Estado de modo.** `mode ∈ {"plan","execute"}` + `signed_plan_hash`. Es un dato
  que el hook lee, no una intención en prosa. Arranca en `plan`. [CÓDIGO]
- **`plan.md` firmable.** Artefacto con objetivo, archivos a tocar, orden de cambios,
  criterio de aceptación y riesgos. Es el objeto cuyo hash se firma. [DOC]
- **Evento de firma.** `{ hash, approved_by, plan_signed_at }`. Referencia el hash
  exacto del plan. Auditable y persistido. [CÓDIGO]
- **Hook `PreToolUse`.** Intercepta cada invocación de tool y decide `allow`/`deny`
  según el modo y la blocklist. Es el enforcement; el modelo no puede saltárselo. [CÓDIGO]
- **Write-blocklist.** Enumeración explícita de write-tools y patrones de Bash mutante.
  Fail-closed: todo lo que no esté en la allowlist de lectura se deniega. [CONFIG]

## Estándares y reglas de decisión

1. **El modo es estado, no prosa.** Si el control vive en una frase ("ahora escribo"),
   no hay gate. Debe ser un campo legible por el hook. [CÓDIGO]
2. **Fail-closed, no fail-open.** Allowlist de lectura + deny por defecto. Una
   whitelist de writes deja pasar lo no enumerado. [INFERENCIA]
3. **La firma referencia el hash exacto.** Aprobar "el plan" sin hash no es firma;
   un cambio posterior se colaría. `hash_now != signed_plan_hash` → revertir a `plan`. [CÓDIGO]
4. **Bash mutante es escritura.** `rm `, `sed -i`, `mv `, `git commit`, `git push`,
   `>`, `>>` se bloquean por patrón de comando, no solo por nombre de tool. [CÓDIGO]
5. **`bypassPermissions` anula el gate.** Se rechaza como caso bloqueado; el gate
   deja de existir si los permisos se saltan. [CONFIG]
6. **Entrada vacía no fabrica plan.** Sin objetivo no hay `plan.md` que firmar →
   detener y pedir, no auto-completar. [INFERENCIA]
7. **Cierre con evidencia.** Plan firmado + diff final = rastro de qué se autorizó
   y qué se ejecutó. Sin este par, no hay auditabilidad. [DOC]

## Máquina de estados (resumen)

```
[plan] --approve_plan(hash, approver)--> [execute]
[execute] --hash(plan.md) != signed_plan_hash--> [plan]   # re-firma obligatoria
[plan] --write-tool o Bash mutante--> DENY (se mantiene en plan)
```

## Anti-patrones a vigilar

- `bypassPermissions` + escritura desde el turno 1, sin plan ni firma.
- Aprobación como "ok" en el chat (sin hash, aprobador ni timestamp).
- Whitelist de writes en lugar de blocklist (fail-open).
- Bash mutante permitido en `plan` como "preparación".
- Cambio de `plan.md` que no revierte a `plan`.

## Taxonomía de evidencia

`[CÓDIGO]` hook/estado/hash · `[CONFIG]` blocklist/policy/permisos · `[DOC]` plan y
aprobación · `[INFERENCIA]` deducción de diseño · `[SUPUESTO]` señal de plataforma
no verificada. Sin precios. Sin PII de cliente. Single-brand (JM Labs).
