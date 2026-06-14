# Brand-Output Routing & Delivery Record

> Fill every field. This is the handoff record from router → playbook → gate.

## 1. Request
- **Raw request:** <what the user asked for>
- **Content/data source:** <inline | file path | structured JSON>
- **Target format:** <HTML | DOCX | XLSX | spec | slides | folio>
- **Brand system:** <MetodologIA DS | MetodologIA | fallback config>
- **artifact_date (caller-supplied):** <YYYY-MM-DD | omitted>
- **depth:** <quick | deep>

## 2. Routing decision
- **Chosen topic:** <one of the 8 enums>
- **Playbook loaded:** `references/<topic>.md`
- **Disambiguating signal:** <why this topic, tagged [INFERENCIA]/[EXPLICIT]>
- **Rejected candidates:** <topic — reason rejected>
- **Asked a clarifying question?** <no | the question + answer>

## 3. Token resolution
- **Config source (first match):** <arg path | ./brand-config.json | references/brand | fallback>
- **Inherited keys (recorded as [SUPUESTO]):** <list | none>
- **Brand-mix check:** single brand confirmed <yes/no>

## 4. Generation
- **Script invoked:** <e.g. scripts/render-folio-html.py --data … | compile-xlsx-template.py …>
- **Artifact path / block:** <path or "fenced html block below">
- **Folio reserved (if any):** <PREFIX-YYYY-NNN | n/a> — dry-run then apply: <yes/no>

## 5. Validation gate (mark only verified boxes)
- [ ] Exactly one playbook loaded; topic matches artifact. [EXPLICIT]
- [ ] DS tokens from config; no hardcoded brand values outside :root/token files. [CONFIG]
- [ ] Determinism honored (no clock/remote/random). [INFERENCIA]
- [ ] Script-first generation (not hand-edited). [EXPLICIT]
- [ ] Format-specific checklist passed (per playbook). [CÓDIGO]
- [ ] Evidence tags present; single Alfa family; no invented prices; no PII. [DOC]
- **check.sh / compile result:** <pass | fail + finding>

## 6. Outcome
- **Status:** <delivered | blocked: {VACIO_CRITICO} | re-routed>
- **Open findings / limitations:** <e.g. contrast indeterminate → browser QA [SUPUESTO]>
