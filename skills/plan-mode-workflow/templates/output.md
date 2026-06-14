# Gate de dos modos — <repo objetivo>

> Contrato determinístico del **plan-mode-workflow**. Todo lo siguiente es dato que
> un hook puede leer y hacer cumplir, no prosa. Tags de evidencia obligatorios.

## 1. Estado de modo

```json
{ "mode": "plan", "signed_plan_hash": null }
```

- Arranca en `plan`. Único camino a `execute`: `approve_plan(hash, approver)`. [CÓDIGO]

## 2. Write-blocklist (fail-closed)

| Categoría | Elementos bloqueados en `plan` |
|-----------|-------------------------------|
| Write-tools | `Write`, `Edit`, `MultiEdit`, `NotebookEdit`, MCP de mutación |
| Bash mutante (por patrón) | `rm `, `sed -i`, `mv `, `git commit`, `git push`, `>`, `>>` |
| Allowlist de lectura | `Read`, `Grep`, `Glob`, `Bash` de inspección |

- Todo lo que no esté en la allowlist se deniega. [CONFIG]

## 3. plan.md (objeto firmable)

- **Objetivo:** <qué se va a lograr> [DOC]
- **Archivos a tocar:** <lista> [DOC]
- **Orden de cambios:** <secuencia> [DOC]
- **Criterio de aceptación:** <cómo se sabe que está bien> [DOC]
- **Riesgos / rollback:** <qué puede salir mal y cómo revertir> [DOC]

## 4. Evento de firma

```json
{ "hash": "<sha256 del plan.md>", "approved_by": "<aprobador>", "plan_signed_at": "<timestamp>" }
```

- Referencia el hash exacto. Un "ok" en chat NO es firma. [CÓDIGO]

## 5. Hook PreToolUse (enforcement)

- Si `hash(plan.md) != signed_plan_hash` → revertir a `plan`, deny. [CÓDIGO]
- Si `mode == "plan"` y tool ∈ blocklist → deny con motivo. [CÓDIGO]
- Si `mode == "plan"` y Bash con patrón mutante → deny por patrón. [CÓDIGO]

## 6. Checklist de aceptación (gate)

- [ ] Escritura deshabilitada por hook, no por convención. [DOC]
- [ ] Aprobación auditable (hash + aprobador + timestamp). [DOC]
- [ ] Cambio de `plan.md` revierte a `plan` y re-pide firma. [DOC]
- [ ] Blocklist enumera write-tools y Bash mutante. [DOC]
- [ ] `bypassPermissions` rechazado; entrada vacía no fabrica plan. [DOC]
- [ ] Plan firmado + diff final como rastro auditable. [DOC]

## 7. Cierre

- **Plan firmado:** <hash> · **Diff final:** <enlace/resumen> — rastro de qué se autorizó vs. ejecutó. [DOC]

---
Sin precios. Sin PII de cliente. Single-brand (JM Labs).
