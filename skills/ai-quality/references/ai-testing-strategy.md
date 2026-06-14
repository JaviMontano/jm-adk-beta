<!-- distilled from alfa skills/ai-testing-strategy -->
<!-- > -->
# AI Testing Strategy: Comprehensive Verification for AI-Enabled Systems

AI testing strategy defines how to verify that an AI system behaves correctly, fairly, securely, and reliably across all layers — from data ingestion through model inference to production monitoring. This skill produces a testing strategy document covering the testing scope matrix, model and prediction tests, data quality tests, compliance and fairness tests, integration approaches, and CI/CD test automation for AI pipelines. [EXPLICIT]

## Deterministic Hardening Contract

This skill must produce a testing strategy that can be checked offline without network, wall-clock, or random dependencies. Use the assets in `assets/` as the contract source before writing the final report:

- `assets/testing-strategy-contract.json`: required report sections and validation checks.
- `assets/matrix-policy.json`: canonical test types, layers, priorities, and matrix coverage rule.
- `assets/model-test-policy.json`: required model and prediction test categories.
- `assets/data-quality-policy.json`: required data quality and pipeline test categories.
- `assets/fairness-compliance-policy.json`: required fairness, privacy, audit, and governance tests.
- `assets/automation-policy.json`: automation tiers, CI/CD gates, and post-deploy monitoring expectations.
- `assets/evidence-policy.json`: allowed evidence tags and provenance rules.

If a JSON testing strategy is requested or used as an intermediate handoff, validate it with `scripts/validate_ai_testing_strategy.py`. The fixture smoke test is `bash skills/ai-testing-strategy/scripts/check.sh`. [EXPLICIT]

## Principio Rector

**Si no puedes probarlo, no lo despliegues.** En sistemas de IA, "funciona en mi notebook" no es evidencia de calidad. La estrategia de testing debe cubrir las 6 capas del sistema y los 6 tipos de prueba, con automatización como requisito, no como aspiración.

### Filosofía de Testing para IA

1. **La matriz completa o nada.** Testing parcial en sistemas de IA es peor que no testear — da falsa confianza. Un modelo con 95% accuracy pero sin fairness testing puede ser discriminatorio. Un pipeline con integration tests pero sin data quality tests puede procesar basura silenciosamente. [EXPLICIT]
2. **Data quality testing ES el test más importante.** En sistemas tradicionales, los bugs están en el código. En sistemas de IA, los bugs están en los datos. Schema validation, distribution testing, lineage tracking, y training-serving skew detection son la primera línea de defensa. [EXPLICIT]
3. **Testing continuo, no testing puntual.** Los modelos degradan con el tiempo (drift). Los datos cambian. Las features evolucionan. La estrategia de testing debe incluir monitoreo continuo en producción, no solo gates en el pipeline de deployment. [EXPLICIT]

## Inputs

The user provides a system or project name as `$ARGUMENTS`. Parse `$1` as the **system/project name** used throughout all output artifacts. [EXPLICIT]

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso`
- `{FORMATO}`: `markdown` (default) | `html` | `dual`
- `{ALCANCE}`: `ejecutiva` (~40% — S1 matrix + S2 model testing + S6 automation) | `técnica` (full 6 sections, default)

Before generating testing strategy, detect the codebase context:

```
Detección automática de contexto:
  Escanear el codebase por frameworks de testing (pytest, unittest, Great Expectations,
  deepchecks), herramientas CI/CD (GitHub Actions, Jenkins, GitLab CI), y monitoring
  (Evidently, WhyLabs, Prometheus) para adaptar recomendaciones. [EXPLICIT]
```

If reference materials exist, load them:

```
Load references:
  ${CLAUDE_SKILL_DIR}/references/testing-matrix.md
  ${CLAUDE_SKILL_DIR}/references/ai-test-types.md
  ${CLAUDE_SKILL_DIR}/references/integration-approaches.md
```

---

## When to Use

- Defining a comprehensive testing strategy for new or existing AI systems
- Designing model validation tests (accuracy, fairness, robustness, explainability)
- Planning data quality tests for AI pipelines (schema, distribution, lineage)
- Implementing compliance and fairness testing (bias detection, audit trails, governance)
- Selecting integration testing approaches for AI systems (top-down, bottom-up, parallel, harness)
- Automating AI tests within CI/CD pipelines
- Evaluating test coverage gaps in existing AI systems

## When NOT to Use

- Internal module structure and layer architecture -> **metodologia-ai-software-architecture**
- CONOPS and operational concept -> **metodologia-ai-conops**
- Pipeline design and CI/CD deployment strategy -> **metodologia-ai-pipeline-architecture**
- Design pattern selection -> **metodologia-ai-design-patterns**
- GenAI/LLM-specific testing (hallucination, RAG quality) -> **metodologia-genai-architecture**
- Traditional software testing without AI context -> **metodologia-testing-strategy**

---

## Delivery Structure: 6 Sections

### S1: Testing Scope Matrix

Defines the complete testing landscape across 6 test types and 6 system layers. [EXPLICIT]

**Test types:**
- **Functional**: Correctness of predictions, transformations, orchestration, and data flows
- **Performance**: Latency, throughput, resource utilization across all layers
- **Security**: Input validation, access controls, encryption, adversarial protection
- **Compliance**: Governance workflows, audit trails, data privacy, regulatory adherence
- **Fairness**: Demographic parity, equal opportunity, disparate impact, explanation equity
- **Integration**: Cross-component contracts, stage-to-stage data flow, end-to-end paths

**Layers:**
- UI, API, Pipeline Ops, Model Processing, Data Management, Infrastructure

**Key decisions:**
- Which cells in the matrix are mandatory vs. aspirational for current maturity
- Test priority ordering based on system risk profile
- Coverage target per cell (percentage of scenarios tested)

**Acceptance criteria:** every one of the 36 cells carries an explicit verdict — `mandatory`, `aspirational`, or `N/A` with a one-line exclusion reason. No cell is left blank. At least the Data Management × Functional and Model Processing × Fairness cells are `mandatory` for any production system. [EXPLICIT]

**Worked example (fraud-scoring API):** the highest-priority cell is `Model Processing × Fairness` (regulatory exposure under disparate-impact law), not `API × Functional` (which most teams reflexively test first). Risk-ordering surfaces this; alphabetical or layer-ordering hides it. [EXPLICIT]

**Failure modes this section prevents:**
- *Coverage theater* — a high cell count with all targets at 5%, giving false confidence. Mitigation: coverage target per cell is mandatory metadata, not optional. [EXPLICIT]
- *Silent N/A* — cells excluded without reason, indistinguishable from cells forgotten. Mitigation: every `N/A` records a reason. [EXPLICIT]

### S2: Model & Prediction Testing

Defines tests that verify model behavior, accuracy, robustness, and regression safety. [EXPLICIT]

**Test categories:**
- **Accuracy & metrics**: Holdout evaluation, slice-based analysis, calibration testing, threshold sensitivity
- **Adversarial testing**: Input perturbation, boundary testing, evasion attacks, data poisoning detection
- **Concept drift simulation**: Synthetic drift injection, detection delay measurement, retraining trigger verification
- **Counterfactual testing**: Feature sensitivity analysis, explanation consistency, actionable recourse
- **Regression testing**: Version-over-version comparison, no-regression gates, Champion vs. Challenger metrics

**Metric thresholds** (from requirements framework):
- AP-7: Model accuracy >= .88 (threshold), >= .94 (objective)
- AP-8: AUC >= .90 (threshold), >= .95 (objective)
- AP-11: Fairness parity >= 90% (threshold), >= 95% (objective)
- AP-13: Robustness to perturbation: +/-10% accuracy change (threshold), +/-5% (objective)

**Key decisions:**
- Test dataset management (static holdout vs. rolling window vs. both)
- Adversarial testing scope (automated tools vs. red team vs. both)
- Regression gate strictness (any degradation blocks vs. threshold-based)

**Acceptance criteria:** holdout never overlaps training rows (verified by hash join, not assumed); slice analysis covers every fairness-relevant segment from S4; each AP threshold maps to exactly one automated assertion in S6. A passing aggregate metric with a failing slice fails the gate. [EXPLICIT]

**Trade-off — "any degradation blocks" vs. threshold-based regression gate:** strict blocking guarantees no quality loss but stalls on metric noise (a 0.1% accuracy wobble from a reshuffled holdout halts release); threshold-based ships faster but can normalize slow erosion. Decision rule: use threshold-based with a *confidence interval* on the metric, not a raw delta — block only when the degradation exceeds the holdout's measurement noise. [EXPLICIT]

**Edge case — metric improves overall but degrades on a protected slice:** treat as a regression, not a pass. Aggregate-only gates are the most common way fairness regressions reach production. [EXPLICIT]

### S3: Data Quality & Pipeline Testing

Defines tests for data integrity, feature quality, and pipeline reliability. [EXPLICIT]

**Data quality tests:**
- Schema validation (types, formats, ranges, cardinality)
- Distribution testing (KS test, PSI against reference distributions)
- Missing value and outlier handling verification
- Lineage tracking completeness and queryability

**Feature quality tests:**
- Training-serving skew detection (compare training feature computation vs. serving)
- Feature freshness within SLA
- Feature coverage (percentage of predictions with all features)
- Feature importance stability across retraining cycles

**Pipeline tests:**
- Stage-to-stage data contracts (schema, types, ranges)
- Error propagation and retry behavior
- Checkpoint/restart from failed stage
- Pipeline execution time against SLA (AP-1, AP-2 thresholds)

**Key decisions:**
- Data quality tool selection (Great Expectations, deepchecks, Pandera, custom)
- Reference distribution management (when to update reference baselines)
- Contract testing scope (which stage boundaries need contracts)

**Acceptance criteria:** schema validation runs on *serving* inputs, not only training data; PSI/KS thresholds are set per-feature (a low-cardinality categorical and a heavy-tailed numeric need different bands); training-serving skew is measured on the *same* feature for the *same* entity, not on aggregate distributions. [EXPLICIT]

**Worked example — training-serving skew:** training computes `days_since_last_login` from a nightly batch (as-of midnight); serving computes it live. The distributions look identical, but per-request the serving value is hours fresher, shifting the decision boundary. The skew test must compare the two computations on identical entities at identical timestamps, or it reports a false pass. [EXPLICIT]

**Failure modes:**
- *Baseline staleness* — a reference distribution frozen at launch flags legitimate seasonal change as drift, training the team to ignore alerts. Mitigation: scheduled baseline review cadence is a named decision above, not an afterthought. [EXPLICIT]
- *Silent garbage-in* — a column flips from cents to dollars; schema (still numeric) passes, predictions degrade. Distribution testing, not schema testing, is the catch — both are mandatory. [EXPLICIT]

### S4: Compliance, Fairness & Ethics Testing

Defines tests for regulatory adherence, bias detection, and ethical AI operation. [EXPLICIT]

**Compliance tests:**
- Model governance workflow verification (approval gates, documentation requirements)
- Audit trail completeness (decision logging, immutability, queryability)
- Data privacy (PII detection, masking, consent tracking, right-to-deletion)
- Encryption verification (at rest CP-3, in use CP-4)
- Retention policy enforcement (CP-2: financial transaction archival)

**Fairness tests:**
- Demographic parity across protected groups
- Equal opportunity (true positive rate consistency)
- Disparate impact ratio (four-fifths rule)
- Intersectional analysis (combinations of protected attributes)
- Calibration fairness (confidence scores accurate across groups)

**Explainability tests:**
- Every prediction generates explanation within latency budget
- Explanation consistency (similar inputs produce similar explanations)
- Explanation completeness (top-N features cover >80% prediction weight)
- AP-12: Explainability score >= 0.7 (threshold), >= 0.8 (objective)

**Key decisions:**
- Protected attributes definition (which groups to test fairness across)
- Fairness metric selection (which fairness definition applies to this domain)
- Compliance framework mapping (GDPR, HIPAA, SOX, PCI-DSS requirements per test)

**Trade-off — fairness metrics are mutually exclusive:** demographic parity and equal opportunity cannot both hold unless base rates are equal across groups (impossibility result). Picking "all of them" is not a strategy; it guarantees a failing gate. Decision rule: choose the metric whose error type carries the domain's real-world harm — equal opportunity (false-negative parity) for medical screening, predictive parity for lending. Document the *rejected* metrics and why. [EXPLICIT]

**Acceptance criteria:** protected attributes come from the business in writing — never inferred by the system; each compliance requirement (CP-2, CP-3, CP-4) maps to at least one executable test, not a checklist tick; audit-trail tests verify *immutability*, not just presence (a writable log is not an audit trail). [EXPLICIT]

**Edge case — small protected subgroup:** an intersectional cell (e.g. group A × region B) with 12 samples yields a fairness ratio with a confidence interval spanning 0.4–1.6. Report the interval and flag "insufficient power," do not report a point estimate that reads as a pass or fail. [EXPLICIT]

**Failure mode:** *proxy leakage* — a removed protected attribute re-enters via a correlated feature (zip code ≈ race). Fairness tests on the protected attribute pass while the model still discriminates. Mitigation: test fairness on outcomes, not on whether the attribute is a model input. [EXPLICIT]

### S5: Integration Approaches & Harness Design

Selects the integration testing strategy and designs the test harness for end-to-end validation. [EXPLICIT]

**Approaches:**
- **Top-Down**: Start from API, stub model and data, progressively replace. Best for user-facing systems.
- **Bottom-Up**: Start from data, validate quality first, progressively add model and API. Best for data-intensive systems.
- **Parallel (Sandwich)**: Test top and bottom simultaneously, meet at model layer. Best for large teams.
- **Big Bang**: All components at once. Only for simple systems or final smoke tests.
- **Integration Harness (Digital Twin)**: Faithful replica of production for realistic testing.

**Harness components:**
- Data simulator (realistic test data matching production distributions)
- Traffic replayer (production traffic patterns against test environment)
- Environment mirror (infrastructure configuration at reduced scale)
- Comparison engine (test vs. production baseline behavior)

**Contract testing:**
- Data contracts between pipeline stages
- Feature contracts between feature store and models
- Model contracts between model and API (input/output schema, latency SLA)
- API contracts (request/response, versioning, deprecation)

**Key decisions:**
- Integration approach selection based on system type and risk profile
- Harness fidelity level (exact replica vs. representative subset)
- Test data strategy (synthetic, anonymized production, sampled production)
- Contract ownership (producer-owned, consumer-owned, shared)

**Approach selection rule (decision shortcut):** user-facing + tight UX SLA → Top-Down; data-intensive + compliance-first → Bottom-Up; large multi-team org → Parallel; production-critical or audit-bound → Integration Harness mandatory. Big Bang only for <3-component systems or as a final smoke test — never as the primary strategy. [EXPLICIT]

**Trade-off — harness fidelity:** an exact production replica gives maximal confidence at high standing infra cost and drift-maintenance burden; a representative subset is cheap but can miss scale-only failures (a join that's fine at 10k rows, OOMs at 10M). Decision rule: replica for the data and model layers (where scale bugs hide), subset for UI/API. [EXPLICIT]

**Contract acceptance criteria:** every contract is executable and version-pinned; a producer change that breaks a consumer contract fails the producer's own CI (consumer-driven contracts), not the consumer's. A contract that lives only in a wiki is not a contract. [EXPLICIT]

**Failure mode:** *replica rot* — the harness silently diverges from production config, so tests pass against a system that no longer exists. Mitigation: the comparison engine periodically diffs harness config against live production and fails on drift. [EXPLICIT]

### S6: CI/CD Test Automation for AI

Defines how tests are automated within the CI/CD pipeline for continuous validation. [EXPLICIT]

**Automation tiers:**
- **T1 Unit** (every commit): Feature computations, transformations, utility functions
- **T2 Component** (every PR): Pipeline stages, model inference, data validation
- **T3 Integration** (daily/pre-deploy): Cross-stage flows, model-pipeline, feature store-model
- **T4 System** (pre-release): End-to-end pipeline, full prediction flow
- **T5 Acceptance** (pre-promotion): Business KPIs, fairness metrics, compliance checks

**CI/CD gates:**
- Code quality gate: linting, type checking, unit tests pass
- Data quality gate: schema validation, distribution checks pass
- Model quality gate: accuracy, AUC, fairness meet thresholds
- Performance gate: latency, throughput within SLA
- Security gate: vulnerability scan, access control verification
- Regression gate: no degradation vs. current production model

**GenAI-specific test automation:**
- Prompt regression testing (prompt template changes validated against golden dataset)
- Guardrail effectiveness testing (known-bad inputs verify filter activation)
- Retrieval quality regression (RAG precision/recall tracked across knowledge base updates)
- Hallucination rate tracking (automated grounding checks on sampled responses)
- Cost regression testing (token usage per query type tracked, alerts on budget drift)

**Continuous monitoring (post-deployment):**
- Drift detection on inputs and outputs
- Performance degradation alerting
- Fairness metric tracking
- Prediction quality sampling and human review

**Key decisions:**
- Gate strictness (hard block vs. warning vs. override with approval)
- Test environment provisioning strategy (on-demand vs. persistent)
- Test data refresh cadence
- Monitoring alert routing and escalation

**Tier-to-trigger acceptance criteria:** T1–T2 run in minutes (or they get skipped under deadline pressure — keep them fast); T5 acceptance is the only tier permitted to gate a production promotion; every CI/CD gate has a named owner who can authorize an override and a logged justification when one is used. An override with no recorded reason is a process failure. [EXPLICIT]

**Trade-off — hard block vs. override-with-approval gate:** hard blocks guarantee the threshold but create incentives to weaken the threshold itself when it stalls a hot fix; override-with-approval preserves throughput but erodes to rubber-stamping without an audit trail. Decision rule: hard-block the fairness, security, and regression gates (irreversible harm); allow logged override on performance gates (recoverable, often noise). [EXPLICIT]

**Failure mode:** *flaky gate fatigue* — a non-deterministic model-quality gate (random seed, GPU non-determinism) fails ~10% of the time, teams learn to re-run until green, and the gate becomes decorative. Mitigation: pin seeds, set thresholds on confidence intervals (S2), quarantine and fix flaky gates rather than tolerating them. [EXPLICIT]

---

## Trade-off Matrix

| Decision | Enables | Constrains | When to Use |
|---|---|---|---|
| **Full matrix coverage** | Comprehensive quality assurance | High test maintenance cost, slow pipeline | Regulated, high-risk AI systems |
| **Model-focused testing** | Fast iteration, model quality | Misses data quality and integration issues | Early-stage, single-model systems |
| **Data-first testing** | Catches most common AI failures | Model behavior tested late | Data-intensive pipeline systems |
| **Automated gates** | Consistent quality, no human bottleneck | Rigid, may block valid models on edge cases | Mature CI/CD with clear thresholds |
| **Manual gates** | Flexibility, expert judgment | Slow, inconsistent, human bottleneck | Novel domains, unclear thresholds |
| **Integration harness** | Realistic testing, high confidence | Infrastructure cost, maintenance overhead | Production-critical AI systems |
| **Contract testing** | Clear team boundaries, fast feedback | Contract maintenance, versioning overhead | Multi-team AI systems |

---

## Assumptions

- AI system has defined requirements with measurable thresholds (AP, NF, SEC, CP metrics)
- Test infrastructure (compute, storage) budget is allocated
- Team has access to representative test data (synthetic or anonymized production)
- CI/CD pipeline exists or is planned for the AI system
- Fairness-relevant protected attributes are identified by the business

## Limits

- Focuses on *testing strategy*, not test implementation code (see testing frameworks documentation)
- Does not design *pipeline architecture* (see **metodologia-ai-pipeline-architecture**)
- Does not select *design patterns* (see **metodologia-ai-design-patterns**)
- GenAI-specific testing (hallucination detection, RAG retrieval quality) requires **metodologia-genai-architecture**
- Does not cover infrastructure testing (see **metodologia-infrastructure-architecture**)

---

## Edge Cases

**No Ground Truth Available:**
Some AI systems (unsupervised, generative) lack clear ground truth. Use proxy metrics (human evaluation, downstream task performance), A/B testing against baselines, and consistency testing (similar inputs should produce similar outputs). [EXPLICIT]

**Regulated Environment with Audit Requirements:**
Every test execution must produce evidence artifacts. Test reports must be immutable and timestamped. Consider the Integration Harness as mandatory for reproducible audit-ready testing. Bottom-Up integration approach ensures data compliance is validated first. [EXPLICIT]

**Continuous Learning System:**
Model updates frequently with new data. Testing strategy must handle continuous model versioning. Regression testing must compare against stable baseline, not just previous version. Drift detection thresholds need regular recalibration. [EXPLICIT]

**Multi-Model Ensemble:**
Testing individual models is necessary but insufficient. Ensemble behavior must be tested as a unit. Disagreement patterns between models should be analyzed. Voting/aggregation logic needs dedicated tests. [EXPLICIT]

**Privacy-Constrained Testing:**
Production data cannot be used for testing (GDPR, HIPAA). Synthetic data generation must match production distributions without exposing real data. Differential privacy techniques for test data. Anonymization verification before test data creation. Note the tension with S3: synthetic test data that perfectly hides real records also hides the rare real-world edge cases that cause production failures — budget for a small, tightly-governed real-data slice for skew validation. [EXPLICIT]

**Cold-Start / Pre-Production System:**
No production traffic, no drift history, no champion model to regress against yet. Substitute: seed regression baselines from the holdout, treat the first release as the champion, and gate on absolute thresholds (AP-7, AP-8) rather than version-over-version deltas until a real baseline exists. [EXPLICIT]

**Vendor / Black-Box Model:**
Model internals are inaccessible (third-party API). Adversarial and counterfactual tests still apply at the input/output boundary; explainability tests degrade to output-consistency checks; the model contract (S5) and output monitoring (S6) carry more weight because internal instrumentation is impossible. [EXPLICIT]

---

## Manejo de Inputs Ambiguos

- Si el nombre del sistema no se proporciona: solicitar antes de proceder.
- Si el MODO no se especifica: usar `piloto-auto` (default).
- Si el contexto es insuficiente para una sección: documentar como "[Requiere input adicional: {descripción}]" en lugar de inventar contenido.
- Si no hay thresholds de accuracy/fairness definidos: proponer thresholds basados en industry standards (AP-7: accuracy >= .88, AP-11: fairness >= 90%) y marcar como "propuesto — requiere validación".
- Si no hay protected attributes definidos para fairness testing: solicitar explícitamente; no asumir atributos protegidos.

---

## Validation Gate

> **Nota al ejecutor:** Esta checklist debe verificarse antes de entregar el artefacto final. Si algún item no aplica al sistema específico, documentar la razón de exclusión.

Before finalizing delivery, verify:

- [ ] Testing scope matrix covers all 6 types x 6 layers (cells prioritized, not necessarily all filled)
- [ ] Model testing includes accuracy, adversarial, drift, counterfactual, and regression tests
- [ ] Data quality testing covers schema, distribution, lineage, and training-serving skew
- [ ] Compliance testing addresses governance, audit trails, privacy, and encryption requirements
- [ ] Fairness testing uses appropriate metrics for the domain with defined thresholds
- [ ] Integration approach selected and justified (top-down, bottom-up, parallel, harness)
- [ ] CI/CD automation tiers defined with clear gates and triggers
- [ ] Continuous monitoring strategy extends testing beyond deployment
- [ ] Test data strategy addresses privacy, representativeness, and freshness
- [ ] Testing strategy is implementable (tools selected, team capability considered)

---

## Cross-References

- **metodologia-ai-software-architecture**: Architecture defines testable components; testing validates architecture
- **metodologia-ai-conops**: Success metrics from CONOPS become test acceptance criteria
- **metodologia-ai-pipeline-architecture**: Pipeline stages define test boundaries; requirements framework provides thresholds
- **metodologia-ai-design-patterns**: Patterns require pattern-specific tests (drift detection accuracy, rollback speed)
- **metodologia-genai-architecture**: GenAI-specific tests (hallucination, retrieval quality) complement this general strategy
- **metodologia-aws-architecture-design**: AWS testing infrastructure (SageMaker Model Monitor, Bedrock evaluation, CloudWatch)
- **metodologia-testing-strategy**: Traditional testing strategy provides foundation; this skill adds AI-specific layers
- **metodologia-quality-engineering**: Quality engineering provides broader quality framework context

## Output Format Protocol

| Format | Default | Description |
|--------|---------|-------------|
| `markdown` | Yes | Rich Markdown + Mermaid diagrams. Token-efficient. |
| `html` | On demand | Branded HTML (Design System). Visual impact. |
| `dual` | On demand | Both formats. |

## Output Artifact

**Primary:** `A-04_AI_Testing_Strategy_Deep.html` — Testing scope matrix (6x6), model test specifications, data quality test plan, compliance and fairness test design, integration approach diagram, CI/CD automation pipeline with gates.

**Secondary:** Test case templates (.md), fairness test specification, integration harness design, CI/CD gate configuration, test data strategy document.

---
**Fuente**: Avila, R.D. & Ahmad, I. (2025). *Architecting AI Software Systems*. Packt.
