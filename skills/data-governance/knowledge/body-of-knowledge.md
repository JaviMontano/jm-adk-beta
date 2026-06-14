# Body of Knowledge — data-governance router

Domain knowledge the router and its agents rely on. Concepts here are shared
across the seven topics; topic-specific depth lives in `references/*.md`. [DOC]

## 1. The router invariant
This skill governs **data**, it does not move it. It resolves one `topic` ∈
{audit-trail-design, data-documentation, data-governance, data-privacy-patterns,
data-storytelling, data-strategy, pipeline-governance} and loads exactly one
playbook. Loading more than one defeats the router. [DOC]

## 2. Disambiguation rule (weakest-overlap)
Pick the topic whose scope overlaps *least* with the others, i.e. the most
specific match. Privacy and audit beat generic governance; DQ-inside-a-pipeline
(pipeline-governance) beats strategy. On a genuine tie, ask one question. [INFERENCIA]

## 3. Privacy concepts (data-privacy-patterns)
- **PII classes**: identifiers, quasi-identifiers (zip+DOB+sex enable linkage),
  Art. 9 special categories (health, biometrics, ethnicity). [DOC]
- **Lawful basis**: consent, contract, legitimate interest — each field maps to one
  plus a retention clock. [DOC]
- **De-identification ladder**: pseudonymization (reversible, keyed, still personal
  data) → masking/tokenization → anonymization (k-anonymity ≥ k, l-diversity,
  t-closeness) → differential privacy (ε-tuned aggregates). [DOC]
- **Decision rule**: prefer irreversible anonymization for analytics/exports;
  reserve pseudonymization for re-linkage needs. Lower k = higher utility but
  higher re-ID risk. [DOC]
- **Consent**: granular, opt-in, timestamped, withdrawable; withdrawal propagates
  to backups and derived datasets (Art. 17). [DOC]

## 4. Audit-trail concepts (audit-trail-design)
- **Tamper-evidence** via `prev_hash` chaining (detects delete/reorder), not just
  per-record signatures. [DOC]
- **Minimum record schema**: `event_id`, UTC ISO-8601 `timestamp`, authenticated
  `actor` (never inferred), `action`, qualified `resource`, `outcome`,
  `source_ip`/`session`, `prev_hash`. [DOC]
- **Append-only over mutable**; **legal hold wins over retention expiry**. [DOC]

## 5. Documentation concepts (data-documentation)
- Deliverables: data dictionary, schema doc, **column-grain** lineage, business
  glossary. Done = zero orphan columns; doc-vs-live drift = 0. [DOC]
- Generators capture shape, never intent — auto-skeleton then hand-annotate. [INFERENCIA]

## 6. Governance & strategy concepts
- **Operating model**: producers, consumers, stewards, regulators; a named
  decision-maker on the escalation path. Missing-steward is the most common gap. [INFERENCIA]
- **Centralized vs federated/mesh**: mesh only with ≥3 autonomous domain teams;
  below that, centralized is cheaper. [INFERENCIA]
- **Architecture**: medallion (bronze/silver/gold) for analytics estates;
  domain-oriented mesh for federated orgs. ETL vs ELT, batch vs streaming chosen
  per source, not globally. [INFERENCIA]

## 7. Pipeline-governance concepts
- **Phase gates G0–G3**: input bounded (G0), context loaded (G1), option chosen +
  confidence scored (G2), outputs evidence-tagged (G3). Hard gates over advisory;
  confidence ≥ 0.95 enforced. [DOC]

## 8. Storytelling concepts (data-storytelling)
- Metrics → insight → narrative arc framed for the audience; every claim traceable
  to its metric; never green-as-success. [INFERENCIA]

## 9. Reference standards & frameworks
- GDPR (lawful basis, Art. 9, Art. 17 erasure); k-anonymity / l-diversity /
  t-closeness; differential privacy; data-mesh principles; medallion architecture.
  CCPA/LGPD/HIPAA add obligations not covered by the GDPR-centric playbooks. [DOC]

## 10. Evidence taxonomy
Alfa set: `[DOC]` / `[CONFIG]` / `[CÓDIGO]` / `[INFERENCIA]`(`[INFERENCE]`) /
`[SUPUESTO]`(`[ASSUMPTION]`). One tag per claim; every assumption has a
verification step. [CONFIG]
