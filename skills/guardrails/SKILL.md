---
name: guardrails
description: "Deterministic guard layer: pre/post tool guards, prompt filter, output contracts, secrets, constitution compliance. Thin doc over hooks/scripts. Topics: constitution-compliance, input-tolerance, integrity-chain-validation, management, output-contract-enforcer, permission-fast-path, post-tool-use-validator, pre-tool-use-guard, quality-gatekeeper, secrets-sanitization, stop-validator, user-prompt-filter."
version: 1.1.0
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

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`. [EXPLICIT]

## When to use
A request targets a deterministic guard: block a command, validate a tool result,
filter a prompt, enforce an output contract, sanitize secrets, check a quality
gate or constitution principle, validate the integrity chain / stop conditions.
Triggers: `/jm:verify`, `/jm:advance`, gate/PR readiness, pre-delivery. [INFERENCE]

## Inputs → Outputs
**In:** `topic` (enum, required) + `depth` (quick|deep). **Out:** that playbook's
verdict — pass/fail/block with evidence-tagged reasons + remediation; never
green-by-default. [DOC]

## Routing
1. Map the request to one `topic`. Disambiguate from `routes.json` `desc` if two
   plausibly fit; if still ambiguous, ask — do NOT load several. [INFERENCE]
2. Read that playbook only. Never load the whole cluster (12 files). [EXPLICIT]
3. `deep` → apply exhaustively, verify each step (Discover → Analyze → Execute →
   Validate); `quick` → essentials. Gates: constitution v6.0.0, evidence tags,
   script-first. [CONFIG]

## Evidence tags
Alfa core family only: `[EXPLICIT]` `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]`
`[ASSUMPTION]`. One tag per claim; never mix families; canon in
`../../references/verification-tags.md`. [DOC]

## Acceptance criteria
- Exactly one playbook read; `topic` ∈ enum; verdict carries evidence tags. [DOC]
- Script-first (prefer the hook/script the playbook names) and fail-closed:
  missing evidence ⇒ fail/block, never pass. [CONFIG]
- Verdict quality bar in `assets/quality-rubric.json`; pre-emit checks in
  `assets/checklist.md`. [CONFIG]

## Anti-patterns
Loading multiple playbooks "to be safe"; guessing `topic` when ambiguous;
reimplementing guard logic the hooks/scripts already enforce; reporting success
without running the gate. [DOC]

## Self-correction
Two files opened, an untagged verdict, or "pass" with unmet criteria → stop;
re-resolve `topic`, re-run the named script, re-tag. [INFERENCE]
