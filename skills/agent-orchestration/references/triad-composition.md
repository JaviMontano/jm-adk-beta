<!-- distilled from alfa skills/triad-composition -->
<!-- Select a deterministic Lead + Support + Guardian triad from the PRISTINO composition matrix using domain classification, confidence thresholds, stable tie-breakers, execution-mode routing, degraded-mode policy, and Guardian validation. Use when the user or orchestrator asks for triad composition, agent role selection, Lead/Support/Guardian routing, Pristino orchestration, domain-to-agent mapping, committee escalation, or quality-gated multiagent execution planning. -->
# Triad Composition

## When to Activate

Activate when the user or orchestrator needs to select Lead, Support, and Guardian roles for a non-trivial task, route a request through PRISTINO orchestration, classify a task domain, choose between triad vs committee execution, or explain degraded-mode behavior when an agent role fails. [EXPLICIT]

Do not activate for unrelated uses of the word "triad" such as music theory, chemistry, or generic three-item lists unless the request also mentions Pristino, orchestration, agents, or Lead/Support/Guardian routing. [EXPLICIT]

## Deterministic Assets

Load these before composing a triad:

- `assets/composition-matrix.json`: canonical domain -> Lead/Support/Guardian matrix.
- `assets/classification-policy.json`: confidence bands, execution modes, and stable tie-breakers.
- `assets/degraded-mode-policy.json`: explicit partial-delivery rules.
- `assets/triad-output-contract.json`: required output sections and blocked phrases.

Validate packet examples with:

```bash
bash skills/triad-composition/scripts/check.sh
python3 -B skills/triad-composition/scripts/validate_triad_packet.py --contract skills/triad-composition/assets/triad-output-contract.json --packet <packet.md> --scenario requirements
```

## Inputs

Require these before auto-selecting:

| Input | Required | Handling |
|---|---:|---|
| Goal | Yes | Ask if missing. |
| Context | Yes | Ask if missing or infer only with `[INFERRED]`. |
| Constraints | Yes | Ask if safety, brand, runtime, deadline, or quality constraints are unknown. |
| Definition of done | Yes | Ask if success criteria are absent. |
| Match confidence | Optional | If absent, calculate from exact phrase matches, keyword hits, and domain order. |

Do not apply defaults for missing Goal, Context, Constraints, or Definition of done. [EXPLICIT]

## Classification Policy

Apply confidence bands exactly. Bands are inclusive at the lower bound: `0.85` auto-selects; `0.84` presents options; `0.60` presents options; `0.59` asks to clarify. [EXPLICIT]

| Confidence | Action |
|---:|---|
| `>=0.85` | Auto-select skill, compose triad, execute sequentially. |
| `0.60-0.84` | Present top 3 domain options and ask user to choose. |
| `<0.60` | Ask one clarifying question before matching again. |

Use stable tie-breakers in this order: exact domain phrase match, highest keyword hit count, highest confidence score, earliest domain order in `composition-matrix.json`. The earliest-order tie-breaker is final and guarantees determinism: two identical requests always yield the same triad. [EXPLICIT]

Confidence is computed, not asserted by the user-supplied `Match confidence`; when both exist and disagree by `>=0.15`, recompute and prefer the deterministic score, flagging the gap. [INFERRED] Anti-scope: this policy never selects a triad below `0.85` — the `0.60-0.84` band always defers to the user, so do not auto-execute "the top option" to save a turn. [EXPLICIT]

## Execution Mode

| Mode | Use when | Output |
|---|---|---|
| Single | Trivial question, clarification, or lookup. | Direct answer; no triad packet required. |
| Triad | Non-trivial analysis, design, implementation, or review. | Lead -> Support -> Guardian sequence. |
| Committee | Critical cross-cutting decision. | Up to 5 agents with Pristino tiebreaker; document why triad is insufficient. |

Critical scopes include production data retention, security policy, compliance, legal risk, enterprise governance, or decisions spanning four or more domains. [INFERRED]

Mode is chosen before scoring domains, not after: a trivial lookup that happens to match a domain at `>=0.85` still resolves as Single, because the triad packet adds no value to a one-fact answer. [EXPLICIT] Committee is the exception, not the default — it costs up to 5 agents and a tiebreaker pass, so each escalation must document, in one line, why a Lead+Support+Guardian triad cannot own the decision. [EXPLICIT] Worked example: "Choose retention period for prod PII across EU + US, billing, and audit" spans four domains and a compliance scope, so it routes to Committee; "Which agent reviews a single Terraform diff?" is Triad (one domain, non-trivial); "What is the default G2 gate?" is Single. [INFERRED]

## Composition Procedure

1. Normalize the request without correcting the user's language. [EXPLICIT]
2. Extract domain signals and required inputs. [EXPLICIT]
3. Score matrix domains from `assets/composition-matrix.json` using deterministic keyword hits and explicit user terms. [EXPLICIT]
4. Apply the confidence band and tie-breakers from `assets/classification-policy.json`. [EXPLICIT]
5. If confidence is `>=0.85`, return the selected Lead, Support, Guardian, execution mode, and G0-G3 gates. [EXPLICIT]
6. If confidence is `0.60-0.84`, return top 3 domain options and ask for a choice; do not execute. [EXPLICIT]
7. If confidence is `<0.60`, ask for missing Goal, Context, Constraints, and Definition of done; do not invent a triad. [EXPLICIT]
8. If any triad member fails, apply `assets/degraded-mode-policy.json` and mark output `[PARTIAL]`. [EXPLICIT]

Failure modes to guard: a domain that scores `>=0.85` against two matrix rows simultaneously — resolve with the tie-breaker chain, never average the two triads. [EXPLICIT] A request whose required inputs are present but whose domain scores `<0.60` — ask for domain disambiguation, not for the already-supplied inputs. [INFERRED] A Guardian that maps to the same agent as the Lead — keep both roles distinct in the packet; if the matrix forces overlap, the Guardian still runs as a separate pass with the validation-gate checklist, never folded into the Lead's output. [INFERRED]

## Output Contract

Use this packet shape:

```markdown
# Triad Composition Packet

# Input Classification

# Selected Triad

# Execution Mode

# Validation Gates

# Risks and Assumptions
```

Every role selection must name the matrix domain, confidence band, Lead, Support, Guardian, and evidence tag. [EXPLICIT] Headings are fixed anchors — do not rename, reorder, or merge them; downstream validation (`validate_triad_packet.py`) matches on these exact section titles. [EXPLICIT] Worked minimal packet:

```markdown
# Triad Composition Packet
# Input Classification
domain: requirements (0.91, band >=0.85) [DOC]
# Selected Triad
Lead: requirements-analyst | Support: domain-modeler | Guardian: spec-reviewer
# Execution Mode
Triad (non-trivial design)
# Validation Gates
G0 inputs, G1 draft, G2 review, G3 sign-off
# Risks and Assumptions
[SUPUESTO] EU-only scope assumed; confirm before G3.
```

Blocked phrases (see `triad-output-contract.json`): never assert a gate "passed" with success language before the Guardian pass runs; report gate state, not a verdict. [EXPLICIT]

## Validation Gate

- [ ] Required inputs are present or explicitly requested with `[OPEN]`.
- [ ] Domain selection cites a matrix row or presents top 3 options.
- [ ] Guardian is always selected for triad or committee mode.
- [ ] Confidence band action matches the threshold policy.
- [ ] No unrelated false-positive use of "triad" activates orchestration.
- [ ] G0-G3 quality gates are named before delivery.
- [ ] Degraded mode is marked `[PARTIAL]` and names the failed role.

## Edge Cases

| Scenario | Handling |
|---|---|
| Minimal input | Ask for Goal, Context, Constraints, and Definition of done. |
| Two close domains | Present top 3 options and ask user to choose. |
| Critical cross-domain decision | Escalate to committee, max 5 agents. |
| Guardian unavailable | Deliver only with `[PARTIAL]` and manual-review warning. |
| False positive "triad" | Route away and do not return orchestration agents. |
| Runtime lacks subagent tools | Apply Lead, Support, and Guardian perspectives sequentially in one response. |
| User asserts a confidence that disagrees with computed score | Recompute; prefer deterministic score; flag the `>=0.15` gap. |
| Three-way domain tie | Run full tie-breaker chain; if still tied, earliest matrix order wins (final). |
| Guardian = Lead in matrix | Run Guardian as a separate validation pass; never fold into Lead output. |
| Critical scope but inputs missing | Stop for inputs first; do not escalate to committee on incomplete data. |

## Related Canon

- `PRISTINO.md`: source for triad pattern, matrix, confidence bands, degraded mode, Constitution XIII/XIV/XVI, and G0-G3 gates. [DOC]
- `AGENTS.md`: runtime bridge exposing the triad pattern for Codex-compatible execution. [DOC]
