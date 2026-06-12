<!-- distilled from alfa skills/validar-liquidacion-co -->
<!-- This skill should be used when the user asks to validate a Colombian labor settlement calculation, recompute cesantias, intereses de cesantias, prima, vacaciones, deductions, net payment, or review paz y salvo questions with an arithmetic-only, evidence-backed report. -->
# Validar Liquidacion Co

## Purpose

Validate arithmetic in a Colombian labor settlement packet using supplied data only. Recompute cesantias, intereses de cesantias, prima, vacaciones, deductions, and net amount; list deviations and open questions; mark paz y salvo posture as arithmetic-only. [DOC]

This skill does NOT provide legal advice. It must recommend legal/accounting review for final decisions, especially when contract type, salary factors, indemnity, sanctions, collective agreements, or disputed facts are involved. [DOC]

**In scope:** arithmetic re-check of supplied figures; deviation and net-mismatch detection; structured open questions; safe paz y salvo posture. [DOC]
**Anti-scope (never do):** infer unsupplied factors; fetch legal tables; declare legal finality; automate signature; access payroll systems; opine on labor-law compliance. [DOC]

## Assumptions

- Inputs are already extracted/transcribed by the user or a prior step; this skill does not OCR or parse PDFs itself. [SUPUESTO] → verify: confirm each numeric input has an evidence ID before recomputing.
- `days_worked` is expressed in the Colombian 360-day commercial-year convention used by the formulas below; if the packet uses calendar days, results will diverge. [SUPUESTO] → verify: ask the user which day basis the packet uses.
- Salary bases are already consolidated (e.g., transport allowance already included or excluded per the packet). This skill never decides that treatment. [SUPUESTO] → verify: open a question if base composition is unstated.

## Deterministic Contract

Follow `assets/output-contract.json` and validate reports with `scripts/liquidacion_validator.py`. A valid report must include: [DOC]

- Currency `COP`. [DOC]
- Evidence records for input values and source documents. [DOC]
- `calculation_basis` with salary bases, days worked, and vacation basis. [DOC]
- Reported components and deductions. [DOC]
- Recomputed components using `assets/formula-policy.json`. [DOC]
- Tolerance from `assets/tolerance-policy.json`. [DOC]
- `paz_y_salvo` posture from `assets/paz-y-salvo-policy.json`. [DOC]
- Validation flags: `offline=true`, `network_used=false`, `not_legal_advice=true`, `legal_review_recommended=true`. [DOC]

## Formula Policy

Deterministic formulas, for arithmetic checking ONLY (not legal entitlement determination): [DOC]

- `cesantias = salary_base_prestaciones * days_worked / 360`
- `intereses_cesantias = cesantias * 0.12 * days_worked / 360`
- `prima = salary_base_prestaciones * days_worked / 360`
- `vacaciones = salary_base_vacaciones * vacation_days / 30` when vacation days are supplied
- otherwise `vacaciones = salary_base_vacaciones * days_worked / 720`

Do not infer salary factors, contract type, transport allowance treatment, indemnity, sanctions, or deductions that are not supplied. [DOC]

**Worked example** (illustrative; values are user-supplied evidence, not legal guidance): base_prestaciones = 2,000,000 COP, days_worked = 180. [SUPUESTO]
- cesantias = 2,000,000 × 180 / 360 = 1,000,000
- intereses_cesantias = 1,000,000 × 0.12 × 180 / 360 = 60,000
- prima = 2,000,000 × 180 / 360 = 1,000,000
- vacaciones (no vacation_days) = 2,000,000 × 180 / 720 = 500,000
If the packet reports cesantias = 1,050,000, flag a +50,000 deviation (exceeds COP tolerance) as `[OPEN]`, not as an error of fact. [INFERENCIA]

## Workflow

1. Inventory supplied documents and assign evidence IDs such as `E-001`. [DOC]
2. Extract numeric inputs exactly as supplied: salary bases, days, vacation days, reported components, deductions, reported net. [DOC]
3. Validate all amounts are COP and non-negative. [DOC]
4. Recompute components with the formula policy and tolerance. [DOC]
5. Compare reported component amounts and net amount. [DOC]
6. Create open questions for missing basis, unclear deductions, disputed vacation days, or paz y salvo uncertainty. [DOC]
7. Use `sign_under_reservation` or `do_not_sign_yet` when questions remain. [DOC]
8. Validate the JSON report with `scripts/liquidacion_validator.py`. [DOC]

## Edge Cases

- **Missing salary base:** do not assume one. Emit `[OPEN]` and `do_not_sign_yet`; skip the dependent component. [INFERENCIA]
- **vacation_days supplied AND a /720 prorate also present:** prefer the explicit `/30` formula; flag the inconsistency. [INFERENCIA]
- **Reported net present but components absent:** validate net is COP and non-negative; cannot reconcile — raise `[OPEN]`. [INFERENCIA]
- **Deviation exactly at tolerance boundary:** treat as within tolerance (inclusive), per `tolerance-policy.json`. [SUPUESTO] → verify: confirm boundary handling in the policy file.
- **Negative or non-COP amount:** hard reject; the validator must fail. [DOC]

## Output Rules

- Tag report claims with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]` (content provenance of each reported figure). [DOC]
- Tag this reference's own claims with the Alfa core set (`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`); never mix tag families in one document. [DOC]
- State arithmetic result separately from legal conclusion. [DOC]
- Never say a settlement is legally final, safe to sign, or fully compliant. [DOC]
- Never use web, payroll systems, or current legal tables unless the user supplies them as evidence. [DOC]
- Never touch or depend on `firma-pdf-legal`; signature automation remains out of scope. [DOC]

## Assets

- `assets/manifest.json` lists deterministic assets. [DOC]
- `assets/output-contract.json` defines the report shape. [DOC]
- `assets/formula-policy.json` defines formulas used by the offline validator. [DOC]
- `assets/tolerance-policy.json` defines COP rounding tolerance. [DOC]
- `assets/evidence-policy.json` defines allowed evidence and required fields. [DOC]
- `assets/paz-y-salvo-policy.json` defines safe recommendations when questions remain. [DOC]
- `assets/legal-boundary-policy.json` defines no-legal-advice blockers. [DOC]

## Scripts

Run: [DOC]

```bash
python3 skills/validar-liquidacion-co/scripts/liquidacion_validator.py --input <report.json>
bash skills/validar-liquidacion-co/scripts/check.sh
```

The validator is offline and rejects missing evidence, non-COP currency, negative amounts, component deviations beyond tolerance, net mismatches, unsafe paz y salvo posture, network use, and legal-final language. [DOC]

## Failure Modes (what a wrong run looks like)

- Silent auto-fill of a missing base instead of `[OPEN]` → produces a confident but unfounded net. Guard: step 6 must run before any recompute on incomplete data. [INFERENCIA]
- Tag-family mixing (`{SUPUESTO}` next to `[DOC]`) → breaks scannability and the single-family rule. [DOC]
- "Safe to sign" phrasing leaking from arithmetic agreement → validator rejects legal-final language. [DOC]
- Using `/720` when `vacation_days` exist → understates vacaciones; caught by the edge-case rule above. [INFERENCIA]

## Acceptance Criteria

- Every reported figure carries exactly one of `[EXPLICIT]`/`[INFERRED]`/`[OPEN]`; every reference claim carries one Alfa-core tag. [DOC]
- All amounts COP and non-negative; flags `offline/not_legal_advice/legal_review_recommended` set true; `network_used=false`. [DOC]
- Each deviation beyond tolerance and each net mismatch has a matching open question and a non-`signed` paz y salvo posture. [DOC]
- `scripts/liquidacion_validator.py` exits clean on the produced report. [DOC]

## Related Skills

- `negociacion-oferta`
- `proceso-seleccion-orchestrator`

## Stop Conditions

Stop when the user asks for legal certainty, signature automation, litigation advice, payroll-system access, or a final compliance opinion without professional review. [DOC]
