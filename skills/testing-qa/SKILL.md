---
name: testing-qa
description: "Software testing strategy and execution: unit, E2E, BDD, cross-browser, and performance testing. Topics: bdd-full-spectrum, cross-browser-testing, e2e-testing, performance-testing, test-strategy, unit-testing."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
