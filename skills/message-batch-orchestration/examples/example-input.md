# Example input — message-batch-orchestration

## Request (from the user)

> Tengo 8.000 tickets de soporte exportados a `tickets.jsonl`, cada uno con un
> `ticket_id` estable. Quiero clasificarlos por categoría esta noche (no hay
> nadie esperando en línea). Usa message-batch-orchestration: máximo 2
> reintentos, persiste los éxitos en JSONL, y reintenta solo los que fallen.

## Parsed parameters

- **Mode:** offline / latency-tolerant (overnight, no user in line). [DOC]
- **Item count:** 8000.
- **Business ID field:** `ticket_id` → used as `custom_id`. [CÓDIGO]
- **Model:** `claude-sonnet-4-5` (pinned default; not overridden). [CONFIG]
- **max_tokens:** 512 (short category label). [SUPUESTO]
- **max_retries (cap):** 2. [CONFIG]
- **Persistence:** successes to `succeeded.jsonl`. [DOC]
- **Evidence:** JSON report required to pass `scripts/check.sh`. [CONFIG]

## Sample of `tickets.jsonl` (2 of 8000)

```jsonl
{"ticket_id": "TK-100231", "prompt": "Clasifica: 'No puedo restablecer mi contraseña, el enlace expira.'"}
{"ticket_id": "TK-100232", "prompt": "Clasifica: 'Me cobraron dos veces la suscripción de junio.'"}
```

## Activation expectation

Activate (offline + stable business ID + selective retry requested). This maps
to the eval case `ticket_backfill_selective_retry`.
