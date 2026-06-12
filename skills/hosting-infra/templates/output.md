# Hosting/Infra Deliverable — {{topic}} ({{depth}})

> Single-playbook output. Every non-obvious line carries ONE Alfa tag. No invented
> hostnames/IPs/cert-paths/registrar-prices. Secrets never echoed.

## 1. Request & routing
- **Resolved topic**: `<one of the nine enum values>`
- **Depth**: `quick | deep`
- **Playbook read**: `references/<topic>.md` (exactly one) [EXPLICIT]
- **In scope / out of scope**: <1–2 lines; redirect cross-cutting or non-Hostinger work>

## 2. Discover (current state)
| Item | Current | Owner / source |
|------|---------|----------------|
| <zone/record/cert/trigger/tier/plan> | <value> | <who controls> |
- **SLA targets**: RTO=<…>, RPO=<…>, traffic geography=<…> (or "not set → escalate") [DOC]

## 3. Analyze (decisions & trade-offs)
| Decision | Options | Chosen | Why (tied to tier/SLA) | Tag |
|----------|---------|--------|------------------------|-----|
| <e.g. failover mechanism> | <DNS vs anycast> | <…> | <…> | [INFERENCIA] |

## 4. Execute (the deliverable)
<The concrete artifact for this topic — pick the matching block:>

- **DNS**: record + TTL table (apex on A/ALIAS, CAA, SPF/DKIM/DMARC), cutover staging.
- **SSL**: cert chain plan + automated renewal command + HSTS gate.
- **CDN**: cache-key + edge TTL + invalidation strategy + TLS-termination decision.
- **Serverless**: function contracts, trigger types, dedupe guard, saga inverses.
- **Backup**: snapshot schedule, retention, RPO mapping, restore-proof step.
- **DR**: runbook (trigger → failover → traffic cutover → **failback**), drill date.
- **Hostinger**: `ecosystem.config.js`, atomic-swap deploy script, CI/CD reload gate.

```text
<config / commands / runbook steps here — tagged where non-obvious>
```

## 5. Validate (gate verdict)
- [ ] Exactly one playbook read and followed [EXPLICIT]
- [ ] Topic matched intent; cross-cutting work sequenced not merged [INFERENCIA]
- [ ] Playbook quality criteria met (topic-specific)
- [ ] Verification evidence captured (dig/openssl/pm2/drill as applicable)
- [ ] Every claim Alfa-tagged; no invented values; secrets safe; single-brand [DOC]

**Verdict**: `gate=pass | gate=fail` — <unmet items, if any>

## 6. Assumptions & follow-ups
- <`[SUPUESTO]` items needing user verification>
- <next sequenced playbook, if this was part of a multi-topic cutover>
