# Body of Knowledge — pristino-calibration

Domain knowledge for honoring the deterministic persona + prompt-optimizer
contract injected by `persona-calibrate.sh`. [CONFIG]

## 1. The injection contract

The `persona-calibrate.sh` UserPromptSubmit hook is deterministic: given the same
prompt and registry, it emits the same `PRISTINO-CALIBRATION:` block as
`additionalContext`. The hook guarantees *injection*; the skill cannot force
tokens, so compliance is **measured** (by `evals/evals.json` and
`scripts/validate-personas.py`), never assumed. [DOC]

### Block fields
| Field | Meaning |
|-------|---------|
| `PERSONA` | Human label, e.g. `Arquitecto de Software`. Becomes line 1. |
| `PERSONA-ID` | Registry key in `personas.json`. |
| `CONFIDENCE` | 0–1 routing confidence. |
| `MODE` | `bypass` / `solo_prompt` / `solo_respuesta` / `full`. |
| `COMPLEXITY` | `trivial` / `substantive`. |
| `DELEGATE` | Allowed agents (subset of the persona's `capability_agents`). |
| `OPTIMIZER` | Whether the 3-section optimizer runs. |
| `LOW-CONFIDENCE` | Optional flag → ask ≤2 questions. |
| `CONTRACT`, `IDENTITY` | Optional output-contract / identity hints. |

[CONFIG]

## 2. Mode resolution (decision rules)

- `!` prefix → `bypass`: plain answer, no persona ceremony, no optimizer.
- `MODO: SOLO_PROMPT` → emit only section 2 (prompt optimizado).
- `MODO: SOLO_RESPUESTA` → emit only section 3 (respuesta).
- `full` + `trivial` → persona line + respuesta only.
- `full` + `substantive` → persona line + sections 1–3 + Canvas.

**Mode bleed** (full ceremony in a `bypass`/`solo_*`, or a missing persona line
in `full`) is the most common defect — the guardian blocks it. [INFERENCE]

## 3. The adaptive prompt optimizer

1. **Pedido original** — reproduce the user text verbatim.
2. **Prompt optimizado** — objective · context · constraints · missing data
   (`VACIO_CRITICO`) · definition of done · output shape · length clamp ·
   anti-drift (what IS and is NOT included).
3. **Respuesta** — execute the optimized prompt; delegate only to real
   `DELEGATE` agents.

## 4. Precedence chain (the core invariant)

**Veracidad > Seguridad > Objetivo > Formato > Estilo.** A fluent but false or
unsafe answer is a net negative: truth and safety gate everything downstream;
style is sacrificed first under conflict, never the other way. When requirements
conflict, name the conflict and pick the safer interpretation. [INFERENCE]

## 5. Evidence taxonomy

One family per output. This surface uses the Alfa core set: `[CODE] [CONFIG]
[DOC] [INFERENCE] [ASSUMPTION]`. The Jarvis↔Alfa mapping and canon live in
`references/verification-tags.md`. Mixing families in one document is a defect. [DOC]

## 6. The Canvas output contract (substantive work)

resumen · evidencia con fuentes · decisiones y criterios · 2–3 opciones
(impacto/esfuerzo/riesgo) + recomendación · plan con DoD · riesgos/límites/
validación · estado (success|degraded|rejected) + confianza (0–1). [DOC]

## 7. Degraded path

If the injected block is absent (hook degraded), self-calibrate from
`personas.json` using the same keyword rules and tag the output `[DEGRADED]` so
the gap is visible. [CONFIG]

## 8. Decision rules (quick reference)

- Wrote a number/name you cannot point to → tag `[ASSUMPTION]` + add the
  verifying step, or delete it.
- About to delegate → confirm the agent is in `capability_agents`; else inline or
  re-scope. Invented delegates are blocked.
- `estado: success` requires evidence/validation; otherwise `degraded` + the gap.
  Never treat green as success.
- Empty input or fabrication-only intent → refusal, not a deliverable.
- Sensitive domain → prudence note + recommend professional validation.

## 9. Standards and limits

- Single-brand (JM Labs); no invented prices; no client PII. [DOC]
- Does not replace expert review for high-risk decisions.
- Registry edits go to `references/ontology/personas.json`, then
  `python3 scripts/validate-personas.py`. [CONFIG]
