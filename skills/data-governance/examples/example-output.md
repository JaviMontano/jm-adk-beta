# Example output — data-governance router (worked)

Response to the export/erasure request in `example-input.md`.

## 1. Routing decision
- **Topic chosen**: `data-privacy-patterns` — request is PII handling +
  anonymization + erasure before an external export; weakest-overlap match over
  generic `data-governance` and `data-documentation`. [INFERENCIA]
- **Playbook loaded**: references/data-privacy-patterns.md (exactly one). [DOC]
- **Depth**: deep — export with re-identification risk warrants the full ladder
  plus a re-identification test. [INFERENCIA]

## 2. Discover — field classification
| Field | Class | Lawful basis | Retention |
|---|---|---|---|
| `customers.email` | Direct identifier (PII) | contract | life of account + 24m [SUPUESTO] |
| `customers.full_name` | Direct identifier (PII) | contract | as above |
| `customers.date_of_birth` | Quasi-identifier | contract | as above |
| `customers.postal_code` | Quasi-identifier | contract | as above |
| `support_tickets.notes` | Free text, may embed PII | legitimate interest | 12m [SUPUESTO] |

`date_of_birth + postal_code + sex` together enable linkage — treat as PII even
though no single field is a direct identifier. [DOC] Retention horizons are
assumptions — confirm against the records policy. [SUPUESTO] → verify with DPO.

## 3. Analyze — technique selection
| Decision | Chosen | Rejected | Trade-off | Tag |
|---|---|---|---|---|
| Direct identifiers (email, name) | Drop / irreversible tokenization (no vault shared) | Pseudonymize with shared key | Sharing a key keeps it personal data under GDPR — defeats the export goal | [DOC] |
| Quasi-identifiers (DOB, postal) | Generalize: DOB→birth year, postal→first 2 chars; enforce k-anonymity k≥5, l-diversity on churn label | Release raw | Raw enables re-identification by linkage | [DOC] |
| Free-text `notes` | NER + masking of detected entities (names, emails, IDs) | Regex only | Regex alone misses unstructured PII | [DOC] |
| Aggregate churn stats vendor also wants | Differential privacy on the aggregate, tune ε | Raw counts | Small cohorts leak individuals | [DOC] |

## 4. Execute — export plan
1. Build a vetted export view: drop direct identifiers, generalize quasi-IDs to
   k≥5 / l-diversity, NER-mask `notes`. [DOC]
2. Encrypt in transit; require an SCC/adequacy basis for the vendor transfer. [DOC]
3. Log the export event with evidence tags (actor, dataset, purpose). [DOC]

## 5. Erasure (Art. 17) handling
- On a deletion request: halt processing for that purpose, then erase the subject
  across the source tables, the export view, derived datasets, and backups. [DOC]
- Because the external copy is anonymized to k≥5 (no longer personal data),
  erasure obligations attach to the **source**, not the released aggregate —
  document this reasoning so it is defensible. [INFERENCIA]

## 6. Validate — gate checklist
- [x] Exactly one playbook loaded (data-privacy-patterns); no siblings. [DOC]
- [x] Each PII field has lawful basis + retention. [DOC]
- [x] Re-identification/linkage test run on the export view before release;
      k≥5 and l-diversity confirmed. [DOC]
- [x] Consent/erasure path defined and propagates to backups. [DOC]
- [x] No prices; no client PII reproduced here; single brand. [CONFIG]

## 7. Open assumptions
- Retention horizons [SUPUESTO] → confirm with DPO/records policy.
- Vendor transfer basis [SUPUESTO] → confirm SCCs or adequacy before export.
