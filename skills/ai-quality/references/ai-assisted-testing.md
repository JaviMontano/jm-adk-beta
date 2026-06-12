<!-- distilled from alfa skills/ai-assisted-testing -->
<!-- > -->
# Ai Assisted Testing
> "Method over hacks."
## TL;DR
AI-proposed test cases, fuzzing, mutation testing, and coverage optimization — every artifact carries target, rationale, oracle, evidence, and an execution status. AI proposes; the gate is determinism, not volume. [EXPLICIT]

Use the deterministic assets in `assets/` for test taxonomy, evidence rules, fuzzing, mutation, coverage, and report shape. When producing a JSON assisted-testing plan, validate it offline (no network, no wall-clock, no RNG) with `bash skills/ai-assisted-testing/scripts/check.sh`. [EXPLICIT]

## Scope & Anti-Scope
- IN: generating/justifying tests, bounded fuzz and mutation specs, coverage targeting, and a validated plan. [EXPLICIT]
- OUT: executing tests in prod, mutating shared/stateful systems, generating tests that assert on non-deterministic output without a stable oracle, replacing human review of safety-critical paths. Route these elsewhere or escalate. [EXPLICIT]

## Procedure
1. **Discover** — gather code, requirements, existing suite, coverage baseline. Missing baseline → measure it first, don't guess. [EXPLICIT]
2. **Analyze** — evaluate options per Constitution XIII/XIV; pick oracle type per test (see Decisions). [EXPLICIT]
3. **Execute** — emit artifacts with evidence tags and status `proposed`. [EXPLICIT]
4. **Validate** — run `scripts/check.sh`; confirm every Quality Criterion before handoff. [EXPLICIT]

## Status State Machine
`proposed` → `generated` (code written) → `executed` (run, result recorded). Never mark `executed` without a captured pass/fail; never skip `generated`. A failing `executed` test is a valid, kept outcome — not a defect to delete. [EXPLICIT]

## Decisions & Trade-offs
- **Oracle choice.** Prefer assertion/known-answer oracles; use metamorphic relations when no ground truth exists; use property invariants for fuzz targets. Snapshot oracles are last resort — they encode current behavior as "correct," masking bugs. [EXPLICIT]
- **Fuzz vs. mutation budget.** Fuzzing finds input-handling gaps; mutation testing finds weak assertions. Spend on mutation first when coverage is high but defects still escape — high coverage with low mutation-kill is false confidence. [EXPLICIT]
- **Coverage thresholds** are per-module, not global. A 90% global average can hide a 0%-covered critical path; set floors on the modules that matter. [EXPLICIT]

## Quality Criteria
- [ ] Every generated test has target, rationale, oracle, and evidence tag. [EXPLICIT]
- [ ] Oracle is explicit and deterministic; non-deterministic targets use a metamorphic/property oracle, never a bare equality check. [EXPLICIT]
- [ ] Fuzzing proposals are bounded by domain, seed, iterations, timeout, and safety scope (no network/filesystem/prod side effects). [EXPLICIT]
- [ ] Mutation testing includes baseline, operators, kill criteria, and explicit surviving-mutant handling (kill, justify as equivalent, or accept-with-reason). [EXPLICIT]
- [ ] Coverage plan names target files/modules and per-module thresholds. [EXPLICIT]
- [ ] Execution status distinguishes `proposed`, `generated`, and `executed`. [EXPLICIT]
- [ ] JSON plan passes `scripts/check.sh` when produced. [EXPLICIT]

## Worked Example (plan fragment)
```json
{
  "tests": [{
    "target": "billing.apply_discount",
    "rationale": "boundary: discount at 0% and 100% must not invert sign",
    "oracle": {"type": "property", "invariant": "0 <= net <= gross"},
    "evidence": "[EXPLICIT]",
    "status": "proposed"
  }],
  "fuzz": [{
    "target": "parse_currency", "domain": "utf8-string",
    "seed": 42, "iterations": 10000, "timeout_s": 30,
    "safety_scope": "pure-function, no IO"
  }],
  "mutation": {
    "baseline_coverage": 0.87, "operators": ["AOR", "ROR", "negate-cond"],
    "kill_criterion": "test suite fails on mutant",
    "surviving_mutant_handling": "review: kill or mark equivalent with reason"
  },
  "coverage": {"targets": {"billing/core.py": 0.95, "billing/io.py": 0.80}}
}
```

## Usage
Example invocations:
- "/ai-assisted-testing" — Run the full ai assisted testing workflow
- "ai assisted testing on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs); without them, output is `proposed`-only and unrunnable. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions or safety-critical sign-off. [EXPLICIT]
- AI-generated assertions can encode the same misunderstanding as the code under test; mutation testing is the guard against tautological tests. [EXPLICIT]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No coverage baseline | Measure baseline before proposing thresholds |
| Non-deterministic target (time, RNG, network) | Require seam/seed/mock; refuse bare equality oracle |
| 100% coverage, escaping defects | Pivot budget to mutation testing — coverage is saturated, assertions are weak |
| Fuzz crash unreproducible | Capture failing seed + input corpus; without repro, downgrade to `proposed` |
| All mutants survive | Suite asserts nothing meaningful — block handoff, flag as critical |
