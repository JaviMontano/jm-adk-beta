---
name: hosting-infra
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
