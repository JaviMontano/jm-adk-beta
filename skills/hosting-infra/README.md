# hosting-infra — skill overview

Router skill for **hosting and infrastructure**: DNS, domains, SSL/TLS, CDN,
serverless (Firestore-centric), backup/DR, infrastructure design, and
provider-specific deployment (notably Hostinger). [EXPLICIT]

## What it does
Resolves ONE `topic` from the request, reads EXACTLY ONE playbook from
`routes:`, and executes it along the **Discover → Analyze → Execute → Validate**
spine — emitting the playbook's deliverable (config, runbook, or design) with
Alfa evidence tags and no invented hostnames/IPs/registrar prices. [EXPLICIT]

## When to use
- DNS records/zones/TTL/propagation, geo-routing, failover. [EXPLICIT]
- Domain registrar/transfer/WHOIS/renewal/auth-code work. [EXPLICIT]
- SSL/TLS certs, chain, HTTPS, renewal, CAA pinning. [EXPLICIT]
- CDN caching, edge rules, cache invalidation. [EXPLICIT]
- Serverless fan-out / saga / event-sourcing on Cloud Functions + Firestore. [EXPLICIT]
- Backup RPO/snapshots/retention and disaster-recovery RTO/failover runbooks. [EXPLICIT]
- Hostinger static + Node deploys (SFTP/Git, cPanel/hPanel, PM2). [EXPLICIT]

**NOT for**: app-code architecture, CI/CD pipeline business logic, or cloud cost
modeling — those route to other skills. Non-Hostinger providers use the generic
design/SSL/DNS playbooks, not `hostinger-deployment`. [INFERENCIA]

## How it routes
1. Map the request to ONE enum value (`backup-strategy`, `cdn-configuration`,
   `disaster-recovery`, `dns-architecture`, `domain-management`,
   `hostinger-deployment`, `infrastructure-design`, `serverless-patterns`,
   `ssl-management`). The verb + artifact usually disambiguates. [INFERENCIA]
2. Read its single `routes:` file — never load the whole cluster. [EXPLICIT]
3. `depth=deep` → apply exhaustively with per-step verification;
   `depth=quick` → essentials only. [CONFIG]
4. Cross-cutting request (e.g. DNS + SSL + CDN cutover) → **sequence** the
   playbooks; never improvise a merged plan. [SUPUESTO]

## References (one per invocation)
- `references/dns-architecture.md` — record topology, TTL strategy, failover, geo.
- `references/domain-management.md` — registrar, transfer, WHOIS, renewal.
- `references/ssl-management.md` — certs, chain, HTTPS, renewal, CAA.
- `references/cdn-configuration.md` — caching, edge rules, invalidation.
- `references/serverless-patterns.md` — fan-out, saga, event-sourcing (Firestore).
- `references/infrastructure-design.md` — topology, sizing.
- `references/backup-strategy.md` — RPO, snapshots, retention.
- `references/disaster-recovery.md` — RTO, failover, runbook, game-day drill.
- `references/hostinger-deployment.md` — static + Node via SFTP/Git, PM2, CI/CD.

## DoD bundle
- `agents/` — lead, specialist, support, guardian role contracts for this skill.
- `knowledge/` — body-of-knowledge + knowledge-graph of hosting/infra concepts.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold.
- `evals/evals.json` — topic-routing and gate eval cases.
- `examples/` — a worked DNS+SSL cutover example.
- `assets/` — reusable rubric/checklist bundle (see `assets/README.md`).
