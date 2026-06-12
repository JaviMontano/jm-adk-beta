# Example output — product-analytics

## 1. Routing
- **Resolved topic:** `ab-testing` [CONFIG]
- **Depth:** `deep` (a ship decision with a guardrail). [INFERENCIA]
- **Why this route:** the question is "did the change work / can we ship?", not
  "where do users drop?" (funnel) or "what do we measure?" (kpi). [INFERENCIA]
- **Playbook read:** `references/ab-testing.md`

## 2. Verdict: NOT READY TO SHIP — peeking at 4 days [INFERENCIA]
"A bit higher after 4 days" is an interim read, not a result. Calling it now is
peeking and inflates false-positive risk. Hold for the pre-committed horizon. [DOC]

## 3. Metric contract
| Field | Value |
|---|---|
| Primary | signup_completion_rate = signups_completed / signups_started |
| Owner | one named decision owner (assign before launch) [SUPUESTO] |
| Guardrail | day1_retention_rate (must not regress) |
| Randomization unit | user_id (matches denominator) [DOC] |
| Method | two-proportion z-test, α=0.05 two-sided, fixed horizon [INFERENCIA] |

## 4. Sample size & duration [INFERENCIA]
Inputs: baseline 12%, MDE +1pp (12% → 13%), power 80%, α=0.05 two-sided.
A two-proportion z-test needs ~20k users per variant (~40k total). At ~6,000
signups-started/day split 50/50, that is ~7 days minimum — round up to a full
**14-day** cycle to absorb weekday/weekend seasonality. At day 4 the test has
seen well under half the required N. [INFERENCIA]
> Numbers are template estimates to execute in a tool, not validated results. [SUPUESTO]

## 5. Decision rule (set before reading data)
| Outcome | Condition | Action |
|---|---|---|
| Win | completion up, significant at horizon, retention not harmed | Ship 100% |
| Loss | completion flat/down, significant | Do not ship; archive learning |
| Inconclusive | CI spans MDE at 14 days | Do not extend silently; pre-commit ship-no |
| Guardrail harmed | day1_retention regresses | Block ship regardless of primary |
| Instrumentation failure | SRM, missing exposures | Invalidate; fix and rerun |

## 6. Validity threats to check before trusting the readout
- **SRM:** confirm the realized split ≈ 50/50 (chi-square p ≥ 0.01); a skewed
  split biases every metric. [INFERENCIA]
- **Novelty effect:** a two-step wizard may spike early then fade — the 14-day
  horizon helps absorb it. [INFERENCIA]
- **Exposure logging:** verify an `experiment_exposed` event fires at assignment,
  deduped per `user_id`. [DOC]

## 7. Validation gate
- [x] Exactly one playbook read (`ab-testing`); topic matches enum. [CONFIG]
- [x] Every numeric claim tagged; estimates marked as templates. [CONFIG]
- [x] No significance/lift claimed before horizon + method satisfied. [DOC]
- [x] No client PII in the deliverable. [CONFIG]

## 8. Residual risks
- Sample-size figures assume frequentist fixed-horizon; a sequential design
  changes the stopping logic and must be declared. [SUPUESTO]
