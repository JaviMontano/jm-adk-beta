---
name: testing-qa
version: 1.0.0
description: "Router for software testing strategy and execution: pick one topic — bdd-full-spectrum, cross-browser-testing, e2e-testing, performance-testing, test-strategy, or unit-testing — and run its playbook."
params:
  topic:
    enum: [bdd-full-spectrum, cross-browser-testing, e2e-testing, performance-testing, test-strategy, unit-testing]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  bdd-full-spectrum: references/bdd-full-spectrum.md
  cross-browser-testing: references/cross-browser-testing.md
  e2e-testing: references/e2e-testing.md
  performance-testing: references/performance-testing.md
  test-strategy: references/test-strategy.md
  unit-testing: references/unit-testing.md
---

# testing-qa

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`. [DOC]

## When to use
- A request names a test type (unit, E2E/BDD, cross-browser, performance) or asks
  for a test plan/coverage gate. Single dimension → that topic; "what should we
  test / where to invest" → `test-strategy`. [INFERENCE]
- Skip if the ask is non-testing (build, deploy, lint) — route elsewhere. [INFERENCE]

## Routing
1. Infer `topic` from the request; ask only on genuine ambiguity between two enums. [DOC]
2. Map `topic` → `routes:` path, Read that ONE file. Never load the cluster. [DOC]
3. `depth=deep` → apply the playbook exhaustively, verifying at each step;
   `quick` → essentials only (the path most requests need). [DOC]

## Disambiguation (overlapping asks)
- BDD scenarios driving a browser → `bdd-full-spectrum` (spec-first), not `e2e-testing`. [INFERENCE]
- Load/latency/throughput → `performance-testing`, even if framed as "E2E under load". [INFERENCE]
- "Increase coverage" with no type named → `unit-testing` (coverage gate lives there). [INFERENCE]

## Spine & gates
- Spine: Discover → Analyze → Execute → Validate. [DOC]
- Gates: constitution v6.0.0 (enforcement), evidence tags (Alfa core set, EN spelling
  per `references/verification-tags.md`), script-first rule. [DOC]

## Acceptance criteria
- Exactly one playbook Read; `topic` set; `depth` respected. [DOC]
- Validate step run before "done"; no green-as-success without evidence. [DOC]
- Gate the deliverable with `assets/` (routing checklist + quality rubric). [DOC]

## Anti-patterns
- Reading 2+ playbooks "to compare", or summarizing a topic from memory instead of
  its playbook. [INFERENCE]
- Guessing `topic` silently when two enums fit equally — ask. [INFERENCE]
- Marking complete on an unrun Validate step. [DOC]
