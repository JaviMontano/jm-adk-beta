<!-- distilled from alfa skills/red-y-referencias -->
<!-- This skill should be used when the user asks to manage a professional reference network, request or audit explicit consent, plan referral follow-ups, map relationship context, decide whether a reference can be contacted, or create an evidence-backed networking handoff. -->
# Red Y Referencias

## Purpose

Manage professional references and networking follow-ups without guessing consent or exposing direct contact details. Convert supplied notes into a deterministic reference packet with evidence IDs, consent status, allowed actions, follow-up cadence, network edges, blockers, and next actions.

Use this skill for relationship tracking and consent-safe referral planning. Do not use it to scrape social networks, enrich contacts, bypass consent, or send messages through live services unless the user separately supplies explicit data and approval.

## Assumptions and Anti-Scope

- `[EXPLICIT]` The user supplies all evidence; this skill never enriches, scrapes, or invents contacts, consent, or dates.
- `[EXPLICIT]` `as_of` is authoritative for every time decision. The current clock is never read — this keeps packets reproducible and audit-safe.
- `[INFERRED]` Absent evidence, `consent_status` defaults to the most restrictive non-actionable state, never to a permissive one.
- Anti-scope (out of bounds): sending messages via live mailbox/calendar/social; deriving willingness from friendship/title/seniority; storing raw PII; ranking or scoring contacts; CRM sync.

## Deterministic Contract

Follow `assets/output-contract.json` and validate packets with `scripts/reference_network_validator.py`. The packet must include:

- `as_of` ISO date (`YYYY-MM-DD`) supplied by the user or report author.
- Evidence records for every consent, relationship, follow-up, and action claim. No claim without an `E-###` reference.
- Contacts with `consent_status` from `assets/consent-policy.json`.
- Allowed actions derived only from explicit consent and evidence.
- Follow-up decisions computed from `as_of`, not from the current clock.
- Privacy-safe labels instead of direct email, phone, payment, or private channel details.

### Acceptance Criteria (packet is `ready` only if ALL hold)

- `[EXPLICIT]` Every contact, edge, follow-up, and action carries ≥1 resolvable `E-###` reference.
- `[EXPLICIT]` No action exists whose contact `consent_status != explicit_granted`.
- `[EXPLICIT]` All dates are absolute ISO; zero relative tokens ("ayer", "next week", "soon").
- `[EXPLICIT]` Every `network_edge` resolves to two existing `C-###` nodes plus evidence.
- `[EXPLICIT]` No stale follow-up lacks a paired remediation action.
- `[EXPLICIT]` Validator exits 0 and no direct contact detail (email/phone/payment) appears anywhere.

### Decisions and Trade-offs

- `[EXPLICIT]` `as_of`-only time vs. live clock: chosen for deterministic, replayable, auditable output. Trade-off — caller must pass a fresh `as_of` each run or follow-ups silently age out.
- `[EXPLICIT]` Fail-closed consent default: a missing/ambiguous status blocks rather than permits. Trade-off — more `blocked` packets, but zero non-consented outreach.
- `[INFERRED]` Labels over raw contact data: privacy by construction. Trade-off — the packet alone cannot send; a separate authorized step must rehydrate details.

## Workflow

1. Inventory supplied evidence and assign stable IDs such as `E-001`.
2. Create contact records with stable IDs such as `C-001`. Use `contact_label`, `relationship`, `consent_status`, `consent_evidence_ref`, `last_contact_date`, and `allowed_actions`.
3. Reject or block any contact action when consent is not `explicit_granted`.
4. Compute stale follow-up from `as_of` and `last_contact_date` using `assets/followup-policy.json`.
5. Build network edges only when both contacts exist and the edge has evidence.
6. Create actions with IDs such as `A-001`, due dates in ISO format, action type from policy, and one evidence reference.
7. Validate JSON with `scripts/reference_network_validator.py` before producing the markdown handoff from `templates/output.md`.

### Edge Cases

- Same person, two evidence sources: one `C-###`, multiple `consent_evidence_ref`; never duplicate the contact.
- Consent granted then revoked: latest-dated evidence wins; revocation forces `blocked` and strips `allowed_actions`.
- `last_contact_date` after `as_of`: invalid input → block; do not compute negative staleness.
- Edge references a contact not yet created: unresolved edge → block (step 5 ordering matters).
- Consent scoped to one channel (e.g. LinkedIn only): allowed actions limited to that channel; other channels stay `[OPEN]`.

### Worked Example

Input: "Ana (ex-manager) said by email 2026-05-02 she'll give a reference; last spoke 2026-03-01. as_of 2026-06-11."
Output: `E-001` (email 2026-05-02), `C-001` Ana `relationship: former_manager`, `consent_status: explicit_granted`, `consent_evidence_ref: E-001`, `allowed_actions: [request_reference]`. Follow-up from `2026-03-01` vs `as_of 2026-06-11` → stale → emits `A-001 follow_up` due ISO date, ref `E-001`. Tag the reference claim `[EXPLICIT]`; tag "ex-manager" relationship `[INFERRED]` if only the email implies it.

### Failure Modes (validator blocks)

Missing evidence ref · non-consented action · stale follow-up without action · relative/ambiguous date · duplicate `C/E/A` ID · unresolved edge · exposed email/phone/payment · `last_contact_date > as_of`.

## Output Rules

- Tag claims with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- Mark the packet `blocked` when consent is missing, relative dates appear, direct contact details are exposed, or follow-up is stale without an action.
- Do not include raw email bodies, phone numbers, private email addresses, or payment identifiers.
- Do not infer willingness to provide a reference from prior friendship, job title, seniority, or social media connection.
- Do not contact or draft as if contact is authorized unless `consent_status` is `explicit_granted`.

## Assets

- `assets/manifest.json` lists deterministic assets.
- `assets/output-contract.json` defines packet structure.
- `assets/consent-policy.json` defines consent statuses and allowed actions.
- `assets/followup-policy.json` defines stale follow-up calculation.
- `assets/privacy-policy.json` defines redaction and contact-detail blockers.
- `assets/network-map-policy.json` defines node and edge requirements.

## Scripts

Run:

```bash
python3 skills/red-y-referencias/scripts/reference_network_validator.py --input <packet.json>
bash skills/red-y-referencias/scripts/check.sh
```

The validator is offline and deterministic. It rejects missing evidence, non-consented contact actions, stale follow-ups without actions, relative dates, duplicate IDs, unresolved network edges, and direct contact details.

## Related Skills

- `onboarding-90-dias`
- `proceso-seleccion-orchestrator`
- `gratitud-post-proceso`

## Stop Conditions

Stop when the user asks to contact a person without explicit consent, enrich contacts from external sources, infer private contact details, or rely on a live mailbox/calendar/social network not already provided as evidence.
