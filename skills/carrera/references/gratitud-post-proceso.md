<!-- distilled from alfa skills/gratitud-post-proceso -->
<!-- Redacta agradecimientos post-proceso diferenciados por persona, evidencia de interaccion, voz de marca y lint offline contra FOMO, hustle, servilismo y promesas no verificables. -->
# Gratitud Post Proceso

## Purpose

Use this skill after an interview, selection process, workshop, review panel, or professional conversation when the user needs a thank-you note that is specific, grounded in supplied evidence, and safe to send. The skill produces differentiated messages per recipient, preserves factual boundaries, and validates tone with `scripts/lint_gratitud.py`. [DOC]

Anti-scope: it does not send messages, schedule follow-ups, fetch CRM/ATS data, infer the recipient's email, or assess whether you will get the job. Drafting only; the user sends. [SUPUESTO]

## Inputs Expected

- Process or meeting context. [DOC]
- Recipient name, role, and relationship to the process.
- Evidence from the interaction: topics discussed, contribution, decision stage, or next step.
- Channel constraints: email, LinkedIn, WhatsApp, note, or internal message.
- Brand voice constraints and any promises that must not be made.

Minimum to produce a *named* (non-template) message: one recipient identifier plus one interaction-specific evidence detail. Below that, output degrades to template-only (see Edge Cases). [INFERENCIA]

## Outputs Expected

- One message per recipient or persona. [DOC]
- Recipient-specific evidence line.
- Subject or opening line when the channel needs it (email/LinkedIn: yes; WhatsApp/internal note: usually no). [INFERENCIA]
- Tone and risk notes for FOMO, hustle, servility, overpromising, or invented process details.
- Validation command evidence when a JSON packet is provided.

## Procedure

### Discover

Identify the process stage, channel, recipient, relationship, evidence from the interaction, and whether the user wants a message draft or a reusable template. Tag each supplied fact; mark anything you cannot source as `[SUPUESTO]` and ask before drafting on top of it. [DOC]

### Analyze

Apply `assets/recipient-differentiation-policy.json`, `assets/evidence-policy.json`, `assets/brand-voice-policy.json`, and `assets/promise-boundary-policy.json` before drafting. [CONFIG]

### Execute

Write concise gratitude that names a real contribution, avoids pressure, and states next steps only when the user supplied them. Do not invent interview details, relationship warmth, availability, outcomes, or deadlines. [DOC]

Length guidance: WhatsApp/note 2-4 sentences; email/LinkedIn 4-7. One distinctive brand phrase maximum; if none fits cleanly, use none. [INFERENCIA]

### Validate

Run the deterministic fixture suite: [CONFIG]

```bash
bash skills/gratitud-post-proceso/scripts/check.sh
```

For a specific packet:

```bash
python3 skills/gratitud-post-proceso/scripts/lint_gratitud.py --input <packet.json>
```

Report the exact command and its pass/fail result. A non-zero exit is a blocker, not a warning — do not present a message the linter rejected as final. [INFERENCIA]

## Assets

- `assets/recipient-differentiation-policy.json` [CONFIG]
- `assets/evidence-policy.json`
- `assets/brand-voice-policy.json`
- `assets/promise-boundary-policy.json`
- `assets/output-contract.json`

## Quality Criteria

- Each message has a named recipient or explicit recipient archetype. [DOC]
- Each message includes at least one interaction-specific evidence detail.
- Tone is grateful, concrete, and calm; it avoids servility, pressure, and performative urgency.
- Brand phrases are not stacked; at most one distinctive phrase is allowed per message.
- Follow-up or availability statements are conditional on user-provided facts.
- Missing process evidence produces a partial or blocked output instead of invented detail.

## Edge Cases

- No recipient: produce a blocked checklist and ask for the target person or persona. [DOC]
- No interaction evidence: provide a generic-safe template and mark missing evidence.
- Multiple recipients: differentiate by role and contribution, not by flattery intensity.
- User asks to pressure the recipient: remove FOMO and state a neutral follow-up.
- User asks to apologize excessively: rewrite to gratitude without servility.
- User asks to imply acceptance, offer, or commitment: block unless supplied as fact.
- Same evidence for several recipients: keep the shared detail but vary the angle per role; identical bodies fail differentiation. [INFERENCIA]
- Panel where one interviewer was silent: thank the panel collectively rather than inventing a contribution for the silent member. [SUPUESTO]

## Worked Examples

**Valid (email, evidence supplied).** Input: recipient "Ana, Eng Manager"; evidence "discussed migrating the batch pipeline to event-driven"; stage "final round, decision next week (user-stated)". [SUPUESTO]
> Subject: Thank you — yesterday's conversation
> Hi Ana, thank you for the time yesterday. The discussion on moving the batch pipeline to an event-driven design was the part I keep thinking about. I'd be glad to go deeper on it whenever useful. — [name]

Why it passes: one named recipient, one specific evidence line, follow-up is conditional, no outcome claimed. [INFERENCIA]

**Invalid → rewrite (overpromising + FOMO).**
> "I know I'm the best fit and I have other offers, so I'd love to hear back fast!"

Linter flags overpromising and pressure. Rewrite: keep gratitude, drop the self-assessment and the urgency, state a neutral availability line only if the user supplied a real deadline. [DOC]

## Assumptions and Limits

- The skill improves professional communication; it does not guarantee process outcomes. [DOC]
- If evidence is unavailable, mark the message as template-only or ask for context.
- Do not include private contact details in examples or fixtures.

## Failure Modes

- Fabricated warmth ("it was great connecting") with no supporting evidence → reads as generic; cut or replace with a real detail. [INFERENCIA]
- Brand-phrase stacking → tonal noise; enforce the one-phrase cap.
- Implying an offer/acceptance the user never confirmed → factual overreach; block per promise-boundary policy. [CONFIG]
- Servile over-apology → undermines the candidate; rewrite to plain gratitude.
- Presenting a linter-rejected draft as final → silent quality regression; treat non-zero exit as terminal. [SUPUESTO]

## Scripts

`scripts/lint_gratitud.py --input <json>` validates gratitude packets for recipient specificity, interaction evidence, tone blockers, promise boundaries, and output sections. It also accepts plain text for ad hoc tone linting. `scripts/check.sh` runs deterministic valid and invalid fixtures offline. [CÓDIGO]

## Related Skills

- `proceso-seleccion-orchestrator`
- `negociacion-oferta`

## Evidence Requirements

- Tie every specific thanks, topic, next step, or process claim to user-provided evidence. [DOC]
- Mark missing evidence as a blocker or assumption.
- Report validation commands and results when a machine-readable packet is used.

## Update-Safety Notes

- Default to draft text unless the user explicitly asks to edit files. [DOC]
- Preserve the user's facts, names, and relationships.
- Do not add network checks, wall-clock timestamps, random IDs, or live process-status claims to validation. Determinism keeps fixtures reproducible offline. [INFERENCIA]
