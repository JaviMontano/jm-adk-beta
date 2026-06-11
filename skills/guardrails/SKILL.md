---
name: guardrails
description: "Deterministic guard layer: pre/post tool guards, prompt filter, output contracts, secrets, constitution compliance. Thin doc over hooks/scripts. Topics: constitution-compliance, input-tolerance, integrity-chain-validation, management, output-contract-enforcer, permission-fast-path, post-tool-use-validator, pre-tool-use-guard, quality-gatekeeper, secrets-sanitization, stop-validator, user-prompt-filter."
params:
  topic:
    enum: [constitution-compliance, input-tolerance, integrity-chain-validation, management, output-contract-enforcer, permission-fast-path, post-tool-use-validator, pre-tool-use-guard, quality-gatekeeper, secrets-sanitization, stop-validator, user-prompt-filter]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  constitution-compliance: references/constitution-compliance.md
  input-tolerance: references/input-tolerance.md
  integrity-chain-validation: references/integrity-chain-validation.md
  management: references/management.md
  output-contract-enforcer: references/output-contract-enforcer.md
  permission-fast-path: references/permission-fast-path.md
  post-tool-use-validator: references/post-tool-use-validator.md
  pre-tool-use-guard: references/pre-tool-use-guard.md
  quality-gatekeeper: references/quality-gatekeeper.md
  secrets-sanitization: references/secrets-sanitization.md
  stop-validator: references/stop-validator.md
  user-prompt-filter: references/user-prompt-filter.md
---

# guardrails

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
