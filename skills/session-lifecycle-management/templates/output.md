# Reporte de Decisión de Ciclo de Vida de Sesión

> Scaffold del entregable. Reemplaza cada campo con datos reales y deja el tag de evidencia.

## 1. Encuadre

- **¿Activa?** `sí | no (no-activación)`
- **Razón si no activa:** sin SessionContext previo | input vacío | dominio ajeno  [INFERENCIA]
- **Goal:** continuo | ramificable; estado mutable compartido: sí | no  [CODE]

## 2. Snapshot del mundo

| Fuente | mtime esperado | mtime observado | hash esperado | hash observado | crítica |
|---|---|---|---|---|---|
| <source> | … | … | … | … | sí/no |

- HEAD git: `<esperado>` → `<observado>`  [CODE]
- Lockfile hash: `<esperado>` → `<observado>`  [CODE]
- Esquema/versión BD: `<esperado>` → `<observado>`  [CODE]

## 3. Staleness detectada

```json
"stale": [
  { "source": "<...>", "expected": "<...>", "observed": "<...>", "critical": true }
]
```

## 4. Decisión

- **Transition:** `resume | fork | fresh`  [CODE]
- **trigger_reason:** <qué result quedó stale / qué invariante cambió>  [CODE]
- **Regla de matriz aplicada:** <cita la regla>  [DOC]

## 5. TypedSummary (solo si `fresh`)

```json
"typed_summary": {
  "goal": "<...>",
  "decisions": ["<...>"],
  "open_questions": ["<...>"],
  "verified_facts": [ { "fact": "<...>", "source": "<...>" } ],
  "stale_dropped": ["<source...>"]
}
```

Invariante verificada: ningún `verified_fact.source` aparece en `stale_dropped`.  [CODE]

## 6. Forks (solo si `fork`)

| Rama | Hipótesis | Scratchpad aislado | Workspace aislado |
|---|---|---|---|
| <branch> | <...> | <ruta> | <ruta> |

## 7. Gate

- `scripts/check.sh`: `exit_code=<n>` — `pass | fail`  [CONFIG]
- Evidencia adjunta (hashes/HEAD usados): sí | no

## 8. Cierre

- Checklist de aceptación: 1–6 satisfechos: sí | no
- Marca: JM Labs · Sin PII · Verde solo con evidencia
