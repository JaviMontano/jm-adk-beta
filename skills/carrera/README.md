# carrera — README

Router skill for the Spanish-language candidate-side career cluster. It resolves
one `topic` and runs exactly one playbook from `routes.json`, never the whole
cluster. Every playbook is deterministic, offline, and evidence-tagged. [DOC]

## What it does

`carrera` turns supplied career evidence (emails, notes, a CV, an offer, a
payslip, interview feedback) into one of twelve scoped deliverables:

| Topic | Deliverable |
|-------|-------------|
| `proceso-seleccion-orchestrator` | Deterministic selection-status board + one next action |
| `simulador-entrevista` | One-question mock interview scored on 3 separate rubrics |
| `negociacion-oferta` | Offer table with acceptance filters + PIVOTE + counterproposal |
| `cv-cover-optimizer` | ATS/role/brand lint of CV + cover letter |
| `cv-enhancement` | Targeted CV rewrite tied to supplied achievements |
| `follow-up-email` | Evidence-anchored post-stage follow-up draft |
| `onboarding-90-dias` | Verifiable 30/60/90 plan with anti-burnout limits |
| `red-y-referencias` | Consent-audited reference network + referral plan |
| `gratitud-post-proceso` | Person-differentiated thank-you notes (anti-FOMO lint) |
| `cierre-conversacion` | Reproducible conversation closeout + durable handoff |
| `acta-formal` | Formal acta / minutes record |
| `validar-liquidacion-co` | Arithmetic-only Colombian liquidación validation |

## When to use

Use it for **candidate-side** work: tracking a selection process, practicing
interviews, evaluating an offer, optimizing a CV, drafting follow-ups, planning
onboarding, managing references, writing gratitude notes, closing a
conversation, recording an acta, or validating a Colombian settlement. [DOC]
Out of scope: hiring-side authoring (JD writing, sourcing, screening rubrics for
an employer), legal/tax/immigration advice, and live market or salary
benchmarks. Route those elsewhere. [INFERENCIA]

## How it routes and executes

1. **Resolve `topic`** against the `routes.json` enum. Ambiguous between two →
   ask one disambiguating question; never guess silently. [INFERENCIA]
2. **Read exactly one** `routes:` playbook for that topic. No sibling preload. [DOC]
3. **Apply depth**: `quick` = essentials only; `deep` = exhaustive, same gates. [CONFIG]
4. **Spine**: Discover → Analyze → Execute → Validate, under constitution
   v6.0.0, evidence tags, and the script-first rule. [CONFIG]
5. **Gate before return** (see `SKILL.md` Validation gate): single playbook,
   contract-shaped output, one tag family, no invented numbers, stop-and-ask on
   `{VACIO_CRITICO}`.

## Evidence taxonomy

Authoring tags (this skill's docs and most playbooks): `[DOC]` `[CONFIG]`
`[INFERENCIA]` `[SUPUESTO]` `[CÓDIGO]`. Board/feedback playbooks add their own
provenance set `[EXPLICIT]` `[INFERRED]` `[OPEN]` and must not mix the two
families in one output. [DOC]

## References

- Playbooks: `references/<topic>.md` (one per route in `routes.json`)
- Routing contract: `routes.json`
- Role contracts: `agents/lead.md`, `agents/specialist.md`, `agents/support.md`,
  `agents/guardian.md`
- Domain knowledge: `knowledge/body-of-knowledge.md`,
  `knowledge/knowledge-graph.json`
- Prompts: `prompts/primary.md`, `prompts/meta.md`, `prompts/variations/`
- Output scaffold: `templates/output.md`
- Worked example: `examples/example-input.md`, `examples/example-output.md`
- Quality + routing assets: `assets/` (see `assets/README.md`)
