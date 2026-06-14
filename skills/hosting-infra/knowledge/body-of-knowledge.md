# Body of Knowledge — hosting-infra

Domain reference for the router's nine topics. Each section states the concepts,
standards, and decision rules a deliverable must respect. [EXPLICIT]

## 1. DNS architecture
- **Record law**: apex (`@`) takes A/AAAA or ALIAS/ANAME — never CNAME (apex
  CNAME breaks NS/SOA/MX). Subdomains take CNAME. [EXPLICIT]
- **TTL strategy**: 300s default; 30–60s on failover targets (faster recovery,
  more queries/cost); lower to 60–300s 24–48h before a cutover, raise after
  propagation. [EXPLICIT]
- **Mail trust**: MX + SPF + DKIM + DMARC (TXT) or spoofing/spam-folder. [EXPLICIT]
- **CAA** pins allowed CAs — set before relying on auto-issued certs. [EXPLICIT]
- **Decision rule**: DNS failover (cheap, bounded by resolver TTL caching) vs
  anycast/global LB (in-network, faster, costlier) — pick per RTO. [EXPLICIT]

## 2. Domain management
- Registrar lock, EPP/auth (transfer) code, 60-day post-transfer/registration
  transfer lock, WHOIS privacy, auto-renew, expiry → redemption → release. [DOC]
- **Decision rule**: never let a production domain ride a single un-monitored
  renewal; track expiry as an asset with an owner. [SUPUESTO]

## 3. SSL / TLS
- Serve the **full chain** (leaf + intermediates), not just the leaf. [DOC]
- Let's Encrypt = 90-day certs → automate renewal (certbot/ACME); verify a cron
  or provider auto-renew exists. [DOC]
- Enable **HSTS only after** HTTPS is proven end-to-end. CAA aligns issuance. [DOC]

## 4. CDN configuration
- Cache-key design, edge TTL vs invalidation cost, origin-shield, stale-while-
  revalidate; decide who terminates TLS (edge vs origin). [INFERENCIA]
- **Decision rule**: prefer long edge TTL + targeted invalidation over short TTL
  (which multiplies origin load). [INFERENCIA]

## 5. Serverless patterns (Firestore-centric)
- Triggers fire **at-least-once** and may arrive **out of order** → every handler
  idempotent (dedupe guard on event/doc ID) and order-independent. [DOC]
- **Fan-out**: one write → N idempotent side-effects. **Saga**: each step has a
  compensating inverse; eventual consistency. **Event sourcing**: replay/audit at
  the cost of storage growth + read-model rebuild. [EXPLICIT]
- **Anti-scope**: AWS Lambda/Azure Functions (R-002); jobs >540s → Cloud Run. [INFERENCIA]

## 6. Infrastructure design
- Topology + sizing per Constitution XIII/XIV; right-size to the tier, not the
  worst case. [EXPLICIT]

## 7. Backup strategy
- **RPO** = max tolerable data loss → drives snapshot frequency + retention. An
  untested backup is not a recovery option — prove restore. [DOC]

## 8. Disaster recovery
- **RTO** = max tolerable downtime; **RPO** per tier, set by business not ops.
  Cost ladder (ascending speed/cost): backup-restore (hours) → pilot-light →
  warm-standby → active-active (near-zero, doubles run cost). [DOC]
- Runbook MUST cover trigger, failover, traffic cutover, **and failback**
  (reconciling diverged writes). Prove with a game-day drill. [DOC]

## 9. Hostinger deployment
- Shared plans give no persistent Node process → use VPS + PM2. `pm2 startup`
  (copy-run the printed sudo line) is required for reboot survival; `pm2 save`
  only persists the list. [DOC]
- Bind app to `127.0.0.1:<port>` behind Nginx/Apache + Let's Encrypt; never
  expose the Node port. Script every deploy; atomic symlink swap for rollback;
  gate `pm2 reload` behind `npm ci` success. [EXPLICIT]

## Cross-cutting rules
- **Single playbook per invocation**; sequence (never merge) cross-cutting work. [EXPLICIT]
- **Evidence taxonomy**: `[EXPLICIT]` `[DOC]` `[INFERENCIA]` `[CONFIG]` `[CÓDIGO]`
  `[SUPUESTO]` — exactly one per non-obvious claim. [DOC]
- **Never invent** hostnames, IPs, cert paths, auth codes, or registrar prices;
  tag unknowns `[SUPUESTO]` and verify. Secrets never echoed. [SUPUESTO]
