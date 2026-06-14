# Email-Comms Deliverable

## 1. Routing decision

- **Request:** <one-line restatement of the user's email task>
- **Resolved topic:** `<email-sending | email-template-builder | email-templates | newsletter-design>`
- **Why this topic:** <signal that mapped the request> [INFERENCE]
- **Prerequisite sequence (if any):** <e.g. builder → sending; or "none">
- **Depth:** `<quick | deep>`
- **Playbook read:** `references/<topic>.md`

## 2. Discover

- Context gathered: <infra, volume, client mix, baselines>
- Constraints / unknowns: <items flagged [ASSUMPTION] for confirmation>

## 3. Analyze

- Decision(s) made with trade-offs: <provider / responsive strategy / content architecture>
- Evidence: <tag each decision> [DOC]/[INFERENCE]

## 4. Execute — deliverable

<Topic-specific artifact. Examples by topic:>

- **email-sending:** DNS records (SPF/DKIM/DMARC), queued send design, webhook + suppression plan. [CONFIG]/[CODE]
- **email-template-builder:** inlined ≤600px HTML + preheader + plain-text part + Firestore `mail`-doc payload. [CODE]
- **email-templates:** MJML/hand-coded template + MSO/VML Outlook fixes. [CODE]
- **newsletter-design:** content template (sections + purpose) + subject/preheader pair + UTM scheme + measurement plan. [DOC]

```
<artifact content / payload / records here>
```

## 5. Validate (gate)

| Check | Result | Evidence |
|-------|--------|----------|
| <topic gate 1> | pass/fail | <tag> |
| <topic gate 2> | pass/fail | <tag> |
| Evidence tags on every claim (Alfa core EN) | pass/fail | [DOC] |
| Single brand / sending domain | pass/fail | [ASSUMPTION] |

## 6. Handoffs & follow-ups

- Next topic to run (if sequenced): <…>
- Deferred to `deep`: <…>
- Open `[ASSUMPTION]` items to confirm against vendor docs: <…>
