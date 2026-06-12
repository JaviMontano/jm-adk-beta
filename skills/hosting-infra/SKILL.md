---
name: hosting-infra
version: 1.0.0
description: "Hosting and infrastructure: DNS, domains, SSL, CDN, serverless, backup/DR, and provider-specific deployment. Topics: backup-strategy, cdn-configuration, disaster-recovery, dns-architecture, domain-management, hostinger-deployment, infrastructure-design, serverless-patterns, ssl-management."
params:
  topic:
    enum: [backup-strategy, cdn-configuration, disaster-recovery, dns-architecture, domain-management, hostinger-deployment, infrastructure-design, serverless-patterns, ssl-management]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  backup-strategy: references/backup-strategy.md
  cdn-configuration: references/cdn-configuration.md
  disaster-recovery: references/disaster-recovery.md
  dns-architecture: references/dns-architecture.md
  domain-management: references/domain-management.md
  hostinger-deployment: references/hostinger-deployment.md
  infrastructure-design: references/infrastructure-design.md
  serverless-patterns: references/serverless-patterns.md
  ssl-management: references/ssl-management.md
---

# hosting-infra

Router skill: resolve one `topic`, Read EXACTLY ONE playbook from `routes:`, execute it. [EXPLICIT]

## When to use
Use for DNS, domains, SSL/TLS, CDN, serverless, backup/DR, and provider deploys (notably Hostinger). [EXPLICIT]
NOT for app-code architecture, CI/CD pipeline logic, or cloud cost modeling — those route elsewhere. [INFERENCIA]

## Inputs → Outputs
- In: `topic` (required, infer from request; ask only on genuine ambiguity), `depth` (`quick` default | `deep`). [CONFIG]
- Out: the playbook's deliverable (config, runbook, design) with evidence tags, no invented hostnames/IPs/prices. [EXPLICIT]

## Routing
1. Map the request to ONE enum value below; the verb + artifact usually disambiguates. [INFERENCIA]
2. Read its single `routes:` file. Never load the whole cluster — one playbook per invocation. [EXPLICIT]
3. `deep` → apply exhaustively with verification at each step; `quick` → essentials only. [CONFIG]

Topic cues (route to the named playbook): [INFERENCIA]
- **dns-architecture** records/zones/propagation · **domain-management** registrar/transfer/WHOIS/renewal
- **ssl-management** certs/HTTPS/renewal/chain · **cdn-configuration** caching/edge/invalidation
- **serverless-patterns** fan-out, saga, event-sourcing (Firestore-centric) · **infrastructure-design** topology/sizing
- **backup-strategy** RPO/snapshots/retention · **disaster-recovery** RTO/failover/runbooks
- **hostinger-deployment** static + Node via SFTP/Git, cPanel/hPanel, PM2

Spine: Discover → Analyze → Execute → Validate.

Gate criteria + per-invocation checklist live in `assets/` (`assets/quality-rubric.json`, `assets/checklist.md`). [CONFIG]

## Validation gate (before "done")
- [ ] Exactly one playbook was read and followed; no cluster-wide loading. [EXPLICIT]
- [ ] Topic matches user intent (re-confirm if a single request spans two — split, don't merge). [INFERENCIA]
- [ ] Every non-obvious claim tagged in ONE Alfa family (`[EXPLICIT]`/`[DOC]`/`[INFERENCIA]`/`[CONFIG]`/`[CÓDIGO]`/`[SUPUESTO]`); constitution v6.0.0 + script-first honored; secrets never echoed. [DOC]

## Anti-patterns
- Loading multiple `routes:` files "for context," or guessing a `topic` that spans two — defeats the router; ask or sequence. [EXPLICIT]
- Hardcoding registrar credentials, DNS records, or cert paths the user did not supply → tag `[SUPUESTO]` + verify. [SUPUESTO]

## Edge cases
- Topic ambiguous (e.g. "fix my site cert renewal") → ssl-management unless a CDN/edge layer owns TLS, then cdn-configuration. [INFERENCIA]
- Cross-cutting request (DNS + SSL + CDN for one cutover) → sequence the playbooks; do not improvise a merged plan. [SUPUESTO]
- Provider other than Hostinger → use the generic design/SSL/DNS playbooks, not hostinger-deployment. [EXPLICIT]