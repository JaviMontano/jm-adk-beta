# carrera — Body of Knowledge

Domain knowledge for the Spanish candidate-side career cluster. Stable concepts,
standards, and decision rules shared across the twelve playbooks. [DOC]

## 1. Router contract
- `topic` (required) selects exactly one playbook from `routes.json`; `depth`
  (`quick`|`deep`, default `quick`) sets thoroughness, not the gates. [CONFIG]
- Single-playbook law: never load siblings "to compare" — it defeats routing and
  leaks scope. [INFERENCIA]
- Spine for every playbook: Discover → Analyze → Execute → Validate, under
  constitution v6.0.0, evidence tags, and a script-first rule. [CONFIG]

## 2. Evidence taxonomy (two families, never mixed)
- **Authoring set** (docs + most playbooks): `[DOC]` documented/policy fact,
  `[CONFIG]` configuration/contract, `[INFERENCIA]` reasoned inference,
  `[SUPUESTO]` assumption pending confirmation, `[CÓDIGO]` script-verified. [DOC]
- **Board/feedback provenance set** (`proceso-seleccion-orchestrator`,
  `simulador-entrevista`): `[EXPLICIT]` stated in evidence, `[INFERRED]` derived,
  `[OPEN]` unknown/open question. One output uses one family only. [DOC]
- `{VACIO_CRITICO}` = critical input missing → stop and ask. `{POR_CONFIRMAR}` /
  `{WEB}` must each pair with a verification step or a citation. [DOC]

## 3. Determinism standard
- Identical input ⇒ byte-identical output. Every tie has a documented secondary
  sort key (e.g. evidence by `received_date` then `id`; contacts by normalized
  `name` then `role`; stages by explicit `sequence`). [INFERENCIA]
- Dates are ISO `YYYY-MM-DD` only. Relative dates ("next week", "mañana") are
  preserved verbatim and **block**, never normalized against the wall clock. [DOC]
- Offline-only: no calendar, email, ATS, web, FX, or market fetch unless the user
  pastes that data into the workspace. This keeps runs replayable and PII-safe. [CONFIG]

## 4. Decision rules by domain
- **Selection board:** record state, never judge fit/outcome; a contact exists
  only with name AND role; exactly one next action resolving to one real stage +
  one real evidence id; missing `sequence` ⇒ `blocked`, not inferred order. [DOC]
- **Interview sim:** three independent rubrics, each with a verbatim evidence
  snippet; no `overall_score` / averaging; next step targets the weakest
  dimension, tie broken by stable order `substance > english > presence`. [DOC]
- **Offer negotiation:** hard filters gate first (floor uses `>=`; exclusivity vs
  parallel-stream; relocation goal; deal breakers); PIVOTE (purpose, income,
  viability, optionality, traction, energy, each 0–10) is a quality score applied
  only after hard filters pass and never resurrects a hard fail. Non-USD with no
  supplied conversion ⇒ open question, never an assumed FX rate. [DOC]
- **CV/cover & enhancement:** offline lint of ATS keywords, sections, length,
  contact hygiene, brand voice; rewrites stay anchored to supplied achievements. [DOC]
- **Onboarding 30/60/90:** milestones must be verifiable; priorities bounded;
  anti-burnout limits enforced; no unsupported performance promises. [DOC]
- **References:** contact only with explicit, current consent; audit consent
  before any referral follow-up. [DOC]
- **Gratitude / closeout / acta:** person-differentiated, evidence-anchored,
  reproducible; lint against FOMO, hustle, servility, and unverifiable promises. [DOC]
- **Liquidación CO:** arithmetic-only recompute of cesantías, intereses de
  cesantías, prima, vacaciones, deductions, and neto from supplied figures; no
  legal advice, no invented bases. [DOC]

## 5. Governance invariants
Single brand per output; no client PII in deliverables; never present a green
script as proof of correctness; never invent prices or live-market claims; stop
and ask rather than auto-fill a critical gap. [DOC]
