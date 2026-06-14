# Ejemplo — Entrada

## Escenario

Un agente de larga duración corrige un bug de pago. En el turno T1 leyó tres archivos y capturó invariantes. Entre T1 y T2 un compañero hizo `npm install` de una dependencia nueva (cambió el lockfile) y un `git pull` (avanzó HEAD). El objetivo sigue siendo el mismo: "arreglar el cálculo de impuesto en checkout".

## SessionContext capturado en T1

```json
{
  "timestamp": "2026-06-11T09:00:00Z",
  "goal": { "text": "arreglar cálculo de impuesto en checkout", "kind": "continuo", "shares_mutable_state": false },
  "tool_results": [
    { "source": "src/checkout/tax.ts", "mtime": "2026-06-11T08:40:00Z", "hash": "a1b2c3", "critical": true },
    { "source": "src/checkout/cart.ts", "mtime": "2026-06-11T08:41:00Z", "hash": "d4e5f6", "critical": false },
    { "source": "package-lock.json",   "mtime": "2026-06-11T08:30:00Z", "hash": "9f9f9f", "critical": true }
  ],
  "world_invariants": { "head": "abc123", "lockfile_hash": "9f9f9f", "db_schema": "v42" },
  "decisions": ["el bug está en redondeo, no en la tasa"],
  "open_questions": ["¿afecta a carritos multi-moneda?"],
  "facts": [
    { "fact": "tax.ts usa Math.round en línea 88", "source": "src/checkout/tax.ts" },
    { "fact": "el lockfile fija decimal.js@10.4.3", "source": "package-lock.json" }
  ]
}
```

## Estado actual observado en T2

- `git rev-parse HEAD` → `def456` (avanzó; difiere de `abc123`).
- `package-lock.json`: mtime `2026-06-11T10:05:00Z`, hash `7c7c7c` (difiere de `9f9f9f`). **Crítica.**
- `src/checkout/tax.ts`: mtime cambió por `touch` del editor, pero hash sigue `a1b2c3` (sin cambio real).
- `src/checkout/cart.ts`: mtime y hash sin cambio.

## Pedido

Decide la transición de sesión para T2 con `session-lifecycle-management` y, si corresponde, emite el `TypedSummary`.
