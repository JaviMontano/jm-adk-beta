# Estimation Integrity — the universal method

Constitution **Principle 8** in practice. An estimate is a computed, sourced, auditable
figure — not a number pulled from intuition or inferred from token counts. This is how
the harness estimates effort for both personas: the vibe coder sizing a build, the
knowledge worker sizing a research effort. [DOC]

## The rule
> Decompose → compute → cite → tag confidence. Skip any step and it is a guess, not an estimate. [DOC]

A figure with no decomposition behind it, or no source per part, is rejected — the same
way untested code and an unsourced claim are rejected. [CONFIG]

## Method

1. **Decompose** the work into atomic tasks (Constitution Principle 1). A task you cannot
   bound is too big — split it until you can give it three points. [DOC]
2. **Source each task's three points** (`optimistic`, `likely`, `pessimistic`) and record WHERE
   they come from — the `basis`:
   - `measured` — a timed prior run or log. Highest trust. [DOC]
   - `analogy` — a comparable past task; name the analog. [INFERENCE]
   - `expert` — a named person's judgment, unverified. Lowest trust; the tool widens its band. [ASSUMPTION]
3. **Compute**, do not eyeball — run the script:
   ```bash
   python3 scripts/estimate.py --tasks tasks.json        # JSON in, JSON out
   python3 scripts/estimate.py --tasks tasks.json --format text
   python3 scripts/estimate.py --selftest                # built-in fixture
   ```
   Per task it applies three-point PERT (`expected = (o + 4·likely + p) / 6`); it sums the
   expecteds and combines the spreads (root-sum-square) into a **P10–P90 band** and a
   confidence label (`high`/`medium`/`low`) from the band-to-size ratio. [CODE]
4. **Tag confidence and assumptions** on the way out. The script emits both; carry them into
   the deliverable. A point number with no band is dishonest. [DOC]

## Units, not currency
Effort is reported in caller-chosen **work units** — hours, story-points, days — never money.
Whether effort converts to a price, and in what currency, is decided by the **active profile**
(`profiles/`), not here. A commercial profile may forbid client-facing prices entirely; a solo
builder may price freely. Core only insists the underlying effort was *computed*. [CONFIG]

## Anti-patterns (rejected)
- "About a week" with no task list. [ASSUMPTION] → decompose first.
- Estimating from token counts, line counts, or model output length. [INFERENCE] → irrelevant to human/system effort.
- A single point with no band. [DOC] → always emit P10–P90.
- A task with no `source`. [CONFIG] → `estimate.py` exits non-zero.

## Input shape
```json
{ "unit": "hours",
  "tasks": [
    { "id": "T1", "desc": "scaffold module", "basis": "measured",
      "source": "prior run log 2026-05", "optimistic": 1, "likely": 2, "pessimistic": 4 }
  ] }
```

## Limits
- Independence is assumed when combining spreads; correlated risk (one blocker stalls many
  tasks) makes the true band wider — note it explicitly when tasks share a dependency. [ASSUMPTION]
- PERT assumes a unimodal task duration; bimodal tasks ("trivial OR a rabbit hole") should be
  split into the two scenarios and weighted, not averaged. [INFERENCE]
- The tool computes; it does not invent the three points. Garbage in, garbage out — which is
  why every point is sourced and auditable. [DOC]

See `scripts/estimate.py` for the implementation and `--selftest` for a worked example.
