# Ejemplo — Salida (plan-mode-workflow)

Gate de dos modos para `payments-core`, derivado de la entrada del ejemplo.

## 1. Estado de modo

```json
{ "mode": "plan", "signed_plan_hash": null }
```

Arranca en `plan`. La exploración de `capture/` usa solo `Read`, `Grep`, `Glob` y
`Bash` de inspección — no se toca nada del trabajo no commiteado del otro dev. [CÓDIGO]

## 2. Write-blocklist (fail-closed)

```json
{
  "deny_tools": ["Write", "Edit", "MultiEdit", "NotebookEdit"],
  "deny_bash_patterns": ["rm ", "sed -i", "mv ", "git commit", "git push", ">", ">>"],
  "allow_read": ["Read", "Grep", "Glob", "Bash(inspeccion)"]
}
```

Todo lo no listado en `allow_read` se deniega en `plan`. [CONFIG]

## 3. plan.md (objeto firmable)

- **Objetivo:** añadir campo `idempotency_key` al endpoint `POST /capture`. [DOC]
- **Archivos a tocar:** `capture/handler.py`, `capture/schema.py`, `tests/test_capture.py`. [DOC]
- **Orden de cambios:** schema → handler → tests. [DOC]
- **Criterio de aceptación:** captura repetida con la misma key no duplica cargo;
  suite verde. [DOC]
- **Riesgos / rollback:** `capture/` tiene cambios ajenos sin commitear → confirmar
  con `lead-pagos@jmlabs` antes de editar; rollback = revertir el commit del cambio. [DOC]

## 4. Evento de firma

```json
{
  "hash": "sha256:9f2c…a1",
  "approved_by": "lead-pagos@jmlabs",
  "plan_signed_at": "2026-06-12T10:30:00Z"
}
```

`approve_plan("sha256:9f2c…a1", "lead-pagos@jmlabs")` mueve `mode` a `execute`. Un
"ok, dale" en el chat NO habría firmado nada. [CÓDIGO]

## 5. Hook PreToolUse (traza de decisiones)

| Intento | Modo | Decisión | Motivo |
|---------|------|----------|--------|
| `Grep "idempotency" capture/` | plan | allow | tool de lectura |
| `Edit capture/handler.py` (antes de firmar) | plan | **deny** | Plan Mode read-only; firma el hash |
| `Bash: sed -i 's/old/new/' capture/schema.py` | plan | **deny** | Bash mutante por patrón |
| `approve_plan(sha256:9f2c…a1, lead-pagos@jmlabs)` | plan→execute | allow | firma del hash exacto |
| `Edit capture/handler.py` (tras firmar) | execute | allow | modo execute habilitado |
| `plan.md` editado (hash cambia a `…b7`) → `Edit` | execute→**plan** | **deny** | hash-mismatch; re-firma requerida |

## 6. Checklist de aceptación

- [x] Escritura deshabilitada por hook en `plan`. [DOC]
- [x] Aprobación auditable (hash + `lead-pagos@jmlabs` + timestamp). [DOC]
- [x] Cambio de `plan.md` revirtió a `plan` y re-pidió firma. [DOC]
- [x] Blocklist cubre write-tools y Bash mutante. [DOC]
- [x] `bypassPermissions` no se usó; objetivo presente, no se fabricó plan. [DOC]
- [x] Plan firmado + diff final registrados. [DOC]

## 7. Cierre

- **Plan firmado:** `sha256:9f2c…a1` · **Diff final:** 3 archivos en `capture/` —
  rastro de qué autorizó `lead-pagos@jmlabs` vs. qué se ejecutó. [DOC]

---
Sin precios. Sin PII de cliente. Single-brand (JM Labs).
