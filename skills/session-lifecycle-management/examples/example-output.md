# Ejemplo — Salida (Reporte de Decisión)

## 1. Encuadre

- **¿Activa?** sí — existe `SessionContext` de T1 y hay una transición que decidir. [INFERENCIA]
- **Goal:** continuo; estado mutable compartido: no. [CODE]

## 2. Snapshot del mundo

| Fuente | mtime esperado | mtime observado | hash esperado | hash observado | crítica |
|---|---|---|---|---|---|
| src/checkout/tax.ts | 08:40 | 08:55 (touch) | a1b2c3 | a1b2c3 | sí |
| src/checkout/cart.ts | 08:41 | 08:41 | d4e5f6 | d4e5f6 | no |
| package-lock.json | 08:30 | 10:05 | 9f9f9f | 7c7c7c | sí |

- HEAD git: `abc123` → `def456` (avanzó). [CODE]
- Lockfile hash: `9f9f9f` → `7c7c7c` (cambió). [CODE]
- Esquema BD: `v42` → `v42` (sin cambio). [CODE]

## 3. Staleness detectada

```json
"stale": [
  { "source": "package-lock.json", "expected": "9f9f9f", "observed": "7c7c7c", "critical": true },
  { "source": "world.head", "expected": "abc123", "observed": "def456", "critical": true }
]
```

- `src/checkout/tax.ts`: mtime divergió pero **hash igual** → falso positivo filtrado, **no** es stale. [CODE]

## 4. Decisión

- **Transition:** `fresh`. [CODE]
- **trigger_reason:** el lockfile (dependencia **crítica**) cambió de `9f9f9f` a `7c7c7c` y HEAD avanzó de `abc123` a `def456`. La criticidad domina sobre la continuidad del objetivo. [CODE]
- **Regla de matriz aplicada:** "Una stale crítica fuerza `fresh` aunque el objetivo sea continuo." [DOC]

## 5. TypedSummary

```json
"typed_summary": {
  "goal": "arreglar cálculo de impuesto en checkout",
  "decisions": ["el bug está en redondeo, no en la tasa"],
  "open_questions": ["¿afecta a carritos multi-moneda?"],
  "verified_facts": [
    { "fact": "tax.ts usa Math.round en línea 88", "source": "src/checkout/tax.ts" }
  ],
  "stale_dropped": ["package-lock.json", "world.head"]
}
```

- Se dropea el hecho "el lockfile fija decimal.js@10.4.3" porque su `source` (`package-lock.json`) está en `stale_dropped`. [CODE]
- Se conserva el hecho de `tax.ts`: su hash no cambió → sigue verificado. [CODE]
- Invariante verificada: ningún `verified_fact.source` aparece en `stale_dropped`. [CODE]

## 6. Forks

No aplica (transición `fresh`, objetivo continuo, sin ramificación). [INFERENCIA]

## 7. Gate

- `scripts/check.sh`: `exit_code=0` — `pass`. [CONFIG]
- Evidencia adjunta: hashes de las tres fuentes + HEAD esperado/observado. [CODE]

## 8. Cierre

- Checklist de aceptación 1–6: satisfecho. Transición válida y razonada; `TypedSummary` presente; `stale_dropped` no vacío; ningún `verified_fact` desde fuente droppeada.
- Marca: JM Labs · Sin PII · Verde solo con evidencia.
