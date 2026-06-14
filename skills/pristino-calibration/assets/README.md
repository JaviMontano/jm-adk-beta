# Assets — pristino-calibration

The `assets/` bundle defines the **local deterministic contract** for this skill:
the persona/mode output shapes, the precedence chain, the evidence-tag family, and
the gate dimensions the guardian enforces. These files are data, not prose — they
let the lead and guardian agree, byte-for-byte, on what a "mode-correct,
gate-passing" output looks like.

## Files

| File | Type | Used by | What it pins down |
|------|------|---------|-------------------|
| `quality-rubric.json` | rubric | `agents/guardian.md`, `templates/output.md`, `SKILL.md` | The gate dimensions (persona_line, mode_shape, optimizer_sections, canvas_contract, evidence, precedence_order, delegate_agents_known, guardian_block, degraded_self_calibration, no_green_as_success, single_brand). Maps 1:1 to `evals/evals.json` `expected_checks`. |
| `mode-shape.json` | lookup | `agents/lead.md`, `knowledge/body-of-knowledge.md`, `SKILL.md` | The MODE(+COMPLEXITY) → output shape table: which modes carry a persona line, which optimizer sections, and whether the Canvas contract appears. |
| `manifest.json` | manifest | (this README) | Declares the bundle for the DoD validator; every `used_by` target exists. |

## Conventions

- Evidence family is **Alfa core**: `[CODE] [CONFIG] [DOC] [INFERENCE]
  [ASSUMPTION]` — one family per output.
- Precedence is fixed: **Veracidad > Seguridad > Objetivo > Formato > Estilo**.
- Single-brand (JM Labs); no invented prices; no client PII.
- Edit the registry of record at `references/ontology/personas.json`, then run
  `python3 scripts/validate-personas.py`. These assets describe the *contract
  shape*, not the persona list.
