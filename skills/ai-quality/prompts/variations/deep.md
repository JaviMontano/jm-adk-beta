# Deep Variation — ai-quality (depth=deep)

Exhaustive path: resolve one topic, read its playbook, execute every step with
verification, and run the full gate. Use for production-critical, regulated,
irreversible, or high-stakes artifacts.

## Steps
1. Resolve `topic` (one enum); record the rejected near-collisions and why. [INFERENCIA]
2. Read only that playbook — still one, never the cluster.
3. Execute with **verification at each step**:
   - `ai-testing-strategy` → give all 36 matrix cells a verdict; design
     training-serving skew on identical entities; pick the fairness metric by
     domain harm and document rejected metrics. [CÓDIGO]
   - `llm-evaluation` → versioned eval set + model + prompt hash + dataset hash;
     baseline reported; human-spot-check ≥20 items or all failures; disclose the
     judge config. [CÓDIGO]
   - `ai-assisted-testing` → tests + bounded fuzz (seed/iters/timeout) + mutation
     (baseline, operators, kill criteria, surviving-mutant handling); per-module
     coverage floors. [CÓDIGO]
   - `ai-code-review` / `code-review` → full category sweep incl. error paths and
     contract/test gaps; executed commands for any pass/fail claim; gapless IDs;
     decision = worst severity. [CÓDIGO]
   - `ai-safety` → full risk→control→jailbreak→metric chains, no orphan ids,
     escalation owner/channels/criteria. [INFERENCIA]
   - `ai-content-detection` → ≥2 concordant signals before a non-inconclusive
     label; contradictory signals lower confidence; human-review gate for
     enforcement. [INFERENCIA]
   - `ai-documentation` → evidence id per section, drift audit, `[OPEN]` for
     unverifiable, safe paths. [CONFIG]
   - `ai-workflow-automation` → gate-before-effect, bounded retries+fallback,
     input/output contracts on every AI step, no circular handoff. [INFERENCIA]
4. Run the topic's `scripts/check.sh` (offline) and the full router + topic gate.

## Discipline
- Verify, don't assume: each step's output is checked before the next begins. [DOC]
- A `deep` run that skips verification is just a slow `quick` run — that is a
  failure, not a style choice. [INFERENCIA]
- Green = well-formed, never safe/correct. State residual risk explicitly. [INFERENCIA]
