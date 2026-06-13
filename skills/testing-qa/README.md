# testing-qa

Router skill for software testing strategy and execution. Resolves one `topic`
from the request, then Reads exactly one playbook and runs its Discover → Analyze
→ Execute → Validate spine. [DOC]

## What it does
Picks the right testing discipline for a request and executes its playbook —
never a generic "test everything" pass. The six routes are distinct disciplines,
not synonyms:

- **test-strategy** — the *policy*: test-level mix (pyramid/trophy), per-module
  coverage floors, runner selection, flaky-test governance, CI gating. Produces
  the policy that per-sprint plans inherit. [DOC]
- **unit-testing** — Jest/Vitest with Firebase mocking, TDD red-green-refactor,
  ≥80% diff coverage, sub-60s deterministic suites. [DOC]
- **e2e-testing** — Cypress/Playwright critical-journey tests via Page Object
  Model against the Firebase emulator, with visual assertions. [DOC]
- **bdd-full-spectrum** — runner-agnostic Gherkin across 11 quality angles
  (`@functional`, `@a11y`, `@security`, `@perf`, …) with traceability to FR/SC/P. [DOC]
- **cross-browser-testing** — per-engine (Blink/Gecko/WebKit) compatibility,
  feature detection, Autoprefixer/polyfill strategy, CI on three engines. [DOC]
- **performance-testing** — Lighthouse CI budgets, Core Web Vitals (LCP/INP/CLS)
  at p75, bundle-size caps, RUM. [DOC]

## When to use
- A request names a test type (unit, E2E/BDD, cross-browser, performance) or asks
  for a test plan / coverage gate. Single dimension → that topic; "what should we
  test / where to invest" → `test-strategy`. [INFERENCE]
- Skip when the ask is non-testing (build, deploy, lint) — route elsewhere. [INFERENCE]

## How it routes and executes
1. Infer `topic` from the request; ask only on genuine ambiguity between two enums. [DOC]
2. Map `topic` → `routes:` path in `SKILL.md`, Read that ONE file (never the cluster). [DOC]
3. `depth=deep` → apply the playbook exhaustively, verifying at each step;
   `quick` → essentials only. [DOC]
4. Run the Validate step before "done"; never assert green without evidence. [DOC]

### Disambiguation
- BDD scenarios driving a browser → `bdd-full-spectrum` (spec-first), not `e2e-testing`. [INFERENCE]
- Load/latency/throughput → `performance-testing`, even when framed as "E2E under load". [INFERENCE]
- "Increase coverage", no type named → `unit-testing` (the coverage gate lives there). [INFERENCE]

## Routes (playbooks)
- [test-strategy](references/test-strategy.md)
- [unit-testing](references/unit-testing.md)
- [e2e-testing](references/e2e-testing.md)
- [bdd-full-spectrum](references/bdd-full-spectrum.md)
- [cross-browser-testing](references/cross-browser-testing.md)
- [performance-testing](references/performance-testing.md)
- [verification-tags](../../references/verification-tags.md) — evidence-tag convention

## Gates
Constitution v6.0.0 enforcement, evidence tags (Alfa core set, EN spelling),
script-first rule. Exactly one playbook Read; `topic` set; `depth` respected;
Validate run before completion. [DOC]

## Supporting bundle
- `agents/` — lead, specialist, support, guardian role contracts.
- `knowledge/` — testing body-of-knowledge and concept graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — the routed deliverable scaffold.
- `assets/` — the quality rubric and routing checklist the gate runs against
  (see `assets/README.md`).
- `evals/evals.json` — routing and gate-discipline test cases.
