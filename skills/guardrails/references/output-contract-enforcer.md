<!-- distilled from alfa skills/output-contract-enforcer -->
<!-- Validate generated outputs against declared contracts for format, required sections, required fields, evidence tags, naming conventions, machine-readable validation packets, and repair suggestions. Use after a skill produces an output, before gate evaluation, when `/jm:verify` is invoked, or when the user asks to validate an artifact against its output contract. [EXPLICIT] -->
# Output Contract Enforcer

Post-execution validator for generated artifacts. It checks that an output matches the contract it claims to satisfy, then returns a deterministic pass/fail packet with exact violations and repairs. It is a verifier, not an author: it never edits, renames, or regenerates the artifact — it only reports. [EXPLICIT]

## When to Activate

Activate when:

- A skill output needs validation before delivery or gate evaluation.
- The user invokes `/jm:verify`.
- The user asks whether an artifact matches a declared contract, schema, template, required section list, evidence-tag rule, or naming convention.
- An orchestrator needs a post-run blocker before merge, publish, or handoff.

Do not activate (anti-scope) when the user only asks to design a JSON schema, format a new response, explain output contracts conceptually, or create a fresh artifact. Route those to the owning creation or design skill unless validation of an existing output is explicitly requested. This guard runs *after* generation; using it as an authoring tool produces no contract to validate against and returns `blocked`. [INFERENCIA]

## Required Inputs

- Contract source: skill `SKILL.md`, `templates/schema.json`, JSON contract, or explicit required fields.
- Generated output: file path or pasted output.
- Output type: markdown, json, html, docx-report, or unknown.
- Required sections or required fields.
- Evidence policy: whether evidence tags are required and which vocabulary is allowed.
- Naming policy: target file path and expected style when file output is involved.

If a required input is missing, return `status: blocked` and list the missing input. Do not guess a contract. Rationale: a guessed contract can pass a non-conforming artifact (false `pass`), which is worse than refusing — a blocked verdict is recoverable, a false pass is not. [INFERENCIA]

Precedence when sources conflict: explicit user-supplied required fields override `templates/schema.json`, which overrides `SKILL.md` prose. Record which source won in `contract_id`. [SUPUESTO]

## Deterministic Contract

- Validate only against declared contract evidence, never against unstated preferences or taste. A check with no declared expectation is omitted, not failed. [EXPLICIT]
- Use one evidence-tag vocabulary: `[CÓDIGO]`, `[CONFIG]`, `[DOC]`, `[INFERENCIA]`, `[SUPUESTO]`. Mixing two tag families in one artifact is itself an `evidence_tags` failure. [EXPLICIT]
- Quick mode still enforces mandatory evidence tags. No mode skips a mandatory check; modes only widen optional coverage. [EXPLICIT]
- Do not auto-rename files. Suggest the corrected name. Rationale: renaming can break inbound references (routes, links, imports) the validator cannot see, so the human owns that edit. [INFERENCIA]
- Do not mark pass if any required section, field, evidence tag, format, or naming check fails.
- Report every violation with path, check id, expected value, observed value, and repair. Aggregate all violations in one pass — never stop at the first. [EXPLICIT]
- Same input must yield the same packet: no clock, network, model-provider call, or random value in the verdict. [EXPLICIT]
- For machine-readable validation, use `templates/schema.json`.
- Use `scripts/validate_output_contract.py` for deterministic fixture-backed checks.

## Assets And Scripts

- `assets/output-contract-checklist.md` - validation checklist.
- `assets/contract-rules.json` - canonical checks, statuses, formats, and evidence tags.
- `assets/evidence-tag-policy.json` - allowed evidence tags and failure behavior.
- `assets/markdown-section-contract.json` - default report section contract.
- `templates/schema.json` - validation packet schema.
- `scripts/validate_output_contract.py` - local validator for fixture-backed output checks.

If a referenced asset is absent, the dependent check returns `blocked` (cannot load its rule), not `pass`. [INFERENCIA]

## Validation Process

1. Load the declared contract.
2. Normalize the output type and output path.
3. Run checks in this order: existence, format, required sections or fields, evidence tags, naming, and packet shape. Order is a dependency chain — a later check cannot pass if an earlier one blocked (e.g. `markdown_sections` is meaningless on a file that does not exist or is not markdown). [INFERENCIA]
4. Emit `status: pass` only when every required check passes.
5. Emit `status: fail` when the output exists but violates the contract.
6. Emit `status: blocked` when the contract or output is missing.
7. Include deterministic repairs for each violation.

`fail` vs `blocked` distinction: `fail` means "I checked and it is wrong" (artifact is the problem); `blocked` means "I could not check" (contract or input is the problem). Downstream gates treat both as non-pass but route them differently — `fail` to the author, `blocked` to whoever owns the contract. [INFERENCIA]

## Validation Packet

Return a Markdown report or JSON packet with:

```json
{
  "schema": 1,
  "skill": "output-contract-enforcer",
  "status": "pass|fail|blocked",
  "contract_id": "contract identifier",
  "artifact": "path or inline artifact label",
  "checks": [
    {
      "id": "markdown_sections",
      "status": "pass|fail|blocked",
      "expected": "declared expectation",
      "observed": "observed output",
      "repair": "deterministic repair"
    }
  ],
  "violations": [],
  "repair_suggestions": [],
  "evidence": []
}
```

The packet is itself a contracted artifact: it must validate against `templates/schema.json`, so the enforcer is expected to pass its own `machine_readable_packet` check (self-application). [INFERENCIA]

## Required Checks

| Check | Pass Condition | Failure |
|---|---|---|
| `contract_loaded` | Contract source is present and parseable. | `blocked`. |
| `format` | Output type matches declared type. | `fail`. |
| `markdown_sections` | Every required section heading exists exactly once or as allowed by contract. | `fail`. |
| `json_schema` | JSON parses and required fields exist. | `fail`. |
| `evidence_tags` | Required evidence tags are present and use allowed vocabulary. | `fail`. |
| `naming` | File name matches declared convention. | `fail` with suggestion, never rename. |
| `machine_readable_packet` | Packet follows `templates/schema.json`. | `fail`. |

## Edge Cases And Failure Modes

| Case | Verdict | Why |
|---|---|---|
| Output file exists but is empty (0 bytes). | `fail` (`format`). | Existence passed; it cannot satisfy any section/field contract. [INFERENCIA] |
| Output is valid JSON but declared type was markdown. | `fail` (`format`). | Parseable in the wrong language is still a format mismatch; do not "accept because it parses." [EXPLICIT] |
| JSON is malformed / unparseable. | `fail` (`json_schema`), not `blocked`. | The artifact is present and wrong; `blocked` is reserved for missing contract/input. [INFERENCIA] |
| A required heading appears twice. | `fail` (`markdown_sections`). | Contract is "exactly once or as allowed"; duplicates break deterministic extraction. [EXPLICIT] |
| Required heading present but renamed/abbreviated. | `fail` with rename repair. | Heading text is the contract key; near-misses are not matches. [INFERENCIA] |
| Two evidence-tag families mixed in one artifact. | `fail` (`evidence_tags`). | Single-family rule; pick the family by audience, never mix. [EXPLICIT] |
| Evidence required, zero tags present. | `fail` (`evidence_tags`). | Absence is a violation, not silent pass. [EXPLICIT] |
| Naming policy declared, no output path given. | `naming` omitted (inline artifact). | Cannot check a file name that does not exist. [INFERENCIA] |
| Contract present, output path missing. | `blocked`. | Nothing to validate. [EXPLICIT] |
| Referenced asset/script missing. | `blocked` on its check. | Rule unloadable ≠ artifact wrong. [INFERENCIA] |

Anti-pattern to avoid: emitting `pass` with an empty `checks` array. A pass with no checks run is indistinguishable from "I did nothing"; require at least `contract_loaded` + one content check before any `pass`. [INFERENCIA]

## Worked Example

Contract: markdown report, sections `# Summary`, `# Findings`; evidence tags required (Alfa set). Artifact has `# Summary`, `# Finding` (typo), one `[DOC]` tag.

```json
{
  "schema": 1, "skill": "output-contract-enforcer", "status": "fail",
  "contract_id": "markdown-section-contract.json",
  "artifact": "out/report.md",
  "checks": [
    {"id": "contract_loaded", "status": "pass", "expected": "section+tag contract", "observed": "loaded", "repair": ""},
    {"id": "format", "status": "pass", "expected": "markdown", "observed": "markdown", "repair": ""},
    {"id": "markdown_sections", "status": "fail", "expected": "# Findings", "observed": "# Finding", "repair": "rename heading '# Finding' to '# Findings'"},
    {"id": "evidence_tags", "status": "pass", "expected": "Alfa set, single family", "observed": "[DOC]", "repair": ""}
  ],
  "violations": ["markdown_sections: missing '# Findings'"],
  "repair_suggestions": ["rename '# Finding' to '# Findings'"]
}
```

Verdict is `fail` (not `blocked`): the artifact exists and is checkable; one section heading does not match. [INFERENCIA]

## Output Template

```markdown
# Output Contract Validation

status: pass|fail|blocked
contract_id: <id>
artifact: <path or label>

## Checks

| Check | Status | Expected | Observed | Repair |
|---|---|---|---|---|

## Violations

- None, or exact violation records.

## Evidence

- [CÓDIGO] File and command evidence.

## Repair Suggestions

- Deterministic next edits.
```

## Validation Gate

Before marking pass:

- Contract is loaded from explicit evidence.
- Required sections or fields are checked.
- Evidence-tag policy is enforced (present, allowed vocabulary, single family).
- Naming policy is checked when an output path exists.
- The verdict is fail when any mandatory check fails; blocked when any input is missing.
- Repairs are specific and actionable (exact target + exact edit, not "fix the heading").
- The validation packet itself matches `templates/schema.json`.
- At least `contract_loaded` and one content check ran — never `pass` on an empty `checks` array.

## Acceptance Criteria

- [ ] Same input yields byte-identical packet across runs (deterministic). [EXPLICIT]
- [ ] Every violation carries path, check id, expected, observed, and repair. [EXPLICIT]
- [ ] All violations aggregated; run does not stop at the first failure. [EXPLICIT]
- [ ] No `pass` while any required check is `fail` or `blocked`. [EXPLICIT]
- [ ] No file was renamed or rewritten by the validator. [EXPLICIT]
- [ ] Evidence tags belong to one family from the allowed vocabulary. [EXPLICIT]
- [ ] Emitted packet validates against `templates/schema.json`. [EXPLICIT]
