<!-- distilled from alfa skills/data-privacy-patterns -->
<!-- > -->
# Data Privacy Patterns
> "Method over hacks."
## TL;DR
Patterns for PII discovery, anonymization, lawful processing (GDPR), and consent lifecycle. Scope: design + review of data flows. NOT a legal sign-off, NOT a DPIA substitute. [EXPLICIT]

## Procedure
### Step 1: Discover
- Inventory data flows; classify fields as PII / sensitive (Art. 9: health, biometrics, ethnicity) / non-PII. [EXPLICIT]
- Map each field to a lawful basis (consent, contract, legitimate interest) and a retention clock. [EXPLICIT]
- Detection: regex for structured PII (email, national ID, card), NER for free text; never rely on column names alone. [EXPLICIT]

### Step 2: Analyze
- Choose technique by re-identification risk vs utility (Constitution XIII/XIV):
  - **Pseudonymization** (reversible, keyed): reversible only with key; key stored separately. Still personal data under GDPR. [EXPLICIT]
  - **Anonymization** (irreversible): k-anonymity ≥ k, plus l-diversity / t-closeness for sensitive attributes to block attribute disclosure. [EXPLICIT]
  - **Masking / tokenization**: format-preserving for test/lower envs; tokens map back only in a vault. [EXPLICIT]
  - **Differential privacy**: aggregate analytics where individual rows must not leak; tune ε. [EXPLICIT]
- Decision rule: prefer irreversible anonymization for analytics/exports; reserve pseudonymization for cases needing re-linkage. Trade-off: lower k raises utility but raises re-ID risk. [EXPLICIT]

### Step 3: Execute
- Implement minimization (collect only what the basis justifies) and purpose limitation at the boundary, not downstream. [EXPLICIT]
- Encrypt at rest + in transit; separate anonymization keys from data; log access with evidence tags. [EXPLICIT]

### Step 4: Validate
- Verify quality criteria; attempt a re-identification/linkage test against the anonymized output before release. [EXPLICIT]

## Quality Criteria
- [ ] Every PII field has lawful basis + retention rule
- [ ] Re-identification test passed (k/l/t thresholds met)
- [ ] Consent state checked before each processing purpose
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output

## Consent Management
- Record per purpose: granular, opt-in, timestamped, withdrawable as easily as given. [EXPLICIT]
- Withdrawal propagates: stop processing + honor erasure (Art. 17) downstream, including backups and derived datasets. [EXPLICIT]
- Re-consent required when purpose changes; pre-ticked boxes and bundled consent are invalid. [EXPLICIT]

## Usage

Example invocations:

- "/data-privacy-patterns" — Run the full data privacy patterns workflow
- "data privacy patterns on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment or legal sign-off for final decisions [EXPLICIT]
- GDPR-centric; CCPA/LGPD/HIPAA add obligations not covered here [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Free-text fields with embedded PII | Run NER + masking; regex alone misses unstructured PII |
| Small cohort breaks k-anonymity | Suppress, generalize, or aggregate; do not release row-level |
| Quasi-identifiers enable linkage | Treat zip+DOB+sex as PII; generalize before publish |
| Consent withdrawn after processing | Halt purpose, trigger erasure across copies + backups |
| Cross-border transfer | Require adequacy decision or SCCs before export |
