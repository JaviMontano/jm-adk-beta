<!-- distilled from alfa skills/cv-cover-optimizer -->
<!-- Optimiza CV y carta de presentacion para ATS, rol objetivo y voz de marca con lint offline de keywords, secciones, longitud, contacto y tono. -->
# Cv Cover Optimizer

## Purpose

Improve a CV, resume, cover letter, or application packet against a target role: ATS-aware edits, coverage gaps, brand-voice guardrails, and a deterministic validation result — without inventing credentials. [DOC]

**Scope.** Edits *existing* text to a *known* role. **Anti-scope:** does not write a CV from zero, generate a portfolio/LinkedIn profile, run career coaching with no artifact, or judge candidate fitness for the role. Route those elsewhere (see Related Skills). [INFERENCIA]

**Tagging.** Kit-facing file → Alfa core set only (`[DOC]` `[CÓDIGO]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]`); never mix the Jarvis set. Canon: `references/verification-tags.md`. [DOC]

## Inputs Expected

- Candidate CV or cover text. **Required** — absent → `[SUPUESTO]` stop, ask. [DOC]
- Target role / company / job description / required keywords. **Required for ATS scoring**; without it only structure/PII checks run. [INFERENCIA]
- Language preference and brand-voice constraints. Default: language of the source text; default voice = neutral-professional if unstated. [SUPUESTO]
- Permission boundary: direct file edit vs proposed copy only. Default = **proposed copy** (see Update-Safety). [CONFIG]

## Outputs Expected

- Optimized CV or cover sections (only those requested). [DOC]
- ATS keyword coverage summary: matched / missing / density-risk. [DOC]
- Missing section / contact / length issues. [DOC]
- Brand-voice risks: stacked trademarks, hustle framing, generic flattery. [DOC]
- Validation evidence from `scripts/ats_lint.py` when a machine-readable packet is supplied. [CÓDIGO]

## Procedure

### Discover

Identify target role, source type (`cv` or `cover`), required keywords, language, and edit-vs-propose intent. Missing role evidence is an assumption, not a blocker for structure-only review — mark it. [INFERENCIA]

### Analyze

Compare source text against `assets/ats-keyword-policy.json`, `assets/document-section-policy.json`, `assets/brand-voice-policy.json`, and `assets/privacy-policy.json`. Policies are the single source of truth — do not hard-code thresholds in prose. [CONFIG]

### Execute

Rewrite **only** requested sections. Preserve facts, seniority, dates, employers, credentials, contact details. Never invent metrics; emit suggested metrics as visibly marked placeholders (e.g. `[MÉTRICA: confirmar]`). [DOC]
**Decision — keywords vs honesty:** if a required keyword has no basis in the source, surface it as a *gap to validate*, never inject it. Trade-off: lower raw ATS score, zero fabrication risk — the right call, since a flagged fabrication fails the screen harder than a missing term. [INFERENCIA]

### Validate

```bash
bash skills/cv-cover-optimizer/scripts/check.sh
```

For a specific packet:

```bash
python3 skills/cv-cover-optimizer/scripts/ats_lint.py --input <packet.json>
```

`check.sh` runs valid + invalid fixtures offline (no network, deterministic). Exit `0` = pass; non-zero = at least one rule violated — report which, do not mark the packet clean. [CÓDIGO]

## Assets

- `assets/ats-keyword-policy.json` — keyword set, match rules, density ceiling.
- `assets/document-section-policy.json` — required/optional sections per `cv`|`cover`.
- `assets/brand-voice-policy.json` — banned framings, trademark-stacking rule.
- `assets/privacy-policy.json` — PII exposure limits for examples/fixtures.
- `assets/output-contract.json` — shape the lint and the response must satisfy. [CONFIG]

## Output Contract

Conform to `assets/output-contract.json`. A response/lint result minimally carries: `doc_type` (`cv`|`cover`), `ats.matched[]` / `ats.missing[]` / `ats.density_flags[]`, `sections.missing[]`, `length.status`, `contact.status`, `voice.risks[]`, and `verdict` (`pass`|`partial`|`blocked`). `blocked` requires a stated reason and the next step to unblock. [CÓDIGO]

## Quality Criteria

- Recommendations grounded in source text + role evidence; each substantive one cites its source. [DOC]
- ATS gaps name missing keywords without stuffing (respect density ceiling). [CONFIG]
- CV output keeps recognizable experience / education / skills / achievement sections. [DOC]
- Cover output stays concise; no generic flattery. [DOC]
- Contact/PII handling explicit and privacy-safe. [CONFIG]
- No invented candidate experience. [DOC]

## Edge Cases

- **No job description:** structure + PII review only; verdict `partial`; ask for role evidence. [DOC]
- **Minimal CV:** fix structure and name missing data; do not fabricate content. [DOC]
- **Conflicting brand tone:** keep user preference; mark unresolved conflict, do not silently pick. [INFERENCIA]
- **Sensitive PII:** never echo real contact details in examples/fixtures; redact. [CONFIG]
- **Over-length cover:** keep evidence-backed value, cut repetition; flag if still over after trimming. [DOC]
- **Non-Latin / mixed-language source:** lint on the declared language; if undetectable, mark `[SUPUESTO]` and ask before scoring keywords. [SUPUESTO]
- **Keyword-stuffed source:** flag density violation as a *risk to fix*, not a strength. [INFERENCIA]

## Failure Modes (anti-patterns)

- Injecting required keywords with no source basis → fabrication; forbidden. [DOC]
- Treating lint exit `0` as "good CV" — it means "rules passed", not "competitive". [INFERENCIA]
- Editing the source file under default (propose-only) authority. [CONFIG]
- Rewriting sections the user did not request ("helpful" scope creep). [DOC]
- Emitting `pass` while a placeholder metric is still unconfirmed → must be `partial`. [INFERENCIA]

## Worked Example

Source bullet: *"Responsible for the sales team."* Role keywords: `revenue`, `quota`, `leadership`.
Rewrite: *"Led a 6-person sales team to [MÉTRICA: % quota attainment — confirmar], owning regional revenue targets."*
Lint result: `ats.matched=[leadership, revenue]`, `ats.missing=[quota]` (no source basis → surfaced as gap, not injected), `voice.risks=[]`, `verdict=partial` (placeholder unconfirmed). [INFERENCIA]

## Scripts

`scripts/ats_lint.py --input <json>` lints CV/cover packets for ATS keyword coverage, section presence, length, contact, stacked trademarks, and hustle language. `scripts/check.sh` runs deterministic valid + invalid fixtures offline. Both are pure-stdlib, network-free, and the only execution surface. [CÓDIGO]

## Related Skills

- `cv-transformer`
- `brand-voice`
- `gratitud-post-proceso`

## Evidence Requirements

- Cite source document, job description, or user constraint for every substantive recommendation. [DOC]
- Mark inferred gaps as assumptions when role evidence is incomplete; pair each `[SUPUESTO]` with the step that would confirm it. [DOC]

## Update-Safety Notes

- Default to proposed copy unless file-edit authority is explicit. [CONFIG]
- Never overwrite the source CV/cover without explicit confirmation. [DOC]
- Keep placeholders visibly marked until the user confirms the metric/detail. [DOC]
