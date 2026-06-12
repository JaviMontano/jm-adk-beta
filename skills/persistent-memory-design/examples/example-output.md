# Persistent Memory Design — Payments API multi-day audit

> Every claim tagged `[DOC] / [CONFIG] / [INFERENCE] / [SUPUESTO]`. State, not a log.

## 1. Context
- **Goal:** auditar una API de pagos multi-servicio durante varios dias; excede una ventana de contexto. [DOC]
- **Sessions:** multi-sesion (se retoma manana). [DOC]
- **Writers:** dos sub-agentes (seguridad, contratos) → concurrencia obligatoria. [INFERENCE]

## 2. File contract
- **Path:** `.agent/scratchpad.md` — repo-relative; un `../scratchpad.md` se rechazaria por fuga entre repos. [DOC]
- **Format:** Markdown plano (legible, diff limpio, sin parser fragil). [INFERENCE]
- **Bootstrap si ausente:** crear el esqueleto de secciones, tratar como estado vacio, nunca error. [INFERENCE]

## 3. Fixed schema (invariant)
```markdown
## Hypotheses
## Decisions
## Findings
## Open
```

## 4. Entry filter
- A `## Findings`/`## Decisions` solo entran conclusiones validadas con `[src:… @ …]`. [DOC]
- Sospechas sin confirmar → `## Hypotheses`; preguntas abiertas → `## Open`. [DOC]
- Se rechaza: transcript crudo, dumps de tools, entradas sin provenance. [DOC]

### Estado tras el primer dia (ejemplo)
```markdown
## Hypotheses
- /refunds podria no revalidar el idempotency-key en reintentos [unvalidated]

## Decisions
- Alcance: solo endpoints v2 publicos esta semana [src:kickoff-notes @ 2026-06-10]

## Findings
- POST /charges valida firma HMAC del webhook [src:gateway/webhooks.py:88 @ 2026-06-11]
- GET /balance no exige scope; cualquier token lee saldo [src:auth/scopes.py:41 @ 2026-06-11]

## Open
- Confirmar rate-limit en /payouts (no auditado aun)
```

## 5. Read protocol
- Bootstrap lee el archivo **una vez** a estado cacheado (`scratchpad_loaded=true`); los turnos siguientes referencian, no releen → preserva el prompt cache. [DOC]

## 6. Write discipline
- Upsert por clave estable (p. ej. `endpoint+check`); nunca rewrite total. [INFERENCE]
- Si `/balance` luego exige scope, se **reemplaza** la entrada por su clave y se nota el cambio en `## Decisions`; no se acumulan dos versiones. [INFERENCE]

## 7. Survival check
- Tras `/compact` y reset, el agente reconstruye "que ya audite" solo desde el archivo y NO vuelve a leer `gateway/webhooks.py`. ☑ pass (estado reconstruido == estado pre-compact). [DOC]

## 8. Concurrency
- Seguridad y contratos hacen upsert por clave; ultimo upsert-por-clave gana; sin merge ciego de texto. [INFERENCE]

## 9. Bounded growth
- Al cerrar `/payouts`, se elimina de `## Open`; hallazgos obsoletos se colapsan por clave. [INFERENCE]

## 10. Acceptance gate
- ☑ Solo conclusiones validadas
- ☑ Esquema fijo de 4 secciones
- ☑ Lectura unica / referencia despues
- ☑ Upsert idempotente, sin rewrite total
- ☑ Sobrevive a `/compact` + reset
- ☑ Cada Finding/Decision con `[src:… @ …]`
- ☑ Concurrencia resuelta (2 escritores)
- ☑ Reporte JSON pasa `scripts/check.sh` [CONFIG]

---
Single brand (JM Labs); no invented prices; no client PII.
