<!-- distilled from alfa skills/ai-safety -->
<!-- > -->
# AI Safety

## TL;DR

Produce a source-backed AI safety report: risk taxonomy, control coverage,
jailbreak tests, evaluation metrics, escalation policy, residual risks. Output
is a packet validated offline against fixed JSON contracts — not a live-model
attestation. [EXPLICIT]

## Inputs & Assumptions

- Required inputs: system description, user groups, deployment context, the five
  `assets/*.json` policy files. Missing any policy file is `[VACIO_CRITICO]` —
  stop and ask, never invent risk/control taxonomies. [INFERENCIA]
- Assumes the asset JSONs are the authority; if the system has a harm domain not
  in `risk-taxonomy.json`, flag it and propose a taxonomy extension rather than
  forcing a near-match. [SUPUESTO]
- One brand/system per report; do not merge two systems' risk surfaces. [INFERENCIA]

## Procedure

### Step 1: Scope The System
- Identify use case, user groups, high-stakes status, known harm domains. [EXPLICIT]
- Create evidence ids before recommending controls (id-first: a control with no
  upstream risk id is orphaned and fails the gate). [EXPLICIT]

### Step 2: Assess Risks
- Classify each risk using `assets/risk-taxonomy.json`. [EXPLICIT]
- Assign severity and scenario text; do not collapse critical risks into generic
  warnings. A vague "may produce harmful output" is non-actionable. [EXPLICIT]

### Step 3: Map Controls
- Map every risk id to >=1 control from `assets/control-policy.json`. [EXPLICIT]
- Critical risks cannot use `allow` as the only action — pair with `block`,
  `escalate`, or `human-review`. [EXPLICIT]

### Step 4: Test And Evaluate
- Define jailbreak tests from `assets/jailbreak-policy.json`. [EXPLICIT]
- Define evaluation metrics from `assets/evaluation-policy.json`. [EXPLICIT]
- Run `bash skills/ai-safety/scripts/check.sh` when scripts are present. [EXPLICIT]

## Worked Example (minimal)

Customer-support chatbot, harm domain `medical-advice` (severity: critical):
risk `r-med-01` → control `c-block-med` (`block` + `escalate` to human owner);
jailbreak `j-roleplay-01` ("pretend you are a doctor") → expected `refuse`;
metrics: unsafe-recall, over-refusal, jailbreak-block-rate. Result: every id
chains risk → control → test → metric with no orphans. [INFERENCIA]

## Quality Criteria

- [ ] Evidence ids support risks, controls, tests, metrics, and escalation. [EXPLICIT]
- [ ] Every risk has >=1 mapped control. [EXPLICIT]
- [ ] Jailbreak coverage exists for any jailbreak or prompt-injection risk. [EXPLICIT]
- [ ] Evaluation includes unsafe recall, over-refusal, and jailbreak block rate. [EXPLICIT]
- [ ] Escalation policy has owner, channels, and criteria. [EXPLICIT]
- [ ] No critical risk relies on `allow` alone. [INFERENCIA]

## Failure Modes & Edge Cases

- Over-refusal: controls so aggressive that benign requests get blocked — the
  over-refusal metric is the guardrail; a high block rate is NOT success. [INFERENCIA]
- Orphan ids: a control/test/metric with no upstream risk id, or a risk with no
  downstream control — both fail the gate; reconcile before "done". [INFERENCIA]
- Taxonomy drift: inventing a severity or action absent from the policy JSONs
  silently breaks `validate_ai_safety_report.py`. Use only enumerated values. [SUPUESTO]
- Green-washing: a passing validator means the packet is well-formed, not that
  the live model is safe — never report it as a safety guarantee. [INFERENCIA]

## Deterministic DoD Assets

- `assets/safety-report-contract.json` — report schema and required checks. [EXPLICIT]
- `assets/risk-taxonomy.json` — harm domains and severity values. [EXPLICIT]
- `assets/control-policy.json` — allowed control types and actions. [EXPLICIT]
- `assets/jailbreak-policy.json` — allowed attack types and expected actions. [EXPLICIT]
- `assets/evaluation-policy.json` — required safety metrics. [EXPLICIT]
- `scripts/validate_ai_safety_report.py` — validates fixtures offline. [EXPLICIT]

## Limits (anti-scope)

- Designs and validates safety report packets offline only. [EXPLICIT]
- Does not certify a live model as safe, nor run the model under test. [EXPLICIT]
- Does not replace red-teaming, pentest, or production monitoring. [INFERENCIA]
- Legal, medical, financial, or emergency escalation requires human owner
  review — the packet routes, it does not decide. [EXPLICIT]
