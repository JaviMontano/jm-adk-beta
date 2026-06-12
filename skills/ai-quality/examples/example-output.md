# Example Output — ai-quality

Routing-and-execution record for the bundled request in `example-input.md`.

## 1. Request summary
- **Request:** Assess Claude-generated pytest cases for `pricing/discount.py`,
  and separately judge whether the PR's docstrings are AI boilerplate.
- **Artifact under review:** PR diff (`pricing/discount.py`, `tests/test_discount.py`).
- **Stakes / reversibility:** moderate, ships to staging not prod → low-stakes. [CONFIG]

## 2. Routing decision
| Field | Value | Tag |
|-------|-------|-----|
| Resolved `topic` | `ai-assisted-testing` | [CÓDIGO] |
| `depth` | `quick` (moderate stakes, staging) | [CONFIG] |
| Playbook read | `references/ai-assisted-testing.md` (only) | [CÓDIGO] |
| Justification | The actionable, blocking concern is whether the generated tests actually verify behavior; the docstring question is informational and reversible. | [INFERENCIA] |
| Rejected near-collision | `ai-content-detection` for the docstrings — split into a **second, separate** run; not co-loaded, to avoid cross-topic bleed. | [INFERENCIA] |

> Router note: two intents → two topics. Primary resolved now; the docstring
> detection is handed back as a follow-up route, not merged into this answer. [DOC]

## 3. Spine execution (ai-assisted-testing, quick)
- **Discover:** No coverage baseline exists for `pricing/` → measure it first,
  do not guess a threshold. [CÓDIGO]
- **Analyze:** The 7 generated tests assert on `apply_discount` return values.
  Oracle risk: an AI-generated assertion can encode the same misunderstanding as
  the code under test → a property oracle is needed on the boundary, plus
  mutation testing to catch tautological assertions. [INFERENCIA]
- **Execute (plan fragment, status `proposed`):**

```json
{
  "tests": [{
    "target": "pricing.discount.apply_discount",
    "rationale": "boundary: 0% and 100% discount must keep 0 <= net <= gross",
    "oracle": {"type": "property", "invariant": "0 <= net <= gross"},
    "evidence": "[CÓDIGO]",
    "status": "proposed"
  }],
  "mutation": {
    "baseline_coverage": null,
    "operators": ["AOR", "ROR", "negate-cond"],
    "kill_criterion": "suite fails on mutant",
    "surviving_mutant_handling": "review: kill or mark equivalent with reason"
  },
  "coverage": {"targets": {"pricing/discount.py": 0.90}}
}
```

  `baseline_coverage` is `null` until measured — recorded as a gap, not invented. [CÓDIGO]

## 4. Deliverable (verdict)
- 5 of 7 generated tests assert concrete return values (good); 2 are snapshot-
  style (`assert result == <captured>`), which encode current behavior as
  "correct" and mask bugs → flag for an explicit oracle. [CÓDIGO]
- Mutation run recommended before relying on the suite: high coverage with low
  mutation-kill would be false confidence. [INFERENCIA]

## 5. Validation gate
- [x] Resolved topic ∈ enum; exactly one playbook read. [CÓDIGO]
- [x] One Alfa family throughout; no `[CÓDIGO]` without an inspected referent. [DOC]
- [x] `quick` stayed at essentials (highest-risk targets, no full fuzz sweep). [CONFIG]
- [x] Every proposed test has target/rationale/oracle/evidence; status `proposed`. [CÓDIGO]
- [ ] `scripts/check.sh` — to run when the JSON plan is finalized. [DOC]
- **Gate verdict:** `warn` — 2 snapshot oracles must be replaced before merge. [DOC]

## 6. Risks & limits
- Quick mode triaged the highest-risk targets only; not a clean bill of health
  for the whole module. [DOC]
- The docstring AI-detection question is unanswered here **by design** — route it
  to a separate `ai-content-detection` run; a passing test plan says nothing
  about authorship. [INFERENCIA]
