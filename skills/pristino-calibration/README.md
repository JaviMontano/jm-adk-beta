# pristino-calibration

Honors the deterministic persona + prompt-optimizer contract injected by the
`persona-calibrate.sh` UserPromptSubmit hook. When the hook emits a
`PRISTINO-CALIBRATION:` `additionalContext` block — or a trigger keyword appears
and persona/mode shaping is expected — this skill reads the signals and executes
the contract instead of answering plainly. [CONFIG]

## What it does

- Declares the resolved **persona** on line 1 (except `bypass`).
- Resolves the `MODE` (`bypass` / `solo_prompt` / `solo_respuesta` / `full`) and
  `COMPLEXITY` (`trivial` / `substantive`) to pick the exact output shape.
- Runs the adaptive **prompt optimizer**: (1) pedido original, (2) prompt
  optimizado, (3) respuesta.
- Applies precedence **Veracidad > Seguridad > Objetivo > Formato > Estilo** at
  all times and names the trade-off under conflict.
- Tags non-obvious claims from ONE evidence family and declares confidence
  (0–1).
- Consolidates substantive work in the **Canvas output contract**.

## When to use

- The injected `PRISTINO-CALIBRATION:` block is present.
- A trigger keyword (`persona`, `calibrar`, `calibrate`, `optimizar prompt`,
  `prompt optimizer`, `rol`, `auto-calibracion`) appears.

Do **not** activate on empty/whitespace input or fabrication-only intent — the
guardian returns a refusal, not a deliverable.

## How it routes / executes

1. **Discover** — read the injected block; if absent, self-calibrate from the
   persona registry and tag `[DEGRADED]`.
2. **Analyze** — resolve `MODE` + `COMPLEXITY`; if `LOW-CONFIDENCE`, ask at most
   2 clarifying questions, else state 2 tagged assumptions.
3. **Execute** — emit the optimizer sections required by the mode; delegate heavy
   work only to the persona's real `DELEGATE` agents.
4. **Validate** — silent acceptance gate; the eight checks map 1:1 to
   `evals/evals.json` `expected_checks`.

## References

- Persona registry of record: `references/ontology/personas.json` [CONFIG]
- Full spec: `references/ontology/persona-protocol.md`
- Evidence-tag canon + Jarvis↔Alfa mapping: `references/verification-tags.md`
- Deterministic contract assets: `assets/` (see `assets/README.md`)
- Role contracts: `agents/lead.md`, `agents/specialist.md`,
  `agents/support.md`, `agents/guardian.md`
- Domain knowledge: `knowledge/body-of-knowledge.md`,
  `knowledge/knowledge-graph.json`
- Prompts: `prompts/primary.md`, `prompts/meta.md`,
  `prompts/variations/quick.md`, `prompts/variations/deep.md`
- Deliverable scaffold: `templates/output.md`
- Worked example: `examples/example-input.md`, `examples/example-output.md`

## Evidence tags

One family per output. This surface uses the Alfa core set:
`[CODE] [CONFIG] [DOC] [INFERENCE] [ASSUMPTION]`. [DOC]
