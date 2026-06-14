# Example Input — sales-bizdev

A concrete request that exercises the router and the `client-dossier` route.

## User request (verbatim)

> "I've got a discovery call in 2 days with Pagomático, a payments fintech in Bogotá. I'll be talking to their VP of Engineering. Build me a prep brief on the company so I don't walk in cold — who they are, what's probably hurting them, and a way to open the conversation. We're pitching from JM Labs."

## Context provided

- **Target account:** Pagomático (fictional fintech, payments vertical, Bogotá HQ).
- **Named contact:** VP of Engineering (name not given).
- **Brand:** JM Labs.
- **Time horizon:** discovery call in 48h.
- **Public signals available to research:** company website, LinkedIn company + people pages, Crunchbase funding data, job postings.

## What the router should do

1. **Classify:** the deliverable is a one-account *brief* for a specific meeting, not a list, a sequence, or a pitch → route to **`client-dossier`**. Channel words ("call", "open the conversation") do not make this `b2b-outreach`; the user asked for the prep brief, not the messages.
2. **Lock brand:** JM Labs (single brand). Dossier output uses JM Labs dark style + the `[EXPLICIT]`/`[INFERRED]`/`[OPEN]` tag family.
3. **Pick depth tier:** call is 1-3 days out → **Standard** dossier (full S2-S5, 2-3 contacts). Not Flash (that is for a <1h inbound), not Deep (no >$50K strategic-account signal stated).
4. **Flag missing input:** the VP of Engineering's name is not given. Ask for the LinkedIn URL or confirm the name before writing a Contact Card — do not profile the wrong person.

## Expected guardrails to surface

- All revenue/headcount for a private fintech tagged `[est. — not verified]`.
- Email pattern (if inferred) labeled `[INFERRED — not verified]` with a confidence level.
- Pain hypotheses presented as hypotheses, each with ≥2 tagged signals and a validation question.
- No personal/home/family data on the contact — public professional only.
- The brief must end in one specific opening hook, not a pile of facts.
